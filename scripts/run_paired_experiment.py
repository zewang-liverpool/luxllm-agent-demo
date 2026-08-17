"""Run a matched-seed, role-swapped Lux AI Season 3 experiment.

Fifty seed pairs produce 100 matches: for every seed, the LLM-assisted agent
plays once as player_0 and once as player_1 against the same rule fallback.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import platform
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


ROOT = Path(__file__).resolve().parents[1]
AGENT_PATH = ROOT / "src" / "agent" / "main.py"
TOOLS_PATH = ROOT / "tools"
sys.path.insert(0, str(TOOLS_PATH))

from evaluation_stats import summarise_records  # noqa: E402


DECISION_METHODS = ("dtav", "direct_prompt")


def method_environment(method: str) -> Dict[str, str]:
    """Return the controlled feature switches for a decision method.

    Direct prompting retains the minimal action adapter and fallback required
    by the Lux runner, but removes DTAV's proposal normalization, strategy
    reuse, and risk-aware target filtering.
    """
    if method == "direct_prompt":
        return {
            "LUX_DECISION_METHOD": "direct_prompt",
            "LUX_NORMALIZE_LLM_OUTPUT": "0",
            "LUX_ENABLE_STRATEGY_CACHE": "0",
            "LUX_LLM_REUSE_LAST_INTENTS": "0",
            "LUX_ENABLE_RISK_AWARE_ACTION_FILTER": "0",
        }
    if method == "dtav":
        return {
            "LUX_DECISION_METHOD": "dtav",
            "LUX_NORMALIZE_LLM_OUTPUT": "1",
            "LUX_ENABLE_STRATEGY_CACHE": "1",
            "LUX_LLM_REUSE_LAST_INTENTS": "1",
            "LUX_ENABLE_RISK_AWARE_ACTION_FILTER": "1",
        }
    raise ValueError(f"Unsupported decision method: {method!r}")


def parse_rewards(text: str) -> Tuple[Optional[int], Optional[int]]:
    patterns = {
        "player_0": [
            r"['\"]player_0['\"]\s*:\s*array\(\s*([-+]?\d+)",
            r"['\"]player_0['\"]\s*:\s*([-+]?\d+)",
        ],
        "player_1": [
            r"['\"]player_1['\"]\s*:\s*array\(\s*([-+]?\d+)",
            r"['\"]player_1['\"]\s*:\s*([-+]?\d+)",
        ],
    }
    values: Dict[str, Optional[int]] = {"player_0": None, "player_1": None}
    for player, player_patterns in patterns.items():
        for pattern in player_patterns:
            matches = re.findall(pattern, text)
            if matches:
                values[player] = int(matches[-1])
                break
    return values["player_0"], values["player_1"]


def winner_from_rewards(player_0: int, player_1: int) -> str:
    if player_0 > player_1:
        return "player_0"
    if player_1 > player_0:
        return "player_1"
    return "draw"


def ollama_inventory(base_url: str) -> List[Dict]:
    url = base_url.rstrip("/") + "/api/tags"
    with urllib.request.urlopen(url, timeout=5) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return [item for item in payload.get("models", []) if isinstance(item, dict)]


def resolve_source_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except Exception:
        return os.environ.get("LUX_SOURCE_COMMIT", "unknown").strip() or "unknown"


def env_flag(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def runtime_metadata(args: argparse.Namespace, inventory: List[Dict]) -> Dict:
    commit = resolve_source_commit()
    try:
        freeze = subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"], text=True, stderr=subprocess.DEVNULL
        ).splitlines()
    except Exception:
        freeze = []
    try:
        ollama_version = subprocess.check_output(
            ["ollama", "--version"], text=True, stderr=subprocess.STDOUT
        ).strip()
    except Exception:
        ollama_version = "unavailable"
    return {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "git_commit": commit,
        "python": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "model": args.model,
        "decision_method": args.method,
        "decision_method_settings": method_environment(args.method),
        "ollama_base_url": args.ollama_base_url,
        "ollama_version": ollama_version,
        "ollama_models": [str(item.get("name")) for item in inventory],
        "ollama_model_inventory": inventory,
        "seed_start": args.seed_start,
        "seed_pairs": args.pairs,
        "planned_matches": args.pairs * 2,
        "temperature": args.temperature,
        "llm_num_predict": int(os.environ.get("LUX_LLM_NUM_PREDICT", "384")),
        "llm_think": env_flag("LUX_LLM_THINK", False),
        "llm_json_mode": env_flag("LUX_LLM_JSON_MODE", True),
        "llm_seed_policy": "same integer as the paired Lux environment seed",
        "pip_freeze": freeze,
    }


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


def write_summary(output_dir: Path, records: List[Dict], metadata: Dict) -> None:
    summary = summarise_records(records)
    summary["metadata"] = metadata
    (output_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def run_match(
    args: argparse.Namespace,
    output_dir: Path,
    seed: int,
    llm_player: str,
    match_index: int,
) -> Dict:
    fallback_player = "player_1" if llm_player == "player_0" else "player_0"
    run_id = f"seed_{seed}_{llm_player}"
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
            "LUX_LLM_PLAYER": llm_player,
            "LUX_FALLBACK_PLAYER": fallback_player,
            "LUX_LLM_MODEL": args.model,
            "LUX_LLM_BASE_URL": args.ollama_base_url,
            "LUX_LLM_TEMPERATURE": str(args.temperature),
            "LUX_LLM_SEED": str(seed),
            "LUX_LLM_TIMEOUT_SECONDS": str(args.timeout),
            "LUX_PRINT_AGENT_DEBUG": "0",
            # Both Lux players are separate processes. Isolated directories
            # prevent cross-process JSONL contention on Barkla's shared home
            # filesystem while retaining complete two-sided step traces.
            "LUX_SEPARATE_PLAYER_LOGS": "1",
        }
    )
    env.update(method_environment(args.method))
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
    status = "complete" if completed.returncode == 0 and player_0_reward is not None and player_1_reward is not None else "failed"
    winner = (
        winner_from_rewards(player_0_reward, player_1_reward)
        if player_0_reward is not None and player_1_reward is not None
        else "unknown"
    )
    record = {
        "run_id": run_id,
        "match_index": match_index,
        "seed": seed,
        "llm_player": llm_player,
        "fallback_player": fallback_player,
        "model": args.model,
        "decision_method": args.method,
        "status": status,
        "return_code": completed.returncode,
        "winner": winner,
        "llm_won": winner == llm_player if winner in ("player_0", "player_1") else None,
        "player_0_reward": player_0_reward,
        "player_1_reward": player_1_reward,
        "elapsed_seconds": round(time.time() - started, 3),
        "run_dir": str(run_dir.relative_to(output_dir)),
    }
    result_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.keep_console or status == "failed":
        (run_dir / "console.txt").write_text(console, encoding="utf-8")
    print(
        f"[{status}] {run_id} winner={winner} score={player_0_reward}:{player_1_reward} "
        f"elapsed={record['elapsed_seconds']}s",
        flush=True,
    )
    return record


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="qwen3:32b")
    parser.add_argument(
        "--method",
        choices=DECISION_METHODS,
        default="dtav",
        help="Full DTAV method or controlled direct-prompt comparison",
    )
    parser.add_argument("--pairs", type=int, default=50, help="Matched seeds; 50 pairs = 100 matches")
    parser.add_argument("--seed-start", type=int, default=20260701)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--ollama-base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--experiment-tag")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--save-replays", action="store_true")
    parser.add_argument("--keep-console", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.experiment_tag:
        args.experiment_tag = f"matched_seed_role_swap_{args.method}_v1"
    if args.pairs < 1:
        raise SystemExit("--pairs must be at least 1")
    if importlib.util.find_spec("luxai_runner.cli") is None:
        raise SystemExit("luxai-s3 is not installed. Run scripts/setup.ps1 or scripts/setup.sh first.")
    if not AGENT_PATH.exists():
        raise SystemExit(f"Agent entry point is missing: {AGENT_PATH}")

    try:
        inventory = ollama_inventory(args.ollama_base_url)
        models = [str(item.get("name")) for item in inventory]
    except Exception as exc:
        raise SystemExit(f"Ollama preflight failed at {args.ollama_base_url}: {exc}") from exc
    if args.model not in models and not any(name.startswith(args.model + ":") for name in models):
        raise SystemExit(f"Model {args.model!r} not found in Ollama. Available models: {models}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.output_dir or ROOT / "results" / (
        f"{timestamp}_{args.model.replace(':', '_')}_{args.method}_paired"
    )
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    history_path = output_dir / "match_history.jsonl"
    metadata_path = output_dir / "environment.json"
    metadata = runtime_metadata(args, inventory)
    if not metadata_path.exists():
        metadata_path.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    records = read_existing_records(history_path) if args.resume else []
    completed_keys = {(item.get("seed"), item.get("llm_player")) for item in records if item.get("status") == "complete"}
    match_index = len(records)
    for pair_index in range(args.pairs):
        seed = args.seed_start + pair_index
        roles = ["player_0", "player_1"] if pair_index % 2 == 0 else ["player_1", "player_0"]
        for role in roles:
            if (seed, role) in completed_keys:
                continue
            match_index += 1
            record = run_match(args, output_dir, seed, role, match_index)
            records.append(record)
            append_record(history_path, record)
            write_summary(output_dir, records, metadata)
            if record["status"] != "complete" and not args.continue_on_error:
                print("Stopping after failure. Re-run with --resume after fixing the issue.", file=sys.stderr)
                return 1

    write_summary(output_dir, records, metadata)
    print(f"Experiment complete: {output_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
