#!/usr/bin/env bash
#
# Hook 1, PreToolUse on Write and Edit.
#
# Runs the integration tests on the current SDK and refuses the first file
# change if they fail. A marker file keyed on the session id means the tests
# run once per session, not once per edit.

set -uo pipefail

REPO="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$REPO" || exit 0

source "$(dirname "${BASH_SOURCE[0]}")/_lib.sh"

INPUT="$(cat)"
SESSION_ID="$(jq -r '.session_id // "nosession"' <<<"$INPUT")"
FILE_PATH="$(jq -r '.tool_input.file_path // ""' <<<"$INPUT")"

SENTINEL="${TMPDIR:-/tmp}/sinch-baseline-${SESSION_ID}"

deny() {
  jq -n --arg r "$1" '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: $r
    }
  }'
  exit 0
}

# Already run this session.
[[ -f "$SENTINEL" ]] && exit 0

# Find the path being written. Write and Edit carry it directly; Bash has to be
# inspected, because a heredoc into a source file bypasses Write entirely.
TOOL="$(jq -r '.tool_name // ""' <<<"$INPUT")"
case "$TOOL" in
  Bash)
    CMD="$(jq -r '.tool_input.command // ""' <<<"$INPUT")"
    FILE_PATH="$(gated_target_in_command "$CMD")" || exit 0
    ;;
  *)
    # Only gate SDK source. Docs and config files pass through.
    is_gated_path "$FILE_PATH" || exit 0
    ;;
esac

# Which domain is being written to.
DOMAIN="$(sed -n "$DOMAIN_SED" <<<"$FILE_PATH" | head -1)"


# A missing script is a setup problem the model cannot fix. Warn and allow,
# rather than refusing every write on a misconfigured machine.
if ! E2E="$(resolve_script verify_e2e.sh)"; then
  jq -n --arg m "Baseline gate INACTIVE: verify_e2e.sh not found. $MISSING_SCRIPT_HELP" \
    '{systemMessage: $m}'
  exit 0
fi

# Only scope to the domain if it already exists. A new domain is not part of
# the current SDK, so scoping to it would fail for the wrong reason.
if [[ -n "$DOMAIN" ]]; then
  [[ -d "$(printf "$DOMAIN_DIR_FMT" "$DOMAIN")" ]] || DOMAIN=""
fi

LOG="${TMPDIR:-/tmp}/sinch-baseline-${SESSION_ID}.log"
if [[ -n "$DOMAIN" ]]; then "$E2E" "$DOMAIN" >"$LOG" 2>&1; else "$E2E" >"$LOG" 2>&1; fi
if [[ $? -ne 0 ]]; then
  deny "$(printf 'Baseline failed. Do not start writing code.\n\nThe integration tests on the current SDK are failing%s. Code written now would sit on a broken baseline, and a later failure could not be traced to your change.\n\nLast 40 lines:\n%s\n\nFull log: %s\n\nFix the baseline (or ask the user to), then retry. Do not work around this gate.' \
    "${DOMAIN:+ for domain '$DOMAIN'}" "$(tail -40 "$LOG")" "$LOG")"
fi

touch "$SENTINEL"
exit 0
