# DeepSeek-R1-32B 50-run Evaluation Summary

## Experiment Overview

This document summarises the DeepSeek-R1-32B comparison experiment for LuxLLM-Agent. The purpose of this experiment is not to build a model leaderboard, but to evaluate whether the current decision-trace and rule-based action-verification framework can support another reasoning-oriented LLM under the same Lux AI Season 3 setting.

## Configuration

| Item | Value |
|---|---|
| Model | deepseek-r1:32b |
| Evaluation scale | 50 matches |
| LLM player | player_0 |
| Opponent | rule-based fallback player |
| Platform | Barkla2 GPU |
| Framework | LuxLLM-Agent v0.9-E5.2 candidate-exploitation |
| Strategy cache | Enabled |
| Rule fallback | Enabled |
| Risk-aware action filter | Enabled |
| Candidate exploitation | Enabled |

## Main Results

| Metric | Value |
|---|---:|
| Total runs | 50 |
| player_0 wins | 26 |
| player_1 wins | 24 |
| player_0 win rate | 52% |
| Average player_0 reward | 2.7 |
| Average player_1 reward | 2.3 |
| Average fresh LLM calls | 33.2 |
| Average LLM strategy used | 27.24 |
| Average cached LLM turns | 412.62 |
| Average fallback count | 570.14 |
| Average LLM errors | 0.0 |
| Average LLM latency | 4143.595 ms |
| Maximum LLM latency | 10581.076 ms |
| Average trace steps | 1010.0 |

## Decision Source Distribution

| Decision source | Count |
|---|---:|
| rule_player | 25250 |
| fallback | 94 |
| rule_fallback | 3163 |
| llm_fresh | 1362 |
| cached_llm | 20631 |

The total number of decision-source events is 50500. LLM-related decision events include both fresh LLM decisions and cached LLM decisions:

```text

llm_fresh + cached_llm = 1362 + 20631 = 21993
LLM decision-source rate = 21993 / 50500 ≈ 43.55%

fallback + rule_fallback = 94 + 3163 = 3257
fallback decision-source rate = 3257 / 50500 ≈ 6.45%
```

## Interpretation Limits

This experiment demonstrates stable execution of the DeepSeek-R1-32B backend within the frozen LuxLLM-Agent framework. The 52% player_0 win rate is a descriptive result for this controlled configuration. Because the LLM-assisted agent remained in the `player_0` role and no matched-seed role swapping or significance test was performed, the result should not be interpreted as a general model ranking or a causal estimate of model quality.

