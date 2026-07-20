"""Run one role-swapped LLM-versus-LLM pair with deterministic mock models."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    server = subprocess.Popen(
        [sys.executable, str(ROOT / "scripts" / "mock_ollama_server.py")],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    try:
        time.sleep(1.0)
        output_dir = ROOT / "results" / "mock_dual_llm_role_swap_smoke"
        if output_dir.exists():
            shutil.rmtree(output_dir)
        command = [
            sys.executable,
            str(ROOT / "scripts" / "run_dual_llm_experiment.py"),
            "--model-a",
            "mock-qwen:latest",
            "--model-b",
            "mock-deepseek:latest",
            "--pairs",
            "1",
            "--seed-start",
            "4343",
            "--temperature",
            "0.0",
            "--model-a-base-url",
            "http://127.0.0.1:11435",
            "--model-b-base-url",
            "http://127.0.0.1:11435",
            "--output-dir",
            str(output_dir),
            "--keep-console",
        ]
        return subprocess.run(command, cwd=ROOT).returncode
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()


if __name__ == "__main__":
    raise SystemExit(main())
