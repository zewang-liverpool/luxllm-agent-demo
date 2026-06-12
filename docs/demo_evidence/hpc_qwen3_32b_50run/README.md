# Qwen3-32B 50-run Evidence

This folder contains the controlled-run evidence for the Lux AI Season 3 LLM-assisted agent evaluation.

## Experiment

- Environment: Lux AI Season 3
- Agent: Lux LLM Agent
- Main LLM model: qwen3:32b
- Run type: controlled multi-run evaluation
- Number of runs: 50
- Demo-selected run: Run008
- Viewer mode: isometric visualization
- Demo video: uploaded separately as a GitHub Release asset

## Contents

- Top-level summary files: aggregated evidence, execution summaries, and match-level records copied from the HPC 50-run folder.
- `decision_logs/decision_log_008.jsonl`: step-level decision trace for the selected demo run.
- `llm_decisions/`: selected LLM decision evidence for Run008, if available.
- `selected_demo_run/`: replay/reference artifacts for the final recorded demo run, if available.

## Purpose

These files support the EMNLP demo-style claims by documenting:

1. controlled multi-run evaluation,
2. LLM-assisted decision traces,
3. fallback and rule-arbitration behavior,
4. reproducible evidence for the selected isometric visualization demo.

## Demo video

The final Run008 isometric visualization video is not committed directly to the repository because the MP4 file is larger than the normal GitHub repository file-size limit. It should be uploaded as a GitHub Release asset and linked from this document after the release is published.
