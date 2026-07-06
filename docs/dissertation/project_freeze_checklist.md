# Project Freeze Checklist



## 1. Purpose of This Document



This document defines the freeze criteria for the LuxLLM-Agent COMP702 project.



The purpose is to prevent unlimited modification and uncontrolled feature expansion. The project has already reached the point where the main system, evidence, technical documentation, analysis documentation, and dissertation chapter drafts exist.



From this point onward, the project should focus on submission quality rather than adding new functionality.



The current target is:



> COMP702 dissertation quality improvement for a 70+ target mark.



The project should now be treated as:



> LuxLLM-Agent COMP702 Submission Freeze v1.



---



## 2. Final Project Positioning



The final project positioning is:



> LuxLLM-Agent is a decision-trace and action-verification framework for inspecting and evaluating LLM-based agents in Lux AI Season 3.



The project should not be positioned as only:



```text

an LLM game bot

```



or:



```text

a Lux AI competition-winning agent

```



The dissertation should consistently present the project as a framework that combines:



\* structured state summarisation;

\* LLM-based strategic planning;

\* structured output parsing;

\* rule-based action verification;

\* fallback behaviour;

\* strategy caching;

\* risk-aware action filtering;

\* decision trace logging;

\* controlled-run evaluation;

\* replay-grounded visual inspection.



---



## 3. Main Research Question



The final main research question is:



> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?



This question is now frozen unless the supervisor explicitly asks for a change.



---



## 4. Sub-research Questions



The final sub-research questions are:



### RQ1: State Summarisation



> How can raw Lux AI Season 3 observations be transformed into compact structured inputs for LLM-based strategic decision making?



### RQ2: Action Verification and Fallback



> How can rule-based verification, fallback mechanisms, and strategy caching reduce invalid or unstable LLM-generated decisions?



### RQ3: Replay-grounded Evaluation



> How can replay-grounded decision traces help analyse the relationship between LLM strategy, decision source, action execution, and game outcome?



These sub-research questions are now frozen unless the supervisor explicitly requests a change.



---



## 5. Completed Core Deliverables



The following core deliverables are considered complete.



### 5.1 Agent System



| Deliverable                     | Status   |

| ------------------------------- | -------- |

| Lux AI Season 3 agent runtime   | Complete |

| Rule-only mode                  | Complete |

| LLM-enabled mode                | Complete |

| qwen3:32b backend support       | Complete |

| deepseek-r1:32b backend support | Complete |

| Structured state summarisation  | Complete |

| LLM strategic decision module   | Complete |

| Action planning                 | Complete |

| Rule-based fallback             | Complete |

| Strategy caching                | Complete |

| Risk-aware action filtering     | Complete |

| Decision trace logging          | Complete |



---



### 5.2 Evaluation Evidence



| Deliverable                     | Status   |

| ------------------------------- | -------- |

| qwen3:32b 50-run evidence       | Complete |

| DeepSeek-R1-32B 50-run evidence | Complete |

| Model comparison summary        | Complete |

| LLM error analysis              | Complete |

| Latency analysis                | Complete |

| Decision-source analysis        | Complete |

| Fallback and cache analysis     | Complete |

| Failure-case analysis           | Complete |



---



### 5.3 Viewer and Visualisation



| Deliverable                               | Status   |

| ----------------------------------------- | -------- |

| Run008 isometric viewer                   | Complete |

| LLM Decision Trace Overlay                | Complete |

| Frame / step synchronisation              | Complete |

| Overlay layout fix                        | Complete |

| H-key overlay toggle                      | Complete |

| Replay-grounded inspection data           | Complete |

| Viewer ready for dissertation screenshots | Complete |



---



### 5.4 Technical Documentation



| File                                                 | Status   |

| ---------------------------------------------------- | -------- |

| `docs/technical/system\_architecture.md`              | Complete |

| `docs/technical/llm\_decision\_pipeline.md`            | Complete |

| `docs/technical/action\_verification\_and\_fallback.md` | Complete |

| `docs/technical/decision\_trace\_overlay.md`           | Complete |

| `docs/technical/evaluation\_metrics.md`               | Complete |



---



### 5.5 Analysis Documentation



| File                                          | Status   |

| --------------------------------------------- | -------- |

| `docs/analysis/qwen3\_vs\_deepseek\_analysis.md` | Complete |

| `docs/analysis/failure\_case\_analysis.md`      | Complete |



---



### 5.6 Dissertation Drafts



| Chapter     | File                                                      | Status                                 |

| ----------- | --------------------------------------------------------- | -------------------------------------- |

| Chapter 1   | `docs/dissertation/chapter\_1\_introduction.md`             | Draft complete                         |

