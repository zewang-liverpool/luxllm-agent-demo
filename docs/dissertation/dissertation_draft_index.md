# Dissertation Draft Index

## Project Title

**LuxLLM-Agent: A Decision-Trace and Action-Verification Framework for Inspecting and Evaluating LLM-based Agents in Lux AI Season 3**

---

## Current Dissertation Goal

The current goal is to develop the project into a strong COMP702 dissertation with a target mark of 70+.

The dissertation is positioned as an artefact-based computer science project. It does not only present an LLM game-playing agent. Instead, it presents a framework for structuring, verifying, tracing, evaluating, and visually inspecting LLM-based agent decisions in Lux AI Season 3.

---

## Main Research Question

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

---

## Sub-research Questions

### RQ1: State Summarisation

> How can raw Lux AI Season 3 observations be transformed into compact structured inputs for LLM-based strategic decision making?

### RQ2: Action Verification and Fallback

> How can rule-based verification, fallback mechanisms, and strategy caching reduce invalid or unstable LLM-generated decisions?

### RQ3: Replay-grounded Evaluation

> How can replay-grounded decision traces help analyse the relationship between LLM strategy, decision source, action execution, and game outcome?

---

## Dissertation Chapter Drafts

The current dissertation draft consists of seven chapters.

| Chapter   | File                                                      | Status                           | Purpose                                                                                                                |
| --------- | --------------------------------------------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| Chapter 1 | `docs/dissertation/chapter_1_introduction.md`             | Draft complete                   | Introduces the project, motivation, problem, aim, RQ, contributions, and dissertation structure                        |
| Chapter 2 | `docs/dissertation/chapter_2_background_related_work.md`  | Draft complete, citations needed | Provides background on LLM agents, game AI, hybrid LLM-rule systems, action verification, traceability, and evaluation |
| Chapter 3 | `docs/dissertation/chapter_3_requirements_methodology.md` | Draft complete                   | Defines requirements and methodology                                                                                   |
| Chapter 4 | `docs/dissertation/chapter_4_system_design.md`            | Draft complete                   | Explains the system architecture and design rationale                                                                  |
| Chapter 5 | `docs/dissertation/chapter_5_implementation.md`           | Draft complete                   | Describes implementation details and project files                                                                     |
| Chapter 6 | `docs/dissertation/chapter_6_evaluation.md`               | Draft complete                   | Evaluates gameplay outcomes, LLM stability, decision sources, fallback, latency, overlay inspection, and failure cases |
| Chapter 7 | `docs/dissertation/chapter_7_discussion_conclusion.md`    | Draft complete                   | Discusses findings, contributions, limitations, threats to validity, future work, and conclusion                       |

---

## Supporting Technical Documentation

The following technical documents support the dissertation chapters.

| File                                                 | Purpose                                                                                        |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `docs/technical/system_architecture.md`              | Explains the overall architecture of LuxLLM-Agent                                              |
| `docs/technical/llm_decision_pipeline.md`            | Explains how LLM decisions are generated, parsed, verified, cached, and converted into actions |
| `docs/technical/action_verification_and_fallback.md` | Explains rule-based verification, fallback, strategy cache, and decision sources               |
| `docs/technical/decision_trace_overlay.md`           | Explains the LLM Decision Trace Overlay viewer                                                 |
| `docs/technical/evaluation_metrics.md`               | Defines gameplay, LLM, fallback, decision-source, and replay-grounded metrics                  |

---

## Supporting Analysis Documentation

The following analysis documents support Chapter 6 and Chapter 7.

| File                                          | Purpose                                               |
| --------------------------------------------- | ----------------------------------------------------- |
| `docs/analysis/qwen3_vs_deepseek_analysis.md` | Analyses qwen3:32b and DeepSeek-R1-32B 50-run results |
| `docs/analysis/failure_case_analysis.md`      | Provides representative failure and limitation cases  |

---

## Main Implementation Files

The main implementation files are:

| File                                  | Role                                                |
| ------------------------------------- | --------------------------------------------------- |
| `agent.py`                            | Main Lux AI Season 3 agent runtime                  |
| `baseline_agent.py`                   | Baseline or rule-based agent implementation         |
| `main.py`                             | Runtime entry point                                 |
| `config.py`                           | Configuration and environment-variable handling     |
| `lux_state.py`                        | Lux AI state representation                         |
| `state_summarizer.py`                 | Converts raw observations into structured summaries |
| `llm_decider.py`                      | Handles LLM-backed strategic decision making        |
| `action_planner.py`                   | Converts verified intents into executable actions   |
| `rule_policy.py`                      | Rule-based policy and fallback support              |
| `record_match_result_from_console.py` | Records match-level evaluation results              |

