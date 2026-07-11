"""
llm_decider.py

LLM decision module for Lux S3.

The LLM produces high-level intents only.
The rule planner converts those intents into official Lux actions.

v0.9-E1 focus:
- Use qwen3:32b as the default local model through config.py.
- Keep detailed LLM logs in llm_decisions.jsonl.
- Write compact decision records to decision_log.jsonl.
- Write trace-oriented records to decision_trace.jsonl.
- Expose last_timed_out, last_error, last_elapsed, last_llm_called,
  last_valid, and last_fallback_reason for agent.py.
"""

import json
import os
import re
import time
import urllib.error
import urllib.request
from typing import Dict, Optional

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


def build_ollama_payload(model: str, prompt: str) -> Dict:
    """Build a deterministic Ollama request for a short strategic decision."""
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": bool(config.LLM_THINK),
        "options": {
            "temperature": float(config.LLM_TEMPERATURE),
            "seed": int(config.LLM_SEED),
            "num_predict": int(config.LLM_NUM_PREDICT),
        },
    }
    if bool(config.LLM_JSON_MODE):
        payload["format"] = "json"
    return payload


def extract_ollama_response(result: Dict) -> str:
    """Return the final answer and reject reasoning-only Ollama responses."""
    if not isinstance(result, dict):
        raise RuntimeError("Ollama returned a non-object response")

    response = result.get("response", "")
    if isinstance(response, str) and response.strip():
        return response

    thinking = result.get("thinking", "")
    done_reason = result.get("done_reason", "unknown")
    eval_count = result.get("eval_count", "unknown")
    if isinstance(thinking, str) and thinking.strip():
        raise RuntimeError(
            "Ollama returned thinking but no final response "
            f"(done_reason={done_reason}, eval_count={eval_count}); "
            "set LUX_LLM_THINK=0 or increase LUX_LLM_NUM_PREDICT"
        )

    raise RuntimeError(
        "Ollama returned an empty final response "
        f"(done_reason={done_reason}, eval_count={eval_count})"
    )


def normalize_unit_intent_keys(parsed: Dict) -> Dict:
    """Normalize model keys such as ``u3`` to the planner's canonical ``3``."""
    if not isinstance(parsed, dict):
        return parsed

    unit_intents = parsed.get("unit_intents")
    if not isinstance(unit_intents, dict):
        return parsed

    normalized = {}
    for raw_key, item in unit_intents.items():
        key = str(raw_key).strip()
        if len(key) > 1 and key[0].lower() == "u" and key[1:].isdigit():
            key = key[1:]
        if isinstance(item, str) and item.strip():
            item = {
                "intent": item.strip(),
                "reason": "normalized model shorthand",
            }
        normalized[key] = item
    parsed["unit_intents"] = normalized
    return parsed


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


