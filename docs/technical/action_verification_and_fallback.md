# Action Verification and Fallback

## 1. Overview

Action verification and fallback are central components of LuxLLM-Agent.

The main design principle is:

> The LLM output is treated as a strategic proposal, not as a directly executable game action.

This means that the LLM does not directly control Lux AI Season 3 units. Instead, the LLM proposes high-level strategic intents, and the system checks whether those intents are valid, safe, and executable before converting them into concrete environment actions.

This design supports the main research question:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

It also directly supports the second sub-research question:

> How can rule-based verification, fallback mechanisms, and strategy caching reduce invalid or unstable LLM-generated decisions?

---

## 2. Why Verification is Needed

LLM-generated decisions may be useful at the strategic level, but they are not guaranteed to be directly executable.

Possible problems include:

* the LLM may refer to a unit that is not available;

* the LLM may choose a target outside the map;

* the LLM may suggest an action that is illegal in the current state;

* the LLM may repeat stale strategic plans;

* the LLM may ignore local tactical risks;

* the LLM may return malformed or incomplete structured output;

* the LLM may time out or fail to respond;

* the LLM may produce a reasonable high-level plan that cannot be executed by the current unit.

Therefore, LuxLLM-Agent uses rule-based verification and fallback to create a safety boundary between LLM reasoning and game execution.

This boundary is important for both system reliability and dissertation evaluation. It allows the project to analyse when the LLM contributes to decision making and when rule-based components take over.

---

## 3. Position in the System Pipeline

Action verification sits between LLM strategic planning and executable action generation.

```text

Structured State Summary

        |

        v

LLM Strategic Plan

        |

        v

Structured Output Parser

        |

        v

Rule-based Verification

        |

        v

Fallback / Cache / Risk Filter

        |

        v

Action Planner

        |

        v

Executable Lux AI Action

```

The verification layer ensures that only valid and usable strategic intents are passed to the action planner.

---

## 4. Inputs to the Verification Layer

The verifier receives information from multiple sources:

### 4.1 Current game state

The current game state includes:

* step;

* phase;

* unit positions;

* unit energy;

* visible map information;

* known relic candidates;

* known scoring tiles;

* enemy unit information;

* available actions.

### 4.2 LLM-generated plan

The LLM plan may include:

* global phase;

* main objective;

* risk posture;

* unit-level intents;

* target locations;

* priorities;

* expected values;

* reasons.

### 4.3 Cached plan

If no fresh LLM call is made, the verifier may receive a cached plan from a previous LLM decision step.

### 4.4 Rule-based policy

The rule-based policy provides fallback behaviour and local tactical decisions when the LLM plan is unavailable or unsuitable.

Relevant files include:

```text

action_planner.py

rule_policy.py

agent.py

llm_decider.py

state_summarizer.py

```

---

## 5. Verification Checks

The verifier checks whether the LLM proposal can be converted into a valid action.

Typical checks include:

### 5.1 Unit validity

The system checks whether the unit referenced by the LLM exists and can act.

Example failure:

```text

The LLM proposes an intent for unit 5, but unit 5 is not currently active.

```

### 5.2 Target validity

The system checks whether the proposed target is valid.

Possible issues:

* target is missing;

* target is outside the map;

* target is not reachable;

* target is no longer useful;

* target conflicts with known information.

### 5.3 Intent validity

The system checks whether the LLM intent is recognised by the action planner.

Examples of valid strategic intents include:

```text

EXPLORE_STALE_TILE

MOVE_TO_RELIC_CANDIDATE

HOLD_POSITION

SECURE_SCORING_TILE

```

If the intent is unknown, the system may fall back to a rule-based policy.

### 5.4 Action legality

The system checks whether the final planned action is legal in Lux AI Season 3.

This prevents invalid low-level action arrays from being submitted to the environment.

### 5.5 Local risk

The system may use risk-aware filtering to avoid unsafe actions.

The risk filter can consider:

* nearby enemy units;

* low energy;

* dangerous movement;

* low-value targets;

* local tactical conflicts.

Relevant fields include:

```text

risk_filter_enabled

risk_filter_changed

risk_filter_reason

risk_filter_changed_targets

risk_filter_events_count

```

---

## 6. Fallback Mechanisms

Fallback is used when the LLM decision cannot be used safely or reliably.

Fallback may occur when:

* rule-only mode is enabled;

* LLM use is disabled;

* the LLM times out;

* the LLM returns malformed output;

* the LLM plan is invalid;

* the plan cannot be converted into actions;

* the risk filter rejects the action;

* no suitable cached plan is available.

Fallback-related decision sources include:

```text

fallback

rule_fallback

rule_player

```

Fallback is not treated as a failure of the system. Instead, it is a deliberate design mechanism for maintaining stable behaviour.

---

## 7. Strategy Cache

The strategy cache allows the agent to reuse recent LLM decisions across multiple game steps.

This is important because LLM calls are expensive. For example, in the DeepSeek-R1-32B 50-run evidence, average LLM latency was approximately 4143.595 ms.

The cache reduces:

* repeated LLM calls;

* runtime latency;

* unnecessary strategic oscillation;

* cost of large-model inference.

Cache-related fields include:

```text

cached_llm_turn

cache_used

stale_decision

last_llm_step

```

A cached decision can still be inspected in the viewer through the decision trace overlay.

---

## 8. Decision Sources

LuxLLM-Agent records the source of each decision.

Important decision sources include:

| Decision source | Meaning                                               |
| --------------- | ----------------------------------------------------- |
| `llm_fresh`     | A fresh LLM decision was used                         |
| `cached_llm`    | A recent LLM plan was reused                          |
| `fallback`      | General fallback behaviour was used                   |
| `rule_fallback` | A rule-based fallback replaced or repaired a decision |
| `rule_player`   | Rule-based player logic produced the action           |
| `rule_only`     | Rule-only mode was active                             |

These sources are important because they allow the evaluation to go beyond final scores. The system can analyse how often the LLM contributed, how often fallback was needed, and how much of the behaviour came from deterministic rules.

---

## 9. Evidence from DeepSeek-R1-32B 50-run

The DeepSeek-R1-32B 50-run experiment provides evidence that the action-verification and fallback framework can support another reasoning-oriented LLM backend.

Main result:

| Metric              |             Value |
| ------------------- | ----------------: |
| Model               | `deepseek-r1:32b` |
| Total runs          |                50 |
| player_0 wins       |                26 |
| player_1 wins       |                24 |
| player_0 win rate   |               52% |
| Average LLM errors  |               0.0 |
| Average LLM latency |       4143.595 ms |
| Maximum LLM latency |      10581.076 ms |

Decision-source distribution:

| Decision source | Count |
| --------------- | ----: |
| `rule_player`   | 25250 |
| `fallback`      |    94 |
| `rule_fallback` |  3163 |
| `llm_fresh`     |  1362 |
| `cached_llm`    | 20631 |

Derived interpretation:

```text

LLM-related decision events = llm_fresh + cached_llm

                            = 1362 + 20631

                            = 21993

Fallback-related decision events = fallback + rule_fallback

                                 = 94 + 3163

                                 = 3257

```

This shows that the system can combine LLM decisions, cached plans, rule-player actions, and fallback actions within one traceable evaluation framework.

---

## 10. Evidence from qwen3:32b 50-run

The qwen3:32b 50-run evidence provides the main LLM-backed controlled-run result.

| Metric            |       Value |
| ----------------- | ----------: |
| Model             | `qwen3:32b` |
| Total runs        |          50 |
| player_0 wins     |          35 |
| player_1 wins     |          15 |
| player_0 win rate |         70% |
| LLM errors        |           0 |

Together with the DeepSeek-R1-32B evidence, this supports the claim that the same action-verification framework can run different LLM backends under controlled evaluation settings.

---

## 11. Role in Replay-grounded Inspection

The action-verification and fallback mechanism is visible in the LLM Decision Trace Overlay.

Relevant files:

```text

tools/build_run008_decision_trace_overlay.py

data/run008_decision_trace_overlay.json

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

```

The overlay displays:

* decision source;

* LLM model;

* current objective;

* fallback status;

* fallback reason;

* risk filter status;

* unit intents;

* score context.

This makes it possible to inspect whether a visible game action came from a fresh LLM plan, cached plan, fallback, or rule-based logic.

This is important for the dissertation because it demonstrates that the system provides replay-grounded decision inspection, not only visual replay.

---

## 12. Evaluation Value

Action verification and fallback provide several evaluation benefits.

### 12.1 Reliability evaluation

The system can measure:

* LLM errors;

* timeout events;

* fallback usage;

* invalid decision handling;

* rule fallback frequency.

### 12.2 Behavioural evaluation

The system can inspect:

* when the LLM was used;

* when cached plans were reused;

* when fallback replaced the LLM;

* whether risk filters changed actions;

* how decision sources relate to game outcome.

### 12.3 Model comparison

The same verification pipeline can be used across multiple LLM backends. This allows qwen3:32b and deepseek-r1:32b to be compared under similar system constraints.

### 12.4 Failure analysis

Fallback and decision-source logs make it easier to identify failure cases, such as:

* stale cached plans;

* weak LLM objectives;

* overuse of fallback;

* actions that are valid but strategically poor.

---

## 13. Design Benefits

The action-verification and fallback design provides the following benefits:

| Benefit            | Explanation                                                                |
| ------------------ | -------------------------------------------------------------------------- |
| Safety             | Prevents arbitrary LLM output from directly controlling game actions       |
| Stability          | Allows the agent to continue acting when the LLM fails                     |
| Inspectability     | Records whether actions come from LLM, cache, fallback, or rule logic      |
| Efficiency         | Reduces unnecessary LLM calls through caching                              |
| Comparability      | Enables multiple LLM backends to be evaluated through the same framework   |
| Dissertation value | Provides a clear technical contribution beyond simple gameplay performance |

---

## 14. Limitations

The current design also has limitations:

* Fallback can hide weak LLM decisions by replacing them with rule-based actions.

* Cached plans may become stale if the game state changes quickly.

* Rule-based verification may reject some creative but potentially useful LLM strategies.

* Fallback counts can be difficult to interpret because they may be measured at different levels, such as unit-level fallback or decision-source fallback.

* The verifier improves stability but does not guarantee optimal gameplay.

* The current trace overlay depends on available logs and may require clear labelling when trace data comes from a specific controlled run.

These limitations should be discussed in the dissertation to show critical reflection.

---

## 15. Summary

Action verification and fallback are core components of LuxLLM-Agent.

They make it possible to use LLMs as strategic planners without allowing them to directly execute arbitrary game actions. The rule-based verifier, fallback policy, strategy cache, and risk-aware filter create a controlled boundary between LLM reasoning and Lux AI action execution.

This design supports the project's main contribution: making LLM-based game-agent behaviour more inspectable, stable, and evaluable through structured decision tracing and rule-based action verification.

