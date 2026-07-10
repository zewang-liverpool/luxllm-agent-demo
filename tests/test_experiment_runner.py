import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_paired_experiment import parse_rewards, winner_from_rewards


class ExperimentRunnerTests(unittest.TestCase):
    def test_parse_numpy_style_rewards(self):
        text = "Rewards: {'player_0': array(5, dtype=int32), 'player_1': array(2, dtype=int32)}"
        self.assertEqual(parse_rewards(text), (5, 2))
        self.assertEqual(winner_from_rewards(5, 2), "player_0")

    def test_parse_scalar_rewards(self):
        text = 'Rewards: {"player_0": 1, "player_1": 4}'
        self.assertEqual(parse_rewards(text), (1, 4))


if __name__ == "__main__":
    unittest.main()
