# Reviewer Response Notes: Qwen3-32B Controlled Evaluation Update

## Purpose

This document records how the LuxLLM-Agent paper should respond to earlier reviewer or supervisor concerns after the latest qwen3:32b controlled evaluation.

The key update is that the project is no longer limited to early small-model experiments. The main empirical evidence now comes from qwen3:32b controlled runs on Barkla2 GPU resources.

## Response to Model-Size Concerns

Earlier project stages used smaller Qwen2.5 models to validate the agent runtime, logging pipeline, replay viewer, fallback handling, and decision-trace generation. Those experiments remain useful as development evidence and lightweight local baselines, but they should not be presented as the main evidence for strategic LLM planning.

The revised paper should present qwen3:32b on Barkla2 as the main controlled evaluation setting. This larger-model setup allows the LLM to operate as a structured strategic planner rather than only as a lightweight intent generator.

## Response to LLM-Contribution Concerns

The updated system is not merely calling an LLM for post-hoc explanation. In the P5.5-light configuration, the LLM produces structured strategic plans containing:

- unit-level intents,
- target coordinates,
- priority scores,
- risk labels,
- expected-value estimates,
- and short natural-language reasons.

The runtime then parses, validates, arbitrates, executes, and logs these decisions. This makes the LLM contribution inspectable through strategy-use rate, fallback rate, LLM error count, and replay-grounded decision traces.

## Main Controlled Result

The latest main result is the P5.5-light qwen3:32b strategic planner.

In a 50-match controlled run, it achieved:

- Total matches: 50
- LLM-assisted player wins: 35
- Rule-controlled opponent wins: 15
- LLM-assisted player win rate: 70%
- Average player 0 reward: 3.140
- Average player 1 reward: 1.860
- Strategy use rate: 0.960
- Fallback rate: 0.040
- LLM errors: 0

This should be treated as the current main qwen3:32b controlled evaluation result.

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

The appropriate controlled-run claim is therefore:

In a 50-match controlled comparison, the target-aware qwen3:32b strategic planner improved descriptive win rate from 56% to 70%, reduced fallback rate from 7.3% to 4.0%, and maintained zero LLM errors.

This should be reported as descriptive controlled-run evidence rather than as a definitive statistical-significance claim.

## Earlier Controlled Configurations

The earlier strategy-diverse prompting configuration achieved 29 wins over 50 matches. The candidate-exploitation ablation achieved 26 wins over 50 matches. These results remain useful as development evidence and ablation context, but they should no longer be presented as the final main result.

The paper should treat them as earlier controlled configurations that helped validate the evaluation pipeline and design space.

## Response to Explainability Concerns

The paper should avoid broad claims of model explainability. The revised framing should use more precise language:

- replay-grounded decision traceability,
- inspectable decision provenance,
- decision-source logging,
- runtime-level observability.

The system records whether actions come from fresh LLM decisions, cached LLM decisions, fallback behaviour, or the rule-controlled opponent. These traces are aligned with replay frames, allowing users to inspect how the agent runtime behaves over time.

The system does not claim to fully explain the internal reasoning process of the LLM.

## Response to Evaluation Concerns

The updated evaluation is stronger because it includes controlled 50-match qwen3:32b experiments rather than only small-model development runs or cherry-picked demo examples.

The key metrics are:

- match outcome,
- reward distribution,
- strategy-use rate,
- fallback rate,
- LLM error count,
- and decision-source trace coverage.

These metrics show whether the LLM is actually used by the runtime and whether the system remains stable across repeated matches.

## Final Paper Positioning

The revised paper should present LuxLLM-Agent as a structured LLM-agent runtime and replay-grounded evaluation system for Lux AI Season 3.

The contribution is the combination of:

- structured LLM strategic planning,
- schema validation,
- rule-based arbitration,
- fallback safety,
- cached strategy reuse,
- decision-source logging,
- replay-grounded inspection,
- and controlled qwen3:32b evaluation.

The paper should not be framed as a state-of-the-art Lux AI competition bot or a competition-winning policy. Its strongest claim is that structured LLM-agent interfaces and runtime safeguards can make LLM planning more reliable, inspectable, and operationally useful in a competitive game-agent setting.
