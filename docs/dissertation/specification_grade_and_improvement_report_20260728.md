# Progress Report Following the Specification and Design Feedback

**Project:** Developing AI/LLM Agents for Playing Games 3<br>
**Dissertation title:** *LuxLLM-Agent: A Decision-Trace and Action-Verification Framework for Inspecting and Evaluating LLM-based Agents in Lux AI Season 3*<br>
**Student:** Ze Wang (201868809)<br>
**Supervisor:** Meng Fang<br>
**Assessment reviewed:** Specification and Design<br>
**Recorded supervisor grade:** B<br>
**Report date:** 28 July 2026

## 1. Executive Summary

The Specification and Design assessment received an overall grade of **B**. As an approximate interpretation, a B normally represents a good or Merit-level performance, broadly comparable to the **60–69%** range. This is not an exact numerical conversion: the feedback form states that the overall grade is based on a profile of criteria and is not necessarily a weighted or averaged mark. The University framework also allows departments to define assessment-specific qualitative descriptors.

The written feedback was positive about the project problem, task, and evaluation plan, but recommended:

1. giving greater consideration to the research questions; and
2. reducing the number of aims.

The detailed category profile also awarded B for **Key Literature and Background Reading**. The project has now been revised directly in response to all three points. The dissertation is organised around one focused aim, three consolidated objectives, one main research question, and three supporting sub-research questions. Chapter 2 has been rewritten as a critical review with opposing evidence, a comparative synthesis, an explicit research gap, and direct mapping to the research questions. The implementation and evaluation have also been aligned with this research structure.

The project now contains a complete working framework, reproducible experiment scripts, automated tests, structured decision traces, rule-based verification evidence, replay-grounded visual inspection, and results from **300 controlled matches**. These changes strengthen the project beyond its original specification. However, they should be described as evidence of improvement rather than as a claim that the work has already been reassessed at an A or Distinction level.

## 2. Original Feedback and Its Interpretation

The supervisor's written justification was:

> The project is good. The project problem is very interesting. The task and evaluation plan is clear.

The formative guidance was:

> It would be better to consider more about research questions and reduce the number of aims.

This feedback indicated that the original proposal was feasible and interesting, but its academic focus was too broad. The key weakness was not the topic itself. It was the relationship between the research question, project aims, implementation, evaluation, and conclusion.

The required response was therefore to make the project more research-led without losing the already clear engineering and evaluation plan.

## 3. Improvements Made in Response to the Feedback

### 3.1 One focused overall aim

The project now uses the following overall aim:

> To develop a decision-trace and action-verification framework that supports the inspection and evaluation of LLM-based agents in Lux AI Season 3.

This replaces a broad feature-oriented description with a single research focus: the inspectability and evaluation of LLM-based agents.

### 3.2 Reduction from seven objectives to three

The earlier implementation-oriented list has been consolidated into three research-aligned objectives:

1. **Structure game state for bounded LLM planning.**
2. **Verify and control LLM-generated proposals.**
3. **Trace, evaluate, and visually inspect agent behaviour.**

Components such as caching, fallback, model support, experiment automation, logging, and the viewer remain important parts of the system, but they are no longer presented as separate project aims.

### 3.3 A clearer research-question structure

The revised main research question is:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

It is supported by three sub-research questions:

- **RQ1 — State summarisation:** How can raw Lux AI Season 3 observations be transformed into compact structured inputs for LLM-based strategic decision making?
- **RQ2 — Action verification and fallback:** How can rule-based verification, fallback mechanisms, and strategy caching reduce invalid or unstable LLM-generated decisions?
- **RQ3 — Replay-grounded evaluation:** How can replay-grounded decision traces help analyse the relationship between LLM strategy, decision source, action execution, and game outcome?

The same structure is now used consistently in the introduction, methodology, evaluation, and conclusion.

### 3.4 Evaluation aligned with the research question

The evaluation no longer treats win rate as the only indicator of success. It examines:

- structured trace completeness;
- decision provenance;
- raw and post-check structured-output validity;
- deterministic normalization;
- rule-based risk-filter interventions;
- fallback and caching behaviour;
- action-array validity;
- replay linkage;
- matched-seed and role-swapped outcomes; and
- limitations and threats to validity.

This alignment provides direct evidence for the central research question rather than only demonstrating that the game agent can run.

### 3.5 Supplementary LLM-versus-LLM evidence

Following further supervisor discussion, a direct LLM-versus-LLM experiment was added. Qwen3-32B and DeepSeek-R1-32B played 100 matches using 50 matched seeds with their player roles swapped.

This experiment remains supplementary. Its purpose is to test whether the same trace-and-verification framework can maintain separate provenance and verifier evidence when both players use LLM-generated proposals. It does not change the dissertation into a general model-ranking study.

### 3.6 Stronger key literature and background reading

Chapter 2 now contains 24 consolidated sources and gives priority to peer-reviewed research, official Lux AI material, and model technical reports where required. It adds critical evidence on autonomous LLM planning, admissible-action grounding, partial observability, runtime shielding, trajectory-level agent evaluation, and the limits of treating generated rationales as faithful explanations. It also compares the closest prior work and states precisely what LuxLLM-Agent does and does not claim.

## 4. Current Empirical Evidence

### 4.1 Primary evaluation

The primary evaluation contains 200 completed matches:

| Backend | Matches | LLM-assisted wins | Win rate | Wilson 95% interval | Valid calls after checks |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen3-32B | 100 | 63 | 63% | 53.2%–71.8% | 2,286/2,286 |
| DeepSeek-R1-32B | 100 | 60 | 60% | 50.2%–69.1% | 2,305/2,305 |

Across both backends:

- all 200 planned matches completed;
- 206,591 structured trace records were retained;
- recorded trace completeness, replay linkage, and action-array shape validity were 100%;
- all 4,591 LLM calls were valid after deterministic checks;
- 520 Qwen responses required deterministic normalization;
- risk filtering changed proposed targets on 5,590 Qwen steps and 7,090 DeepSeek steps; and
- no LLM timeout, API error, or downstream action fallback was observed in the formal runs.

These figures show why the verification layer is an evaluated part of the system rather than only an architectural claim.

### 4.2 Supplementary direct LLM-versus-LLM evaluation

The supplementary experiment completed all 100 planned matches:

| Metric | Result |
| --- | ---: |
| Qwen wins | 54 |
| DeepSeek wins | 46 |
| Fresh LLM calls valid after checks | 4,676/4,676 |
| Complete structured trace records | 106,317 |
| Deterministic normalization interventions | 571 |
| Seed-level exact sign-test p-value | 0.503 |

The 54:46 outcome was not statistically significant under the matched-seed analysis. Therefore, it is not used to claim that one model is generally superior. The important result for this dissertation is that complete per-player traces and verifier interventions remained observable when both sides used the framework concurrently.

## 5. Improvement Against the Original Assessment Concerns

| Original concern or strength | Action taken | Current evidence | Status |
| --- | --- | --- | --- |
| Research questions needed more consideration | Defined one main RQ and three focused sub-RQs | Consistent RQ structure in Chapters 1, 3, 6, and 7 | Addressed |
| Too many aims | Reduced seven implementation-oriented objectives to three research objectives under one overall aim | Matching aim and objectives in the introduction and methodology | Addressed |
| Key Literature and Background Reading received B | Rewrote Chapter 2 as a critical, RQ-led review | Opposing evidence, related-work matrix, research gap, RQ mapping, and 24 consolidated sources | Addressed in the current draft |
| Task was clear | Preserved the complete end-to-end pipeline | State summarisation, LLM planning, verification, fallback, action planning, logging, and viewer | Strengthened |
| Evaluation plan was clear | Expanded evaluation beyond outcomes | 300 controlled matches, uncertainty estimates, trace metrics, verifier audits, and replay inspection | Strengthened |
| Academic contribution needed sharper positioning | Reframed the work as a trace-and-verification framework | Evaluation and conclusion focus on inspectability and verification rather than only gameplay | Strengthened |
| Reproducibility was previously weak | Added setup, execution, validation, test, and HPC experiment workflows | Reproducibility guide, pinned environments, automated tests, validation tools, provenance, seeds, and retained summaries | Substantially addressed |

