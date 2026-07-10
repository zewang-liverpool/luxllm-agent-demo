# Supervisor Review Summary

## Project Title

**LuxLLM-Agent: A Decision-Trace and Action-Verification Framework for Inspecting and Evaluating LLM-based Agents in Lux AI Season 3**

---

## 1. Project Overview

This project investigates how large language models can be used as part of an agent system in Lux AI Season 3.

Instead of treating the LLM as a direct game controller, the project treats the LLM output as a **strategic proposal**. The proposal is then parsed, checked, verified, cached when appropriate, and converted into executable Lux AI actions through rule-based components.

The project focuses on three main ideas:

1. structured state summarisation for LLM-based decision making;

2. rule-based action verification and fallback for stable execution;

3. decision trace logging and replay-grounded inspection for evaluation.

The final system is therefore positioned as an inspectable and evaluable LLM-assisted agent framework, rather than as a pure leaderboard-oriented Lux AI bot.

---

## 2. Main Research Question

The current research question is:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

---

## 3. Sub-research Questions

### RQ1: State Summarisation

> How can raw Lux AI Season 3 observations be transformed into compact structured inputs for LLM-based strategic decision making?

### RQ2: Action Verification and Fallback

> How can rule-based verification, fallback mechanisms, and strategy caching reduce invalid or unstable LLM-generated decisions?

### RQ3: Replay-grounded Evaluation

> How can replay-grounded decision traces help analyse the relationship between LLM strategy, decision source, action execution, and game outcome?

---

## 4. Main Technical Contribution

The main technical contribution is a hybrid LLM-rule agent framework for Lux AI Season 3.

The implemented system includes:

* a Lux AI Season 3 agent runtime;

* structured game-state summarisation;

* LLM-based strategic decision generation;

* structured plan parsing;

* rule-based action verification;

* fallback behaviour;

* strategy caching;

* risk-aware action filtering;

* action planning;

* decision-source logging;

* controlled-run evaluation;

* an LLM Decision Trace Overlay viewer.

The key design principle is:

> The LLM output is treated as a strategic proposal, not as a directly executable game action.

This principle is important because Lux AI Season 3 requires valid and timely actions. Direct LLM output may be invalid, incomplete, unstable, or too slow. The framework therefore places deterministic verification and fallback mechanisms between the LLM and the game environment.

---

## 5. Evaluation Evidence

The project includes controlled evaluation evidence for two LLM backends.

### qwen3:32b 50-run result

| Metric            | Value |
| ----------------- | ----: |
| Total runs        |    50 |
| player_0 wins     |    35 |
| player_1 wins     |    15 |
| player_0 win rate |   70% |
| LLM errors        |     0 |

### DeepSeek-R1-32B 50-run result

| Metric                   |        Value |
| ------------------------ | -----------: |
| Total runs               |           50 |
| player_0 wins            |           26 |
| player_1 wins            |           24 |
| player_0 win rate        |          52% |
| Average player_0 reward  |          2.7 |
| Average player_1 reward  |          2.3 |
| Average fresh LLM calls  |         33.2 |
| Average cached LLM turns |       412.62 |
| Average fallback count   |       570.14 |
| Average LLM errors       |          0.0 |
| Average LLM latency      |  4143.595 ms |
| Maximum LLM latency      | 10581.076 ms |
| Average trace steps      |       1010.0 |

The current results suggest that both LLM backends can complete controlled runs without LLM execution errors in this framework, but they produce different gameplay outcomes. This supports the dissertation argument that evaluation should not rely only on final win/loss. It should also consider decision source, fallback behaviour, caching, latency, and traceability.

---

## 6. Decision-source Analysis

For the DeepSeek-R1-32B 50-run evidence, the recorded decision-source distribution is:

| Decision source | Count |
| --------------- | ----: |
| `rule_player`   | 25250 |
| `fallback`      |    94 |
| `rule_fallback` |  3163 |
| `llm_fresh`     |  1362 |
| `cached_llm`    | 20631 |

Derived values:

```text id="e02d12"

Total decision-source events = 50500

LLM-related decision events = 1362 + 20631 = 21993

Fallback-related decision events = 94 + 3163 = 3257

LLM decision-source rate = approximately 43.55%

Fallback decision-source rate = approximately 6.45%

```

This supports the claim that LuxLLM-Agent can analyse not only whether the agent wins or loses, but also where its decisions come from.

---

## 7. Replay-grounded Inspection

The project includes an LLM Decision Trace Overlay for the Season 3 replay viewer.

The overlay displays:

* frame and step;

* phase;

