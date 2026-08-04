# Supervisor Review Summary

**Student:** Ze Wang (`201868809`)

**Supervisor:** Meng Fang

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

The primary evaluation uses 50 matched environment seeds per backend and swaps the LLM-controlled side for every seed. Each backend therefore completes 100 matches against the same rule-based policy.

| Model | Matches | LLM wins | Win rate | Wilson 95% CI | Valid LLM calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| qwen3:32b | 100 | 63 | 63% | 53.2%-71.8% | 2,286/2,286 |
| deepseek-r1:32b | 100 | 60 | 60% | 50.2%-69.1% | 2,305/2,305 |

Across these 200 primary matches, all 206,591 structured traces passed the recorded completeness checks, replay linkage and action-array shape validity were 100%, and no LLM timeout, API error, or downstream action fallback was observed. Deterministic checks normalized 520 Qwen responses, while the risk filter changed proposed targets on 5,590 Qwen steps and 7,090 DeepSeek steps. The matched backend difference was not statistically supported, so these outcomes are not presented as a general model ranking.

Following supervisor feedback, a supplementary direct LLM-versus-LLM experiment placed Qwen and DeepSeek against each other over another 50 role-swapped seed pairs. It completed all 100 matches, retained 106,317 complete traces, and recorded 4,676/4,676 valid fresh calls. Qwen won 54 matches and DeepSeek won 46, but the seed-level exact sign p-value was 0.503. The main value of this experiment is that tracing, normalization, and risk-filter interventions remained attributable when both players used LLM proposals concurrently.

---

## 6. Decision-source and Verifier Analysis

The retained traces distinguish fresh LLM calls, cached plans, rule fallback, normalization, and risk-filter interventions. This supports the central claim that LuxLLM-Agent can analyse not only whether an agent wins or loses, but also where a decision came from and whether deterministic components changed the proposal before action construction. The raw evidence, machine-readable summaries, and audit scripts are retained so the reported counts can be checked independently.

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

* 200-match primary matched-seed and role-swapped evaluation;

* 100-match supplementary direct LLM-versus-LLM evaluation;

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

3. Is the evaluation scope acceptable with 200 primary matches and the 100-match direct LLM-versus-LLM supplementary experiment?

4. Are the current metrics sufficient, including win rate, LLM errors, latency, fallback, cache, decision source, and replay-grounded inspection?

5. Does the dissertation need stronger emphasis on implementation details, evaluation, or related work?

6. Are the proposed figures and tables appropriate for the final dissertation?

7. Is there any major missing element that should be addressed before final formatting?

---

## 12. Planned Final Revision Tasks

The remaining work is limited to submission-quality preparation:

1. obtain the official COMP702 assessment brief and confirm its word limit and formatting rules;

2. add the confirmed student ID and exact programme title to the title page;

3. convert the canonical Markdown draft into the required submission format;

4. verify captions, cross-references, pagination, contents pages, and figure readability;

5. perform one supervisor review and one final proofread before submission.

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

