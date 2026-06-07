# Lux AI Season 3 Scalability Evaluation Table

Version: `v0.9-O3-scalability-evaluation-table-and-paper-text`  
Created at: `2026-06-07 19:25:53`

## 1. Purpose

This document converts the O2 scalability simulation results into paper-ready evaluation material.

The goal is to provide a careful, non-overclaiming answer to the 1000-agent scalability question.

## 2. Source

- O2 summary: `logs/scalability_simulation_summary_v09o2.json`
- Exists: `True`

## 3. Scope Reminder

This is an architecture-level lightweight-worker simulation. It is not a full Lux AI Season 3 benchmark and does not represent 1000 full Lux matches.

## 4. Scaling Summary

- Min agent count: `10`
- Max agent count: `1000`
- Max total decisions: `100000`
- Constant LLM calls: `True`
- LLM calls: `5`
- Max decisions/sec: `132199.94`
- Decisions per LLM call at max agents: `20000.0`
- Runtime at max agents: `0.807`
- Memory estimate at max agents: `9.894` MB

## 5. Paper-Ready Table

| Agent count | Total decisions | LLM calls | Cached policy uses | Fallback uses | Runtime (s) | Decisions/sec | Memory MB |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 10 | 1000 | 5 | 1000 | 0 | 0.008 | 132,199.94 | 0.346 |
| 100 | 10000 | 5 | 10000 | 4 | 0.079 | 126,607.92 | 1.214 |
| 500 | 50000 | 5 | 50000 | 48 | 0.409 | 122,103.52 | 5.072 |
| 1000 | 100000 | 5 | 100000 | 81 | 0.807 | 123,915.78 | 9.894 |

## 6. Paper-Ready Claims

- The scalability runner reaches 1000 lightweight workers and 100,000 synthetic worker decisions.
- The number of synthetic LLM calls remains fixed at 5 across all tested worker counts, because the LLM is treated as a sparse strategist that generates reusable policy templates.
- At the 1000-worker setting, the runner completes 100,000 decisions in 0.807 seconds with an estimated 9.894 MB lightweight worker-state footprint.
- The result supports an architecture-level scalability claim, not a claim that 1000 full Lux AI Season 3 matches were executed.

## 7. Paper-Ready Paragraph

To evaluate scalability without overstating full-game throughput, we implemented a synthetic lightweight-worker simulation. The runner instantiates 10, 100, 500, and 1000 worker agents, each executing cached policy templates for 100 decision steps. The simulation does not launch full Lux AI Season 3 matches and does not invoke an LLM for every worker. Instead, five synthetic LLM calls represent sparse strategy-template generation. The 1000-worker setting completes 100,000 lightweight decisions in 0.807 seconds, while the LLM-call count remains fixed at 5. This result supports the intended scaling mechanism: expensive strategic reasoning is amortised across many low-cost worker decisions.


## 8. Limitations Paragraph

This experiment is an architecture-level scalability simulation rather than a full Lux benchmark. The reported runtime measures lightweight policy execution and synthetic worker-state updates, not environment stepping, game-engine rendering, or 1000 complete Lux matches. We therefore use the result to support the system design claim that the LLM can act as a sparse strategist while many workers execute cached policy templates, rather than to claim full-game multi-agent performance at this scale.

## 9. Generated Artifacts

- JSON: `logs/scalability_evaluation_table_v09o3.json`
- Markdown: `docs/scalability_evaluation_table_v09o3.md`
- LaTeX table: `docs/latex/scalability_table_v09o3.tex`

## 10. Recommended Paper Location

- Primary section: `Evaluation`
- Secondary section: `Discussion or Limitations`
- Availability note: Mention the JSON and Markdown reports as part of the artifact package.

## 11. Next Version

Next version:

`v0.9-O4-scalability-paper-integration`

Planned goals:

- Safely merge the scalability table into the integrated LaTeX paper.
- Add the paper-ready scalability paragraph to the Evaluation section.
- Add the limitations paragraph to the Limitations section.
- Update the artifact index with O1/O2/O3 scalability reports.
- Compile the updated paper and close the scalability line.

## 12. Development Decision

`v0.9-O3` converts the synthetic scalability runner output into paper-ready evaluation material. The next step should integrate this material into the LaTeX paper and update the artifact index.
