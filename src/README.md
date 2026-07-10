# Source Code Snapshot

This directory contains the frozen source-code snapshot used to document the LuxLLM-Agent implementation. It exposes the main agent, fallback policy, LLM decision layer, replay summarisation utilities, and development scripts without including large local logs, models, replays, or environment files.

## Structure

```text
src/
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

The tracked Run008 viewer can be inspected without executing this runtime. Full match re-execution additionally depends on the compatible Lux AI Season 3 environment, Ollama, the named model, and the original local or Slurm configuration. The scripts are retained as development evidence rather than presented as a clean-install, one-command runner.
