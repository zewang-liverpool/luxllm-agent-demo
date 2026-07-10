import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from evaluation_stats import exact_binomial_pvalue, summarise_records, wilson_interval
from compare_paired_experiments import compare


class EvaluationStatsTests(unittest.TestCase):
    def test_wilson_interval_contains_observed_rate(self):
        low, high = wilson_interval(35, 50)
        self.assertLess(low, 0.70)
        self.assertGreater(high, 0.70)

    def test_exact_binomial_is_symmetric(self):
        self.assertAlmostEqual(exact_binomial_pvalue(15, 50), exact_binomial_pvalue(35, 50))

    def test_role_swapped_summary_uses_matched_seeds(self):
        records = [
            {"status": "complete", "seed": 1, "llm_player": "player_0", "winner": "player_0", "llm_won": True},
            {"status": "complete", "seed": 1, "llm_player": "player_1", "winner": "player_0", "llm_won": False},
            {"status": "complete", "seed": 2, "llm_player": "player_0", "winner": "player_1", "llm_won": False},
            {"status": "complete", "seed": 2, "llm_player": "player_1", "winner": "player_1", "llm_won": True},
        ]
        summary = summarise_records(records)
        self.assertEqual(summary["paired_seeds_completed"], 2)
        self.assertEqual(summary["by_llm_role"]["player_0"]["matches"], 2)
        self.assertEqual(summary["matched_role_analysis"]["player_0_only_wins"], 1)
        self.assertEqual(summary["matched_role_analysis"]["player_1_only_wins"], 1)

    def test_paired_model_comparison_matches_seed_and_role(self):
        left = {
            (1, "player_0"): {"llm_won": True, "winner": "player_0"},
            (1, "player_1"): {"llm_won": False, "winner": "player_0"},
        }
        right = {
            (1, "player_0"): {"llm_won": False, "winner": "player_1"},
            (1, "player_1"): {"llm_won": False, "winner": "player_0"},
        }
        result = compare(left, right, "a", "b")
        self.assertEqual(result["matched_seed_role_strata"], 2)
        self.assertEqual(result["left_only_wins"], 1)


if __name__ == "__main__":
    unittest.main()
