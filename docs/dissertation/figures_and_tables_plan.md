# Figures and Tables Plan

## 1. Purpose of This Document

This document defines the planned figures and tables for the LuxLLM-Agent COMP702 dissertation.

The purpose is to avoid uncontrolled figure expansion. The dissertation should include enough visual and tabular evidence to support the project argument, but it should not include unnecessary screenshots or repeated tables.

The project is now in the freeze stage. Therefore, figures and tables should support the existing dissertation argument rather than introduce new functionality.

The central dissertation argument is:

> LuxLLM-Agent demonstrates that LLM-based game agents can be made more stable, inspectable, and evaluable by treating LLM outputs as strategic proposals rather than directly executable actions. The project-specific DTAV decision-trace approach, rule-based verification, fallback, caching, and replay-grounded inspection make it possible to analyse how LLM-backed agents behave in Lux AI Season 3.

---

## 2. Figure Selection Rules

The dissertation should use figures only when they help explain the system, evidence, or evaluation.

A figure should be included only if it supports at least one of the following:

* explains the system architecture;

* explains the LLM decision pipeline;

* shows the replay-grounded decision trace overlay;

* visualises evaluation results;

* supports failure-case analysis;

* makes the dissertation easier to understand.

Avoid adding figures that are only decorative.

---

## 3. Table Selection Rules

Tables should be used for structured information that would be difficult to read in paragraph form.

A table should be included only if it supports at least one of the following:

* summarises requirements;

* lists implementation files;

* compares model results;

* presents evaluation metrics;

* presents decision-source distribution;

* summarises limitations or threats to validity;

* summarises future work.

Avoid repeating the same table in many chapters unless the context requires it.

---

## 4. Final Figure List

The final dissertation should include approximately 5 figures.

| Figure   | Proposed title                               | Source                                                                  | Chapter        | Purpose                                                                                                              | Status                   |
| -------- | -------------------------------------------- | ----------------------------------------------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| Figure 1 | LuxLLM-Agent System Architecture    | Mermaid source embedded in Chapter 4                                | Chapter 4 | Shows the bounded proposal, verifier, action, trace, and viewer pipeline | Source complete |
| Figure 2 | LLM Decision Pipeline               | Mermaid source embedded in Chapter 5                                | Chapter 5 | Shows parsing, normalization, verification, fallback, and action construction | Source complete |
| Figure 3 | Formal Framework Evidence Rates     | `reports/figures/framework_evidence_rates.png`                       | Chapter 6 | Shows trace coverage, validity, raw-schema quality, and verifier intervention | Complete |
| Figure 4 | Formal Decision-source Distribution | `reports/figures/decision_source_distribution.png`                   | Chapter 6 | Compares cached, fresh, and rule-fallback provenance for both backends | Complete |
| Figure 5 | Run008 Isometric Replay Viewer      | `paper/figures/figure_s3_replay_viewer.png`                          | Chapter 6 | Shows the replay artefact used for qualitative inspection | Complete |
| Figure 6 | Detailed Decision Trace Overlay     | `docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html` | Chapter 6 | Shows step, source, objective, verifier fields, and unit intents | Optional |

Recommended final count:

```text

Minimum: 4 figures

Ideal: 5 figures

Maximum: 6 figures

```

Do not exceed 6 figures unless the supervisor requests more.

---

## 5. Figure Details

## 5.1 Figure 1: LuxLLM-Agent System Architecture

### Purpose

This figure should explain the complete system design.

### Suggested diagram content

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

### Recommended chapter

Chapter 4: System Design

### Why it is needed

This figure helps the reader understand the overall architecture before reading the implementation details.

### Status

Source complete in Chapter 4.

---

## 5.2 Figure 2: LLM Decision Pipeline

### Purpose

This figure should focus on how the LLM is used inside the system.

### Suggested diagram content

```text

Structured Game State

        |

        v

Prompt Construction

        |

        v

LLM Strategic Decision

        |

        v

Structured Output Parsing

        |

        v

Plan Validation

        |

        v

Fallback / Cache / Risk-aware Filtering

        |

        v

Action Planning

        |

        v

Executable Lux AI Action

```

### Recommended chapter

Chapter 5: Implementation

