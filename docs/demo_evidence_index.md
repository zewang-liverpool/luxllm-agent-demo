# LuxLLM-Agent Demo Evidence Index

This document indexes the main experimental and demonstration evidence for **LuxLLM-Agent**, an interactive decision-trace and action-verification platform for LLM-based agents in **Lux AI Season 3**.

The evidence is organised around the project's main research question:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in complex multi-agent game environments such as Lux AI Season 3?

The evidence below supports the system implementation, controlled evaluation, LLM backend comparison, replay-grounded inspection, and thesis/demo documentation.

---

## 1. Project Positioning

**System name:** LuxLLM-Agent

**Main focus:**  
Structured decision tracing, rule-based action verification, replay-grounded inspection, and controlled-run evaluation for LLM-based game agents.

**Environment:**  
Lux AI Season 3

**Main LLM backend:**  
`qwen3:32b`

**Comparison LLM backend:**  
`deepseek-r1:32b`

**Core contribution:**  
The project does not only build a Lux AI game agent. It develops a framework for making LLM-agent decisions more inspectable, controllable, and evaluable through:

- structured game-state summarisation;
- LLM strategic decision generation;
- rule-based action verification;
- fallback and cache mechanisms;
- decision-source logging;
- replay-grounded visual inspection;
- controlled-run evaluation.

---

## 2. Main Evaluation Evidence

### 2.1 qwen3:32b 50-run Evaluation Evidence

This is the main LLM evaluation evidence used in the original LuxLLM-Agent controlled-run experiment.

| Item | Value |
|---|---|
| Model | `qwen3:32b` |
| Evaluation scale | 50 controlled matches |
| LLM player | `player_0` |
| Opponent | Rule-based fallback player |
| player_0 wins | 35 |
| player_1 wins | 15 |
| Draws | 0 |
| player_0 win rate | 70% |
| Strategy use rate | 96% |
| Fallback rate | 4% |
| LLM errors | 0 |

**Purpose:**  
This evidence demonstrates the main LLM-assisted setting for LuxLLM-Agent. It shows that the qwen3:32b-backed agent can run controlled Lux AI Season 3 matches with strategy caching, rule fallback, and risk-aware action filtering enabled.

**Evidence location:**

```text
docs/demo_evidence/hpc_qwen3_32b_50run/
````

If the exact local directory differs, use the directory containing the qwen3:32b 50-run summary and controlled-run logs.

---

### 2.2 DeepSeek-R1-32B 50-run Comparison Evidence

This is the newly added comparison LLM backend evidence. The purpose is not to build a general model leaderboard, but to test whether the LuxLLM-Agent decision-trace and action-verification framework can support another reasoning-oriented LLM under the same Lux AI Season 3 evaluation setting.

| Item                      | Value                                         |
| ------------------------- | --------------------------------------------- |
| Model                     | `deepseek-r1:32b`                             |
| Evaluation scale          | 50 controlled matches                         |
| LLM player                | `player_0`                                    |
| Opponent                  | Rule-based fallback player                    |
| Platform                  | Barkla2 GPU                                   |
| Framework version         | LuxLLM-Agent v0.9-E5.2 candidate-exploitation |
| Strategy cache            | Enabled                                       |
| Rule fallback             | Enabled                                       |
| Risk-aware action filter  | Enabled                                       |
| Candidate exploitation    | Enabled                                       |
| player_0 wins             | 26                                            |
| player_1 wins             | 24                                            |
| player_0 win rate         | 52%                                           |
| Average player_0 reward   | 2.7                                           |
| Average player_1 reward   | 2.3                                           |
| Average fresh LLM calls   | 33.2                                          |
| Average LLM strategy used | 27.24                                         |
| Average cached LLM turns  | 412.62                                        |
| Average fallback count    | 570.14                                        |
| Average LLM errors        | 0.0                                           |
| Average LLM latency       | 4143.595 ms                                   |
| Maximum LLM latency       | 10581.076 ms                                  |
| Average trace steps       | 1010.0                                        |

**Decision source distribution:**

| Decision source | Count |
| --------------- | ----: |
| `rule_player`   | 25250 |
| `fallback`      |    94 |
| `rule_fallback` |  3163 |
| `llm_fresh`     |  1362 |
| `cached_llm`    | 20631 |

**Derived rates:**

```text
Total decision-source events = 50500
LLM-related events = llm_fresh + cached_llm = 1362 + 20631 = 21993
LLM decision-source rate approximately 43.55%

