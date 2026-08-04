# Response to Specification and Design Feedback

## Feedback record

| Field | Recorded value |
| --- | --- |
| Assessment | Specification and Design |
| Allocated project | Developing AI/LLM agents for playing games 3 |
| Student | Ze Wang |
| Student ID | 201868809 |
| Supervisor | Meng Fang |
| Supervisor grade | B |

The detailed assessment profile recorded A grades for 15 criteria and B grades for two criteria:

* **Aims and Requirements: B**
* **Key Literature and Background Reading: B**

The form states that the overall grade is guided by the profile but is not necessarily a weighted or averaged grade.

The supervisor's written justification was:

> The project is good. The project problem is very interesting. The task and evaluation plan is clear.

The formative guidance was:

> It would be better to consider more about research questions and reduce the number of aims.

## Interpretation

The feedback identified two related risks in the early specification:

1. the research direction needed to be expressed through clearer research questions rather than through a broad engineering feature list;
2. too many aims could make the project appear unfocused and make it difficult to connect implementation, evaluation, and conclusion.

The feedback did not request a different project topic. It asked for a more focused research structure.

## How the final project addresses the feedback

### 1. One focused project aim

The dissertation now uses one overall aim:

> To develop a decision-trace and action-verification framework that supports the inspection and evaluation of LLM-based agents in Lux AI Season 3.

This keeps the project centred on the inspectability and evaluation of LLM-based agents rather than on an open-ended list of game-agent features.

### 2. Three consolidated objectives

The seven implementation-oriented objectives previously listed in Chapter 1 have been consolidated into three research-aligned objectives:

1. structure game state for bounded LLM planning;
2. verify and control LLM-generated proposals;
3. trace, evaluate, and visually inspect agent behaviour.

The same three-objective structure is used in Chapters 1 and 3. Implementation details such as caching, fallback, multi-backend evaluation, and the viewer remain system components rather than separate project aims.

### 3. One main research question and three sub-research questions

The final main research question is:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

It is supported by three sub-research questions:

- **RQ1 — State summarisation:** how raw observations can be transformed into compact structured inputs for LLM planning;
- **RQ2 — Action verification and fallback:** how deterministic checks, fallback, and caching can control unstable or invalid model proposals;
- **RQ3 — Replay-grounded evaluation:** how decision traces can connect strategy, provenance, execution, and outcome during replay inspection.

These questions define the structure used by the requirements, system design, evaluation, and final discussion.

### 4. Evaluation is connected to the research questions

The final evaluation does not rely only on match outcomes. It reports:

- structured trace completeness;
- LLM-call validity and deterministic normalization;
- observable risk-filter interventions;
- decision provenance;
- replay linkage;
- action-array validity;
- controlled matched-seed and role-swapped outcomes;
- limitations and threats to validity.

The supplementary direct LLM-versus-LLM experiment tests whether the same tracing and verification framework remains inspectable when both players use LLM proposals. It does not introduce a new aim or change the dissertation into a model-ranking study.

### 5. Key literature and background reading have been strengthened

Chapter 2 has been rewritten as a critical, research-question-led review rather than a sequence of paper summaries. The revised chapter:

* balances positive demonstrations of LLM agents with critical evidence about autonomous planning limitations;
* adds partial observability and structured state representation as the foundation for RQ1;
* compares affordance grounding, admissible-action mapping, and formal shielding with the empirical verifier used for RQ2;
* uses AgentBench and AgentBoard to motivate trajectory-level evaluation beyond final success;
* distinguishes observable proposal and execution provenance from claims about faithful internal model reasoning;
* includes a comparative related-work matrix;
* identifies a bounded research gap without claiming formal safety or universal novelty; and
* maps the literature directly to RQ1, RQ2, and RQ3.

The consolidated bibliography now contains 24 checked sources, prioritising peer-reviewed papers, official competition material, and model technical reports where required.

## Closeout judgement

The written formative feedback is now addressed:

| Feedback item | Final status | Evidence |
| --- | --- | --- |
| Consider research questions in greater depth | Addressed | One main RQ and three sub-RQs are consistently used in Chapters 1, 3, 6, and 7 |
| Reduce the number of aims | Addressed | One overall aim and three consolidated objectives are used in Chapters 1 and 3 |
| Strengthen key literature and background reading | Addressed in the current draft | Critical synthesis, opposing evidence, comparison matrix, explicit gap, RQ mapping, and 24 consolidated sources in Chapter 2 |
| Keep task and evaluation plan clear | Preserved and strengthened | Controlled matched-seed experiments, trace reports, verifier audits, and replay inspection are documented |

No new research aim should be added during final closeout unless the supervisor identifies a specific missing requirement.
