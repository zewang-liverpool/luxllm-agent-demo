"""
main.py

Official-compatible entry point for Lux AI Season 3 Python agent.

Important:
- Do not import numpy here.
- stdout must ONLY print valid JSON actions.
- Debug information must go to stderr or log files.
"""

import json
import os
import sys
from argparse import Namespace
from typing import Any, Dict

from agent import Agent


agent_dict = {}


def from_json(state: Any):
    """
    Keep JSON data as normal Python lists/dicts.

    This project intentionally avoids numpy in main.py because the Lux runner
    subprocess may not have numpy available in the same environment.
    """
    if isinstance(state, dict):
        return {k: from_json(v) for k, v in state.items()}
    if isinstance(state, list):
        return [from_json(v) for v in state]
    return state


def to_json(obj: Any):
    """
    Convert action output into JSON-safe Python objects.
    """
    if isinstance(obj, dict):
        return {k: to_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [to_json(v) for v in obj]
    if isinstance(obj, tuple):
        return [to_json(v) for v in obj]

    try:
        if hasattr(obj, "tolist"):
            return obj.tolist()
    except Exception:
        pass

    try:
        if hasattr(obj, "item"):
            return obj.item()
    except Exception:
        pass

    return obj


def agent_fn(observation, configurations: Dict):
    """
    Official Lux-compatible agent function.
    """
    global agent_dict

    obs = observation.obs
    if isinstance(obs, str):
        obs = json.loads(obs)

    step = int(observation.step)
    player = observation.player
    remaining_overage_time = observation.remainingOverageTime

    if step == 0 or player not in agent_dict:
        agent_dict[player] = Agent(player, configurations["env_cfg"])

    if "__raw_path__" in configurations:
        dirname = os.path.dirname(configurations["__raw_path__"])
    else:
        dirname = os.path.dirname(__file__)

    abs_dirname = os.path.abspath(dirname)
    if abs_dirname not in sys.path:
        sys.path.append(abs_dirname)

    agent = agent_dict[player]

    actions = agent.act(
        step=step,
        obs=from_json(obs),
        remainingOverageTime=remaining_overage_time,
    )

    return {"action": to_json(actions)}


def read_input():
    """
    Read one JSON line from stdin.
    """
    try:
        return input()
    except EOFError as eof:
        raise SystemExit(eof)


if __name__ == "__main__":
    env_cfg = None
    i = 0

    while True:
        inputs = read_input()
        raw_input = json.loads(inputs)

        observation = Namespace(
            step=raw_input["step"],
            obs=raw_input["obs"],
            remainingOverageTime=raw_input["remainingOverageTime"],
            player=raw_input["player"],
            info=raw_input["info"],
        )

        if i == 0:
            env_cfg = raw_input["info"]["env_cfg"]

        i += 1

        actions = agent_fn(observation, {"env_cfg": env_cfg})

        # stdout must only contain valid JSON.
        print(json.dumps(actions), flush=True)