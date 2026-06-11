# Paper Assets Index

Version: `v0.9-K3-final-packaging`

Generated at: `2026-06-03T22:58:14`

## 1. Main Paper Draft

- `docs/paper_polished_draft_v09k2.md`
- `docs/paper_first_draft_v09k1.md`
- `docs/emnlp_demo_paper_draft.md`

## 2. Core Evidence Documents

- `docs/explainability_feature_summary.md`
- `docs/risk_aware_filter_effect_summary.md`
- `docs/risk_filter_event_summary.md`
- `docs/j3_risk_aware_agent_evidence.md`
- `docs/risk_filter_distance_diagnostics.md`
- `docs/local_utility_risk_filter_effect_summary.md`
- `docs/local_utility_risk_filter_evidence.md`
- `docs/final_consistency_check_v09j5.md`
- `docs/l1e_lightweight_consistency_check.md`
- `docs/reproducibility_guide.md`
- `docs/final_project_structure.md`

## 3. Core Evidence Logs

- `logs/viewer_frames.json`
- `logs/frame_log.jsonl`
- `logs/decision_log.jsonl`
- `logs/match_history.jsonl`
- `logs/risk_filter_distance_diagnostics.json`
- `logs/local_utility_risk_filter_effect_summary.json`
- `logs/l1d_paper_note_refresh_summary.json`
- `logs/l1e_lightweight_consistency_check.json`
- `logs/explainability_feature_summary.json`
- `logs/risk_aware_filter_effect_summary.json`
- `logs/risk_filter_event_summary.json`
- `logs/final_consistency_check_v09j5.json`
- `logs/paper_quality_review_v09k2.json`

## 4. Screenshots

- `docs/screenshots/v09b_step78_memory_overlay.png`
- `docs/screenshots/v09c_sensor_energy_overlay.png`

## 5. Viewer and Replay Assets

- `s3_log_driven_gameview.html`
- `logs/viewer_frames.json`
- `replays/lux_s3_llm_vs_rule_replay.html`

Latest replay files:

- `replays/lux_s3_llm_vs_rule_20260603_211251.html`
- `replays/lux_s3_llm_vs_rule_replay.html`
- `replays/lux_s3_llm_vs_rule_20260603_152343.html`
- `replays/lux_s3_llm_vs_rule_20260603_151643.html`
- `replays/lux_s3_llm_vs_rule_20260603_150625.html`

## 6. Recommended Figures for Paper

Suggested figures:

1. **System Architecture:** LLM intent layer, fallback policy, memory, action planner, viewer log pipeline.
2. **Inspectable GameView Screenshot:** final J6-C2 viewer with decision-trace dock and compact legend.
3. **Opponent Risk / Risk Filter Panel:** visible enemy risk and target rewrite event.
4. **Local Utility Effect Table:** far rewrite rate before and after L1-B.

## 7. Paper-Ready Key Claim

The final package supports the claim that LuxLLM-Agent is an inspectable LLM-assisted Lux AI Season 3 system with opponent-aware and local-utility-aware risk filtering and replay-grounded decision traceability. It does not claim state-of-the-art competition performance or full opponent modeling.

---

## qwen3:32b Controlled Evaluation Update

This section records the final qwen3:32b evidence used for the current EMNLP demo paper closeout.

### Main Controlled Result

- Configuration: E4 strategy-diversity
- Run directory: `docs/hpc_qwen3_gpu_e4_50run/20260610_180133_qwen3_32b_gpu_e4_50run_job8994080/`
- Summary file: `summary_50run.json`
- Match history: `match_history_50run.jsonl`
- Total runs: 50
- LLM-assisted player wins: 29
- Rule-controlled player wins: 21
- Avg LLM errors: 0.0
- Avg trace steps: 1010.0
- Avg LLM latency: 4778.339 ms

### Supplementary Ablation

- Configuration: E5.2 candidate-exploitation
- Run directory: `docs/hpc_qwen3_gpu_e52_50run/20260610_221857_qwen3_32b_gpu_e52_50run_job8997743/`
- Summary file: `summary_50run.json`
- Match history: `match_history_50run.jsonl`
- Total runs: 50
- LLM-assisted player wins: 26
- Rule-controlled player wins: 24
- Avg LLM errors: 0.0
- Avg trace steps: 1010.0
- Avg LLM latency: 4893.165 ms

### Paper and Response Files

- Main paper file: `main.tex`
- qwen3 evidence index: `docs/evidence/qwen3_gpu_evidence_index.md`
- Reviewer/supervisor response note: `docs/reviewer_response_qwen3_update.md`

### Paper Usage

- Use E4 strategy-diversity as the main controlled result.
- Use E5.2 candidate-exploitation as a supplementary ablation.
- Do not claim that E5.2 improves the agent.
- Frame the contribution as replay-grounded decision traceability and fallback-safe LLM-agent execution, not as state-of-the-art Lux AI performance.
