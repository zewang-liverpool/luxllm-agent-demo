# LuxLLM-Agent

**LuxLLM-Agent** is an interactive decision-trace and evaluation platform for inspecting LLM-based agents in **Lux AI Season 3**.

The project combines a Lux AI Season 3 agent, structured game-state summarisation, LLM-based strategic decision generation, rule-based action verification, fallback handling, decision provenance logging, controlled-run evaluation, and an isometric replay viewer.

The project is designed for an MSc dissertation and research-demo style artifact. Its main goal is not simply to build an agent that plays Lux AI, but to investigate how LLM-based game-agent decisions can be structured, verified, traced, and evaluated.

> **Project status:** `LuxLLM-Agent COMP702 Submission Freeze v1`. The core system, controlled experiments, decision-trace viewer, and dissertation drafts are complete. Current work is limited to supervisor feedback, citations, figures, tables, screenshots, formatting, and final submission preparation.

---

## Project Focus

This project investigates the following research question:

> **How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?**

The system is built around three sub-questions:

1. How can raw Lux AI Season 3 game states be transformed into compact structured inputs for LLM-based strategic decision making?
2. How can rule-based verification and fallback mechanisms reduce invalid or unstable LLM-generated actions?
3. How can replay-grounded decision traces help inspect the relationship between LLM reasoning, selected strategies, executed actions, and game outcomes?

---

## Demo Preview

<p align="center">
  <img src="assets/luxllm_agent_final_demo_run008.gif" alt="LuxLLM-Agent Season 3 Run008 demo" width="760">
</p>

<p align="center">
  <b>LuxLLM-Agent Season 3 Run008 isometric replay and evaluation demo.</b>
</p>

The tracked preview asset is `assets/luxllm_agent_final_demo_run008.gif`.

---

## System Overview

LuxLLM-Agent separates strategic reasoning from executable game actions.

```text
Lux AI Season 3 Observation
        |
        v
Structured State Summariser
        |
        v
LLM Strategist
        |
        v
Structured Output Parser
        |
        v
Rule-based Action Verifier
        |
        v
Action Planner
        |
        v
Lux AI Environment
        |
        v
Decision Logger + Replay Viewer + Evaluation Harness
```

The LLM does not directly execute arbitrary environment actions. Instead, it produces high-level strategic decisions, which are parsed, verified, repaired, cached, or rejected before being converted into legal Lux AI actions.

---

## Key Features

### LLM-assisted Lux AI Season 3 agent

* Supports LLM-based strategic planning.
* Uses `qwen3:32b` as the main LLM backend.
* Adds `deepseek-r1:32b` as a comparison LLM backend.
* Supports rule-only and LLM-enabled experimental settings.

### Structured game-state summarisation

* Converts raw Lux AI observations into compact state summaries.
* Reduces the burden on the LLM.
* Provides a structured interface between the game environment and the LLM strategist.

### Rule-based action verification

* Prevents direct execution of arbitrary LLM outputs.
* Checks action feasibility and safety.
* Supports fallback behaviour when LLM outputs are invalid, unstable, or low-confidence.

### Decision provenance logging

* Records whether decisions come from:

  * fresh LLM calls;
  * cached LLM decisions;
  * rule-based player logic;
  * fallback logic;
  * rule fallback.
* Supports later replay-grounded analysis.

### Isometric replay viewer

* Provides a Season 1-style visual replay interface for Lux AI Season 3.
* Displays replay state, battle timeline, score context, and final evaluation summary.
* Includes the completed LLM Decision Trace Overlay for replay-grounded inspection.

### Controlled-run evaluation

* Includes 50-run evidence for `qwen3:32b`.
* Includes 50-run comparison evidence for `deepseek-r1:32b`.
* Reports win/loss, LLM errors, latency, fallback behaviour, and decision-source distribution.

---

## Main Evaluation Results

### 50-run LLM backend comparison

| Model             | Runs | player_0 wins | player_1 wins | player_0 win rate | LLM errors | Notes                  |
| ----------------- | ---: | ------------: | ------------: | ----------------: | ---------: | ---------------------- |
| `qwen3:32b`       |   50 |            35 |            15 |               70% |          0 | Main LLM backend       |
| `deepseek-r1:32b` |   50 |            26 |            24 |               52% |          0 | Comparison LLM backend |

The model comparison is not intended as a general-purpose LLM leaderboard. Instead, it evaluates whether the LuxLLM-Agent decision-trace and rule-based action-verification framework can support different reasoning-oriented LLM backends under the same Lux AI Season 3 setting.