def infer_fallback_reason(
    enabled: bool,
    force_rule_only: bool,
    force_fallback: bool,
    timed_out: bool,
    error: str,
    parsed: Dict,
) -> Optional[str]:
    """
    Return a compact fallback reason for trace/evaluation summaries.
    """
    if force_rule_only:
        return "force_rule_only"

    if force_fallback:
        return "force_fallback"

    if not enabled:
        return "llm_disabled"

    if timed_out:
        return "llm_timeout"

    if error:
        return "llm_error"

    if not isinstance(parsed, dict):
        return "invalid_response"

    if not has_valid_strategy(parsed):
        return "empty_or_invalid_intents"

    return None


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

        # v0.9-E1 trace fields.
        self.last_llm_called = False
        self.last_valid = False
        self.last_raw_text = ""
        self.last_prompt_chars = 0
        self.last_unit_intent_count = 0
        self.last_fallback_reason = None

    def decide(self, gameview: Dict) -> Dict:
        """
        Return:
        {
            "unit_intents": {
                "0": {"intent": "...", "reason": "..."}
            }
        }
        """
        self._reset_runtime_fields()

        step = gameview.get("step")
        match = gameview.get("match", {})
        prompt = gameview_to_prompt(gameview)
        self.last_prompt_chars = len(prompt)

        if config.FORCE_RULE_ONLY or config.FORCE_FALLBACK or not self.enabled:
            parsed = {"unit_intents": {}}
            self.last_fallback_reason = infer_fallback_reason(
                enabled=self.enabled,
                force_rule_only=bool(config.FORCE_RULE_ONLY),
                force_fallback=bool(config.FORCE_FALLBACK),
                timed_out=False,
                error="",
                parsed=parsed,
            )
            self._write_decision_logs(
                step=step,
                match=match,
                elapsed=0.0,
                prompt=prompt,
                raw_text="",
                parsed=parsed,
                timed_out=False,
                error="",
                llm_called=False,
                fallback_reason=self.last_fallback_reason,
            )
            return parsed

        started = time.time()
        raw_text = ""
        parsed = {}

        try:
            self.last_llm_called = True
            raw_text = self._call_ollama(prompt)
            self.last_raw_text = raw_text
            parsed = normalize_unit_intent_keys(extract_json_object(raw_text))

        except Exception as exc:
            error_text = str(exc)
            self.last_error = error_text
            self.last_timed_out = self._is_timeout_error(error_text)

            parsed = {
                "unit_intents": {},
                "error": error_text,
            }

            append_jsonl(
                LLM_ERROR_LOG_PATH,
                {
                    "time": time.time(),
                    "event": "llm_error",
                    "experiment_tag": config.EXPERIMENT_TAG,
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
        self.last_valid = self.last_strategy_used
        self.last_unit_intent_count = count_unit_intents(parsed)

        self.last_fallback_reason = infer_fallback_reason(
            enabled=self.enabled,
            force_rule_only=bool(config.FORCE_RULE_ONLY),
            force_fallback=bool(config.FORCE_FALLBACK),
            timed_out=self.last_timed_out,
            error=self.last_error,
            parsed=parsed,
        )

        self._write_decision_logs(
            step=step,
            match=match,
            elapsed=elapsed,
            prompt=prompt,
            raw_text=raw_text,
            parsed=parsed,
            timed_out=self.last_timed_out,
            error=self.last_error,
            llm_called=self.last_llm_called,
            fallback_reason=self.last_fallback_reason,
        )

        return parsed

    def _reset_runtime_fields(self) -> None:
        self.last_elapsed = 0.0
        self.last_error = ""
        self.last_timed_out = False
        self.last_strategy_used = False

        self.last_llm_called = False
        self.last_valid = False
        self.last_raw_text = ""
        self.last_prompt_chars = 0
        self.last_unit_intent_count = 0
        self.last_fallback_reason = None

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
        llm_called: bool,
        fallback_reason: Optional[str],
    ) -> None:
        """
        Write detailed, compact, and trace-oriented LLM decision logs.

        llm_decisions.jsonl:
            Detailed debug log.

        decision_log.jsonl:
            Compact log for match recorder/statistics.

        decision_trace.jsonl:
            Trace-oriented decision provenance log for paper evaluation.
        """
        strategy_used = has_valid_strategy(parsed)
        unit_intent_count = count_unit_intents(parsed)
        fallback_used = fallback_reason is not None or not strategy_used

        detailed_record = {
            "time": time.time(),
            "event": "llm_decision",
            "experiment_tag": config.EXPERIMENT_TAG,
            "step": step,
            "match": match,
            "elapsed": elapsed,
            "llm_latency_ms": round(elapsed * 1000.0, 3),
            "model": self.model,
            "llm_called": bool(llm_called),
            "timed_out": bool(timed_out),
            "error": error,
            "strategy_used": bool(strategy_used),
            "llm_valid": bool(strategy_used),
            "fallback_used": bool(fallback_used),
            "fallback_reason": fallback_reason,
            "unit_intent_count": int(unit_intent_count),
            "prompt_chars": len(prompt),
            "raw_text": raw_text,
            "parsed": parsed,
        }

        compact_record = {
            "time": time.time(),
            "event": "llm_decision",
            "experiment_tag": config.EXPERIMENT_TAG,
            "step": step,
            "match_idx": match.get("match_idx"),
            "step_in_match": match.get("step_in_match"),
            "elapsed": elapsed,
            "llm_latency_ms": round(elapsed * 1000.0, 3),
            "model": self.model,
            "llm_called": bool(llm_called),
            "fresh_llm_call": bool(llm_called),
            "llm_strategy_used": bool(strategy_used),
            "cached_llm_turn": False,
            "event_refresh": False,
            "safety_override": False,
            "fallback_used": bool(fallback_used),
            "fallback_reason": fallback_reason,
            "timed_out": bool(timed_out),
            "error": error,
            "unit_intent_count": int(unit_intent_count),
            "intents": parsed.get("unit_intents", {}),
        }

        trace_record = {
            "time": time.time(),
            "event": "decision_trace",
            "experiment_tag": config.EXPERIMENT_TAG,
            "step": step,
            "match_idx": match.get("match_idx"),
            "step_in_match": match.get("step_in_match"),
            "player": match.get("player"),
            "llm_enabled": bool(self.enabled),
            "llm_model": self.model,
            "llm_called": bool(llm_called),
            "decision_source": self._infer_decision_source(
                llm_called=llm_called,
                strategy_used=strategy_used,
                fallback_used=fallback_used,
            ),
            "llm_latency_ms": round(elapsed * 1000.0, 3),
            "llm_valid": bool(strategy_used),
            "llm_error": error or None,
            "timed_out": bool(timed_out),
            "fallback_used": bool(fallback_used),
            "fallback_reason": fallback_reason,
            "cache_used": False,
            "stale_decision": False,
            "unit_intent_count": int(unit_intent_count),
            "intents": parsed.get("unit_intents", {}),
        }

        append_jsonl(config.LLM_DECISION_LOG, detailed_record)
        append_jsonl(DECISION_LOG_PATH, compact_record)

        if bool(getattr(config, "LOG_DECISION_TRACE", True)):
            append_jsonl(config.DECISION_TRACE_LOG, trace_record)

        if bool(getattr(config, "LOG_ABLATION_METRICS", True)):
            append_jsonl(config.ABLATION_METRICS_LOG, compact_record)

    def _infer_decision_source(
        self,
        llm_called: bool,
        strategy_used: bool,
        fallback_used: bool,
    ) -> str:
        if config.FORCE_RULE_ONLY:
            return "rule_only"

        if config.FORCE_FALLBACK:
            return "forced_fallback"

        if fallback_used:
            return "fallback"

        if llm_called and strategy_used:
            return "llm_fresh"

        if strategy_used:
            return "llm_strategy"

        return "unknown"

    def _call_ollama(self, prompt: str) -> str:
        """
        Call local Ollama generate API.
        """
        url = self.base_url.rstrip("/") + "/api/generate"

        payload = build_ollama_payload(self.model, prompt)

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            url=url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(
            request,
            timeout=float(config.LLM_TIMEOUT_SECONDS),
        ) as response:
            body = response.read().decode("utf-8", errors="replace")

        result = json.loads(body)
        return extract_ollama_response(result)

    def _is_timeout_error(self, error_text: str) -> bool:
        if not error_text:
            return False

        lowered = error_text.lower()
        timeout_markers = [
            "timed out",
            "timeout",
            "read timed out",
            "operation timed out",
        ]

        return any(marker in lowered for marker in timeout_markers)
