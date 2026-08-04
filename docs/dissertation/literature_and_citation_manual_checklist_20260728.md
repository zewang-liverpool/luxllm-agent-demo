# Chapter 2 Manual Reading and Citation Audit Checklist

## 1. Files to inspect

| Purpose | Local file |
| --- | --- |
| Main file under review | `D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_2_background_related_work.md` |
| Authoritative dissertation reference list | `D:\PythonProject\lux_llm_agent\docs\dissertation\references.md` |
| Assembled dissertation | `D:\PythonProject\lux_llm_agent\docs\dissertation\full_dissertation_draft.md` |
| Feedback response record | `D:\PythonProject\lux_llm_agent\docs\dissertation\specification_feedback_response_20260728.md` |
| Original reference-planning record | `D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_2_reference_plan.md` |
| Dissertation assembly tool | `D:\PythonProject\lux_llm_agent\tools\assemble_dissertation.py` |

The authoritative source for the current Markdown dissertation is `references.md`. If the dissertation is later converted to LaTeX, the approved entries must also be transferred to the final `.bib` file.

## 2. Preparation

- [ ] **P1 — Open Chapter 2.** Confirm that the file opens normally and Chinese/European author names contain no broken characters.
- [ ] **P2 — Open the reference list.** Confirm that all 24 entries are visible.
- [ ] **P3 — Open the assembled dissertation.** Confirm that the revised Chapter 2 appears between Chapters 1 and 3.
- [ ] **P4 — Read the supervisor feedback again.** Confirm that the two B-profile areas were `Aims and Requirements` and `Key Literature and Background Reading`.
- [ ] **P5 — Prepare a correction log.** For every problem, record the file, section, original text, proposed correction, and recheck result.
- [ ] **P6 — Do not edit experimental quantities during this check.** This audit concerns literature, argument, and citation format.

## 3. First-pass human reading

- [ ] **R1 — Read continuously without editing.** Chapter 2 should explain why the project needs state summarisation, verification, tracing, and process-level evaluation.
- [ ] **R2 — Check the opening scope.** It must say that the chapter is a focused narrative review and must not claim to be a systematic review.
- [ ] **R3 — Check the chapter flow.** The order from interactive agents to state representation, planning, games, verification, provenance, evaluation, and research gap should feel logical.
- [ ] **R4 — Check RQ1 support.** Partial observability and structured state representation must provide a clear foundation for state summarisation.
- [ ] **R5 — Check RQ2 support.** SayCan, admissible-action mapping, planning limitations, and shielding must lead clearly to verification and fallback.
- [ ] **R6 — Check RQ3 support.** AgentBench, AgentBoard, explanation limits, and replay inspection must lead clearly to trajectory-level evaluation.
- [ ] **R7 — Check terminology.** `proposal`, `verification`, `normalization`, `fallback`, `provenance`, `trace`, and `executed action` must not be used interchangeably.
- [ ] **R8 — Check repetition.** Remove repeated claims unless the later occurrence adds comparison, limitation, or synthesis.
- [ ] **R9 — Check paragraph purpose.** Every paragraph should introduce evidence, compare evidence, state a limitation, or connect literature to the project.
- [ ] **R10 — Check transitions.** Each major section should explain why the next literature theme is required.

## 4. Critical-analysis checks

- [ ] **A1 — Positive and negative evidence are balanced.** The chapter should not imply that LLM planning is generally reliable.
- [ ] **A2 — ReAct is not claimed as an implementation.** It is a related proposal/action architecture, not the method implemented by this project.
- [ ] **A3 — SayCan is used as an analogy, not equivalence.** Robot affordance grounding must not be described as identical to Lux verification.
- [ ] **A4 — Shielding boundary is explicit.** LuxLLM-Agent must not claim formal temporal-logic safety or a formally synthesised shield.
- [ ] **A5 — Rationale boundary is explicit.** A model-provided reason is a recorded proposal field, not proof of faithful internal reasoning.
- [ ] **A6 — Outcome attribution is limited.** Win rate must not be attributed only to the LLM because rules, caching, verification, and planning also contribute.
- [ ] **A7 — Dual-LLM scope remains supplementary.** The literature section must not turn the dissertation into a Qwen-versus-DeepSeek ranking study.
- [ ] **A8 — Research gap is bounded.** Use wording such as “within this focused review”; do not claim that no similar system exists anywhere.
- [ ] **A9 — Contribution is precise.** The contribution is an integrated trace-and-verification artefact and evaluation framework, not a new foundation model.
- [ ] **A10 — Comparison table is fair.** Every limitation in Section 2.11 must describe scope differences without dismissing the cited work.

