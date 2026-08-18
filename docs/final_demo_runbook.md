# LuxLLM-Agent Final Demonstration Runbook

## Purpose

This runbook provides a repeatable 7-10 minute demonstration that answers the project research question:

> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent, long-horizon, and rule-constrained strategy game such as Lux AI Season 3, and how can the project-specific Decision-Trace and Action-Verification (DTAV) method address the observed limitations?

The demonstration should foreground inspection, verification, and evidence. Match win rate is secondary.

## Local artifact paths

Project root:

```text
D:\PythonProject\lux_llm_agent
```

Primary live viewer:

```text
D:\PythonProject\lux_llm_agent\docs\viewers\s3_isometric_battle_viewer_v09n12d_trace_overlay.html
```

Viewer data:

```text
D:\PythonProject\lux_llm_agent\logs\isometric_replay_frames_v09n11.json
D:\PythonProject\lux_llm_agent\data\run008_decision_trace_overlay.json
```

Primary backup video:

```text
D:\PythonProject\lux_llm_agent\docs\demo_videos\LuxLLM_Agent_Final_Demo_Run008_Isometric_Visualization.mp4
```

Verified video properties: MP4 container, H.264 video, AAC audio, 2528x1212, 30 fps, 75.33 seconds, 121,229,530 bytes.

Primary evaluation report:

```text
D:\PythonProject\lux_llm_agent\reports\final_trace_evaluation.md
```

Supplementary direct LLM-versus-LLM report:

```text
D:\PythonProject\lux_llm_agent\reports\dual_llm_trace_evaluation.md
```

Reproducibility guide:

```text
D:\PythonProject\lux_llm_agent\docs\reproducibility_guide.md
```

## Pre-demonstration checklist

Complete these checks at least 30 minutes before presenting:

1. Connect the laptop to power and disable disruptive notifications.
2. Confirm the four paths above exist.
3. Open PowerShell in the project root.
4. Start the local server:

   ```powershell
   cd D:\PythonProject\lux_llm_agent
   python -m http.server 8000
   ```

5. Open the viewer:

   ```text
   http://localhost:8000/docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html
   ```

6. Confirm the replay timeline loads and the decision-trace panel does not report a data-loading error.
7. Open `reports/final_trace_evaluation.md` and `reports/dual_llm_trace_evaluation.md` in separate tabs.
8. Open the backup MP4 and pause it at the beginning.
9. Keep the repository README open as a fallback architecture explanation.

## Demonstration script

### 0:00-1:00 — Problem and research question

Say:

> LuxLLM-Agent does not treat an LLM response as a directly executable game action. The project investigates how the project-specific DTAV decision-trace approach and rule-based action verification make an LLM-assisted agent inspectable and evaluable in Lux AI Season 3.

Explain that final win/loss alone cannot reveal whether the LLM was called, whether a cached decision was used, or whether a verifier changed a proposal.

### 1:00-2:15 — Controlled architecture

Show the README architecture section. Follow this sequence verbally:

```text
Lux observation -> state summary -> structured LLM proposal
-> parsing and normalization -> rule/risk verification
-> legal action construction -> trace logging -> replay inspection
```

Emphasise that the LLM provides bounded unit intents and the deterministic layer retains control of executable actions.

### 2:15-4:30 — Replay-grounded inspection

Show the live viewer. Move through several replay steps and point out:

- the **Lux AI Season 3** label and the three-stage **Proposal Context -> Rule Verification -> Executed State** layout;
- current match and step;
- score and player context;
- the **Proposal attempt**, **Fallback checkpoint**, and **Final frame** shortcuts;
- model objective, risk posture, and unit intents;
- verifier or risk-filter intervention fields;
- connection between the displayed state and recorded trace.

State clearly that Run008 is a qualitative fallback replay and must not be used as proof of the formal call-validity result. Open **Final** to show the separately labelled aggregate evidence from all 200 primary matches and the 100 supplementary direct dual-LLM matches.

### 4:30-6:30 — Formal evidence

Open `reports/final_trace_evaluation.md` and explain:

- 200/200 formal matches completed;
- 206,591 trace records;
- 100% recorded agent-step and LLM-call field completeness;
- 100% replay linkage and action-array shape validity;
- 4,591/4,591 calls valid after checks;
- 520 Qwen responses required deterministic normalization;
- risk filtering changed proposed targets on 5,590 Qwen and 7,090 DeepSeek steps;
- no timeout, LLM error, or downstream action fallback was observed.

Explain that these numbers are evidence of inspectability and verifier operation, not proof that all possible LLM outputs are safe.

Briefly open `reports/dual_llm_trace_evaluation.md`. State that the supervisor-requested supplementary experiment completed 100/100 direct Qwen-versus-DeepSeek matches over 50 role-swapped seed pairs, retained 106,317 complete traces, and produced 4,676/4,676 valid fresh calls. Emphasise that this demonstrates simultaneous two-sided tracing and verification. Do not present the 54:46 outcome as a model ranking; the seed-level exact sign p-value was 0.503.

### 6:30-7:30 — Controlled outcomes and limitations

Report Qwen 63/100 and DeepSeek 60/100, then immediately add that the matched difference was not statistically supported: paired-bootstrap 95% interval [-0.07, 0.13], McNemar p=0.690.

State the main limitations: two models, one rule-based opponent, one game environment, hybrid attribution, and hardware-dependent latency.

### 7:30-8:30 — Reproducibility and conclusion

Show `docs/reproducibility_guide.md`, `tests/`, and `.github/workflows/ci.yml`.

Conclude:

> Structured decision traces make decision provenance and verifier intervention auditable. Rule-based verification creates a controlled boundary between model proposals and legal actions. Together, they support evaluation that is richer than win rate alone.

## Backup plan

If the live viewer fails:

1. Play `LuxLLM_Agent_Final_Demo_Run008_Isometric_Visualization.mp4`.
2. Use the figures under `paper/figures/` to explain the overlay and final result.
3. Continue with `reports/final_trace_evaluation.md`; the evaluation argument does not depend on a live LLM call.

Do not attempt to run Qwen3-32B or DeepSeek-R1-32B live during the presentation. The formal runs are preserved evidence, and a live model call introduces avoidable network, GPU, and latency risk.

## Likely questions and short answers

**Why not let the LLM directly control actions?**

Lux actions must be legal and timely. Bounded strategic proposals preserve model input while deterministic code retains execution control.

**Does zero action fallback prove the system is safe?**

No. It shows no downstream action failure was observed in these runs. The trace also records normalization and risk-filter interventions, which reveal where control was needed.

**Is Qwen better than DeepSeek?**

Not established here. The matched comparison interval crosses zero and the McNemar test is not significant. The experiment demonstrates framework support for both backends.

**Can one LLM-assisted agent play directly against another?**

Yes. The supplementary experiment completed 100 role-swapped Qwen-versus-DeepSeek matches while keeping separate per-player traces. Its purpose is to test concurrent inspection and verification, not to replace the main research question with a model-ranking study.

**Can the results be reproduced without a GPU?**

The setup, tests, smoke runs, statistics, trace analysis, and viewer can be reproduced locally. Re-running the formal 32B inference requires suitable GPU resources and the recorded Ollama models.
