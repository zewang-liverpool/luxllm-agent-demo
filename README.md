# LuxLLM-Agent Demo Package

LuxLLM-Agent is an explainable LLM-assisted agent and replay viewer for **Lux AI Season 3**.
This repository contains a clean demonstration package prepared for an EMNLP System Demonstrations paper draft.

The project demonstrates how an LLM-assisted game agent can be made inspectable through structured decision logs, replay-frame generation, an S1-style isometric battle replay viewer, controlled evaluation summaries, lightweight scalability evidence, and a minimal source-code package.

---

## 1. Repository Contents

```text
luxllm-agent-demo/
├── README.md
├── .gitignore
├── paper/
│   ├── main.tex
│   ├── acl.sty
│   ├── acl_natbib.bst
│   ├── anthology.bib
│   ├── custom.bib
│   ├── luxllm_agent_demo_draft.pdf
│   ├── README.md
│   └── figures/
│       ├── figure_s3_replay_viewer.png
│       ├── figure_s3_presentation_mode.png
│       ├── figure_s3_final_result_overlay.png
│       └── figure_s3_match_score_summary.png
├── viewer/
│   └── s3_isometric_battle_viewer.html
├── data/
│   └── isometric_replay_frames.json
├── reports/
│   ├── final_capture_verification.md
│   ├── scalability_direction_plan.md
│   ├── scalability_simulation_summary.md
│   ├── scalability_evaluation_table.md
│   └── scalability_closeout.md
├── docs/
│   └── demo_artifact_index.md
├── video/
│   └── README.md
└── src/
    ├── README.md
    ├── agent/
    │   ├── main.py
    │   ├── agent.py
    │   ├── baseline_agent.py
    │   ├── rule_policy.py
    │   ├── llm_decider.py
    │   ├── action_planner.py
    │   ├── game_memory.py
    │   └── config.py
    ├── viewer_tools/
    │   ├── state_summarizer.py
    │   └── record_match_result_from_console.py
    └── scripts/
        ├── run_match_llm.bat
        └── run_v09c_pipeline.bat
```

---

## 2. Main Demo

The main demo artifact is the S3-style isometric battle replay viewer:

```text
viewer/s3_isometric_battle_viewer.html
```

The viewer visualises a Lux AI Season 3 replay using merged replay-frame data. It shows:

* an S1-style floating-island battle map;
* both players' units;
* battle timeline information;
* per-match score summary;
* current match state;
* ship counts;
* known relics;
* risk-change count;
* final result overlay;
* recording-friendly presentation mode.

The replay data used by the viewer is stored in:

```text
data/isometric_replay_frames.json
```

---

## 3. Running the Viewer Locally

From the repository root, run:

```bash
python -m http.server 8010 --bind 127.0.0.1
```

Then open the viewer in a browser:

```text
http://127.0.0.1:8010/viewer/s3_isometric_battle_viewer.html
```

The viewer is configured to load the replay JSON from:

```text
../data/isometric_replay_frames.json
```

If automatic loading fails, use the file selector in the lower-left panel of the viewer and manually select:

```text
data/isometric_replay_frames.json
```

---

## 4. Paper Source

The LaTeX paper source is located in:

```text
paper/main.tex
```

The compiled draft PDF is:

```text
paper/luxllm_agent_demo_draft.pdf
```

The paper uses the ACL/EMNLP LaTeX style files included in the `paper/` directory:

```text
paper/acl.sty
paper/acl_natbib.bst
paper/anthology.bib
paper/custom.bib
```

The paper figures are stored in:

```text
paper/figures/
```

Current figures:

```text
paper/figures/figure_s3_replay_viewer.png
paper/figures/figure_s3_presentation_mode.png
paper/figures/figure_s3_final_result_overlay.png
paper/figures/figure_s3_match_score_summary.png
```

---

## 5. Source Code Package

The `src/` directory contains the minimal source-code package for the demo:

```text
src/
├── agent/
├── viewer_tools/
└── scripts/
```

The source package is intentionally smaller than the full development workspace. It includes the core files needed to understand the system implementation:

* agent entry points;
* rule-based fallback policy;
* LLM decision layer;
* action planning;
* memory and state handling;
* replay/evaluation support tools;
* demo run scripts.

The full development workspace contains additional experimental scripts, historical viewers, controlled-run logs, archive tools, and local debugging utilities. Those files are not included here in order to keep the demo package clean and reviewable.

---

## 6. Evaluation Artifacts

