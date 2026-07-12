# Decision-Trace and Action-Verification Evaluation

## Research question

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

This report treats backend win rate as a secondary outcome. The primary evidence concerns trace coverage, decision provenance, structured-output verification, safe action construction, fallback observability, and replay linkage.

Analysis code commit: `04c346c`.

## Primary framework evidence

| Metric | Qwen3-32B | DeepSeek-R1-32B |
|---|---:|---:|
| Completed matches | 100 | 100 |
| Matches with trace | 100 (100.0%) | 100 (100.0%) |
| Structured trace records | 103,286 | 103,305 |
| Agent-step trace completeness | 100.0% | 100.0% |
| LLM-call trace completeness | 100.0% | 100.0% |
| Replay-linkage coverage | 100.0% | 100.0% |
| LLM calls | 2,286 | 2,305 |
| Post-normalization structured-valid calls | 2,286 (100.0%) | 2,305 (100.0%) |
| Raw schema-valid calls | 1,766 (77.3%) | 2,305 (100.0%) |
| Normalization interventions | 520 (22.7%) | 0 (0.0%) |
| Cached-decision steps | 45,399 (89.9%) | 45,380 (89.9%) |
| Observable rule-fallback steps | 2,815 (5.6%) | 2,815 (5.6%) |
| Action fallback steps | 0 | 0 |
| Risk-filter changed steps | 5,590 (11.1%) | 7,090 (14.0%) |
| Risk-filter changed targets | 31,128 | 34,379 |
| Action-array shape validity | 100.0% | 100.0% |
| LLM timeouts / errors | 0 / 0 | 0 / 0 |
| Median LLM latency | 3785.7 ms | 3508.6 ms |
| P95 LLM latency | 4293.3 ms | 3856.6 ms |

## Decision provenance

### Qwen3-32B

| Decision source | LLM-agent steps |
|---|---:|
| `cached_llm` | 45,399 (89.9%) |
| `llm_fresh` | 2,286 (4.5%) |
| `rule_fallback` | 2,815 (5.6%) |

Fallback reasons are retained in the JSON report for audit and debugging.

### DeepSeek-R1-32B

| Decision source | LLM-agent steps |
|---|---:|
| `cached_llm` | 45,380 (89.9%) |
| `llm_fresh` | 2,305 (4.6%) |
| `rule_fallback` | 2,815 (5.6%) |

Fallback reasons are retained in the JSON report for audit and debugging.

## Interpretation aligned with the research question

1. **Inspection:** Per-step provenance and replay-link fields quantify whether an evaluator can connect state, decision source, score context, and execution time after a match.
2. **Verification:** Raw-output parsing and schema checks expose where deterministic normalization was required before a proposal could enter the action planner.
3. **Safe execution:** Action-array shape, action fallback, timeout, error, and completed-match metrics show whether verified proposals remained executable under controlled runs.
4. **Evaluation:** Matched-seed outcomes demonstrate that the same trace-and-verification framework supports controlled backend evaluation; they do not establish a general LLM leaderboard.

## Limitations

The logs establish operational provenance and recorded verification events, not a complete causal explanation of agent behaviour. A zero action-fallback count means no downstream action failure was observed in these runs; it does not prove that every possible LLM proposal would be safe. Viewer-based inspection remains a qualitative complement to the quantitative coverage metrics.
