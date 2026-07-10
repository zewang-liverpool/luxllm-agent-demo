# Chapter 4: System Design

## 4.1 Introduction

This chapter presents the system design of LuxLLM-Agent, a decision-trace and action-verification framework for inspecting and evaluating LLM-based agents in Lux AI Season 3.

The project is designed around the following research question:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

The system is not designed only as a game-playing agent. Instead, it is designed as a complete framework that connects LLM-based strategic decision making with deterministic action verification, fallback handling, controlled evaluation, logging, and replay-grounded visual inspection.

The main design principle is:

> The LLM output is treated as a strategic proposal, not as a directly executable game action.

This principle is important because large language models may produce outputs that are incomplete, invalid, stale, inconsistent with the current game state, or too slow to request at every step. LuxLLM-Agent therefore separates high-level LLM reasoning from low-level action execution.

This chapter describes the architecture, data flow, main components, design rationale, and traceability mechanisms of the system.

---

## 4.2 Design Goals

The design of LuxLLM-Agent is guided by five goals.

### 4.2.1 Inspectability

The system should make agent behaviour inspectable. It should be possible to determine whether a decision came from a fresh LLM call, a cached LLM plan, fallback behaviour, rule fallback, or rule-based policy.

This is necessary because final game outcomes alone do not explain how an LLM-based agent behaved.

### 4.2.2 Stability

The system should remain stable even when the LLM is disabled, unavailable, slow, or produces unusable output.

To support this, the system includes fallback mechanisms, strategy caching, rule-based verification, and risk-aware filtering.

### 4.2.3 Controlled LLM Use

The LLM should be used as a strategic planner rather than a direct action controller.

This reduces the risk of invalid Lux AI actions and makes the system easier to evaluate.

### 4.2.4 Evaluation Support

The system should produce logs and metrics that support controlled multi-run evaluation.

Important evaluation dimensions include:

* win/loss results;

* rewards;

* LLM errors;

* LLM latency;

* fresh LLM calls;

* cached LLM turns;

* fallback frequency;

* decision-source distribution;

* replay-grounded inspection.

### 4.2.5 Reproducibility and Demonstrability

The system should support reproducible experiments and visual demonstration. This is achieved through controlled run scripts, evidence directories, JSON/JSONL logs, replay frame generation, and an HTML-based viewer.

---

## 4.3 High-level Architecture

The high-level architecture is shown below:

```text

Lux AI Season 3 Observation

        |

        v

Structured State Summariser

        |

        v

LLM Decision Module

        |

        v

Structured Plan Parser

        |

        v

Rule-based Action Verifier

        |

        v

Fallback / Strategy Cache / Risk Filter

        |

        v

Action Planner

        |

        v

Executable Lux AI Action

        |

        v

Decision Logs + Evaluation Metrics + Replay Viewer

```

This architecture separates strategic reasoning from executable action generation.

The LLM decision module produces high-level plans and unit-level intents. These are then parsed, checked, filtered, cached, or replaced by fallback behaviour before being converted into executable Lux AI Season 3 actions.

This design is different from a direct LLM controller. In a direct controller, the LLM would output low-level actions directly. In LuxLLM-Agent, the LLM only proposes strategy, while deterministic components maintain action validity and traceability.

---

## 4.4 System Components

### 4.4.1 Lux AI Season 3 Runtime

The runtime layer connects the project to the Lux AI Season 3 environment.

Its responsibilities include:

* receiving observations;

* producing actions;

* supporting rule-only and LLM-enabled modes;

* running controlled matches;

* recording match results;

* generating replay and evaluation evidence.

Relevant files include:

```text

agent.py

baseline_agent.py

main.py

config.py

run_match_llm.bat

```

The runtime supports different experimental settings through environment variables, including:

```text

LUX_LLM_ENABLED

LUX_FORCE_RULE_ONLY

LUX_LLM_MODEL

LUX_EXPERIMENT_TAG

LUX_ENABLE_STRATEGY_CACHE

LUX_ENABLE_RISK_AWARE_ACTION_FILTER

```

This allows the same system to be tested under different settings, including rule-only mode, qwen3:32b-backed mode, and DeepSeek-R1-32B-backed mode.

---

### 4.4.2 Structured State Summariser

The structured state summariser converts raw Lux AI Season 3 observations into compact information suitable for LLM-based planning.

Raw environment observations are not ideal for direct LLM prompting because they are detailed, low-level, and may include information that is not relevant to high-level strategy. The summariser extracts strategic information such as:

* current step;

* game phase;

* score context;

* visible units;

* unit positions;

* unit energy;

* known relic candidates;

* known scoring tiles;

* unexplored or stale tiles;

* local risk context;

* available units and actions.

This design supports the first sub-research question:

> How can raw Lux AI Season 3 observations be transformed into compact structured inputs for LLM-based strategic decision making?

The summariser reduces prompt noise and helps the LLM reason about strategy rather than raw environment mechanics.

