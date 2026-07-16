# Reproducibility Validation Report

Validation date: 16 July 2026
Branch: `codex/dissertation-demo-finalization`

## Closed Weaknesses

| Previous weakness | Resolution | Validation |
| --- | --- | --- |
| Missing runtime dependency specification | Added `requirements.txt`, `requirements-dev.txt`, `environment.yml`, `pyproject.toml`, and a verified Windows lock file | Fresh `.venv-repro` installed successfully |
| Incomplete GitHub runtime source | Promoted the complete v0.9-E1 runtime to `src/agent/`; added `lux_state.py` and `state_summarizer.py` | Source compilation and real Lux subprocess run passed |
| Broken legacy script paths | Replaced legacy `src/scripts` workflow with top-level setup, smoke, paired-experiment, and Slurm scripts | Commands executed from repository root |
| No one-command verification | Added `scripts/smoke_test.py` and `scripts/run_rule_smoke.py` | Both completed successfully |
| No automated tests | Added 23 unit tests and GitHub Actions for Python 3.10/3.11 | 23/23 unittest and pytest tests passed locally |
| Fixed `player_0` prompt | Prompt now derives the actual player from `team_id` | Unit test and two-role mock integration run passed |
| No matched-seed protocol | Added `scripts/run_paired_experiment.py`; every seed runs once per role | Mock seed 4242 completed as both roles |
| No statistical uncertainty | Added Wilson intervals, exact binomial tests, exact McNemar analysis, and paired bootstrap role-effect intervals | Statistics unit tests passed |
| Historical results not mechanically recomputable | Added `tools/recompute_reported_metrics.py` | Reproduced 70% and 52% from tracked JSON |
| Output/environment provenance incomplete | Every formal experiment records Git commit, Python/platform, package versions, Ollama models, temperature, seed policy, and per-run results | Verified in both 100-match formal experiments |
| Broken `.venv` could block clean reproduction | Setup scripts now detect and rebuild stale environments that point to removed Python installations | Windows recovery tested locally; Linux recovery added to CI |
| Verifier operation was reported only in aggregate | Added deterministic offline normalization and risk-filter intervention audit | Regenerated from both formal raw result directories |
| Documentation could regress to historical claims | Added a mechanical evidence-consistency validator to the smoke test | Formal reports, verifier audit, canonical chapters, and assembled draft agree |
| Local workspace contained many untracked legacy files | Archived 100 legacy files under ignored `archive/legacy-untracked-20260711/` with a manifest | `git status` is clean after archival |

## Local Validation Results

### Unit and repository checks

```text
pytest: 23 passed
unittest: 23 passed
viewer data: 505+ frames and 500+ trace items validated
project evidence consistency: passed
```

### Rule-only end-to-end match

```text
seed: 42
status: complete
return code: 0
score: player_0 3, player_1 2
```

### Mock LLM matched-role integration

```text
seed 4242, LLM as player_0: complete, score 5:0
seed 4242, LLM as player_1: complete, score 1:4 from the LLM perspective
paired seeds completed: 1
```

The mock server tests the complete HTTP, parsing, strategy, trace, Lux runner,
role swap, result collection, resume, and statistics pipeline. It is not an LLM
quality experiment and must not be reported as gameplay evidence.

## Recomputed Historical Statistics

| Model | Historical role | Matches | Wins | Win rate | Wilson 95% CI | Exact p vs 0.5 |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| qwen3:32b | player_0 | 50 | 35 | 70.0% | 56.2%-80.9% | 0.006600 |
| deepseek-r1:32b | player_0 | 50 | 26 | 52.0% | 38.5%-65.2% | 0.887725 |

These intervals resolve the absence of uncertainty reporting for each historical
run. They do not resolve player-side bias or establish a matched causal model
comparison.

## Completed Formal Large-model Validation

The Barkla2 paired experiments are complete:

| Model | Matched seeds | Role-swapped matches | LLM wins | Valid LLM calls |
| --- | ---: | ---: | ---: | ---: |
| qwen3:32b | 50 | 100 | 63 | 2,286/2,286 |
| deepseek-r1:32b | 50 | 100 | 60 | 2,305/2,305 |

Across the two experiments, all 200 matches completed and 206,591 structured
trace records were retained. The compact tracked evidence is under `reports/`;
the large raw results and SHA-256-verified transfer archives remain under the
ignored local `archive/` directory.

No additional large-model execution is required for technical closeout.
