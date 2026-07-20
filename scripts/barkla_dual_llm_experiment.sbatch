#!/usr/bin/env bash
#SBATCH --job-name=lux-dual-llm
#SBATCH --partition=gpu-l40s
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --gres=gpu:l40s:1
#SBATCH --time=24:00:00
#SBATCH --output=slurm-%j.out

set -euo pipefail

cd "$SLURM_SUBMIT_DIR"

module purge
module load miniforge3/25.3.0-python3.12.10
module load ollama/0.12.11

MODEL_A="${MODEL_A:-qwen3:32b}"
MODEL_B="${MODEL_B:-deepseek-r1:32b}"
PAIRS="${PAIRS:-1}"
SEED_START="${SEED_START:-20260701}"
OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://127.0.0.1:11434}"
PYTHON_BIN="${PYTHON_BIN:-$PWD/.venv/bin/python}"
MODEL_A_SLUG="${MODEL_A//:/_}"
MODEL_B_SLUG="${MODEL_B//:/_}"
OUTPUT_DIR="${OUTPUT_DIR:-$PWD/results/${SLURM_JOB_ID}_${MODEL_A_SLUG}_vs_${MODEL_B_SLUG}}"
: "${LUX_SOURCE_COMMIT:?Submit with LUX_SOURCE_COMMIT set to the tested source commit}"

export PYTHONNOUSERSITE=1
export LUX_LLM_NUM_PREDICT="${LUX_LLM_NUM_PREDICT:-384}"
export LUX_LLM_THINK="${LUX_LLM_THINK:-0}"
export LUX_LLM_JSON_MODE="${LUX_LLM_JSON_MODE:-1}"
export OLLAMA_HOST="$OLLAMA_BASE_URL"
export OLLAMA_HOME="$HOME/fastscratch/.ollama"
export OLLAMA_MODELS="$OLLAMA_HOME/models"
export OLLAMA_GPU_LAYERS=999
export OLLAMA_NUM_THREADS="${SLURM_CPUS_PER_TASK:-8}"
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=2
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
echo "Model A: $MODEL_A"
echo "Model B: $MODEL_B"
echo "Pairs: $PAIRS"
echo "Source commit: $LUX_SOURCE_COMMIT"
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
timeout 900 ollama pull "$MODEL_A"
timeout 900 ollama pull "$MODEL_B"
timeout 300 ollama run "$MODEL_A" 'Return exactly this JSON: {"ready":true}'
timeout 300 ollama run "$MODEL_B" 'Return exactly this JSON: {"ready":true}'

"$PYTHON_BIN" scripts/smoke_test.py
"$PYTHON_BIN" scripts/run_dual_llm_experiment.py \
  --model-a "$MODEL_A" \
  --model-b "$MODEL_B" \
  --pairs "$PAIRS" \
  --seed-start "$SEED_START" \
  --temperature 0.0 \
  --timeout 60 \
  --model-a-base-url "$OLLAMA_BASE_URL" \
  --model-b-base-url "$OLLAMA_BASE_URL" \
  --output-dir "$OUTPUT_DIR" \
  --resume