---

### 4.4.3 LLM Decision Module

The LLM decision module uses a large language model to generate high-level strategic plans.

The LLM backend can be configured through:

```text

LUX_LLM_MODEL=qwen3:32b

LUX_LLM_MODEL=deepseek-r1:32b

```

The LLM output is expected to contain structured strategic information, including:

* phase;

* main objective;

* risk posture;

* global reason;

* unit-level intents;

* target locations;

* priorities;

* expected value;

* unit-level reasons.

For example, the LLM may suggest that a unit should explore stale tiles or move to a relic candidate. These are strategic intents, not executable actions.

The LLM decision module therefore contributes high-level reasoning while leaving execution control to deterministic components.

---

### 4.4.4 Structured Plan Parser

The structured plan parser converts the LLM response into an internal representation.

Its responsibilities include:

* checking whether the LLM output is parseable;

* extracting the global plan;

* extracting unit-level intents;

* detecting missing fields;

* detecting invalid fields;

* recording LLM errors;

* triggering fallback behaviour when needed.

The parser is a safety boundary between LLM output and the action pipeline. Without this boundary, malformed LLM output could directly affect the game agent.

---

### 4.4.5 Rule-based Action Verifier

The rule-based action verifier checks whether the parsed LLM plan is usable in the current game state.

The verifier may check:

* whether a referenced unit exists;

* whether the unit can act;

* whether the target is valid;

* whether the target is inside the map;

* whether the target is reachable;

* whether the intent is recognised;

* whether the proposed behaviour is legal;

* whether the plan appears locally risky.

If a plan is invalid, unsafe, or unusable, the system may repair it or replace it with fallback behaviour.

This supports the second sub-research question:

> How can rule-based verification, fallback mechanisms, and strategy caching reduce invalid or unstable LLM-generated decisions?

The verifier is one of the main technical contributions of LuxLLM-Agent because it prevents arbitrary LLM output from directly controlling units.

---

### 4.4.6 Fallback Mechanism

Fallback behaviour is used when the LLM decision cannot be used safely or reliably.

Fallback may occur when:

* rule-only mode is enabled;

* LLM use is disabled;

* the LLM times out;

* the LLM output is invalid;

* the LLM response cannot be parsed;

* the plan fails verification;

* no suitable LLM plan is available;

* a rule-based action is safer.

The system records fallback-related information through fields such as:

```text

fallback_used

fallback_reason

decision_source

rule_fallback

```

Fallback is not treated as a system failure. Instead, it is a deliberate stability mechanism. It allows the agent to continue acting when the LLM is unavailable or unsuitable.

---

### 4.4.7 Strategy Cache

The strategy cache allows the system to reuse recent LLM plans across multiple steps.

This is necessary because large LLMs may have high latency. Calling the LLM at every game step would be inefficient and impractical.

The cache reduces:

* repeated LLM calls;

* latency overhead;

* unnecessary strategic oscillation;

* runtime cost.

Cached decisions are recorded using fields such as:

```text

cached_llm_turn

stale_decision

last_llm_step

llm_step_used

```

The strategy cache introduces a trade-off. It improves efficiency, but cached plans may become stale when the game state changes. This limitation is later examined in the evaluation and discussion chapters.

---

### 4.4.8 Risk-aware Action Filter

The risk-aware action filter provides another layer of rule-based safety.

It may detect cases where the selected action appears unsafe, such as:

* moving near enemy units;

* targeting a low-value area;

* moving with low energy;

* following a stale or risky plan;

* selecting a target that conflicts with local tactical conditions.

The system records risk-filter behaviour using fields such as:

```text

risk_filter_enabled

risk_filter_changed

risk_filter_reason

risk_filter_changed_targets

risk_filter_events_count

```

The risk-aware filter supports the broader design goal of treating LLM decisions as proposals that can be modified by deterministic checks.

---

### 4.4.9 Action Planner

The action planner converts verified strategic intents into executable Lux AI Season 3 actions.

For example, an LLM intent such as:

```text

EXPLORE_STALE_TILE

```

or:

```text

MOVE_TO_RELIC_CANDIDATE

```

must be converted into a concrete unit movement action.

The action planner considers:

* current unit location;

* target location;

* legal movement directions;

* unit energy;

* available action slots;

* fallback options.

This component bridges the gap between strategic planning and environment execution.

---

### 4.4.10 Decision Trace Logger

The decision trace logger records step-level information about how decisions are produced.

Important log files include:

```text

logs/decision_trace.jsonl

logs/decision_log.jsonl

logs/ablation_metrics.jsonl

logs/match_history.jsonl

```

Important logged fields include:

```text

step

phase

player

decision_source

llm_mode

llm_model

llm_called

llm_valid

llm_error

fallback_used

fallback_reason

cached_llm_turn

stale_decision

risk_filter_changed

unit_intent_count

unit_action_count

score_player_0

score_player_1

```