## 6. Current Assessment of Project Maturity

The project has progressed from a promising specification to a functioning and empirically evaluated Master's project. Its principal strengths are:

- a clear and technically relevant research problem;
- a complete end-to-end implementation;
- explicit separation between LLM proposals and executable actions;
- observable deterministic verification and fallback mechanisms;
- structured and replay-linked decision traces;
- controlled matched-seed and role-swapped experiments;
- support for two local LLM backends;
- automated testing and evidence validation; and
- a clear statement of limitations that avoids unsupported model-ranking or causal claims.

The remaining work is mainly dissertation and presentation closeout rather than further expansion of the software. The priority is final citation cross-checking, figure readability, manual proofreading, and ensuring that each reported result is explicitly connected to the research questions.

## 7. Standard for Final Closeout

The project should be considered technically complete when:

1. the existing automated tests and project-evidence validation pass;
2. the 200-match primary and 100-match supplementary evidence is preserved and reproducible from the documented workflow;
3. the viewer clearly identifies Lux AI Season 3 and displays proposal, verification, provenance, and executed-state information;
4. all quantitative claims in the dissertation can be traced to retained evidence;
5. each research question is explicitly answered in the evaluation and conclusion;
6. limitations and threats to validity are stated without overclaiming; and
7. the final dissertation and demonstration have passed manual proofreading and presentation checks.

Once these criteria are satisfied, further features or large experiments should only be added if they address a specific supervisor or assessment requirement.

## 8. Questions for Supervisor Review

I would appreciate feedback on the following points:

1. Does the revised structure adequately address the recommendation to reduce the number of aims and develop the research questions more clearly?
2. Is the project now positioned clearly enough as a decision-trace and action-verification framework rather than only as an LLM game-playing agent?
3. Is the current empirical scope—200 primary matches and 100 supplementary direct LLM-versus-LLM matches—appropriate for the final dissertation?
4. Are there any required COMP702 dissertation formatting, word-count, template, or submission conventions that I should follow?
5. Which area should receive the greatest attention before submission: literature and critical discussion, evaluation presentation, user-interface presentation, or another area?

## 9. Short Supervisor Update

> Following the B-grade Specification and Design feedback, I revised the project to address the two main recommendations. I reduced the original objectives to one overall aim and three focused objectives, and I now use one main research question with three supporting sub-questions consistently across the dissertation. The evaluation has also been aligned with these questions. The project currently includes a complete decision-trace and rule-based action-verification framework, 200 primary matched-seed matches, and a supplementary 100-match direct LLM-versus-LLM experiment. All planned matches completed, the retained trace and verifier evidence passed the project checks, and the results are reported with uncertainty and limitations rather than as a general model ranking. I would be grateful for your feedback on whether this revision adequately addresses the original assessment comments and whether there are any required dissertation formatting or submission guidelines I should now follow.

## 10. Grade Interpretation Note

The approximate interpretation of B as Merit-level work should not be treated as an official conversion for this individual assessment. The University of Liverpool's Code of Practice establishes the postgraduate pass, Merit, and Distinction framework, while departments may define assessment-specific qualitative descriptors. The recorded B grade remains the authoritative result for the Specification and Design assessment unless the School provides an exact numerical conversion.

Official reference: [University of Liverpool — Code of Practice on Assessment](https://www.liverpool.ac.uk/study/academic-quality-and-standards-division/academic-codes-of-practice/code-of-practice-on-assessment/)