Both `qwen3:32b` and `deepseek-r1:32b` completed 50 controlled runs with zero LLM errors, showing that the framework can run different LLMs through the same structured decision pipeline.

---

## DeepSeek-R1-32B 50-run Results

The newly added DeepSeek-R1-32B experiment provides an additional model-level comparison.

| Metric                    |             Value |
| ------------------------- | ----------------: |
| Model                     | `deepseek-r1:32b` |
| Total runs                |                50 |
| player_0 wins             |                26 |
| player_1 wins             |                24 |
| player_0 win rate         |               52% |
| Average player_0 reward   |               2.7 |
| Average player_1 reward   |               2.3 |
| Average fresh LLM calls   |              33.2 |
| Average LLM strategy used |             27.24 |
| Average cached LLM turns  |            412.62 |
| Average fallback count    |            570.14 |
| Average LLM errors        |               0.0 |
| Average LLM latency       |       4143.595 ms |
| Maximum LLM latency       |      10581.076 ms |
| Average trace steps       |            1010.0 |

### DeepSeek decision-source distribution

| Decision source | Count |
| --------------- | ----: |
| `rule_player`   | 25250 |
| `fallback`      |    94 |
| `rule_fallback` |  3163 |
| `llm_fresh`     |  1362 |
| `cached_llm`    | 20631 |

Derived rates:

```text
Total decision-source events = 50500

LLM-related events:
llm_fresh + cached_llm = 1362 + 20631 = 21993
LLM decision-source rate ≈ 43.55%

Fallback-related events:
fallback + rule_fallback = 94 + 3163 = 3257
Fallback decision-source rate ≈ 6.45%
```

---

## Evidence

Main evidence files and directories:

```text
docs/demo_evidence_index.md
docs/demo_evidence/llm_model_comparison_summary.md
docs/demo_evidence/hpc_qwen3_32b_50run/
docs/demo_evidence/hpc_deepseek_r1_32b_50run/
docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html
data/isometric_replay_frames.json
data/run008_decision_trace_overlay.json
```

DeepSeek-R1-32B raw evidence directory:

```text
docs/demo_evidence/hpc_deepseek_r1_32b_50run/20260624_152843_deepseek_r1_32b_gpu_50run_job9189419/
```

Expected DeepSeek summary file:

```text
docs/demo_evidence/hpc_deepseek_r1_32b_50run/20260624_152843_deepseek_r1_32b_gpu_50run_job9189419/summary_50run.json
```

---

## Repository Structure

```text
.
├── assets/
│   └── luxllm_agent_final_demo_run008.gif
├── data/
│   ├── isometric_replay_frames.json
│   └── run008_decision_trace_overlay.json
├── docs/
│   ├── analysis/
│   ├── demo_evidence/
│   ├── dissertation/
│   ├── technical/
│   └── viewers/
│       └── s3_isometric_battle_viewer_v09n12d_trace_overlay.html
├── paper/
├── reports/
├── src/
│   ├── agent/
│   ├── scripts/
│   └── viewer_tools/
├── tools/
├── viewer/
├── LICENSE
└── README.md
```

Some generated or local-only folders may not be tracked in Git if they contain large raw logs, videos, temporary output, or generated PDFs.

---

## Quick Start: Local Viewer

From the project root:

```powershell
cd D:\PythonProject\lux_llm_agent
python -m http.server 8000
```

Open the Season 3 viewer:

```text
http://localhost:8000/docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html
```

The viewer reads replay frame data from:

```text
data/isometric_replay_frames.json
data/run008_decision_trace_overlay.json
```

---

## Agent Runtime Snapshot

The frozen source snapshot is provided under `src/agent/`, with supporting scripts under `src/scripts/` and viewer post-processing utilities under `src/viewer_tools/`. Re-running the full controlled experiments additionally requires a compatible Lux AI Season 3 environment, Ollama, the named local models, and the original local or Slurm runtime configuration. The tracked viewer and evidence summaries can be inspected without rerunning a match.

---

## Barkla2 GPU Evaluation

Large LLM experiments are intended to run on Barkla2 GPU nodes rather than local CPU nodes.

Example Barkla evidence already produced:

```text
qwen3:32b 50-run
deepseek-r1:32b 50-run
```

DeepSeek-R1-32B 50-run evidence was produced with:

```text
Model: deepseek-r1:32b
Runs: 50
Platform: Barkla2 GPU
LLM errors: 0
```