Fallback-related events = fallback + rule_fallback = 94 + 3163 = 3257
Fallback decision-source rate approximately 6.45%
```

**Evidence location:**

```text
docs/demo_evidence/hpc_deepseek_r1_32b_50run/
```

**Raw run directory:**

```text
docs/demo_evidence/hpc_deepseek_r1_32b_50run/20260624_152843_deepseek_r1_32b_gpu_50run_job9189419/
```

**Expected summary file:**

```text
docs/demo_evidence/hpc_deepseek_r1_32b_50run/20260624_152843_deepseek_r1_32b_gpu_50run_job9189419/summary_50run.json
```

---

## 3. LLM Backend Comparison

The main model comparison is between the original qwen3:32b setting and the newly added DeepSeek-R1-32B setting.

| Model             | Runs | player_0 wins | player_1 wins | player_0 win rate | LLM errors | Notes                  |
| ----------------- | ---: | ------------: | ------------: | ----------------: | ---------: | ---------------------- |
| `qwen3:32b`       |   50 |            35 |            15 |               70% |          0 | Main LLM backend       |
| `deepseek-r1:32b` |   50 |            26 |            24 |               52% |          0 | Comparison LLM backend |

**Interpretation:**
Both LLM backends completed 50 controlled Lux AI Season 3 runs with zero LLM errors. This supports the system-level robustness of the LuxLLM-Agent framework across different reasoning-oriented LLMs.

The comparison should not be interpreted as a general LLM leaderboard. Instead, it supports the dissertation argument that the proposed decision-trace and rule-based action-verification framework can run different LLM backends through the same structured pipeline and produce comparable evaluation evidence.

**Comparison summary document:**

```text
docs/demo_evidence/llm_model_comparison_summary.md
```

---

## 4. Replay-grounded Viewer Evidence

### 4.1 Season 3 Isometric Replay Viewer

The Season 3 viewer provides an isometric replay interface for inspecting Lux AI Season 3 matches. It is designed to support replay-grounded analysis of match status, scores, agent behaviour, and evaluation context.

**Main viewer file:**

```text
docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html
```

**Main Run008 replay frame data:**

```text
data/isometric_replay_frames.json
```

**Purpose:**
The viewer demonstrates how game trajectories and evaluation evidence can be connected to a visual replay interface. It supports the dissertation direction of using replay-grounded inspection rather than relying only on aggregate win/loss metrics.

---

### 4.2 Run008 Final Demo Evidence

Run008 is used as the main visual demonstration run for the project.

**Associated evidence:**

```text
replays/
data/isometric_replay_frames.json
docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html
```

**Purpose:**
Run008 provides a concrete replay example for visualising LuxLLM-Agent behaviour and connecting match replay to evaluation context.

---

### 4.3 Final Demo Video / GIF Evidence

The project includes visual demo assets used in the README and paper/demo materials.

Expected assets include:

```text
assets/lux_s3_demo_run008.gif
assets/luxllm_agent_final_demo_run008.gif
docs/demo_videos/
```

If both GIF names exist, the README should use the most up-to-date final demo GIF and keep older GIFs as supporting evidence only.

---

## 5. Decision Trace and Logging Evidence

LuxLLM-Agent records decision-level information that supports inspection of LLM-agent behaviour.

Important log types include:

```text
decision_log.jsonl
llm_decisions.jsonl
decision_trace.jsonl
ablation_metrics.jsonl
match_history.jsonl
latest_match_console.txt
```

The most important fields for dissertation evaluation include:

* `llm_model`
* `experiment_tag`
* `winner`
* `player_0_reward`
* `player_1_reward`
* `fresh_llm_calls`
* `llm_strategy_used`
* `cached_llm_turns`
* `fallback_count`
* `llm_errors`
* `avg_llm_latency_ms`
* `max_llm_latency_ms`
* `decision_source_counts`
* `stale_decision_count`
* `risk_filter_changed_count`

These logs support the project's claim that LuxLLM-Agent provides more than a replay viewer: it provides structured decision provenance and evaluation evidence.

---

## 6. Dissertation-oriented Evaluation Metrics

For the MSc dissertation, the evaluation should not rely only on match win/loss. The recommended evaluation metrics are:

### 6.1 Gameplay outcome metrics

* Total matches
* player_0 wins
* player_1 wins
* Draws
* Average reward
* Win rate

### 6.2 LLM execution metrics

* Fresh LLM calls
* LLM strategy used
* Cached LLM turns
* LLM errors
* LLM latency
* Maximum LLM latency

### 6.3 Decision provenance metrics

* `llm_fresh`
* `cached_llm`
* `rule_player`
* `fallback`
* `rule_fallback`
* Decision source distribution
* LLM decision-source rate
* Fallback decision-source rate

### 6.4 Stability and safety metrics

* Fallback count
* Rule fallback count
* Risk filter change count
* Stale decision count
* Structured output validity
* Parser or action-verification failures

### 6.5 Qualitative inspection metrics

* Representative success cases
* Representative failure cases
* Reasoning/action consistency
* State-to-decision alignment
* Replay-grounded examples

---

## 7. Recommended Thesis Use

The evidence in this directory supports the following dissertation chapters:

| Dissertation chapter | Relevant evidence                                                                    |
| -------------------- | ------------------------------------------------------------------------------------ |
| Introduction         | Project motivation, Lux AI S3 as a controlled LLM-agent environment                  |
| Background           | LLM agents, game environments, decision tracing, action verification                 |
| System Design        | State summariser, LLM strategist, action verifier, fallback, viewer                  |
| Implementation       | Python agent runtime, Ollama backend, Barkla GPU evaluation, viewer implementation   |
| Evaluation           | qwen3:32b 50-run, deepseek-r1:32b 50-run, model comparison, decision-source analysis |
| Discussion           | Framework stability, model differences, limitations, failure cases                   |
| Conclusion           | Decision tracing and action verification as a method for inspecting LLM game agents  |

---

## 8. Current Evidence Status

| Evidence item                    | Status                          |
| -------------------------------- | ------------------------------- |
| qwen3:32b 50-run evidence        | Complete                        |
| DeepSeek-R1-32B 50-run evidence  | Complete                        |
| Run008 replay viewer             | Complete                        |
| Final demo GIF/video             | Complete or available locally   |
| LLM backend comparison table     | Added                           |
| Decision trace logs              | Available                       |
| Failure analysis                 | To be expanded                  |
| Viewer decision trace overlay    | Planned / next development step |
| README evaluation update         | Added                           |
| Dissertation evaluation write-up | Next step                       |

---

## 9. Next Steps

The next project-improvement steps are:

1. Add the DeepSeek-R1-32B evidence directory to the local repository.
2. Add `llm_model_comparison_summary.md`.
3. Update the README evaluation section.
4. Add failure-case analysis using selected `decision_trace.jsonl` examples.
5. Extend the viewer with a synchronised LLM Decision Trace Overlay.
6. Update the dissertation proposal and evaluation chapter with the qwen3 vs DeepSeek comparison.
7. Commit the new evidence and documentation to GitHub after removing large unnecessary logs such as `frame_log.jsonl`.

---

## 10. Notes on Large Files

Do not commit unnecessary large generated files such as:

```text
frame_log.jsonl
large raw video files
temporary local recordings
generated PDFs unless explicitly required
```

Recommended evidence files to keep:

```text
summary_50run.json
match_history_50run.jsonl
decision_log.jsonl
llm_decisions.jsonl
decision_trace.jsonl
ablation_metrics.jsonl
latest_match_console.txt
slurm output logs
small compressed evidence archives
```

Large replay or video files should be stored through GitHub Releases, external storage, or kept locally unless required for the artifact.

```
```

