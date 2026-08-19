#!/bin/bash
# Runs, in order: unit tests, Ruff lint/format checks and the e2e (behave) suites.
#
# The e2e step needs the mock servers from the sinch-sdk-mockserver repository.
# Point MOCKSERVER_DIR at your local clone if it is not next to this repository:
#
#   MOCKSERVER_DIR=~/Desktop/sinch-sdk-mockserver ./scripts/run_checks.sh
#
# Options:
#   --skip-e2e   run only the unit tests and the Ruff checks

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MOCKSERVER_DIR="${MOCKSERVER_DIR:-$(dirname "$REPO_DIR")/sinch-sdk-mockserver}"

SKIP_E2E=false
for arg in "$@"; do
  case "$arg" in
    --skip-e2e) SKIP_E2E=true ;;
    *) echo "Unknown option: $arg" >&2; exit 2 ;;
  esac
done

DOMAINS=(numbers sms number_lookup conversation)

step() {
  echo ""
  echo "=============================================================="
  echo "  $1"
  echo "=============================================================="
}

cd "$REPO_DIR"

step "1/3 Unit tests"
python -m pytest tests/unit

step "2/3 Ruff"
FIX_COMMANDS=()
for domain in "${DOMAINS[@]}"; do
  ruff check "sinch/domains/$domain" --statistics \
    || FIX_COMMANDS+=("ruff check sinch/domains/$domain --fix")
  ruff format "sinch/domains/$domain" --check --diff \
    || FIX_COMMANDS+=("ruff format sinch/domains/$domain")
done

if [ ${#FIX_COMMANDS[@]} -gt 0 ]; then
  echo ""
  echo "Ruff found issues. Fix them with:"
  for command in "${FIX_COMMANDS[@]}"; do
    echo "  $command"
  done
  exit 1
fi

if [ "$SKIP_E2E" = true ]; then
  echo ""
  echo "Skipping e2e tests (--skip-e2e)."
  exit 0
fi

step "3/3 E2E tests"

if [ ! -d "$MOCKSERVER_DIR" ]; then
  echo "Mock server repository not found at: $MOCKSERVER_DIR" >&2
  echo "Clone https://github.com/sinch/sinch-sdk-mockserver or set MOCKSERVER_DIR." >&2
  exit 1
fi

echo "Starting mock servers from $MOCKSERVER_DIR..."
(cd "$MOCKSERVER_DIR" && docker compose up -d)

./.github/scripts/wait-for-mockserver.sh

echo "Copying feature files..."
cp "$MOCKSERVER_DIR"/features/numbers/available-regions.feature ./tests/e2e/numbers/features/
cp "$MOCKSERVER_DIR"/features/numbers/callback-configuration.feature ./tests/e2e/numbers/features/
cp "$MOCKSERVER_DIR"/features/numbers/numbers.feature ./tests/e2e/numbers/features/
cp "$MOCKSERVER_DIR"/features/numbers/webhooks.feature ./tests/e2e/numbers/features/
cp "$MOCKSERVER_DIR"/features/sms/* ./tests/e2e/sms/features/
cp "$MOCKSERVER_DIR"/features/number-lookup/lookups.feature ./tests/e2e/number-lookup/features/
cp "$MOCKSERVER_DIR"/features/conversation/messages.feature ./tests/e2e/conversation/features/
cp "$MOCKSERVER_DIR"/features/conversation/apps.feature ./tests/e2e/conversation/features/
cp "$MOCKSERVER_DIR"/features/conversation/contacts.feature ./tests/e2e/conversation/features/
cp "$MOCKSERVER_DIR"/features/conversation/webhooks-events.feature ./tests/e2e/conversation/features/

python -m behave tests/e2e/numbers/features
python -m behave tests/e2e/sms/features
python -m behave tests/e2e/conversation/features
python -m behave tests/e2e/number-lookup/features

echo ""
echo "All checks passed."
