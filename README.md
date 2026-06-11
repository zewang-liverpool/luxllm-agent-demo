# EMNLP 2026 — System Demonstrations Track (Overleaf project)

Ready-to-upload LaTeX project using the **official ACL style files**, set up
for the EMNLP 2026 **System Demonstrations** track (single-blind review).

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
- [ ] Paper PDF, <= 6 pages, ACL style.
- [ ] **Evaluation reported** (quantitative / user study / human eval) —
      papers with no evaluation may be desk rejected. See Section "Evaluation".
- [ ] **Live demo URL or installable package link** — strict requirement;
      missing link => desk reject (exceptions only for special-hardware cases,
      which must be justified in the paper).
- [ ] **Screencast video**, <= 2.5 min (YouTube/similar link in the paper, or
      MPEG-4 as supplementary material).
- [ ] Licensing stated (Section "Licensing and Availability").
- [ ] Ethics statement conforming to the ACM Code of Ethics.

## Important dates
- Paper submission: **Friday, 10 July 2026** (AoE, UTC-12)
- Notification: 20 August 2026
- Camera-ready: 30 August 2026
- Conference: 24-29 October 2026, Budapest, Hungary
- Note: **no rebuttal stage**. Submission via OpenReview (link posted ~2 weeks
  before the deadline).

---

## Current Experimental Status

This project has reached the controlled-evaluation stage for the Lux AI Season 3 LLM-assisted agent. The current stable research configuration uses `qwen3:32b` with GPU-backed Ollama inference on Barkla2, combined with rule fallback, strategy caching, decision tracing, and replay-grounded inspection.

The main reported configuration is **E4 strategy-diversity**, which achieved the strongest 50-match controlled result among the stable qwen3:32b variants:

| Configuration | Matches | Player 0 Wins | Player 1 Wins | Avg. LLM Errors | Avg. Trace Steps | Main Observation |
|---|---:|---:|---:|---:|---:|---|
| E4 strategy-diversity | 50 | 29 | 21 | 0.0 | 1010.0 | Main reported result |
| E5.2 candidate-exploitation | 50 | 26 | 24 | 0.0 | 1010.0 | Stable ablation, but did not outperform E4 |

The E5.2 candidate-exploitation variant remained technically stable, with zero LLM errors, complete trace coverage, and consistent cached decision reuse. However, it did not improve the 50-match win rate over E4. Therefore, E4 is used as the main paper configuration, while E5.2 is retained as an ablation showing that additional candidate-target exploitation does not necessarily improve long-horizon performance.

### Evidence Directories

- `docs/hpc_qwen3_gpu_e4_50run/20260610_180133_qwen3_32b_gpu_e4_50run_job8994080/`
  - Main 50-match controlled evaluation.
  - `player_0 = 29`, `player_1 = 21`.
  - `avg_llm_errors = 0.0`.
  - `avg_trace_steps = 1010.0`.

- `docs/hpc_qwen3_gpu_e52_50run/20260610_221857_qwen3_32b_gpu_e52_50run_job8997743/`
  - Candidate-exploitation ablation.
  - `player_0 = 26`, `player_1 = 24`.
  - `avg_llm_errors = 0.0`.
  - `avg_trace_steps = 1010.0`.

### Final Project Positioning

This project is not presented as a competition-winning Lux AI policy. Instead, it is presented as an inspectable LLM-assisted game-agent system that combines:

1. structured LLM decision generation;
2. safe rule-based fallback;
3. strategy caching for long-horizon consistency;
4. replay-grounded decision tracing;
5. controlled evaluation across multiple agent variants.

The paper should report E4 as the main controlled configuration and E5.2 as a supplementary ablation.
