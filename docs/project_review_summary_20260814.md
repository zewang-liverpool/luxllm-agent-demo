# LuxLLM-Agent: Current Project Status and Improvement Summary

**Originally prepared for academic review:** 14 August 2026

**Final status update:** 18 August 2026

**Student:** Ze Wang (201868809), University of Liverpool

**Supervisor:** Dr Meng Fang

**Repository:** <https://github.com/zewang-liverpool/luxllm-agent-demo>

**Canonical branch:** `main`

## 1. Project focus

**Title:** *LuxLLM-Agent: A Decision-Trace and Action-Verification Method for LLM Decision-Making in Lux AI Season 3*

**Research question:**

> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent, long-horizon, and rule-constrained strategy game such as Lux AI Season 3, and how can the project-specific Decision-Trace and Action-Verification (DTAV) method address the observed limitations?

The project is not intended to establish a general leaderboard for language models. Lux AI Season 3 is an adversarial multi-agent strategy game with incomplete observations, multiple controlled units, long-horizon state, and strict action rules. The study first asks whether direct prompting can handle these properties, then evaluates the project-specific DTAV method.

The three current research objectives are:

1. Establish a controlled direct-prompting baseline with matched seeds, role swapping, and the same model settings.
2. Implement DTAV so LLM proposals can be normalised, reused, checked, filtered, or replaced before legal environment actions are constructed.
3. Compare direct prompting and DTAV using action validity, fallback/intervention rates, reliability, latency, game outcomes, and replay-linked inspection.

DTAV is the name of this project's method, not an established field term. Its trace is a predefined audit record and must not be described as access to hidden model reasoning.

## 2. Current completion status

The working baseline, earlier formal studies, evidence analysis, reproducibility hardening, and the bounded direct-prompt-versus-DTAV comparison requested on 14 August are complete. The two method conditions each completed 100 matches over the same 50 role-swapped seeds and passed the repository validators. The remaining work is CA2 recording/Q&A and final human checking rather than further expansion of the core system.

The repository currently contains:

- a working Lux AI Season 3 hybrid-agent pipeline;
- structured decision, verification, fallback, risk, latency, score, and replay-link traces;
- a rule-based execution boundary that prevents free-form model text from directly controlling Lux;
- local and Barkla-compatible experiment scripts for single-LLM and direct dual-LLM evaluation;
- matched-seed, role-swapped evaluation and uncertainty estimates;
- automated unit, consistency, smoke, and evidence-validation checks;
- a player-first replay Viewer with the project-specific DTAV Inspector;
- dissertation drafts, evidence reports, reproducibility guidance, and CA2 preparation materials.

## 3. Earlier weaknesses and how they were addressed

