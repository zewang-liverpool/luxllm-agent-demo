"""
lux_state.py

Safe observation parser for Lux AI Season 3.

This file converts the official observation dictionary into a small internal
state representation that is easier for the LLM and rule policy to use.
"""

from typing import Dict, List, Optional, Tuple


Position = Tuple[int, int]


def safe_get_list_item(value, index, default=None):
    try:
        return value[index]
    except Exception:
        return default


def get_team_points(obs: Dict, team_id: int) -> int:
    team_points = obs.get("team_points")
    if team_points is None:
        return 0

    try:
        return int(team_points[team_id])
    except Exception:
        return 0


def get_opp_team_id(team_id: int) -> int:
    return 1 - int(team_id)


def get_unit_arrays(obs: Dict, team_id: int):
    """
    Return unit position, energy and mask arrays for one team.

    Official obs usually contains:
    obs["units"]["position"][team_id]
    obs["units"]["energy"][team_id]
    obs["units_mask"][team_id]
    """
    units = obs.get("units", {})
    units_position = units.get("position", [])
    units_energy = units.get("energy", [])
    units_mask = obs.get("units_mask", [])

    positions = safe_get_list_item(units_position, team_id, [])
    energies = safe_get_list_item(units_energy, team_id, [])
    masks = safe_get_list_item(units_mask, team_id, [])

    return positions, energies, masks


def parse_units(obs: Dict, team_id: int) -> List[Dict]:
    positions, energies, masks = get_unit_arrays(obs, team_id)

    parsed = []

    max_len = max(len(positions), len(energies), len(masks))

    for unit_id in range(max_len):
        visible = bool(safe_get_list_item(masks, unit_id, False))
        if not visible:
            continue

        pos = safe_get_list_item(positions, unit_id)
        energy = safe_get_list_item(energies, unit_id, 0)

        if pos is None:
            continue

        try:
            x, y = int(pos[0]), int(pos[1])
            # Lux S3 observations commonly encode energy as ``[value]`` per
            # unit.  Accept both that official shape and scalar snapshots.
            if isinstance(energy, (list, tuple)):
                energy = energy[0] if energy else 0
            energy_value = int(energy)
        except Exception:
            continue

        parsed.append(
            {
                "unit_id": unit_id,
                "pos": (x, y),
                "energy": energy_value,
            }
        )

    return parsed


def parse_visible_enemies(obs: Dict, team_id: int) -> List[Dict]:
    opp_id = get_opp_team_id(team_id)
    return parse_units(obs, opp_id)


def parse_relic_nodes(obs: Dict) -> List[Position]:
    relic_nodes = obs.get("relic_nodes")
    relic_mask = obs.get("relic_nodes_mask")

    if relic_nodes is None:
        return []

    results: List[Position] = []

    for i, pos in enumerate(relic_nodes):
        visible = True

        if relic_mask is not None:
            try:
                visible = bool(relic_mask[i])
            except Exception:
                visible = True

        if not visible:
            continue

        try:
            x, y = int(pos[0]), int(pos[1])
        except Exception:
            continue

        results.append((x, y))

    return results


def get_env_value(env_cfg: Dict, key: str, default):
    try:
        return env_cfg.get(key, default)
    except Exception:
        return default


def manhattan(a: Position, b: Position) -> int:
    return abs(int(a[0]) - int(b[0])) + abs(int(a[1]) - int(b[1]))


def summarize_score(obs: Dict, team_id: int) -> Dict:
    my_points = get_team_points(obs, team_id)
    opp_points = get_team_points(obs, get_opp_team_id(team_id))

    return {
        "my_points": my_points,
        "opp_points": opp_points,
        "score_diff": my_points - opp_points,
    }
