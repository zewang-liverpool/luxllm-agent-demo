"""
rule_policy.py

Rule-only fallback policy for Lux S3.

This module is intentionally simple. The main action conversion is handled by
action_planner.py. This file exists to preserve your project structure.
"""

from typing import Dict

from action_planner import build_actions_from_intents


class RulePolicy:
    def decide(self) -> Dict:
        """
        Return empty intents and let action_planner select fallback targets.
        """
        return {"unit_intents": {}}


def build_rule_actions(
    obs,
    team_id,
    env_cfg,
    memory,
    match_context,
    current_step,
):
    return build_actions_from_intents(
        obs=obs,
        team_id=team_id,
        env_cfg=env_cfg,
        memory=memory,
        intents={"unit_intents": {}},
        match_context=match_context,
        current_step=current_step,
    )