### Why it is needed

This figure supports the key design principle:

> The LLM output is treated as a strategic proposal, not as a directly executable game action.

### Status

Source complete in Chapter 5.

---

## 5.3 Figure 3: Run008 Isometric Replay Viewer

### Purpose

This figure should show the replay viewer without focusing only on the overlay.

### Source

```text

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

```

or:

```text

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

```

### Recommended chapter

Chapter 5 or Chapter 6

### Why it is needed

This figure demonstrates that the project includes a visual replay artefact, not only logs and tables.

### Status

Complete. The selected screenshot is `paper/figures/figure_s3_replay_viewer.png` and is referenced in Chapter 6.

---

## 5.4 Figure 4: LLM Decision Trace Overlay

### Purpose

This is the most important screenshot figure.

It should show:

* replay map;

* LLM Decision Trace Overlay;

* current frame and step;

* decision source;

* LLM model;

* objective;

* fallback status;

* risk filter status;

* unit intents;

* original match status panel visible.

### Source

```text

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

```

### Recommended chapter

Chapter 6: Evaluation

### Why it is needed

This figure directly supports RQ3:

> How can replay-grounded decision traces help analyse the relationship between LLM strategy, decision source, action execution, and game outcome?

### Status

Optional supporting artefact. The interactive overlay is retained in the repository; it should be added to the submitted dissertation only if a legible full-page capture is available.

---

## 5.5 Figure 5: DeepSeek-R1-32B Decision-source Distribution

### Purpose

This figure should visualise the decision-source distribution from the DeepSeek-R1-32B 50-run evidence.

### Source values

| Decision source | Count |
| --------------- | ----: |
| `rule_player`   | 25250 |
| `fallback`      |    94 |
| `rule_fallback` |  3163 |
| `llm_fresh`     |  1362 |
| `cached_llm`    | 20631 |

### Recommended chapter

Chapter 6: Evaluation

### Why it is needed

This figure supports the argument that the framework can analyse decision provenance rather than only final score.

### Status

Optional but recommended.

---

## 5.6 Figure 6: Failure-case Example with Overlay

### Purpose

This figure should support failure-case analysis.

Possible examples:

* cached LLM plan being reused;

* fallback being active;

* rule-only behaviour appearing in the trace;

* a valid strategy with limited outcome impact.

### Recommended chapter

Chapter 6 or Chapter 7

### Why it is needed

This figure shows critical analysis rather than only successful demonstration.

### Status

Optional.

Only include this figure if a clear screenshot can be captured without creating extra confusion.

---

## 6. Final Table List

The final dissertation should include approximately 8 tables.

| Table   | Proposed title                               | Chapter   | Purpose                                                                            | Status      |
| ------- | -------------------------------------------- | --------- | ---------------------------------------------------------------------------------- | ----------- |
| Table 1 | Functional Requirements                      | Chapter 3 | Summarises what the system must do                                                 | Needed      |
| Table 2 | Non-functional Requirements                  | Chapter 3 | Summarises quality requirements such as stability, inspectability, reproducibility | Needed      |
| Table 3 | Main Implementation Files                    | Chapter 5 | Maps project files to their implementation roles                                   | Needed      |
| Table 4 | Evaluation Metrics                           | Chapter 6 | Defines gameplay, LLM, decision-source, fallback, latency, and replay metrics      | Needed      |
| Table 5 | Formal matched-seed backend outcomes          | Chapter 6 | Reports 100 role-swapped matches per backend with uncertainty                      | Complete    |
| Table 6 | Formal trace and verification evidence        | Chapter 6 | Reports trace coverage, normalization, filtering, and action validity              | Complete    |
| Table 7 | Failure-case Summary                         | Chapter 6 | Summarises representative failure and limitation cases                             | Recommended |
| Table 8 | Threats to Validity                          | Chapter 7 | Summarises internal, external, construct, and reliability threats                  | Recommended |
| Table 9 | Future Work Summary                          | Chapter 7 | Summarises possible future improvements                                            | Optional    |

Recommended final count:

```text

Minimum: 6 tables

Ideal: 8 tables

Maximum: 9 tables

```

Do not exceed 9 tables unless necessary.

---

## 7. Table Details

