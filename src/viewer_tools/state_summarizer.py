"""
state_summarizer.py

Build a compact official-rule-aware game view for the LLM.

Version focus:
- Keep the full structured gameview for internal debug.
- Build a much shorter compact prompt for the local LLM.
- Reduce timeout risk for qwen2.5:1.5b.
"""

from typing import Dict, List, Tuple

import config
from lux_state import (
    manhattan,
    parse_relic_nodes,
    parse_units,
    parse_visible_enemies,
    summarize_score,
)


Position = Tuple[int, int]


def _nearest_target(pos: Position, targets: List[Position]):
    if not targets:
        return None

    best = min(targets, key=lambda target: manhattan(pos, target))
    return {
        "target": best,
        "distance": manhattan(pos, best),
    }


def build_gameview(
    step: int,
    obs: Dict,
    team_id: int,
    env_cfg: Dict,
    memory,
    match_context: Dict,
) -> Dict:
    """
    Build a compact game view dictionary for LLM decision-making.
    """
    my_units = parse_units(obs, team_id)
    enemies = parse_visible_enemies(obs, team_id)
    visible_relics = parse_relic_nodes(obs)
    score = summarize_score(obs, team_id)

    relic_targets = memory.get_relic_targets()
    stale_targets = memory.get_best_stale_tiles(
        current_step=step,
        limit=config.MAX_STALE_TARGETS_IN_GAMEVIEW,
    )

    unit_summaries = []
    for unit in my_units:
        unit_id = unit["unit_id"]
        pos = unit["pos"]
        energy = unit["energy"]

        memory.update_unit_position(unit_id, pos)

        unit_summaries.append(
            {
                "unit_id": unit_id,
                "pos": pos,
                "energy": energy,
                "stuck_count": memory.get_unit_stuck_count(unit_id),
                "nearest_relic_target": _nearest_target(pos, relic_targets),
                "nearest_stale_target": _nearest_target(pos, stale_targets),
            }
        )

    enemy_summaries = []
    for enemy in enemies:
        enemy_summaries.append(
            {
                "unit_id": enemy["unit_id"],
                "pos": enemy["pos"],
                "energy": enemy["energy"],
            }
        )

    gameview = {
        "agent_version": config.AGENT_VERSION,
        "step": int(step),
        "match": {
            "match_idx": match_context.get("match_idx", 0),
            "step_in_match": match_context.get("step_in_match", 0),
            "phase": match_context.get("phase", "unknown"),
            "is_early_match": match_context.get("is_early_match", False),
            "is_mid_match": match_context.get("is_mid_match", False),
            "is_final_match": match_context.get("is_final_match", False),
        },
        "score": score,
        "my_units": unit_summaries,
        "visible_enemies": enemy_summaries,
        "visible_relics": visible_relics,
        "memory": {
            "known_relic_nodes": list(sorted(memory.relic_nodes)),
            "relic_candidate_tiles_sample": list(sorted(memory.relic_candidate_tiles))[
                : config.MAX_RELIC_TARGETS_IN_GAMEVIEW
            ],
            "confirmed_scoring_tiles": list(sorted(memory.confirmed_scoring_tiles)),
            "bad_scoring_tiles": list(sorted(memory.bad_scoring_tiles)),
            "top_stale_tiles": stale_targets,
            "last_point_gain_step": memory.last_point_gain_step,
        },
        "policy_hint": {
            "allowed_intents": [
                "MOVE_TO_CONFIRMED_SCORE",
                "MOVE_TO_RELIC_CANDIDATE",
                "EXPLORE_STALE_TILE",
                "HOLD_POSITION",
                "RECOVER_ENERGY",
                "CONTEST_RELIC_ZONE",
            ],
            "sap_enabled": config.ENABLE_SAP,
        },
    }

    return gameview


def _format_pos_list(items: List, limit: int = 8) -> str:
    if not items:
        return "[]"

    clipped = items[:limit]
    return "[" + ", ".join(str(item) for item in clipped) + "]"


