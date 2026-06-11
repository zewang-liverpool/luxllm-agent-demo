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

This project has reached the controlled-evaluation stage for the Lux AI Season 3 LLM-assisted agent. The current stable research configuration uses `qwen3:32b` with GPU-backed Ollama inference on Barkla2, combined with rule-based fallback, structured LLM planning, decision tracing, and replay-grounded inspection.

The current main controlled result is the **target-aware qwen3:32b strategic planner**. This configuration extends the earlier basic intent-only JSON planner by adding target coordinates, priority scores, risk labels, expected-value estimates, and lightweight rule-based arbitration.

| Configuration | Matches | LLM-Assisted Wins | Rule Opponent Wins | Win Rate | Strategy Use | Fallback Rate | LLM Errors | Main Observation |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Basic qwen3 planner | 50 | 28 | 22 | 56% | 92.7% | 7.3% | 0 | Previous basic JSON planner |
| Target-aware qwen3 strategic planner | 50 | 35 | 15 | 70% | 96.0% | 4.0% | 0 | Current main controlled result |
| Strategy-diverse prompting | 50 | 29 | 21 | 58% | — | — | 0.0 avg. | Earlier controlled configuration |
| Candidate-exploitation ablation | 50 | 26 | 24 | 52% | — | — | 0.0 avg. | Stable ablation, but not an improvement |

The target-aware qwen3:32b strategic planner is now the main reported controlled result. In a 50-match controlled comparison, it improved the LLM-assisted player's descriptive win rate from 56% to 70% compared with the previous basic qwen3 planner, reduced fallback rate from 7.3% to 4.0%, and maintained zero LLM errors.

The earlier strategy-diverse prompting and candidate-exploitation configurations are retained as development evidence and ablation context. They show that the evaluation pipeline can compare design variants, but they should not be presented as the final main result.

### Evidence Files

- `docs/evidence/qwen3_gpu_evidence_index.md`
  - Consolidated qwen3:32b GPU evidence index.
  - Includes earlier strategy-diverse and candidate-exploitation runs.
  - Identifies the target-aware qwen3 strategic planner as the current main controlled result.

- `docs/closeout_summary_qwen3_p55_light.md`
  - Closeout summary for the latest 50-match target-aware qwen3:32b strategic-planner run.
  - Records the 35/50 main result and reliability metrics.

- `docs/reviewer_response_qwen3_update.md`
  - Response notes for reviewer or supervisor concerns.
  - Explains how the project moved beyond small-model limitations.
  - Clarifies that the contribution is a structured LLM-agent runtime and replay-grounded evaluation system.

### Final Project Positioning

This project is not presented as a state-of-the-art Lux AI competition bot or a competition-winning policy. It is presented as an inspectable LLM-assisted game-agent system for Lux AI Season 3.

The main contribution is the integration of:

1. structured LLM strategic planning;
2. schema validation;
3. rule-based arbitration;
4. fallback-safe execution;
5. cached strategy reuse;
6. decision-source logging;
7. replay-grounded inspection;
8. controlled qwen3:32b evaluation.

The strongest empirical claim is that, in controlled 50-match experiments, a target-aware qwen3:32b strategic planner achieved a higher descriptive win rate and lower fallback rate than the previous basic qwen3 planner, while maintaining zero LLM errors.
