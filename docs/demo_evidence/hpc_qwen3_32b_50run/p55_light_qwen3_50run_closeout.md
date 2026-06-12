# v0.9-P5.5-light Qwen3-32B Strategic Planner 50-Run Closeout

## Status

PASS.

A 50-match controlled run was completed on Barkla2 using qwen3:32b as a target-aware strategic planner.

## Main Result

- Total matches: 50
- Player 0 wins: 35
- Player 1 wins: 15
- Draws: 0
- Average player 0 reward: 3.140
- Average player 1 reward: 1.860

## LLM Integration Metrics

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

## Comparison with P5.4b Basic Qwen3 Planner

The previous P5.4b qwen3:32b basic JSON planner achieved:

- 28 wins / 50 matches
- 56% win rate
- 0.927 strategy use rate
- 0.073 fallback rate
- 0 LLM errors
- average reward: 2.740 vs 2.260

The P5.5-light strategic planner achieved:

- 35 wins / 50 matches
- 70% win rate
- 0.960 strategy use rate
- 0.040 fallback rate
- 0 LLM errors
- average reward: 3.140 vs 1.860

## Interpretation

The P5.5-light result suggests that qwen3:32b benefits from a richer strategic interface. Compared with the basic intent-only planner, the target-aware schema with priority, risk, expected value, and lightweight arbitration improved both integration reliability and descriptive match performance.

This result should be reported as a controlled-run observation rather than a statistically significant claim. Its strongest contribution is that the LLM-agent interface can be made more reliable and more useful by moving beyond basic intent generation toward structured strategic planning.

## Paper Relevance

This evidence supports the paper's revised framing around LLM-agent observability and interface design:

- The system distinguishes between merely calling an LLM and actually using a parsed strategic plan.
- Target-aware structured outputs improve practical LLM-agent integration.
- Fallback rate and strategy-use rate provide measurable reliability indicators.
- Larger models require carefully designed runtime controls, not simply larger prompts.
