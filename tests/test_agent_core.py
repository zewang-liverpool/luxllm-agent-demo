import os
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "agent"))

os.environ.setdefault("LUX_RUN_DIR", str(ROOT / "results" / "test-runtime"))

from action_planner import make_empty_actions
import config
from llm_decider import (
    build_ollama_payload,
    extract_json_object,
    extract_ollama_response,
    infer_fallback_reason,
    has_valid_strategy,
    normalize_unit_intent_keys,
)
from lux_state import parse_units
from state_summarizer import gameview_to_prompt


class AgentCoreTests(unittest.TestCase):
    @mock.patch.dict(
        os.environ,
        {
            "LUX_LLM_PLAYERS": "player_0,player_1",
            "LUX_PLAYER_0_LLM_MODEL": "qwen3:32b",
            "LUX_PLAYER_1_LLM_MODEL": "deepseek-r1:32b",
        },
    )
    def test_dual_llm_player_routing_and_models_are_independent(self):
        self.assertTrue(config.llm_enabled_for_player("player_0"))
        self.assertTrue(config.llm_enabled_for_player("player_1"))
        self.assertEqual(config.llm_model_for_player("player_0"), "qwen3:32b")
        self.assertEqual(config.llm_model_for_player("player_1"), "deepseek-r1:32b")

    @mock.patch.dict(
        os.environ,
        {
            "LUX_LLM_PLAYERS": "player_0,player_1",
            "LUX_PLAYER_1_LLM_ENABLED": "0",
        },
    )
    def test_explicit_player_disable_overrides_dual_player_list(self):
        self.assertTrue(config.llm_enabled_for_player("player_0"))
        self.assertFalse(config.llm_enabled_for_player("player_1"))

    def test_parse_units_accepts_official_nested_energy_shape(self):
        observation = {
            "units": {
                "position": [[[[3, 4]][0]], [[[20, 21]][0]]],
                "energy": [[[75]], [[60]]],
            },
            "units_mask": [[True], [True]],
        }
        self.assertEqual(parse_units(observation, 0), [{"unit_id": 0, "pos": (3, 4), "energy": 75}])

    def test_prompt_uses_actual_player_role(self):
        prompt = gameview_to_prompt(
            {
                "player": "player_1",
                "team_id": 1,
                "step": 0,
                "match": {},
                "score": {},
                "memory": {},
                "my_units": [],
                "visible_enemies": [],
                "visible_relics": [],
            }
        )
        self.assertIn("You control player_1", prompt)
        self.assertNotIn("You control player_0", prompt)

    def test_llm_json_extraction_handles_markdown_wrapper(self):
        parsed = extract_json_object('answer: {"unit_intents":{"0":{"intent":"HOLD_POSITION"}}}')
        self.assertEqual(parsed["unit_intents"]["0"]["intent"], "HOLD_POSITION")

    def test_ollama_payload_disables_thinking_and_requests_json(self):
        payload = build_ollama_payload("qwen3:32b", "choose an intent")
        self.assertFalse(payload["think"])
        self.assertEqual(payload["format"], "json")
        self.assertFalse(payload["stream"])

    def test_reasoning_only_ollama_response_is_an_explicit_error(self):
        with self.assertRaisesRegex(RuntimeError, "thinking but no final response"):
            extract_ollama_response(
                {
                    "response": "",
                    "thinking": "still reasoning",
                    "done_reason": "length",
                    "eval_count": 120,
                }
            )

    def test_prefixed_unit_keys_are_normalized_for_the_planner(self):
        parsed = normalize_unit_intent_keys(
            {"unit_intents": {"u3": {"intent": "HOLD_POSITION"}}}
        )
        self.assertEqual(
            parsed,
            {"unit_intents": {"3": {"intent": "HOLD_POSITION"}}},
        )

    def test_string_intent_shorthand_is_normalized_for_the_planner(self):
        parsed = normalize_unit_intent_keys(
            {"unit_intents": {"0": "EXPLORE_STALE_TILE"}}
        )
        self.assertEqual(
            parsed["unit_intents"]["0"]["intent"],
            "EXPLORE_STALE_TILE",
        )

    def test_unknown_intent_is_not_counted_as_valid_strategy(self):
        self.assertFalse(
            has_valid_strategy(
                {"unit_intents": {"0": {"intent": "INVENT_A_NEW_ACTION"}}}
            )
        )

    def test_non_numeric_unit_key_requires_dtav_normalization(self):
        self.assertFalse(
            has_valid_strategy(
                {"unit_intents": {"u3": {"intent": "HOLD_POSITION"}}}
            )
        )

    def test_timeout_has_explicit_fallback_reason(self):
        reason = infer_fallback_reason(True, False, False, True, "timed out", {})
        self.assertEqual(reason, "llm_timeout")

    def test_empty_actions_match_lux_shape(self):
        self.assertEqual(make_empty_actions(2), [[0, 0, 0], [0, 0, 0]])


if __name__ == "__main__":
    unittest.main()
