#!/usr/bin/env bash
#
# Hook 3, Stop. Runs the checks at the end of a turn.
#
# Stop can only allow or block, so this one script picks what to run based on
# what changed:
#
#   only snippet files    -> snippet check
#   domain source         -> format/compile/test, extra checks, e2e, diff gate
#   nothing relevant      -> allow


set -uo pipefail

REPO="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$REPO" || exit 0

source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"

INPUT="$(cat)"

# Set when this turn was started by this hook blocking. Without the check a
# failing gate would loop.
[[ "$(jq -r '.stop_hook_active // false' <<<"$INPUT")" == "true" ]] && exit 0

CHANGED="$(git status --porcelain 2>/dev/null | cut -c4- | sed 's/.* -> //')"
[[ -z "$CHANGED" ]] && exit 0

block() {
  printf '%s\n' "$1" >&2
  exit 2
}

run() {
  local label="$1"; shift
  local log; log="$(mktemp)"
  if ! "$@" >"$log" 2>&1; then
    block "$(printf 'Verification failed: %s\n\nCommand: %s\n\nLast 60 lines:\n%s\n\nFix the cause and re-run. Do not disable the check, do not hand-format around spotless, and do not weaken a test to make it pass.' \
      "$label" "$*" "$(grep -v -e '^[[:space:]]*at ' -e '^[[:space:]]*\.\.\. [0-9]* more' "$log" | tail -60)")"
  fi
  rm -f "$log"
}

# Snippet files only.
if ! grep -qv "^$SNIPPET_PREFIX" <<<"$CHANGED"; then
  run "snippet check ($SNIPPET_PREFIX)" bash -c "$SNIPPET_CMD"
  echo "Snippet branch: $SNIPPET_PREFIX passed."
  exit 0
fi

# Which domains changed.
DOMAINS="$(sed -n "$DOMAIN_SED" <<<"$CHANGED" | sort -u)"
[[ -z "$DOMAINS" ]] && exit 0

# A missing script is a setup problem the model cannot fix. Report it and let
# the turn end instead of blocking.
VALIDATE="$(resolve_script validate_endpoint.sh)" || true
E2E="$(resolve_script verify_e2e.sh)" || true
if [[ -z "${VALIDATE:-}" || -z "${E2E:-}" ]]; then
  jq -n --arg m "Verification did not run: the skill's validation scripts were not found. $MISSING_SCRIPT_HELP" \
    '{systemMessage: $m}'
  exit 0
fi

for DOMAIN in $DOMAINS; do

  # Format, compile, run this domain's tests. Fails if no tests matched.
  run "3a tidy & build (domain: $DOMAIN)" "$VALIDATE" "$DOMAIN"

  # --- 3b·A · Deterministic spec-conformance scripts --------------------
  shopt -s nullglob
  CHECKS=(.claude/hooks/checks/check-*.sh)
  shopt -u nullglob
  if (( ${#CHECKS[@]} == 0 )); then
    echo "3b-A: no check-*.sh installed for '$DOMAIN'."
  else
    for check in "${CHECKS[@]}"; do
      run "3b-A $(basename "$check" .sh) (domain: $DOMAIN)" "$check" "$DOMAIN"
    done
  fi

  # e2e. Exits 0 with a notice if the mockserver has no features for it.
  run "3b-B e2e against the mockserver (domain: $DOMAIN)" "$E2E" "$DOMAIN"

  # The gate applies whenever a tracked file changed, because a shipped file
  # changed. That is not the same as "this is an update": adding an endpoint to
  # an existing domain also edits the wiring (service interface, client
  # registration, config). Untracked files alongside the edits tell the two
  # apart, and only the wording differs.
  MODIFIED="$(git status --porcelain 2>/dev/null | grep '^ *M' | sed -n "$DOMAIN_SED" | grep -cx "$DOMAIN" || true)"
  ADDED="$(git status --porcelain 2>/dev/null | grep '^??' | sed -n "$DOMAIN_SED" | grep -cx "$DOMAIN" || true)"
  if (( MODIFIED > 0 )); then
    if (( ADDED > 0 )); then
      WHAT="new code plus edits to $MODIFIED shipped file(s)"
    else
      WHAT="edits to $MODIFIED shipped file(s), and no new files, so an update"
    fi
    if [[ -x .claude/hooks/checks/diff-gate.sh ]]; then
      run "3c diff & breaking-change gate ($DOMAIN: $WHAT)" .claude/hooks/checks/diff-gate.sh "$DOMAIN"
    else
      echo "3c: $DOMAIN has $WHAT. Shipped files changed, so a consumer can break; diff-gate.sh is not installed, so that is not checked."
    fi
  fi
done

echo "Verification passed for: $(tr '\n' ' ' <<<"$DOMAINS")"

# Reminder only. Snippets are written by a separate skill in a later turn, so
# blocking here would fail the wrong turn. In Java, examples/ is a CI gate the
# main build does not cover.
if ! grep -q "^$SNIPPET_PREFIX" <<<"$CHANGED"; then
  echo "NOTE: endpoint code changed, but nothing under '$SNIPPET_PREFIX'."
  echo "      The runnable snippet is a separate skill (sinch-add-snippet) and is"
  echo "      still needed before a PR. examples/ is a CI gate of its own."
fi

exit 0
