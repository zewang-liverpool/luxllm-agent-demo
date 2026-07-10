# LLM Decision Pipeline

## 1. Overview

The LLM decision pipeline is the part of LuxLLM-Agent that connects structured game-state information to strategic LLM-generated plans and verified Lux AI Season 3 actions.

The key design principle is:

> The LLM output is treated as a strategic proposal, not as a directly executable game action.

This is important because LLM outputs may be incomplete, unstable, invalid, or inconsistent with the current game state. Instead of allowing the LLM to directly control the environment, LuxLLM-Agent places the LLM inside a controlled decision pipeline:

```text

Structured Game State

        |

        v

Prompt Construction

        |

        v

LLM Strategic Decision

        |

        v

Structured Output Parsing

        |

        v

Plan Validation

        |

        v

Fallback / Cache / Risk-aware Filtering

        |

        v

Action Planning

        |

        v

Executable Lux AI Action

```

This pipeline supports the project research question:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

---

## 2. Role of the LLM

The LLM is used as a high-level strategic planner.

It is not responsible for directly producing raw Lux AI action arrays. Instead, it produces structured strategic information such as:

* current game phase;

* main objective;

* risk posture;

* unit-level intent;

* target location;

* priority;

* expected value;

* reason.

For example, the LLM may suggest that a unit should:

```text

MOVE_TO_RELIC_CANDIDATE

```

or:

```text

EXPLORE_STALE_TILE

```

These are strategic intents. They still need to be checked and converted into legal Lux AI Season 3 actions by deterministic components.

Relevant files:

```text

llm_decider.py

agent.py

state_summarizer.py

action_planner.py

rule_policy.py

```

---

## 3. Input: Structured Game State

The LLM receives a structured summary of the game state rather than raw observation data.

The state summary may include:

* current step;

* match phase;

* score context;

* unit positions;

* unit energy;

* known relic candidates;

* known scoring tiles;

* unexplored or stale tiles;

* nearby enemy units;

* risk context;

* available units;

* previous strategy or cached plan.

The goal of this step is to make the prompt compact, relevant, and stable.

This supports the first sub-research question:

> How can raw Lux AI Season 3 observations be transformed into compact structured inputs for LLM-based strategic decision making?

The structured input reduces prompt noise and helps the LLM reason at the level of strategy rather than raw environment mechanics.

---

## 4. Prompt Construction

The prompt construction stage turns the structured state summary into an instruction for the LLM.

The prompt should encourage the LLM to return structured strategic output rather than free-form text. The intended output format includes:

```text

global_plan:

  phase

  main_objective

  risk_posture

  reason

unit_intents:

  unit_id

  intent

  target

  priority

  risk

  expected_value

  reason

```

The prompt is designed to make the LLM decision:

* interpretable;

* parseable;

* comparable across models;

* suitable for rule-based verification;

* useful for logging and replay-grounded inspection.

This structure is important because unstructured natural-language responses are difficult to verify automatically.

---

## 5. LLM Backend Configuration

The LLM backend is configurable through environment variables.

Main configuration:

```text

LUX_LLM_MODEL=qwen3:32b

LUX_LLM_MODEL=deepseek-r1:32b

```

The project currently includes controlled 50-run evidence for:

| Model           | Role                   |
| --------------- | ---------------------- |
| qwen3:32b       | Main LLM backend       |
| deepseek-r1:32b | Comparison LLM backend |

The purpose of comparing multiple LLM backends is not to create a general LLM leaderboard. Instead, it tests whether the same decision-trace and action-verification framework can support different reasoning-oriented models.

This supports the dissertation argument that LuxLLM-Agent is a framework for inspecting and evaluating LLM-based agents, rather than a single hard-coded LLM demo.

---

## 6. LLM Call Scheduling

The system does not need to call the LLM at every game step.

Calling a large LLM at every step would be expensive and slow. Instead, LuxLLM-Agent uses controlled LLM call scheduling and strategy reuse.

A fresh LLM call may occur when:

* the match reaches a decision interval;

* the game phase changes;

* the previous plan is stale;

* an event refresh is triggered;

* the current strategy is no longer suitable.

Between fresh LLM calls, the agent may use a cached plan.

Important logged fields include:

```text

fresh_llm_call

cached_llm_turn

stale_decision

last_llm_step

llm_latency_ms

```

This design reduces latency while still allowing the LLM to provide high-level strategic direction.

---

## 7. Structured Output Parsing

After the LLM returns a response, the system parses it into structured internal data.

The parser checks whether the output contains usable fields such as:

* global plan;

* main objective;

* unit intents;

* target positions;

* priorities;

* risk posture;

* reasons.

If the output is missing fields, malformed, or unusable, the system records the issue and may trigger fallback behaviour.

Important logged fields include:

```text

llm_valid

llm_error

timed_out

fallback_used

fallback_reason

```

This parsing stage is an important reliability boundary. It prevents invalid LLM output from being passed directly to the action planner.

---

## 8. Plan Validation

The parsed LLM plan must be checked against the current game state.

Validation may consider:

* whether the referenced unit exists;

* whether the unit is active;

* whether the target is inside the map;

* whether the target is reachable;

* whether the intent is recognised;

* whether the plan conflicts with known rules;

* whether the plan is too risky.

If the plan is usable, it can be passed to the action planner. If not, it may be repaired or replaced by fallback logic.

This step is central to the second sub-research question:

> How can rule-based verification, fallback mechanisms, and strategy caching reduce invalid or unstable LLM-generated decisions?

---

## 9. Fallback Behaviour

Fallback behaviour is used when the LLM cannot provide a usable decision.

Fallback may occur when:

* LLM use is disabled;

* rule-only mode is enabled;

