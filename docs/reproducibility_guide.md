# Reproducibility Guide

Version: `LuxLLM-Agent reproducibility-hardening v1`

Verified locally on 11 July 2026 with Windows 11, Python 3.12.13,
`luxai-s3==0.2.1`, and seed 42.  The original Barkla2 experiments used a
Python 3.11 environment; both the direct dependency and the verified Windows
lock file are included.

## 1. Reproducibility Levels

The repository supports three independent workflows:

1. **Viewer reproduction** — no Lux environment or LLM is required.
2. **Rule-only runtime reproduction** — requires Python and `luxai-s3`, but no Ollama.
3. **LLM evaluation reproduction** — additionally requires Ollama and the named model.

Generated logs, replays, model weights, and `results/` are intentionally not
committed. Machine-readable summaries intended as dissertation evidence may be
copied into `docs/demo_evidence/` after review.

## 2. Clean Installation

### Windows PowerShell

```powershell
git clone https://github.com/zewang-liverpool/luxllm-agent-demo.git
cd luxllm-agent-demo
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

The setup script validates an existing `.venv`. If it points to a Python
installation that has been removed, it rebuilds the environment using the
first available supported Python 3.10-3.12 interpreter.

### Linux / Barkla2

```bash
git clone https://github.com/zewang-liverpool/luxllm-agent-demo.git
cd luxllm-agent-demo
PYTHON_BIN=python3.11 bash scripts/setup.sh
```

`PYTHON_BIN` can be omitted to select the first available supported
interpreter. The Linux script also rebuilds an unusable `.venv`.

Runtime dependencies are declared in `requirements.txt`; development/test
dependencies are in `requirements-dev.txt`; the exact verified Windows Python
3.12 environment is in `requirements-lock-py312-win.txt`.

## 3. Repository and Unit Tests

The smoke test compiles every tracked Python utility without creating
`__pycache__`, validates the frozen viewer JSON, and runs the unit tests:

```powershell
.\.venv\Scripts\python.exe scripts\smoke_test.py
.\.venv\Scripts\python.exe -m pytest
```

Expected result:

```text
35 tests passed
```

GitHub Actions runs the same checks on Python 3.10 and 3.11 for pushes and pull
requests.  CI intentionally avoids LLM inference because model weights and GPU
availability are external resources.

## 4. Rule-Only End-to-End Smoke Match

This checks the real Lux runner and agent subprocess protocol without Ollama:

```powershell
.\.venv\Scripts\python.exe scripts\run_rule_smoke.py --seed 42
```

Verified local result on 11 July 2026:

```json
{
  "status": "complete",
  "seed": 42,
  "return_code": 0,
  "player_0_reward": 3,
  "player_1_reward": 2,
  "winner": "player_0"
}
```

The exact score is seed- and dependency-sensitive; the required acceptance
condition is `status=complete`, return code zero, and two parsed rewards.

## 5. Viewer Reproduction

From the repository root:

```powershell
python -m http.server 8000
```

Open:

```text
http://localhost:8000/docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html
```

The viewer uses only these tracked artefacts:

```text
data/isometric_replay_frames.json
data/run008_decision_trace_overlay.json
```

## 6. Ollama Preflight

Start Ollama and confirm the model before an LLM experiment:

```bash
ollama serve
ollama list
```

Supported experiment examples:

```text
qwen3:32b
deepseek-r1:32b
```

The runner stops before launching matches when Ollama is unreachable or the
requested model is absent.  Each run records the Git commit, Python version,
platform, installed packages, available Ollama model names, seed protocol, and
temperature in `environment.json`.

## 7. Matched-Seed, Role-Swapped Evaluation

The previous evaluation always assigned the LLM to `player_0`.  The new
protocol uses every seed twice: once with the LLM as `player_0`, and once as
`player_1`.  Fifty paired seeds therefore produce 100 matches.

```powershell
.\.venv\Scripts\python.exe scripts\run_paired_experiment.py `
  --model qwen3:32b `
  --pairs 50 `
  --seed-start 20260701 `
  --temperature 0.0 `
  --output-dir results\qwen3_32b_paired_100 `
  --resume
```

Run DeepSeek with the same seeds:

```powershell
.\.venv\Scripts\python.exe scripts\run_paired_experiment.py `
  --model deepseek-r1:32b `
  --pairs 50 `
  --seed-start 20260701 `
  --temperature 0.0 `
  --output-dir results\deepseek_r1_32b_paired_100 `
  --resume
