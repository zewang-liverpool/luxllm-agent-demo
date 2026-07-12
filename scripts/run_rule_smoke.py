"""Run one deterministic rule-only Lux S3 match without Ollama."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "src" / "agent" / "main.py"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_paired_experiment import parse_rewards, winner_from_rewards  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    try:
        runner_available = importlib.util.find_spec("luxai_runner.cli") is not None
    except ModuleNotFoundError:
        runner_available = False
    if not runner_available:
        raise SystemExit("luxai-s3 is not installed. Run scripts/setup.ps1 or scripts/setup.sh first.")

    output_dir = (args.output_dir or ROOT / "results" / f"smoke_{datetime.now():%Y%m%d_%H%M%S}").resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        {
            "LUX_RUN_DIR": str(output_dir),
            "LUX_EXPERIMENT_TAG": "rule_only_smoke",
            "LUX_FORCE_RULE_ONLY": "1",
            "LUX_LLM_ENABLED": "0",
            "LUX_PRINT_AGENT_DEBUG": "0",
        }
    )
    command = [
        sys.executable,
        "-m",
        "luxai_runner.cli",
        str(AGENT),
        str(AGENT),
        "--seed",
        str(args.seed),
        "--verbose",
        "1",
    ]
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
    (output_dir / "console.txt").write_text(completed.stdout, encoding="utf-8")
    player_0, player_1 = parse_rewards(completed.stdout)
    result = {
        "status": "complete" if completed.returncode == 0 and player_0 is not None and player_1 is not None else "failed",
        "seed": args.seed,
        "return_code": completed.returncode,
        "player_0_reward": player_0,
        "player_1_reward": player_1,
        "winner": winner_from_rewards(player_0, player_1) if player_0 is not None and player_1 is not None else "unknown",
    }
    (output_dir / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
