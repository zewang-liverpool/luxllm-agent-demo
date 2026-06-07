"""
record_match_result_from_console.py

Record Lux S3 match result from console log and decision logs.

This script parses:
- match_console_xxx.txt
- latest_match_console.txt
- decision_log.jsonl
- llm_error_log.jsonl, if it exists

It supports the v0.8-M decision log schema:
{
    "event": "llm_decision",
    "fresh_llm_call": true,
    "llm_strategy_used": true,
    "cached_llm_turn": false,
    "event_refresh": false,
    "safety_override": false,
    "fallback_used": false,
    "timed_out": false,
    "error": ""
}
"""

import argparse
import ast
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
REPLAY_DIR = os.path.join(PROJECT_ROOT, "replays")

DEFAULT_CONSOLE_LOG = os.path.join(LOG_DIR, "latest_match_console.txt")
DEFAULT_DECISION_LOG = os.path.join(LOG_DIR, "decision_log.jsonl")
DEFAULT_ERROR_LOG = os.path.join(LOG_DIR, "llm_error_log.jsonl")
DEFAULT_HISTORY_LOG = os.path.join(LOG_DIR, "match_history.jsonl")


def ensure_dirs() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(REPLAY_DIR, exist_ok=True)


def read_text(path: str) -> str:
    """
    Read text robustly.

    PowerShell Tee-Object can write different encodings depending on the shell
    version. This function tries multiple decoders and also removes NUL chars.
    """
    if not path or not os.path.exists(path):
        return ""

    with open(path, "rb") as f:
        data = f.read()

    if not data:
        return ""

    encodings = [
        "utf-8-sig",
        "utf-16",
        "utf-16-le",
        "utf-16-be",
        "gbk",
        "latin-1",
    ]

    best_text = ""

    for encoding in encodings:
        try:
            text = data.decode(encoding, errors="replace")
            if len(text) > len(best_text):
                best_text = text
            if "Rewards:" in text or "Time Elapsed:" in text:
                best_text = text
                break
        except Exception:
            continue

    best_text = best_text.replace("\x00", "")
    best_text = re.sub(r"\x1b\[[0-9;]*m", "", best_text)
    return best_text


def iter_jsonl(path: str) -> List[Dict]:
    records = []

    if not path or not os.path.exists(path):
        return records

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            try:
                records.append(json.loads(line))
            except Exception:
                continue

    return records


def parse_rewards_from_console(console_text: str) -> Tuple[Optional[int], Optional[int], str]:
    """
    Parse rewards from console output.

    Supported examples:
    Rewards:  {'player_0': array(5, dtype=int32), 'player_1': array(0, dtype=int32)}
    Rewards: {'player_0': 5, 'player_1': 0}
    """
    if not console_text:
        return None, None, "console_missing"

    text = console_text.replace("\x00", "")
    text = re.sub(r"\x1b\[[0-9;]*m", "", text)

    # Most robust direct regex: search across the whole file, not per-line only.
    player_0_patterns = [
        r"'player_0'\s*:\s*array\(\s*([-+]?\d+)",
        r'"player_0"\s*:\s*array\(\s*([-+]?\d+)',
        r"'player_0'\s*:\s*([-+]?\d+)",
        r'"player_0"\s*:\s*([-+]?\d+)',
    ]

    player_1_patterns = [
        r"'player_1'\s*:\s*array\(\s*([-+]?\d+)",
        r'"player_1"\s*:\s*array\(\s*([-+]?\d+)',
        r"'player_1'\s*:\s*([-+]?\d+)",
        r'"player_1"\s*:\s*([-+]?\d+)',
    ]

    player_0_reward = None
    player_1_reward = None

    for pattern in player_0_patterns:
        match = re.search(pattern, text, flags=re.DOTALL)
        if match:
            player_0_reward = int(match.group(1))
            break

    for pattern in player_1_patterns:
        match = re.search(pattern, text, flags=re.DOTALL)
        if match:
            player_1_reward = int(match.group(1))
            break

    if player_0_reward is not None and player_1_reward is not None:
        return player_0_reward, player_1_reward, "console_rewards_line"

    # Fallback: find the Rewards line and normalize array(...) into plain ints.
    reward_line = None
    for line in text.splitlines():
        if "Rewards:" in line:
            reward_line = line.strip()

    if not reward_line:
        return None, None, "rewards_line_missing"

    try:
        raw = reward_line.split("Rewards:", 1)[1].strip()
        raw = re.sub(r"array\(\s*([-+]?\d+)\s*,\s*dtype=\w+\s*\)", r"\1", raw)
        parsed = ast.literal_eval(raw)

        return int(parsed.get("player_0")), int(parsed.get("player_1")), "console_rewards_line"
    except Exception:
        return None, None, "rewards_parse_failed"