* the LLM times out;

* the LLM output is invalid;

* the LLM response cannot be parsed;

* the plan fails verification;

* a safer rule-based action is required.

Fallback-related decision sources include:

```text

fallback

rule_fallback

rule_player

```

Fallback is not a weakness of the system. It is part of the safety and stability design. It ensures that the agent continues to act even when the LLM decision is unavailable or unsafe.

---

## 10. Strategy Cache

The strategy cache allows the system to reuse recent LLM decisions across multiple steps.

This is useful because large LLMs may have high latency. In the DeepSeek-R1-32B 50-run evidence, the average LLM latency was approximately 4143.595 ms, which makes step-by-step LLM calls impractical.

The cache helps reduce:

* repeated LLM calls;

* latency overhead;

* unnecessary strategic changes;

* runtime instability.

Cache-related fields include:

```text

cached_llm_turn

cache_used

stale_decision

last_llm_step

```

A cached LLM plan can still be inspected through the decision trace overlay. This is important because even when no fresh LLM call occurs at a frame, the agent may still be acting under a recent LLM plan.

---

## 11. Risk-aware Action Filtering

The risk-aware action filter checks whether the planned action appears unsafe.

It may detect cases such as:

* moving into dangerous areas;

* choosing a target near enemy units;

* sending a unit toward low-value or high-risk areas;

* using a plan that conflicts with local tactical conditions.

Relevant logged fields include:

```text

risk_filter_enabled

risk_filter_changed

risk_filter_reason

risk_filter_changed_targets

risk_filter_events_count

```

The risk filter gives the system another layer of control between LLM strategy and action execution.

---

## 12. Action Planning

Once a strategic plan has passed parsing, validation, fallback, caching, and risk filtering, the action planner converts it into executable Lux AI Season 3 actions.

For example, a unit intent such as:

```text

EXPLORE_STALE_TILE

```

must be converted into a concrete move action.

The action planner considers:

* current unit location;

* target location;

* legal movement directions;

* unit energy;

* nearby objects;

* available action slots;

* fallback behaviour when no valid action exists.

This step converts high-level strategy into low-level environment actions.

---

## 13. Decision Trace Logging

Every step of the pipeline produces logs that support inspection and evaluation.

Important log files include:

```text

logs/decision_trace.jsonl

logs/decision_log.jsonl

logs/ablation_metrics.jsonl

logs/match_history.jsonl

```

The decision trace records information such as:

```text

step

phase

decision_source

llm_mode

llm_model

llm_called

llm_valid

llm_error

fallback_used

fallback_reason

cache_used

stale_decision

risk_filter_changed

unit_intent_count

unit_action_count

score_player_0

score_player_1

```

These logs make it possible to analyse not only what happened, but why a decision was made and which system component produced it.

---

## 14. Replay-grounded Inspection

The LLM decision pipeline is connected to the viewer through the decision trace overlay.

Relevant files:

```text

tools/build_run008_decision_trace_overlay.py

data/run008_decision_trace_overlay.json

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

```

The overlay shows:

* frame and step;

* phase;

* decision source;

* LLM model;

* current objective;

* risk posture;

* fallback status;

* risk filter status;

* score context;

* unit intents.

This supports the third sub-research question:

> How can replay-grounded decision traces help analyse the relationship between LLM strategy, decision source, action execution, and game outcome?

The viewer makes the LLM decision pipeline visible and easier to evaluate.

---

## 15. Evidence from Current Experiments

The pipeline has been tested with two LLM backends.

| Model           | Runs | player_0 wins | player_1 wins | player_0 win rate | LLM errors |
| --------------- | ---: | ------------: | ------------: | ----------------: | ---------: |
| qwen3:32b       |   50 |            35 |            15 |               70% |          0 |
| deepseek-r1:32b |   50 |            26 |            24 |               52% |          0 |

Both models completed 50 controlled Lux AI Season 3 runs with zero LLM errors.

This suggests that the decision pipeline can support different reasoning-oriented LLM backends while keeping execution stable through parsing, fallback, caching, and rule-based action verification.

---

## 16. Design Benefits

The LLM decision pipeline provides several benefits.

### 16.1 Inspectability

The system records the decision source, LLM plan, fallback status, and action context. This makes the agent easier to inspect than a black-box LLM controller.

### 16.2 Stability

Fallback and rule-based verification reduce the risk of invalid LLM outputs causing invalid actions.

### 16.3 Efficiency

Strategy caching reduces the number of expensive LLM calls.

### 16.4 Comparability

The same pipeline can be used with multiple LLM backends, allowing qwen3:32b and deepseek-r1:32b to be compared under similar conditions.

### 16.5 Dissertation value

The pipeline provides a clear technical contribution for the COMP702 dissertation: it demonstrates how LLM-based game agents can be structured, verified, traced, and evaluated.

---

## 17. Limitations

The current pipeline also has limitations:

* The LLM may still produce weak strategic plans.

* Cached decisions may become stale.

* Rule-based fallback may dominate in some situations.

* The viewer overlay currently depends on available trace logs.

* The system evaluates framework stability more than optimal Lux AI gameplay.

* Some trace evidence may come from different controlled runs and must be clearly labelled.

These limitations should be discussed in the dissertation to show critical reflection.

---

## 18. Summary

The LLM decision pipeline is the central mechanism that connects LLM reasoning to safe and inspectable Lux AI Season 3 behaviour.

Its main contribution is that it prevents direct execution of arbitrary LLM output. Instead, it uses structured prompts, parsers, verification, fallback, caching, risk filtering, action planning, and decision tracing.

This makes LuxLLM-Agent suitable as a framework for inspecting and evaluating LLM-based agents in a complex multi-agent game environment.

