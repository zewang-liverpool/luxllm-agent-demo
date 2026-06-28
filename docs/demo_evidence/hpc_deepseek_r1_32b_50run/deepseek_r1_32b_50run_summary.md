\# DeepSeek-R1-32B 50-run Evaluation Summary



\## Experiment Overview



This document summarises the DeepSeek-R1-32B comparison experiment for LuxLLM-Agent. The purpose of this experiment is not to build a model leaderboard, but to evaluate whether the current decision-trace and rule-based action-verification framework can support another reasoning-oriented LLM under the same Lux AI Season 3 setting.



\## Configuration



| Item | Value |

|---|---|

| Model | deepseek-r1:32b |

| Evaluation scale | 50 matches |

| LLM player | player\_0 |

| Opponent | rule-based fallback player |

| Platform | Barkla2 GPU |

| Framework | LuxLLM-Agent v0.9-E5.2 candidate-exploitation |

| Strategy cache | Enabled |

| Rule fallback | Enabled |

| Risk-aware action filter | Enabled |

| Candidate exploitation | Enabled |



\## Main Results



| Metric | Value |

|---|---:|

| Total runs | 50 |

| player\_0 wins | 26 |

| player\_1 wins | 24 |

| player\_0 win rate | 52% |

| Average player\_0 reward | 2.7 |

| Average player\_1 reward | 2.3 |

| Average fresh LLM calls | 33.2 |

| Average LLM strategy used | 27.24 |

| Average cached LLM turns | 412.62 |

| Average fallback count | 570.14 |

| Average LLM errors | 0.0 |

| Average LLM latency | 4143.595 ms |

| Maximum LLM latency | 10581.076 ms |

| Average trace steps | 1010.0 |



\## Decision Source Distribution



| Decision source | Count |

|---|---:|

| rule\_player | 25250 |

| fallback | 94 |

| rule\_fallback | 3163 |

| llm\_fresh | 1362 |

| cached\_llm | 20631 |



The total number of decision-source events is 50500. LLM-related decision events include both fresh LLM decisions and cached LLM decisions:



```text

llm\_fresh + cached\_llm = 1362 + 20631 = 21993


