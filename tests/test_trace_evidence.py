import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from analyse_trace_evidence import percentile, raw_intent_shape, summarise_experiment
from audit_verifier_interventions import audit_experiment, reason_fragments


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

    def test_verifier_reason_fragments_are_unique_and_ordered(self):
        self.assertEqual(
            reason_fragments("unsafe target; safer target selected; unsafe target"),
            ["unsafe target", "safer target selected"],
        )

    def test_nested_dual_llm_log_streams_count_as_one_traced_run(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "match_history.jsonl").write_text(
                json.dumps({"status": "complete"}) + "\n", encoding="utf-8"
            )
            (root / "summary.json").write_text(
                json.dumps(
                    {
                        "model_a": "mock-a",
                        "model_b": "mock-b",
                        "model_a_win_rate": 0.5,
                        "metadata": {
                            "git_commit": "test",
                            "planned_matches": 1,
                        },
                    }
                ),
                encoding="utf-8",
            )

            for player in ("player_0", "player_1"):
                log_dir = root / "runs" / "run_0" / "logs" / player
                log_dir.mkdir(parents=True, exist_ok=True)
                (log_dir / "decision_trace.jsonl").write_text(
                    json.dumps(
                        {
                            "event": "agent_step_trace",
                            "llm_enabled": True,
                            "llm_model": f"mock-{player}",
                            "decision_source": "rule_fallback",
                            "fallback_used": True,
                            "fallback_reason": "test",
                            "cache_used": False,
                            "action_fallback_used": False,
                            "risk_filter_changed": False,
                            "risk_filter_changed_targets": 0,
                            "risk_filter_events_count": 0,
                            "unit_action_count": 16,
                            "active_action_count": 0,
                            "llm_called": False,
                            "timed_out": False,
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )
                (log_dir / "llm_decisions.jsonl").write_text(
                    json.dumps(
                        {
                            "llm_called": True,
                            "llm_valid": True,
                            "llm_latency_ms": 1.0,
                            "raw_text": (
                                '{"unit_intents":{"0":{"intent":"HOLD_POSITION"}}}'
                            ),
                        }
                    )
                    + "\n",
                    encoding="utf-8",
                )

            result = summarise_experiment("dual", root)
            audit = audit_experiment("dual", root)

            self.assertEqual(result["runs_with_trace"], 1)
            self.assertEqual(result["trace_streams"], 2)
            self.assertEqual(result["decision_log_calls"], 2)
            self.assertEqual(result["model"], "mock-a vs mock-b")
            self.assertEqual(audit["llm_calls"], 2)


if __name__ == "__main__":
    unittest.main()
