"""Validate a completed matched-role LLM-versus-LLM experiment directory."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List


def read_jsonl(path: Path) -> Iterable[Dict]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            if isinstance(item, dict):
                yield item


def validate(result_dir: Path, require_all_valid: bool = True) -> Dict:
    summary_path = result_dir / "summary.json"
    history_path = result_dir / "match_history.jsonl"
    if not summary_path.exists():
        raise ValueError(f"Missing summary: {summary_path}")
    if not history_path.exists():
        raise ValueError(f"Missing match history: {history_path}")

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    records = list(read_jsonl(history_path))
    model_a = str(summary.get("model_a", ""))
    model_b = str(summary.get("model_b", ""))
    expected_models = {model_a, model_b}
    if not model_a or not model_b or model_a == model_b:
        raise ValueError(f"Invalid model pair: {model_a!r}, {model_b!r}")

    completed = [record for record in records if record.get("status") == "complete"]
    if len(completed) != int(summary.get("completed_matches", -1)):
        raise ValueError("Completed-match count disagrees with summary.json")

    seed_roles = defaultdict(set)
    for record in completed:
        seed_roles[int(record["seed"])].add(str(record.get("model_a_player")))
        model_by_player = record.get("model_by_player", {})
        if set(model_by_player.values()) != expected_models:
            raise ValueError(
                f"{record.get('run_id')}: incorrect model routing: {model_by_player}"
            )
    complete_pairs = sum(
        roles == {"player_0", "player_1"}
        for roles in seed_roles.values()
    )
    if complete_pairs != int(summary.get("paired_seeds_completed", -1)):
        raise ValueError("Matched role-swap pair count disagrees with summary.json")

    decision_records: List[Dict] = []
    run_model_pairs = {}
    for run_dir in sorted((result_dir / "runs").glob("*")):
        paths = sorted((run_dir / "logs").rglob("llm_decisions.jsonl"))
        if not paths:
            raise ValueError(f"Missing LLM decision logs under: {run_dir / 'logs'}")
        items = [
            item
            for path in paths
            for item in read_jsonl(path)
            if item.get("llm_called")
        ]
        if not items:
            raise ValueError(f"No fresh LLM calls recorded under {run_dir / 'logs'}")
        observed = {
            (str(item.get("player")), str(item.get("model")))
            for item in items
        }
        players = {player for player, _ in observed}
        models = {model for _, model in observed}
        if players != {"player_0", "player_1"} or models != expected_models:
            raise ValueError(
                f"{run_dir.name}: expected both players and models, observed {sorted(observed)}"
            )
        run_model_pairs[run_dir.name] = sorted(observed)
        decision_records.extend(items)

    invalid = [item for item in decision_records if not item.get("llm_valid")]
    errors = [item for item in decision_records if item.get("error")]
    timeouts = [item for item in decision_records if item.get("timed_out")]
    if require_all_valid and invalid:
        reasons = Counter(
            str(item.get("fallback_reason") or "unknown")
            for item in invalid
        )
        raise ValueError(f"Invalid LLM decisions observed: {dict(reasons)}")
    if errors:
        raise ValueError(f"LLM errors observed: {len(errors)}")
    if timeouts:
        raise ValueError(f"LLM timeouts observed: {len(timeouts)}")

    by_player_model = Counter(
        (str(item.get("player")), str(item.get("model")))
        for item in decision_records
    )
    return {
        "status": "passed",
        "result_dir": str(result_dir),
        "completed_matches": len(completed),
        "paired_seeds_completed": complete_pairs,
        "model_a": model_a,
        "model_b": model_b,
        "fresh_llm_calls": len(decision_records),
        "valid_llm_calls": len(decision_records) - len(invalid),
        "invalid_llm_calls": len(invalid),
        "calls_by_player_and_model": {
            f"{player}|{model}": count
            for (player, model), count in sorted(by_player_model.items())
        },
        "validated_runs": len(run_model_pairs),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result_dir", type=Path)
    parser.add_argument(
        "--allow-invalid",
        action="store_true",
        help="Report invalid structured decisions without failing validation.",
    )
    args = parser.parse_args()
    report = validate(
        args.result_dir.resolve(),
        require_all_valid=not args.allow_invalid,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
