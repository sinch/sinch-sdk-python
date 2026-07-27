#!/usr/bin/env bash
# Regenerates requirements-dev.txt from requirements.in.
set -euo pipefail
cd "$(dirname "$0")/.."
uv pip compile --universal --python-version 3.9 --output-file=requirements-dev.txt --upgrade \
  --custom-compile-command "./scripts/compile_requirements.sh" requirements.in
