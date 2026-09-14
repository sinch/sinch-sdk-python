#!/usr/bin/env bash
#
# Hook 2, SessionStart.
#
# Adds the operation-id to SDK-name mapping to the session, so the skill does
# not have to look it up. Reads a local copy of the Confluence page; a hook has
# no Atlassian credentials and cannot fetch it. Update the copy by hand.


set -uo pipefail

REPO="${CLAUDE_PROJECT_DIR:-$PWD}"
SNAPSHOT="$REPO/.claude/context/operation-ids.md"
PAGE_URL="https://sinchenterprise.atlassian.net/wiki/spaces/PF/pages/812783650"

read -r -d '' DECISION <<'RULE' || true
DECISION RULE. A new endpoint that is not listed in Confluence:
  STOP. Do not invent a name, do not derive one from the operationId, do not
  copy the pattern from a sibling operation, and do not proceed with a
  placeholder you intend to fix later. Report which operation id is missing and
  ask for the Confluence page to be extended first. Naming is a team decision.
  This applies even when the correct name looks obvious.
RULE

read -r -d '' UPDATE_RULES <<'RULES' || true
KEEPING THIS LIST CURRENT

This list is a copy of the page, and can be behind it. BEFORE you rely on a name
from it, if the Atlassian connector is available, check it. That check is not
optional: finding your operation in this list is not evidence the list is
current.

Check both, because neither alone is enough:

  - the page's last-modified date against the one in the header below. The date
    is day-granular, so a page edited later on the same day still matches.
  - the actual rows for the domain you are working in, against the rows here.

If the page differs, use what the page says for the rest of this run, subject to
the two rules below on corrections and on conflicting names.

If the connector is not available, use this list and say that you could not
check the page.

When the page has rows this copy is missing, add them, under these rules:

  - Only for a domain that already has a heading here. Do not add new domains;
    the scope is deliberate and covers the domains of this SDK only.
  - Keep the headings and the layout exactly as they are. The coverage list
    above is generated from them.
  - Never remove or reword a row that this copy marks as a correction to the
    page. Those were checked against the spec and they win.
  - If a row exists in both but the names differ, and this copy does not mark it
    as a correction, STOP. Report both names and ask which is right. Do not
    switch the name and do not edit the copy: a rename changes a public SDK
    surface and is a team decision.
  - Update the "Page lastModified" line to the date the page reports.

Then say what you added, and that the master copy in the tooling repo
(hooks/operation-ids.<lang>.md) needs the same edit, or the next install will
overwrite it.
RULES

emit() {
  jq -n --arg c "$1" '{
    hookSpecificOutput: {
      hookEventName: "SessionStart",
      additionalContext: $c
    }
  }'
  exit 0
}

if [[ ! -f "$SNAPSHOT" ]]; then
  emit "$(printf 'OPERATION-ID MAPPING: NOT AVAILABLE LOCALLY\n\nThe operation-id -> SDK function mapping could not be read (%s is missing).\n\nBefore naming any public method, open the Confluence page "APIs Operation Ids <-> SDK functions mapping" and use the name exactly as written there:\n  %s\n\n%s' \
    "$SNAPSHOT" "$PAGE_URL" "$DECISION")"
fi

AGE_DAYS=$(( ( $(date +%s) - $(stat -f %m "$SNAPSHOT" 2>/dev/null || stat -c %Y "$SNAPSHOT") ) / 86400 ))
STALE=""
(( AGE_DAYS > 30 )) && STALE=$(printf '\n\n[!] This copy is %s days old. If an operation looks missing, read the\nConfluence page above and update %s.' "$AGE_DAYS" "$SNAPSHOT")

# Which domains this copy covers. If it does not cover your domain, its
# absence says nothing about the Confluence page.
# Line 1 is the file's own title, not a domain. Skip it.
COVERAGE="$(tail -n +2 "$SNAPSHOT" | grep -oE '^# .*' | sed 's/^# /  - /')"
[[ -z "$COVERAGE" ]] && COVERAGE="  - (unlabelled)"

emit "$(printf 'OPERATION-ID MAPPING: operation id to SDK function name\n\nThe "# ... API" sections below are authoritative: use those names verbatim.\nSections marked NOT authoritative are not. Never reuse a name already taken\nwithin the same service. Whichever name you end up using, it is used VERBATIM.\n\n%s\n\nCOVERS THESE DOMAINS ONLY, and says nothing about any other:\n%s\n\n%s\n\nSource: %s (copy: %s)%s\n\n%s' \
  "$DECISION" "$COVERAGE" "$UPDATE_RULES" "$PAGE_URL" "$SNAPSHOT" "$STALE" "$(cat "$SNAPSHOT")")"
