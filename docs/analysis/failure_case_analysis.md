# Failure Case Analysis

## 1. Overview

This document analyses representative failure cases and limitation cases in LuxLLM-Agent.

The purpose is not only to show that the system can run successfully, but also to examine where the current decision-trace and action-verification framework still has limitations.

This supports the main research question:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

Failure-case analysis is important for the COMP702 dissertation because it demonstrates critical reflection. A strong dissertation should not only report successful runs and aggregate metrics, but should also analyse cases where the system behaves imperfectly, relies on fallback, reuses stale plans, or produces strategically weak outcomes.

---

## 2. Why Failure Analysis is Needed

The current project already includes successful evidence:

* qwen3:32b completed 50 controlled runs with zero LLM errors;

* DeepSeek-R1-32B completed 50 controlled runs with zero LLM errors;

* the viewer can replay Run008;

* the LLM Decision Trace Overlay can display step-aligned decision information;

* the system records decision source, fallback status, LLM usage, and risk-filter information.

However, zero LLM errors does not mean that all decisions are optimal. It only means that the LLM interaction and execution pipeline did not fail at the parser or runtime level.

The system may still show limitations such as:

* weak high-level strategy;

* over-reliance on cached plans;

* fallback replacing LLM decisions;

* valid but strategically poor actions;

* mismatch between local tactical state and high-level objective;

* limited information in trace logs;

* replay frames and decision traces requiring careful alignment.

Failure analysis helps separate:

```text

execution stability

strategic quality

action validity

decision provenance

game outcome

```

This distinction is important for evaluating LLM-based game agents.

---

## 3. Evidence Sources

The failure analysis uses the following evidence sources:

```text

logs/decision_trace.jsonl

logs/decision_log.jsonl

data/run008_decision_trace_overlay.json

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

docs/demo_evidence/hpc_deepseek_r1_32b_50run/

docs/demo_evidence/llm_model_comparison_summary.md

docs/analysis/qwen3_vs_deepseek_analysis.md

```

The most useful trace fields include:

```text

step

phase

decision_source

llm_mode

llm_model

llm_called

fresh_llm_call

cached_llm_turn

stale_decision

llm_valid

llm_error

fallback_used

fallback_reason

risk_filter_changed

risk_filter_reason

unit_intent_count

unit_action_count

score_player_0

score_player_1

global_plan

intents

overlay_summary

```

These fields allow the analysis to connect a visible replay frame to the decision process that generated the action.

---

## 4. Case Analysis Template

Each failure case should be analysed using the following structure:

| Field                             | Description                                                      |
| --------------------------------- | ---------------------------------------------------------------- |
| Evidence source                   | Log file, viewer frame, or experiment summary                    |
| Step / frame                      | When the case occurred                                           |
| Observed state                    | What was visible or known at the time                            |
| LLM plan                          | What the LLM or cached plan proposed                             |
| Decision source                   | Fresh LLM, cached LLM, fallback, rule fallback, or rule player   |
| Verification / fallback behaviour | Whether the verifier, fallback, cache, or risk filter intervened |
| Outcome                           | What happened after the decision                                 |
| Interpretation                    | What the case reveals                                            |
| Possible improvement              | How the system could be improved                                 |

This structure will later be reused in the dissertation evaluation chapter.

---

## 5. Case 1: Valid LLM Plan but Limited Strategic Impact

### Evidence source

```text

data/run008_decision_trace_overlay.json

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

logs/decision_log.jsonl

```

### Example trace pattern

The LLM may produce a valid strategic plan such as:

```text

main_objective: explore_stale_tiles

risk_posture: low

reason: initial exploration to uncover potential scoring tiles

```

or:

```text

main_objective: explore_relic_candidates

risk_posture: low

reason: focus on relic candidates and scoring tile discovery

```

The plan is structurally valid and can be displayed in the viewer overlay. However, a valid plan does not necessarily lead to a strong game outcome.

### Interpretation

This case shows the difference between:

```text

valid LLM output

```

and:

```text

strong strategic decision

```

The LLM can produce a reasonable high-level objective, but the final outcome still depends on:

* map uncertainty;

* unit positions;

* opponent movement;

* energy constraints;

* local action planning;

* whether the target is actually valuable;

* whether the strategy is updated at the right time.