---

## Main Viewer and Overlay Files

The main viewer and overlay files are:

| File                                                                 | Purpose                                                              |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html` | Current viewer with LLM Decision Trace Overlay                       |
| `data/isometric_replay_frames.json`                           | Replay frame data for Run008                                         |
| `data/run008_decision_trace_overlay.json`                            | Step-aligned decision trace overlay data                             |
| `tools/build_run008_isometric_from_replay.py`                        | Builds isometric replay frames from replay data                      |
| `tools/build_run008_decision_trace_overlay.py`                       | Aligns replay frames with decision trace logs                        |
| `tools/build_v09n12d_trace_overlay_viewer.py`                        | Builds the overlay viewer                                            |
| `tools/fix_v09n12d_trace_overlay_layout.py`                          | Fixes overlay layout so it does not block the original right sidebar |

---

## Main Evidence Files

The main evidence files are:

| File                                                                                                                          | Purpose                                             |
| ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------- |
| `docs/demo_evidence_index.md`                                                                                                 | Index of project evidence                           |
| `docs/demo_evidence/llm_model_comparison_summary.md`                                                                          | Summary of qwen3:32b and DeepSeek-R1-32B comparison |
| `docs/demo_evidence/hpc_deepseek_r1_32b_50run/deepseek_r1_32b_50run_summary.md`                                               | Human-readable DeepSeek-R1-32B 50-run summary       |
| `docs/demo_evidence/hpc_deepseek_r1_32b_50run/20260624_152843_deepseek_r1_32b_gpu_50run_job9189419/summary_50run.json`        | Machine-readable DeepSeek-R1-32B 50-run summary     |
| `docs/demo_evidence/hpc_deepseek_r1_32b_50run/20260624_152843_deepseek_r1_32b_gpu_50run_job9189419/match_history_50run.jsonl` | Match-level DeepSeek-R1-32B 50-run history          |

---

## Key Evaluation Results

### qwen3:32b 50-run Result

| Metric            |       Value |
| ----------------- | ----------: |
| Model             | `qwen3:32b` |
| Total runs        |          50 |
| player_0 wins     |          35 |
| player_1 wins     |          15 |
| Draws             |           0 |
| player_0 win rate |         70% |
| LLM errors        |           0 |

### DeepSeek-R1-32B 50-run Result

| Metric                    |             Value |
| ------------------------- | ----------------: |
| Model                     | `deepseek-r1:32b` |
| Total runs                |                50 |
| player_0 wins             |                26 |
| player_1 wins             |                24 |
| player_0 win rate         |               52% |
| Average player_0 reward   |               2.7 |
| Average player_1 reward   |               2.3 |
| Average fresh LLM calls   |              33.2 |
| Average LLM strategy used |             27.24 |
| Average cached LLM turns  |            412.62 |
| Average fallback count    |            570.14 |
| Average LLM errors        |               0.0 |
| Average LLM latency       |       4143.595 ms |
| Maximum LLM latency       |      10581.076 ms |
| Average trace steps       |            1010.0 |

---

## DeepSeek-R1-32B Decision Source Distribution

| Decision source | Count |
| --------------- | ----: |
| `rule_player`   | 25250 |
| `fallback`      |    94 |
| `rule_fallback` |  3163 |
| `llm_fresh`     |  1362 |
| `cached_llm`    | 20631 |

Derived values:

```text

Total decision-source events = 50500

LLM-related decision events:

llm_fresh + cached_llm = 1362 + 20631 = 21993

Fallback-related decision events:

fallback + rule_fallback = 94 + 3163 = 3257

```

Approximate rates:

```text

LLM decision-source rate = 21993 / 50500 = approximately 43.55%

Fallback decision-source rate = 3257 / 50500 = approximately 6.45%

```

---

## Replay-grounded Overlay Evidence

The current LLM Decision Trace Overlay uses:

```text

data/run008_decision_trace_overlay.json

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