## 7.1 Table 1: Functional Requirements

### Chapter

Chapter 3: Requirements and Methodology

### Suggested columns

| Requirement ID | Requirement | Description | Related RQ |
| -------------- | ----------- | ----------- | ---------- |

### Example rows

| Requirement ID | Requirement                | Description                                              | Related RQ |
| -------------- | -------------------------- | -------------------------------------------------------- | ---------- |
| FR1            | Run Lux AI S3 agent        | Agent must receive observations and return valid actions | All        |
| FR3            | State summarisation        | Convert raw observations into structured LLM input       | RQ1        |
| FR6            | Action verification        | Verify LLM proposals before execution                    | RQ2        |
| FR11           | Replay-grounded inspection | Show decision traces during replay                       | RQ3        |

---

## 7.2 Table 2: Non-functional Requirements

### Chapter

Chapter 3: Requirements and Methodology

### Suggested columns

| Requirement ID | Requirement | Description |
| -------------- | ----------- | ----------- |

### Example rows

| Requirement ID | Requirement     | Description                                                     |
| -------------- | --------------- | --------------------------------------------------------------- |
| NFR1           | Stability       | Agent should continue acting when LLM is unavailable or invalid |
| NFR2           | Inspectability  | Decision sources and traces should be recorded                  |
| NFR3           | Reproducibility | Experiments should be supported by scripts and evidence files   |
| NFR6           | Demonstrability | System should support visual replay and screenshots             |

---

## 7.3 Table 3: Main Implementation Files

### Chapter

Chapter 5: Implementation

### Suggested columns

| File | Role |
| ---- | ---- |

### Example rows

| File                  | Role                                            |
| --------------------- | ----------------------------------------------- |
| `agent.py`            | Main Lux AI Season 3 agent runtime              |
| `state_summarizer.py` | Builds structured game-state summaries          |
| `llm_decider.py`      | Handles LLM strategic decision generation       |
| `action_planner.py`   | Converts verified intents into actions          |
| `rule_policy.py`      | Provides rule-based fallback and policy support |

---

## 7.4 Table 4: Evaluation Metrics

### Chapter

Chapter 6: Evaluation

### Suggested columns

| Metric category | Metrics | Purpose |
| --------------- | ------- | ------- |

### Example rows

| Metric category     | Metrics                        | Purpose                          |
| ------------------- | ------------------------------ | -------------------------------- |
| Gameplay            | wins, rewards, win rate        | Measures final outcome           |
| LLM execution       | errors, latency, fresh calls   | Measures LLM stability           |
| Decision provenance | source counts                  | Explains where actions come from |
| Replay inspection   | matched frames, overlay fields | Connects logs to visual replay   |

---

## 7.5 Table 5: Formal Matched-seed Backend Outcomes

### Chapter

Chapter 6: Evaluation

### Final table

| Model | Matches | LLM wins | Win rate | Wilson 95% CI | Valid LLM calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| qwen3:32b | 100 | 63 | 63% | 53.2%-71.8% | 2,286/2,286 |
| deepseek-r1:32b | 100 | 60 | 60% | 50.2%-69.1% | 2,305/2,305 |

### Why it is needed

This is the main gameplay-outcome table, but it remains secondary to the trace and verification evidence.

---

## 7.6 Table 6: Formal Trace and Verification Evidence

### Chapter

Chapter 6: Evaluation

### Final table

| Metric | Qwen3-32B | DeepSeek-R1-32B |
| --- | ---: | ---: |
| Structured trace records | 103,286 | 103,305 |
| Trace and replay-link completeness | 100% | 100% |
| Post-check valid LLM calls | 2,286/2,286 | 2,305/2,305 |
| Deterministic normalizations | 520 | 0 |
| Rule-fallback steps | 2,815 | 2,815 |
| Risk-filter changed steps | 5,590 | 7,090 |
| Action-array shape validity | 100% | 100% |

### Why it is needed

This table directly supports the research question by connecting inspectability, structured-output checks, verifier intervention, and executable action evidence.

---

## 7.7 Table 7: Failure-case Summary

### Chapter

Chapter 6: Evaluation

### Suggested columns

| Case | Description | What it shows | Possible improvement |
| ---- | ----------- | ------------- | -------------------- |