This means that LuxLLM-Agent should not be evaluated only by whether the LLM output is parseable or valid. Strategic quality requires additional analysis.

### Possible improvement

Future versions could include stronger value estimation for candidate targets. Instead of relying mainly on high-level LLM objectives, the system could combine LLM strategy with a rule-based scoring function that estimates:

* target distance;

* expected reward;

* risk from enemy units;

* energy cost;

* uncertainty of the tile;

* opportunity cost compared with other targets.

This would make the LLM plan more grounded in local game-state utility.

---

## 6. Case 2: Fallback Replaces or Supports LLM Decision

### Evidence source

```text

logs/decision_trace.jsonl

data/run008_decision_trace_overlay.json

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

```

### Example trace pattern

The trace may show fields such as:

```text

decision_source: rule_only

fallback_used: true

fallback_reason: force_rule_only

llm_mode: force_rule_only

```

or, in other controlled settings:

```text

decision_source: rule_fallback

fallback_used: true

```

This indicates that the final decision was not directly produced by a fresh LLM action. Instead, rule-based behaviour or fallback logic produced or repaired the action.

### Interpretation

This case shows that fallback is not simply an error. It is part of the system's safety design.

Fallback allows the agent to continue acting when:

* LLM mode is disabled;

* the LLM is not called at that frame;

* the LLM output cannot be used;

* cached plans are insufficient;

* rule-based action repair is safer;

* verification rejects a proposed plan.

This is important because LLM-based systems need a reliable execution layer. Without fallback, invalid or missing LLM decisions could lead to unstable agent behaviour.

However, fallback also complicates evaluation. If many actions come from fallback or rule-based logic, final match outcomes cannot be attributed only to the LLM.

### Possible improvement

The dissertation should clearly distinguish between:

```text

LLM strategic contribution

```

and:

```text

rule-based execution support

```

Future evaluation could report separate metrics for:

* fresh LLM decisions;

* cached LLM decisions;

* unit-level fallback;

* decision-source fallback;

* rule-player actions.

This would make the contribution of each component clearer.

---

## 7. Case 3: Cached LLM Plan May Become Stale

### Evidence source

```text

data/run008_decision_trace_overlay.json

logs/decision_trace.jsonl

logs/decision_log.jsonl

```

### Example trace pattern

The overlay may show:

```text

has_exact_llm_decision: false

has_recent_llm_decision: true

cached_llm_turn: true

llm_step_used: previous step

overlay_summary: Using most recent LLM plan from step X

```

This indicates that the current frame is using a recent LLM plan rather than a fresh LLM decision.

### Interpretation

Strategy caching is necessary because large LLM calls are slow. For example, the DeepSeek-R1-32B 50-run evidence shows an average LLM latency of approximately 4143.595 ms.

However, cached plans may become stale when:

* the opponent moves unexpectedly;

* a target becomes less useful;

* a unit's energy changes;

* local tactical risk increases;

* the map state changes;

* the original LLM objective no longer matches the best current action.

This case shows a trade-off between efficiency and adaptiveness.

### Possible improvement

Future versions could use event-triggered LLM refreshes. For example, the system could request a new LLM plan when:

* a unit reaches its target;

* enemy units become visible;

* the score changes;

* a relic candidate is confirmed or rejected;

* a cached plan has been used for too many steps;

* risk filter interventions increase.

This would reduce stale-plan behaviour without calling the LLM at every frame.

---

## 8. Case 4: Stable Execution but Different Model Outcomes

### Evidence source

```text

docs/analysis/qwen3_vs_deepseek_analysis.md

docs/demo_evidence/llm_model_comparison_summary.md

```

### Evidence

The 50-run comparison shows:

| Model           | Runs | player_0 wins | player_1 wins | player_0 win rate | LLM errors |
| --------------- | ---: | ------------: | ------------: | ----------------: | ---------: |
| qwen3:32b       |   50 |            35 |            15 |               70% |          0 |
| deepseek-r1:32b |   50 |            26 |            24 |               52% |          0 |

Both models completed 50 controlled runs with zero LLM errors, but their win rates were different.

### Interpretation

This case shows that execution stability and strategic performance are different.

Both models were stable under the same framework. However, qwen3:32b produced stronger gameplay outcomes in the current evidence.

This suggests that:

* the framework can support multiple LLM backends;

* model choice still affects strategic quality;

* zero errors do not imply equal performance;

* final gameplay outcome depends on both model behaviour and the surrounding verification/action pipeline.

### Possible improvement

Future analysis could compare the actual strategy distributions produced by each model. For example:

* how often each model selected exploration;

* how often each model selected relic candidate movement;

* whether one model produced more fallback-triggering outputs;

* whether one model used higher-risk plans;

* how model decisions affected score progression.

This would provide a deeper explanation of why the win rates differ.

---

## 9. Case 5: Viewer Trace Alignment Requires Careful Labelling

### Evidence source

```text

data/run008_decision_trace_overlay.json

tools/build_run008_decision_trace_overlay.py

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

```

### Evidence

The overlay generation result is:

```text

frames: 506

trace rows: 1009

llm decision rows: 23

matched step trace frames: 505

matched exact LLM frames: 23

matched recent LLM frames: 506

```

This shows that the script successfully aligns most replay frames with decision trace information.

### Interpretation

The alignment is useful for demonstration and inspection, but it must be labelled carefully. If the replay frames and logs come from different runs or experimental tags, then the overlay should be described as a replay-grounded inspection prototype rather than a perfect reconstruction of one exact match.

This matters for academic honesty and dissertation quality. The viewer is still valuable, but the dissertation should clearly state what data is aligned and what assumptions are made.

### Possible improvement

Future versions should save a unique run ID in both replay frames and decision trace logs. Then the overlay builder could verify that:

```text

replay.run_id == trace.run_id

```

or:

```text

replay.experiment_tag == trace.experiment_tag

```

This would make trace alignment more rigorous.

---

## 10. Cross-case Findings

The failure and limitation cases reveal several broader findings.

### 10.1 LLM validity is not the same as strategic quality

An LLM decision may be parseable and valid but still not optimal for the game state.

### 10.2 Fallback is both a strength and an evaluation complication

Fallback improves stability, but it makes it harder to attribute final behaviour only to the LLM.

### 10.3 Strategy caching is necessary but can introduce stale decisions

Caching reduces latency but may reduce adaptiveness when the game state changes quickly.

### 10.4 Model comparison should be interpreted at framework level

The qwen3 and DeepSeek comparison shows framework stability across models, not universal model superiority.

### 10.5 Replay-grounded inspection improves interpretability

The trace overlay helps connect decisions to frames, but trace alignment must be clearly documented.

---

## 11. Implications for System Design

The failure cases suggest the following design improvements:

| Limitation                           | Possible improvement                             |
| ------------------------------------ | ------------------------------------------------ |
| Valid but weak LLM plans             | Add stronger rule-based utility scoring          |
| Over-reliance on fallback            | Separate fallback metrics by level and reason    |
| Stale cached plans                   | Add event-triggered LLM refresh                  |
| Limited model comparison explanation | Compare strategy distributions across models     |
| Trace alignment assumptions          | Add shared run IDs across replay and logs        |
| Limited verifier visibility          | Log rejected actions and verifier decisions      |
| Limited viewer analysis              | Add timeline markers for LLM and fallback frames |

These improvements could be discussed as future work in the dissertation.

---

## 12. How to Use This in the Dissertation

This analysis can be used in the Evaluation and Discussion chapters.

Recommended placement:

```text

Chapter 6: Evaluation

- Include two or three representative failure cases.

- Use screenshots from the trace overlay.

- Discuss decision source, fallback, and cached-plan behaviour.

Chapter 7: Discussion

- Summarise limitations.

- Explain what the failure cases reveal.

- Discuss future work.

```

A strong dissertation should not claim that LuxLLM-Agent solves all problems of LLM-based game agents. Instead, it should show that the project provides tools to inspect and evaluate these problems.

---

## 13. Summary

The failure-case analysis shows that LuxLLM-Agent provides stable execution and useful decision tracing, but also has important limitations.

The most important findings are:

* valid LLM output does not guarantee strong gameplay;

* fallback improves reliability but complicates attribution;

* cached plans reduce latency but may become stale;

* different LLMs can be stable while producing different outcomes;

* replay-grounded inspection is valuable but requires careful trace alignment.

These findings strengthen the dissertation because they demonstrate critical analysis rather than only presenting successful results.