## 5. In-text citation and reference correspondence

- [ ] **C1 — Ahn et al. (2022)** appears in `references.md`.
- [ ] **C2 — Alshiekh et al. (2018)** appears in `references.md`.
- [ ] **C3 — Berner et al. (2019)** appears in `references.md`.
- [ ] **C4 — Browne et al. (2012)** appears in `references.md`.
- [ ] **C5 — Huang et al. (2022)** appears in `references.md`.
- [ ] **C6 — Kaelbling et al. (1998)** appears in `references.md`.
- [ ] **C7 — Li et al. (2023)** appears in `references.md`.
- [ ] **C8 — Liu et al. (2024)** appears in `references.md`.
- [ ] **C9 — Lux AI Challenge (2024)** appears in `references.md`.
- [ ] **C10 — Ma et al. (2024)** appears in `references.md`.
- [ ] **C11 — Mnih et al. (2015)** appears in `references.md`.
- [ ] **C12 — Park et al. (2023)** appears in `references.md`.
- [ ] **C13 — Schick et al. (2023)** appears in `references.md`.
- [ ] **C14 — Shinn et al. (2023)** appears in `references.md`.
- [ ] **C15 — Tao et al. (2024)** appears in `references.md`.
- [ ] **C16 — Turpin et al. (2023)** appears in `references.md`.
- [ ] **C17 — Valmeekam et al. (2023)** appears in `references.md`.
- [ ] **C18 — Vinyals et al. (2019)** appears in `references.md`.
- [ ] **C19 — Wang et al. (2023)** appears in `references.md`.
- [ ] **C20 — Yao et al. (2023a)** refers only to ReAct.
- [ ] **C21 — Yao et al. (2023b)** refers only to Tree of Thoughts.
- [ ] **C22 — Every author-year citation in Chapter 2 has one matching reference entry.**
- [ ] **C23 — Every Chapter 2 reference entry is cited where its claim is discussed.**
- [ ] **C24 — References used only in other chapters are not incorrectly deleted as “unused in Chapter 2.”**

## 6. Source-quality and claim verification

Open each link and check the title, authors, year, venue, and whether the cited claim is supported.

| Check | Source | Link |
| --- | --- | --- |
| [ ] S1 | SayCan | https://arxiv.org/abs/2204.01691 |
| [ ] S2 | Safe Reinforcement Learning via Shielding | https://doi.org/10.1609/aaai.v32i1.11797 |
| [ ] S3 | Language Models as Zero-Shot Planners | https://proceedings.mlr.press/v162/huang22a.html |
| [ ] S4 | POMDP foundation | https://doi.org/10.1016/S0004-3702(98)00023-X |
| [ ] S5 | AgentBench | https://proceedings.iclr.cc/paper_files/paper/2024/hash/e9df36b21ff4ee211a8b71ee8b7e9f57-Abstract-Conference.html |
| [ ] S6 | AgentBoard | https://doi.org/10.52202/079017-2365 |
| [ ] S7 | LLM planning limitations | https://doi.org/10.52202/075280-3320 |
| [ ] S8 | Unfaithful CoT explanations | https://doi.org/10.52202/075280-3275 |
| [ ] S9 | ReAct | https://openreview.net/forum?id=WE_vluYUL-X |
| [ ] S10 | Reflexion | https://doi.org/10.52202/075280-0377 |
| [ ] S11 | Toolformer | https://proceedings.neurips.cc/paper_files/paper/2023/hash/d842425e4bf79ba039352da0f658a906-Abstract-Conference.html |
| [ ] S12 | Tree of Thoughts | https://proceedings.neurips.cc/paper_files/paper/2023/hash/271db9922b8d1f4dd7aaef84ed5ac703-Abstract-Conference.html |
| [ ] S13 | Lux AI Season 3 paper | https://openreview.net/forum?id=7t8kWYbOcj |
| [ ] S14 | Official Lux-Design-S3 repository | https://github.com/Lux-AI-Challenge/Lux-Design-S3 |

