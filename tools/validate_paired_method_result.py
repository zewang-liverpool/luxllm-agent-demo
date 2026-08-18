"""Validate a paired DTAV or direct-prompt experiment directory."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List


EXPECTED_SETTINGS = {
    "dtav": {
        "LUX_DECISION_METHOD": "dtav",
        "LUX_NORMALIZE_LLM_OUTPUT": "1",
        "LUX_ENABLE_STRATEGY_CACHE": "1",
        "LUX_LLM_REUSE_LAST_INTENTS": "1",
        "LUX_ENABLE_RISK_AWARE_ACTION_FILTER": "1",
    },
    "direct_prompt": {
        "LUX_DECISION_METHOD": "direct_prompt",
        "LUX_NORMALIZE_LLM_OUTPUT": "0",
        "LUX_ENABLE_STRATEGY_CACHE": "0",
        "LUX_LLM_REUSE_LAST_INTENTS": "0",
        "LUX_ENABLE_RISK_AWARE_ACTION_FILTER": "0",
    },
}


def read_jsonl(path: Path, errors: List[str] | None = None) -> Iterable[Dict]:
    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = line.strip()
        if line:
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                message = f"invalid JSONL at {path}:{line_number}: {exc.msg}"
                if errors is None:
                    raise ValueError(message) from exc
                errors.append(message)


def validate_settings(metadata: Dict, expected_method: str) -> List[str]:
    errors: List[str] = []
    if metadata.get("decision_method") != expected_method:
        errors.append(
            f"environment decision_method is {metadata.get('decision_method')!r}, "
            f"expected {expected_method!r}"
        )
    actual = metadata.get("decision_method_settings", {})
    for key, value in EXPECTED_SETTINGS[expected_method].items():
        if str(actual.get(key)) != value:
            errors.append(f"{key} is {actual.get(key)!r}, expected {value!r}")
    return errors


def validate(result_dir: Path, expected_method: str) -> Dict:
    result_dir = result_dir.resolve()
    errors: List[str] = []
    environment_path = result_dir / "environment.json"
    history_path = result_dir / "match_history.jsonl"
    summary_path = result_dir / "summary.json"
    for path in (environment_path, history_path, summary_path):
        if not path.exists():
            errors.append(f"missing required file: {path.name}")
    if errors:
        return {"status": "failed", "result_dir": str(result_dir), "errors": errors}

    metadata = json.loads(environment_path.read_text(encoding="utf-8"))
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    records = list(read_jsonl(history_path, errors))
    errors.extend(validate_settings(metadata, expected_method))

    planned = int(metadata.get("planned_matches", 0))
    completed = [item for item in records if item.get("status") == "complete"]
    if len(records) != planned:
        errors.append(f"history contains {len(records)} records; planned {planned}")
    if len(completed) != planned:
        errors.append(f"only {len(completed)} of {planned} matches are complete")
    if int(summary.get("completed_matches", -1)) != len(completed):
        errors.append("summary completed_matches does not match history")

    roles_by_seed = defaultdict(set)
    for record in completed:
        roles_by_seed[int(record["seed"])].add(str(record.get("llm_player")))
        if record.get("decision_method") != expected_method:
            errors.append(
                f"record {record.get('run_id')} has method "
                f"{record.get('decision_method')!r}"
            )
    improper = {
        seed: sorted(roles)
        for seed, roles in roles_by_seed.items()
        if roles != {"player_0", "player_1"}
    }
    if improper:
        errors.append(f"improper role-swapped seed pairs: {improper}")

    # New paired runs isolate player processes under logs/player_0 and
    # logs/player_1. Recursive discovery also accepts historical flat logs.
    decision_paths = sorted(
        result_dir.glob("runs/*/logs/**/llm_decisions.jsonl")
    )
    trace_paths = sorted(
        result_dir.glob("runs/*/logs/**/decision_trace.jsonl")
    )
    llm_records = [
        record for path in decision_paths for record in read_jsonl(path, errors)
    ]
    step_records = [
        record
        for path in trace_paths
        for record in read_jsonl(path, errors)
        if record.get("event") == "agent_step_trace"
    ]
    if not llm_records:
        errors.append("no LLM decision records found")
    if not step_records:
        errors.append("no agent-step trace records found")

    wrong_llm_method = sum(
        record.get("decision_method") != expected_method for record in llm_records
    )
    wrong_step_method = sum(
        record.get("decision_method") != expected_method for record in step_records
    )
    if wrong_llm_method:
        errors.append(f"{wrong_llm_method} LLM records have the wrong method")
    if wrong_step_method:
        errors.append(f"{wrong_step_method} step records have the wrong method")

    return {
        "status": "failed" if errors else "passed",
        "result_dir": str(result_dir),
        "decision_method": expected_method,
        "completed_matches": len(completed),
        "paired_seeds_completed": sum(
            roles == {"player_0", "player_1"} for roles in roles_by_seed.values()
        ),
        "llm_decision_records": len(llm_records),
        "agent_step_records": len(step_records),
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result_dir", type=Path)
    parser.add_argument("--method", choices=sorted(EXPECTED_SETTINGS), required=True)
    args = parser.parse_args()
    result = validate(args.result_dir, args.method)
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
