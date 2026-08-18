import json
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "agent"))

from jsonl_io import append_jsonl_atomic


class JsonlIoTests(unittest.TestCase):
    def test_concurrent_large_records_remain_one_json_object_per_line(self):
        results_dir = ROOT / "results"
        results_dir.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=results_dir) as directory:
            path = Path(directory) / "shared.jsonl"

            def write_record(index: int) -> None:
                append_jsonl_atomic(
                    str(path),
                    {"index": index, "payload": "x" * 20000},
                )

            with ThreadPoolExecutor(max_workers=8) as pool:
                list(pool.map(write_record, range(200)))

            records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(records), 200)
            self.assertEqual({record["index"] for record in records}, set(range(200)))


if __name__ == "__main__":
    unittest.main()
