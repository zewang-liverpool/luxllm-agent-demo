"""
action_planner.py

Convert high-level LLM intents into official Lux S3 action arrays.

Official action format:
[action_type, dx, dy]

Movement:
0 stay
1 up
2 right
3 down
4 left

Sap:
5 sap with dx, dy

v0.9-J3-C update:
- Keep the conservative risk-aware target filter from v0.9-J3-A.
- Add explicit risk-filter event logging.
- Store the latest risk-filter summary on memory so agent.py can write it into
  frame_log.jsonl and viewer_frames.json.
"""

from typing import Dict, List, Optional, Tuple

import config
from lux_state import manhattan, parse_units


Position = Tuple[int, int]


def make_empty_actions(max_units: int) -> List[List[int]]:
    return [[config.ACTION_STAY, 0, 0] for _ in range(int(max_units))]


def direction_to_target(src: Position, dst: Position, memory=None) -> List[int]:
    """
    Choose a simple Manhattan step toward target.
    Avoid known asteroid if memory is available.
    """
    sx, sy = src
    tx, ty = dst

    candidates = []

    if tx > sx:
        candidates.append((config.ACTION_RIGHT, (sx + 1, sy)))
    elif tx < sx:
        candidates.append((config.ACTION_LEFT, (sx - 1, sy)))

    if ty > sy:
        candidates.append((config.ACTION_DOWN, (sx, sy + 1)))
    elif ty < sy:
        candidates.append((config.ACTION_UP, (sx, sy - 1)))

    # Add fallback order to break local stuck states.
    candidates.extend(
        [
            (config.ACTION_UP, (sx, sy - 1)),
            (config.ACTION_RIGHT, (sx + 1, sy)),
            (config.ACTION_DOWN, (sx, sy + 1)),
            (config.ACTION_LEFT, (sx - 1, sy)),
        ]
    )

    for action_id, next_pos in candidates:
        if memory is not None:
            if not memory.in_bounds(next_pos):
                continue
            if memory.is_known_asteroid(next_pos):
                continue

        return [action_id, 0, 0]

    return [config.ACTION_STAY, 0, 0]


def nearest_target(pos: Position, targets: List[Position]) -> Optional[Position]:
    if not targets:
        return None
    return min(targets, key=lambda target: manhattan(pos, target))


def _unique_positions(positions: List[Position]) -> List[Position]:
    """
    Preserve deterministic order while removing duplicates.
    """
    result: List[Position] = []
    seen = set()

    for pos in positions:
        try:
            clean = (int(pos[0]), int(pos[1]))
        except Exception:
            continue

        if clean in seen:
            continue

        seen.add(clean)
        result.append(clean)

    return result


def _position_to_list(pos: Optional[Position]) -> Optional[List[int]]:
    if pos is None:
        return None

    try:
        return [int(pos[0]), int(pos[1])]
    except Exception:
        return None


def _enemy_positions(obs: Dict, team_id: int) -> List[Position]:
    """
    Parse visible enemy positions from the current observation.

    The function uses parse_units() for the opponent team. If no visible enemies
    are present, it returns an empty list. This keeps the risk-aware filter
    conservative and observation-driven.
    """
    try:
        enemy_team_id = 1 - int(team_id)
        enemies = parse_units(obs, enemy_team_id)
    except Exception:
        return []

    positions: List[Position] = []

    for enemy in enemies:
        try:
            pos = enemy.get("pos")
            if not isinstance(pos, tuple):
                pos = tuple(pos)
            if len(pos) < 2:
                continue

            x = int(pos[0])
            y = int(pos[1])

            if x < 0 or y < 0:
                continue

            positions.append((x, y))
        except Exception:
            continue

    return _unique_positions(positions)


def _min_enemy_distance(pos: Position, enemy_positions: List[Position]) -> Optional[int]:
    if not enemy_positions:
        return None

    try:
        return min(manhattan(pos, enemy_pos) for enemy_pos in enemy_positions)
    except Exception:
        return None