| Earlier issue | Improvement made | Current evidence/status |
|---|---|---|
| Research aims were too numerous and the project focus was broad | Consolidated the work around one research question, one overall goal, and three research objectives | Dissertation introduction, methodology, evaluation, and conclusion now use the same scope |
| Literature/background section was underdeveloped | Reorganised the review around LLM agents, structured outputs, tool/action verification, game-agent evaluation, observability, and reproducibility; strengthened the citation plan and manual reference checklist | `docs/dissertation/chapter_2_background_related_work.md` and associated reference/checking documents |
| Complete runtime environment was difficult to reproduce | Added dependency files, setup instructions, environment documentation, locked Windows dependencies, and Barkla execution guidance | `requirements*.txt`, `environment.yml`, `scripts/setup.*`, and `docs/reproducibility_guide.md` |
| GitHub originally contained an incomplete runnable snapshot | Added the missing agent modules, experiment runners, analysis tools, reports, tests, and operational documentation | Repository now contains the executable and analysis paths used for the retained evidence |
| No simple reproduction entry point | Added setup, smoke-test, mock-LLM, single-LLM, dual-LLM, and result-validation entry points | Scripts are documented and covered by automated checks |
| No automated test or CI coverage | Added unit tests, project-consistency checks, evidence validation, Viewer assertions, and GitHub Actions | 35 tests pass; smoke test and evidence validator pass on 18 August 2026 |
| Random seed and player-role bias were insufficiently controlled | Used 50 matched environment seeds with role swapping in each formal study | 100 matches per study, with paired/clustered analyses and role-specific summaries |
| Statistical reliability was weak | Added Wilson intervals, exact binomial/sign/McNemar tests, paired and seed-clustered bootstrap intervals | Statistics are generated by tested analysis code and retained in machine-readable reports |
| Experimental evidence was too limited | Completed two 100-match model-versus-rule studies and one 100-match direct model-versus-model study | 300/300 formal matches completed |
| Validity could be overstated by counting only final parsed outputs | Separated raw-schema validity, deterministic normalisation, and post-check validity | 1,091 normalisation interventions are explicitly recorded rather than hidden |
| Rule-based verification was described but not quantified | Added offline verifier audits for target changes and their reasons | 28,401 risk-filter changed steps and 151,312 changed targets are recorded across all studies |
| Win/loss alone did not explain behaviour | Added per-step provenance, verification, fallback, latency, score context, and replay linkage | 312,908 structured trace records with complete trace and replay-link coverage |
| The direct LLM-versus-LLM question from the supervisor was unanswered | Added a supplementary Qwen3-32B versus DeepSeek-R1-32B experiment using matched seeds and role swaps | 100 matches; 4,676/4,676 calls valid after checks; complete two-sided traces |
| Direct prompting had not been isolated from the project method | Added explicit `direct_prompt` and `dtav` conditions, method-labelled logs, matched-role runners, validation, and local mock acceptance runs | Both formal conditions completed 100/100 matches from the same source commit and passed validation |
| The earlier Viewer was visually crowded and could misreport replay score/context | Reworked layout reservation, player-first and Inspection views, inspector reopening, current replay score, stage labels, status explanations, and automated Viewer checks | Current Viewer separates proposal, deterministic checks, and executed state while preserving map visibility |
| Claims were sometimes stronger than the evidence | Revised the dissertation and reports to distinguish operational provenance from causal reasoning and to treat win rate as secondary | Reports explicitly avoid general model-ranking and universal-safety claims |
| Large local experiment archives made file management unclear | Kept large raw archives and recordings outside Git tracking, retained checksums/provenance, and committed compact analysis outputs | GitHub remains reviewable while formal evidence can be traced to archived raw runs |

## 4. Formal empirical evidence

### Primary studies: LLM-assisted agent versus the same rule opponent

| Backend | Matches | LLM wins | Win rate | Seed-clustered 95% interval | Seed-level exact p-value |
|---|---:|---:|---:|---:|---:|
| Qwen3-32B | 100 | 63 | 63% | [57%, 70%] | 0.00098 |
| DeepSeek-R1-32B | 100 | 60 | 60% | [51%, 69%] | 0.05248 |

Across these 200 matches, the framework retained 206,591 structured trace records and 4,591/4,591 post-check-valid fresh LLM calls. Qwen required 520 deterministic normalisations; DeepSeek required none. The risk filter changed proposed targets on 5,590 Qwen steps and 7,090 DeepSeek steps.

### Supplementary direct dual-LLM study

- Qwen3-32B versus DeepSeek-R1-32B: 100 matches over 50 role-swapped seed pairs.
- Outcome: 54 wins to 46; seed-level exact sign p-value `0.5034`.
- Fresh calls valid after recorded checks: 4,676/4,676.
- Complete structured trace records: 106,317.
- Deterministic normalisations: 571.
- Risk-filter changed steps: 15,721.

The 54:46 outcome is not statistically distinguishable from parity and is not used to claim that Qwen is generally superior. The study instead shows that the framework can trace and verify both LLM-assisted players concurrently.

### Supporting framework evidence from the earlier model studies

- 300/300 completed formal matches.
- 9,267/9,267 fresh LLM calls valid after recorded checks.
- 312,908 structured trace records.
- 1,091 deterministic normalisation interventions.
- 28,401 risk-filter changed steps.
- 100% action-array shape validity in the retained formal runs.
- No recorded LLM timeout, API error, or downstream action fallback in those formal runs.

### Final direct-prompt versus DTAV study

