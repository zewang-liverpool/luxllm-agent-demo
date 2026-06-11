"""
game_memory.py

Persistent memory for Lux AI Season 3 agent.

This module stores cross-match knowledge:
- Seen tiles
- Last seen step
- Relic nodes
- Relic candidate scoring tiles
- Confirmed / bad scoring tiles placeholders
- Match-aware phase information

All comments are written in English to keep the project style consistent.
"""

from typing import Dict, List, Optional, Set, Tuple


Position = Tuple[int, int]


class GameMemory:
    """
    Cross-match memory for one Lux AI Season 3 game.

    Lux S3 uses a sequence of matches in one game. Map knowledge is valuable
    across matches, so this memory should not be reset every match.
    """

    def __init__(self, map_width: int = 24, map_height: int = 24):
        self.map_width = int(map_width)
        self.map_height = int(map_height)

        self.global_step = 0
        self.match_idx = 0
        self.step_in_match = 0

        self.last_seen_step: List[List[int]] = [
            [-1 for _ in range(self.map_height)] for _ in range(self.map_width)
        ]

        self.explored_mask: List[List[bool]] = [
            [False for _ in range(self.map_height)] for _ in range(self.map_width)
        ]

        self.tile_type_memory: List[List[Optional[int]]] = [
            [None for _ in range(self.map_height)] for _ in range(self.map_width)
        ]

        self.energy_memory: List[List[Optional[int]]] = [
            [None for _ in range(self.map_height)] for _ in range(self.map_width)
        ]

        self.relic_nodes: Set[Position] = set()
        self.relic_candidate_tiles: Set[Position] = set()
        self.confirmed_scoring_tiles: Set[Position] = set()
        self.bad_scoring_tiles: Set[Position] = set()

        self.unit_last_targets: Dict[int, Position] = {}
        self.unit_last_positions: Dict[int, Position] = {}
        self.unit_stuck_count: Dict[int, int] = {}

        self.previous_team_points: Optional[int] = None
        self.last_point_gain_step: int = -1

    def in_bounds(self, pos: Position) -> bool:
        x, y = pos
        return 0 <= x < self.map_width and 0 <= y < self.map_height

    def update_match_context(self, step: int, env_cfg: Dict) -> Dict:
        """
        Compute match index and step inside match according to official S3 structure.

        Official replay has max_steps_in_match + 1 frames per match.
        """
        max_steps = int(env_cfg.get("max_steps_in_match", 100))
        match_count = int(env_cfg.get("match_count_per_episode", 5))
        frames_per_match = max_steps + 1

        self.global_step = int(step)
        self.match_idx = min(int(step) // frames_per_match, match_count - 1)
        self.step_in_match = int(step) % frames_per_match

        if self.match_idx <= 1:
            phase = "early_exploration"
        elif self.match_idx in (2, 3):
            phase = "mid_exploit"
        else:
            phase = "final_push"

        return {
            "match_idx": self.match_idx,
            "step_in_match": self.step_in_match,
            "phase": phase,
            "is_early_match": self.match_idx <= 1,
            "is_mid_match": self.match_idx in (2, 3),
            "is_final_match": self.match_idx >= 4,
        }

    def update_from_obs(self, step: int, obs: Dict, team_id: int, env_cfg: Dict) -> Dict:
        """
        Update memory from official observation dictionary.
        """
        match_context = self.update_match_context(step, env_cfg)

        self._update_visible_map(step, obs)
        self._update_relic_nodes(obs)
        self._update_team_points(step, obs, team_id)

        return match_context

    def _update_visible_map(self, step: int, obs: Dict) -> None:
        sensor_mask = obs.get("sensor_mask")
        map_features = obs.get("map_features", {})

        tile_types = map_features.get("tile_type")
        energy = map_features.get("energy")

        if sensor_mask is None:
            return

        for x in range(min(self.map_width, len(sensor_mask))):
            row = sensor_mask[x]
            for y in range(min(self.map_height, len(row))):
                if bool(row[y]):
                    self.last_seen_step[x][y] = int(step)
                    self.explored_mask[x][y] = True

                    if tile_types is not None:
                        try:
                            self.tile_type_memory[x][y] = int(tile_types[x][y])
                        except Exception:
                            pass

                    if energy is not None:
                        try:
                            self.energy_memory[x][y] = int(energy[x][y])
                        except Exception:
                            pass

    def _update_relic_nodes(self, obs: Dict) -> None:
        relic_nodes = obs.get("relic_nodes")
        relic_mask = obs.get("relic_nodes_mask")

        if relic_nodes is None:
            return

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

            relic_pos = (x, y)
            if self.in_bounds(relic_pos):
                self.relic_nodes.add(relic_pos)
                self.add_relic_candidates(relic_pos)

    def _update_team_points(self, step: int, obs: Dict, team_id: int) -> None:
        team_points = obs.get("team_points")
        if team_points is None:
            return

        try:
            current_points = int(team_points[team_id])
        except Exception:
            return

        if self.previous_team_points is not None:
            if current_points > self.previous_team_points:
                self.last_point_gain_step = int(step)

        self.previous_team_points = current_points

    def add_relic_candidates(self, relic_pos: Position) -> None:
        """
        Add 5x5 candidate scoring area around a discovered relic node.

        In Lux S3, scoring tiles are hidden around relic nodes.
        """
        x, y = relic_pos
        radius = 2

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                tx = x + dx
                ty = y + dy
                candidate = (tx, ty)
                if self.in_bounds(candidate):
                    self.relic_candidate_tiles.add(candidate)

    def is_known_asteroid(self, pos: Position) -> bool:
        """
        Official tile type usually uses 2 for asteroid in Lux S3.
        This function is defensive in case unknown tiles are not loaded yet.
        """
        if not self.in_bounds(pos):
            return True

        x, y = pos
        tile_type = self.tile_type_memory[x][y]
        return tile_type == 2

    def get_stale_score(self, pos: Position, current_step: int) -> int:
        if not self.in_bounds(pos):
            return -9999

        x, y = pos
        last_seen = self.last_seen_step[x][y]

        if last_seen < 0:
            return 300

        return max(0, int(current_step) - int(last_seen))

    def get_best_stale_tiles(
        self,
        current_step: int,
        limit: int = 20,
        avoid_asteroids: bool = True,
    ) -> List[Position]:
        scored = []

        for x in range(self.map_width):
            for y in range(self.map_height):
                pos = (x, y)

                if avoid_asteroids and self.is_known_asteroid(pos):
                    continue

                score = self.get_stale_score(pos, current_step)

                if pos in self.relic_candidate_tiles:
                    score += 80

                if pos in self.confirmed_scoring_tiles:
                    score += 200

                if pos in self.bad_scoring_tiles:
                    score -= 150

                scored.append((score, pos))

        scored.sort(reverse=True, key=lambda item: item[0])
        return [pos for _, pos in scored[:limit]]

    def get_relic_targets(self) -> List[Position]:
        """
        Target priority:
        confirmed scoring tiles > candidate scoring tiles > relic nodes.
        """
        targets: List[Position] = []

        for pos in sorted(self.confirmed_scoring_tiles):
            if self.in_bounds(pos):
                targets.append(pos)

        for pos in sorted(self.relic_candidate_tiles):
            if self.in_bounds(pos) and pos not in targets:
                targets.append(pos)

        for pos in sorted(self.relic_nodes):
            if self.in_bounds(pos) and pos not in targets:
                targets.append(pos)

        return targets

    def update_unit_position(self, unit_id: int, pos: Position) -> None:
        old_pos = self.unit_last_positions.get(unit_id)

        if old_pos == pos:
            self.unit_stuck_count[unit_id] = self.unit_stuck_count.get(unit_id, 0) + 1
        else:
            self.unit_stuck_count[unit_id] = 0

        self.unit_last_positions[unit_id] = pos

    def get_unit_stuck_count(self, unit_id: int) -> int:
        return self.unit_stuck_count.get(unit_id, 0)

    def assign_unit_target(self, unit_id: int, target: Position) -> None:
        self.unit_last_targets[unit_id] = target

    def get_unit_target(self, unit_id: int) -> Optional[Position]:
        return self.unit_last_targets.get(unit_id)

    def to_summary_dict(self, current_step: int) -> Dict:
        stale_tiles = self.get_best_stale_tiles(current_step=current_step, limit=10)

        return {
            "match_idx": self.match_idx,
            "step_in_match": self.step_in_match,
            "relic_nodes": list(sorted(self.relic_nodes)),
            "relic_candidate_tiles_count": len(self.relic_candidate_tiles),
            "confirmed_scoring_tiles_count": len(self.confirmed_scoring_tiles),
            "bad_scoring_tiles_count": len(self.bad_scoring_tiles),
            "top_stale_tiles": stale_tiles,
            "last_point_gain_step": self.last_point_gain_step,
        }