def _is_target_risky(target: Position, enemy_positions: List[Position]) -> bool:
    """
    Return True when target is close to any visible enemy.

    Default radius is intentionally small. It can be overridden in config.py with:
    RISK_AWARE_TARGET_ENEMY_RADIUS = 4
    """
    if not enemy_positions:
        return False

    radius = int(getattr(config, "RISK_AWARE_TARGET_ENEMY_RADIUS", 4))
    nearest = _min_enemy_distance(target, enemy_positions)

    if nearest is None:
        return False

    return nearest <= radius


def _risk_aware_enabled() -> bool:
    return bool(getattr(config, "ENABLE_RISK_AWARE_ACTION_FILTER", True))


def _risk_aware_target_pool(
    intent: str,
    memory,
    match_context: Dict,
    current_step: int,
) -> List[Position]:
    """
    Build a deterministic alternative target pool for risk-aware filtering.
    """
    is_early = bool(match_context.get("is_early_match", False))
    is_final = bool(match_context.get("is_final_match", False))

    confirmed = list(sorted(getattr(memory, "confirmed_scoring_tiles", [])))
    candidates = list(sorted(getattr(memory, "relic_candidate_tiles", [])))
    relic_targets = list(memory.get_relic_targets())
    stale_targets = list(
        memory.get_best_stale_tiles(
            current_step=current_step,
            limit=int(getattr(config, "RISK_AWARE_STALE_TARGET_LIMIT", 20)),
        )
    )

    if intent == "MOVE_TO_CONFIRMED_SCORE":
        pool = confirmed + candidates + relic_targets + stale_targets
    elif intent == "MOVE_TO_RELIC_CANDIDATE":
        pool = candidates + confirmed + relic_targets + stale_targets
    elif intent == "CONTEST_RELIC_ZONE":
        pool = relic_targets + candidates + confirmed + stale_targets
    elif intent == "EXPLORE_STALE_TILE":
        pool = stale_targets + candidates + relic_targets + confirmed
    else:
        if confirmed:
            pool = confirmed + candidates + relic_targets + stale_targets
        elif candidates and not is_early:
            pool = candidates + relic_targets + stale_targets
        elif is_final:
            pool = relic_targets + candidates + stale_targets
        elif is_early:
            pool = stale_targets + candidates + relic_targets
        else:
            pool = candidates + stale_targets + relic_targets + confirmed

    valid: List[Position] = []
    for target in pool:
        try:
            clean = (int(target[0]), int(target[1]))
        except Exception:
            continue

        if hasattr(memory, "in_bounds") and not memory.in_bounds(clean):
            continue

        if hasattr(memory, "is_known_asteroid") and memory.is_known_asteroid(clean):
            continue

        valid.append(clean)

    return _unique_positions(valid)