def _compact_unit_line(unit: Dict) -> str:
    unit_id = unit.get("unit_id")
    pos = unit.get("pos")
    energy = unit.get("energy")
    stuck = unit.get("stuck_count", 0)

    relic_target = unit.get("nearest_relic_target")
    stale_target = unit.get("nearest_stale_target")

    relic_text = "none"
    stale_text = "none"

    if relic_target:
        relic_text = f"{relic_target.get('target')} d={relic_target.get('distance')}"

    if stale_target:
        stale_text = f"{stale_target.get('target')} d={stale_target.get('distance')}"

    return (
        f"u{unit_id}: pos={pos}, energy={energy}, stuck={stuck}, "
        f"nearest_relic={relic_text}, nearest_stale={stale_text}"
    )


def gameview_to_prompt(gameview: Dict) -> str:
    """
    Convert gameview dictionary into a short LLM prompt.

    The previous version used str(gameview), which was too long and caused
    frequent local LLM timeouts. This version only sends the minimum useful
    strategic information.
    """
    step = gameview.get("step", 0)
    match = gameview.get("match", {})
    score = gameview.get("score", {})
    memory = gameview.get("memory", {})

    my_units = gameview.get("my_units", [])
    visible_enemies = gameview.get("visible_enemies", [])
    visible_relics = gameview.get("visible_relics", [])

    known_relics = memory.get("known_relic_nodes", [])
    candidate_tiles = memory.get("relic_candidate_tiles_sample", [])
    confirmed_tiles = memory.get("confirmed_scoring_tiles", [])
    stale_tiles = memory.get("top_stale_tiles", [])

    unit_lines = []
    for unit in my_units[:6]:
        unit_lines.append(_compact_unit_line(unit))

    enemy_lines = []
    for enemy in visible_enemies[:6]:
        enemy_lines.append(
            f"enemy{enemy.get('unit_id')}: pos={enemy.get('pos')}, energy={enemy.get('energy')}"
        )

    lines = []

    lines.append("You control player_0 in Lux AI Season 3.")
    lines.append("Return ONLY valid JSON. No markdown. No explanation outside JSON.")
    lines.append("")
    lines.append("Rules:")
    lines.append("- Game has 5 matches; map memory persists.")
    lines.append("- Relic nodes reveal possible scoring tiles in a nearby 5x5 area.")
    lines.append("- Early phase: explore stale/unseen tiles.")
    lines.append("- Later phase: exploit relic candidate or confirmed scoring tiles.")
    lines.append("- Avoid repeated low-value recently observed tiles.")
    lines.append("- Do not use sap.")
    lines.append("")
    lines.append("Allowed intents:")
    lines.append(
        "EXPLORE_STALE_TILE, MOVE_TO_RELIC_CANDIDATE, "
        "MOVE_TO_CONFIRMED_SCORE, CONTEST_RELIC_ZONE, "
        "RECOVER_ENERGY, HOLD_POSITION"
    )
    lines.append("")
    lines.append("Output format:")
    lines.append('{"unit_intents":{"0":{"intent":"EXPLORE_STALE_TILE","reason":"short reason"}}}')
    lines.append("")
    lines.append("State:")
    lines.append(
        f"step={step}, match_idx={match.get('match_idx')}, "
        f"step_in_match={match.get('step_in_match')}, phase={match.get('phase')}"
    )
    lines.append(
        f"score: my={score.get('my_points')}, opp={score.get('opp_points')}, "
        f"diff={score.get('score_diff')}"
    )
    lines.append(f"visible_relics={_format_pos_list(visible_relics, limit=6)}")
    lines.append(f"known_relics={_format_pos_list(known_relics, limit=6)}")
    lines.append(f"candidate_tiles={_format_pos_list(candidate_tiles, limit=8)}")
    lines.append(f"confirmed_tiles={_format_pos_list(confirmed_tiles, limit=8)}")
    lines.append(f"top_stale_tiles={_format_pos_list(stale_tiles, limit=8)}")

    lines.append("")
    lines.append("My units:")
    if unit_lines:
        lines.extend(unit_lines)
    else:
        lines.append("none")

    lines.append("")
    lines.append("Visible enemies:")
    if enemy_lines:
        lines.extend(enemy_lines)
    else:
        lines.append("none")

    lines.append("")
    lines.append("Choose intents only for visible my units.")
    lines.append("Prefer relic/candidate tiles if known; otherwise explore stale tiles.")

    return "\n".join(lines)