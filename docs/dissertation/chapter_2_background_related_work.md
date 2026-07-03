\# Chapter 2: Background and Related Work



\## 2.1 Introduction



This chapter introduces the background and related work relevant to LuxLLM-Agent.



The project investigates how structured decision tracing and rule-based action verification can support the inspection and evaluation of LLM-based agents in Lux AI Season 3. To place the project in context, this chapter discusses several related areas:



\* large language models as agents;

\* LLMs for planning and decision making;

\* game AI and sequential decision making;

\* hybrid LLM-rule systems;

\* action verification and safety boundaries;

\* explainability and decision traceability;

\* evaluation of LLM-based agents;

\* Lux AI Season 3 as an experimental environment.



The purpose of this chapter is not to provide a complete survey of all LLM-agent research. Instead, it identifies the concepts needed to understand the design choices of LuxLLM-Agent.



\---



\## 2.2 Large Language Models as Agents



Large language models are increasingly used as components of agent systems. In these systems, the model is not only used to answer a single question, but also to support planning, reasoning, tool use, environment interaction, and decision making.



An LLM-based agent usually follows a loop:



```text

Observation

&#x20;   |

&#x20;   v

State interpretation

&#x20;   |

&#x20;   v

Reasoning or planning

&#x20;   |

&#x20;   v

Action selection

&#x20;   |

&#x20;   v

Environment update

```



This loop is different from ordinary text generation because the model must respond to a changing environment over time. In a sequential decision-making task, each decision may affect future states.



LLMs can be useful in agent systems because they can process structured descriptions, produce high-level plans, and generate explanations. However, they also have limitations. They may produce outputs that are invalid, inconsistent, incomplete, or not grounded in the current environment state.



For this reason, many practical LLM-agent systems do not allow the LLM to directly control the environment. Instead, the LLM is often used as a planner, advisor, or reasoning component inside a larger system.



LuxLLM-Agent follows this approach. The LLM is used to propose strategic plans, while deterministic components handle parsing, verification, fallback, action planning, logging, and evaluation.



\---



\## 2.3 LLMs for Planning and Decision Making



Planning is an important part of intelligent agent behaviour. A planning system must decide what objective to pursue, which actions to take, and how to adapt when the environment changes.



LLMs can support planning because they can generate high-level strategies from structured context. For example, an LLM may suggest that an agent should explore unknown areas, secure a scoring location, avoid risk, or prioritise a particular target.



However, LLM-based planning has several challenges.



First, the LLM may not fully understand the environment rules. It may suggest actions that sound reasonable in natural language but are not legal in the game.



Second, the LLM may produce plans that are too abstract. A plan such as "explore the map" still needs to be converted into unit-level actions.



Third, LLM decisions may be unstable across steps. If the model is called repeatedly, it may change strategy too frequently.



Fourth, LLM calls may be slow, especially when using large local or HPC-hosted models.



LuxLLM-Agent addresses these challenges by treating the LLM plan as a strategic proposal. The proposal is parsed into structured fields, checked by rule-based logic, cached when appropriate, and converted into executable actions by an action planner.



This design allows the LLM to contribute high-level reasoning without giving it direct control over low-level actions.



\---



\## 2.4 Game AI and Sequential Decision Making



Game AI has long been used as a testbed for artificial intelligence. Games provide clear rules, measurable outcomes, controlled environments, and replayable behaviour.



Lux AI Season 3 is a sequential multi-agent game environment. An agent must repeatedly observe the game state and choose actions for its units. The environment includes hidden information, movement constraints, scoring opportunities, resource discovery, and interaction with an opponent.



This creates several difficulties:



\* the agent does not know the full map at all times;

\* the value of a target may be uncertain;

\* decisions must be made repeatedly;

\* actions must be legal in the current state;

\* unit energy and location affect what can be done;

\* an opponent may interfere with the agent’s plan.



These properties make Lux AI Season 3 suitable for studying LLM-assisted agent decision making. The environment is complex enough to require strategic reasoning, but structured enough to support logging, evaluation, and replay analysis.



In this project, Lux AI Season 3 is used not only as a game environment, but also as an experimental setting for studying how LLM-based decisions can be verified, traced, and inspected.



\---



\## 2.5 Hybrid LLM-rule Agent Architectures



A purely LLM-controlled agent may be difficult to make reliable in a rule-based game environment. The model may generate an invalid target, refer to a non-existent unit, or produce a plan that cannot be executed.



Hybrid LLM-rule architectures address this by combining LLM reasoning with deterministic rule-based components.



In a hybrid architecture, the LLM may handle:



\* high-level planning;

\* objective selection;

\* risk posture;

\* unit-level intent generation;

\* explanation of strategy.



Rule-based components may handle:



\* action legality;

\* movement constraints;

\* fallback behaviour;

\* local tactical decisions;

\* safety filtering;

\* environment-specific execution.



LuxLLM-Agent is designed as a hybrid LLM-rule architecture. The LLM provides strategic proposals, while rule-based modules verify and execute those proposals.



This architecture has two advantages.



First, it improves stability. The agent can still act if the LLM is disabled, invalid, slow, or unavailable.



Second, it improves inspectability. Since the system records whether actions come from fresh LLM decisions, cached LLM plans, fallback, or rules, the behaviour can be analysed more carefully.



\---



\## 2.6 Action Verification and Safety Boundaries



Action verification is the process of checking whether a proposed action is legal, safe, and appropriate before execution.



In LLM-based agents, action verification is important because the model output cannot be assumed to be correct. An LLM may produce an action that violates environment constraints or refers to information that is not available.



A safety boundary is therefore needed between model output and environment execution.



