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

E5.2 was a technically stable candidate-exploitation ablation. It completed all 50 matches with zero LLM errors and full trace coverage. However, it did not outperform the earlier strategy-diversity configuration at the 50-match scale. After the later P5.5-light qwen3:32b strategic-planner run, both E4 and E5.2 should be treated as earlier controlled configurations rather than the final main result.

Paper usage:

- Treat E4 strategy-diversity as an earlier controlled configuration.
- Treat E5.2 candidate-exploitation as a supplementary ablation.
- Use P5.5-light qwen3:32b strategic planner as the current main controlled result.
- Do not claim that E5.2 improves the agent.
- Present E4 and E5.2 as evidence that the system is stable enough to evaluate design variants.

---

## P5.5-light Qwen3-32B Strategic Planner Controlled Run

### Status

PASS.

A 50-match controlled run was completed on Barkla2 using `qwen3:32b` as a target-aware strategic planner.

### Result Summary

- Total matches: 50
- LLM-assisted player wins: 35
- Rule-controlled opponent wins: 15
- Draws: 0
- LLM-assisted player win rate: 70%
- Average player 0 reward: 3.140
- Average player 1 reward: 1.860

### LLM Integration Metrics

- Total fresh LLM calls: 1249
- Total LLM strategy used: 1199
- Total fallback count: 50
- Total LLM errors: 0
- Strategy use rate: 0.960
- Fallback rate: 0.040
- Average fresh LLM calls per match: 24.980
- Average strategy-used calls per match: 23.980
- Average fallback count per match: 1.000
- Average LLM errors per match: 0.000

### Comparison with Previous Basic Qwen3 Planner

The previous qwen3:32b basic JSON planner achieved 28 wins and 22 losses over 50 matches, corresponding to a 56% descriptive win rate. It achieved a strategy-use rate of 0.927, a fallback rate of 0.073, and zero LLM errors.

The P5.5-light strategic planner achieved 35 wins and 15 losses over 50 matches, corresponding to a 70% descriptive win rate. It improved the strategy-use rate to 0.960, reduced fallback rate to 0.040, and maintained zero LLM errors.

### Paper Interpretation

This result should be used as the main qwen3:32b controlled evaluation result. It supports the claim that a structured strategic LLM-agent interface can make larger-model planning more operationally useful than a basic intent-only JSON planner.

This should be reported as controlled-run evidence, not as a state-of-the-art Lux AI performance claim or a definitive statistical-significance claim.


