# qwen3:32b GPU Evidence Index

## Completed Evidence

### v3 GPU sanity

Purpose:
- Verify qwen3:32b GPU inference.
- Verify `/api/chat` with `think=false`.
- Verify structured unit-intent parsing.

Key result:
- qwen3:32b structured planning chain was successfully connected.
- LLM strategies were accepted by the agent and reused through cache.

### v3 5-run controlled evaluation

Run directory:
docs/hpc_qwen3_gpu_v3_5run/20260610_173327_qwen3_32b_gpu_v3_5run_job8991741

Summary:
- player_0 wins: 1/5
- player_1 wins: 4/5
- avg_llm_errors: 0.0
- avg_llm_strategy_used: 14.8
- avg_cached_llm_turns: 449.8

### E4 strategy-diversity 5-run controlled evaluation

Run directory:
docs/hpc_qwen3_gpu_e4_5run/20260610_174731_qwen3_32b_gpu_e4_5run_job8993933

Summary:
- player_0 wins: 3/5
- player_1 wins: 2/5
- avg_llm_errors: 0.0
- avg_llm_strategy_used: 15.8
- avg_cached_llm_turns: 489.2
- avg_fallback_count: 505.0

Interpretation:
- E4 improved the preliminary 5-match result from 1/5 to 3/5 wins.
- E4 preserved zero LLM errors.
- E4 removed aggregate rule_fallback usage and produced cleaner LLM decision traces.

## Running Evidence

### E4 strategy-diversity 50-run controlled evaluation

Purpose:
- Test whether the E4 improvement remains stable at a larger scale.
- Produce paper-level controlled evaluation evidence.

Expected output:
docs/hpc_qwen3_gpu_e4_50run/<run_dir>/summary_50run.json
docs/hpc_qwen3_gpu_e4_50run/<run_dir>/match_history_50run.jsonl

---

## E5.2 Candidate-Exploitation 50-run Ablation

Run directory:

`docs/hpc_qwen3_gpu_e52_50run/20260610_221857_qwen3_32b_gpu_e52_50run_job8997743`

Summary:

- Total runs: 50
- Player 0 wins: 26
- Player 1 wins: 24
- Avg fresh LLM calls: 25.62
- Avg LLM strategy used: 25.54
- Avg cached LLM turns: 479.46
- Avg fallback count: 505.0
- Avg LLM errors: 0.0
- Avg LLM latency: 4893.165 ms
- Max LLM latency: 5511.419 ms
- Avg trace steps: 1010.0
- Avg stale decision count: 479.46
- Decision source counts:
  - rule_player: 25250
  - llm_fresh: 1277
  - cached_llm: 23973

Interpretation:

E5.2 was a technically stable candidate-exploitation ablation. It completed all 50 matches with zero LLM errors and full trace coverage. However, it did not outperform the E4 strategy-diversity configuration at the 50-match scale. E4 therefore remains the main reported configuration, while E5.2 is retained as an ablation showing that more aggressive candidate-target exploitation does not necessarily improve long-horizon match performance.

Paper usage:

- Use E4 strategy-diversity as the main controlled result.
- Use E5.2 candidate-exploitation as a supplementary ablation.
- Do not claim that E5.2 improves the agent.
- Present E5.2 as evidence that the system is stable enough to evaluate design variants.
