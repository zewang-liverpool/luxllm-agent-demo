# LLM Model Comparison Summary

## Purpose

This document compares two reasoning-oriented LLM backends used in LuxLLM-Agent: qwen3:32b and deepseek-r1:32b. The purpose of this comparison is not to rank LLMs as a general benchmark. Instead, the goal is to examine whether the proposed decision-trace and rule-based action-verification framework can support different LLMs and produce inspectable evaluation evidence.

## Compared Settings

| Setting | Description |
|---|---|
| Rule-only baseline | Deterministic non-LLM control setting |
| qwen3:32b | Main LLM backend used in the original 50-run evidence |
| deepseek-r1:32b | Comparison LLM backend added for model-level evaluation |

## 50-run Comparison

| Model | Runs | player_0 wins | player_1 wins | player_0 win rate | LLM errors | Notes |
|---|---:|---:|---:|---:|---:|---|
| qwen3:32b | 50 | 35 | 15 | 70% | 0 | Main LLM setting |
| deepseek-r1:32b | 50 | 26 | 24 | 52% | 0 | Comparison LLM setting |

## DeepSeek-R1-32B Additional Metrics

| Metric | Value |
|---|---:|
| Average player_0 reward | 2.7 |
| Average player_1 reward | 2.3 |
| Average fresh LLM calls | 33.2 |
| Average LLM strategy used | 27.24 |
| Average cached LLM turns | 412.62 |
| Average fallback count | 570.14 |
| Average LLM latency | 4143.595 ms |
| Maximum LLM latency | 10581.076 ms |

## Decision Source Distribution for DeepSeek-R1-32B

| Decision source | Count |
|---|---:|
| rule_player | 25250 |
| fallback | 94 |
| rule_fallback | 3163 |
| llm_fresh | 1362 |
| cached_llm | 20631 |

Approximate LLM decision-source rate:

```text

(llm_fresh + cached_llm) / total decision-source events

= (1362 + 20631) / 50500

approximately 43.55%
```

Approximate fallback decision-source rate:

```text
(fallback + rule_fallback) / total decision-source events
= (94 + 3163) / 50500
approximately 6.45%
```

## Interpretation Limits

The two 50-run results demonstrate that the same decision-trace and action-verification framework can support both backends. They are descriptive controlled-run outcomes rather than a general model ranking. In the reported evidence, the LLM-assisted configuration occupied `player_0` and the rule-controlled opponent occupied `player_1`; roles were not swapped under matched seeds, and no confidence intervals or hypothesis tests were reported.

