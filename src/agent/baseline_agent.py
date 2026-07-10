"""Rule-only entry point for Lux AI Season 3 local smoke tests.

This module intentionally reuses the production ``main.py`` protocol instead
of maintaining a second, incompatible parser.  Environment variables must be
set before importing ``main`` because the agent configuration is loaded at
import time.
"""

import os


os.environ.setdefault("LUX_FORCE_RULE_ONLY", "1")
os.environ.setdefault("LUX_LLM_ENABLED", "0")
os.environ.setdefault("LUX_EXPERIMENT_TAG", "rule_only_baseline")

from main import main  # noqa: E402  (configuration must be set first)


if __name__ == "__main__":
    main()
