# Lux AI Season 3 1000-Agent Scalability Plan

Version: `v0.9-O1-1000-agents-scalability-plan`  
Created at: `2026-06-07 19:08:44`

## 1. Purpose

This document starts the 1000-agent scalability direction after the S3 battle replay viewer and paper/demo integration line has been closed.

The goal is to answer the supervisor's scalability concern in a realistic and paper-ready way.

## 2. Previous Line Status

The S3 battle replay viewer, screenshots, demo video, artifact index, and integrated paper PDF have been completed. The next development direction can now shift to scalability.

- Paper/demo line complete: `True`
- Integrated PDF ready: `True`
- Viewer package ready: `True`

## 3. Existing Replay Evidence

- Frame count: `505`
- Both-player frame rate: `96.83%`
- Risk-filter changes: `662`
- Final score: `72:84`
- Winner: `player_1`
- Match wins: `3:2`
- Total score: `407:363`

## 4. Scalability Problem Definition

**Supervisor question:**  
Can the system scale beyond a single LLM-controlled demo agent, for example towards many agents or 1000 agents?

**Wrong interpretation:**  
Running 1000 fully independent LLM calls per decision step is not the intended or practical interpretation. This would be too slow, too expensive, and unsuitable for real-time game environments.

**Project interpretation:**  
In this project, 1000 agents means a scalable agent runtime in which many lightweight agents can be simulated, scheduled, evaluated, or controlled using shared policy templates and batched decision logic, while the LLM acts as a high-level strategist rather than a per-unit controller.

## 5. Proposed Scalable Architecture

| Layer | Role | Example |
|---|---|---|
| LLM Strategist Layer | Generates high-level strategy, policy templates, evaluation rubrics, or scenario-level instructions. It is called sparsely rather than once per lightweight agent. | Ask Qwen2.5 to produce a strategy template for exploration, relic control, risk avoidance, or late-game scoring. |
| Policy Template Layer | Stores reusable strategies as structured rules. These templates can be applied by many agents without additional LLM calls. | A template may specify target selection priority, risk radius, fallback movement, and scoring behaviour. |
| Lightweight Agent Worker Layer | Runs many low-cost agents using local rules, cached LLM decisions, or policy templates. This is the layer that can scale to hundreds or thousands of simulated agents. | 1000 workers can each run a simple policy instance with different seeds, maps, parameters, or opponent assumptions. |
| Batch Runner / Simulation Layer | Executes large batches of lightweight agents, records metrics, and produces aggregate evidence for scalability. | Run 10, 100, 500, and 1000 lightweight policy instances in a synthetic simulation to measure runtime, memory use, decision throughput, and outcome diversity. |
| Evaluation and Viewer Layer | Summarizes results through JSON, Markdown, tables, and visual viewers. The existing S3 battle replay viewer becomes the demonstration layer. | Use artifact index, replay viewer, and evaluation tables to connect scalability evidence back to the paper. |

## 6. O2 Runner Design

Next runner name:

`v0.9-O2-scalability-simulation-runner`

Goal:

Create a lightweight scalability simulation runner that can instantiate many agent workers without launching full Lux matches for every worker.

### Inputs

- Agent counts: `[10, 100, 500, 1000]`
- Policy templates: `['explore', 'collect_energy', 'move_to_relic', 'risk_aware', 'late_game_score']`
- Random seeds: `integer seed list`
- Step count: `synthetic decision steps per agent`

### Outputs

- JSON: `logs/scalability_simulation_summary_v09o2.json`
- Markdown: `docs/scalability_simulation_summary_v09o2.md`

Metrics:

- `agent_count`
- `total_decisions`
- `runtime_seconds`
- `decisions_per_second`
- `llm_calls`
- `cached_policy_uses`
- `fallback_uses`
- `memory_estimate_mb`
- `policy_distribution`

Important constraint:

O2 should not require running 1000 full Lux matches. It should first test the agent runtime and decision architecture using lightweight synthetic worker states.

## 7. Paper Explanation

Short claim:

The system scales by separating expensive strategic reasoning from low-cost agent execution.

Paper paragraph:

Rather than assigning an LLM call to every unit or every agent, the proposed architecture uses the LLM as a sparse strategist that produces reusable policy templates. These templates are then executed by many lightweight worker agents under a batch runner. This design allows the system to evaluate hundreds or thousands of policy instances while keeping LLM cost bounded. The viewer and artifact pipeline provide demonstration-level evidence, while the scalability runner provides system-level evidence.

Suggested scalability table columns:

- Configuration
- Agent count
- LLM calls
- Decision steps
- Runtime
- Decisions/sec
- Notes

## 8. Development Plan

| Version | Status | Deliverable |
|---|---|---|
| `v0.9-O1` | current | Scalability direction plan and paper-ready architecture explanation. |
| `v0.9-O2` | next | Synthetic scalability simulation runner for 10/100/500/1000 lightweight agents. |
| `v0.9-O3` | planned | Scalability result summary, tables, and paper-ready evaluation text. |
| `v0.9-O4` | planned | Integration of scalability evidence into the EMNLP Demo Paper discussion. |

## 9. Risks and Boundaries

| Risk | Mitigation |
|---|---|
| Overclaiming real 1000-agent Lux performance | Clearly state that O2 is a lightweight scalability simulation of the agent runtime, not 1000 full Lux matches. |
| LLM latency grows linearly with agent count | Use sparse LLM calls and policy templates so LLM calls do not scale linearly with the number of workers. |
| Scalability evidence becomes disconnected from the S3 viewer | Connect O2/O3 evidence back to the existing viewer and artifact pipeline in the paper narrative. |

## 10. Next Version

Next version:

`v0.9-O2-scalability-simulation-runner`

Planned goals:

- Implement a synthetic lightweight agent worker state.
- Implement policy templates without requiring LLM calls per worker.
- Run 10, 100, 500, and 1000 worker simulations.
- Record runtime, decision throughput, LLM-call count, cache usage, and policy distribution.
- Generate JSON and Markdown reports for paper evaluation.

## 11. Development Decision

`v0.9-O1` defines the scalability direction. The next implementation should be a lightweight scalability simulation runner, not a full 1000-match Lux benchmark.
