import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))

from run_paired_experiment import (
    method_environment,
    parse_rewards,
    resolve_source_commit,
    winner_from_rewards,
)
from run_dual_llm_experiment import model_available, summarise_dual_records
from validate_paired_method_result import validate_settings


class ExperimentRunnerTests(unittest.TestCase):
    def test_direct_prompt_method_disables_dtav_interventions(self):
        env = method_environment("direct_prompt")
        self.assertEqual(env["LUX_DECISION_METHOD"], "direct_prompt")
        self.assertEqual(env["LUX_NORMALIZE_LLM_OUTPUT"], "0")
        self.assertEqual(env["LUX_ENABLE_STRATEGY_CACHE"], "0")
        self.assertEqual(env["LUX_LLM_REUSE_LAST_INTENTS"], "0")
        self.assertEqual(env["LUX_ENABLE_RISK_AWARE_ACTION_FILTER"], "0")

    def test_dtav_method_enables_project_interventions(self):
        env = method_environment("dtav")
        self.assertTrue(all(value == "1" for key, value in env.items() if key != "LUX_DECISION_METHOD"))

    def test_method_validator_rejects_mislabeled_direct_prompt_settings(self):
        metadata = {
            "decision_method": "direct_prompt",
            "decision_method_settings": method_environment("dtav"),
        }
        self.assertTrue(validate_settings(metadata, "direct_prompt"))

    def test_dual_llm_summary_tracks_model_a_across_role_swap(self):
        records = [
            {
                "status": "complete",
                "seed": 7,
                "winner": "player_0",
                "winner_model": "qwen3:32b",
                "model_a_player": "player_0",
                "llm_player": "player_0",
                "llm_won": True,
            },
            {
                "status": "complete",
                "seed": 7,
                "winner": "player_0",
                "winner_model": "deepseek-r1:32b",
                "model_a_player": "player_1",
                "llm_player": "player_1",
                "llm_won": False,
            },
        ]
        summary = summarise_dual_records(
            records,
            model_a="qwen3:32b",
            model_b="deepseek-r1:32b",
        )
        self.assertEqual(summary["completed_matches"], 2)
        self.assertEqual(summary["paired_seeds_completed"], 1)
        self.assertEqual(summary["model_a_wins"], 1)
        self.assertEqual(summary["model_a_losses"], 1)
        self.assertEqual(
            summary["winner_model_counts"],
            {"qwen3:32b": 1, "deepseek-r1:32b": 1},
        )

    def test_dual_llm_inventory_requires_both_named_models(self):
        inventory = [
            {"name": "qwen3:32b"},
            {"name": "deepseek-r1:32b"},
        ]
        self.assertTrue(model_available("qwen3:32b", inventory))
        self.assertTrue(model_available("deepseek-r1:32b", inventory))
        self.assertFalse(model_available("missing:32b", inventory))

    def test_parse_numpy_style_rewards(self):
        text = "Rewards: {'player_0': array(5, dtype=int32), 'player_1': array(2, dtype=int32)}"
        self.assertEqual(parse_rewards(text), (5, 2))
        self.assertEqual(winner_from_rewards(5, 2), "player_0")

    def test_parse_scalar_rewards(self):
        text = 'Rewards: {"player_0": 1, "player_1": 4}'
        self.assertEqual(parse_rewards(text), (1, 4))

    @mock.patch("run_paired_experiment.subprocess.check_output", side_effect=OSError("no git"))
    @mock.patch.dict("run_paired_experiment.os.environ", {"LUX_SOURCE_COMMIT": "67c2a3b"})
    def test_source_commit_falls_back_to_transfer_manifest(self, _check_output):
        self.assertEqual(resolve_source_commit(), "67c2a3b")


if __name__ == "__main__":
    unittest.main()
