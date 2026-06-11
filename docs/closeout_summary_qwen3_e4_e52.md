# Closeout Summary: qwen3:32b E4 / E5.2 Evaluation Update

## Closeout Date

2026-06-11

## Main Paper Configuration

The main reported configuration is **E4 strategy-diversity**.

Run directory:

`docs/hpc_qwen3_gpu_e4_50run/20260610_180133_qwen3_32b_gpu_e4_50run_job8994080/`

Main result:

- Total runs: 50
- LLM-assisted player wins: 29
- Rule-controlled player wins: 21
- Avg fresh LLM calls: 15.74
- Avg LLM strategy used: 15.74
- Avg cached LLM turns: 489.26
- Avg fallback count: 505.0
- Avg LLM errors: 0.0
- Avg LLM latency: 4778.339 ms
- Max LLM latency: 5616.218 ms
- Avg trace steps: 1010.0
- Decision sources:
  - rule_player: 25250
  - llm_fresh: 787
  - cached_llm: 24463

## Supplementary Ablation

The supplementary ablation is **E5.2 candidate-exploitation**.

Run directory:

`docs/hpc_qwen3_gpu_e52_50run/20260610_221857_qwen3_32b_gpu_e52_50run_job8997743/`

Result:

- Total runs: 50
- LLM-assisted player wins: 26
- Rule-controlled player wins: 24
- Avg fresh LLM calls: 25.62
- Avg LLM strategy used: 25.54
- Avg cached LLM turns: 479.46
- Avg fallback count: 505.0
- Avg LLM errors: 0.0
- Avg LLM latency: 4893.165 ms
- Max LLM latency: 5511.419 ms
- Avg trace steps: 1010.0
- Decision sources:
  - rule_player: 25250
  - llm_fresh: 1277
  - cached_llm: 23973

## Interpretation

E4 remains the main reported configuration because it achieved the strongest stable 50-match controlled result among the current qwen3:32b variants.

E5.2 remained technically stable, with zero average LLM errors and complete trace coverage, but it did not outperform E4 at the 50-match scale. It should therefore be reported as a supplementary ablation rather than as an improvement.

## Updated Files

The following files were updated during this closeout:

- `README.md`
- `main.tex`
- `docs/evidence/qwen3_gpu_evidence_index.md`
- `docs/reviewer_response_qwen3_update.md`
- `docs/paper_assets_index_v09k3.md`
- `docs/closeout_summary_qwen3_e4_e52.md`

## Backup Directories

- `archive/doc_backups_20260611_172718`
- `archive/paper_backups_20260611_173355`

## Final Paper Positioning

The paper should present LuxLLM-Agent as an inspectable LLM-assisted game-agent system for Lux AI Season 3. The contribution is not state-of-the-art Lux AI performance. The contribution is a stable and reproducible system pipeline combining:

1. structured LLM decision generation;
2. deterministic rule fallback;
3. cached strategy reuse;
4. replay-grounded decision traceability;
5. controlled qwen3:32b evaluation;
6. lightweight scalability simulation.

The paper should use E4 as the main controlled result and E5.2 as a supplementary ablation.
