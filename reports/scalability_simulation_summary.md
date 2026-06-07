# Lux AI Season 3 Scalability Simulation Runner

Version: `v0.9-O2-scalability-simulation-runner`  
Created at: `2026-06-07 19:22:04`

## 1. Purpose

This document reports the O2 scalability simulation runner.

The goal is to provide lightweight architecture-level evidence for the 1000-agent scalability direction. This is not a full Lux AI Season 3 match benchmark.

## 2. Simulation Scope

- Full Lux match benchmark: `False`
- Uses Ollama: `False`
- Uses luxai-s3 executable: `False`
- Uses real LLM call per agent: `False`

This is a synthetic lightweight worker simulation designed to test the decision architecture and throughput, not a benchmark of 1000 full Lux matches.

## 3. Scalability Interpretation

In this project, 1000 agents means a scalable agent runtime in which many lightweight agents can be simulated, scheduled, evaluated, or controlled using shared policy templates and batched decision logic, while the LLM acts as a high-level strategist rather than a per-unit controller.

Short claim:

The system scales by separating expensive strategic reasoning from low-cost agent execution.

## 4. Policy Templates

- `explore`
- `collect_energy`
- `move_to_relic`
- `risk_aware`
- `late_game_score`

## 5. Headline Results

- Max agent count: `1000`
- Max total decisions: `100000`
- Max decisions/sec: `132199.94`
- Scaling claim: LLM calls remain constant because the LLM is treated as a sparse strategist that generates reusable policy templates, while many lightweight workers execute cached policies locally.

## 6. Simulation Metrics

| Agent count | Steps/agent | Total decisions | LLM calls | Cached policy uses | Fallback uses | Runtime (s) | Decisions/sec | Memory MB |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 100 | 1000 | 5 | 1000 | 0 | 0.007564 | 132199.94 | 0.346 |
| 100 | 100 | 10000 | 5 | 10000 | 4 | 0.078984 | 126607.92 | 1.214 |
| 500 | 100 | 50000 | 5 | 50000 | 48 | 0.409489 | 122103.52 | 5.072 |
| 1000 | 100 | 100000 | 5 | 100000 | 81 | 0.807 | 123915.78 | 9.894 |

## 7. Policy Distribution

### 10 agents

- `collect_energy`: `2`
- `explore`: `2`
- `late_game_score`: `2`
- `move_to_relic`: `2`
- `risk_aware`: `2`

### 100 agents

- `collect_energy`: `20`
- `explore`: `20`
- `late_game_score`: `20`
- `move_to_relic`: `20`
- `risk_aware`: `20`

### 500 agents

- `collect_energy`: `100`
- `explore`: `100`
- `late_game_score`: `100`
- `move_to_relic`: `100`
- `risk_aware`: `100`

### 1000 agents

- `collect_energy`: `200`
- `explore`: `200`
- `late_game_score`: `200`
- `move_to_relic`: `200`
- `risk_aware`: `200`


## 8. Action Distribution

### 10 agents

- `COLLECT`: `118`
- `MOVE_EAST`: `254`
- `MOVE_NORTH`: `276`
- `MOVE_SOUTH`: `168`
- `MOVE_WEST`: `172`
- `RETREAT`: `12`

### 100 agents

- `COLLECT`: `1480`
- `MOVE_EAST`: `2564`
- `MOVE_NORTH`: `2660`
- `MOVE_SOUTH`: `1616`
- `MOVE_WEST`: `1611`
- `RETREAT`: `69`

### 500 agents

- `COLLECT`: `7566`
- `MOVE_EAST`: `13046`
- `MOVE_NORTH`: `13393`
- `MOVE_SOUTH`: `7805`
- `MOVE_WEST`: `7919`
- `RETREAT`: `271`

### 1000 agents

- `COLLECT`: `14638`
- `MOVE_EAST`: `26287`
- `MOVE_NORTH`: `26851`
- `MOVE_SOUTH`: `15852`
- `MOVE_WEST`: `15835`
- `RETREAT`: `537`


## 9. Paper-Ready Paragraph

To evaluate scalability without overstating full-game throughput, we implemented a synthetic lightweight-worker simulation. The runner instantiates 10, 100, 500, and 1000 worker agents, each executing cached policy templates for a fixed number of decision steps. The simulation does not launch Lux matches and does not call the LLM per worker. Instead, a small fixed number of synthetic LLM calls represents the generation of reusable strategy templates. This demonstrates the intended scaling mechanism: expensive strategic reasoning is amortised across many low-cost worker decisions.


## 10. Limitations

- This simulation does not represent 1000 full Lux AI Season 3 matches.
- Runtime numbers measure lightweight decision throughput, not full environment stepping.
- Memory estimates are conservative synthetic estimates for worker state and decision logs.
- The result should be described as architecture-level scalability evidence.

## 11. Next Version

Next version:

`v0.9-O3-scalability-evaluation-table-and-paper-text`

Planned goals:

- Convert O2 metrics into LaTeX tables.
- Generate paper-ready scalability evaluation text.
- Add a limitations paragraph that avoids overclaiming.
- Prepare integration into the EMNLP Demo Paper discussion section.

## 12. Development Decision

`v0.9-O2` provides synthetic scalability evidence for the agent runtime architecture. It should be followed by O3, which converts the metrics into paper-ready tables and discussion text.
