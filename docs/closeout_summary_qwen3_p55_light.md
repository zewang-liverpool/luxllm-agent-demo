# v0.9-P5.5-light Qwen3-32B Strategic Planner 50-Run Closeout

## Status

PASS.

A 50-match controlled run was completed on Barkla2 using qwen3:32b as a target-aware strategic planner for the LLM-assisted player.

## Main Result

- Total matches: 50
- LLM-assisted player wins: 35
- Rule-controlled opponent wins: 15
- Draws: 0
- LLM-assisted player win rate: 70%
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

## Comparison with Previous Basic Qwen3 Planner

The previous qwen3:32b basic JSON planner achieved:

- Total matches: 50
- LLM-assisted player wins: 28
- Rule-controlled opponent wins: 22
- LLM-assisted player win rate: 56%
- Average player 0 reward: 2.740
- Average player 1 reward: 2.260
- Strategy use rate: 0.927
- Fallback rate: 0.073
- LLM errors: 0

The P5.5-light strategic planner achieved:

- Total matches: 50
- LLM-assisted player wins: 35
- Rule-controlled opponent wins: 15
- LLM-assisted player win rate: 70%
- Average player 0 reward: 3.140
- Average player 1 reward: 1.860
- Strategy use rate: 0.960
- Fallback rate: 0.040
- LLM errors: 0

## Interpretation

The P5.5-light result suggests that qwen3:32b benefits from a richer structured LLM-agent interface. Compared with the previous basic intent-only planner, the target-aware schema with priority, risk, expected value, and lightweight rule arbitration improved both integration reliability and descriptive match performance.

This result should be reported as controlled-run evidence rather than as a definitive statistical-significance claim. The strongest conclusion is that structured strategic planning makes the LLM output more operationally useful for the agent runtime.

## Paper Relevance

This result supports the revised paper framing:

- The system is not only a replay viewer or a small-model demo.
- The LLM acts as a structured strategic planner.
- The runtime validates, parses, arbitrates, and logs LLM decisions.
- Strategy-use rate, fallback rate, and LLM errors provide measurable reliability indicators.
- Larger-model evaluation on Barkla2 directly addresses earlier concerns about small-model limitations.
- The project should be framed as an inspectable LLM-assisted game-agent runtime with replay-grounded evaluation, not as a state-of-the-art Lux AI competition bot.