```

Overlay generation summary:

| Metric                    | Value |
| ------------------------- | ----: |
| Replay frames             |   506 |
| Decision trace rows       |  1009 |
| LLM decision rows         |    23 |
| Matched step trace frames |   505 |
| Matched exact LLM frames  |    23 |
| Matched recent LLM frames |   506 |

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

This supports replay-grounded decision inspection.

---

## Current Dissertation Argument

The central argument of the dissertation is:

> LuxLLM-Agent demonstrates that LLM-based game agents can be made more stable, inspectable, and evaluable by treating LLM outputs as strategic proposals rather than directly executable actions. Structured decision tracing, rule-based verification, fallback, caching, and replay-grounded inspection make it possible to analyse how LLM-backed agents behave in Lux AI Season 3.

---

## Main Contributions

The dissertation currently claims the following contributions:

1. A structured LLM-assisted agent framework for Lux AI Season 3.

2. A rule-based action verification layer that controls LLM strategic proposals before execution.

3. A fallback and strategy-cache mechanism for improving stability and reducing LLM latency.

4. Decision-source logging for analysing whether actions come from fresh LLM decisions, cached plans, fallback, rule fallback, or rule-based policy.

5. Controlled 50-run evidence for qwen3:32b and DeepSeek-R1-32B.

6. A replay-grounded LLM Decision Trace Overlay for visual inspection.

7. Failure-case analysis showing limitations such as stale cached plans, fallback attribution, and valid but weak LLM strategies.

---

## Current Limitations

The dissertation should clearly acknowledge the following limitations:

* The system is not designed as a leaderboard-level Lux AI agent.

* Final match outcomes cannot be attributed only to the LLM because the system is hybrid.

* Fallback improves stability but complicates attribution.

* Strategy caching reduces latency but can introduce stale decisions.

* The evaluation compares only two LLM backends.

* Some replay-grounded inspection depends on correct alignment between replay frames and trace logs.

* Failure-case analysis is representative rather than exhaustive.

* Chapter 2 still needs stronger citation support.

* Figures and tables still need to be finalised.

---

## Next Revision Tasks

The next revision stage should focus on quality improvement rather than adding major new features.

Priority tasks:

1. Add real citations to Chapter 2.

2. Create a figure and table list.

3. Select final dissertation screenshots.

4. Add architecture and pipeline diagrams.

5. Check terminology consistency across all chapters.

6. Convert repeated technical text into polished dissertation prose.

7. Add references and bibliography.

8. Assemble a single full dissertation draft.

9. Review word count and chapter balance.

10. Prepare a supervisor review version.

---

## Suggested Figures

Suggested dissertation figures:

| Figure                                      | Source                                                               | Purpose                                               |
| ------------------------------------------- | -------------------------------------------------------------------- | ----------------------------------------------------- |
| System architecture diagram                 | Based on Chapter 4                                                   | Shows complete LuxLLM-Agent pipeline                  |
| LLM decision pipeline diagram               | Based on Chapter 5                                                   | Shows structured state to LLM plan to verified action |
| LLM Decision Trace Overlay screenshot       | `docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html` | Shows replay-grounded inspection                      |
| qwen3 vs DeepSeek result table              | Chapter 6                                                            | Shows model comparison                                |
| DeepSeek decision-source distribution chart | `summary_50run.json`                                                 | Shows LLM/cache/fallback/rule contribution            |
| Failure-case example screenshot             | Viewer overlay                                                       | Shows qualitative analysis case                       |

---

## Suggested Tables

Suggested dissertation tables:

| Table                                 | Purpose   |
| ------------------------------------- | --------- |
| Functional requirements table         | Chapter 3 |
| Non-functional requirements table     | Chapter 3 |
| Main implementation files             | Chapter 5 |
| Evaluation metrics                    | Chapter 6 |
| qwen3 vs DeepSeek comparison          | Chapter 6 |
| DeepSeek decision-source distribution | Chapter 6 |
| Threats to validity                   | Chapter 7 |
| Future work summary                   | Chapter 7 |

---

## Current Git Milestones

Recent important commits:

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

```

---

## Immediate Next Step

The immediate next step is to improve Chapter 2 with citations and related work references.

Recommended next file:

```text

docs/dissertation/chapter_2_background_related_work.md

```

Recommended task:

```text

Chapter 2 citation enhancement:

- Add references for LLM agents.

- Add references for ReAct-style reasoning and tool use.

- Add references for planning with LLMs.

- Add references for game AI and sequential decision making.

- Add references for explainability, traceability, and evaluation.

- Add references for Lux AI / competition environment if available.

```

