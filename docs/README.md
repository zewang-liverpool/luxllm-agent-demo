# LuxLLM-Agent Documentation Map

This page is the entry point for the tracked project documentation. Files with
dates in their names may preserve an earlier project state; use the current
sources below before consulting historical material.

## Start here

1. [Project overview](../README.md) — current research question, method,
   headline results, architecture, and quick start.
2. [Current research scope](research_scope_20260814.md) — canonical title,
   research question, three objectives, and terminology boundary.
3. [Project closeout standard](project_closeout_standard.md) — completed
   technical stopping criteria and the rule for reopening development.
4. [Developer handoff](developer_handoff_20260814.md) — operational handoff
   from the canonical `main` branch.

## Reproduction and experiments

- [Reproducibility guide](reproducibility_guide.md) — Windows/Linux setup,
  tests, smoke runs, Viewer reproduction, Ollama preflight, and Barkla2 runs.
- [Direct Prompt versus DTAV protocol](direct_prompt_dtav_experiment_guide.md)
  — primary controlled method comparison.
- [Dual-LLM experiment guide](dual_llm_experiment_guide.md) — supplementary
  Qwen-versus-DeepSeek protocol.
- [Primary method-comparison report](../reports/direct_prompt_vs_dtav_trace_analysis.md)
  — validated Direct Prompt–DTAV process and inspection evidence.
- [Primary matched outcome comparison](../reports/direct_prompt_vs_dtav_comparison.json)
  — machine-readable paired outcome statistics.
- [Earlier model-versus-rule evidence](../reports/final_trace_evaluation.md) —
  supporting evidence retained with a scope note.
- [Supplementary dual-LLM evidence](../reports/dual_llm_trace_evaluation.md) —
  concurrent two-LLM tracing and verification evidence.

Large raw Barkla archives, local recordings, and generated per-run directories
are intentionally excluded from Git. Compact reports and provenance records
under `reports/` are the reviewable repository evidence.

## Architecture and implementation

- [System architecture](technical/system_architecture.md)
- [LLM decision pipeline](technical/llm_decision_pipeline.md)
- [Action verification and fallback](technical/action_verification_and_fallback.md)
- [Decision-trace overlay](technical/decision_trace_overlay.md)
- [Evaluation metrics](technical/evaluation_metrics.md)
- Canonical runtime source: [`../src/agent/`](../src/agent/)
- Runnable and setup entry points: [`../scripts/`](../scripts/)
- Analysis and validation tools: [`../tools/`](../tools/)
- Automated tests: [`../tests/`](../tests/)

## Viewer

- [Current Viewer](viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html)
  — player-first replay interface with the project-specific DTAV Inspector.
- Replay frames: [`../data/isometric_replay_frames.json`](../data/isometric_replay_frames.json)
- Replay-linked trace overlay: [`../data/run008_decision_trace_overlay.json`](../data/run008_decision_trace_overlay.json)

Run `python -m http.server 8000` from the repository root, then open:

```text
http://localhost:8000/docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html
```

The top-level `viewer/` directory contains the legacy June prototype and is not
the recording or evaluation Viewer.

## CA2

- [CA2 preparation pack](ca2/README.md)
- Final editable deck: `ca2/LuxLLM_Agent_CA2_Presentation_20260818.pptx`
- Full content manuscript: `ca2/LuxLLM_Agent_CA2_PPT_Content_Manuscript_20260818.docx`
- Narration: [CA2 narration script](ca2/CA2_NARRATION_SCRIPT.md)
- Q&A: [CA2 Q&A preparation](ca2/CA2_QA_PREPARATION.md)
- Automated status: [CA2 readiness report](ca2/CA2_AUTOMATED_READINESS.md)

## Dissertation

- [Dissertation draft index](dissertation/dissertation_draft_index.md)
- [Full assembled draft](dissertation/full_dissertation_draft.md)
- [Background and related work](dissertation/chapter_2_background_related_work.md)
- [Evaluation](dissertation/chapter_6_evaluation.md)
- [Discussion and conclusion](dissertation/chapter_7_discussion_conclusion.md)
- [References](dissertation/references.md)

The dissertation chapters and index use the current Direct Prompt–DTAV research
question. Submission formatting, official front matter, citation checks, and
final human proofreading remain manual tasks.

## Historical and dated material

The following material is retained for provenance and should not override the
current scope or status:

- `paper/` — earlier EMNLP-format artifact; not an active submission plan.
- `dissertation/project_freeze_checklist.md` — earlier freeze checklist.
- `supervisor_project_report_20260716.md` — July supervisor-facing snapshot.
- historical sections inside the root README — explicitly marked superseded.
- dated evidence reports that carry a scope note at the top.

When two documents disagree, use this order of authority:

1. root `README.md` and `research_scope_20260814.md`;
2. `project_closeout_standard.md` and current compact reports;
3. dissertation draft index and current chapters;
4. dated or historical snapshots.
