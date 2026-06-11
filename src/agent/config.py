"""
config.py

Central configuration for Lux LLM Agent.

Keep all tunable parameters here.

v0.9-D2 note:
- Controlled experiments use environment variables to switch between
  rule-only, qwen2.5:1.5b, and qwen2.5:7b without editing this file.
"""

import os


AGENT_VERSION = "v0.9-D2-controlled-runner"


# ============================================================
# Environment variable helpers
# ============================================================


def get_env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return bool(default)

    value = value.strip().lower()
    if value in ("1", "true", "yes", "y", "on"):
        return True
    if value in ("0", "false", "no", "n", "off"):
        return False

    return bool(default)


def get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return int(default)

    try:
        return int(value)
    except Exception:
        return int(default)


def get_env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return str(default)

    value = value.strip()
    if not value:
        return str(default)

    return value


# ============================================================
# Project paths
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(PROJECT_ROOT, "logs")
ERROR_LOG_DIR = os.path.join(PROJECT_ROOT, "errorlogs")
REPLAY_DIR = os.path.join(PROJECT_ROOT, "replays")

LLM_DECISION_LOG = os.path.join(LOG_DIR, "llm_decisions.jsonl")
AGENT_DEBUG_LOG = os.path.join(LOG_DIR, "agent_debug.log")


# ============================================================
# Stability test switch
# ============================================================

# True  = no LLM call at all, both players use fallback rule logic.
# False = player_0 uses LLM according to LLM_PLAYER, player_1 uses fallback.
#
# v0.9-D2 controlled runner can override this with:
#   LUX_FORCE_RULE_ONLY=1 or 0
FORCE_RULE_ONLY = get_env_bool("LUX_FORCE_RULE_ONLY", False)


# ============================================================
# LLM settings
# ============================================================

LLM_ENABLED = get_env_bool("LUX_LLM_ENABLED", True)

# Only this player is allowed to call LLM when FORCE_RULE_ONLY is False.
LLM_PLAYER = get_env_str("LUX_LLM_PLAYER", "player_0")

# This player always uses fallback rule logic.
FALLBACK_PLAYER = get_env_str("LUX_FALLBACK_PLAYER", "player_1")

# Local Ollama model settings.
LLM_MODEL = get_env_str("LUX_LLM_MODEL", "qwen2.5:1.5b")
LLM_BASE_URL = get_env_str("LUX_LLM_BASE_URL", "http://127.0.0.1:11434")

# Keep timeout moderate.
# If this is too high, the Lux runner looks frozen.
# If this is too low, the model may never answer.
LLM_TIMEOUT_SECONDS = get_env_int("LUX_LLM_TIMEOUT_SECONDS", 8)

# If the LLM fails or returns invalid JSON, rule policy takes over.
ENABLE_RULE_FALLBACK = get_env_bool("LUX_ENABLE_RULE_FALLBACK", True)


# ============================================================
# LLM speed control
# ============================================================

# LLM is a strategic planner, not a per-frame action controller.
LLM_CALL_INTERVAL = get_env_int("LUX_LLM_CALL_INTERVAL", 30)

# Early strategic thinking steps.
LLM_CALL_EARLY_STEPS = {0}

# Reuse the last valid LLM intents between LLM calls.
LLM_REUSE_LAST_INTENTS = get_env_bool("LUX_LLM_REUSE_LAST_INTENTS", True)

# Disable LLM after repeated timeouts.
LLM_DISABLE_AFTER_TIMEOUTS = get_env_int("LUX_LLM_DISABLE_AFTER_TIMEOUTS", 3)


# ============================================================
# Official Lux S3 defaults
# ============================================================

MAP_WIDTH = 24
MAP_HEIGHT = 24


# ============================================================
# Feature switches
# ============================================================

ENABLE_ROUND_AWARE = get_env_bool("LUX_ENABLE_ROUND_AWARE", True)
ENABLE_STALE_TILE_GUARD = get_env_bool("LUX_ENABLE_STALE_TILE_GUARD", True)
ENABLE_RELIC_CANDIDATE_MEMORY = get_env_bool("LUX_ENABLE_RELIC_CANDIDATE_MEMORY", True)

# Keep SAP conservative for this version.
ENABLE_SAP = get_env_bool("LUX_ENABLE_SAP", False)


# ============================================================
# Planning parameters
# ============================================================

LOW_ENERGY_THRESHOLD = get_env_int("LUX_LOW_ENERGY_THRESHOLD", 20)
SAFE_ENERGY_THRESHOLD = get_env_int("LUX_SAFE_ENERGY_THRESHOLD", 35)
STUCK_STEP_THRESHOLD = get_env_int("LUX_STUCK_STEP_THRESHOLD", 3)

MAX_STALE_TARGETS_IN_GAMEVIEW = get_env_int("LUX_MAX_STALE_TARGETS_IN_GAMEVIEW", 10)
MAX_RELIC_TARGETS_IN_GAMEVIEW = get_env_int("LUX_MAX_RELIC_TARGETS_IN_GAMEVIEW", 20)


# ============================================================
# Official Lux action ids
# ============================================================

ACTION_STAY = 0
ACTION_UP = 1
ACTION_RIGHT = 2
ACTION_DOWN = 3
ACTION_LEFT = 4
ACTION_SAP = 5


# ============================================================
# Debug switch
# ============================================================

PRINT_AGENT_DEBUG = get_env_bool("LUX_PRINT_AGENT_DEBUG", True)
ENABLE_FRAME_LOGGING = True
FRAME_LOG_PATH = os.path.join(LOG_DIR, "frame_log.jsonl")
VIEWER_FRAMES_PATH = os.path.join(LOG_DIR, "viewer_frames.json")
VIEWER_FRAME_SCHEMA_VERSION = "lux_s3_viewer_frames_v1"


# v0.9-J3-A risk-aware action filter
ENABLE_RISK_AWARE_ACTION_FILTER = True
RISK_AWARE_TARGET_ENEMY_RADIUS = 4
RISK_AWARE_STALE_TARGET_LIMIT = 20