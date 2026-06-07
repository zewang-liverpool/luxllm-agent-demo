# Demo Artifact Index v09o4

Version: `v0.9-O4-scalability-paper-integration`  
Created at: `2026-06-07 19:29:11`

This index extends the previous viewer artifact index with the O1/O2/O3/O4 scalability materials.

## Scalability Artifacts

| Category | Name | Path | Exists | Size MB | Description |
|---|---|---|---:|---:|---|
| paper | Scalability-integrated paper draft | `docs/latex/luxllm_agent_v09k3_scalability_integrated_v09o4.tex` | `True` | `0.056` | Paper draft containing the S3 viewer integration and scalability simulation section. |
| scalability | O1 scalability direction plan | `docs/scalability_direction_plan_v09o1.md` | `True` | `0.006` | Explains the 1000-agent interpretation and layered scalability architecture. |
| scalability | O1 scalability direction JSON | `logs/scalability_direction_plan_v09o1.json` | `True` | `0.008` | Structured O1 scalability plan. |
| scalability | O2 scalability simulation summary | `docs/scalability_simulation_summary_v09o2.md` | `True` | `0.005` | Markdown summary of the lightweight-worker scalability simulation. |
| scalability | O2 scalability simulation JSON | `logs/scalability_simulation_summary_v09o2.json` | `True` | `0.007` | Structured metrics from the lightweight-worker scalability runner. |
| scalability | O3 scalability evaluation summary | `docs/scalability_evaluation_table_v09o3.md` | `True` | `0.004` | Paper-ready scalability table, paragraph, and limitations text. |
| scalability | O3 scalability evaluation JSON | `logs/scalability_evaluation_table_v09o3.json` | `True` | `0.008` | Structured O3 paper-ready scalability evaluation data. |
| scalability | O3 scalability LaTeX table | `docs/latex/scalability_table_v09o3.tex` | `True` | `0.002` | Generated LaTeX table for the scalability simulation. |
| viewer | Previous viewer artifact index | `docs/demo_artifact_index_v09n12g.md` | `True` | `0.003` | Artifact index for the completed S3 battle replay viewer line. |

## Scalability Claim

The system scales by amortising sparse LLM-generated strategy templates over many lightweight worker agents rather than invoking an LLM once per worker.

## Boundary

The O2/O3 result is an architecture-level lightweight-worker simulation, not a full benchmark of 1000 Lux AI Season 3 matches.