def _choose_safe_target(
    unit_pos: Position,
    original_target: Position,
    candidate_targets: List[Position],
    enemy_positions: List[Position],
) -> Position:
    """
    Choose a safer alternative target when the original target is risky.

    v0.9-L1-B local-utility-aware scoring:
    - Keep the risk-aware behavior from J3.
    - Avoid selecting safe but unnecessarily distant targets.
    - Prefer candidates that are:
      1. outside visible-enemy risk radius,
      2. close to the original target,
      3. close to the unit,
      4. not much farther than the original target from the unit,
      5. still reasonably far from visible enemies.

    This function intentionally remains deterministic.
    """
    if not candidate_targets:
        return original_target

    safe_targets = [
        target for target in candidate_targets
        if not _is_target_risky(target, enemy_positions)
    ]

    if not safe_targets:
        return original_target

    risk_radius = int(getattr(config, "RISK_AWARE_TARGET_ENEMY_RADIUS", 4))

    max_original_shift = int(
        getattr(config, "RISK_AWARE_MAX_ORIGINAL_TARGET_SHIFT", 10)
    )
    max_extra_unit_distance = int(
        getattr(config, "RISK_AWARE_MAX_EXTRA_UNIT_DISTANCE", 6)
    )
    enemy_distance_cap = int(
        getattr(config, "RISK_AWARE_ENEMY_DISTANCE_CAP", 12)
    )

    weight_original_shift = float(
        getattr(config, "RISK_AWARE_WEIGHT_ORIGINAL_SHIFT", 2.2)
    )
    weight_unit_distance = float(
        getattr(config, "RISK_AWARE_WEIGHT_UNIT_DISTANCE", 1.0)
    )
    weight_extra_unit_distance = float(
        getattr(config, "RISK_AWARE_WEIGHT_EXTRA_UNIT_DISTANCE", 1.8)
    )
    weight_enemy_safety_bonus = float(
        getattr(config, "RISK_AWARE_WEIGHT_ENEMY_SAFETY_BONUS", 0.35)
    )

    original_unit_distance = manhattan(unit_pos, original_target)

    def candidate_features(target: Position) -> Dict:
        unit_distance = manhattan(unit_pos, target)
        original_shift = manhattan(original_target, target)
        enemy_distance = _min_enemy_distance(target, enemy_positions)

        if enemy_distance is None:
            enemy_distance = enemy_distance_cap

        capped_enemy_distance = min(int(enemy_distance), enemy_distance_cap)
        extra_unit_distance = int(unit_distance) - int(original_unit_distance)

        return {
            "target": target,
            "unit_distance": int(unit_distance),
            "original_shift": int(original_shift),
            "enemy_distance": int(enemy_distance),
            "capped_enemy_distance": int(capped_enemy_distance),
            "extra_unit_distance": int(extra_unit_distance),
        }

    features = [candidate_features(target) for target in safe_targets]

    # First pass: prefer candidates that remain local around the original target
    # and do not introduce too much extra travel for the unit.
    local_features = [
        item for item in features
        if item["original_shift"] <= max_original_shift
        and item["extra_unit_distance"] <= max_extra_unit_distance
    ]

    # If no local safe candidate exists, fall back to all safe candidates.
    # This preserves safety even when local alternatives are unavailable.
    scoring_pool = local_features if local_features else features

    def weighted_score(item: Dict) -> Tuple[float, int, int, int, int]:
        extra_distance_penalty = max(0, int(item["extra_unit_distance"]))

        score = (
            weight_original_shift * float(item["original_shift"])
            + weight_unit_distance * float(item["unit_distance"])
            + weight_extra_unit_distance * float(extra_distance_penalty)
            - weight_enemy_safety_bonus * float(item["capped_enemy_distance"])
        )

        # Tuple tie-breakers keep behavior deterministic:
        # 1. lower weighted score
        # 2. lower original shift
        # 3. lower unit distance
        # 4. higher enemy distance
        # 5. stable coordinate order
        return (
            score,
            int(item["original_shift"]),
            int(item["unit_distance"]),
            -int(item["enemy_distance"]),
            int(item["target"][0]) * 100 + int(item["target"][1]),
        )

    best = min(scoring_pool, key=weighted_score)
    return best["target"]



def _make_filter_event(
    unit_id: int,
    intent: str,
    unit_pos: Position,
    original_target: Position,
    filtered_target: Position,
    enemy_positions: List[Position],
    changed: bool,
    reason: str,
) -> Dict:
    original_distance = _min_enemy_distance(original_target, enemy_positions)
    filtered_distance = _min_enemy_distance(filtered_target, enemy_positions)

    return {
        "unit_id": int(unit_id),
        "intent": str(intent or "RULE_OR_CACHED_FALLBACK"),
        "unit_pos": _position_to_list(unit_pos),
        "original_target": _position_to_list(original_target),
        "filtered_target": _position_to_list(filtered_target),
        "changed": bool(changed),
        "nearest_enemy_distance_before": original_distance,
        "nearest_enemy_distance_after": filtered_distance,
        "visible_enemy_count": int(len(enemy_positions)),
        "risk_radius": int(getattr(config, "RISK_AWARE_TARGET_ENEMY_RADIUS", 4)),
        "reason": reason,
    }


def _reset_risk_filter_trace(memory) -> None:
    """
    Reset per-call risk filter trace on memory.

    agent.py reads this data after actions are built and writes it into frame logs.
    """
    try:
        memory.last_risk_filter_events = []
        memory.last_risk_filter_summary = {
            "enabled": bool(_risk_aware_enabled()),
            "evaluated_units": 0,
            "risky_original_targets": 0,
            "changed_targets": 0,
            "unchanged_risky_targets": 0,
            "visible_enemy_units": 0,
            "risk_radius": int(getattr(config, "RISK_AWARE_TARGET_ENEMY_RADIUS", 4)),
            "events": [],
        }
    except Exception:
        pass


