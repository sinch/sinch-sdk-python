import importlib.util
from pathlib import Path
from textwrap import dedent
import pytest

ROOT = Path(__file__).parent.parent.parent
_SPEC = importlib.util.spec_from_file_location(
    "check_snippet_coverage",
    ROOT / "scripts" / "check_snippet_coverage.py",
)
_CHECK_SNIPPET_MOD = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_CHECK_SNIPPET_MOD)
validate_snippet = _CHECK_SNIPPET_MOD.validate_snippet


@pytest.fixture
def temp_snippet_dir(tmp_path):
    """Temporary directory for snippet files."""
    return tmp_path


def test_nonexistent_module_import_expects_failure_with_broken_import_message(
    temp_snippet_dir,
):
    """Test that importing a nonexistent module returns failure with broken import message."""
    path = temp_snippet_dir / "snippet.py"
    path.write_text("from nonexistent_module_xyz import foo")

    success, error = validate_snippet(path)

    assert success is False
    assert "Broken import" in error
    assert "nonexistent_module_xyz" in error


def test_missing_name_import_from_sinch_expects_failure(temp_snippet_dir):
    """Test that importing a missing name from sinch returns failure."""
    path = temp_snippet_dir / "snippet.py"
    path.write_text("from sinch import NonExistentClass")

    success, error = validate_snippet(path)

    assert success is False
    assert "Broken import" in error or "ImportError" in error


def test_nonexistent_sdk_method_expects_attribute_error(temp_snippet_dir):
    """Test that calling a nonexistent SDK method returns failure with attribute error."""
    snippet = """
        from sinch import SinchClient

        sinch_client = SinchClient(
            project_id="my-project-id",
            key_id="my-key-id",
            key_secret="my-key-secret",
            sms_region="us",
        )
        sinch_client.sms.batches.send_nonexistent_method(
            to=["+1"], from_="+1", body="hi"
        )
    """
    path = temp_snippet_dir / "snippet.py"
    path.write_text(dedent(snippet))

    success, error = validate_snippet(path)

    assert success is False
    assert "Method/attribute does not exist" in error
    assert "send_nonexistent_method" in error


def test_invalid_syntax_expects_syntax_error(temp_snippet_dir):
    """Test that invalid Python syntax returns failure with syntax error."""
    path = temp_snippet_dir / "snippet.py"
    path.write_text("def foo()\n    return 42")

    success, error = validate_snippet(path)

    assert success is False
    assert "Syntax error" in error


def test_snippet_without_api_call_expects_failure(temp_snippet_dir):
    """Test that a snippet that does not make an API call returns failure."""
    snippet = """
        from sinch import SinchClient

        sinch_client = SinchClient(
            project_id="my-project-id",
            key_id="my-key-id",
            key_secret="my-key-secret",
            sms_region="us",
        )
        print("no api call")
    """
    path = temp_snippet_dir / "snippet.py"
    path.write_text(dedent(snippet))

    success, error = validate_snippet(path)

    assert success is False
    assert "without making API call" in error


def test_invalid__args_expects_failure(temp_snippet_dir):
    """Test that invalid arguments return failure (TypeError or similar)."""
    snippet = """
        from sinch import SinchClient

        sinch_client = SinchClient(
            project_id="my-project-id",
            key_id="my-key-id",
            key_secret="my-key-secret",
            sms_region="us",
        )
        sinch_client.sms.batches.send_sms(
            to="not_a_list", from_="+1", body="hi"
        )
    """
    path = temp_snippet_dir / "snippet.py"
    path.write_text(dedent(snippet))

    success, error = validate_snippet(path)

    assert success is False
    assert "TypeError" in error or "AttributeError" in error or len(error) > 0


def test_valid_snippet_expects_success(temp_snippet_dir):
    """Test that a valid snippet (inline string) passes validation."""
    snippet = """
        from sinch import SinchClient

        sinch_client = SinchClient(
            project_id="my-project-id",
            key_id="my-key-id",
            key_secret="my-key-secret",
            sms_region="us",
        )
        sinch_client.sms.batches.send_sms(to=["+1"], from_="+1", body="hi")
    """
    path = temp_snippet_dir / "snippet.py"
    path.write_text(dedent(snippet))

    success, error = validate_snippet(path)

    assert success is True, f"Snippet failed: {error}"
