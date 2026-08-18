# Decision-Trace and Action-Verification Evaluation

> **Scope note (18 August 2026):** this is a supplementary two-LLM study. It
> preserves the research framing used when the experiment was produced and
> does not replace the canonical Direct Prompt–DTAV comparison. See
> `docs/research_scope_20260814.md` and
> `reports/direct_prompt_vs_dtav_trace_analysis.md` for the current scope.

## Research question

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

This report treats backend win rate as a secondary outcome. The primary evidence concerns trace coverage, decision provenance, structured-output verification, safe action construction, fallback observability, and replay linkage.

Analysis code commit: `working-tree-after-3f7a7f5`.

## Primary framework evidence

| Metric | Dual LLM (Qwen vs DeepSeek) |
|---|---:|
| Completed matches | 100 |
| Matches with trace | 100 (100.0%) |
| Structured trace records | 106,317 |
| Agent-step trace completeness | 100.0% |
| LLM-call trace completeness | 100.0% |
| Replay-linkage coverage | 100.0% |
| LLM calls | 4,676 |
| Post-normalization structured-valid calls | 4,676 (100.0%) |
| Raw schema-valid calls | 4,105 (87.8%) |
| Normalization interventions | 571 (12.2%) |
| Cached-decision steps | 91,215 (89.7%) |
| Observable rule-fallback steps | 5,750 (5.7%) |
| Action fallback steps | 0 |
| Risk-filter changed steps | 15,721 (15.5%) |
| Risk-filter changed targets | 85,805 |
| Action-array shape validity | 100.0% |
| LLM timeouts / errors | 0 / 0 |
| Median LLM latency | 6080.3 ms |
| P95 LLM latency | 7050.0 ms |

## Decision provenance

### Dual LLM (Qwen vs DeepSeek)

| Decision source | LLM-agent steps |
|---|---:|
| `cached_llm` | 91,215 (89.7%) |
| `llm_fresh` | 4,676 (4.6%) |
| `rule_fallback` | 5,750 (5.7%) |

Fallback reasons are retained in the JSON report for audit and debugging.

## Player-model call coverage

### Dual LLM (Qwen vs DeepSeek)

| Player and model | Fresh calls | Valid after checks |
|---|---:|---:|
| `player_0|deepseek-r1:32b` | 1,192 | 1,192 |
| `player_0|qwen3:32b` | 1,149 | 1,149 |
| `player_1|deepseek-r1:32b` | 1,166 | 1,166 |
| `player_1|qwen3:32b` | 1,169 | 1,169 |

## Secondary matched outcome

These outcomes are retained as controlled context, not as a general model leaderboard.

| Experiment | Wins | Win rate | Match-level Wilson 95% CI | Match-level binomial p | Seed-clustered 95% CI | Seed-level sign p |
|---|---:|---:|---:|---:|---:|---:|
| Dual LLM (Qwen vs DeepSeek) | qwen3:32b 54 : deepseek-r1:32b 46 | 54.0% | [44.3%, 63.4%] | 0.4841 | [45.0%, 63.0%] | 0.5034 |

## Interpretation aligned with the research question

1. **Inspection:** Per-step provenance and replay-link fields quantify whether an evaluator can connect state, decision source, score context, and execution time after a match.
2. **Verification:** Raw-output parsing and schema checks expose where deterministic normalization was required before a proposal could enter the action planner.
3. **Safe execution:** Action-array shape, action fallback, timeout, error, and completed-match metrics show whether verified proposals remained executable under controlled runs.
4. **Evaluation:** Matched-seed outcomes demonstrate that the same trace-and-verification framework supports controlled backend evaluation; they do not establish a general LLM leaderboard.

## Limitations

The logs establish operational provenance and recorded verification events, not a complete causal explanation of agent behaviour. A zero action-fallback count means no downstream action failure was observed in these runs; it does not prove that every possible LLM proposal would be safe. Viewer-based inspection remains a qualitative complement to the quantitative coverage metrics.
