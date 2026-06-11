# baseline_agent.py
# Simple rule-only opponent agent for local testing.
#
# It uses the same parser and action planner but disables LLM.

import os
import sys
from typing import List, Optional

from lux_state import LuxState, parse_lux_state
from state_summarizer import summarize_state
from llm_decider import rule_based_decide
from action_planner import plan_actions


_previous_state: Optional[LuxState] = None
_step = 0


def _log(message: str) -> None:
    print(f"[BaselineAgent] {message}", file=sys.stderr)


def agent_from_updates(updates: List[str]) -> List[str]:
    global _previous_state
    global _step

    state = parse_lux_state(updates, step=_step, previous_state=_previous_state)
    summary = summarize_state(state)
    decision = rule_based_decide(summary)
    actions = plan_actions(state, decision)

    _log(f"step={_step} strategy={decision.get('strategy')} actions={len(actions)}")

    _previous_state = state
    _step += 1
    return actions


def _read_turn_block() -> Optional[List[str]]:
    updates: List[str] = []

    while True:
        try:
            line = input()
        except EOFError:
            if not updates:
                return None
            return updates

        line = line.strip()
        if line in ("DONE", "D_DONE"):
            break

        updates.append(line)

    return updates


def main() -> None:
    # Force baseline to avoid accidental local LLM calls.
    os.environ["LUX_LLM_MODE"] = "rules"

    _log("Baseline started.")

    while True:
        updates = _read_turn_block()
        if updates is None:
            break

        try:
            actions = agent_from_updates(updates)
        except Exception as exc:
            _log(f"Error, returning empty actions: {exc}")
            actions = []

        print(",".join(actions), flush=True)


if __name__ == "__main__":
    main()