### Suggested rows

| Case                     | Description                                            | What it shows                                           | Possible improvement           |
| ------------------------ | ------------------------------------------------------ | ------------------------------------------------------- | ------------------------------ |
| Valid plan, weak outcome | LLM plan is valid but does not guarantee strong result | Validity is not strategic quality                       | Add utility scoring            |
| Fallback support         | Rule fallback replaces or supports LLM decision        | Fallback improves stability but complicates attribution | Separate fallback metrics      |
| Cached plan stale        | Cached LLM plan may become outdated                    | Efficiency-adaptiveness trade-off                       | Event-triggered refresh        |
| Different model outcomes | qwen3 and DeepSeek stable but different win rates      | Stability is not equal to performance                   | Compare strategy distributions |
| Trace alignment          | Viewer depends on replay/log alignment                 | Replay inspection needs careful labelling               | Add shared run IDs             |

---

## 7.8 Table 8: Threats to Validity

### Chapter

Chapter 7: Discussion and Conclusion

### Suggested columns

| Threat | Description | Mitigation |
| ------ | ----------- | ---------- |

### Suggested rows

| Threat             | Description                                        | Mitigation                            |
| ------------------ | -------------------------------------------------- | ------------------------------------- |
| Internal validity  | Hybrid system makes LLM-only attribution difficult | Decision-source logging               |
| External validity  | Lux AI S3 may not generalise to other environments | State scope clearly                   |
| Construct validity | Win rate does not fully measure strategic quality  | Use multi-dimensional metrics         |
| Reliability        | Runs depend on local/HPC setup                     | Use scripts, logs, and evidence files |

---

## 7.9 Table 9: Future Work Summary

### Chapter

Chapter 7: Discussion and Conclusion

### Suggested columns

| Future work | Motivation |
| ----------- | ---------- |

### Suggested rows

| Future work                  | Motivation                                     |
| ---------------------------- | ---------------------------------------------- |
| Event-triggered LLM refresh  | Reduce stale cached decisions                  |
| Stronger utility scoring     | Improve target selection                       |
| Better verifier logging      | Improve failure analysis                       |
| Multi-run viewer support     | Generalise replay inspection                   |
| Cross-model trace comparison | Compare qwen3 and DeepSeek behaviours visually |

This table is optional because Chapter 7 may already discuss future work in prose.

---

## 8. Screenshot Capture Plan

The dissertation should include screenshots only after selecting final viewer states.

Recommended screenshot capture rules:

```text

Use the current v09n12d trace overlay viewer.

Use browser zoom that keeps text readable.

Ensure the overlay does not cover Match Status.

Capture at least one frame where objective, source, fallback, and score are visible.

Avoid screenshots with console open.

Avoid screenshots showing irrelevant desktop UI.

Use consistent image size.

```

Recommended viewer URL:

```text

http://localhost:8000/docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

```

Recommended command to start local server:

```text

python -m http.server 8000

```

---

## 9. Final Figure/Table Limit

To avoid over-expansion, the dissertation should stop at:

```text

Maximum figures: 6

Maximum tables: 9

```

The recommended target is:

```text

Figures: 5

Tables: 8

```

This is enough for a strong COMP702 dissertation without making it look overloaded.

---

## 10. Remaining Figure/Table Tasks

The visual evidence set is closed. The remaining work belongs to final document production:

1. Render the Mermaid architecture and decision-pipeline sources in the required submission format.

2. Confirm that the four completed PNG figures and the selected replay screenshot remain legible at final page size.

3. Number captions and add cross-references after conversion from Markdown.

4. Add alternative text or an equivalent textual description where required by the submission format.

5. Use the detailed overlay as Figure 6 only if it remains readable; otherwise retain it as a linked supporting artefact rather than adding another crowded screenshot.

No additional charts or tables should be created unless supervisor review identifies a specific missing argument.

---

## 11. Stop Condition

Figure and table planning is complete when:

```text

The final figure list has no more than 6 figures.

The final table list has no more than 9 tables.

Each figure has a clear source and purpose.

Each table has a clear chapter and purpose.

No extra visual artefacts are added without supervisor request.

```

After this, do not add more figures or tables unless there is a clear need.