| Chapter 2   | `docs/dissertation/chapter\_2\_background\_related\_work.md`  | Draft complete, citations still needed |

| Chapter 3   | `docs/dissertation/chapter\_3\_requirements\_methodology.md` | Draft complete                         |

| Chapter 4   | `docs/dissertation/chapter\_4\_system\_design.md`            | Draft complete                         |

| Chapter 5   | `docs/dissertation/chapter\_5\_implementation.md`           | Draft complete                         |

| Chapter 6   | `docs/dissertation/chapter\_6\_evaluation.md`               | Draft complete                         |

| Chapter 7   | `docs/dissertation/chapter\_7\_discussion\_conclusion.md`    | Draft complete                         |

| Draft index | `docs/dissertation/dissertation\_draft\_index.md`           | Complete                               |



---



## 6. Current Git Milestones



Important completed commits:



```text

2d17884 Add DeepSeek-R1 32B evaluation evidence

4e789ef Add LLM decision trace overlay viewer

572494b Add technical and evaluation analysis documentation

0a42e4b Draft dissertation system design chapter

b9de7e2 Draft dissertation implementation chapter

efa3f38 Draft dissertation evaluation chapter

1f86db7 Draft dissertation discussion and conclusion chapter

72b822e Draft dissertation requirements and methodology chapter

8db0fc4 Draft dissertation introduction chapter

542863b Draft dissertation background chapter

b9aea9a Add dissertation draft index

```



These commits show that the project has reached a stable dissertation-draft stage.



---



## 7. What Is Now Frozen



The following items are frozen and should not be changed unless there is a serious bug or supervisor request.



### 7.1 Research Direction



Frozen:



```text

Decision-trace and action-verification framework for LLM-based agents in Lux AI Season 3.

```



Do not change to a new topic such as:



```text

general LLM game agent benchmark

leaderboard Lux AI bot

multi-agent communication framework

pure reinforcement learning project

```



---



### 7.2 Main Experiment Scope



Frozen:



```text

qwen3:32b 50-run

deepseek-r1:32b 50-run

rule-based / fallback / cache / decision-source analysis

Run008 replay-grounded inspection

```



Do not add:



```text

third LLM model

100-run or 200-run expansion

new HPC benchmark

new unrelated ablation

new competition submission target

```



unless the supervisor explicitly requests it.



---



### 7.3 Viewer Scope



Frozen:



```text

Season 3 isometric replay viewer with LLM Decision Trace Overlay.

```



Do not add major new viewer features such as:



```text

multi-run selector

cross-model viewer comparison

timeline heatmap

interactive JSON inspector

new visual style

new animation pipeline

```



unless needed for a serious issue.



---



### 7.4 Dissertation Structure



Frozen:



```text

Chapter 1: Introduction

Chapter 2: Background and Related Work

Chapter 3: Requirements and Methodology

Chapter 4: System Design

Chapter 5: Implementation

Chapter 6: Evaluation

Chapter 7: Discussion and Conclusion

```



Do not add more major chapters unless the university template requires it.



---



## 8. Allowed Changes After Freeze



Only the following types of changes are allowed.



### 8.1 Bug Fixes



Allowed if:



\* the viewer does not load;

\* a documented path is wrong;

\* a table contains incorrect values;

\* a script has a clear error;

\* a dissertation statement contradicts evidence.



---



### 8.2 Citation and Reference Improvements



Allowed because Chapter 2 still needs stronger citation support.



Allowed tasks:



\* add real references;

\* add BibTeX entries;

\* replace citation placeholders;

\* improve related work comparison;

\* avoid overclaiming.



---



### 8.3 Figure and Table Preparation



Allowed because the final dissertation needs visual evidence.



Allowed tasks:



\* select final screenshots;

\* create architecture diagram;

\* create pipeline diagram;

\* prepare result tables;

\* create decision-source chart;

\* create figure/table list.



---



### 8.4 Writing Quality Improvements



Allowed tasks:



\* improve clarity;

\* remove repetition;

\* unify terminology;

\* improve transitions;

\* correct grammar;

\* shorten overly long sections;

\* make claims more cautious.



---



### 8.5 Final Assembly



Allowed tasks:



\* assemble full dissertation draft;

\* create supervisor review summary;

\* prepare final PDF or Word version;

\* check structure and formatting;

\* check references and appendix.



---



## 9. Disallowed Changes After Freeze



The following should not be done unless there is a strong reason.



