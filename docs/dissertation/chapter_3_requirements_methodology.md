\# Chapter 3: Requirements and Methodology



\## 3.1 Introduction



This chapter presents the requirements and methodology of the LuxLLM-Agent project.



The project investigates the following research question:



> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?



To answer this question, the project develops a working system that integrates LLM-based strategic planning with rule-based action verification, fallback behaviour, strategy caching, decision trace logging, controlled-run evaluation, and replay-grounded visual inspection.



This chapter explains the requirements that guided the system, the methodology used to design and evaluate it, and the reasons for selecting Lux AI Season 3 as the experimental environment.



\---



\## 3.2 Project Aim



The aim of the project is to design, implement, and evaluate a framework for inspecting and evaluating LLM-based agents in Lux AI Season 3.



The project is not intended only to build a stronger competition bot. Instead, it focuses on how LLM-based agent decisions can be structured, verified, traced, and evaluated.



The main project aim can be summarised as follows:



> To develop a decision-trace and action-verification framework that allows LLM-based Lux AI Season 3 agents to be inspected and evaluated through structured logs, controlled experiments, and replay-grounded visualisation.



This aim leads to three sub-objectives:



1\. Transform raw Lux AI Season 3 observations into structured state summaries suitable for LLM planning.

2\. Use rule-based verification, fallback, and caching to control LLM-generated strategic proposals before execution.

3\. Connect decision traces to evaluation metrics and replay visualisation so that agent behaviour can be inspected.



\---



\## 3.3 Research Questions



The main research question is:



> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?



This question is divided into three sub-research questions.



\### 3.3.1 RQ1: State summarisation



> How can raw Lux AI Season 3 observations be transformed into compact structured inputs for LLM-based strategic decision making?



This question focuses on the state summarisation process. Raw game observations are complex and low-level, so the system must extract information that is useful for strategic planning.



\### 3.3.2 RQ2: Action verification and fallback



> How can rule-based verification, fallback mechanisms, and strategy caching reduce invalid or unstable LLM-generated decisions?



This question focuses on the reliability of LLM-based agents. The LLM output is treated as a strategic proposal rather than a directly executable action.



\### 3.3.3 RQ3: Replay-grounded evaluation



> How can replay-grounded decision traces help analyse the relationship between LLM strategy, decision source, action execution, and game outcome?



This question focuses on evaluation and inspection. The system should allow the user to connect decisions to replay frames and evaluation metrics.



\---



\## 3.4 Project Requirements



The system requirements are divided into functional and non-functional requirements.



Functional requirements describe what the system should do. Non-functional requirements describe qualities such as stability, inspectability, reproducibility, and maintainability.



\---



\## 3.5 Functional Requirements



\### 3.5.1 FR1: Run a Lux AI Season 3 agent



The system must be able to run a Lux AI Season 3 agent and produce valid environment actions.



This requirement is necessary because the project is implemented as a working game-agent system rather than only a conceptual framework.



The agent must support:



\* receiving observations;

\* producing actions;

\* completing full matches;

\* recording match outcomes.



\---



\### 3.5.2 FR2: Support rule-only and LLM-enabled modes



The system must support both rule-only and LLM-enabled configurations.



This is necessary for controlled comparison and fallback testing. The same codebase should support different modes through configuration rather than separate implementations.



Examples of configuration variables include:



```text

LUX\_LLM\_ENABLED

LUX\_FORCE\_RULE\_ONLY

LUX\_LLM\_MODEL

LUX\_EXPERIMENT\_TAG

```



This allows the project to compare baseline rule-based behaviour with LLM-backed behaviour.



\---



\### 3.5.3 FR3: Summarise game state for LLM planning



The system must convert raw Lux AI Season 3 observations into compact structured summaries.



The summary should include information such as:



\* current step;

\* game phase;

\* score context;

\* unit positions;

\* unit energy;

\* known relic candidates;

\* known scoring tiles;

\* unexplored or stale tiles;

