# Reproducible Source Code

`src/agent/` is the canonical LuxLLM-Agent runtime.  It is no longer a partial
documentation snapshot: the state parser, prompt builder, planner, rule
fallback, decision logger, and official Lux entry point are all tracked.

```text
src/agent/
├── main.py
├── agent.py
├── baseline_agent.py
├── action_planner.py
├── config.py
├── game_memory.py
├── llm_decider.py
├── lux_state.py
├── rule_policy.py
└── state_summarizer.py
```

Supporting result parsing utilities remain under `src/viewer_tools/`.  Current
installation, smoke-test, single-match, paired 100-match, and Slurm entry points
are under the top-level `scripts/` directory.

See `docs/reproducibility_guide.md` for exact commands and acceptance criteria.
