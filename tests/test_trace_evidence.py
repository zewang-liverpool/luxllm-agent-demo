import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from analyse_trace_evidence import percentile, raw_intent_shape


class TraceEvidenceTests(unittest.TestCase):
    def test_raw_schema_classifies_string_shorthand(self):
        shape = raw_intent_shape(
            '{"unit_intents":{"0":"EXPLORE_STALE_TILE"}}'
        )
        self.assertEqual(shape["raw_json_parseable"], 1)
        self.assertEqual(shape["raw_schema_valid"], 0)
        self.assertEqual(shape["string_shorthand"], 1)

    def test_raw_schema_classifies_prefixed_key(self):
        shape = raw_intent_shape(
            '{"unit_intents":{"u3":{"intent":"HOLD_POSITION"}}}'
        )
        self.assertEqual(shape["raw_schema_valid"], 1)
        self.assertEqual(shape["prefixed_unit_key"], 1)

    def test_nearest_rank_percentile_is_deterministic(self):
        self.assertEqual(percentile([1, 2, 3, 4], 0.95), 4.0)


if __name__ == "__main__":
    unittest.main()