\* risk context;

\* available strategic options.



This requirement supports RQ1.



\---



\### 3.5.4 FR4: Generate structured LLM decisions



The system must use an LLM to generate high-level strategic decisions.



The LLM should not directly output raw Lux AI action arrays. Instead, it should produce structured strategic proposals such as:



\* main objective;

\* risk posture;

\* global reason;

\* unit intent;

\* target location;

\* priority;

\* expected value;

\* unit-level reason.



This design makes the LLM output easier to parse, verify, log, and inspect.



\---



\### 3.5.5 FR5: Parse LLM output into internal structures



The system must parse the LLM response into an internal representation.



The parser should detect:



\* valid outputs;

\* malformed outputs;

\* missing fields;

\* invalid intents;

\* timeout or error cases.



This requirement is necessary because LLM output cannot be assumed to be reliable.



\---



\### 3.5.6 FR6: Verify and convert strategic proposals into actions



The system must verify LLM-generated strategic proposals before execution.



Verification should check whether:



\* the referenced unit exists;

\* the target is valid;

\* the target is reachable;

\* the intent is recognised;

\* the action is legal;

\* the action appears locally safe.



Only after verification should the system convert the strategy into executable Lux AI Season 3 actions.



This requirement supports RQ2.



\---



\### 3.5.7 FR7: Provide fallback behaviour



The system must provide fallback behaviour when LLM decisions are unavailable, invalid, unsafe, or disabled.



Fallback should allow the agent to continue acting rather than failing.



Fallback may be used when:



\* rule-only mode is enabled;

\* LLM use is disabled;

\* the LLM times out;

\* the LLM output is invalid;

\* the plan fails verification;

\* a safer rule-based action is required.



\---



\### 3.5.8 FR8: Support strategy caching



The system must support strategy caching so that recent LLM plans can be reused across multiple game steps.



This is necessary because large LLM calls may be slow. Calling the LLM at every step is impractical.



The system should record when cached plans are used so that cached behaviour can be analysed later.



\---



\### 3.5.9 FR9: Record decision traces and metrics



The system must record decision traces and evaluation metrics.



Important logged fields include:



```text

step

phase

decision\_source

llm\_mode

llm\_model

llm\_called

llm\_valid

llm\_error

fallback\_used

fallback\_reason

cached\_llm\_turn

stale\_decision

risk\_filter\_changed

unit\_intent\_count

unit\_action\_count

score\_player\_0

score\_player\_1

```



These logs support controlled evaluation and replay-grounded inspection.



\---



\### 3.5.10 FR10: Support controlled multi-run evaluation



The system must support controlled multi-run evaluation for different LLM backends.



The evaluation should record:



\* total runs;

\* winner counts;

\* average rewards;

\* LLM call counts;

\* LLM errors;

\* latency;

\* fallback count;

\* decision-source distribution.



This requirement allows qwen3:32b and DeepSeek-R1-32B to be compared under the same framework.



\---



\### 3.5.11 FR11: Provide replay-grounded visual inspection



The system must provide a replay viewer that can display game behaviour and decision trace information.



The LLM Decision Trace Overlay should show:



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



This requirement supports RQ3.



\---



\## 3.6 Non-functional Requirements



\### 3.6.1 NFR1: Stability



The system should remain stable even when the LLM is disabled, slow, invalid, or unavailable.



Fallback and rule-based verification are required to support this.



\---



\### 3.6.2 NFR2: Inspectability



The system should make agent behaviour inspectable through decision traces, logs, metrics, and viewer overlays.



This is central to the project because the goal is not only to run an agent but also to understand how it behaves.



\---



\### 3.6.3 NFR3: Reproducibility



The system should support reproducible evaluation through scripts, configuration variables, JSON/JSONL logs, evidence directories, and version-controlled documentation.



\---



\### 3.6.4 NFR4: Modularity



The implementation should separate major components such as state summarisation, LLM decision making, verification, fallback, action planning, logging, and viewer generation.