def _append_risk_filter_event(memory, event: Dict) -> None:
    try:
        if not hasattr(memory, "last_risk_filter_events"):
            memory.last_risk_filter_events = []
        memory.last_risk_filter_events.append(event)

        if not hasattr(memory, "last_risk_filter_summary"):
            memory.last_risk_filter_summary = {}

        summary = memory.last_risk_filter_summary
        summary["events"] = list(memory.last_risk_filter_events)
        summary["evaluated_units"] = int(summary.get("evaluated_units", 0)) + 1

        if event.get("nearest_enemy_distance_before") is not None:
            radius = int(event.get("risk_radius", 4))
            if int(event["nearest_enemy_distance_before"]) <= radius:
                summary["risky_original_targets"] = int(summary.get("risky_original_targets", 0)) + 1

        if event.get("changed"):
            summary["changed_targets"] = int(summary.get("changed_targets", 0)) + 1
        elif event.get("nearest_enemy_distance_before") is not None:
            radius = int(event.get("risk_radius", 4))
            if int(event["nearest_enemy_distance_before"]) <= radius:
                summary["unchanged_risky_targets"] = int(summary.get("unchanged_risky_targets", 0)) + 1

        summary["visible_enemy_units"] = max(
            int(summary.get("visible_enemy_units", 0)),
            int(event.get("visible_enemy_count", 0)),
        )
    except Exception:
        pass


def apply_risk_aware_target_filter(
    obs: Dict,
    team_id: int,
    unit: Dict,
    target: Optional[Position],
    intent: str,
    memory,
    match_context: Dict,
    current_step: int,
) -> Optional[Position]:
    """
    Apply conservative opponent-risk filtering to the selected target.

    This function records explicit risk-filter events when visible enemy data is
    available. It does not alter HOLD_POSITION or RECOVER_ENERGY.
    """
    if target is None:
        return None

    if not _risk_aware_enabled():
        return target

    if intent in {"HOLD_POSITION", "RECOVER_ENERGY"}:
        return target

    try:
        unit_id = int(unit["unit_id"])
        unit_pos = unit["pos"]
        if not isinstance(unit_pos, tuple):
            unit_pos = tuple(unit_pos)
        unit_pos = (int(unit_pos[0]), int(unit_pos[1]))

        clean_target = (int(target[0]), int(target[1]))
    except Exception:
        return target

    enemies = _enemy_positions(obs, team_id)
    if not enemies:
        return clean_target

    if not _is_target_risky(clean_target, enemies):
        event = _make_filter_event(
            unit_id=unit_id,
            intent=intent,
            unit_pos=unit_pos,
            original_target=clean_target,
            filtered_target=clean_target,
            enemy_positions=enemies,
            changed=False,
            reason="original target outside visible-enemy risk radius",
        )
        _append_risk_filter_event(memory, event)
        return clean_target

    pool = _risk_aware_target_pool(
        intent=intent,
        memory=memory,
        match_context=match_context,
        current_step=current_step,
    )

    safe_target = _choose_safe_target(
        unit_pos=unit_pos,
        original_target=clean_target,
        candidate_targets=pool,
        enemy_positions=enemies,
    )

    changed = safe_target != clean_target
    reason = (
        "original target inside visible-enemy risk radius; safer target selected"
        if changed
        else "original target inside visible-enemy risk radius; no safer alternative found"
    )

    event = _make_filter_event(
        unit_id=unit_id,
        intent=intent,
        unit_pos=unit_pos,
        original_target=clean_target,
        filtered_target=safe_target,
        enemy_positions=enemies,
        changed=changed,
        reason=reason,
    )
    _append_risk_filter_event(memory, event)

    return safe_target


