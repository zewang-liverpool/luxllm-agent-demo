# Chapter 1: Introduction



## 1.1 Background



Large language models have increasingly been explored as components of autonomous agents. Their ability to process structured information, generate plans, and produce natural-language explanations makes them attractive for complex decision-making tasks. However, using an LLM as part of an interactive agent is different from using it for static text generation. In a game or simulation environment, the agent must repeatedly observe the state, make decisions, produce valid actions, and adapt to changes over time.



This project studies LLM-based agent design in the context of Lux AI Season 3. Lux AI Season 3 is a competitive multi-agent environment in which agents must make sequential decisions under uncertainty. The environment includes exploration, resource discovery, unit movement, hidden information, scoring opportunities, and interaction with an opponent. These properties make it a useful testbed for studying LLM-assisted decision making.



A direct LLM-based controller is difficult to use in this setting. An LLM may produce invalid actions, incomplete responses, unstable plans, or decisions that do not match the current game state. Large LLMs may also be too slow to call at every game step. Therefore, a practical LLM-based agent needs more than prompt design. It requires a structured system that can summarise the game state, request high-level plans from the LLM, verify those plans, fall back to rule-based behaviour when necessary, and record decision traces for later inspection.



This dissertation presents LuxLLM-Agent, a decision-trace and action-verification framework for inspecting and evaluating LLM-based agents in Lux AI Season 3.



---



## 1.2 Motivation



The motivation for this project comes from the gap between LLM reasoning ability and reliable agent execution.



LLMs can be useful for high-level planning. For example, an LLM may suggest that an agent should explore unknown areas, move toward candidate scoring locations, or adopt a low-risk strategy. However, these suggestions are not automatically executable game actions. They must be translated into valid unit-level actions that satisfy the environment rules.



This creates several practical challenges:



\* raw game observations are too detailed for direct LLM use;

\* LLM output may be malformed or incomplete;

\* LLM-generated plans may be strategically reasonable but impossible to execute;

\* LLM calls may introduce high latency;

\* cached LLM plans may become stale;

\* fallback behaviour may be needed when the LLM is unavailable or unsuitable;

\* final win/loss results do not explain how decisions were made.



These challenges motivated the design of a hybrid LLM-rule system. In this project, the LLM is not treated as a direct action controller. Instead, it is treated as a strategic planner whose outputs are parsed, verified, cached, repaired, or replaced before execution.



The project is also motivated by the need for inspectable evaluation. If an LLM-based agent wins or loses a match, the final score alone does not explain whether the LLM contributed, whether fallback was used, or whether actions came from cached plans. For this reason, LuxLLM-Agent records decision-source information and provides a replay-grounded viewer with an LLM Decision Trace Overlay.



---



## 1.3 Problem Statement



The main problem addressed by this project is how to make LLM-based game-agent behaviour stable, inspectable, and evaluable in a complex sequential environment.



A simple LLM agent may directly ask the model for actions and execute the output. This approach is risky in Lux AI Season 3 because actions must be legal, timely, and consistent with the current game state. Invalid or delayed decisions can make the agent unreliable. At the same time, using only a final match score as evaluation hides important behaviour, such as fallback usage, cached decisions, and rule-based corrections.



Therefore, the project addresses the following problem:



> How can an LLM be integrated into a Lux AI Season 3 agent in a way that supports stable execution, rule-based action verification, decision traceability, controlled evaluation, and replay-grounded inspection?



This problem is both practical and research-oriented. It requires implementing a working agent system, but it also requires designing evaluation methods that reveal how the agent behaves internally.



---



## 1.4 Aim and Objectives



The aim of the project is:



> To develop a decision-trace and action-verification framework that supports the inspection and evaluation of LLM-based agents in Lux AI Season 3.



This aim is divided into the following objectives.



### Objective 1: Implement a working Lux AI Season 3 agent



The project must implement an agent that can receive observations, produce actions, complete matches, and record outcomes.



### Objective 2: Build a structured state summarisation pipeline



The system should convert raw Lux AI observations into compact structured summaries suitable for LLM-based strategic planning.



### Objective 3: Integrate LLM-based strategic planning



The system should use an LLM to produce high-level strategic proposals, such as objectives, risk posture, target locations, and unit-level intents.



### Objective 4: Verify and control LLM-generated decisions



The system should parse LLM output and use rule-based verification, fallback, strategy caching, and risk-aware filtering before converting plans into executable actions.



### Objective 5: Record decision traces and evaluation metrics



The system should record decision-source information, LLM usage, fallback status, cache usage, errors, latency, score context, and match outcomes.



### Objective 6: Evaluate multiple LLM backends



The project should compare at least two LLM backends under the same framework to test whether the system can support different reasoning-oriented models.



### Objective 7: Provide replay-grounded visual inspection



The project should provide a viewer that connects replay frames with decision-trace information, allowing behaviour to be inspected visually.



---



## 1.5 Research Question



The main research question is:



> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?



This question is supported by three sub-research questions.



### RQ1: State summarisation



> How can raw Lux AI Season 3 observations be transformed into compact structured inputs for LLM-based strategic decision making?



This question examines how the system prepares game-state information for LLM reasoning.