This makes the project easier to test, document, and extend.



\---



\### 3.6.5 NFR5: Practicality



The system should work with local or HPC-hosted LLMs. Since large LLMs can be slow, the system should reduce unnecessary calls through caching and fallback behaviour.



\---



\### 3.6.6 NFR6: Demonstrability



The system should provide visual artefacts that can be used for project demonstration and dissertation figures.



The replay viewer and LLM Decision Trace Overlay support this requirement.



\---



\## 3.7 Methodology Overview



The project uses an artefact-based engineering methodology.



Instead of only analysing LLM-based agents theoretically, the project implements a working system and evaluates it using controlled experiments and replay-grounded inspection.



The methodology consists of five stages:



```text

1\. Environment and baseline setup

2\. LLM-assisted agent design

3\. Rule-based verification and fallback implementation

4\. Controlled-run evaluation

5\. Replay-grounded inspection and failure analysis

```



This methodology is appropriate because the research question concerns how a system can support inspection and evaluation. Therefore, the project requires both implementation and empirical evidence.



\---



\## 3.8 Environment and Task Selection



Lux AI Season 3 was selected as the main experimental environment.



It is suitable for this project because it is:



\* sequential;

\* partially observable;

\* multi-agent;

\* strategic;

\* uncertain;

\* action-constrained;

\* suitable for replay analysis.



These properties make it a good environment for studying LLM-based agent decision making. The agent must repeatedly choose actions under uncertainty, and the final outcome depends on both strategic planning and local execution.



Lux AI Season 3 is also suitable because it produces replay data that can be converted into visual inspection artefacts.



\---



\## 3.9 LLM Integration Method



The LLM is integrated as a high-level strategic planner.



The integration method follows this pipeline:



```text

Structured State Summary

&#x20;       |

&#x20;       v

Prompt Construction

&#x20;       |

&#x20;       v

LLM Strategic Decision

&#x20;       |

&#x20;       v

Structured Output Parsing

&#x20;       |

&#x20;       v

Verification and Fallback

&#x20;       |

&#x20;       v

Action Planning

```



The key design choice is that the LLM does not directly control units. It proposes strategies, which are then checked and converted into legal actions.



This method reduces the risk of invalid LLM output and makes the system easier to evaluate.



The project evaluates two LLM backends:



| Model           | Purpose                |

| --------------- | ---------------------- |

| qwen3:32b       | Main LLM backend       |

| deepseek-r1:32b | Comparison LLM backend |



The comparison tests whether the same framework can support multiple reasoning-oriented LLMs.



\---



\## 3.10 Verification and Fallback Method



The verification and fallback method is designed to make LLM decisions safer and more stable.



The system verifies whether LLM proposals are usable in the current game state. If the plan cannot be used, the system may repair it or replace it with fallback behaviour.



Fallback is used when:



\* LLM mode is disabled;

\* the LLM fails;

\* the LLM output is invalid;

\* the parsed plan is not usable;

\* the action is unsafe;

\* a cached plan is unavailable or stale.



This method supports the research focus on rule-based action verification.



The fallback mechanism also makes evaluation more honest because the system records when fallback is used. This allows the dissertation to distinguish LLM contribution from rule-based support.



\---



\## 3.11 Strategy Cache Method



The strategy cache method addresses the practical cost of large LLM inference.



Large LLMs may take several seconds to respond. For example, the DeepSeek-R1-32B evaluation recorded an average LLM latency of approximately 4143.595 ms.



Because of this, the system reuses recent LLM plans across multiple steps instead of calling the LLM at every frame.



The cache method records:



```text

cached\_llm\_turn

stale\_decision

last\_llm\_step

llm\_step\_used

```



This makes it possible to analyse both the benefits and limitations of caching.



Caching improves runtime practicality, but it can introduce stale decisions. This trade-off is discussed in the evaluation and discussion chapters.



\---



\## 3.12 Evaluation Method