The corresponding evidence archive can be stored locally under:

```text
docs/demo_evidence/hpc_deepseek_r1_32b_50run/
```

---

## Main Environment Variables

The main runtime settings include:

```text
LUX_LLM_ENABLED
LUX_FORCE_RULE_ONLY
LUX_FORCE_FALLBACK
LUX_LLM_MODEL
LUX_LLM_BASE_URL
LLM_BASE_URL
LUX_EXPERIMENT_TAG
LUX_ENABLE_RULE_FALLBACK
LUX_ENABLE_STRATEGY_CACHE
LUX_ENABLE_RISK_AWARE_ACTION_FILTER
LUX_ENABLE_CANDIDATE_EXPLOITATION
LUX_LLM_TIMEOUT_SECONDS
LUX_LLM_CALL_INTERVAL
LUX_LLM_NUM_PREDICT
LUX_LLM_TEMPERATURE
```

Typical qwen3 setting:

```text
LUX_LLM_MODEL=qwen3:32b
```

Typical DeepSeek setting:

```text
LUX_LLM_MODEL=deepseek-r1:32b
```

---

## Research Interpretation

The current results support the following dissertation-level interpretation:

1. **Structured decision tracing** makes the LLM-agent behaviour inspectable beyond final match scores.
2. **Rule-based action verification** allows LLM outputs to be used as strategic proposals rather than unsafe direct actions.
3. **Fallback and caching** improve runtime stability and reduce the cost of repeated LLM calls.
4. **Replay-grounded inspection** connects state, decision source, action execution, and outcome.
5. **Model comparison** shows that the same framework can support different reasoning-oriented LLM backends.

The main contribution is not that one LLM is always better than another, but that LuxLLM-Agent provides a framework for running, tracing, validating, and evaluating LLM-based game agents under controlled conditions.

---

## Dissertation Use

This repository supports an MSc dissertation with the following likely structure:

```text
1. Introduction
2. Background and Related Work
3. Research Questions and Requirements
4. System Design
5. Implementation
6. Evaluation
7. Discussion
8. Conclusion
```

The strongest dissertation angle is:

> LuxLLM-Agent investigates how LLM-based game agents can be made more inspectable and reliable through structured decision tracing, rule-based action verification, and replay-grounded evaluation.

---

## Current Project Status

| Component                         | Status    |
| --------------------------------- | --------- |
| Lux AI Season 3 agent runtime     | Complete  |
| Rule-based baseline               | Complete  |
| qwen3:32b integration             | Complete  |
| DeepSeek-R1-32B comparison        | Complete  |
| 50-run qwen3 evidence             | Complete  |
| 50-run DeepSeek evidence          | Complete  |
| Match history logging             | Complete  |
| Decision trace logging            | Complete  |
| Isometric Season 3 viewer         | Complete  |
| Final Run008 demo visualisation   | Complete  |
| README evaluation update          | Complete  |
| Evidence index update             | Complete  |
| Failure analysis document         | Complete  |
| Viewer LLM Decision Trace Overlay | Complete  |
| Dissertation chapter drafts       | Complete  |
| Final 75-second demo screencast    | Complete  |
| Supervisor feedback integration   | Pending   |
| Citation and bibliography review  | Pending   |
| Final figures, tables, and format  | Pending   |

---

## Submission-Freeze Next Steps

1. Incorporate supervisor feedback without expanding the project scope.
2. Finalise citations and bibliography entries.
3. Verify that figures, tables, captions, and reported metrics agree across all documents.
4. Verify the final Run008 screenshots and upload the prepared 75-second screencast if a public URL is required.
5. Complete author, repository, licensing, and submission metadata.
6. Keep generated PDFs, raw videos, large logs, archives, and per-run directories out of normal Git history.

---

## File-size and Git Notes

Avoid committing very large generated files unless necessary:

```text
frame_log.jsonl
large raw videos
temporary local recordings
generated PDFs
temporary archives
```

Recommended compact evidence to commit:

```text
summary_50run.json
match_history_50run.jsonl
decision_log.jsonl
llm_decisions.jsonl
decision_trace.jsonl
ablation_metrics.jsonl
latest_match_console.txt
small markdown summaries
```

Generated PDFs should generally remain untracked unless required for submission. The `run01/` to `run50/` raw directories and local demo videos should remain outside normal Git history.

---

## License

This project is developed for academic research and MSc dissertation purposes. External dependencies, Lux AI components, LLM backends, and viewer assets should follow their respective licenses.

