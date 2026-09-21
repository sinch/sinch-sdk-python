#!/bin/bash

check_server() {
  local url=$1

  if curl -sSf "$url" > /dev/null 2>&1; then
    echo "$url is available!"
    return 0
  fi

  echo "Error: $url is not available"
  exit 1
}

MOCKSERVER_BASE_URL="${MOCKSERVER_BASE_URL:-https://sinch-sdk-mockserver.sliplane.app}"

# Check the root /health endpoint aggregates the health of all domain configs.
check_server "$MOCKSERVER_BASE_URL/health"

echo "Mock servers are available!"
