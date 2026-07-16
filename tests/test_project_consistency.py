import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from validate_project_evidence import find_forbidden_claims, validate


class ProjectConsistencyTests(unittest.TestCase):
    def test_forbidden_claim_detection(self):
        self.assertEqual(
            find_forbidden_claims("status: Pending Barkla2 run"),
            ["Pending Barkla2 run"],
        )

    def test_tracked_project_evidence_is_consistent(self):
        self.assertEqual(validate(), [])


if __name__ == "__main__":
    unittest.main()
