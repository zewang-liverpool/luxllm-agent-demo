# EMNLP 2026 — System Demonstrations Track (Overleaf project)

> **Historical artifact:** this directory preserves an earlier paper-format
> snapshot for provenance. It is not the canonical description of the current
> MSc project and is not an active submission plan. Use the repository
> `README.md`, `docs/research_scope_20260814.md`, and the dissertation materials
> for the current research question, terminology, results, and submission work.

Ready-to-upload LaTeX project using the **official ACL style files**, set up
for the EMNLP 2026 **System Demonstrations** track (single-blind review).

## Frozen artifact

- Repository: <https://github.com/zewang-liverpool/luxllm-agent-demo>
- Local viewer: run `python -m http.server 8000` from the repository root, then open `docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html`.
- Full match re-execution requires the compatible Lux AI Season 3, Ollama, model, and local or Slurm runtime configuration; the tracked Run008 viewer does not require model inference.

## Upload to Overleaf
1. Zip this folder (or use the provided `emnlp2026-demo.zip`).
2. In Overleaf: **New Project -> Upload Project** and select the zip.
3. Set the main document to `main.tex`, compiler **pdfLaTeX**.

## Files
- `main.tex` — the paper (structured to address all demo-track questions).
- `acl.sty`, `acl_natbib.bst` — official ACL style files (do **not** modify).
- `custom.bib` — citations not in the ACL Anthology.
- `anthology.bib` — ACL Anthology entries (replace with the full file from
  the ACL Anthology if you cite many Anthology papers).

## Key rules baked into the template
- **6 pages** of content max (hard limit; longer => desk reject).
- **Unlimited** references and **unlimited** optional ethics/broader-impact
  statement; appendix capped at **2 pages**.
- **Single-blind**: show real author names and affiliations (the template uses
  the non-anonymous `preprint` option, which also adds page numbers for
  reviewers). Switch to `[final]` for camera-ready; never use `[review]`
  (that anonymises).
- Accepted papers get **1 extra content page** for the camera-ready.

## Submission checklist (all enforced this year)
- [x] Six pages of main content in ACL style; references, ethics, and appendix currently occupy page 7.
- [x] **Evaluation reported** (quantitative / user study / human eval) —
      papers with no evaluation may be desk rejected. See Section "Evaluation".
- [x] **Installable artifact link** — the frozen GitHub repository and local viewer instructions are included in the paper.
- [x] Replace the placeholder author names, affiliations, and email addresses.
- [ ] **Live demo URL**, if required separately from the installable artifact link.
      missing link => desk reject (exceptions only for special-hardware cases,
      which must be justified in the paper).
- [x] **Screencast video**, 75-second MPEG-4 prepared as supplementary material and intentionally excluded from Git history.
- [x] Licensing and availability stated in the corresponding paper section.
- [x] Ethics statement included.
- [ ] Recheck the final page-count interpretation and all requirements against the official call immediately before submission.

Local supplementary video:

```text
docs/demo_videos/LuxLLM_Agent_Final_Demo_Run008_Isometric_Visualization.mp4
```

## Important dates
- Paper submission: **Friday, 10 July 2026** (AoE, UTC-12)
- Notification: 20 August 2026
- Camera-ready: 30 August 2026
- Conference: 24-29 October 2026, Budapest, Hungary
- Note: **no rebuttal stage**. Submission via OpenReview (link posted ~2 weeks
  before the deadline).
