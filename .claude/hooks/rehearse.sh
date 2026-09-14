#!/usr/bin/env bash
#
# Checks that the hooks are installed and working, without starting a Claude
# session and without waiting for a build. Takes a few seconds.
#
# Claude Code passes each hook a small piece of JSON on stdin and reads what the
# hook prints back. This script sends that same JSON by hand and shows you the
# reply, so you can see what a hook would do before trusting it in a real
# session.
#
#   rehearse.sh          # the cases where the hooks allow the work through
#   rehearse.sh --block  # also the cases where they refuse it
#
# --block does not fake a failure. It runs the real baseline against a
# mockserver directory that does not exist, so the failure and the refusal are
# genuine.

set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-$PWD}" || exit 1
HOOKS=".claude/hooks"
BLOCK=0; [[ "${1:-}" == "--block" ]] && BLOCK=1

b() { printf '\n\033[1m%s\033[0m\n%s\n' "$1" "$(printf '─%.0s' {1..70})"; }
verdict() { if [[ "$1" == "$2" ]]; then printf '\033[32m  ✓ exit %s (%s)\033[0m\n' "$1" "$3"; else printf '\033[31m  ✗ exit %s, expected %s\033[0m\n' "$1" "$2"; fi; }

source "$HOOKS/_lib.sh"

b "Hook 2, SessionStart: what gets added to every session"
echo '{}' | "$HOOKS/inject-conventions.sh" | jq -r '.hookSpecificOutput.additionalContext'
verdict $? 0 "injects context, never blocks"

b "Hook 1, PreToolUse: editing a doc is not gated"
echo '{"session_id":"rehearse","tool_input":{"file_path":"'"$PWD"'/README.md"}}' | "$HOOKS/baseline-gate.sh"
verdict $? 0 "allowed without running anything"

b "Hook 3, Stop: the real gate"
if git status --porcelain 2>/dev/null | sed -n "$DOMAIN_SED" | grep -q .; then
  echo "  Domain files ARE modified, so this runs the real 3a/3b gate."
  echo "  exit 0 = they pass; exit 2 = a genuine failure it is right to block on."
  echo '{"stop_hook_active":false}' | "$HOOKS/verify-gate.sh"; rc=$?
  printf '  -> exit %s\n' "$rc"
else
  echo '{"stop_hook_active":false}' | "$HOOKS/verify-gate.sh"
  verdict $? 0 "nothing under domains/ changed: ends immediately, no build"
fi

b "Hook 3, Stop: loop guard"
echo '{"stop_hook_active":true}' | "$HOOKS/verify-gate.sh"
verdict $? 0 "already blocked once; does not bounce forever"

if (( BLOCK )); then
  b "Hook 1, PreToolUse: baseline failing, editing domain source"
  echo "  (making the baseline genuinely fail: MOCKSERVER_DIR points nowhere)"
  echo
  MOCKSERVER_DIR=/nonexistent-on-purpose \
  echo '{"session_id":"rehearse-block","tool_input":{"file_path":"'"$PWD"'/openapi-contracts/src/main/com/sinch/sdk/domains/voice/Probe.java"}}' \
    | MOCKSERVER_DIR=/nonexistent-on-purpose "$HOOKS/baseline-gate.sh" \
    | jq -r '.hookSpecificOutput | "DECISION: " + .permissionDecision + "\n\n" + .permissionDecisionReason'
  rm -f "${TMPDIR:-/tmp}"/sinch-baseline-rehearse-block*
  echo
  echo "  ^ Claude Code refuses the Write and hands that text to the skill."
fi

b "Setup"
for s in validate_endpoint.sh verify_e2e.sh; do
  if p="$(resolve_script $s)"; then printf '  ✓ %-22s -> %s\n' "$s" "$p"
  else printf '  ✗ %-22s not found. The gate that uses it is inactive.\n' "$s"; fi
done

b "Optional files"
[[ -f .claude/context/operation-ids.md ]] \
  && echo "  ✓ operation-ids.md present. Hook 2 adds the mapping." \
  || echo "  ! operation-ids.md missing. Hook 2 adds only the page URL."
shopt -s nullglob; C=(.claude/hooks/checks/check-*.sh); shopt -u nullglob
(( ${#C[@]} )) \
  && printf '  ✓ %s spec-conformance check(s) wired into Hook 3\n' "${#C[@]}" \
  || echo "  ! no check-*.sh installed."
echo
