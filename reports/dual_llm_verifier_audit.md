# Verifier Intervention Audit

This deterministic offline audit uses the retained formal experiment logs. It measures observable normalization and risk-filter interventions without making new model calls.

## Summary

| Metric | Dual LLM (Qwen vs DeepSeek) |
|---|---:|
| LLM calls | 4,676 |
| Raw schema-valid calls | 4,105 (87.8%) |
| Would fail strict schema without normalization | 571 |
| Normalization interventions | 571 |
| Risk-filter changed steps | 15,721 (15.5%) |
| Risk-filter changed targets | 85,805 |
| Mean changed targets per intervention step | 5.46 |

## Interpretation

1. A raw-schema rejection count is a deterministic formatting counterfactual: these responses would not pass the strict raw schema without the implemented normalization path.
2. A risk-filter intervention records that the deterministic verifier changed one or more proposed targets before action construction.
3. These counts demonstrate operational use of the verifier. They do not, by themselves, prove that an intervention improved match outcome.

## Per-model intervention coverage

### Dual LLM (Qwen vs DeepSeek)

| Model | Fresh calls | Raw-schema valid | Normalized | Risk-changed steps | Risk-changed targets |
|---|---:|---:|---:|---:|---:|
| `deepseek-r1:32b` | 2,358 | 2,358 | 0 | 8,128 | 42,330 |
| `qwen3:32b` | 2,318 | 1,747 | 571 | 7,593 | 43,475 |

## Dual LLM (Qwen vs DeepSeek)

### Normalization types

| Type | Calls |
|---|---:|
| `string_intent_shorthand` | 571 |

### Risk-filter interventions by decision source

| Decision source | Steps |
|---|---:|
| `cached_llm` | 14,541 |
| `llm_fresh` | 1,018 |
| `rule_fallback` | 162 |

### Risk-filter interventions by phase

| Phase | Steps |
|---|---:|
| `early_exploration` | 10,528 |
| `mid_exploit` | 3,426 |
| `final_push` | 1,767 |

### Recorded verifier reasons

| Reason | Steps |
|---|---:|
| original target inside visible-enemy risk radius | 15,721 |
| safer target selected | 15,721 |
