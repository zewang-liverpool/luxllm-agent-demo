"""Run a matched-seed, role-swapped LLM-versus-LLM Lux experiment.

For every environment seed, model A plays once as player_0 and once as
player_1 against model B. Both agents retain independent model routing,
strategy caches, fallback state, and player-labelled decision traces.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


ROOT = Path(__file__).resolve().parents[1]
AGENT_PATH = ROOT / "src" / "agent" / "main.py"
TOOLS_PATH = ROOT / "tools"
sys.path.insert(0, str(TOOLS_PATH))

from evaluation_stats import summarise_records  # noqa: E402
from run_paired_experiment import (  # noqa: E402
    env_flag,
    ollama_inventory,
    parse_rewards,
    resolve_source_commit,
    winner_from_rewards,
)


def model_available(model: str, inventory: List[Dict]) -> bool:
    names = [str(item.get("name", "")) for item in inventory]
    return model in names or any(name.startswith(model + ":") for name in names)


def read_existing_records(history_path: Path) -> List[Dict]:
    records = []
    if not history_path.exists():
        return records
    for line in history_path.read_text(encoding="utf-8").splitlines():
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return records


def append_record(history_path: Path, record: Dict) -> None:
    with history_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def summarise_dual_records(records: List[Dict], model_a: str, model_b: str) -> Dict:
    """Return model-labelled statistics while reusing the paired estimator."""
    paired = summarise_records(records)
    completed = [record for record in records if record.get("status") == "complete"]
    winner_models = Counter(record.get("winner_model", "unknown") for record in completed)
    return {
        "experiment_type": "matched_seed_role_swapped_llm_vs_llm",
        "model_a": model_a,
        "model_b": model_b,
        "total_records": paired["total_records"],
        "completed_matches": paired["completed_matches"],
        "paired_seeds_completed": paired["paired_seeds_completed"],
        "winner_model_counts": dict(winner_models),
        "model_a_wins": paired["llm_wins"],
        "model_a_losses": paired["llm_losses"],
        "draws": paired["draws"],
        "model_a_win_rate": paired["llm_win_rate"],
        "model_a_win_rate_wilson_95_ci": paired["llm_win_rate_wilson_95_ci"],
        "exact_binomial_pvalue_vs_0_5": paired["exact_binomial_pvalue_vs_0_5"],
        "by_model_a_role": paired["by_llm_role"],
        "matched_seed_performance": paired["matched_seed_performance"],
        "matched_role_analysis": paired["matched_role_analysis"],
    }


def write_summary(
    output_dir: Path,
    records: List[Dict],
    metadata: Dict,
    model_a: str,
    model_b: str,
) -> None:
    summary = summarise_dual_records(records, model_a=model_a, model_b=model_b)
    summary["metadata"] = metadata
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def runtime_metadata(
    args: argparse.Namespace,
    inventory_a: List[Dict],
    inventory_b: List[Dict],
) -> Dict:
    try:
        freeze = subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).splitlines()
    except Exception:
        freeze = []
    try:
        ollama_version = subprocess.check_output(
            ["ollama", "--version"],
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()
    except Exception:
        ollama_version = "unavailable"
    return {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": resolve_source_commit(),
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "experiment_type": "matched_seed_role_swapped_llm_vs_llm",
        "model_a": args.model_a,
        "model_b": args.model_b,
        "model_a_base_url": args.model_a_base_url,
        "model_b_base_url": args.model_b_base_url,
        "ollama_version": ollama_version,
        "model_a_inventory": inventory_a,
        "model_b_inventory": inventory_b,
        "seed_start": args.seed_start,
        "seed_pairs": args.pairs,
        "planned_matches": args.pairs * 2,
        "temperature": args.temperature,
        "llm_num_predict": int(os.environ.get("LUX_LLM_NUM_PREDICT", "384")),
        "llm_think": env_flag("LUX_LLM_THINK", False),
        "llm_json_mode": env_flag("LUX_LLM_JSON_MODE", True),
        "llm_seed_policy": "same integer as the matched Lux environment seed",
        "role_swap_policy": "model A plays both player_0 and player_1 per seed",
        "pip_freeze": freeze,
    }


def run_match(
    args: argparse.Namespace,
    output_dir: Path,
    seed: int,
    model_a_player: str,
    match_index: int,
) -> Dict:
    model_b_player = "player_1" if model_a_player == "player_0" else "player_0"
    model_by_player = {
        model_a_player: args.model_a,
        model_b_player: args.model_b,
    }
    base_url_by_player = {
        model_a_player: args.model_a_base_url,
        model_b_player: args.model_b_base_url,
    }
    run_id = f"seed_{seed}_model_a_{model_a_player}"
    run_dir = output_dir / "runs" / run_id
    run_dir.mkdir(parents=True, exist_ok=True)
    result_path = run_dir / "result.json"
    if args.resume and result_path.exists():
        existing = json.loads(result_path.read_text(encoding="utf-8"))
        if existing.get("status") == "complete":
            print(f"[resume] {run_id}", flush=True)
            return existing

    env = os.environ.copy()
    env.update(
        {
            "LUX_RUN_DIR": str(run_dir.resolve()),
            "LUX_EXPERIMENT_TAG": args.experiment_tag,
            "LUX_LLM_ENABLED": "1",
            "LUX_FORCE_RULE_ONLY": "0",
            "LUX_FORCE_FALLBACK": "0",
            "LUX_LLM_PLAYERS": "player_0,player_1",
            "LUX_PLAYER_0_LLM_ENABLED": "1",
            "LUX_PLAYER_1_LLM_ENABLED": "1",
            "LUX_PLAYER_0_LLM_MODEL": model_by_player["player_0"],
            "LUX_PLAYER_1_LLM_MODEL": model_by_player["player_1"],
            "LUX_PLAYER_0_LLM_BASE_URL": base_url_by_player["player_0"],
            "LUX_PLAYER_1_LLM_BASE_URL": base_url_by_player["player_1"],
            "LUX_LLM_MODEL": args.model_a,
            "LUX_LLM_TEMPERATURE": str(args.temperature),
            "LUX_LLM_SEED": str(seed),
            "LUX_LLM_TIMEOUT_SECONDS": str(args.timeout),
            "LUX_PRINT_AGENT_DEBUG": "0",
        }
    )
    command = [
        sys.executable,
        "-m",
        "luxai_runner.cli",
        str(AGENT_PATH),
        str(AGENT_PATH),
        "--seed",
        str(seed),
        "--verbose",
        "1",
    ]
    if args.save_replays:
        command.extend(["--output", str(run_dir / "replay.json")])

    started = time.time()
    completed = subprocess.run(
        command,
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    console = completed.stdout
    player_0_reward, player_1_reward = parse_rewards(console)
    status = (
        "complete"
        if completed.returncode == 0
        and player_0_reward is not None
        and player_1_reward is not None
        else "failed"
    )
    winner = (
        winner_from_rewards(player_0_reward, player_1_reward)
        if player_0_reward is not None and player_1_reward is not None
        else "unknown"
    )
    if winner == model_a_player:
        winner_model = args.model_a
    elif winner == model_b_player:
        winner_model = args.model_b
    elif winner == "draw":
        winner_model = "draw"
    else:
        winner_model = "unknown"

    record = {
        "run_id": run_id,
        "match_index": match_index,
        "seed": seed,
        "status": status,
        "return_code": completed.returncode,
        "winner": winner,
        "winner_model": winner_model,
        "player_0_reward": player_0_reward,
        "player_1_reward": player_1_reward,
        "model_a": args.model_a,
        "model_b": args.model_b,
        "model_a_player": model_a_player,
        "model_b_player": model_b_player,
        "model_by_player": model_by_player,
        "llm_player": model_a_player,
        "llm_won": winner == model_a_player if winner in ("player_0", "player_1") else None,
        "elapsed_seconds": round(time.time() - started, 3),
        "run_dir": str(run_dir.relative_to(output_dir)),
    }
    result_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if args.keep_console or status == "failed":
        (run_dir / "console.txt").write_text(console, encoding="utf-8")
    print(
        f"[{status}] {run_id} winner={winner_model} "
        f"score={player_0_reward}:{player_1_reward} "
        f"elapsed={record['elapsed_seconds']}s",
        flush=True,
    )
    return record


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-a", default="qwen3:32b")
    parser.add_argument("--model-b", default="deepseek-r1:32b")
    parser.add_argument(
        "--pairs",
        type=int,
        default=1,
        help="Matched seeds; 1 pair = 2 role-swapped games",
    )
    parser.add_argument("--seed-start", type=int, default=20260701)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument(
        "--model-a-base-url",
        default="http://127.0.0.1:11434",
    )
    parser.add_argument(
        "--model-b-base-url",
        default="http://127.0.0.1:11434",
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument(
        "--experiment-tag",
        default="dual_llm_matched_role_swap_v1",
    )
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--save-replays", action="store_true")
    parser.add_argument("--keep-console", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.pairs < 1:
        raise SystemExit("--pairs must be at least 1")
    if args.model_a == args.model_b:
        raise SystemExit("--model-a and --model-b must be different for this comparison")
    if importlib.util.find_spec("luxai_runner.cli") is None:
        raise SystemExit(
            "luxai-s3 is not installed. Run scripts/setup.ps1 or scripts/setup.sh first."
        )
    if not AGENT_PATH.exists():
        raise SystemExit(f"Agent entry point is missing: {AGENT_PATH}")

    try:
        inventory_a = ollama_inventory(args.model_a_base_url)
        inventory_b = (
            inventory_a
            if args.model_b_base_url == args.model_a_base_url
            else ollama_inventory(args.model_b_base_url)
        )
    except Exception as exc:
        raise SystemExit(f"Ollama preflight failed: {exc}") from exc
    if not model_available(args.model_a, inventory_a):
        names = [str(item.get("name")) for item in inventory_a]
        raise SystemExit(f"Model A {args.model_a!r} not found. Available models: {names}")
    if not model_available(args.model_b, inventory_b):
        names = [str(item.get("name")) for item in inventory_b]
        raise SystemExit(f"Model B {args.model_b!r} not found. Available models: {names}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.output_dir or (
        ROOT
        / "results"
        / f"{timestamp}_{args.model_a.replace(':', '_')}_vs_{args.model_b.replace(':', '_')}"
    )
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    history_path = output_dir / "match_history.jsonl"
    metadata_path = output_dir / "environment.json"
    metadata = runtime_metadata(args, inventory_a, inventory_b)
    if not metadata_path.exists():
        metadata_path.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    else:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    records = read_existing_records(history_path) if args.resume else []
    completed_keys = {
        (item.get("seed"), item.get("model_a_player"))
        for item in records
        if item.get("status") == "complete"
    }
    match_index = len(records)
    for pair_index in range(args.pairs):
        seed = args.seed_start + pair_index
        roles = (
            ["player_0", "player_1"]
            if pair_index % 2 == 0
            else ["player_1", "player_0"]
        )
        for role in roles:
            if (seed, role) in completed_keys:
                continue
            match_index += 1
            record = run_match(args, output_dir, seed, role, match_index)
            records.append(record)
            append_record(history_path, record)
            write_summary(
                output_dir,
                records,
                metadata,
                model_a=args.model_a,
                model_b=args.model_b,
            )
            if record["status"] != "complete" and not args.continue_on_error:
                print(
                    "Stopping after failure. Re-run with --resume after fixing the issue.",
                    file=sys.stderr,
                )
                return 1

    write_summary(
        output_dir,
        records,
        metadata,
        model_a=args.model_a,
        model_b=args.model_b,
    )
    print(f"Experiment complete: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