def choose_rule_target(
    unit: Dict,
    memory,
    match_context: Dict,
    current_step: int,
) -> Optional[Position]:
    """
    Rule-based fallback target selection.
    """
    pos = unit["pos"]
    energy = int(unit.get("energy", 0))

    if energy <= config.LOW_ENERGY_THRESHOLD:
        return pos

    relic_targets = memory.get_relic_targets()
    stale_targets = memory.get_best_stale_tiles(current_step=current_step, limit=20)

    is_early = match_context.get("is_early_match", False)
    is_final = match_context.get("is_final_match", False)

    confirmed = list(sorted(memory.confirmed_scoring_tiles))
    if confirmed:
        return nearest_target(pos, confirmed)

    candidates = list(sorted(memory.relic_candidate_tiles))
    if candidates and not is_early:
        return nearest_target(pos, candidates)

    if is_final and relic_targets:
        return nearest_target(pos, relic_targets)

    if is_early and stale_targets:
        return nearest_target(pos, stale_targets)

    if candidates:
        return nearest_target(pos, candidates)

    if stale_targets:
        return nearest_target(pos, stale_targets)

    if relic_targets:
        return nearest_target(pos, relic_targets)

    return pos


def target_from_intent(
    intent: str,
    unit: Dict,
    memory,
    match_context: Dict,
    current_step: int,
) -> Optional[Position]:
    pos = unit["pos"]

    if intent == "HOLD_POSITION":
        return pos

    if intent == "RECOVER_ENERGY":
        return pos

    if intent == "MOVE_TO_CONFIRMED_SCORE":
        targets = list(sorted(memory.confirmed_scoring_tiles))
        return nearest_target(pos, targets) if targets else None

    if intent == "MOVE_TO_RELIC_CANDIDATE":
        targets = list(sorted(memory.relic_candidate_tiles))
        return nearest_target(pos, targets) if targets else None

    if intent == "CONTEST_RELIC_ZONE":
        targets = memory.get_relic_targets()
        return nearest_target(pos, targets) if targets else None

    if intent == "EXPLORE_STALE_TILE":
        targets = memory.get_best_stale_tiles(current_step=current_step, limit=20)
        return nearest_target(pos, targets) if targets else None

    return None


def build_actions_from_intents(
    obs: Dict,
    team_id: int,
    env_cfg: Dict,
    memory,
    intents: Dict,
    match_context: Dict,
    current_step: int,
) -> List[List[int]]:
    """
    Build official Lux S3 action array from LLM high-level intents.
    """
    max_units = int(env_cfg.get("max_units", 16))
    actions = make_empty_actions(max_units)

    _reset_risk_filter_trace(memory)

    units = parse_units(obs, team_id)
    unit_intents = intents.get("unit_intents", {}) if isinstance(intents, dict) else {}

    for unit in units:
        unit_id = int(unit["unit_id"])
        pos = unit["pos"]

        if unit_id >= max_units:
            continue

        intent_item = unit_intents.get(str(unit_id), {})
        if not isinstance(intent_item, dict):
            intent_item = {}

        intent = intent_item.get("intent", "")

        target = target_from_intent(
            intent=intent,
            unit=unit,
            memory=memory,
            match_context=match_context,
            current_step=current_step,
        )

        if target is None:
            target = choose_rule_target(
                unit=unit,
                memory=memory,
                match_context=match_context,
                current_step=current_step,
            )

        target = apply_risk_aware_target_filter(
            obs=obs,
            team_id=team_id,
            unit=unit,
            target=target,
            intent=str(intent),
            memory=memory,
            match_context=match_context,
            current_step=current_step,
        )

        if target is None:
            actions[unit_id] = [config.ACTION_STAY, 0, 0]
            continue

        memory.assign_unit_target(unit_id, target)

        if target == pos:
            actions[unit_id] = [config.ACTION_STAY, 0, 0]
        else:
            actions[unit_id] = direction_to_target(pos, target, memory=memory)

    try:
        if hasattr(memory, "last_risk_filter_summary"):
            memory.last_risk_filter_summary["enabled"] = bool(_risk_aware_enabled())
            memory.last_risk_filter_summary["events"] = list(
                getattr(memory, "last_risk_filter_events", [])
            )
    except Exception:
        pass

    return actions