def parse_match_id(console_text: str, fallback: str = "") -> str:
    text = console_text.replace("\x00", "")

    patterns = [
        r"Match ID:\s*\n\s*([0-9_]+)",
        r"Match ID\s*:\s*([0-9_]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.DOTALL)
        if match:
            return match.group(1).strip()

    if fallback:
        return fallback

    return datetime.now().strftime("%Y%m%d_%H%M%S")


def parse_replay_path(console_text: str, fallback: str = "") -> str:
    text = console_text.replace("\x00", "")

    patterns = [
        r"Replay output:\s*\n\s*(.+?\.html)",
        r"Replay\s*:\s*(.+?\.html)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, flags=re.DOTALL)
        if match:
            return match.group(1).strip()

    return fallback


def detect_winner(player_0_reward: Optional[int], player_1_reward: Optional[int]) -> str:
    if player_0_reward is None or player_1_reward is None:
        return "unknown"

    if player_0_reward > player_1_reward:
        return "player_0"

    if player_1_reward > player_0_reward:
        return "player_1"

    return "draw"


def categorize_error(error_text: str, timed_out: bool = False) -> str:
    text = (error_text or "").lower()

    if timed_out or "timed out" in text or "timeout" in text:
        return "timeout"

    if "connection refused" in text:
        return "connection_refused"

    if "urlopen error" in text:
        return "connection_error"

    if "json" in text or "parse" in text:
        return "parse_error"

    if not text:
        return "unknown"

    return "unknown"


def summarize_decision_records(records: List[Dict]) -> Dict:
    fresh_llm_calls = 0
    llm_strategy_used = 0
    cached_llm_turns = 0
    event_refresh = 0
    safety_override = 0
    fallback_count = 0
    llm_errors = 0
    error_categories: Dict[str, int] = {}

    for record in records:
        event = record.get("event", "")

        if bool(record.get("fresh_llm_call", False)):
            fresh_llm_calls += 1

        if bool(record.get("llm_strategy_used", False)):
            llm_strategy_used += 1

        if bool(record.get("cached_llm_turn", False)):
            cached_llm_turns += 1

        if bool(record.get("event_refresh", False)):
            event_refresh += 1

        if bool(record.get("safety_override", False)):
            safety_override += 1

        if bool(record.get("fallback_used", False)):
            fallback_count += 1

        if event in ("fresh_llm_call", "llm_fresh_call"):
            fresh_llm_calls += 1

        if event in ("llm_strategy_used", "strategy_used"):
            llm_strategy_used += 1

        if event in ("cached_llm_turn", "reuse_cached_llm_intents"):
            cached_llm_turns += 1

        if event in ("event_refresh", "llm_event_refresh"):
            event_refresh += 1

        if event in ("safety_override", "rule_safety_override"):
            safety_override += 1

        if event in ("fallback", "fallback_used", "rule_fallback"):
            fallback_count += 1

        error_text = str(record.get("error", "") or "")
        timed_out = bool(record.get("timed_out", False))

        if error_text or timed_out or event in ("llm_error", "error"):
            llm_errors += 1
            category = record.get("category") or categorize_error(error_text, timed_out)
            error_categories[category] = error_categories.get(category, 0) + 1

    return {
        "fresh_llm_calls": fresh_llm_calls,
        "llm_strategy_used": llm_strategy_used,
        "cached_llm_turns": cached_llm_turns,
        "event_refresh": event_refresh,
        "safety_override": safety_override,
        "fallback_count": fallback_count,
        "llm_errors": llm_errors,
        "error_categories": error_categories,
    }


def summarize_error_records(records: List[Dict]) -> Dict:
    llm_errors = 0
    error_categories: Dict[str, int] = {}

    for record in records:
        llm_errors += 1

        error_text = str(record.get("error", "") or "")
        timed_out = bool(record.get("timed_out", False))
        category = record.get("category") or categorize_error(error_text, timed_out)

        error_categories[category] = error_categories.get(category, 0) + 1

    return {
        "llm_errors": llm_errors,
        "error_categories": error_categories,
    }


def merge_error_summaries(decision_summary: Dict, error_summary: Dict) -> Dict:
    merged = dict(decision_summary)

    explicit_errors = int(error_summary.get("llm_errors", 0))
    if explicit_errors <= 0:
        return merged

    merged["llm_errors"] = max(int(merged.get("llm_errors", 0)), explicit_errors)

    categories = dict(merged.get("error_categories", {}))
    for key, value in error_summary.get("error_categories", {}).items():
        categories[key] = max(categories.get(key, 0), value)

    merged["error_categories"] = categories
    return merged


def build_history_record(
    match_id: str,
    winner: str,
    player_0_reward: Optional[int],
    player_1_reward: Optional[int],
    score_source: str,
    replay_path: str,
    llm_player: str,
    llm_model: str,
    decision_summary: Dict,
) -> Dict:
    return {
        "time": datetime.now().isoformat(timespec="seconds"),
        "match_id": match_id,
        "score_source": score_source,
        "winner": winner,
        "player_0_reward": player_0_reward,
        "player_1_reward": player_1_reward,
        "llm_player": llm_player,
        "llm_model": llm_model,
        "fresh_llm_calls": decision_summary.get("fresh_llm_calls", 0),
        "llm_strategy_used": decision_summary.get("llm_strategy_used", 0),
        "cached_llm_turns": decision_summary.get("cached_llm_turns", 0),
        "event_refresh": decision_summary.get("event_refresh", 0),
        "safety_override": decision_summary.get("safety_override", 0),
        "fallback_count": decision_summary.get("fallback_count", 0),
        "llm_errors": decision_summary.get("llm_errors", 0),
        "error_categories": decision_summary.get("error_categories", {}),
        "replay": replay_path,
    }


def append_history(path: str, record: Dict) -> None:
    ensure_dirs()

    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def print_summary(record: Dict) -> None:
    print("========================================================================")
    print("Match result recorded.")
    print("========================================================================")
    print(f"Match ID          : {record.get('match_id')}")
    print(f"Score source      : {record.get('score_source')}")
    print(f"Winner            : {record.get('winner')}")
    print(f"player_0 reward   : {record.get('player_0_reward')}")
    print(f"player_1 reward   : {record.get('player_1_reward')}")
    print(f"LLM player        : {record.get('llm_player')}")
    print(f"LLM model         : {record.get('llm_model')}")
    print(f"Fresh LLM calls   : {record.get('fresh_llm_calls')}")
    print(f"LLM strategy used : {record.get('llm_strategy_used')}")
    print(f"Cached LLM turns  : {record.get('cached_llm_turns')}")
    print(f"Event refresh     : {record.get('event_refresh')}")
    print(f"Safety override   : {record.get('safety_override')}")
    print(f"Fallback count    : {record.get('fallback_count')}")
    print(f"LLM errors        : {record.get('llm_errors')}")
    print(f"Error categories  : {record.get('error_categories')}")
    print(f"Replay            : {record.get('replay')}")
    print("========================================================================")


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--match-id", default="")
    parser.add_argument("--console-log", default=DEFAULT_CONSOLE_LOG)
    parser.add_argument("--decision-log", default=DEFAULT_DECISION_LOG)
    parser.add_argument("--error-log", default=DEFAULT_ERROR_LOG)
    parser.add_argument("--history-log", default=DEFAULT_HISTORY_LOG)
    parser.add_argument("--replay", default="")
    parser.add_argument("--llm-player", default="player_0")
    parser.add_argument("--llm-model", default="qwen2.5:1.5b")

    return parser.parse_args()


def main() -> None:
    ensure_dirs()
    args = parse_args()

    console_text = read_text(args.console_log)

    match_id = parse_match_id(console_text, fallback=args.match_id)
    replay_path = parse_replay_path(console_text, fallback=args.replay)

    player_0_reward, player_1_reward, score_source = parse_rewards_from_console(console_text)
    winner = detect_winner(player_0_reward, player_1_reward)

    decision_records = iter_jsonl(args.decision_log)
    error_records = iter_jsonl(args.error_log)

    decision_summary = summarize_decision_records(decision_records)
    error_summary = summarize_error_records(error_records)
    decision_summary = merge_error_summaries(decision_summary, error_summary)

    history_record = build_history_record(
        match_id=match_id,
        winner=winner,
        player_0_reward=player_0_reward,
        player_1_reward=player_1_reward,
        score_source=score_source,
        replay_path=replay_path,
        llm_player=args.llm_player,
        llm_model=args.llm_model,
        decision_summary=decision_summary,
    )

    append_history(args.history_log, history_record)
    print_summary(history_record)


if __name__ == "__main__":
    main()