* decision source;

* LLM model;

* objective;

* risk posture;

* fallback status;

* risk filter status;

* score context;

* unit intents.

The overlay generation summary is:

| Metric                    | Value |
| ------------------------- | ----: |
| Replay frames             |   506 |
| Decision trace rows       |  1009 |
| LLM decision rows         |    23 |
| Matched step trace frames |   505 |
| Matched exact LLM frames  |    23 |
| Matched recent LLM frames |   506 |

This supports RQ3 by connecting replay frames with decision trace information.

---

## 8. Current Dissertation Status

The dissertation currently has a complete first draft across seven chapters.

| Chapter    | File                                                      | Status                                   |
| ---------- | --------------------------------------------------------- | ---------------------------------------- |
| Chapter 1  | `docs/dissertation/chapter_1_introduction.md`             | Draft complete                           |
| Chapter 2  | `docs/dissertation/chapter_2_background_related_work.md`  | Draft complete with citation enhancement |
| Chapter 3  | `docs/dissertation/chapter_3_requirements_methodology.md` | Draft complete                           |
| Chapter 4  | `docs/dissertation/chapter_4_system_design.md`            | Draft complete                           |
| Chapter 5  | `docs/dissertation/chapter_5_implementation.md`           | Draft complete                           |
| Chapter 6  | `docs/dissertation/chapter_6_evaluation.md`               | Draft complete                           |
| Chapter 7  | `docs/dissertation/chapter_7_discussion_conclusion.md`    | Draft complete                           |
| Full draft | `docs/dissertation/full_dissertation_draft.md`            | Assembled                                |

Supporting documents include:

| File                                            | Purpose                                                                  |
| ----------------------------------------------- | ------------------------------------------------------------------------ |
| `docs/dissertation/dissertation_draft_index.md` | Index of dissertation chapters, evidence, implementation, and next tasks |
| `docs/dissertation/project_freeze_checklist.md` | Defines project freeze criteria and stop condition                       |
| `docs/dissertation/figures_and_tables_plan.md`  | Defines the planned figures and tables                                   |
| `docs/dissertation/chapter_2_reference_plan.md` | Plans related-work references for Chapter 2                              |

---

## 9. Current Project Status

The project is now in a feature-freeze stage.

Completed:

* agent implementation;

* LLM decision module;

* action verification and fallback;

* strategy caching;

* risk-aware action filtering;

* qwen3:32b 50-run evaluation;

* DeepSeek-R1-32B 50-run evaluation;

* decision-source analysis;

* failure-case analysis;

* LLM Decision Trace Overlay;

* technical documentation;

* analysis documentation;

* dissertation chapter drafts;

* full dissertation draft assembly.

The project should not add major new features unless required.

---

## 10. Known Limitations

The dissertation will explicitly acknowledge the following limitations:

1. The system is not designed as a leaderboard-level Lux AI agent.

2. The hybrid architecture makes it difficult to attribute final outcomes only to the LLM.

3. Fallback improves stability but complicates attribution.

4. Strategy caching reduces latency but may introduce stale decisions.

5. The evaluation currently compares two LLM backends.

6. Replay-grounded inspection depends on correct alignment between replay frames and decision logs.

7. Failure-case analysis is representative rather than exhaustive.

8. The viewer supports inspection but does not prove strategic optimality.

---

## 11. Feedback Requested

I would like feedback on the following points:

1. Is the research question sufficiently technical and appropriate for COMP702?

2. Is the project positioning clear enough as a decision-trace and action-verification framework, rather than only an LLM game bot?

3. Is the evaluation scope acceptable with two 50-run LLM model evaluations?

4. Are the current metrics sufficient, including win rate, LLM errors, latency, fallback, cache, decision source, and replay-grounded inspection?

5. Does the dissertation need stronger emphasis on implementation details, evaluation, or related work?

6. Are the proposed figures and tables appropriate for the final dissertation?

7. Is there any major missing element that should be addressed before final formatting?

---

## 12. Planned Final Revision Tasks

The remaining work is limited to submission-quality preparation:

1. polish the full dissertation draft;

2. finalise citations and bibliography;

3. prepare final figures and screenshots;

4. insert figure and table references;

5. check terminology consistency;

6. check word count and chapter balance;

7. prepare the final submitted document.

No major new functionality or experiment expansion is planned unless requested.

---

## 13. Repository

GitHub repository:

```text id="w55l7k"

https://github.com/zewang-liverpool/luxllm-agent-demo

```

Main project path:

```text id="s6y5aj"

D:\\PythonProject\\lux_llm_agent

```

