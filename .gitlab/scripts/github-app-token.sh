#!/bin/sh
# Prints a GitHub App installation token scoped to a single repository.
# This is the GitLab CI equivalent of actions/create-github-app-token.
#
# Usage: github-app-token.sh <owner> <repo>
# Needs: GITHUB_SYNC_APP_CLIENT_ID (variable) and GITHUB_SYNC_APP_PRIVATE_KEY
#        (File variable, so its value is a path to the PEM file).
# Tools: curl, jq, openssl.
set -eu

owner="$1"
repo="$2"
: "${GITHUB_SYNC_APP_CLIENT_ID:?GITHUB_SYNC_APP_CLIENT_ID is not set}"
: "${GITHUB_SYNC_APP_PRIVATE_KEY:?GITHUB_SYNC_APP_PRIVATE_KEY is not set}"

b64url() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }

# JWT signed with the App key. GitHub accepts the client ID as issuer and a
# lifetime of at most 10 minutes. iat is backdated to allow for clock drift.
now=$(date +%s)
header=$(printf '{"alg":"RS256","typ":"JWT"}' | b64url)
payload=$(printf '{"iat":%d,"exp":%d,"iss":"%s"}' $((now - 60)) $((now + 540)) "$GITHUB_SYNC_APP_CLIENT_ID" | b64url)
signature=$(printf '%s.%s' "$header" "$payload" | openssl dgst -sha256 -binary -sign "$GITHUB_SYNC_APP_PRIVATE_KEY" | b64url)
jwt="$header.$payload.$signature"

# Prints the response body. On an HTTP error, prints GitHub's message to stderr
# and fails, so a bad key never turns into a "null" token.
github_api() {
  if ! body=$(curl --fail-with-body --silent --show-error \
    -H "Authorization: Bearer $jwt" \
    -H "Accept: application/vnd.github+json" \
    -H "X-GitHub-Api-Version: 2026-03-10" \
    "$@" 2>&1); then
    echo "GitHub API request failed: $body" >&2
    return 1
  fi
  printf '%s' "$body"
}

installation=$(github_api "https://api.github.com/repos/$owner/$repo/installation")
installation_id=$(printf '%s' "$installation" | jq -r '.id')

access=$(github_api -X POST "https://api.github.com/app/installations/$installation_id/access_tokens" \
  -d "{\"repositories\":[\"$repo\"]}")
token=$(printf '%s' "$access" | jq -r '.token // empty')
if [ -z "$token" ]; then
  echo "GitHub returned no token: $access" >&2
  exit 1
fi
printf '%s\n' "$token"
