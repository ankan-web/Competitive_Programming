#!/usr/bin/env bash
# Usage: bash scripts/validate.sh <base_sha> <head_sha>
# Reports FAIL and returns nonzero on invalid input or validation errors.
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/validate.py" "${1:-origin/main}" "${2:-HEAD}"
