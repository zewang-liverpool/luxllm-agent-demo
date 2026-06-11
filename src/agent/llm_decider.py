"""
llm_decider.py

LLM decision module for Lux S3.

The LLM produces high-level intents only.
The rule planner converts those intents into official Lux actions.

Version focus:
- Keep detailed LLM log in llm_decisions.jsonl.
- Also write compact decision records to decision_log.jsonl.
- Expose last_timed_out, last_error and last_elapsed for agent.py.
"""

import json
import os
import re
import time
import urllib.request
from typing import Dict

import config
from state_summarizer import gameview_to_prompt


DECISION_LOG_PATH = os.path.join(config.LOG_DIR, "decision_log.jsonl")
LLM_ERROR_LOG_PATH = os.path.join(config.LOG_DIR, "llm_error_log.jsonl")


def ensure_log_dirs() -> None:
    os.makedirs(config.LOG_DIR, exist_ok=True)
    os.makedirs(config.ERROR_LOG_DIR, exist_ok=True)


def append_jsonl(path: str, data: Dict) -> None:
    ensure_log_dirs()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")


def extract_json_object(text: str) -> Dict:
    """
    Extract the first JSON object from LLM output.
    """
    if not text:
        return {}

    text = text.strip()

    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        return {}

    try:
        return json.loads(match.group(0))
    except Exception:
        return {}


def count_unit_intents(parsed: Dict) -> int:
    if not isinstance(parsed, dict):
        return 0

    unit_intents = parsed.get("unit_intents", {})
    if not isinstance(unit_intents, dict):
        return 0

    return len(unit_intents)


def has_valid_strategy(parsed: Dict) -> bool:
    if not isinstance(parsed, dict):
        return False

    unit_intents = parsed.get("unit_intents", {})
    if not isinstance(unit_intents, dict):
        return False

    for _, item in unit_intents.items():
        if not isinstance(item, dict):
            continue

        intent = item.get("intent")
        if isinstance(intent, str) and intent.strip():
            return True

    return False


class LLMDecider:
    def __init__(self, model: str = None, base_url: str = None, enabled: bool = None):
        self.model = model or config.LLM_MODEL
        self.base_url = base_url or config.LLM_BASE_URL
        self.enabled = config.LLM_ENABLED if enabled is None else bool(enabled)

        # agent.py depends on these runtime fields.
        self.last_elapsed = 0.0
        self.last_error = ""
        self.last_timed_out = False
        self.last_strategy_used = False

    def decide(self, gameview: Dict) -> Dict:
        """
        Return:
        {
            "unit_intents": {
                "0": {"intent": "...", "reason": "..."}
            }
        }
        """
        self.last_elapsed = 0.0
        self.last_error = ""
        self.last_timed_out = False
        self.last_strategy_used = False

        step = gameview.get("step")
        match = gameview.get("match", {})
        prompt = gameview_to_prompt(gameview)

        if not self.enabled:
            parsed = {"unit_intents": {}}
            self._write_decision_logs(
                step=step,
                match=match,
                elapsed=0.0,
                prompt=prompt,
                raw_text="",
                parsed=parsed,
                timed_out=False,
                error="disabled",
            )
            return parsed

        started = time.time()
        raw_text = ""
        parsed = {}

        try:
            raw_text = self._call_ollama(prompt)
            parsed = extract_json_object(raw_text)

        except Exception as exc:
            error_text = str(exc)
            self.last_error = error_text
            self.last_timed_out = "timed out" in error_text.lower()

            parsed = {
                "unit_intents": {},
                "error": error_text,
            }

            append_jsonl(
                LLM_ERROR_LOG_PATH,
                {
                    "time": time.time(),
                    "step": step,
                    "match": match,
                    "model": self.model,
                    "error": error_text,
                    "timed_out": self.last_timed_out,
                },
            )

        elapsed = time.time() - started
        self.last_elapsed = elapsed

        if not isinstance(parsed, dict):
            parsed = {"unit_intents": {}}

        if "unit_intents" not in parsed or not isinstance(parsed.get("unit_intents"), dict):
            parsed["unit_intents"] = {}

        self.last_strategy_used = has_valid_strategy(parsed)

        self._write_decision_logs(
            step=step,
            match=match,
            elapsed=elapsed,
            prompt=prompt,
            raw_text=raw_text,
            parsed=parsed,
            timed_out=self.last_timed_out,
            error=self.last_error,
        )

        return parsed

    def _write_decision_logs(
        self,
        step,
        match: Dict,
        elapsed: float,
        prompt: str,
        raw_text: str,
        parsed: Dict,
        timed_out: bool,
        error: str,
    ) -> None:
        """
        Write both detailed and compact decision logs.

        llm_decisions.jsonl:
            Detailed debug log.

        decision_log.jsonl:
            Compact log for match recorder/statistics.
        """
        strategy_used = has_valid_strategy(parsed)
        unit_intent_count = count_unit_intents(parsed)

        detailed_record = {
            "time": time.time(),
            "event": "llm_decision",
            "step": step,
            "match": match,
            "elapsed": elapsed,
            "model": self.model,
            "timed_out": timed_out,
            "error": error,
            "strategy_used": strategy_used,
            "unit_intent_count": unit_intent_count,
            "prompt_chars": len(prompt),
            "raw_text": raw_text,
            "parsed": parsed,
        }

        compact_record = {
            "time": time.time(),
            "event": "llm_decision",
            "step": step,
            "match_idx": match.get("match_idx"),
            "step_in_match": match.get("step_in_match"),
            "elapsed": elapsed,
            "model": self.model,
            "fresh_llm_call": True,
            "llm_strategy_used": strategy_used,
            "cached_llm_turn": False,
            "event_refresh": False,
            "safety_override": False,
            "fallback_used": not strategy_used,
            "timed_out": timed_out,
            "error": error,
            "unit_intent_count": unit_intent_count,
            "intents": parsed.get("unit_intents", {}),
        }

        append_jsonl(config.LLM_DECISION_LOG, detailed_record)
        append_jsonl(DECISION_LOG_PATH, compact_record)

    def _call_ollama(self, prompt: str) -> str:
        """
        Call local Ollama generate API.
        """
        url = self.base_url.rstrip("/") + "/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 120,
            },
        }

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            url=url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(
            request,
            timeout=config.LLM_TIMEOUT_SECONDS,
        ) as response:
            body = response.read().decode("utf-8", errors="replace")

        result = json.loads(body)
        return result.get("response", "")