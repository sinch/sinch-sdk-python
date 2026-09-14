#!/usr/bin/env bash

# Paths whose edits are gated by the baseline (PreToolUse).
GATED_PATHS=('*/src/*')
# sed expression extracting the domain name from a repo path.
DOMAIN_SED='s#.*/domains/\([a-z_]*\)/.*#\1#p'
# Prefix identifying snippet/example files (the Stop hook's snippet branch).
SNIPPET_PREFIX='examples/'
# Command run when only snippet files changed.
SNIPPET_CMD='true'
# printf format for a domain's source directory, used to tell an existing
# domain from a new one.
DOMAIN_DIR_FMT='sinch/domains/%s'
# Extra directories searched for the skill's validation scripts.
SKILL_DIRS=()

CONF="$(dirname "${BASH_SOURCE[0]}")/repo.conf"
[[ -f "$CONF" ]] && source "$CONF"

# validate_endpoint.sh and verify_e2e.sh belong to the skill, not the SDK repo,
# so a hook running in an SDK checkout cannot assume ./scripts/.
resolve_script() {
  local name="$1" c
  for c in "${SINCH_SKILL_SCRIPTS:+${SINCH_SKILL_SCRIPTS}/$name}" \
           "scripts/$name" "${SKILL_DIRS[@]/%//$name}"; do
    [[ -n "$c" && -x "$c" ]] && { printf '%s' "$c"; return 0; }
  done
  return 1
}

# Is $1 a path the baseline gate should protect?
is_gated_path() {
  local p="$1" g
  for g in "${GATED_PATHS[@]}"; do [[ "$p" == $g ]] && return 0; done
  return 1
}

# Print the first gated path a shell command appears to write to, if any.
# Covers redirects, tee, touch, mkdir -p, sed -i, and the destination of cp/mv.
# A determined command can still evade this; the gate is a guardrail, not a
# sandbox.
gated_target_in_command() {
  local cmd="$1" tok flat
  flat="$(tr '\n' ' ' <<<"$cmd")"

  # One-token forms: the path follows the operator.
  # Two-token forms (cp, mv): the path is the SECOND argument, so match both
  # and keep the last.
  for tok in $( { grep -oE '(>>?|tee( -a)?|touch|mkdir -p)[[:space:]]+[^[:space:];|&]+' <<<"$flat"
                  grep -oE '(cp|mv)([[:space:]]+-[A-Za-z]+)*[[:space:]]+[^[:space:];|&]+[[:space:]]+[^[:space:];|&]+' <<<"$flat"
                  grep -oE 'sed[^;|&]*[[:space:]]-i[^;|&]*' <<<"$flat"
                } | sed 's/[[:space:]]*$//' | grep -oE '[^[:space:]]+$' ); do
    tok="${tok%\"}"; tok="${tok#\"}"; tok="${tok%\'}"; tok="${tok#\'}"
    case "$tok" in /*) ;; *) tok="$PWD/$tok" ;; esac
    if is_gated_path "$tok"; then printf '%s' "$tok"; return 0; fi
  done
  return 1
}

MISSING_SCRIPT_HELP='Set SINCH_SKILL_SCRIPTS to the skill'\''s scripts directory, e.g.
  export SINCH_SKILL_SCRIPTS=<tooling-repo>/<Lang>/skills/sinch-add-endpoint/scripts
or clone sinch-sdk-tooling-internal next to this repo.'
