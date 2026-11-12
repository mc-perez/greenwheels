#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PYTHON="${ROOT}/.venv/bin/python"
if [[ ! -x "$PYTHON" ]]; then
  echo "Create venv first: cd mcp-server && python -m venv .venv && pip install -e '.[dev]'" >&2
  exit 1
fi
export GREENWHEELS_API_URL="${GREENWHEELS_API_URL:-http://localhost:8000}"
exec "$PYTHON" -m greenwheels_mcp
