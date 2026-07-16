#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$ROOT/.venv"
VENV_PYTHON="$VENV/bin/python"

if [[ ( -e "$VENV_PYTHON" || -L "$VENV_PYTHON" ) ]] && ! "$VENV_PYTHON" --version >/dev/null 2>&1; then
  echo "Existing .venv is broken or points to a missing Python installation; rebuilding it." >&2
  rm -rf -- "$VENV"
fi

if [[ ! -x "$VENV_PYTHON" ]]; then
  if [[ -n "${PYTHON_BIN:-}" ]]; then
    CANDIDATES=("$PYTHON_BIN")
  else
    CANDIDATES=(python3.11 python3.12 python3.10 python3)
  fi

  SELECTED=""
  for candidate in "${CANDIDATES[@]}"; do
    if command -v "$candidate" >/dev/null 2>&1 && "$candidate" --version >/dev/null 2>&1; then
      SELECTED="$candidate"
      break
    fi
  done
  if [[ -z "$SELECTED" ]]; then
    echo "No supported Python 3.10-3.12 interpreter was found." >&2
    exit 1
  fi

  echo "Creating .venv with: $SELECTED"
  "$SELECTED" -m venv "$VENV"
fi

"$VENV_PYTHON" -m pip install --upgrade "pip==23.1.2"
"$VENV_PYTHON" -m pip install -r "$ROOT/requirements-dev.txt"

echo "Environment ready: $VENV_PYTHON"
echo "Next: $VENV_PYTHON scripts/smoke_test.py"
