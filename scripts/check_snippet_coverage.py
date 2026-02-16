"""
Validate that snippets have valid syntax, working imports, and reference existing SDK methods by executing them until the first outbound API call.
"""
import argparse
import os
import sys
from pathlib import Path
from unittest.mock import patch

for var in [
    "SINCH_PROJECT_ID", "SINCH_KEY_ID", "SINCH_KEY_SECRET",
    "SINCH_SMS_REGION", "SINCH_CONVERSATION_REGION",
    "SINCH_PHONE_NUMBER", "SINCH_SERVICE_PLAN_ID",
]:
    os.environ.setdefault(var, "test")


class SnippetValidationComplete(Exception):
    """Raised when snippet successfully reaches first API call."""


def validate_snippet(snippet_path: Path, quiet: bool = True) -> tuple[bool, str]:
    """Run snippet; success when it reaches the first API call."""
    def mock_request(self, endpoint):
        raise SnippetValidationComplete()

    try:
        with patch(
            "sinch.core.adapters.requests_http_transport.HTTPTransportRequests.request",
            mock_request,
        ):
            with open(snippet_path) as f:
                source = f.read()
            if quiet:
                with open(os.devnull, "w") as devnull:
                    old_stdout, old_stderr = sys.stdout, sys.stderr
                    sys.stdout, sys.stderr = devnull, devnull
                    try:
                        exec(source, {"__name__": "__main__"})
                    finally:
                        sys.stdout, sys.stderr = old_stdout, old_stderr
            else:
                exec(source, {"__name__": "__main__"})
        return False, "Snippet ran without making API call"
    except SnippetValidationComplete:
        return True, ""
    except ModuleNotFoundError as e:
        return False, f"Broken import: {e}"
    except ImportError as e:
        return False, f"Broken import: {e}"
    except AttributeError as e:
        return False, f"Method/attribute does not exist: {e}"
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def main():
    parser = argparse.ArgumentParser(
        description="Validate snippets (imports, syntax, SDK method names)"
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Only print failures")
    args = parser.parse_args()

    root = Path(__file__).parent.parent
    os.chdir(root)

    snippets_dir = root / "examples" / "snippets"
    if not snippets_dir.exists():
        print("ERROR: examples/snippets directory not found")
        return 1

    snippet_files = list(snippets_dir.rglob("snippet.py"))
    if not snippet_files:
        print("ERROR: No snippet.py files found")
        return 1

    failed = []
    for snippet_path in sorted(snippet_files):
        rel_path = snippet_path.relative_to(root)
        success, error = validate_snippet(snippet_path, quiet=args.quiet)
        if success:
            if not args.quiet:
                print(f"  OK  {rel_path}")
        else:
            print(f"  FAIL {rel_path}\n       {error}")
            failed.append((rel_path, error))

    if failed:
        print(f"\n{len(failed)} snippet(s) failed validation:")
        for path, err in failed:
            print(f"  - {path}: {err}")
        return 1

    print(f"\nAll {len(snippet_files)} snippets validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