```text

Do not add new LLM models.

Do not expand experiments to more runs.

Do not redesign the agent architecture.

Do not rewrite the viewer from scratch.

Do not create a new project direction.

Do not add unrelated features.

Do not repeatedly rework already stable chapters.

Do not commit raw logs, videos, PDFs, ZIP files, or large temporary outputs.

Do not use git add .

Do not use git add docs without checking staged files.

```



---



## 10. Final Completion Criteria



The project can be considered ready for supervisor review when the following are complete.



| Item                             |    Required | Status   |

| -------------------------------- | ----------: | -------- |

| Agent runtime implemented        |         Yes | Complete |

| qwen3:32b 50-run evidence        |         Yes | Complete |

| DeepSeek-R1-32B 50-run evidence  |         Yes | Complete |

| LLM Decision Trace Overlay       |         Yes | Complete |

| Technical documentation          |         Yes | Complete |

| Analysis documentation           |         Yes | Complete |

| Dissertation Chapter 1-7 drafts  |         Yes | Complete |

| Chapter 2 citation enhancement   |         Yes | Pending  |

| Figure and table plan            |         Yes | Pending  |

| Full dissertation draft assembly |         Yes | Pending  |

| Supervisor review summary        | Recommended | Pending  |

| Final Git safety check           |         Yes | Pending  |



The project should stop major modification after these pending items are complete.



---



## 11. Evidence for 70+ Target



The project supports a 70+ target because it includes:



### 11.1 Clear Research Question



The project has a focused research question about structured decision tracing and rule-based action verification.



### 11.2 Non-trivial Technical Implementation



The project includes an implemented agent, LLM decision module, action verifier, fallback system, cache, risk filter, logging, evaluation scripts, and viewer overlay.



### 11.3 Controlled Evaluation



The project includes 50-run evidence for two LLM backends.



### 11.4 Multi-dimensional Metrics



The evaluation includes win/loss, LLM errors, latency, decision-source distribution, fallback, caching, and replay alignment.



### 11.5 Critical Reflection



The project includes failure-case analysis, limitations, threats to validity, and future work.



### 11.6 Demonstrable Artefact



The project includes a replay-grounded visual interface with LLM Decision Trace Overlay.



### 11.7 Reproducible Documentation



The project includes technical docs, analysis docs, evidence index, and dissertation chapters.



---



## 12. Remaining Tasks Before Supervisor Review



Only the following tasks remain before preparing a supervisor review version.



### Task 1: Chapter 2 Citation Enhancement



File:



```text

docs/dissertation/chapter\_2\_background\_related\_work.md

```



Goal:



```text

Add real references and related-work comparisons.

```



Completion standard:



```text

Each major Chapter 2 section has at least one relevant citation.

Claims are supported.

No fake references are used.

```



---



### Task 2: Figure and Table Plan



File:



```text

docs/dissertation/figures\_and\_tables\_plan.md

```



Goal:



```text

Decide the final figures and tables.

```



Completion standard:



```text

4-6 figures are selected.

6-8 tables are selected.

Each figure/table has a purpose and source.

No unnecessary figures are added.

```



---



### Task 3: Full Dissertation Draft Assembly



File:



```text

docs/dissertation/full\_dissertation\_draft.md

```



Goal:



```text

Assemble Chapter 1-7 into one readable draft.

```



Completion standard:



```text

Chapters are in correct order.

Research question is consistent.

Terminology is consistent.

No obvious placeholders remain.

```



---



### Task 4: Supervisor Review Summary



File:



```text

docs/dissertation/supervisor\_review\_summary.md

```



Goal:



```text

Create a short summary for supervisor feedback.

```



Completion standard:



```text

The summary explains:

\- project aim;

\- research question;

\- technical contribution;

\- current evidence;

\- remaining revision tasks;

\- feedback requested.

```



---



### Task 5: Final Git Safety Check



Goal:



```text

Ensure important files are committed and dangerous files are not committed.

```



Completion standard:



```text

No mp4, pdf, zip, raw logs, frame\_log, or temporary files are staged.

All dissertation and evidence files are committed.

Remote GitHub is up to date.

```



---



## 13. Stop Condition



The project should stop active modification when the following are complete:



```text

Chapter 2 has citation support.

Figure/table plan is complete.

Full dissertation draft is assembled.

Supervisor review summary is complete.

Final Git safety check passes.

```



After this point, only supervisor-requested changes or final formatting corrections should be made.



---



## 14. Final Reminder



The project does not need more features to be strong.



The remaining work is not about adding complexity. It is about making the existing work clear, evidenced, well-cited, and professionally presented.



The correct strategy from this point onward is:



```text

Freeze features.

Improve clarity.

Support claims with evidence.

Prepare supervisor review.

Stop when completion criteria are met.

```




