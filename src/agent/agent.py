import json
import os
import sys
import time
from typing import Dict, List, Optional, Tuple

import config
from action_planner import build_actions_from_intents, make_empty_actions
from game_memory import GameMemory
from jsonl_io import append_jsonl_atomic
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
            and (not getattr(config, "FORCE_FALLBACK", False))
            and config.LLM_ENABLED
            and config.llm_enabled_for_player(self.player)
        )

        self.is_fallback_player = not self.llm_enabled_for_this_player
        self.llm_model = config.llm_model_for_player(self.player)
        self.llm_base_url = config.llm_base_url_for_player(self.player)
        self.log_dir = config.log_dir_for_player(self.player)
        self.error_log_dir = config.error_log_dir_for_player(self.player)
        self.replay_dir = config.replay_dir_for_player(self.player)
        self.agent_debug_log = os.path.join(self.log_dir, "agent_debug.log")
        self.decision_trace_log = os.path.join(self.log_dir, "decision_trace.jsonl")
        self.ablation_metrics_log = os.path.join(self.log_dir, "ablation_metrics.jsonl")
        self.frame_log_path = os.path.join(self.log_dir, "frame_log.jsonl")

        self.llm_decider = LLMDecider(
            model=self.llm_model,
            base_url=self.llm_base_url,
            enabled=self.llm_enabled_for_this_player,
            player=self.player,
            log_dir=self.log_dir,
            error_log_dir=self.error_log_dir,
        )

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
                "experiment_tag": getattr(config, "EXPERIMENT_TAG", "unknown"),
                "decision_method": getattr(config, "DECISION_METHOD", "dtav"),
                "normalize_llm_output": bool(
                    getattr(config, "NORMALIZE_LLM_OUTPUT", True)
                ),
                "player": self.player,
                "team_id": self.team_id,
                "env_cfg": self.env_cfg,
                "force_rule_only": config.FORCE_RULE_ONLY,
                "force_fallback": bool(getattr(config, "FORCE_FALLBACK", False)),
                "enable_strategy_cache": bool(getattr(config, "ENABLE_STRATEGY_CACHE", True)),
                "enable_risk_filter": bool(getattr(config, "ENABLE_RISK_AWARE_ACTION_FILTER", True)),
                "llm_enabled_for_this_player": self.llm_enabled_for_this_player,
                "is_fallback_player": self.is_fallback_player,
                "llm_player": config.LLM_PLAYER,
                "fallback_player": config.FALLBACK_PLAYER,
                "llm_players": os.getenv("LUX_LLM_PLAYERS"),
                "llm_model": self.llm_model,
                "llm_base_url": self.llm_base_url,
                "frame_logging": bool(getattr(config, "ENABLE_FRAME_LOGGING", False)),
                "frame_log_path": self.frame_log_path,
                "decision_trace_log": self.decision_trace_log,
                "ablation_metrics_log": self.ablation_metrics_log,
            }
        )

        print(
            f"[Lux LLM Agent {config.AGENT_VERSION}] "
            f"Agent initialized. player={self.player}, team_id={self.team_id}, "
            f"experiment_tag={getattr(config, 'EXPERIMENT_TAG', 'unknown')}, "
            f"decision_method={getattr(config, 'DECISION_METHOD', 'dtav')}, "
            f"force_rule_only={config.FORCE_RULE_ONLY}, "
            f"force_fallback={getattr(config, 'FORCE_FALLBACK', False)}, "
            f"llm_enabled_for_this_player={self.llm_enabled_for_this_player}, "
            f"is_fallback_player={self.is_fallback_player}, "
            f"llm_player={config.LLM_PLAYER}, fallback_player={config.FALLBACK_PLAYER}, "
            f"model={self.llm_model}",
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

            decision_trace = self._build_step_decision_trace(
                step=step,
                gameview=gameview,
                match_context=match_context,
                llm_intents=llm_intents,
                llm_mode=llm_mode,
                actions=actions,
                elapsed=elapsed,
                action_fallback_used=action_fallback_used,
            )

            self._log_debug(
                {
                    "event": "act",
                    "step": int(step),
                    "elapsed": elapsed,
                    "player": self.player,
                    "team_id": self.team_id,
                    "experiment_tag": getattr(config, "EXPERIMENT_TAG", "unknown"),
                    "force_rule_only": config.FORCE_RULE_ONLY,
                    "force_fallback": bool(getattr(config, "FORCE_FALLBACK", False)),
                    "llm_mode": llm_mode,
                    "decision_trace": decision_trace,
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
                decision_trace=decision_trace,
            )

            self._write_step_trace_logs(decision_trace)

            return actions

        except Exception as exc:
            self._log_debug(
                {
                    "event": "act_error",
                    "step": int(step),
                    "player": self.player,
                    "force_rule_only": config.FORCE_RULE_ONLY,
                    "force_fallback": bool(getattr(config, "FORCE_FALLBACK", False)),
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

        The returned llm_mode is intentionally explicit because it becomes part
        of the paper-facing decision provenance trace.
        """
        if config.FORCE_RULE_ONLY:
            return {"unit_intents": {}}, "force_rule_only"

        if bool(getattr(config, "FORCE_FALLBACK", False)):
            return {"unit_intents": {}}, "forced_fallback"

        if not self.llm_enabled_for_this_player:
            return {"unit_intents": {}}, "fallback_rule_player"

        my_units = gameview.get("my_units", []) if isinstance(gameview, dict) else []
        if not isinstance(my_units, list) or not my_units:
            return {"unit_intents": {}}, "skip_llm_rule_fallback:no_active_units"

        cache_enabled = bool(getattr(config, "ENABLE_STRATEGY_CACHE", True))
        reuse_enabled = bool(getattr(config, "LLM_REUSE_LAST_INTENTS", True))

        if self.llm_temporarily_disabled:
            if cache_enabled and reuse_enabled:
                return self.last_llm_intents, "llm_disabled_after_timeouts_reuse_cache"
            return {"unit_intents": {}}, "llm_disabled_after_timeouts_rule_fallback"

        should_call, reason = self._should_call_llm(
            step=step,
            gameview=gameview,
            match_context=match_context,
        )

        if not should_call:
            if cache_enabled and reuse_enabled and self._has_cached_llm_intents():
                return self.last_llm_intents, f"reuse_cached_llm_intents:{reason}"

            if not cache_enabled:
                return {"unit_intents": {}}, f"skip_llm_no_cache_rule_fallback:{reason}"

            return {"unit_intents": {}}, f"skip_llm_rule_fallback:{reason}"

        intents = self.llm_decider.decide(gameview)

        timed_out = bool(getattr(self.llm_decider, "last_timed_out", False))
        error_text = str(getattr(self.llm_decider, "last_error", ""))

        if isinstance(intents, dict):
            error_text += " " + str(intents.get("error", ""))

        if "timed out" in error_text.lower() or "timeout" in error_text.lower():
            timed_out = True

        if timed_out:
            self.consecutive_llm_timeouts += 1
        else:
            self.consecutive_llm_timeouts = 0

        if self.consecutive_llm_timeouts >= config.LLM_DISABLE_AFTER_TIMEOUTS:
            self.llm_temporarily_disabled = True

            if cache_enabled and reuse_enabled and self._has_cached_llm_intents():
                return self.last_llm_intents, "llm_disabled_after_timeout_limit_reuse_cache"

            return {"unit_intents": {}}, "llm_disabled_after_timeout_limit_rule_fallback"

        if isinstance(intents, dict) and isinstance(intents.get("unit_intents"), dict):
            if intents.get("unit_intents"):
                self.last_llm_intents = intents
                self.last_llm_step = int(step)
                return intents, f"fresh_llm_call:{reason}"

        if cache_enabled and reuse_enabled and self._has_cached_llm_intents():
            return self.last_llm_intents, f"fresh_llm_empty_reuse_cache:{reason}"

        return {"unit_intents": {}}, f"fresh_llm_empty_rule_fallback:{reason}"

    def _has_cached_llm_intents(self) -> bool:
        try:
            if not isinstance(self.last_llm_intents, dict):
                return False

            unit_intents = self.last_llm_intents.get("unit_intents", {})
            return isinstance(unit_intents, dict) and bool(unit_intents)
        except Exception:
            return False

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
        os.makedirs(self.log_dir, exist_ok=True)
        os.makedirs(self.error_log_dir, exist_ok=True)
        os.makedirs(self.replay_dir, exist_ok=True)

        if hasattr(config, "VIEW_DIR"):
            os.makedirs(config.VIEW_DIR, exist_ok=True)

        if hasattr(config, "DOCS_DIR"):
            os.makedirs(config.DOCS_DIR, exist_ok=True)

    def _log_debug(self, data: Dict) -> None:
        try:
            append_jsonl_atomic(self.agent_debug_log, data)
        except Exception:
            pass

    def _append_jsonl(self, path: str, data: Dict) -> None:
        try:
            append_jsonl_atomic(path, data)
        except Exception:
            pass

    def _build_step_decision_trace(
        self,
        step: int,
        gameview: Dict,
        match_context: Dict,
        llm_intents: Dict,
        llm_mode: str,
        actions: List[List[int]],
        elapsed: float,
        action_fallback_used: bool,
    ) -> Dict:
        """
        Build a per-frame decision provenance record.

        This is the main evidence object for:
        - ablation statistics,
        - LLM latency analysis,
        - fallback analysis,
        - trace/replay alignment,
        - paper case studies.
        """
        score = gameview.get("score", {}) if isinstance(gameview, dict) else {}
        my_points = int(score.get("my_points", 0))
        opp_points = int(score.get("opp_points", 0))

        if self.team_id == 0:
            score_player_0 = my_points
            score_player_1 = opp_points
        else:
            score_player_0 = opp_points
            score_player_1 = my_points

        risk_summary = self._build_frame_risk_filter()
        risk_events = risk_summary.get("events", [])
        if not isinstance(risk_events, list):
            risk_events = []

        risk_filter_changed = int(risk_summary.get("changed_targets", 0)) > 0
        risk_filter_reason = self._risk_filter_reason_from_summary(risk_summary)

        unit_intents = {}
        if isinstance(llm_intents, dict) and isinstance(llm_intents.get("unit_intents"), dict):
            unit_intents = llm_intents.get("unit_intents", {})

        llm_called = self._mode_has_fresh_llm_call(llm_mode)
        cache_used = self._mode_uses_cache(llm_mode)
        stale_decision = self._mode_is_stale_or_cached(step=step, llm_mode=llm_mode)
        decision_source = self._infer_step_decision_source(
            llm_mode=llm_mode,
            action_fallback_used=action_fallback_used,
            cache_used=cache_used,
        )

        fallback_reason = self._infer_step_fallback_reason(
            llm_mode=llm_mode,
            action_fallback_used=action_fallback_used,
        )

        llm_latency_seconds = 0.0
        llm_latency_ms = 0.0
        llm_valid = False
        llm_error = None
        timed_out = False

        if llm_called:
            llm_latency_seconds = float(getattr(self.llm_decider, "last_elapsed", 0.0))
            llm_latency_ms = round(llm_latency_seconds * 1000.0, 3)
            llm_valid = bool(getattr(self.llm_decider, "last_valid", False))
            llm_error_text = str(getattr(self.llm_decider, "last_error", ""))
            llm_error = llm_error_text or None
            timed_out = bool(getattr(self.llm_decider, "last_timed_out", False))
        elif cache_used:
            llm_valid = True

        active_action_count = self._count_active_actions(actions)

        return {
            "time": time.time(),
            "event": "agent_step_trace",
            "agent_version": config.AGENT_VERSION,
            "experiment_tag": getattr(config, "EXPERIMENT_TAG", "unknown"),
            "decision_method": getattr(config, "DECISION_METHOD", "dtav"),
            "step": int(step),
            "match_idx": int(match_context.get("match_idx", 0)),
            "step_in_match": int(match_context.get("step_in_match", 0)),
            "phase": str(match_context.get("phase", "unknown")),
            "player": self.player,
            "team_id": int(self.team_id),

            "decision_source": decision_source,
            "llm_mode": str(llm_mode),
            "llm_enabled": bool(self.llm_enabled_for_this_player),
            "llm_model": self.llm_model,
            "llm_called": bool(llm_called),
            "llm_latency_ms": float(llm_latency_ms),
            "llm_latency_seconds": float(llm_latency_seconds),
            "llm_valid": bool(llm_valid),
            "llm_error": llm_error,
            "timed_out": bool(timed_out),

            "fallback_used": bool(self._mode_implies_fallback(llm_mode) or action_fallback_used),
            "fallback_reason": fallback_reason,
            "action_fallback_used": bool(action_fallback_used),

            "cache_enabled": bool(getattr(config, "ENABLE_STRATEGY_CACHE", True)),
            "cache_used": bool(cache_used),
            "stale_decision": bool(stale_decision),
            "last_llm_step": int(self.last_llm_step),

            "risk_filter_enabled": bool(risk_summary.get("enabled", False)),
            "risk_filter_changed": bool(risk_filter_changed),
            "risk_filter_reason": risk_filter_reason,
            "risk_filter_changed_targets": int(risk_summary.get("changed_targets", 0)),
            "risk_filter_evaluated_units": int(risk_summary.get("evaluated_units", 0)),
            "risk_filter_visible_enemy_units": int(risk_summary.get("visible_enemy_units", 0)),
            "risk_filter_events_count": int(len(risk_events)),

            "unit_intent_count": int(len(unit_intents)),
            "unit_action_count": int(len(actions)) if isinstance(actions, list) else 0,
            "active_action_count": int(active_action_count),

            "score_player_0": int(score_player_0),
            "score_player_1": int(score_player_1),
            "score_diff_player_0_minus_player_1": int(score_player_0 - score_player_1),
            "my_points": int(my_points),
            "opp_points": int(opp_points),

            "elapsed_total_ms": round(float(elapsed) * 1000.0, 3),
            "remaining_overage_note": (
                "remainingOverageTime is not logged here because the official "
                "act() call does not require it for paper-level trace analysis."
            ),
        }

    def _write_step_trace_logs(self, decision_trace: Dict) -> None:
        """
        Write per-action-step trace and ablation metrics.

        llm_decider.py writes LLM-call-level records. This method writes
        frame/action-step-level records, including cached and fallback steps.
        """
        if bool(getattr(config, "LOG_DECISION_TRACE", True)):
            self._append_jsonl(self.decision_trace_log, decision_trace)

        if bool(getattr(config, "LOG_ABLATION_METRICS", True)):
            metrics_record = {
                "time": decision_trace.get("time", time.time()),
                "event": "agent_step_metrics",
                "agent_version": decision_trace.get("agent_version"),
                "experiment_tag": decision_trace.get("experiment_tag"),
                "step": decision_trace.get("step"),
                "match_idx": decision_trace.get("match_idx"),
                "step_in_match": decision_trace.get("step_in_match"),
                "player": decision_trace.get("player"),
                "decision_source": decision_trace.get("decision_source"),
                "llm_model": decision_trace.get("llm_model"),
                "llm_called": decision_trace.get("llm_called"),
                "llm_latency_ms": decision_trace.get("llm_latency_ms"),
                "llm_valid": decision_trace.get("llm_valid"),
                "timed_out": decision_trace.get("timed_out"),
                "fallback_used": decision_trace.get("fallback_used"),
                "fallback_reason": decision_trace.get("fallback_reason"),
                "cache_used": decision_trace.get("cache_used"),
                "stale_decision": decision_trace.get("stale_decision"),
                "risk_filter_enabled": decision_trace.get("risk_filter_enabled"),
                "risk_filter_changed": decision_trace.get("risk_filter_changed"),
                "risk_filter_changed_targets": decision_trace.get("risk_filter_changed_targets"),
                "unit_intent_count": decision_trace.get("unit_intent_count"),
                "unit_action_count": decision_trace.get("unit_action_count"),
                "active_action_count": decision_trace.get("active_action_count"),
                "score_player_0": decision_trace.get("score_player_0"),
                "score_player_1": decision_trace.get("score_player_1"),
                "elapsed_total_ms": decision_trace.get("elapsed_total_ms"),
            }
            self._append_jsonl(self.ablation_metrics_log, metrics_record)

    def _mode_has_fresh_llm_call(self, llm_mode: str) -> bool:
        text = str(llm_mode).lower()
        return text.startswith("fresh_llm_call") or text.startswith("fresh_llm_empty")

    def _mode_uses_cache(self, llm_mode: str) -> bool:
        text = str(llm_mode).lower()
        cache_tokens = [
            "reuse_cached_llm_intents",
            "fresh_llm_empty_reuse_cache",
            "llm_disabled_after_timeouts_reuse_cache",
            "llm_disabled_after_timeout_limit_reuse_cache",
        ]
        return any(token in text for token in cache_tokens)

    def _mode_is_stale_or_cached(self, step: int, llm_mode: str) -> bool:
        if not self._mode_uses_cache(llm_mode):
            return False

        try:
            return int(step) > int(self.last_llm_step)
        except Exception:
            return True

    def _infer_step_decision_source(
        self,
        llm_mode: str,
        action_fallback_used: bool,
        cache_used: bool,
    ) -> str:
        text = str(llm_mode).lower()

        if config.FORCE_RULE_ONLY:
            return "rule_only"

        if bool(getattr(config, "FORCE_FALLBACK", False)):
            return "forced_fallback"

        if action_fallback_used:
            return "action_fallback"

        if cache_used:
            return "cached_llm"

        if text.startswith("fresh_llm_call"):
            return "llm_fresh"

        if text.startswith("fresh_llm_empty"):
            return "fallback"

        if "fallback_rule_player" in text:
            return "rule_player"

        if "skip_llm_no_cache_rule_fallback" in text:
            return "rule_fallback_no_cache"

        if "skip_llm_rule_fallback" in text:
            return "rule_fallback"

        if "llm_disabled" in text:
            return "fallback"

        if "force_rule_only" in text:
            return "rule_only"

        if "forced_fallback" in text:
            return "forced_fallback"

        return "unknown"

    def _infer_step_fallback_reason(
        self,
        llm_mode: str,
        action_fallback_used: bool,
    ) -> Optional[str]:
        text = str(llm_mode)

        if action_fallback_used:
            return "invalid_action_output"

        if config.FORCE_RULE_ONLY:
            return "force_rule_only"

        if bool(getattr(config, "FORCE_FALLBACK", False)):
            return "force_fallback"

        if text.startswith("fallback_rule_player"):
            return "configured_fallback_player"

        if text.startswith("skip_llm_no_cache_rule_fallback"):
            return "llm_not_called_cache_disabled"

        if text.startswith("skip_llm_rule_fallback"):
            return "llm_not_called_no_valid_cache"

        if text.startswith("fresh_llm_empty_rule_fallback"):
            reason = getattr(self.llm_decider, "last_fallback_reason", None)
            return reason or "fresh_llm_empty_or_invalid"

        if text.startswith("fresh_llm_empty_reuse_cache"):
            reason = getattr(self.llm_decider, "last_fallback_reason", None)
            return reason or "fresh_llm_empty_reused_cache"

        if "llm_disabled_after_timeout" in text:
            return "llm_disabled_after_timeouts"

        if self._mode_implies_fallback(text):
            return text

        return None

    def _count_active_actions(self, actions: List[List[int]]) -> int:
        if not isinstance(actions, list):
            return 0

        count = 0
        for action in actions:
            try:
                if not isinstance(action, list) or len(action) != 3:
                    continue

                action_type = int(action[0])
                dx = int(action[1])
                dy = int(action[2])

                if action_type != config.ACTION_STAY or dx != 0 or dy != 0:
                    count += 1
            except Exception:
                continue

        return count

    def _risk_filter_reason_from_summary(self, risk_summary: Dict) -> Optional[str]:
        try:
            if not isinstance(risk_summary, dict):
                return None

            events = risk_summary.get("events", [])
            if not isinstance(events, list):
                return None

            changed_reasons = []
            for event in events:
                if not isinstance(event, dict):
                    continue

                if bool(event.get("changed", False)):
                    reason = str(event.get("reason", "")).strip()
                    if reason:
                        changed_reasons.append(reason)

            if changed_reasons:
                return "; ".join(changed_reasons[:3])

            if int(risk_summary.get("evaluated_units", 0)) > 0:
                return "risk filter evaluated targets without changing them"

            return None
        except Exception:
            return None

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
        decision_trace: Optional[Dict] = None,
    ) -> None:
        """
        Write one compact explanation frame for the log-driven viewer.

        This function must never affect the official action output.
        Any failure is swallowed so logging cannot crash the Lux runner.
        """
        if not bool(getattr(config, "ENABLE_FRAME_LOGGING", False)):
            return

        try:
            os.makedirs(self.log_dir, exist_ok=True)

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

            risk_filter = self._build_frame_risk_filter()

            if decision_trace is None:
                decision_trace = self._build_step_decision_trace(
                    step=step,
                    gameview=gameview,
                    match_context=match_context,
                    llm_intents=llm_intents,
                    llm_mode=llm_mode,
                    actions=actions,
                    elapsed=elapsed,
                    action_fallback_used=action_fallback_used,
                )

            frame = {
                "schema_version": getattr(
                    config,
                    "VIEWER_FRAME_SCHEMA_VERSION",
                    "lux_s3_viewer_frames_v1",
                ),
                "agent_version": config.AGENT_VERSION,
                "experiment_tag": getattr(config, "EXPERIMENT_TAG", "unknown"),
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
                "decision_trace": decision_trace,
                "llm": {
                    "enabled_for_player": bool(self.llm_enabled_for_this_player),
                    "is_fallback_player": bool(self.is_fallback_player),
                    "model": self.llm_model,
                    "called": bool(decision_trace.get("llm_called", False)),
                    "elapsed": float(decision_trace.get("llm_latency_seconds", 0.0)),
                    "latency_ms": float(decision_trace.get("llm_latency_ms", 0.0)),
                    "valid": bool(decision_trace.get("llm_valid", False)),
                    "timed_out": bool(decision_trace.get("timed_out", False)),
                    "error": decision_trace.get("llm_error") or "",
                    "fallback_used": bool(decision_trace.get("fallback_used", False)),
                    "fallback_reason": decision_trace.get("fallback_reason"),
                    "decision_source": decision_trace.get("decision_source"),
                    "cache_used": bool(decision_trace.get("cache_used", False)),
                    "stale_decision": bool(decision_trace.get("stale_decision", False)),
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
                "risk_filter": risk_filter,
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

            append_jsonl_atomic(self.frame_log_path, frame)

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
            "events_count": 0,
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

        if bool(getattr(config, "FORCE_FALLBACK", False)):
            warnings.append("FORCE_FALLBACK is enabled; this frame skips LLM decisions.")

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

        if self._mode_uses_cache(mode_text):
            warnings.append(f"Cached LLM strategy is reused: {mode_text}")

        if not bool(getattr(config, "ENABLE_STRATEGY_CACHE", True)):
            warnings.append("Strategy cache is disabled for this ablation run.")

        if not bool(getattr(config, "ENABLE_RISK_AWARE_ACTION_FILTER", True)):
            warnings.append("Risk-aware action filter is disabled for this ablation run.")

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
            "forced_fallback",
            "fallback_rule_player",
            "skip_llm_rule_fallback",
            "skip_llm_no_cache_rule_fallback",
            "fresh_llm_empty_rule_fallback",
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
