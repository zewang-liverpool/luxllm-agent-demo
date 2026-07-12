# Recomputed Historical Metrics

Generated deterministically by `tools/recompute_reported_metrics.py` from tracked JSON evidence.

| Model | Matches | LLM wins | Win rate | Wilson 95% CI | Exact binomial p vs 0.5 |
| --- | ---: | ---: | ---: | ---: | ---: |
| qwen3:32b | 50 | 35 | 70.0% | [56.2%, 80.9%] | 0.006600 |
| deepseek-r1:32b | 50 | 26 | 52.0% | [38.5%, 65.2%] | 0.887725 |

> These historical experiments kept the LLM as `player_0` and were not matched by seed. The intervals are valid descriptive summaries of each run, not evidence of a causal model ranking.
