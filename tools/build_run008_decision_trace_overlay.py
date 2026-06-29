from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


ROOT = Path(".")
FRAME_PATH = ROOT / "data" / "isometric_replay_frames_run008.json"
TRACE_PATH = ROOT / "logs" / "decision_trace.jsonl"
LLM_DECISION_PATH = ROOT / "logs" / "decision_log.jsonl"
OUT_PATH = ROOT / "data" / "run008_decision_trace_overlay.json"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8", errors="replace") as f:
        return json.load(f)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    if not path.exists():
        return rows

    with path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if isinstance(obj, dict):
                rows.append(obj)
    return rows


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def short_text(value: Any, max_len: int = 260) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False)
    else:
        text = str(value)
    text = " ".join(text.split())
    if len(text) > max_len:
        return text[: max_len - 3] + "..."
    return text


def frame_step(frame: Dict[str, Any], index: int) -> int:
    for key in ["step", "game_step", "env_step", "frame_step", "turn"]:
        if key in frame:
            return safe_int(frame.get(key), index)
    return index


def summarise_global_plan(plan: Any) -> Dict[str, str]:
    if not isinstance(plan, dict):
        return {
            "phase": "",
            "main_objective": "",
            "risk_posture": "",
            "reason": "",
        }

    return {
        "phase": short_text(plan.get("phase", ""), 120),
        "main_objective": short_text(plan.get("main_objective", ""), 160),
        "risk_posture": short_text(plan.get("risk_posture", ""), 80),
        "reason": short_text(plan.get("reason", ""), 260),
    }


def summarise_intents(intents: Any, limit: int = 4) -> List[Dict[str, Any]]:
    if not isinstance(intents, dict):
        return []

    items: List[Dict[str, Any]] = []
    for unit_id, item in list(intents.items())[:limit]:
        if not isinstance(item, dict):
            continue
        items.append(
            {
                "unit_id": str(unit_id),
                "intent": short_text(item.get("intent", ""), 100),
                "priority": item.get("priority", ""),
                "risk": short_text(item.get("risk", ""), 80),
                "expected_value": item.get("expected_value", ""),
                "target": item.get("target", None),
                "reason": short_text(item.get("reason", ""), 180),
            }
        )
    return items