These logs allow evaluation to go beyond final scores. They make it possible to analyse when the LLM contributed, when fallback was used, when cached plans were reused, and how decision sources relate to outcomes.

---

## 4.5 Data Flow

The complete data flow is:

```text

1. The Lux AI Season 3 environment provides an observation.

2. The runtime passes the observation to the agent.

3. The state summariser extracts a compact structured summary.

4. The LLM decision module receives the structured prompt.

5. The LLM returns a strategic plan.

6. The parser converts the plan into structured internal data.

7. The verifier checks whether the plan is usable.

8. The fallback mechanism handles invalid or unavailable decisions.

9. The strategy cache may reuse a previous LLM plan.

10. The risk-aware filter may change unsafe actions.

11. The action planner generates executable Lux AI actions.

12. The environment executes the actions.

13. The system records decision traces, metrics, and match results.

14. Replay frames are generated for visual inspection.

15. The viewer displays replay frames with decision trace overlay data.

```

This data flow shows how the project connects gameplay, LLM reasoning, rule-based verification, logging, and visual explanation.

---

## 4.6 Decision Provenance Design

Decision provenance is the ability to identify where a decision came from.

LuxLLM-Agent records decision sources such as:

| Decision source | Meaning                                             |
| --------------- | --------------------------------------------------- |
| `llm_fresh`     | A fresh LLM decision was used                       |
| `cached_llm`    | A recent LLM plan was reused                        |
| `fallback`      | General fallback behaviour was used                 |
| `rule_fallback` | Rule-based fallback repaired or replaced a decision |
| `rule_player`   | Rule-based player logic produced the action         |
| `rule_only`     | Rule-only mode was active                           |

This design is important because it prevents misleading evaluation. If a match is won, the system can inspect whether the result came mainly from LLM reasoning, cached plans, fallback, or rule-based logic.

Decision provenance also supports failure analysis. For example, if a visible action is poor, the trace can help identify whether the problem came from a fresh LLM plan, a stale cached decision, or rule fallback.

---

## 4.7 Replay-grounded Inspection

The system includes a Season 3 isometric replay viewer with an LLM Decision Trace Overlay.

Relevant files include:

```text

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

data/run008_decision_trace_overlay.json

tools/build_run008_decision_trace_overlay.py

```

The overlay displays:

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

The overlay turns the viewer from a replay-only tool into a decision inspection interface. This is important for the dissertation because it provides visual evidence of the project's central contribution: structured decision tracing and replay-grounded evaluation.

---

## 4.8 Evaluation-oriented Design

The architecture is designed to support controlled evaluation.

The system can compare:

* rule-only behaviour;

* qwen3:32b-backed LLM behaviour;

* DeepSeek-R1-32B-backed LLM behaviour.

The evaluation is not based only on win/loss. It also records:

* LLM errors;

* LLM latency;

* fresh LLM calls;

* cached LLM turns;

* fallback counts;

* decision-source distribution;

* replay-frame alignment;

* trace steps.

This design supports a stronger dissertation evaluation because it measures both gameplay outcome and system behaviour.

---

## 4.9 Design Rationale

The system design is motivated by three main challenges.

### 4.9.1 LLM Output May Be Invalid

LLMs may produce malformed or non-executable outputs. The parser, verifier, and fallback system reduce this risk.

### 4.9.2 LLM Calls Are Expensive

Large LLMs can take several seconds to respond. The strategy cache and controlled LLM call scheduling reduce the need for frequent calls.

### 4.9.3 Win/Loss Alone Is Not Explainable

A final score does not explain how decisions were made. Decision trace logging and the overlay provide additional evidence for inspection and analysis.

---

## 4.10 Limitations of the Design

The design also has limitations.

First, fallback may make attribution difficult. If many actions come from fallback or rule-based behaviour, final outcomes cannot be attributed only to the LLM.

Second, cached plans may become stale. The system improves efficiency by reusing plans, but game-state changes may make older plans less suitable.

Third, rule-based verification may reject some creative LLM strategies. This improves safety but may reduce strategic diversity.

Fourth, the viewer overlay depends on available logs and correct alignment between replay frames and decision traces.

Fifth, the system is designed for inspection and evaluation rather than leaderboard-level Lux AI performance.

These limitations are not hidden. They are important parts of the evaluation and discussion chapters.

---

## 4.11 Summary

This chapter has presented the design of LuxLLM-Agent as a decision-trace and action-verification framework for LLM-based agents in Lux AI Season 3.

The system separates LLM strategic reasoning from low-level action execution. It uses structured state summarisation, LLM planning, parsing, rule-based verification, fallback, strategy caching, risk-aware filtering, action planning, decision trace logging, and replay-grounded inspection.

The key technical contribution is the controlled boundary between LLM reasoning and executable game actions. This boundary makes the system more stable, inspectable, and evaluable.

The next chapter describes the implementation of these design components in more detail.

