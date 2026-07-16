# Verifier Intervention Audit

This deterministic offline audit uses the retained formal experiment logs. It measures observable normalization and risk-filter interventions without making new model calls.

## Summary

| Metric | Qwen3-32B | DeepSeek-R1-32B |
|---|---:|---:|
| LLM calls | 2,286 | 2,305 |
| Raw schema-valid calls | 1,766 (77.3%) | 2,305 (100.0%) |
| Would fail strict schema without normalization | 520 | 0 |
| Normalization interventions | 520 | 0 |
| Risk-filter changed steps | 5,590 (11.1%) | 7,090 (14.0%) |
| Risk-filter changed targets | 31,128 | 34,379 |
| Mean changed targets per intervention step | 5.57 | 4.85 |

## Interpretation

1. A raw-schema rejection count is a deterministic formatting counterfactual: these responses would not pass the strict raw schema without the implemented normalization path.
2. A risk-filter intervention records that the deterministic verifier changed one or more proposed targets before action construction.
3. These counts demonstrate operational use of the verifier. They do not, by themselves, prove that an intervention improved match outcome.

## Qwen3-32B

### Normalization types

| Type | Calls |
|---|---:|
| `string_intent_shorthand` | 520 |

### Risk-filter interventions by decision source

| Decision source | Steps |
|---|---:|
| `cached_llm` | 5,153 |
| `llm_fresh` | 361 |
| `rule_fallback` | 76 |

### Risk-filter interventions by phase

| Phase | Steps |
|---|---:|
| `early_exploration` | 4,959 |
| `mid_exploit` | 535 |
| `final_push` | 96 |

### Recorded verifier reasons

| Reason | Steps |
|---|---:|
| original target inside visible-enemy risk radius | 5,590 |
| safer target selected | 5,590 |

## DeepSeek-R1-32B

### Normalization types

| Type | Calls |
|---|---:|
| None observed | 0 |

### Risk-filter interventions by decision source

| Decision source | Steps |
|---|---:|
| `cached_llm` | 6,569 |
| `llm_fresh` | 445 |
| `rule_fallback` | 76 |

### Risk-filter interventions by phase

| Phase | Steps |
|---|---:|
| `early_exploration` | 4,884 |
| `mid_exploit` | 1,472 |
| `final_push` | 734 |

### Recorded verifier reasons

| Reason | Steps |
|---|---:|
| original target inside visible-enemy risk radius | 7,090 |
| safer target selected | 7,090 |
