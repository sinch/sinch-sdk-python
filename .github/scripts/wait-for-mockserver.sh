#!/bin/bash

wait_for_server() {
  local url=$1
  echo "Waiting for $url to be ready..."

  for i in {1..30}; do
    if curl -sSf "$url" > /dev/null; then
      echo "$url is ready!"
      return 0
    fi
    echo "Still waiting for $url..."
    sleep 2
  done

  echo "Error: $url did not start in time"
  exit 1
}

# Wait for auth mock servers
wait_for_server "http://localhost:3011/health"
# Wait for numbers mock servers
wait_for_server "http://localhost:3013/health"

echo "All mock servers are ready!"