def build_trace_by_step(rows: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    """
    decision_trace.jsonl may contain both player_0 and player_1 rows for the same step.
    For the overlay we prefer player_0 / team_id 0 because player_0 is the LLM-side agent
    in the controlled evidence.
    """
    grouped: Dict[int, List[Dict[str, Any]]] = {}
    for row in rows:
        step = safe_int(row.get("step", row.get("step_in_match", 0)))
        grouped.setdefault(step, []).append(row)

    out: Dict[int, Dict[str, Any]] = {}
    for step, candidates in grouped.items():
        player0 = [
            r for r in candidates
            if r.get("player") == "player_0" or r.get("team_id") == 0
        ]
        if player0:
            out[step] = player0[-1]
        else:
            out[step] = candidates[-1]
    return out


def build_llm_by_step(rows: List[Dict[str, Any]]) -> Dict[int, Dict[str, Any]]:
    out: Dict[int, Dict[str, Any]] = {}
    for row in rows:
        step = safe_int(row.get("step", row.get("step_in_match", 0)))
        out[step] = row
    return out


def nearest_previous_llm(step: int, llm_steps: List[int], llm_by_step: Dict[int, Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    prev = [s for s in llm_steps if s <= step]
    if not prev:
        return None
    return llm_by_step[max(prev)]


def main() -> None:
    replay = read_json(FRAME_PATH)

    if isinstance(replay, dict) and isinstance(replay.get("frames"), list):
        frames = replay["frames"]
        replay_meta = {
            "schema_version": replay.get("schema_version", ""),
            "builder_version": replay.get("builder_version", ""),
            "source_replay": replay.get("source_replay", ""),
            "source_decision_log": replay.get("source_decision_log", ""),
            "source_llm_decisions": replay.get("source_llm_decisions", ""),
            "frame_count": replay.get("frame_count", len(frames)),
            "first_step": replay.get("first_step", None),
            "last_step": replay.get("last_step", None),
            "final_score_team0": replay.get("final_score_team0", None),
            "final_score_team1": replay.get("final_score_team1", None),
            "winner": replay.get("winner", ""),
            "paper_result_context": replay.get("paper_result_context", None),
        }
    elif isinstance(replay, list):
        frames = replay
        replay_meta = {
            "schema_version": "",
            "builder_version": "",
            "frame_count": len(frames),
        }
    else:
        raise TypeError(f"Unsupported replay frame structure: {type(replay)}")

    trace_rows = read_jsonl(TRACE_PATH)
    llm_rows = read_jsonl(LLM_DECISION_PATH)

    trace_by_step = build_trace_by_step(trace_rows)
    llm_by_step = build_llm_by_step(llm_rows)
    llm_steps = sorted(llm_by_step.keys())

    items: List[Dict[str, Any]] = []

    for frame_index, frame in enumerate(frames):
        if not isinstance(frame, dict):
            step = frame_index
            frame_dict: Dict[str, Any] = {}
        else:
            step = frame_step(frame, frame_index)
            frame_dict = frame

        trace = trace_by_step.get(step, {})
        exact_llm = llm_by_step.get(step)
        recent_llm = nearest_previous_llm(step, llm_steps, llm_by_step)
        llm = exact_llm or recent_llm or {}

        global_plan = summarise_global_plan(llm.get("global_plan"))
        intents = summarise_intents(llm.get("intents"), limit=4)

        decision_source = short_text(trace.get("decision_source", "no_trace"), 100)
        llm_mode = short_text(trace.get("llm_mode", ""), 100)

        item = {
            "frame_index": frame_index,
            "step": step,

            "has_step_trace": bool(trace),
            "has_exact_llm_decision": exact_llm is not None,
            "has_recent_llm_decision": bool(llm),

            "player": trace.get("player", "player_0"),
            "team_id": trace.get("team_id", 0),

            "phase": short_text(trace.get("phase", global_plan.get("phase", "")), 120),
            "decision_source": decision_source,
            "llm_mode": llm_mode,
            "llm_model": short_text(trace.get("llm_model", llm.get("model", "")), 120),

            "llm_called": bool(trace.get("llm_called", False) or llm.get("fresh_llm_call", False)),
            "fresh_llm_call": bool(llm.get("fresh_llm_call", False)),
            "llm_strategy_used": bool(llm.get("llm_strategy_used", False)),
            "cached_llm_turn": bool(llm.get("cached_llm_turn", False) or trace.get("cache_used", False)),
            "stale_decision": bool(trace.get("stale_decision", False)),
            "last_llm_step": trace.get("last_llm_step", None),
            "llm_step_used": llm.get("step", None),

            "llm_valid": bool(trace.get("llm_valid", False)),
            "llm_error": short_text(trace.get("llm_error", llm.get("error", "")), 180),
            "timed_out": bool(trace.get("timed_out", False) or llm.get("timed_out", False)),
            "llm_latency_ms": safe_float(trace.get("llm_latency_ms", 0.0)),

            "fallback_used": bool(trace.get("fallback_used", False) or llm.get("fallback_used", False)),
            "fallback_reason": short_text(trace.get("fallback_reason", ""), 180),
            "action_fallback_used": bool(trace.get("action_fallback_used", False)),

            "risk_filter_enabled": bool(trace.get("risk_filter_enabled", False)),
            "risk_filter_changed": bool(trace.get("risk_filter_changed", False)),
            "risk_filter_reason": short_text(trace.get("risk_filter_reason", ""), 220),
            "risk_filter_changed_targets": trace.get("risk_filter_changed_targets", 0),
            "risk_filter_events_count": trace.get("risk_filter_events_count", 0),

            "unit_intent_count": trace.get("unit_intent_count", llm.get("unit_intent_count", 0)),
            "unit_action_count": trace.get("unit_action_count", 0),
            "active_action_count": trace.get("active_action_count", 0),

            "score_player_0": trace.get("score_player_0", replay_meta.get("final_score_team0", 0)),
            "score_player_1": trace.get("score_player_1", replay_meta.get("final_score_team1", 0)),
            "score_diff_player_0_minus_player_1": trace.get("score_diff_player_0_minus_player_1", 0),

            "global_plan": global_plan,
            "intents": intents,

            "overlay_summary": "",
        }

        if item["has_exact_llm_decision"]:
            item["overlay_summary"] = (
                f"Fresh LLM decision at step {step}: "
                f"{global_plan.get('main_objective') or 'no objective recorded'}."
            )
        elif item["has_recent_llm_decision"]:
            item["overlay_summary"] = (
                f"Using most recent LLM plan from step {item['llm_step_used']}: "
                f"{global_plan.get('main_objective') or 'no objective recorded'}."
            )
        elif item["has_step_trace"]:
            item["overlay_summary"] = (
                f"Step trace available with decision source {decision_source}; "
                f"no LLM decision log matched this step."
            )
        else:
            item["overlay_summary"] = "No trace entry matched this replay frame."

        items.append(item)

    matched_trace = sum(1 for x in items if x["has_step_trace"])
    matched_exact_llm = sum(1 for x in items if x["has_exact_llm_decision"])
    matched_recent_llm = sum(1 for x in items if x["has_recent_llm_decision"])

    output = {
        "schema": "luxllm_run008_decision_trace_overlay_v2",
        "description": "Step-aligned overlay data for the LuxLLM-Agent Run008 isometric viewer.",
        "frame_file": str(FRAME_PATH).replace("\\", "/"),
        "trace_file": str(TRACE_PATH).replace("\\", "/"),
        "llm_decision_file": str(LLM_DECISION_PATH).replace("\\", "/"),
        "replay_meta": replay_meta,
        "num_frames": len(frames),
        "num_trace_rows": len(trace_rows),
        "num_llm_decision_rows": len(llm_rows),
        "matched_step_trace_frames": matched_trace,
        "matched_exact_llm_frames": matched_exact_llm,
        "matched_recent_llm_frames": matched_recent_llm,
        "items": items,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=" * 80)
    print("Build Run008 decision trace overlay")
    print("=" * 80)
    print(f"frame file: {FRAME_PATH}")
    print(f"trace file: {TRACE_PATH}")
    print(f"llm decision file: {LLM_DECISION_PATH}")
    print(f"frames: {len(frames)}")
    print(f"trace rows: {len(trace_rows)}")
    print(f"llm decision rows: {len(llm_rows)}")
    print(f"matched step trace frames: {matched_trace}")
    print(f"matched exact llm frames: {matched_exact_llm}")
    print(f"matched recent llm frames: {matched_recent_llm}")
    print(f"output: {OUT_PATH}")


if __name__ == "__main__":
    main()