The `reports/` directory contains the main evaluation and verification reports:

```text
reports/final_capture_verification.md
reports/scalability_direction_plan.md
reports/scalability_simulation_summary.md
reports/scalability_evaluation_table.md
reports/scalability_closeout.md
```

These reports document:

* S3 viewer screenshot and video capture verification;
* the 1000-agent scalability interpretation;
* synthetic lightweight-worker scalability simulation;
* paper-ready scalability table and explanation;
* final closeout of the scalability line.

---

## 7. Key Demonstration Evidence

The current replay package contains:

* 505 replay frames;
* 96.83% both-player frame coverage;
* 662 risk-filter changes;
* final replay result: `player_1` wins the final match;
* total match wins: `3:2`;
* total score: `407:363`.

The viewer and paper figures are based on the verified replay package.

---

## 8. Scalability Note

The 1000-agent result is an **architecture-level lightweight-worker simulation**.

It should not be interpreted as a benchmark of 1000 full Lux AI Season 3 matches.

The scalability simulation demonstrates that the system can amortise sparse LLM-generated policy templates across many lightweight worker agents:

```text
Max agent count: 1000
Synthetic decisions: 100,000
Synthetic LLM calls: 5
Runtime at 1000 workers: 0.807 seconds
Decisions per LLM call at 1000 workers: 20,000
```

The main claim is:

```text
The system scales by reusing sparse LLM-generated strategy templates across many lightweight worker agents, rather than invoking an LLM once per worker.
```

---

## 9. Demo Video

The demo screencast video is provided through the GitHub Release page:

```text
https://github.com/zewang-liverpool/luxllm-agent-demo/releases/tag/demo-video
```

The video demonstrates the S3 isometric battle replay viewer, including:

* replay loading;
* timeline playback;
* S1-style isometric battle map;
* presentation mode;
* match score summary;
* final result overlay.

Target video:

```text
Lux S3 Isometric Battle Replay demo
Length: <= 2.5 minutes
```

---

## 10. Availability

Repository:

```text
https://github.com/zewang-liverpool/luxllm-agent-demo
```

Demo video:

```text
https://github.com/zewang-liverpool/luxllm-agent-demo/releases/tag/demo-video
```

The paper source, compiled draft PDF, viewer, replay data, figures, reports, minimal source code, and video release link are included in this repository package.

---

## 11. Reproducibility Notes

This repository is a clean demonstration package, not the full development workspace.

The full development workspace contains additional intermediate scripts, logs, experimental viewers, paper-generation scripts, archive files, and local run artifacts. This package keeps only the demonstration files needed for review and reproduction.

The viewer can be opened locally using Python's built-in HTTP server. No cloud LLM API is required to inspect the included replay.

The included replay is already generated and can be inspected directly through the viewer. Re-running full Lux AI Season 3 matches may require the Lux AI Season 3 environment, local Python dependencies, and an optional local Ollama model backend.

---

## 12. Recommended Reviewer Workflow

A reviewer or supervisor can inspect the package in this order:

1. Open the paper draft:

```text
paper/luxllm_agent_demo_draft.pdf
```

2. Start a local HTTP server:

```bash
python -m http.server 8010 --bind 127.0.0.1
```

3. Open the viewer:

```text
http://127.0.0.1:8010/viewer/s3_isometric_battle_viewer.html
```

4. Inspect the replay data:

```text
data/isometric_replay_frames.json
```

5. Review the minimal source-code package:

```text
src/
```

6. Review the evaluation and scalability reports:

```text
reports/
```

7. Review the artifact index:

```text
docs/demo_artifact_index.md
```

8. Watch the demo video:

```text
https://github.com/zewang-liverpool/luxllm-agent-demo/releases/tag/demo-video
```

---

## 13. Project Status

Current package status:

```text
S3 replay viewer: ready
Replay JSON: ready
Paper figures: ready
Paper draft PDF: ready
Evaluation reports: ready
Scalability reports: ready
Minimal source-code package: ready
Demo video link: ready
Public repository URL: ready
```

---

## 14. License

The intended release license will be confirmed before public submission.
Recommended options are MIT or Apache-2.0.

For now, this package should be treated as a research prototype prepared for supervisor review and demo-paper development.

---

## 15. Citation / Acknowledgement

This project is built around the Lux AI Season 3 competition environment and is intended for research and educational use in game AI, LLM-assisted agents, and explainable agent evaluation.

The system is not a deployed autonomous decision-making system and does not process personal data.
