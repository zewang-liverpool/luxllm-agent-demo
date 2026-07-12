"""Run dependency-free repository checks, then the unit-test suite."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = [ROOT / "src" / "agent", ROOT / "src" / "viewer_tools", ROOT / "scripts", ROOT / "tools", ROOT / "tests"]


def compile_sources() -> None:
    failures = []
    for directory in SOURCE_DIRS:
        for path in sorted(directory.glob("*.py")):
            try:
                compile(path.read_text(encoding="utf-8-sig"), str(path), "exec")
            except Exception as exc:
                failures.append(f"{path.relative_to(ROOT)}: {exc}")
    if failures:
        raise SystemExit("Python compilation failed:\n" + "\n".join(failures))


def validate_demo_data() -> None:
    frames_path = ROOT / "data" / "isometric_replay_frames.json"
    trace_path = ROOT / "data" / "run008_decision_trace_overlay.json"
    viewer_path = ROOT / "docs" / "viewers" / "s3_isometric_battle_viewer_v09n12d_trace_overlay.html"
    frames = json.loads(frames_path.read_text(encoding="utf-8"))
    trace = json.loads(trace_path.read_text(encoding="utf-8"))
    frame_items = frames.get("frames", frames) if isinstance(frames, dict) else frames
    trace_items = trace.get("items", trace.get("trace", trace.get("frames", trace))) if isinstance(trace, dict) else trace
    if not isinstance(frame_items, list) or len(frame_items) < 500:
        raise SystemExit(f"Unexpected replay frame count: {len(frame_items) if isinstance(frame_items, list) else 'invalid'}")
    if not isinstance(trace_items, list) or len(trace_items) < 500:
        raise SystemExit(f"Unexpected decision trace count: {len(trace_items) if isinstance(trace_items, list) else 'invalid'}")
    viewer = viewer_path.read_text(encoding="utf-8")
    for required in ("isometric_replay_frames.json", "run008_decision_trace_overlay.json"):
        if required not in viewer:
            raise SystemExit(f"Viewer does not reference {required}")


def run_tests() -> int:
    env = os.environ.copy()
    paths = [str(ROOT / "src" / "agent"), str(ROOT / "src" / "viewer_tools"), str(ROOT / "tools"), str(ROOT / "scripts")]
    env["PYTHONPATH"] = os.pathsep.join(paths + ([env["PYTHONPATH"]] if env.get("PYTHONPATH") else []))
    completed = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT,
        env=env,
    )
    return completed.returncode


def main() -> int:
    compile_sources()
    validate_demo_data()
    return run_tests()


if __name__ == "__main__":
    raise SystemExit(main())