Additional checks:

- [ ] **S15 — Prefer the published venue page.** Use arXiv only where no more suitable published version is recorded.
- [ ] **S16 — Do not cite search-result pages, blogs, Wikipedia, or secondary summaries for central technical claims.**
- [ ] **S17 — Model reports are treated as model documentation.** They are not used as independent proof that one backend is superior.
- [ ] **S18 — Official Lux sources support environment facts.** Project-specific observations are supported by this project's evidence instead.

## 7. Reference-format checks

Until the School confirms a required style, the current list should remain internally consistent in an APA-like author–date format.

- [ ] **F1 — Alphabetical order.** Entries are ordered by the first author or organisation.
- [ ] **F2 — Author spelling.** Check accents and apostrophes, including `Dębiak`, `Könighofer`, `Dessì`, and `O'Brien`.
- [ ] **F3 — Year format.** Every entry has one publication year in parentheses.
- [ ] **F4 — Title capitalisation.** Paper titles use consistent sentence case.
- [ ] **F5 — Venue formatting.** Journal, conference, and proceedings names are italicised consistently.
- [ ] **F6 — Volume and issue format.** Journal volume/issue information is included where available.
- [ ] **F7 — Page ranges.** Use an en dash, for example `99–134`, rather than a hyphen.
- [ ] **F8 — DOI preference.** Use DOI links where available and stable venue links otherwise.
- [ ] **F9 — URL cleanliness.** No tracking parameters or search-result URLs remain.
- [ ] **F10 — Organisation authors.** `Lux AI Challenge` and `Ollama` are formatted consistently.
- [ ] **F11 — `et al.` use.** The shortened author lists follow one rule consistently.
- [ ] **F12 — Year suffixes.** ReAct is `2023a` and Tree of Thoughts is `2023b` in both text and references.
- [ ] **F13 — Markdown rendering.** Italics, tables, inline code, and links display normally.
- [ ] **F14 — Final template conversion.** When the official dissertation style is known, convert all entries once rather than mixing styles manually.

## 8. Full-dissertation consistency

- [ ] **D1 — Chapter 1 claims match Chapter 2.** The contribution and research gap use compatible language.
- [ ] **D2 — Chapter 3 methods are motivated by Chapter 2.** State summarisation, verification, fallback, and replay linkage have literature foundations.
- [ ] **D3 — Chapter 6 does not overclaim.** Empirical intervention evidence is not described as formal safety proof.
- [ ] **D4 — Chapter 7 answers the same RQs.** Its conclusions respect the limitations established in Chapter 2.
- [ ] **D5 — The complete reference list appears once.** It must follow Chapter 7 in the assembled draft.
- [ ] **D6 — No obsolete Chapter 2 remains.** Search the assembled draft for the new heading `Introduction and Review Scope`.
- [ ] **D7 — Reassemble after any edit.** Run `python tools\assemble_dissertation.py`.
- [ ] **D8 — Revalidate after reassembly.** Run `python tools\validate_project_evidence.py`.

## 9. Stop criteria

The literature weakness can be considered closed when all of the following are true:

- [ ] **G1 — All mandatory reading, critical-analysis, correspondence, source, and formatting checks pass.**
- [ ] **G2 — Every failed item has a recorded correction and a completed recheck.**
- [ ] **G3 — No broken citation, unsupported central claim, or unreadable character remains.**
- [ ] **G4 — The chapter makes a clear, bounded research-gap argument.**
- [ ] **G5 — The final citation style has either been confirmed by the School or explicitly marked as awaiting confirmation.**
- [ ] **G6 — The assembled dissertation and project-evidence validation both pass.**

Final decision:

```text
Status: READY FOR SUPERVISOR REVIEW / REQUIRES REVISION
Unresolved items:
Checked by:
Date:
```