- Direct prompting: 48 wins in 100 completed matches.
- DTAV: 63 wins in 100 completed matches.
- Matched seed-role strata: 100.
- Direct-prompt-only wins: 6; DTAV-only wins: 21.
- McNemar exact `p = 0.0059`.
- Estimated DTAV advantage: 15 percentage points; paired-bootstrap 95% interval 6 to 25 percentage points.
- Post-check structured-call validity: 86.1% for direct prompting and 99.9% for DTAV.
- Observable rule-fallback steps: 95.5% for direct prompting and 5.6% for DTAV.
- Trace completeness, replay linkage, and action-array shape validity: 100% in both conditions.

This comparison evaluates DTAV as a complete method bundle under the recorded Qwen3-32B, prompt, seed, role, software, and hardware configuration. It does not establish that every individual DTAV component caused the observed outcome difference.

## 5. Reproducibility and verification status

Local validation repeated on 18 August 2026:

```text
pytest: 35 passed
smoke test: passed
project evidence validator: passed
final CA2 PowerPoint: seven slides; content, template, and overflow checks passed
```

The formal GPU experiments were run on the University of Liverpool Barkla cluster with retained job identifiers, model/version metadata, matched seed ranges, environment information, result summaries, logs, and local SHA-256-checked archives. The direct-prompt and DTAV jobs used the same source commit, model configuration, 50 matched seeds, and role-swap protocol. No additional GPU experiment is required unless validation exposes a defect or the supervisor identifies a specific evidence gap.

## 6. Current Viewer and CA2 preparation

The Viewer now provides:

- separate Proposal Attempt, Rule Verification, and Executed State sections;
- replay-grounded score and frame context;
- explicit proposal acceptance/rejection, fallback, and risk-filter status;
- an optional Inspection View with stable map/control placement;
- a visible control for reopening the inspector after it is closed;
- aggregate-evidence separation so the qualitative Run008 replay is not presented as formal valid-call evidence.

The narration, detailed recording guide, interactive manual checklist, Q&A preparation, and final seven-slide PowerPoint under `docs/ca2/` use the current scope and the validated direct-prompt-versus-DTAV evidence.

## 7. Remaining limitations

1. The evaluation covers one game environment and two local 32-billion-parameter model backends; results are not universally generalisable.
2. Logged provenance and interventions are operational evidence, not a complete causal account of model reasoning.
3. A zero downstream action-fallback count in the retained formal runs does not prove safety for every possible future proposal.
4. Viewer inspection is qualitative evidence that complements, rather than replaces, quantitative evaluation.
5. Reproducing the full formal studies requires a suitable GPU allocation and local Ollama models; CPU-only smoke and mock checks remain available for routine validation.
6. The direct-prompt-versus-DTAV comparison covers one complete method bundle and one recorded model configuration; it does not isolate the causal effect of each DTAV component.

## 8. Defined stopping standard

Core development is considered sufficiently complete when:

- automated tests, smoke checks, and evidence validation pass;
- formal evidence is complete and internally consistent;
- the Viewer accurately distinguishes proposal, verification, and execution;
- reproducibility instructions and bounded limitations are documented;
- no assessor-identified factual defect remains.

The software, formal evidence, and local acceptance conditions are met. The same-commit formal direct-prompt-versus-DTAV comparison and its evidence integration are complete. Further model additions or repeated 50/100-run experiments are not required. The priority is now a clear CA2 demonstration, Q&A preparation, dissertation fact/citation/format checking, and final submission QA.

## 9. Recommended files for reviewers

- Project overview: `README.md`
- Architecture: `docs/technical/system_architecture.md`
- Reproducibility: `docs/reproducibility_guide.md`
- Primary framework evidence: `reports/final_trace_evaluation.md`
- Primary method comparison: `reports/direct_prompt_vs_dtav_trace_analysis.md`
- Direct dual-LLM evidence: `reports/dual_llm_trace_evaluation.md`
- Verifier audits: `reports/verifier_intervention_audit.md` and `reports/dual_llm_verifier_audit.md`
- Current Viewer: `docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html`
- CA2 materials: `docs/ca2/`
- Dissertation draft index: `docs/dissertation/dissertation_draft_index.md`
