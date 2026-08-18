# Supplementary LLM-versus-LLM Experiment

## Purpose

This supplementary experiment runs Qwen3-32B directly against
DeepSeek-R1-32B while preserving the dissertation's primary focus on
decision tracing and rule-based action verification. It is not presented as
a general model leaderboard.

For every Lux environment seed:

1. Qwen plays as `player_0` and DeepSeek as `player_1`;
2. the same seed is repeated with the roles swapped;
3. both agents use independent model routing, strategy caches, fallback
   state, and player-labelled decision logs.

## Local acceptance

Run before transferring the source to Barkla2:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\run_mock_dual_llm_smoke.py
.\.venv\Scripts\python.exe tools\validate_dual_llm_result.py `
  results\mock_dual_llm_role_swap_smoke
```

Expected minimum result:

```text
35 tests pass
2/2 mock matches complete
1 matched seed pair complete
both players and both mock models present in every run
all fresh mock LLM calls valid
```

## Barkla2 sanity test

Never run Ollama on a login node. Submit the included Slurm script with one
seed pair first:

```bash
cd ~/luxllm-agent-dual
SOURCE_COMMIT=$(cat SOURCE_COMMIT.txt)

sbatch \
  --partition=gpu-l40s \
  --gres=gpu:l40s:1 \
  --export=ALL,LUX_SOURCE_COMMIT="$SOURCE_COMMIT",PAIRS=1,SEED_START=20260701 \
  scripts/barkla_dual_llm_experiment.sbatch
```

After completion:

```bash
JOBID=<completed-job-id>
RESULT_DIR="results/${JOBID}_qwen3_32b_vs_deepseek-r1_32b"

sacct -j "$JOBID" \
  --format=JobID,Partition,State,ExitCode,Elapsed,AllocTRES%60

.venv/bin/python tools/validate_dual_llm_result.py "$RESULT_DIR"
```

The sanity test passes only when:

- two matches and one role-swapped seed pair complete;
- both models make fresh calls in both runs;
- model-to-player routing changes between the two matches;
- no LLM error or timeout occurs;
- all called responses are structurally valid after deterministic checks.

If one L40S cannot keep both 32B models resident, do not launch the formal
run. Record the Ollama and Slurm error and move the sanity test to an H100 or
an approved two-GPU configuration.

## Formal run

Only after the one-pair sanity test passes:

```bash
SOURCE_COMMIT=$(cat SOURCE_COMMIT.txt)

sbatch \
  --partition=gpu-l40s \
  --gres=gpu:l40s:1 \
  --export=ALL,LUX_SOURCE_COMMIT="$SOURCE_COMMIT",PAIRS=50,SEED_START=20260701 \
  scripts/barkla_dual_llm_experiment.sbatch
```

This produces 50 matched seeds and 100 role-swapped matches. Treat the
head-to-head outcome as supplementary evidence. The primary analysis remains
trace completeness, model-labelled provenance, normalization, fallback,
latency, risk-filter intervention, and executable action validity.

## Completed formal evidence

The formal Barkla2 run completed on job `9845992` using an A100 80 GB node:

- 100/100 matches and 50/50 role-swapped seed pairs completed;
- Qwen won 54 and DeepSeek won 46, with no draws;
- the seed-clustered Qwen win-rate interval was `[0.45, 0.63]`;
- the seed-level exact sign-test p-value was `0.5034`;
- 4,676/4,676 fresh LLM calls were valid after deterministic checks;
- 106,317 structured trace records had complete required fields and replay linkage;
- 571 raw responses required deterministic normalization;
- risk verification changed targets on 15,721 steps;
- no LLM timeout, API error, or downstream action fallback was observed.

The 54:46 result is not statistically distinguishable from parity. Its proper
use is supplementary evidence that simultaneous LLM agents remain inspectable
and verifiable through the framework.
