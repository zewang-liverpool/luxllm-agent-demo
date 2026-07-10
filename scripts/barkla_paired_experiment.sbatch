#!/usr/bin/env bash
#SBATCH --job-name=luxllm-paired
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:1
#SBATCH --time=48:00:00
#SBATCH --output=slurm-%j.out

set -euo pipefail

# Submit from the repository root. Override these with sbatch --export.
MODEL="${MODEL:-qwen3:32b}"
PAIRS="${PAIRS:-50}"
SEED_START="${SEED_START:-20260701}"
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://127.0.0.1:11434}"
PYTHON_BIN="${PYTHON_BIN:-$PWD/.venv/bin/python}"
OUTPUT_DIR="${OUTPUT_DIR:-$PWD/results/${SLURM_JOB_ID}_${MODEL//:/_}_paired}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Python environment not found: $PYTHON_BIN" >&2
  echo "Create it with scripts/setup.sh or export PYTHON_BIN." >&2
  exit 2
fi

"$PYTHON_BIN" scripts/smoke_test.py
"$PYTHON_BIN" scripts/run_paired_experiment.py \
  --model "$MODEL" \
  --pairs "$PAIRS" \
  --seed-start "$SEED_START" \
  --temperature 0.0 \
  --timeout 60 \
  --ollama-base-url "$OLLAMA_BASE_URL" \
  --output-dir "$OUTPUT_DIR" \
  --resume
