\# System Architecture



\## 1. Overview



LuxLLM-Agent is a decision-trace and action-verification framework for inspecting and evaluating LLM-based agents in Lux AI Season 3.



The system is designed around the following research question:



> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?



The project is not only an LLM game-playing agent. It is a complete inspection and evaluation framework that connects:



\* Lux AI Season 3 observations;

\* structured state summarisation;

\* LLM-based strategic decision making;

\* structured output parsing;

\* rule-based action verification;

\* fallback and strategy caching;

\* risk-aware action filtering;

\* action planning;

\* decision trace logging;

\* controlled-run evaluation;

\* replay-grounded visual inspection.



The main system design principle is that the LLM should not directly execute arbitrary game actions. Instead, the LLM provides strategic proposals, which are parsed, checked, filtered, cached, repaired, or replaced by rule-based fallback behaviour before being converted into executable Lux AI actions.



This separation between high-level LLM reasoning and low-level action execution is the core technical design of the project.



\---



\## 2. High-level Architecture



The overall pipeline is:



```text

Lux AI Season 3 Observation

&#x20;       |

&#x20;       v

Structured State Summariser

&#x20;       |

&#x20;       v

LLM Decision Module

&#x20;       |

&#x20;       v

Structured Plan Parser

&#x20;       |

&#x20;       v

Rule-based Action Verifier

&#x20;       |

&#x20;       v

Fallback / Cache / Risk Filter

&#x20;       |

&#x20;       v

Action Planner

&#x20;       |

&#x20;       v

Lux AI Environment

&#x20;       |

&#x20;       v

Decision Logs + Evaluation Metrics + Replay Viewer

```



The architecture separates strategic reasoning from direct action execution. This is important because LLM outputs may be incomplete, invalid, unstable, expensive to request at every step, or inconsistent with the current game state.



By separating the LLM from executable actions, LuxLLM-Agent can use LLMs as strategic decision sources while still maintaining rule-based safety, reproducibility, and evaluation control.



\---



\## 3. Main Components



\### 3.1 Lux AI Season 3 Runtime



The runtime connects the project to the Lux AI Season 3 environment. It receives observations, produces actions, records match results, and supports both rule-only and LLM-enabled configurations.



Relevant files:



```text

agent.py

baseline\_agent.py

main.py

config.py

run\_match\_llm.bat

```



The runtime supports multiple experimental modes through environment variables, including:



```text

LUX\_LLM\_ENABLED

LUX\_FORCE\_RULE\_ONLY

LUX\_LLM\_MODEL

LUX\_EXPERIMENT\_TAG

LUX\_ENABLE\_STRATEGY\_CACHE

LUX\_ENABLE\_RISK\_AWARE\_ACTION\_FILTER

```



This makes it possible to run controlled comparisons between:



\* rule-only baseline agents;

\* qwen3:32b-backed LLM agents;

\* deepseek-r1:32b-backed LLM agents.



The runtime layer is also responsible for producing match-level evidence such as rewards, winners, LLM call counts, latency, fallback counts, and decision-source statistics.



\---



\### 3.2 State Summarisation



The state summariser converts raw Lux AI observations into compact structured information suitable for LLM-based strategic decision making.



Relevant files:



```text

state\_summarizer.py

lux\_state.py

```



Raw Lux AI observations are too detailed and unstable to pass directly into the LLM. The summariser extracts higher-level information, including:



\* current step;

\* game phase;

\* score context;

\* visible units;

\* unit positions and energy;

\* candidate relic or scoring locations;

\* exploration status;

\* known and unknown areas;

\* risk context;

\* available strategic options.



This component supports the first sub-research question:



> How can raw Lux AI Season 3 observations be transformed into compact structured inputs for LLM-based strategic decision making?



The state summarisation module improves LLM usability by reducing prompt noise and presenting the game state in a format that is closer to strategic planning than raw environment data.



\---



\### 3.3 LLM Decision Module



The LLM decision module produces high-level strategic decisions rather than directly executable actions.



Relevant files:



```text

llm\_decider.py

agent.py

```



The LLM backend can be changed through the runtime configuration:



```text

LUX\_LLM\_MODEL=qwen3:32b

LUX\_LLM\_MODEL=deepseek-r1:32b

```



The current project includes 50-run evaluation evidence for both qwen3:32b and deepseek-r1:32b.



The LLM decision output typically contains:



\* game phase;

\* main objective;

\* risk posture;

\* per-unit intent;

\* target location;

\* priority;

\* reason.



