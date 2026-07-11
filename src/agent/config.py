"""
config.py

Central configuration for Lux LLM Agent.

Keep all tunable parameters here.

v0.9-E1 note:
- The main local LLM model is now qwen3:32b by default.
- Local small models are treated only as historical/lightweight references.
- Controlled experiments should use environment variables instead of editing code.
- This version adds ablation switches and trace-metric switches for EMNLP review evidence.
"""

import os


AGENT_VERSION = "v0.9-E1-qwen3-32b-trace-metrics"


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


def get_env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return float(default)

    try:
        return float(value)
    except Exception:
        return float(default)


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
RUNTIME_ROOT = os.path.abspath(os.getenv("LUX_RUN_DIR", PROJECT_ROOT))

LOG_DIR = os.path.join(RUNTIME_ROOT, "logs")
ERROR_LOG_DIR = os.path.join(RUNTIME_ROOT, "errorlogs")
REPLAY_DIR = os.path.join(RUNTIME_ROOT, "replays")

LLM_DECISION_LOG = os.path.join(LOG_DIR, "llm_decisions.jsonl")
AGENT_DEBUG_LOG = os.path.join(LOG_DIR, "agent_debug.log")
DECISION_TRACE_LOG = os.path.join(LOG_DIR, "decision_trace.jsonl")
ABLATION_METRICS_LOG = os.path.join(LOG_DIR, "ablation_metrics.jsonl")


# ============================================================
# Experiment identity
# ============================================================

# Recommended values:
#   rule_only
#   qwen3_32b_full
#   qwen3_32b_no_risk
#   qwen3_32b_no_cache
#   qwen3_32b_forced_fallback
EXPERIMENT_TAG = get_env_str("LUX_EXPERIMENT_TAG", "qwen3_32b_full")


# ============================================================
# Stability / ablation switches
# ============================================================

# True  = no LLM call at all, both players use fallback rule logic.
# False = player_0 uses LLM according to LLM_PLAYER, player_1 uses fallback.
#
# Controlled experiments can override this with:
#   LUX_FORCE_RULE_ONLY=1 or 0
FORCE_RULE_ONLY = get_env_bool("LUX_FORCE_RULE_ONLY", False)

# Force the LLM-side player to skip LLM decisions and use fallback logic.
# This is useful for ablation and sanity tests without changing player routing.
FORCE_FALLBACK = get_env_bool("LUX_FORCE_FALLBACK", False)


# ============================================================
# LLM settings
# ============================================================

LLM_ENABLED = get_env_bool("LUX_LLM_ENABLED", True)

# Only this player is allowed to call LLM when FORCE_RULE_ONLY is False.
LLM_PLAYER = get_env_str("LUX_LLM_PLAYER", "player_0")

# This player always uses fallback rule logic.
FALLBACK_PLAYER = get_env_str("LUX_FALLBACK_PLAYER", "player_1")

# Local Ollama model settings.
# v0.9-E1 main model:
#   qwen3:32b
LLM_MODEL = get_env_str("LUX_LLM_MODEL", "qwen3:32b")
LLM_BASE_URL = get_env_str("LUX_LLM_BASE_URL", "http://127.0.0.1:11434")

# Keep timeout configurable.
# For qwen3:32b on Barkla2, this may need to be higher than local small models.
LLM_TIMEOUT_SECONDS = get_env_float("LUX_LLM_TIMEOUT_SECONDS", 12.0)
LLM_TEMPERATURE = get_env_float("LUX_LLM_TEMPERATURE", 0.1)
LLM_SEED = get_env_int("LUX_LLM_SEED", 42)
LLM_NUM_PREDICT = get_env_int("LUX_LLM_NUM_PREDICT", 384)
# Qwen3 enables a separate reasoning trace by default in Ollama.  Strategic
# decisions need a short machine-readable answer, so reproducible experiments
# disable that trace and request JSON output explicitly.
LLM_THINK = get_env_bool("LUX_LLM_THINK", False)
LLM_JSON_MODE = get_env_bool("LUX_LLM_JSON_MODE", True)

# If the LLM fails or returns invalid JSON, rule policy takes over.
ENABLE_RULE_FALLBACK = get_env_bool("LUX_ENABLE_RULE_FALLBACK", True)


# ============================================================
# LLM speed / cache control
# ============================================================

# LLM is a strategic planner, not a per-frame action controller.
LLM_CALL_INTERVAL = get_env_int("LUX_LLM_CALL_INTERVAL", 30)

# Early strategic thinking steps.
LLM_CALL_EARLY_STEPS = {0}

# Reuse the last valid LLM intents between LLM calls.
LLM_REUSE_LAST_INTENTS = get_env_bool("LUX_LLM_REUSE_LAST_INTENTS", True)

# New explicit cache switch for ablation.
ENABLE_STRATEGY_CACHE = get_env_bool("LUX_ENABLE_STRATEGY_CACHE", True)

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
# Debug / trace switches
# ============================================================

PRINT_AGENT_DEBUG = get_env_bool("LUX_PRINT_AGENT_DEBUG", True)

ENABLE_FRAME_LOGGING = get_env_bool("LUX_ENABLE_FRAME_LOGGING", True)
FRAME_LOG_PATH = os.path.join(LOG_DIR, "frame_log.jsonl")
VIEWER_FRAMES_PATH = os.path.join(LOG_DIR, "viewer_frames.json")
VIEWER_FRAME_SCHEMA_VERSION = "lux_s3_viewer_frames_v1"

# New trace switches for EMNLP evidence.
LOG_DECISION_TRACE = get_env_bool("LUX_LOG_DECISION_TRACE", True)
LOG_LLM_LATENCY = get_env_bool("LUX_LOG_LLM_LATENCY", True)
LOG_ABLATION_METRICS = get_env_bool("LUX_LOG_ABLATION_METRICS", True)


# ============================================================
# Risk-aware action filter
# ============================================================

# v0.9-E1:
# This must be environment-controlled so that we can run:
#   qwen3_32b_full
#   qwen3_32b_no_risk
ENABLE_RISK_AWARE_ACTION_FILTER = get_env_bool(
    "LUX_ENABLE_RISK_AWARE_ACTION_FILTER",
    True,
)

RISK_AWARE_TARGET_ENEMY_RADIUS = get_env_int(
    "LUX_RISK_AWARE_TARGET_ENEMY_RADIUS",
    4,
)

RISK_AWARE_STALE_TARGET_LIMIT = get_env_int(
    "LUX_RISK_AWARE_STALE_TARGET_LIMIT",
    20,
)
