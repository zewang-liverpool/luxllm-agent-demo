"""Recompute dissertation-facing rates and confidence intervals from tracked evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Tuple

from evaluation_stats import exact_binomial_pvalue, wilson_interval


ROOT = Path(__file__).resolve().parents[1]
QWEN_PATH = ROOT / "docs" / "demo_evidence" / "hpc_qwen3_32b_50run" / "hpc_qwen3_32b_multirun_summary.json"
DEEPSEEK_PATH = (
    ROOT
    / "docs"
    / "demo_evidence"
    / "hpc_deepseek_r1_32b_50run"
    / "20260624_152843_deepseek_r1_32b_gpu_50run_job9189419"
    / "summary_50run.json"
)


def extract_counts(path: Path) -> Tuple[int, int, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if "total_matches" in data:
        return int(data["player_0_wins"]), int(data["player_1_wins"]), int(data.get("draws", 0))
    counts: Dict[str, int] = {str(key): int(value) for key, value in data["winner_counts"].items()}
    return counts.get("player_0", 0), counts.get("player_1", 0), counts.get("draw", counts.get("draws", 0))


def model_summary(name: str, path: Path) -> Dict:
    player_0_wins, player_1_wins, draws = extract_counts(path)
    total = player_0_wins + player_1_wins + draws
    low, high = wilson_interval(player_0_wins, total)
    return {
        "model": name,
        "source": str(path.relative_to(ROOT)).replace("\\", "/"),
        "llm_role": "player_0",
        "matches": total,
        "llm_wins": player_0_wins,
        "rule_wins": player_1_wins,
        "draws": draws,
        "llm_win_rate": player_0_wins / total,
        "llm_win_rate_wilson_95_ci": [low, high],
        "exact_binomial_pvalue_vs_0_5": exact_binomial_pvalue(player_0_wins, total),
        "interpretation_limit": "Historical fixed-player evidence; not a matched-seed model comparison.",
    }


def main() -> None:
    results = {
        "schema": "luxllm_reported_metrics_v1",
        "results": [
            model_summary("qwen3:32b", QWEN_PATH),
            model_summary("deepseek-r1:32b", DEEPSEEK_PATH),
        ],
        "comparison_warning": (
            "The two historical runs were not matched by seed or swapped by player role. "
            "Their confidence intervals describe each fixed-player run and do not establish a causal model ranking."
        ),
    }
    json_path = ROOT / "reports" / "recomputed_metrics.json"
    markdown_path = ROOT / "reports" / "recomputed_metrics.md"
    json_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    lines = [
        "# Recomputed Historical Metrics",
        "",
        "Generated deterministically by `tools/recompute_reported_metrics.py` from tracked JSON evidence.",
        "",
        "| Model | Matches | LLM wins | Win rate | Wilson 95% CI | Exact binomial p vs 0.5 |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in results["results"]:
        low, high = item["llm_win_rate_wilson_95_ci"]
        lines.append(
            f"| {item['model']} | {item['matches']} | {item['llm_wins']} | "
            f"{item['llm_win_rate']:.1%} | [{low:.1%}, {high:.1%}] | "
            f"{item['exact_binomial_pvalue_vs_0_5']:.6f} |"
        )
    lines.extend(
        [
            "",
            "> These historical experiments kept the LLM as `player_0` and were not matched by seed. "
            "The intervals are valid descriptive summaries of each run, not evidence of a causal model ranking.",
            "",
        ]
    )
    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    print(json_path)
    print(markdown_path)


if __name__ == "__main__":
    main()
