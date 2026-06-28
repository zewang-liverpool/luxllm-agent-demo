\# LLM Model Comparison Summary



\## Purpose



This document compares two reasoning-oriented LLM backends used in LuxLLM-Agent: qwen3:32b and deepseek-r1:32b. The purpose of this comparison is not to rank LLMs as a general benchmark. Instead, the goal is to examine whether the proposed decision-trace and rule-based action-verification framework can support different LLMs and produce inspectable evaluation evidence.



\## Compared Settings



| Setting | Description |

|---|---|

| Rule-only baseline | Deterministic non-LLM control setting |

| qwen3:32b | Main LLM backend used in the original 50-run evidence |

| deepseek-r1:32b | Comparison LLM backend added for model-level evaluation |



\## 50-run Comparison



| Model | Runs | player\_0 wins | player\_1 wins | player\_0 win rate | LLM errors | Notes |

|---|---:|---:|---:|---:|---:|---|

| qwen3:32b | 50 | 35 | 15 | 70% | 0 | Main LLM setting |

| deepseek-r1:32b | 50 | 26 | 24 | 52% | 0 | Comparison LLM setting |



\## DeepSeek-R1-32B Additional Metrics



| Metric | Value |

|---|---:|

| Average player\_0 reward | 2.7 |

| Average player\_1 reward | 2.3 |

| Average fresh LLM calls | 33.2 |

| Average LLM strategy used | 27.24 |

| Average cached LLM turns | 412.62 |

| Average fallback count | 570.14 |

| Average LLM latency | 4143.595 ms |

| Maximum LLM latency | 10581.076 ms |



\## Decision Source Distribution for DeepSeek-R1-32B



| Decision source | Count |

|---|---:|

| rule\_player | 25250 |

| fallback | 94 |

| rule\_fallback | 3163 |

| llm\_fresh | 1362 |

| cached\_llm | 20631 |



Approximate LLM decision-source rate:



```text

(llm\_fresh + cached\_llm) / total decision-source events

= (1362 + 20631) / 50500

?43.55%


