"""Compare two completed matched-seed role-swapped experiments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple

from evaluation_stats import bootstrap_role_difference, exact_binomial_pvalue, outcome_score


def load_history(path: Path) -> Dict[Tuple[int, str], Dict]:
    records: Dict[Tuple[int, str], Dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if record.get("status") != "complete":
            continue
        key = (int(record["seed"]), str(record["llm_player"]))
        records[key] = record
    return records


def compare(left: Dict, right: Dict, left_name: str, right_name: str) -> Dict:
    common_keys = sorted(set(left) & set(right))
    paired_scores: List[Tuple[float, float]] = []
    left_only_wins = 0
    right_only_wins = 0
    for key in common_keys:
        left_record = left[key]
        right_record = right[key]
        paired_scores.append((outcome_score(left_record), outcome_score(right_record)))
        left_win = left_record.get("llm_won") is True
        right_win = right_record.get("llm_won") is True
        if left_win and not right_win:
            left_only_wins += 1
        elif right_win and not left_win:
            right_only_wins += 1
    estimate, low, high = bootstrap_role_difference(paired_scores)
    discordant = left_only_wins + right_only_wins
    return {
        "left": left_name,
        "right": right_name,
        "matched_seed_role_strata": len(common_keys),
        "left_only_wins": left_only_wins,
        "right_only_wins": right_only_wins,
        "mcnemar_exact_pvalue": exact_binomial_pvalue(left_only_wins, discordant),
        "mean_outcome_score_difference_left_minus_right": estimate,
        "paired_bootstrap_95_ci": [low, high],
        "bootstrap_iterations": 10000,
        "bootstrap_seed": 42,
        "interpretation": (
            "A matched association under the recorded seed/role/model settings; "
            "not a hardware-independent causal model ranking."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("left", type=Path, help="First match_history.jsonl")
    parser.add_argument("right", type=Path, help="Second match_history.jsonl")
    parser.add_argument("--left-name", default="left")
    parser.add_argument("--right-name", default="right")
    parser.add_argument("--output", type=Path, default=Path("reports/paired_model_comparison.json"))
    args = parser.parse_args()
    result = compare(load_history(args.left), load_history(args.right), args.left_name, args.right_name)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
