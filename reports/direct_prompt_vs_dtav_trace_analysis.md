# Decision-Trace and Action-Verification Evaluation

## Research question

> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent, long-horizon, and rule-constrained strategy game such as Lux AI Season 3, and how can the project-specific Decision-Trace and Action-Verification (DTAV) method address the observed limitations?

This report treats backend win rate as a secondary outcome. The primary evidence concerns trace coverage, decision provenance, structured-output verification, safe action construction, fallback observability, and replay linkage.

Analysis code commit: `354c30beb1a179904fc52b53a577fe09c0fbfdf1`.

## Primary framework evidence

| Metric | direct_prompt | dtav |
|---|---:|---:|
| Completed matches | 100 | 100 |
| Matches with trace | 100 (100.0%) | 100 (100.0%) |
| Structured trace records | 104,005 | 103,932 |
| Agent-step trace completeness | 100.0% | 100.0% |
| LLM-call trace completeness | 100.0% | 100.0% |
| Replay-linkage coverage | 100.0% | 100.0% |
| LLM calls | 2,284 | 2,325 |
| Post-normalization structured-valid calls | 1,966 (86.1%) | 2,323 (99.9%) |
| Raw schema-valid calls | 1,969 (86.2%) | 1,767 (76.0%) |
| Normalization interventions | 315 (13.8%) | 558 (24.0%) |
| Cached-decision steps | 0 (0.0%) | 45,645 (89.8%) |
| Observable rule-fallback steps | 48,576 (95.5%) | 2,833 (5.6%) |
| Action fallback steps | 0 | 0 |
| Risk-filter changed steps | 0 (0.0%) | 5,706 (11.2%) |
| Risk-filter changed targets | 0 | 29,741 |
| Action-array shape validity | 100.0% | 100.0% |
| LLM timeouts / errors | 0 / 0 | 0 / 0 |
| Median LLM latency | 3448.1 ms | 3389.8 ms |
| P95 LLM latency | 6353.6 ms | 6369.0 ms |

## Decision provenance

### direct_prompt

| Decision source | LLM-agent steps |
|---|---:|
| `llm_fresh` | 2,284 (4.5%) |
| `rule_fallback` | 101 (0.2%) |
| `rule_fallback_no_cache` | 48,475 (95.3%) |

Fallback reasons are retained in the JSON report for audit and debugging.

### dtav

| Decision source | LLM-agent steps |
|---|---:|
| `cached_llm` | 45,645 (89.8%) |
| `llm_fresh` | 2,325 (4.6%) |
| `rule_fallback` | 2,833 (5.6%) |

Fallback reasons are retained in the JSON report for audit and debugging.

## Player-model call coverage

### direct_prompt

| Player and model | Fresh calls | Valid after checks |
|---|---:|---:|
| `player_0|qwen3:32b` | 1,129 | 1,080 |
| `player_1|qwen3:32b` | 1,155 | 886 |

### dtav

| Player and model | Fresh calls | Valid after checks |
|---|---:|---:|
| `player_0|qwen3:32b` | 1,141 | 1,139 |
| `player_1|qwen3:32b` | 1,184 | 1,184 |

## Interpretation aligned with the research question

1. **Inspection:** Per-step provenance and replay-link fields quantify whether an evaluator can connect state, decision source, score context, and execution time after a match.
2. **Verification:** Raw-output parsing and schema checks expose where deterministic normalization was required before a proposal could enter the action planner.
3. **Safe execution:** Action-array shape, action fallback, timeout, error, and completed-match metrics show whether verified proposals remained executable under controlled runs.
4. **Evaluation:** Matched-seed outcomes demonstrate that the same trace-and-verification framework supports controlled backend evaluation; they do not establish a general LLM leaderboard.

## Limitations

The logs establish operational provenance and recorded verification events, not a complete causal explanation of agent behaviour. A zero action-fallback count means no downstream action failure was observed in these runs; it does not prove that every possible LLM proposal would be safe. Viewer-based inspection remains a qualitative complement to the quantitative coverage metrics.
