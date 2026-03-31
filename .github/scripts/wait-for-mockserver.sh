#!/bin/bash

wait_for_server() {
  local url=$1
  echo "Waiting for $url to be ready..."

  MAX_RETRIES="${MAX_RETRIES:-30}"
  SLEEP_SECONDS="${SLEEP_SECONDS:-2}"

  for ((i = 1; i <= MAX_RETRIES; i++)); do
    if curl -sSf "$url" > /dev/null; then
      echo "$url is ready!"
      return 0
    fi
    echo "Attempt $i/$MAX_RETRIES: Still waiting for $url..."
    sleep "$SLEEP_SECONDS"
  done

  echo "Error: $url was not available after $((MAX_RETRIES * SLEEP_SECONDS)) seconds"
  exit 1
}

# Wait for auth mock servers
wait_for_server "http://localhost:3011/health"
# Wait for numbers mock servers
wait_for_server "http://localhost:3013/health"

echo "All mock servers are ready!"