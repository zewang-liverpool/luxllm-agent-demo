#!/usr/bin/env bash
#SBATCH --job-name=luxllm-paired
#SBATCH --partition=gpu-h100
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:h100:1
#SBATCH --time=48:00:00
#SBATCH --output=slurm-%j.out

set -euo pipefail

cd "$SLURM_SUBMIT_DIR"

module purge
module load miniforge3/25.3.0-python3.12.10
module load ollama/0.12.11

# Submit from the repository root. Override these with sbatch --export.
MODEL="${MODEL:-qwen3:32b}"
PAIRS="${PAIRS:-50}"
SEED_START="${SEED_START:-20260701}"
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://127.0.0.1:11434}"
PYTHON_BIN="${PYTHON_BIN:-$PWD/.venv/bin/python}"
OUTPUT_DIR="${OUTPUT_DIR:-$PWD/results/${SLURM_JOB_ID}_${MODEL//:/_}_paired}"

export PYTHONNOUSERSITE=1
export OLLAMA_HOST="$OLLAMA_BASE_URL"
export OLLAMA_HOME="$HOME/fastscratch/.ollama"
export OLLAMA_MODELS="$OLLAMA_HOME/models"
export OLLAMA_GPU_LAYERS=999
export OLLAMA_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_KEEP_ALIVE=-1
export OLLAMA_NO_CPU_FALLBACK=1
export TMPDIR="$OLLAMA_HOME/tmp"

mkdir -p "$OUTPUT_DIR" "$OLLAMA_MODELS" "$TMPDIR"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Python environment not found: $PYTHON_BIN" >&2
  echo "Create it with scripts/setup.sh or export PYTHON_BIN." >&2
  exit 2
fi

echo "Host: $(hostname)"
echo "Job: $SLURM_JOB_ID"
echo "Model: $MODEL"
echo "Pairs: $PAIRS"
echo "Output: $OUTPUT_DIR"
"$PYTHON_BIN" --version
nvidia-smi

ollama serve >"$OUTPUT_DIR/ollama-server.log" 2>&1 &
OLLAMA_PID=$!
cleanup() {
  kill "$OLLAMA_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

sleep 10
ollama list
timeout 900 ollama pull "$MODEL"
timeout 300 ollama run "$MODEL" 'Return exactly this JSON: {"ready":true}'

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