### RQ2: Action verification and fallback



> How can rule-based verification, fallback mechanisms, and strategy caching reduce invalid or unstable LLM-generated decisions?



This question examines how the system controls LLM output before execution.



### RQ3: Replay-grounded evaluation



> How can replay-grounded decision traces help analyse the relationship between LLM strategy, decision source, action execution, and game outcome?



This question examines how the system evaluates and visualises agent behaviour.



---



## 1.6 Project Contributions



This project makes several contributions.



### 1.6.1 A structured LLM-assisted agent framework



The project implements a complete framework that connects state summarisation, LLM strategic planning, structured parsing, action verification, fallback, caching, action planning, logging, and visualisation.



### 1.6.2 Rule-based verification of LLM proposals



The system treats LLM output as a strategic proposal rather than a directly executable action. This creates a controlled boundary between LLM reasoning and environment execution.



### 1.6.3 Decision-source logging



The system records whether decisions come from fresh LLM calls, cached LLM plans, fallback behaviour, rule fallback, or rule-based policy. This makes agent behaviour more inspectable.



### 1.6.4 Controlled evaluation with multiple LLM backends



The project evaluates qwen3:32b and DeepSeek-R1-32B under the same framework. Both models completed 50 controlled Lux AI Season 3 runs with zero LLM errors in the current evidence.



### 1.6.5 Replay-grounded decision trace overlay



The project implements an LLM Decision Trace Overlay for the Season 3 viewer. This overlay displays step-aligned decision information during replay playback, including decision source, objective, fallback status, risk posture, score context, and unit intents.



### 1.6.6 Dissertation-oriented analysis and documentation



The project includes technical documentation, evaluation analysis, model comparison, and failure-case analysis. These artefacts support a structured dissertation rather than only an engineering demo.



---



## 1.7 Project Scope



The scope of the project is limited to Lux AI Season 3 and the implemented LuxLLM-Agent framework.



The project focuses on:



\* LLM-assisted strategic planning;

\* rule-based action verification;

\* fallback and strategy caching;

\* controlled multi-run evaluation;

\* decision trace logging;

\* replay-grounded inspection.



The project does not claim to produce a leaderboard-winning Lux AI agent. It also does not claim that qwen3:32b is universally better than DeepSeek-R1-32B. The model comparison is specific to the current framework, prompt design, environment, and evaluation setup.



The project is best understood as an artefact-based investigation into how LLM-based agents can be structured, verified, traced, and evaluated in a complex game environment.



---



## 1.8 Summary of Evaluation Evidence



The project includes controlled-run evidence for two LLM backends.



| Model           | Runs | player\_0 wins | player\_1 wins | player\_0 win rate | LLM errors |

| --------------- | ---: | ------------: | ------------: | ----------------: | ---------: |

| qwen3:32b       |   50 |            35 |            15 |               70% |          0 |

| deepseek-r1:32b |   50 |            26 |            24 |               52% |          0 |



These results show that both LLM backends can be integrated into the framework with zero recorded LLM errors in the current 50-run experiments. The qwen3:32b-backed configuration achieved a higher player\_0 win rate, while the DeepSeek-R1-32B-backed configuration demonstrated that the framework can support another reasoning-oriented LLM backend.



The evaluation also includes decision-source analysis, latency analysis, fallback analysis, replay-grounded inspection, and failure-case analysis.



---



## 1.9 Dissertation Structure



The rest of the dissertation is organised as follows.



### Chapter 2: Background and Related Work



This chapter introduces relevant background on LLM-based agents, game AI, hybrid rule-based and LLM systems, action verification, explainability, and evaluation methods.



### Chapter 3: Requirements and Methodology



This chapter presents the project requirements and methodology. It explains the functional and non-functional requirements, the choice of Lux AI Season 3, the LLM integration method, and the evaluation method.



### Chapter 4: System Design



This chapter presents the system architecture of LuxLLM-Agent. It explains state summarisation, LLM decision making, parsing, verification, fallback, caching, risk filtering, action planning, logging, and replay-grounded inspection.



### Chapter 5: Implementation



This chapter describes how the system was implemented in the project codebase. It explains the main runtime files, logging implementation, controlled-run evidence, replay generation, and LLM Decision Trace Overlay viewer.



### Chapter 6: Evaluation



This chapter evaluates the system using gameplay outcomes, LLM execution metrics, decision-source distribution, fallback analysis, latency analysis, replay-grounded inspection, and failure-case analysis.



### Chapter 7: Discussion and Conclusion



This chapter discusses the main findings, limitations, threats to validity, future work, and final conclusions.



---



## 1.10 Summary



This chapter introduced the LuxLLM-Agent project and explained its motivation, problem statement, aim, research question, objectives, contributions, scope, and dissertation structure.



The central argument is that LLM-based game agents should not be evaluated only by final match outcomes. Their decisions should also be structured, verified, traced, and inspected. LuxLLM-Agent addresses this by treating the LLM as a strategic planner inside a controlled execution pipeline, supported by rule-based verification, fallback, caching, decision-source logging, controlled evaluation, and replay-grounded visualisation.



The next chapter introduces the background and related work needed to situate this project.




