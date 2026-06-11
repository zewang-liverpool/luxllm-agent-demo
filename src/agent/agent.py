"""
agent.py

Main Lux S3 Agent.

Version focus:
- Official-compatible no-numpy action output
- Stable rule-only switch for replay validation
- One-player LLM mode:
    player_0 -> LLM strategic planner
    player_1 -> fallback rule policy
- Round-aware memory
- Stale tile guard
- Fast LLM cache to avoid calling LLM every step
- Robust timeout handling
- v0.9-A frame logging baseline
- v0.9-B memory overlay coordinates
- v0.9-C sensor / energy overlay coordinates
"""

import json
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

import config
from action_planner import build_actions_from_intents, make_empty_actions
from game_memory import GameMemory
from llm_decider import LLMDecider
from rule_policy import build_rule_actions
from state_summarizer import build_gameview


Position = Tuple[int, int]


class Agent:
    def __init__(self, player: str, env_cfg: Dict):
        self.player = player
        self.env_cfg = env_cfg or {}

        self.team_id = 0 if player == "player_0" else 1

        self.map_width = int(self.env_cfg.get("map_width", config.MAP_WIDTH))
        self.map_height = int(self.env_cfg.get("map_height", config.MAP_HEIGHT))
        self.max_units = int(self.env_cfg.get("max_units", 16))

        self.memory = GameMemory(
            map_width=self.map_width,
            map_height=self.map_height,
        )

        self.llm_enabled_for_this_player = bool(
            (not config.FORCE_RULE_ONLY)
            and config.LLM_ENABLED
            and self.player == config.LLM_PLAYER
        )

        self.is_fallback_player = bool(
            config.FORCE_RULE_ONLY
            or self.player == config.FALLBACK_PLAYER
            or not self.llm_enabled_for_this_player
        )

        self.llm_decider = LLMDecider(enabled=self.llm_enabled_for_this_player)

        self.last_llm_intents = {"unit_intents": {}}
        self.last_llm_step = -9999
        self.consecutive_llm_timeouts = 0
        self.llm_temporarily_disabled = False

        self.last_relic_count = 0
        self.last_match_idx = 0
        self.last_score_diff = 0

        self._ensure_dirs()

        self._log_debug(
            {
                "event": "agent_initialized",
                "version": config.AGENT_VERSION,
                "player": self.player,
                "team_id": self.team_id,
                "env_cfg": self.env_cfg,
                "force_rule_only": config.FORCE_RULE_ONLY,
                "llm_enabled_for_this_player": self.llm_enabled_for_this_player,
                "is_fallback_player": self.is_fallback_player,
                "llm_player": config.LLM_PLAYER,
                "fallback_player": config.FALLBACK_PLAYER,
                "llm_model": config.LLM_MODEL,
                "frame_logging": bool(getattr(config, "ENABLE_FRAME_LOGGING", False)),
                "frame_log_path": getattr(config, "FRAME_LOG_PATH", ""),
            }
        )

        print(
            f"[Lux LLM Agent {config.AGENT_VERSION}] "
            f"Agent initialized. player={self.player}, team_id={self.team_id}, "
            f"force_rule_only={config.FORCE_RULE_ONLY}, "
            f"llm_enabled_for_this_player={self.llm_enabled_for_this_player}, "
            f"is_fallback_player={self.is_fallback_player}, "
            f"llm_player={config.LLM_PLAYER}, fallback_player={config.FALLBACK_PLAYER}, "
            f"model={config.LLM_MODEL}",
            file=sys.stderr,
            flush=True,
        )

    def act(self, step: int, obs: Dict, remainingOverageTime: int = 60):
        """
        Official Lux S3 action entry.

        Return:
            List[List[int]] with shape [max_units][3]
        """
        started = time.time()

        try:
            match_context = self.memory.update_from_obs(
                step=step,
                obs=obs,
                team_id=self.team_id,
                env_cfg=self.env_cfg,
            )

            gameview = build_gameview(
                step=step,
                obs=obs,
                team_id=self.team_id,
                env_cfg=self.env_cfg,
                memory=self.memory,
                match_context=match_context,
            )

            llm_intents, llm_mode = self._get_llm_intents(
                step=step,
                gameview=gameview,
                match_context=match_context,
            )

            actions = build_actions_from_intents(
                obs=obs,
                team_id=self.team_id,
                env_cfg=self.env_cfg,
                memory=self.memory,
                intents=llm_intents,
                match_context=match_context,
                current_step=step,
            )

            action_fallback_used = False
            if not self._valid_actions(actions):
                action_fallback_used = True
                actions = build_rule_actions(
                    obs=obs,
                    team_id=self.team_id,
                    env_cfg=self.env_cfg,
                    memory=self.memory,
                    match_context=match_context,
                    current_step=step,
                )

            actions = self._to_action_list(actions)
            elapsed = time.time() - started

            self._update_event_tracking(gameview, match_context)

            self._log_debug(
                {
                    "event": "act",
                    "step": int(step),
                    "elapsed": elapsed,
                    "player": self.player,
                    "team_id": self.team_id,
                    "force_rule_only": config.FORCE_RULE_ONLY,
                    "llm_mode": llm_mode,
                    "llm_enabled_for_this_player": self.llm_enabled_for_this_player,
                    "is_fallback_player": self.is_fallback_player,
                    "action_fallback_used": action_fallback_used,
                    "last_llm_step": self.last_llm_step,
                    "consecutive_llm_timeouts": self.consecutive_llm_timeouts,
                    "llm_temporarily_disabled": self.llm_temporarily_disabled,
                    "match_context": match_context,
                    "memory": self.memory.to_summary_dict(current_step=step),
                    "actions": actions,
                }
            )

            self._write_frame_log(
                step=step,
                obs=obs,
                gameview=gameview,
                match_context=match_context,
                llm_intents=llm_intents,
                llm_mode=llm_mode,
                actions=actions,
                elapsed=elapsed,
                action_fallback_used=action_fallback_used,
            )

            return actions

        except Exception as exc:
            self._log_debug(
                {
                    "event": "act_error",
                    "step": int(step),
                    "player": self.player,
                    "force_rule_only": config.FORCE_RULE_ONLY,
                    "error": repr(exc),
                }
            )

            print(
                f"[Lux LLM Agent ERROR] "
                f"step={step}, player={self.player}, error={repr(exc)}",
                file=sys.stderr,
                flush=True,
            )

            return make_empty_actions(self.max_units)

    def _get_llm_intents(
        self,
        step: int,
        gameview: Dict,
        match_context: Dict,
    ) -> Tuple[Dict, str]:
        """
        Decide whether to call LLM or reuse cached intents.
        """
        if config.FORCE_RULE_ONLY:
            return {"unit_intents": {}}, "force_rule_only"

        if not self.llm_enabled_for_this_player:
            return {"unit_intents": {}}, "fallback_rule_player"

        if self.llm_temporarily_disabled:
            return self.last_llm_intents, "llm_disabled_after_timeouts"

        should_call, reason = self._should_call_llm(
            step=step,
            gameview=gameview,
            match_context=match_context,
        )

        if not should_call:
            if config.LLM_REUSE_LAST_INTENTS:
                return self.last_llm_intents, f"reuse_cached_llm_intents:{reason}"
            return {"unit_intents": {}}, f"skip_llm_rule_fallback:{reason}"

        intents = self.llm_decider.decide(gameview)

        timed_out = bool(getattr(self.llm_decider, "last_timed_out", False))
        error_text = str(getattr(self.llm_decider, "last_error", ""))

        if isinstance(intents, dict):
            error_text += " " + str(intents.get("error", ""))

        if "timed out" in error_text.lower():
            timed_out = True

        if timed_out:
            self.consecutive_llm_timeouts += 1
        else:
            self.consecutive_llm_timeouts = 0

        if self.consecutive_llm_timeouts >= config.LLM_DISABLE_AFTER_TIMEOUTS:
            self.llm_temporarily_disabled = True
            return self.last_llm_intents, "llm_disabled_after_timeout_limit"

        if isinstance(intents, dict) and isinstance(intents.get("unit_intents"), dict):
            if intents.get("unit_intents"):
                self.last_llm_intents = intents
                self.last_llm_step = int(step)
                return intents, f"fresh_llm_call:{reason}"

        return self.last_llm_intents, f"fresh_llm_empty_reuse_cache:{reason}"

    def _should_call_llm(
        self,
        step: int,
        gameview: Dict,
        match_context: Dict,
    ) -> Tuple[bool, str]:
        """
        LLM call policy.

        LLM is called:
        - On configured early steps
        - Every LLM_CALL_INTERVAL steps
        - When a new match starts
        - When a new relic is discovered
        - When score changes sharply
        """
        step = int(step)

        if step in config.LLM_CALL_EARLY_STEPS:
            return True, "early_step"

        interval = max(1, int(config.LLM_CALL_INTERVAL))
        if step % interval == 0:
            return True, "periodic_interval"

        current_match_idx = int(match_context.get("match_idx", 0))
        current_step_in_match = int(match_context.get("step_in_match", 0))

        if current_step_in_match == 0 and current_match_idx != self.last_match_idx:
            return True, "new_match"

        current_relic_count = len(self.memory.relic_nodes)
        if current_relic_count > self.last_relic_count:
            return True, "new_relic_discovered"

        score = gameview.get("score", {})
        score_diff = int(score.get("score_diff", 0))
        if abs(score_diff - self.last_score_diff) >= 5:
            return True, "score_diff_changed"

        return False, "no_trigger"

    def _update_event_tracking(self, gameview: Dict, match_context: Dict) -> None:
        """
        Update event-tracking fields after each action.
        """
        try:
            self.last_relic_count = len(self.memory.relic_nodes)
        except Exception:
            pass

        try:
            self.last_match_idx = int(match_context.get("match_idx", self.last_match_idx))
        except Exception:
            pass

        try:
            score = gameview.get("score", {})
            self.last_score_diff = int(score.get("score_diff", self.last_score_diff))
        except Exception:
            pass

    def _valid_actions(self, actions) -> bool:
        if not isinstance(actions, list):
            return False

        if len(actions) != self.max_units:
            return False

        for item in actions:
            if not isinstance(item, list):
                return False

            if len(item) != 3:
                return False

            for value in item:
                try:
                    int(value)
                except Exception:
                    return False

        return True

    def _to_action_list(self, actions) -> List[List[int]]:
        fixed = make_empty_actions(self.max_units)

        if not isinstance(actions, list):
            return fixed

        rows = min(self.max_units, len(actions))

        for i in range(rows):
            try:
                row = actions[i]
                if not isinstance(row, list) or len(row) != 3:
                    continue

                fixed[i] = [
                    int(row[0]),
                    int(row[1]),
                    int(row[2]),
                ]
            except Exception:
                fixed[i] = [0, 0, 0]

        return fixed

    def _ensure_dirs(self) -> None:
        os.makedirs(config.LOG_DIR, exist_ok=True)
        os.makedirs(config.ERROR_LOG_DIR, exist_ok=True)
        os.makedirs(config.REPLAY_DIR, exist_ok=True)

        if hasattr(config, "VIEW_DIR"):
            os.makedirs(config.VIEW_DIR, exist_ok=True)

        if hasattr(config, "DOCS_DIR"):
            os.makedirs(config.DOCS_DIR, exist_ok=True)

    def _log_debug(self, data: Dict) -> None:
        try:
            os.makedirs(config.LOG_DIR, exist_ok=True)
            with open(config.AGENT_DEBUG_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(data, ensure_ascii=False) + "\n")
        except Exception:
            pass


    def _build_frame_enemy_units(self, obs: Dict) -> List[Dict]:
        """
        Build a compact visible-enemy unit list for the explanation viewer.

        This method is intentionally defensive:
        - It never affects official Lux actions.
        - It supports the standard Lux S3 observation layout:
          obs["units"]["position"][team_id][unit_id]
          obs["units"]["energy"][team_id][unit_id]
          obs["units_mask"][team_id][unit_id]
        - It returns an empty list when enemy units are not visible or not present
          in the current observation.

        The output is written into frame_log.jsonl and later carried into
        viewer_frames.json by view/build_viewer_frames.py.
        """
        enemy_units: List[Dict] = []

        try:
            if not isinstance(obs, dict):
                return enemy_units

            enemy_team_id = 1 - int(self.team_id)

            units = obs.get("units", {})
            if not isinstance(units, dict):
                return enemy_units

            positions_all = units.get("position", [])
            energies_all = units.get("energy", [])
            masks_all = obs.get("units_mask", [])

            if not isinstance(positions_all, (list, tuple)):
                return enemy_units

            if enemy_team_id >= len(positions_all):
                return enemy_units

            enemy_positions = positions_all[enemy_team_id]
            enemy_energies = (
                energies_all[enemy_team_id]
                if isinstance(energies_all, (list, tuple)) and enemy_team_id < len(energies_all)
                else []
            )
            enemy_masks = (
                masks_all[enemy_team_id]
                if isinstance(masks_all, (list, tuple)) and enemy_team_id < len(masks_all)
                else []
            )

            if not isinstance(enemy_positions, (list, tuple)):
                return enemy_units

            for unit_id, pos in enumerate(enemy_positions):
                try:
                    if isinstance(enemy_masks, (list, tuple)) and unit_id < len(enemy_masks):
                        if not bool(enemy_masks[unit_id]):
                            continue

                    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
                        continue

                    x = int(pos[0])
                    y = int(pos[1])

                    if x < 0 or y < 0:
                        continue

                    energy = 0
                    if isinstance(enemy_energies, (list, tuple)) and unit_id < len(enemy_energies):
                        raw_energy = enemy_energies[unit_id]
                        if isinstance(raw_energy, (list, tuple)) and raw_energy:
                            raw_energy = raw_energy[0]
                        energy = int(raw_energy)

                    enemy_units.append(
                        {
                            "unit_id": int(unit_id),
                            "team_id": int(enemy_team_id),
                            "pos": [x, y],
                            "energy": int(energy),
                            "visible": True,
                            "source": "obs.units.position",
                        }
                    )
                except Exception:
                    continue

        except Exception:
            return []

        return enemy_units

    def _write_frame_log(
        self,
        step: int,
        obs: Dict,
        gameview: Dict,
        match_context: Dict,
        llm_intents: Dict,
        llm_mode: str,
        actions: List[List[int]],
        elapsed: float,
        action_fallback_used: bool,
    ) -> None:
        """
        Write one compact explanation frame for the log-driven viewer.

        This function must never affect the official action output.
        Any failure is swallowed so logging cannot crash the Lux runner.
        """
        if not bool(getattr(config, "ENABLE_FRAME_LOGGING", False)):
            return

        try:
            os.makedirs(config.LOG_DIR, exist_ok=True)

            score = gameview.get("score", {}) if isinstance(gameview, dict) else {}
            my_points = int(score.get("my_points", 0))
            opp_points = int(score.get("opp_points", 0))

            if self.team_id == 0:
                team0_points = my_points
                team1_points = opp_points
            else:
                team0_points = opp_points
                team1_points = my_points

            memory_summary = self.memory.to_summary_dict(current_step=step)
            memory_overlay = self._build_memory_overlay(current_step=step)
            vision_overlay = self._build_vision_energy_overlay(obs=obs)

            units = self._build_frame_units(
                gameview=gameview,
                llm_intents=llm_intents,
                actions=actions,
            )

            enemy_units = self._build_frame_enemy_units(obs=obs)

            warnings = self._build_frame_warnings(
                llm_mode=llm_mode,
                action_fallback_used=action_fallback_used,
                units=units,
                memory_overlay=memory_overlay,
                vision_overlay=vision_overlay,
            )

            unit_intents = {}
            if isinstance(llm_intents, dict) and isinstance(llm_intents.get("unit_intents"), dict):
                unit_intents = llm_intents.get("unit_intents", {})

            frame = {
                "schema_version": getattr(
                    config,
                    "VIEWER_FRAME_SCHEMA_VERSION",
                    "lux_s3_viewer_frames_v1",
                ),
                "agent_version": config.AGENT_VERSION,
                "event": "frame",
                "time": time.time(),
                "step": int(step),
                "match_idx": int(match_context.get("match_idx", 0)),
                "step_in_match": int(match_context.get("step_in_match", 0)),
                "phase": str(match_context.get("phase", "unknown")),
                "player": self.player,
                "team_id": int(self.team_id),
                "map_width": int(self.map_width),
                "map_height": int(self.map_height),
                "max_units": int(self.max_units),
                "score": {
                    "team0": int(team0_points),
                    "team1": int(team1_points),
                    "my_points": int(my_points),
                    "opp_points": int(opp_points),
                    "diff": int(team0_points - team1_points),
                    "my_diff": int(my_points - opp_points),
                },
                "llm_mode": str(llm_mode),
                "llm": {
                    "enabled_for_player": bool(self.llm_enabled_for_this_player),
                    "is_fallback_player": bool(self.is_fallback_player),
                    "model": config.LLM_MODEL,
                    "elapsed": float(getattr(self.llm_decider, "last_elapsed", 0.0)),
                    "timed_out": bool(getattr(self.llm_decider, "last_timed_out", False)),
                    "error": str(getattr(self.llm_decider, "last_error", "")),
                    "fallback_used": bool(
                        self._mode_implies_fallback(llm_mode) or action_fallback_used
                    ),
                    "fresh_strategy_used": bool(
                        getattr(self.llm_decider, "last_strategy_used", False)
                    ),
                    "consecutive_timeouts": int(self.consecutive_llm_timeouts),
                    "temporarily_disabled": bool(self.llm_temporarily_disabled),
                    "last_llm_step": int(self.last_llm_step),
                    "unit_intent_count": int(len(unit_intents)),
                },
                "units": units,
                "enemy_units": enemy_units,
                "risk_filter": self._build_frame_risk_filter(),
                "opponent_awareness": {
                    "enemy_units_logged": int(len(enemy_units)),
                    "enemy_unit_source": "obs.units.position",
                    "enemy_team_id": int(1 - int(self.team_id)),
                    "note": (
                        "Visible enemy units are logged when the Lux observation "
                        "contains enemy unit positions for this player."
                    ),
                },
                "actions": actions,
                "memory": {
                    "known_relic_nodes": memory_overlay["known_relic_nodes"],
                    "known_relic_nodes_count": len(memory_overlay["known_relic_nodes"]),
                    "relic_candidate_tiles": memory_overlay["relic_candidate_tiles"],
                    "candidate_tiles_count": int(len(self.memory.relic_candidate_tiles)),
                    "confirmed_scoring_tiles": memory_overlay["confirmed_scoring_tiles"],
                    "confirmed_tiles_count": int(len(self.memory.confirmed_scoring_tiles)),
                    "bad_scoring_tiles": memory_overlay["bad_scoring_tiles"],
                    "bad_tiles_count": int(len(self.memory.bad_scoring_tiles)),
                    "top_stale_tiles": memory_overlay["top_stale_tiles"],
                    "top_stale_tiles_count": int(len(memory_overlay["top_stale_tiles"])),
                    "unit_targets": memory_overlay["unit_targets"],
                    "last_point_gain_step": int(memory_summary.get("last_point_gain_step", -1)),
                    "overlay_note": (
                        "Coordinates are clipped by MAX_*_IN_FRAME config values "
                        "to keep viewer_frames.json browser-friendly."
                    ),
                },
                "vision": vision_overlay,
                "warnings": warnings,
                "elapsed_total": float(elapsed),
            }

            with open(config.FRAME_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(frame, ensure_ascii=False) + "\n")

        except Exception as exc:
            self._log_debug(
                {
                    "event": "frame_log_error",
                    "step": int(step),
                    "player": self.player,
                    "error": repr(exc),
                }
            )

    def _build_memory_overlay(self, current_step: int) -> Dict:
        """
        Build coordinate lists for memory overlay.

        These coordinates are consumed directly by s3_log_driven_gameview.html.
        """
        known_relic_nodes = self._clip_positions(
            self.memory.relic_nodes,
            limit=getattr(config, "MAX_RELIC_TARGETS_IN_GAMEVIEW", 20),
        )

        relic_candidate_tiles = self._clip_positions(
            self.memory.relic_candidate_tiles,
            limit=getattr(config, "MAX_RELIC_CANDIDATE_TILES_IN_FRAME", 80),
        )

        confirmed_scoring_tiles = self._clip_positions(
            self.memory.confirmed_scoring_tiles,
            limit=getattr(config, "MAX_CONFIRMED_SCORING_TILES_IN_FRAME", 80),
        )

        bad_scoring_tiles = self._clip_positions(
            self.memory.bad_scoring_tiles,
            limit=getattr(config, "MAX_BAD_SCORING_TILES_IN_FRAME", 80),
        )

        top_stale_tiles = self._clip_positions(
            self.memory.get_best_stale_tiles(
                current_step=current_step,
                limit=getattr(config, "MAX_STALE_TILES_IN_FRAME", 24),
            ),
            limit=getattr(config, "MAX_STALE_TILES_IN_FRAME", 24),
        )

        unit_targets = []
        for unit_id, target in sorted(self.memory.unit_last_targets.items()):
            if len(unit_targets) >= getattr(config, "MAX_UNIT_TARGETS_IN_FRAME", 32):
                break

            clean_target = self._clean_position(target)
            if clean_target is None:
                continue

            unit_targets.append(
                {
                    "unit_id": int(unit_id),
                    "target": clean_target,
                }
            )

        return {
            "known_relic_nodes": known_relic_nodes,
            "relic_candidate_tiles": relic_candidate_tiles,
            "confirmed_scoring_tiles": confirmed_scoring_tiles,
            "bad_scoring_tiles": bad_scoring_tiles,
            "top_stale_tiles": top_stale_tiles,
            "unit_targets": unit_targets,
        }

    def _build_vision_energy_overlay(self, obs: Dict) -> Dict:
        """
        Build visible / explored / energy / tile-type overlay data.

        visible_tiles:
            Current visible tiles from obs["sensor_mask"].

        explored_tiles / energy_tiles / tile_type_tiles:
            Data from GameMemory if the memory fields exist.
        """
        visible_tiles = []
        explored_tiles = []
        energy_tiles = []
        tile_type_tiles = []

        sensor_mask = obs.get("sensor_mask") if isinstance(obs, dict) else None

        if sensor_mask is not None:
            for x in range(min(self.map_width, len(sensor_mask))):
                try:
                    row = sensor_mask[x]
                except Exception:
                    continue

                for y in range(min(self.map_height, len(row))):
                    try:
                        if bool(row[y]):
                            visible_tiles.append([int(x), int(y)])
                    except Exception:
                        continue

        for x in range(self.map_width):
            for y in range(self.map_height):
                try:
                    if hasattr(self.memory, "explored_mask") and bool(self.memory.explored_mask[x][y]):
                        explored_tiles.append([int(x), int(y)])
                except Exception:
                    pass

                try:
                    if hasattr(self.memory, "energy_memory"):
                        energy_value = self.memory.energy_memory[x][y]
                        if energy_value is not None:
                            energy_tiles.append(
                                {
                                    "pos": [int(x), int(y)],
                                    "energy": int(energy_value),
                                }
                            )
                except Exception:
                    pass

                try:
                    if hasattr(self.memory, "tile_type_memory"):
                        tile_type = self.memory.tile_type_memory[x][y]
                        if tile_type is not None:
                            tile_type_tiles.append(
                                {
                                    "pos": [int(x), int(y)],
                                    "tile_type": int(tile_type),
                                }
                            )
                except Exception:
                    pass

        visible_tiles = self._clip_positions(
            visible_tiles,
            limit=getattr(config, "MAX_VISIBLE_TILES_IN_FRAME", 576),
        )

        explored_tiles = self._clip_positions(
            explored_tiles,
            limit=getattr(config, "MAX_EXPLORED_TILES_IN_FRAME", 576),
        )

        energy_tiles = self._clip_overlay_items(
            energy_tiles,
            limit=getattr(config, "MAX_ENERGY_TILES_IN_FRAME", 576),
        )

        tile_type_tiles = self._clip_overlay_items(
            tile_type_tiles,
            limit=getattr(config, "MAX_TILE_TYPE_TILES_IN_FRAME", 576),
        )

        known_energy_values = []
        for item in energy_tiles:
            try:
                known_energy_values.append(int(item.get("energy", 0)))
            except Exception:
                pass

        if known_energy_values:
            min_energy = min(known_energy_values)
            max_energy = max(known_energy_values)
        else:
            min_energy = 0
            max_energy = 0

        return {
            "visible_tiles": visible_tiles,
            "visible_tiles_count": len(visible_tiles),
            "explored_tiles": explored_tiles,
            "explored_tiles_count": len(explored_tiles),
            "energy_tiles": energy_tiles,
            "energy_tiles_count": len(energy_tiles),
            "energy_min": int(min_energy),
            "energy_max": int(max_energy),
            "tile_type_tiles": tile_type_tiles,
            "tile_type_tiles_count": len(tile_type_tiles),
            "note": (
                "visible_tiles are from the current sensor_mask; "
                "explored_tiles, energy_tiles, and tile_type_tiles are from GameMemory when available."
            ),
        }


    def _build_frame_risk_filter(self) -> Dict:
        """
        Build frame-level risk filter metadata for the explanation viewer.

        action_planner.py stores the latest per-frame risk filter trace on
        self.memory.last_risk_filter_summary. This method converts it into a
        compact, JSON-safe dictionary for frame_log.jsonl.
        """
        default_summary = {
            "enabled": bool(getattr(config, "ENABLE_RISK_AWARE_ACTION_FILTER", True)),
            "evaluated_units": 0,
            "risky_original_targets": 0,
            "changed_targets": 0,
            "unchanged_risky_targets": 0,
            "visible_enemy_units": 0,
            "risk_radius": int(getattr(config, "RISK_AWARE_TARGET_ENEMY_RADIUS", 4)),
            "events": [],
            "note": "No risk-filter events were recorded for this frame.",
        }

        try:
            summary = getattr(self.memory, "last_risk_filter_summary", None)
            if not isinstance(summary, dict):
                return default_summary

            events = summary.get("events", [])
            if not isinstance(events, list):
                events = []

            clean_events = []
            for event in events[:32]:
                if not isinstance(event, dict):
                    continue

                clean_events.append(
                    {
                        "unit_id": int(event.get("unit_id", -1)),
                        "intent": str(event.get("intent", "")),
                        "unit_pos": self._clean_position(event.get("unit_pos")),
                        "original_target": self._clean_position(event.get("original_target")),
                        "filtered_target": self._clean_position(event.get("filtered_target")),
                        "changed": bool(event.get("changed", False)),
                        "nearest_enemy_distance_before": event.get("nearest_enemy_distance_before"),
                        "nearest_enemy_distance_after": event.get("nearest_enemy_distance_after"),
                        "visible_enemy_count": int(event.get("visible_enemy_count", 0)),
                        "risk_radius": int(event.get("risk_radius", default_summary["risk_radius"])),
                        "reason": str(event.get("reason", "")),
                    }
                )

            return {
                "enabled": bool(summary.get("enabled", default_summary["enabled"])),
                "evaluated_units": int(summary.get("evaluated_units", 0)),
                "risky_original_targets": int(summary.get("risky_original_targets", 0)),
                "changed_targets": int(summary.get("changed_targets", 0)),
                "unchanged_risky_targets": int(summary.get("unchanged_risky_targets", 0)),
                "visible_enemy_units": int(summary.get("visible_enemy_units", 0)),
                "risk_radius": int(summary.get("risk_radius", default_summary["risk_radius"])),
                "events": clean_events,
                "events_count": int(len(clean_events)),
                "note": (
                    "Risk-filter events are recorded only when visible enemy units "
                    "are available and a unit target can be evaluated."
                ),
            }
        except Exception:
            return default_summary

    def _build_frame_units(
        self,
        gameview: Dict,
        llm_intents: Dict,
        actions: List[List[int]],
    ) -> List[Dict]:
        units = []

        try:
            raw_units = gameview.get("my_units", []) if isinstance(gameview, dict) else []
        except Exception:
            raw_units = []

        unit_intents = {}
        if isinstance(llm_intents, dict) and isinstance(llm_intents.get("unit_intents"), dict):
            unit_intents = llm_intents.get("unit_intents", {})

        for unit in raw_units:
            try:
                unit_id = int(unit.get("unit_id"))
                intent_item = unit_intents.get(str(unit_id), {})
                if not isinstance(intent_item, dict):
                    intent_item = {}

                target = self._clean_position(self.memory.get_unit_target(unit_id))

                action = [0, 0, 0]
                if isinstance(actions, list) and 0 <= unit_id < len(actions):
                    raw_action = actions[unit_id]
                    if isinstance(raw_action, list) and len(raw_action) == 3:
                        action = [
                            int(raw_action[0]),
                            int(raw_action[1]),
                            int(raw_action[2]),
                        ]

                units.append(
                    {
                        "unit_id": int(unit_id),
                        "pos": self._clean_position(unit.get("pos")),
                        "energy": int(unit.get("energy", 0)),
                        "stuck_count": int(unit.get("stuck_count", 0)),
                        "target": target,
                        "action": action,
                        "action_name": self._action_name(action[0]),
                        "intent": str(intent_item.get("intent", "RULE_OR_CACHED_FALLBACK")),
                        "reason": str(
                            intent_item.get(
                                "reason",
                                "No fresh LLM reason for this unit.",
                            )
                        ),
                        "nearest_relic_target": unit.get("nearest_relic_target"),
                        "nearest_stale_target": unit.get("nearest_stale_target"),
                    }
                )
            except Exception:
                continue

        return units

    def _build_frame_warnings(
        self,
        llm_mode: str,
        action_fallback_used: bool,
        units: List[Dict],
        memory_overlay: Optional[Dict] = None,
        vision_overlay: Optional[Dict] = None,
    ) -> List[str]:
        warnings = []
        mode_text = str(llm_mode)

        if config.FORCE_RULE_ONLY:
            warnings.append("FORCE_RULE_ONLY is enabled; this frame uses rule logic only.")

        if self.is_fallback_player:
            warnings.append(f"{self.player} is configured as a fallback/rule player.")

        if bool(getattr(self.llm_decider, "last_timed_out", False)):
            warnings.append("LLM request timed out on the most recent fresh call.")

        if str(getattr(self.llm_decider, "last_error", "")):
            warnings.append(
                "LLM error recorded: "
                + str(getattr(self.llm_decider, "last_error", ""))[:160]
            )

        if self.llm_temporarily_disabled:
            warnings.append("LLM is temporarily disabled after repeated timeouts.")

        if action_fallback_used:
            warnings.append("Action planner returned invalid actions; rule fallback actions were used.")

        if self._mode_implies_fallback(mode_text):
            warnings.append(f"LLM mode indicates fallback or non-fresh strategy: {mode_text}")

        if not units:
            warnings.append("No visible friendly units in this frame.")

        stuck_units = []
        for unit in units:
            try:
                stuck_count = int(unit.get("stuck_count", 0))
                if stuck_count >= int(config.STUCK_STEP_THRESHOLD):
                    stuck_units.append(f"u{unit.get('unit_id')}:{stuck_count}")
            except Exception:
                continue

        if stuck_units:
            warnings.append(
                "Potential stuck units: "
                + ", ".join(stuck_units[:8])
                + (" ..." if len(stuck_units) > 8 else "")
            )

        if memory_overlay:
            if not memory_overlay.get("known_relic_nodes"):
                warnings.append("No relic node has been memorized yet; exploration remains important.")

            if memory_overlay.get("relic_candidate_tiles") and not memory_overlay.get("confirmed_scoring_tiles"):
                warnings.append(
                    "Relic candidates exist, but no confirmed scoring tile has been identified yet."
                )

        if vision_overlay:
            if int(vision_overlay.get("visible_tiles_count", 0)) <= 0:
                warnings.append("No currently visible tiles recorded in sensor overlay.")

            if int(vision_overlay.get("energy_tiles_count", 0)) <= 0:
                warnings.append("No energy memory tiles have been recorded yet.")

        limit = int(getattr(config, "MAX_WARNINGS_IN_FRAME", 12))
        if len(warnings) > limit:
            kept = warnings[:limit]
            kept.append(f"{len(warnings) - limit} additional warnings hidden.")
            return kept

        return warnings

    def _clip_positions(self, positions, limit: int) -> List[List[int]]:
        """
        Convert a set/list of tuple-like positions into sorted JSON-safe lists.
        """
        cleaned = []

        try:
            iterable = list(positions)
        except Exception:
            iterable = []

        for pos in iterable:
            clean = self._clean_position(pos)
            if clean is not None:
                cleaned.append(clean)

        cleaned.sort(key=lambda item: (item[0], item[1]))

        if limit is None or int(limit) <= 0:
            return cleaned

        return cleaned[: int(limit)]

    def _clip_overlay_items(self, items, limit: int) -> List[Dict]:
        """
        Convert overlay item list into JSON-safe items with valid positions.
        """
        cleaned = []

        try:
            iterable = list(items)
        except Exception:
            iterable = []

        for item in iterable:
            if not isinstance(item, dict):
                continue

            pos = self._clean_position(item.get("pos"))
            if pos is None:
                continue

            new_item = dict(item)
            new_item["pos"] = pos
            cleaned.append(new_item)

        cleaned.sort(key=lambda item: (item["pos"][0], item["pos"][1]))

        if limit is None or int(limit) <= 0:
            return cleaned

        return cleaned[: int(limit)]

    def _clean_position(self, pos) -> Optional[List[int]]:
        """
        Return [x, y] if pos is a valid map coordinate, otherwise None.
        """
        if pos is None:
            return None

        try:
            x = int(pos[0])
            y = int(pos[1])
        except Exception:
            return None

        if not (0 <= x < self.map_width and 0 <= y < self.map_height):
            return None

        return [x, y]

    def _mode_implies_fallback(self, llm_mode: str) -> bool:
        text = str(llm_mode).lower()
        fallback_tokens = [
            "force_rule_only",
            "fallback_rule_player",
            "skip_llm_rule_fallback",
            "fresh_llm_empty_reuse_cache",
            "llm_disabled",
        ]
        return any(token in text for token in fallback_tokens)

    def _action_name(self, action_id: int) -> str:
        mapping = {
            config.ACTION_STAY: "STAY",
            config.ACTION_UP: "UP",
            config.ACTION_RIGHT: "RIGHT",
            config.ACTION_DOWN: "DOWN",
            config.ACTION_LEFT: "LEFT",
            config.ACTION_SAP: "SAP",
        }
        return mapping.get(int(action_id), f"UNKNOWN_{action_id}")