In LuxLLM-Agent, this safety boundary is implemented through:



\* structured output parsing;

\* rule-based action verification;

\* fallback behaviour;

\* strategy caching;

\* risk-aware action filtering;

\* action planning.



The core principle is:



> The LLM output is treated as a strategic proposal, not as a directly executable game action.



This principle reduces the risk of invalid LLM output affecting the environment. It also makes the system easier to evaluate because the pipeline records when a plan is accepted, cached, replaced, or supported by fallback.



Action verification is therefore not only a reliability mechanism. It is also part of the project’s evaluation framework.



\---



\## 2.7 Explainability, Traceability, and Decision Provenance



Explainability is important for systems where users need to understand how decisions are made. In agent systems, this is especially important because behaviour emerges over time through repeated interactions with the environment.



For LLM-based agents, explainability can be difficult. A final action may be influenced by a model response, cached strategy, fallback rule, local verifier, or action planner. Without logs, it is difficult to know which component produced the final behaviour.



This project therefore focuses on decision traceability and decision provenance.



Decision traceability means that the system records information about decisions over time. Decision provenance means that the system identifies the source of a decision.



In LuxLLM-Agent, important decision sources include:



```text

llm\_fresh

cached\_llm

fallback

rule\_fallback

rule\_player

rule\_only

```



These decision sources allow the project to analyse whether behaviour came from a fresh LLM call, a cached LLM plan, fallback, or rule-based logic.



The LLM Decision Trace Overlay extends this idea by showing decision trace information during replay playback. This makes the system more inspectable than a standard replay viewer.



\---



\## 2.8 Evaluation of LLM-based Agents



Evaluating LLM-based agents is more complex than evaluating ordinary text generation systems.



A text generation system may be evaluated using output quality, correctness, or human preference. An agent system must also be evaluated by how it behaves in an environment over time.



For game agents, common evaluation metrics include:



\* win rate;

\* reward;

\* number of completed matches;

\* score difference;

\* failure rate.



However, these metrics are not sufficient for LLM-based agents. A final win or loss does not explain how the decision was made.



LuxLLM-Agent therefore uses a broader evaluation approach, including:



\* gameplay outcome metrics;

\* LLM execution metrics;

\* decision-source metrics;

\* fallback and verification metrics;

\* latency metrics;

\* replay-grounded inspection metrics;

\* qualitative failure-case analysis.



This evaluation approach supports the dissertation research question because it focuses on inspection and evaluation rather than only performance.



The project’s controlled-run evidence includes 50-run results for qwen3:32b and DeepSeek-R1-32B. Both models completed 50 controlled runs with zero LLM errors in the current evidence, while producing different gameplay outcomes.



This shows why evaluation should distinguish between execution stability, strategic quality, and final outcome.



\---



\## 2.9 Replay-based Analysis and Visual Inspection



Replay-based analysis is useful in game AI because it allows behaviour to be inspected after a match. A replay can show how units moved, how the score changed, and how the game state evolved.



However, a normal replay does not show why an agent made a decision.



For LLM-based agents, this is a limitation. A user may see a unit move toward a target, but the replay alone does not reveal whether the action came from an LLM plan, a cached strategy, fallback logic, or rule-based movement.



LuxLLM-Agent addresses this by adding an LLM Decision Trace Overlay to the Season 3 viewer.



The overlay displays:



\* frame and step;

\* phase;

\* decision source;

\* LLM model;

\* objective;

\* risk posture;

\* fallback status;

\* risk filter status;

\* score context;

\* unit intents.



This turns replay analysis into replay-grounded decision inspection.



The overlay is important for the project because it connects implementation, evaluation, and demonstration. It provides visual evidence that the system can trace and inspect LLM-agent behaviour.



\---



\## 2.10 Lux AI Season 3 as an Evaluation Environment



Lux AI Season 3 was selected because it provides a structured but challenging environment for agent evaluation.



It has several useful properties:



\* it is sequential;

\* it involves hidden or uncertain information;

\* it requires repeated decision making;

\* it involves multiple units;

\* it includes scoring and exploration;

\* it supports replay-based analysis;

\* it provides measurable outcomes.



These properties make it suitable for studying LLM-based agents.



The environment also exposes the limitations of direct LLM control. Since actions must be legal and timely, the LLM cannot simply output arbitrary text. It must be integrated into a controlled action pipeline.



This makes Lux AI Season 3 a suitable environment for investigating the project’s research question.



\---



\## 2.11 Positioning of LuxLLM-Agent



LuxLLM-Agent is positioned as a framework for inspecting and evaluating LLM-based agents, rather than as a pure competition bot.



Its main distinguishing features are:



\* structured state summarisation;

\* LLM-based strategic planning;

\* rule-based verification;

\* fallback and caching;

\* risk-aware filtering;

\* decision-source logging;

\* controlled multi-run evaluation;

\* replay-grounded decision trace overlay.



This positioning is important because the project’s contribution is not only that an LLM can be connected to Lux AI Season 3. The contribution is that LLM decisions can be structured, verified, traced, evaluated, and visually inspected.



This distinguishes the project from a simple LLM wrapper around an existing rule-based agent.



\---



\## 2.12 Summary



This chapter introduced the background and related work relevant to LuxLLM-Agent.



LLMs can support high-level planning, but they are difficult to use as direct controllers in sequential game environments. Game agents require valid actions, stable execution, and repeated decision making. Therefore, a hybrid architecture is needed.



LuxLLM-Agent addresses this by combining LLM strategic planning with rule-based verification, fallback, strategy caching, risk-aware filtering, decision trace logging, controlled evaluation, and replay-grounded inspection.



The next chapter presents the project requirements and methodology in more detail.