For example, a high-level LLM plan may suggest that a unit should move to a relic candidate or explore stale tiles. The plan is not executed directly. It is first parsed, checked, and converted into legal actions by downstream components.



This design reduces the risk of allowing the LLM to directly control low-level game actions.



\---



\### 3.4 Structured Plan Parser



The structured plan parser converts the LLM response into an internal representation that the agent can inspect and use.



Its responsibilities include:



\* checking whether the LLM response is parseable;

\* extracting global plan fields;

\* extracting unit-level intents;

\* detecting missing or invalid fields;

\* recording LLM errors;

\* triggering fallback behaviour when needed.



This component provides a boundary between LLM-generated text or JSON-like output and the deterministic game-action pipeline.



Without this boundary, invalid or malformed LLM outputs could directly affect the game agent. With the parser, the system can detect malformed outputs and use fallback policies instead.



\---



\### 3.5 Rule-based Action Verification



The action verifier checks whether proposed LLM decisions are feasible and safe in the current game state.



Relevant files:



```text

action\_planner.py

rule\_policy.py

agent.py

```



The verifier can reject, repair, or replace LLM-generated plans. It checks constraints such as:



\* whether a unit exists;

\* whether a proposed target is reachable;

\* whether an action is legal;

\* whether a move is risky;

\* whether a plan conflicts with known game rules;

\* whether fallback is required.



The core design principle is:



> The LLM output is treated as a strategic proposal, not as a directly executable game action.



This component supports the second sub-research question:



> How can rule-based verification, fallback mechanisms, and strategy caching reduce invalid or unstable LLM-generated decisions?



Rule-based action verification is one of the main technical contributions of the project. It makes LLM decisions more controllable and easier to inspect.



\---



\### 3.6 Fallback, Strategy Cache, and Risk Filter



The system includes several stability mechanisms.



\#### Fallback



Fallback is used when the LLM is disabled, invalid, unavailable, timed out, or produces unusable output.



Fallback-related decision sources include:



```text

fallback

rule\_fallback

rule\_player

```



Fallback is important because it ensures that the agent can still act even when the LLM cannot provide a usable decision.



\#### Strategy Cache



The LLM is not called at every frame. Instead, recent LLM decisions can be reused across multiple game steps.



This reduces:



\* latency;

\* repeated LLM calls;

\* unstable step-by-step plan changes;

\* runtime cost.



Cache-related decision source:



```text

cached\_llm

```



Strategy caching is especially important when using large local or HPC-hosted LLMs because generation latency can be several seconds.



\#### Risk-aware Action Filter



The risk-aware filter can change or reject actions that appear dangerous according to rule-based checks.



Relevant metrics include:



```text

risk\_filter\_enabled

risk\_filter\_changed

risk\_filter\_reason

risk\_filter\_changed\_targets

risk\_filter\_events\_count

```



Together, fallback, caching, and risk filtering make the system more stable and easier to evaluate.



\---



\### 3.7 Action Planner



The action planner converts verified strategic intents into executable Lux AI Season 3 actions.



Relevant files:



```text

action\_planner.py

rule\_policy.py

```



The planner bridges the gap between high-level strategy and low-level game actions.



For example, an LLM intent such as:



```text

MOVE\_TO\_RELIC\_CANDIDATE

```



must be converted into a concrete movement action for a specific unit at a specific step.



The action planner is responsible for turning strategic intent into legal environment actions while respecting the current state, unit availability, and movement constraints.



\---



\### 3.8 Decision Trace Logging



The system records decision-level information for later evaluation and inspection.



Important logs include:



```text

logs/decision\_trace.jsonl

logs/decision\_log.jsonl

logs/ablation\_metrics.jsonl

logs/match\_history.jsonl

```



Important fields include:



```text

step

phase

player

decision\_source

llm\_mode

llm\_model

llm\_called

llm\_valid

llm\_error

fallback\_used

fallback\_reason

cache\_used

stale\_decision

risk\_filter\_changed

unit\_intent\_count

unit\_action\_count

score\_player\_0

score\_player\_1

```



Decision trace logging is essential because final match outcomes alone cannot explain how the agent behaved. The trace logs make it possible to inspect whether a decision came from a fresh LLM call, cached LLM plan, fallback policy, rule player, or rule fallback.



This supports both quantitative evaluation and qualitative failure analysis.



\---



\### 3.9 Controlled-run Evaluation



The system supports controlled multi-run evaluation.



Current main evidence includes:



| Model           | Runs | player\_0 wins | player\_1 wins | player\_0 win rate | LLM errors |

| --------------- | ---: | ------------: | ------------: | ----------------: | ---------: |

| qwen3:32b       |   50 |            35 |            15 |               70% |          0 |

| deepseek-r1:32b |   50 |            26 |            24 |               52% |          0 |



The model comparison is not intended as a general LLM leaderboard. Instead, it evaluates whether the same decision-trace and action-verification framework can support different reasoning-oriented LLM backends.



Relevant evidence:



```text

docs/demo\_evidence/hpc\_qwen3\_32b\_multirun/

docs/demo\_evidence/hpc\_deepseek\_r1\_32b\_50run/

docs/demo\_evidence/llm\_model\_comparison\_summary.md

```



The evaluation uses more than win/loss results. It also considers:



\* LLM errors;

\* LLM latency;

\* fresh LLM calls;

\* cached LLM turns;

\* fallback count;

\* decision-source distribution;

\* trace steps;

\* replay-grounded inspection.



This makes the evaluation more suitable for a dissertation project than a simple gameplay leaderboard.



\---



\### 3.10 Replay Viewer and Decision Trace Overlay



The project includes a Season 3 isometric replay viewer.



Relevant files:



```text

docs/viewers/s3\_isometric\_battle\_viewer\_v09n12c3.html

docs/viewers/s3\_isometric\_battle\_viewer\_v09n12d\_trace\_overlay.html

data/isometric\_replay\_frames\_run008.json

data/run008\_decision\_trace\_overlay.json

tools/build\_run008\_decision\_trace\_overlay.py

```



The v09n12d viewer adds an LLM Decision Trace Overlay that shows:



\* frame and step;

\* phase;

\* decision source;

\* LLM model;

\* current objective;

\* risk posture;

\* fallback status;

\* risk filter status;

\* score context;

\* unit intents.



This component supports the third sub-research question:



> How can replay-grounded decision traces help analyse the relationship between LLM strategy, decision source, action execution, and game outcome?



The overlay makes the system easier to inspect and demonstrate. It also provides dissertation evidence that the project supports decision traceability rather than only replay visualisation.



\---



\## 4. Data Flow



The complete data flow is:



```text

1\. Lux AI observation is received by the agent.

2\. The observation is converted into a structured state summary.

3\. The LLM module receives the structured prompt.

4\. The LLM returns a strategic plan.

5\. The plan is parsed into structured global and unit-level intents.

6\. The action verifier checks whether the plan is usable.

7\. The strategy cache may reuse recent LLM plans.

8\. The fallback policy handles invalid or unavailable decisions.

9\. The risk-aware filter may change unsafe actions.

10\. The action planner produces executable Lux AI actions.

11\. Logs are written for decisions, traces, metrics, and match results.

12\. Replay frames are generated for visual inspection.

13\. The viewer displays the replay together with decision trace overlay data.

```



\---



\## 5. Design Rationale



The architecture is motivated by three practical challenges in LLM-based game agents.



\### 5.1 LLM decisions are not always executable



LLMs may produce outputs that are not legal or useful in the current environment. LuxLLM-Agent avoids this by treating LLM output as strategic intent and using rule-based verification before execution.



\### 5.2 LLM calls are expensive and slow



Calling a large LLM at every game step is inefficient. The system uses strategy caching and controlled call intervals to reduce overhead.



\### 5.3 Final scores alone are not enough for evaluation



A win/loss result does not explain how the agent behaved. The system records decision source, fallback, latency, errors, and replay-grounded traces to make the behaviour inspectable.



\---



\## 6. Relation to the Research Questions



| Research question                     | Architecture support                                                               |

| ------------------------------------- | ---------------------------------------------------------------------------------- |

| RQ1: State summarisation              | Structured summariser converts raw observations into compact LLM inputs            |

| RQ2: Action verification and fallback | Rule verifier, fallback, cache, and risk filter stabilise LLM-generated strategies |

| RQ3: Replay-grounded evaluation       | Decision logs and viewer overlay connect steps, decisions, sources, and outcomes   |



\---



\## 7. Summary



The LuxLLM-Agent architecture separates strategic reasoning, action verification, execution, logging, and visual inspection.



This separation is the main technical contribution of the project. It allows LLM-based agents to be inspected and evaluated in a complex multi-agent game setting without relying only on final match scores.



For the COMP702 dissertation, this architecture supports the argument that structured decision tracing and rule-based action verification can make LLM-based game agents more reliable, inspectable, and evaluable.



