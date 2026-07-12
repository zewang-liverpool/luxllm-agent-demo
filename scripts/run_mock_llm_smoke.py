"""Run one complete matched seed pair through a deterministic mock Ollama."""

from __future__ import annotations

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
        output_dir = ROOT / "results" / "mock_llm_role_swap_smoke"
        command = [
            sys.executable,
            str(ROOT / "scripts" / "run_paired_experiment.py"),
            "--model",
            "mock:latest",
            "--pairs",
            "1",
            "--seed-start",
            "4242",
            "--temperature",
            "0.0",
            "--ollama-base-url",
            "http://127.0.0.1:11435",
            "--output-dir",
            str(output_dir),
            "--keep-console",
            "--resume",
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
