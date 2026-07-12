#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3.11}"

if [[ ! -x "$ROOT/.venv/bin/python" ]]; then
  "$PYTHON_BIN" -m venv "$ROOT/.venv"
fi

"$ROOT/.venv/bin/python" -m pip install --upgrade "pip==23.1.2"
"$ROOT/.venv/bin/python" -m pip install -r "$ROOT/requirements-dev.txt"

echo "Environment ready: $ROOT/.venv/bin/python"
echo "Next: $ROOT/.venv/bin/python scripts/smoke_test.py"
