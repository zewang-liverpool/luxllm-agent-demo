"""Small deterministic Ollama-compatible server for integration testing only."""

from __future__ import annotations

import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


MODEL = "mock:latest"
MODELS = [MODEL, "mock-qwen:latest", "mock-deepseek:latest"]


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A003
        return

    def _write_json(self, payload, status=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802
        if self.path == "/api/tags":
            self._write_json(
                {
                    "models": [
                        {"name": model, "model": model, "size": 0}
                        for model in MODELS
                    ]
                }
            )
            return
        self._write_json({"error": "not found"}, status=404)

    def do_POST(self):  # noqa: N802
        if self.path != "/api/generate":
            self._write_json({"error": "not found"}, status=404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        request = json.loads(self.rfile.read(length).decode("utf-8"))
        requested_model = str(request.get("model", MODEL))
        if requested_model not in MODELS:
            self._write_json({"error": "model not found"}, status=404)
            return
        prompt = str(request.get("prompt", ""))
        unit_ids = sorted(set(re.findall(r"\bu(\d+):", prompt)), key=int)
        intents = {
            unit_id: {"intent": "HOLD_POSITION", "reason": "deterministic mock integration test"}
            for unit_id in unit_ids
        }
        self._write_json(
            {
                "model": requested_model,
                "response": json.dumps({"unit_intents": intents}),
                "done": True,
            }
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=11435)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Mock Ollama listening on http://{args.host}:{args.port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
