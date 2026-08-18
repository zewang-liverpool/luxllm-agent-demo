# Direct Prompting versus DTAV Experiment Guide

This comparison implements the supervisor's 14 August 2026 suggestion to ask
whether direct prompting can solve the selected type of game before evaluating
the project-specific method.

## Conditions

Both conditions use the same:

- Lux AI Season 3 compact observation;
- LLM backend and model build;
- temperature and generation budget;
- environment and LLM seeds;
- LLM call schedule;
- matched-seed, role-swapped match protocol;
- official Lux action adapter and emergency deterministic fallback.

The **DTAV** condition enables deterministic output normalisation, strategy
reuse, and risk-aware target filtering. The **direct_prompt** condition disables
those three DTAV interventions. The minimal adapter remains because the Lux
runner only accepts fixed-shape numeric actions. Every fallback remains visible
in the logs, so this boundary must be stated when interpreting the baseline.

## Local mock acceptance test

This checks the complete two-match path without downloading an LLM:

```powershell
.\.venv\Scripts\python.exe scripts\run_mock_direct_prompt_smoke.py
```

Acceptance criteria:

- two matches complete;
- `environment.json` reports `decision_method: direct_prompt`;
- each `result.json` reports the same method;
- LLM decision and step-trace records contain `decision_method`;
- strategy cache, output normalisation, and the risk filter are disabled.

Validate the generated directory mechanically:

```powershell
.\.venv\Scripts\python.exe tools\validate_paired_method_result.py `
  results\mock_direct_prompt_role_swap_smoke `
  --method direct_prompt
```

## Barkla2 sanity runs

Submit both methods with one seed pair before a formal run:

```bash
COMMIT=$(git rev-parse HEAD)

sbatch --export=ALL,LUX_SOURCE_COMMIT="$COMMIT",MODEL=qwen3:32b,METHOD=direct_prompt,PAIRS=1,SEED_START=20260701 \
  scripts/barkla_paired_experiment.sbatch

sbatch --export=ALL,LUX_SOURCE_COMMIT="$COMMIT",MODEL=qwen3:32b,METHOD=dtav,PAIRS=1,SEED_START=20260701 \
  scripts/barkla_paired_experiment.sbatch
```

Validate completion, GPU allocation, log errors, method metadata, and LLM-call
validity before scaling up. Use `tools/validate_paired_method_result.py` on each
result directory; validation must pass before scaling up.

## Formal matched comparison

Use the same commit and seed range for both 50-pair jobs:

```bash
COMMIT=$(git rev-parse HEAD)

sbatch --export=ALL,LUX_SOURCE_COMMIT="$COMMIT",MODEL=qwen3:32b,METHOD=direct_prompt,PAIRS=50,SEED_START=20260701 \
  scripts/barkla_paired_experiment.sbatch

sbatch --export=ALL,LUX_SOURCE_COMMIT="$COMMIT",MODEL=qwen3:32b,METHOD=dtav,PAIRS=50,SEED_START=20260701 \
  scripts/barkla_paired_experiment.sbatch
```

Do not reuse an older DTAV result as the formal comparator if its source commit,
prompt, model build, runner version, or method metadata differs. This prevents a
code-version change from being mistaken for a method effect.

## Outcome comparison

After both jobs complete:

```bash
.venv/bin/python tools/compare_paired_experiments.py \
  results/<dtav-job>/match_history.jsonl \
  results/<direct-job>/match_history.jsonl \
  --left-name dtav \
  --right-name direct_prompt \
  --output results/<dtav-job>/dtav_vs_direct_prompt.json
```

Also run `tools/analyse_trace_evidence.py` separately on each result directory
to compare raw-schema validity, post-check validity, fallback, cache use,
risk-filter interventions, latency, action shape, and trace completeness.

## Interpretation boundary

The comparison can show differences under the recorded model, prompt, seed,
role, software, and hardware configuration. It does not prove that DTAV is
universally superior, that the trace exposes hidden model reasoning, or that
every possible future action is safe.