The evaluation method combines quantitative and qualitative analysis.



\### 3.12.1 Quantitative evaluation



The quantitative evaluation uses controlled multi-run results.



Main metrics include:



\* total runs;

\* player\_0 wins;

\* player\_1 wins;

\* win rate;

\* rewards;

\* fresh LLM calls;

\* cached LLM turns;

\* fallback counts;

\* LLM errors;

\* LLM latency;

\* decision-source distribution.



The main 50-run comparison is:



| Model           | Runs | player\_0 wins | player\_1 wins | player\_0 win rate | LLM errors |

| --------------- | ---: | ------------: | ------------: | ----------------: | ---------: |

| qwen3:32b       |   50 |            35 |            15 |               70% |          0 |

| deepseek-r1:32b |   50 |            26 |            24 |               52% |          0 |



This comparison evaluates both gameplay outcome and framework stability.



\---



\### 3.12.2 Decision-source evaluation



Decision-source evaluation analyses how behaviour is produced.



Important decision sources include:



```text

llm\_fresh

cached\_llm

fallback

rule\_fallback

rule\_player

rule\_only

```



This makes it possible to measure how much behaviour comes from the LLM, cached LLM plans, fallback, or rule-based logic.



\---



\### 3.12.3 Replay-grounded evaluation



Replay-grounded evaluation uses the LLM Decision Trace Overlay to inspect decisions during playback.



The overlay connects replay frames to decision information such as:



\* decision source;

\* objective;

\* fallback status;

\* risk posture;

\* score context;

\* unit intents.



This allows qualitative analysis of representative cases.



\---



\### 3.12.4 Failure-case analysis



Failure-case analysis is used to examine limitations and representative problem cases.



Examples include:



\* valid LLM plans with limited strategic impact;

\* fallback replacing or supporting LLM decisions;

\* cached plans becoming stale;

\* stable execution but different model outcomes;

\* trace alignment requiring careful labelling.



This analysis is important because a high-quality dissertation should not only report successful results but should also examine system limitations.



\---



\## 3.13 Evidence Management



The project uses evidence directories and version control to manage results.



Important evidence files include:



```text

docs/demo\_evidence\_index.md

docs/demo\_evidence/llm\_model\_comparison\_summary.md

docs/demo\_evidence/hpc\_deepseek\_r1\_32b\_50run/

docs/analysis/qwen3\_vs\_deepseek\_analysis.md

docs/analysis/failure\_case\_analysis.md

```



The project separates summary evidence from large raw outputs. This keeps the repository manageable while preserving the key information needed for evaluation.



\---



\## 3.14 Ethical and Practical Considerations



The project does not involve human participants or personal data. The main ethical considerations are therefore related to transparency, reproducibility, and honest reporting.



The dissertation should avoid overclaiming. In particular, it should not claim that LuxLLM-Agent is an optimal Lux AI agent or that one LLM is universally better than another.



Instead, the project should clearly state that:



\* the system is a hybrid LLM-rule framework;

\* final outcomes are not caused only by the LLM;

\* fallback and verification contribute to behaviour;

\* evaluation results are specific to the current setup;

\* replay alignment assumptions should be clearly labelled.



Practical considerations include hardware availability, LLM latency, local and HPC configuration, and repository management.



\---



\## 3.15 Summary



This chapter presented the requirements and methodology of the LuxLLM-Agent project.



The system requirements focus on running a Lux AI Season 3 agent, integrating LLM-based strategic planning, verifying LLM proposals, supporting fallback and caching, recording decision traces, evaluating controlled runs, and providing replay-grounded visual inspection.



The methodology is artefact-based. It develops a working system and evaluates it through controlled multi-run experiments, decision-source analysis, replay-grounded inspection, and failure-case analysis.



This chapter provides the foundation for the following chapters. Chapter 4 presents the system design, Chapter 5 describes the implementation, and Chapter 6 evaluates the system using the methodology described here.