```

Important controls:

- Lux environment seed: `20260701` through `20260750`.
- The same seed is passed to Ollama for both roles.
- Temperature is `0.0`.
- Role order alternates between seed pairs to reduce time-order bias.
- `--resume` skips completed `(seed, role)` combinations.
- A separate output directory is used for every match.

## 8. Barkla2 Slurm Submission

The supplied Slurm file is configured for Barkla2's `gpu-h100` partition,
`miniforge3/25.3.0-python3.12.10`, and `ollama/0.12.11`. It starts and stops an
isolated Ollama server inside the allocation. Prepare the shared Python virtual
environment first, then submit from the repository root:

```bash
sbatch --export=ALL,MODEL=qwen3:32b,PAIRS=50,SEED_START=20260701 \
  scripts/barkla_paired_experiment.sbatch
```

The runner also supports the supervisor-requested method comparison. Set
`METHOD=dtav` for the full project method or `METHOD=direct_prompt` for the
controlled baseline. The direct condition disables output normalisation,
strategy reuse, and risk-aware filtering while retaining the minimal legal
action adapter and logged emergency fallback. Use the same source commit and
seeds for both conditions. See
`docs/direct_prompt_dtav_experiment_guide.md` for the complete protocol.

If Python or Ollama is in a non-default location, additionally export
`PYTHON_BIN` or `OLLAMA_BASE_URL`.

## 9. Generated Evidence

Every paired experiment produces:

```text
results/<experiment>/
├── environment.json
├── match_history.jsonl
├── summary.json
└── runs/
    └── seed_<seed>_<role>/
        ├── result.json
        ├── logs/
        └── console.txt        # failures, or all runs with --keep-console
```

`summary.json` contains:

- overall and per-role win rates;
- Wilson 95% confidence intervals;
- an exact binomial test against 0.5;
- exact McNemar analysis for role-discordant seed pairs;
- a deterministic paired bootstrap interval for the player-role effect.

These statistics improve reporting but do not make the two LLM configurations
causally identical.  Hardware, model build, Ollama version, prompt, source
commit, and seed metadata must be reported alongside the result.

## 10. Offline Evidence Audit

With the two formal result directories extracted under
`archive/barkla_results/`, regenerate the verifier audit without Ollama or a
GPU:

```powershell
.\.venv\Scripts\python.exe tools\audit_verifier_interventions.py
.\.venv\Scripts\python.exe tools\validate_project_evidence.py
```

The first command writes deterministic Markdown, JSON, and CSV reports under
`reports/`. The second rejects stale primary claims and checks that the compact
formal report, verifier audit, and canonical documentation agree.

For the supervisor-requested direct dual-LLM archive, validate and regenerate
the supplementary reports locally without Ollama:

```powershell
$dual = "archive\barkla_results\dual_llm_9845992\results\9845992_qwen3_32b_vs_deepseek-r1_32b"
.\.venv\Scripts\python.exe tools\validate_dual_llm_result.py $dual
.\.venv\Scripts\python.exe tools\analyse_trace_evidence.py `
  --experiment "Dual LLM (Qwen vs DeepSeek)=$dual" `
  --json-output reports\dual_llm_trace_evaluation.json `
  --csv-output reports\dual_llm_trace_metrics.csv `
  --markdown-output reports\dual_llm_trace_evaluation.md `
  --figure-dir reports\dual_llm_figures
.\.venv\Scripts\python.exe tools\audit_verifier_interventions.py `
  --experiment "Dual LLM (Qwen vs DeepSeek)=$dual" `
  --output-prefix reports\dual_llm_verifier_audit
```

The retained archive is
`archive\barkla_transfer\9845992_qwen3_32b_vs_deepseek-r1_32b.tar.gz`
with SHA-256
`2B16B3C03EDA364F599F2EEF8884669124A1398D5BA1AAB7DE4709D9CF8A4EA7`.

## 11. Reproducibility Acceptance Checklist

- [ ] A new environment installs from a tracked dependency file.
- [ ] A broken `.venv` is detected and rebuilt by the setup script.
- [ ] `scripts/smoke_test.py` passes.
- [ ] `pytest` passes.
- [ ] The rule-only Lux match exits successfully.
- [ ] The viewer loads both tracked JSON files.
- [ ] Ollama preflight reports the requested model.
- [ ] All planned seed/role pairs are complete.
- [ ] `environment.json`, `match_history.jsonl`, and `summary.json` exist.
- [ ] The verifier intervention audit regenerates from retained raw logs.
- [ ] The project evidence consistency check passes.
- [ ] Only reviewed summaries are committed; raw large runs remain ignored.
