"""Analyse decision tracing and rule-based verification evidence.

This analysis treats match outcome as secondary.  Its primary purpose is to
measure whether completed Lux AI Season 3 runs expose enough structured
evidence to inspect decision provenance and verify LLM-assisted execution.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import tempfile
from collections import Counter
from pathlib import Path
from statistics import mean, median
from typing import Dict, Iterable, List, Sequence, Tuple


TRACE_REQUIRED_FIELDS = (
    "event",
    "step",
    "match_idx",
    "step_in_match",
    "player",
    "decision_source",
    "llm_model",
    "llm_called",
    "llm_valid",
    "fallback_used",
    "action_fallback_used",
    "risk_filter_enabled",
    "risk_filter_changed",
    "unit_action_count",
    "active_action_count",
    "score_player_0",
    "score_player_1",
    "elapsed_total_ms",
)

CALL_TRACE_REQUIRED_FIELDS = (
    "event",
    "step",
    "match_idx",
    "step_in_match",
    "player",
    "llm_enabled",
    "llm_model",
    "llm_called",
    "decision_source",
    "llm_latency_ms",
    "llm_valid",
    "timed_out",
    "fallback_used",
    "fallback_reason",
    "unit_intent_count",
)

REPLAY_LINK_FIELDS = (
    "step",
    "match_idx",
    "step_in_match",
    "player",
    "decision_source",
    "score_player_0",
    "score_player_1",
)


def iter_jsonl(path: Path) -> Iterable[Dict]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def percentile(values: Sequence[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(float(value) for value in values)
    index = max(0, min(len(ordered) - 1, math.ceil(fraction * len(ordered)) - 1))
    return ordered[index]


def raw_intent_shape(raw_text: str) -> Dict[str, int]:
    result = {
        "raw_json_parseable": 0,
        "raw_schema_valid": 0,
        "string_shorthand": 0,
        "prefixed_unit_key": 0,
    }
    try:
        payload = json.loads(raw_text)
    except (TypeError, json.JSONDecodeError):
        return result
    result["raw_json_parseable"] = 1
    intents = payload.get("unit_intents") if isinstance(payload, dict) else None
    if not isinstance(intents, dict) or not intents:
        return result
    schema_valid = True
    for key, item in intents.items():
        key_text = str(key).strip()
        if len(key_text) > 1 and key_text[0].lower() == "u" and key_text[1:].isdigit():
            result["prefixed_unit_key"] = 1
        if isinstance(item, str) and item.strip():
            result["string_shorthand"] = 1
            schema_valid = False
        elif not (
            isinstance(item, dict)
            and isinstance(item.get("intent"), str)
            and item.get("intent", "").strip()
        ):
            schema_valid = False
    result["raw_schema_valid"] = int(schema_valid)
    return result


def ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def summarise_experiment(label: str, root: Path) -> Dict:
    history_path = root / "match_history.jsonl"
    summary_path = root / "summary.json"
    if not history_path.exists() or not summary_path.exists():
        raise FileNotFoundError(f"Incomplete experiment directory: {root}")

    history = list(iter_jsonl(history_path))
    completed = [record for record in history if record.get("status") == "complete"]
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    run_dirs = sorted(path for path in (root / "runs").iterdir() if path.is_dir())

    trace_files = []
    decision_files = []
    runs_with_trace = 0
    missing_trace_runs = []
    for run_dir in run_dirs:
        # Single-LLM runs use logs/<file>.  Dual-LLM runs isolate concurrent
        # writers under logs/player_0 and logs/player_1 to prevent JSONL
        # corruption.  Recursive discovery supports both layouts.
        run_trace_files = sorted((run_dir / "logs").glob("**/decision_trace.jsonl"))
        run_decision_files = sorted((run_dir / "logs").glob("**/llm_decisions.jsonl"))
        if run_trace_files:
            trace_files.extend(run_trace_files)
            runs_with_trace += 1
        else:
            missing_trace_runs.append(run_dir.name)
        decision_files.extend(run_decision_files)

    trace_records = 0
    agent_step_trace_records = 0
    complete_agent_step_trace_records = 0
    decision_call_trace_records = 0
    complete_decision_call_trace_records = 0
    unknown_trace_records = 0
    replay_linked_records = 0
    missing_fields = Counter()
    decision_sources = Counter()
    llm_modes = Counter()
    fallback_reasons = Counter()
    llm_agent_records = 0
    rule_player_records = 0
    llm_agent_fallback_steps = 0
    cache_steps = 0
    action_fallback_steps = 0
    risk_changed_steps = 0
    risk_changed_targets = 0
    risk_events = 0
    action_shape_valid_steps = 0
    active_action_steps = 0
    active_actions = 0
    trace_call_latencies = []
    trace_calls = 0
    trace_valid_calls = 0
    trace_timeouts = 0
    trace_errors = 0

    for path in trace_files:
        for record in iter_jsonl(path):
            trace_records += 1
            event = str(record.get("event", "unknown"))
            if event == "agent_step_trace":
                agent_step_trace_records += 1
                required_fields = TRACE_REQUIRED_FIELDS
            elif event == "decision_trace":
                decision_call_trace_records += 1
                required_fields = CALL_TRACE_REQUIRED_FIELDS
            else:
                unknown_trace_records += 1
                required_fields = ()
            missing = [field for field in required_fields if field not in record]
            for field in missing:
                missing_fields[f"{event}:{field}"] += 1
            if event == "agent_step_trace":
                if not missing:
                    complete_agent_step_trace_records += 1
                if all(field in record for field in REPLAY_LINK_FIELDS):
                    replay_linked_records += 1
            elif event == "decision_trace" and not missing:
                complete_decision_call_trace_records += 1

            if event != "agent_step_trace":
                continue

            if bool(record.get("llm_enabled")):
                llm_agent_records += 1
                decision_sources[str(record.get("decision_source", "unknown"))] += 1
                llm_modes[str(record.get("llm_mode", "unknown"))] += 1
                if bool(record.get("fallback_used")):
                    llm_agent_fallback_steps += 1
                    fallback_reasons[str(record.get("fallback_reason") or "unspecified")] += 1
                if bool(record.get("cache_used")):
                    cache_steps += 1
                if bool(record.get("action_fallback_used")):
                    action_fallback_steps += 1
                if bool(record.get("risk_filter_changed")):
                    risk_changed_steps += 1
                risk_changed_targets += int(record.get("risk_filter_changed_targets", 0) or 0)
                risk_events += int(record.get("risk_filter_events_count", 0) or 0)
                if int(record.get("unit_action_count", -1)) == 16:
                    action_shape_valid_steps += 1
                active = int(record.get("active_action_count", 0) or 0)
                active_actions += active
                if active > 0:
                    active_action_steps += 1
                if bool(record.get("llm_called")):
                    trace_calls += 1
                    trace_call_latencies.append(float(record.get("llm_latency_ms", 0.0) or 0.0))
                    if bool(record.get("llm_valid")):
                        trace_valid_calls += 1
                    if bool(record.get("timed_out")):
                        trace_timeouts += 1
                    if record.get("llm_error"):
                        trace_errors += 1
            else:
                rule_player_records += 1

    decision_records = 0
    decision_calls = 0
    decision_valid = 0
    raw_json_parseable = 0
    raw_schema_valid = 0
    shorthand_normalizations = 0
    key_normalizations = 0
    decision_latencies = []
    calls_by_player_and_model = Counter()
    valid_calls_by_player_and_model = Counter()
    for path in decision_files:
        for record in iter_jsonl(path):
            decision_records += 1
            if not bool(record.get("llm_called")):
                continue
            decision_calls += 1
            route = (
                f'{record.get("player", "unknown")}|'
                f'{record.get("model", record.get("llm_model", "unknown"))}'
            )
            calls_by_player_and_model[route] += 1
            decision_latencies.append(float(record.get("llm_latency_ms", 0.0) or 0.0))
            if bool(record.get("llm_valid")):
                decision_valid += 1
                valid_calls_by_player_and_model[route] += 1
            shape = raw_intent_shape(str(record.get("raw_text", "")))
            raw_json_parseable += shape["raw_json_parseable"]
            raw_schema_valid += shape["raw_schema_valid"]
            shorthand_normalizations += shape["string_shorthand"]
            key_normalizations += shape["prefixed_unit_key"]

    metadata = summary.get("metadata", {})
    return {
        "label": label,
        "experiment_directory": root.name,
        "model": (
            metadata.get("model")
            or (
                f'{summary.get("model_a")} vs {summary.get("model_b")}'
                if summary.get("model_a") and summary.get("model_b")
                else None
            )
        ),
        "source_commit": metadata.get("git_commit"),
        "completed_matches": len(completed),
        "planned_matches": int(metadata.get("planned_matches", len(history))),
        "match_completion_rate": ratio(len(completed), int(metadata.get("planned_matches", len(history)))),
        "runs_with_trace": runs_with_trace,
        "trace_streams": len(trace_files),
        "missing_trace_runs": missing_trace_runs,
        "match_trace_coverage": ratio(runs_with_trace, len(completed)),
        "trace_records": trace_records,
        "agent_step_trace_records": agent_step_trace_records,
        "agent_step_trace_records_complete": complete_agent_step_trace_records,
        "agent_step_trace_completeness_rate": ratio(
            complete_agent_step_trace_records, agent_step_trace_records
        ),
        "decision_call_trace_records": decision_call_trace_records,
        "decision_call_trace_records_complete": complete_decision_call_trace_records,
        "decision_call_trace_completeness_rate": ratio(
            complete_decision_call_trace_records, decision_call_trace_records
        ),
        "unknown_trace_records": unknown_trace_records,
        "replay_linked_trace_records": replay_linked_records,
        "replay_linkage_rate": ratio(replay_linked_records, agent_step_trace_records),
        "missing_trace_fields": dict(missing_fields),
        "llm_agent_trace_records": llm_agent_records,
        "rule_player_trace_records": rule_player_records,
        "decision_source_counts": dict(decision_sources),
        "llm_mode_counts": dict(llm_modes),
        "llm_agent_fallback_steps": llm_agent_fallback_steps,
        "llm_agent_fallback_rate": ratio(llm_agent_fallback_steps, llm_agent_records),
        "fallback_reason_counts": dict(fallback_reasons),
        "cache_steps": cache_steps,
        "cache_step_rate": ratio(cache_steps, llm_agent_records),
        "trace_llm_calls": trace_calls,
        "trace_valid_llm_calls": trace_valid_calls,
        "trace_llm_validity_rate": ratio(trace_valid_calls, trace_calls),
        "trace_timeouts": trace_timeouts,
        "trace_llm_errors": trace_errors,
        "decision_log_records": decision_records,
        "decision_log_calls": decision_calls,
        "decision_log_valid_calls": decision_valid,
        "decision_log_validity_rate": ratio(decision_valid, decision_calls),
        "calls_by_player_and_model": dict(calls_by_player_and_model),
        "valid_calls_by_player_and_model": dict(valid_calls_by_player_and_model),
        "raw_json_parseable_calls": raw_json_parseable,
        "raw_json_parse_rate": ratio(raw_json_parseable, decision_calls),
        "raw_schema_valid_calls": raw_schema_valid,
        "raw_schema_valid_rate": ratio(raw_schema_valid, decision_calls),
        "string_shorthand_normalizations": shorthand_normalizations,
        "prefixed_key_normalizations": key_normalizations,
        "normalization_interventions": shorthand_normalizations + key_normalizations,
        "normalization_intervention_rate": ratio(
            shorthand_normalizations + key_normalizations, decision_calls
        ),
        "action_fallback_steps": action_fallback_steps,
        "risk_filter_changed_steps": risk_changed_steps,
        "risk_filter_changed_step_rate": ratio(risk_changed_steps, llm_agent_records),
        "risk_filter_changed_targets": risk_changed_targets,
        "risk_filter_events": risk_events,
        "action_shape_valid_steps": action_shape_valid_steps,
        "action_shape_valid_rate": ratio(action_shape_valid_steps, llm_agent_records),
        "active_action_steps": active_action_steps,
        "active_actions": active_actions,
        "llm_latency_ms_mean": mean(decision_latencies) if decision_latencies else 0.0,
        "llm_latency_ms_median": median(decision_latencies) if decision_latencies else 0.0,
        "llm_latency_ms_p95": percentile(decision_latencies, 0.95),
        "llm_latency_ms_max": max(decision_latencies) if decision_latencies else 0.0,
        "llm_win_rate_secondary": summary.get(
            "llm_win_rate", summary.get("model_a_win_rate")
        ),
        "matched_seed_performance_secondary": summary.get("matched_seed_performance"),
        "secondary_outcome": {
            "model_a": summary.get("model_a"),
            "model_b": summary.get("model_b"),
            "model_a_wins": summary.get("model_a_wins"),
            "model_a_losses": summary.get("model_a_losses"),
            "draws": summary.get("draws"),
            "model_a_win_rate": summary.get("model_a_win_rate"),
            "model_a_win_rate_wilson_95_ci": summary.get(
                "model_a_win_rate_wilson_95_ci"
            ),
            "exact_binomial_pvalue_vs_0_5": summary.get(
                "exact_binomial_pvalue_vs_0_5"
            ),
            "by_model_a_role": summary.get("by_model_a_role"),
            "matched_seed_performance": summary.get("matched_seed_performance"),
            "matched_role_analysis": summary.get("matched_role_analysis"),
        },
    }


def write_csv(path: Path, results: Sequence[Dict]) -> None:
    scalar_keys = [
        key
        for key, value in results[0].items()
        if not isinstance(value, (dict, list))
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=scalar_keys)
        writer.writeheader()
        for result in results:
            writer.writerow({key: result.get(key) for key in scalar_keys})


def percent(value: float) -> str:
    return f"{100.0 * value:.1f}%"


def write_markdown(path: Path, results: Sequence[Dict], analysis_commit: str) -> None:
    lines = [
        "# Decision-Trace and Action-Verification Evaluation",
        "",
        "## Research question",
        "",
        "> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent, long-horizon, and rule-constrained strategy game such as Lux AI Season 3, and how can the project-specific Decision-Trace and Action-Verification (DTAV) method address the observed limitations?",
        "",
        "This report treats backend win rate as a secondary outcome. The primary evidence concerns trace coverage, decision provenance, structured-output verification, safe action construction, fallback observability, and replay linkage.",
        "",
        f"Analysis code commit: `{analysis_commit}`.",
        "",
        "## Primary framework evidence",
        "",
        "| Metric | " + " | ".join(result["label"] for result in results) + " |",
        "|---|" + "|".join("---:" for _ in results) + "|",
    ]
    rows = [
        ("Completed matches", lambda r: str(r["completed_matches"])),
        ("Matches with trace", lambda r: f'{r["runs_with_trace"]} ({percent(r["match_trace_coverage"])})'),
        ("Structured trace records", lambda r: f'{r["trace_records"]:,}'),
        ("Agent-step trace completeness", lambda r: percent(r["agent_step_trace_completeness_rate"])),
        ("LLM-call trace completeness", lambda r: percent(r["decision_call_trace_completeness_rate"])),
        ("Replay-linkage coverage", lambda r: percent(r["replay_linkage_rate"])),
        ("LLM calls", lambda r: f'{r["decision_log_calls"]:,}'),
        ("Post-normalization structured-valid calls", lambda r: f'{r["decision_log_valid_calls"]:,} ({percent(r["decision_log_validity_rate"])})'),
        ("Raw schema-valid calls", lambda r: f'{r["raw_schema_valid_calls"]:,} ({percent(r["raw_schema_valid_rate"])})'),
        ("Normalization interventions", lambda r: f'{r["normalization_interventions"]:,} ({percent(r["normalization_intervention_rate"])})'),
        ("Cached-decision steps", lambda r: f'{r["cache_steps"]:,} ({percent(r["cache_step_rate"])})'),
        ("Observable rule-fallback steps", lambda r: f'{r["llm_agent_fallback_steps"]:,} ({percent(r["llm_agent_fallback_rate"])})'),
        ("Action fallback steps", lambda r: str(r["action_fallback_steps"])),
        ("Risk-filter changed steps", lambda r: f'{r["risk_filter_changed_steps"]:,} ({percent(r["risk_filter_changed_step_rate"])})'),
        ("Risk-filter changed targets", lambda r: f'{r["risk_filter_changed_targets"]:,}'),
        ("Action-array shape validity", lambda r: percent(r["action_shape_valid_rate"])),
        ("LLM timeouts / errors", lambda r: f'{r["trace_timeouts"]} / {r["trace_llm_errors"]}'),
        ("Median LLM latency", lambda r: f'{r["llm_latency_ms_median"]:.1f} ms'),
        ("P95 LLM latency", lambda r: f'{r["llm_latency_ms_p95"]:.1f} ms'),
    ]
    for name, formatter in rows:
        lines.append("| " + name + " | " + " | ".join(formatter(result) for result in results) + " |")

    lines.extend(
        [
            "",
            "## Decision provenance",
            "",
        ]
    )
    for result in results:
        lines.extend(
            [
                f'### {result["label"]}',
                "",
                "| Decision source | LLM-agent steps |",
                "|---|---:|",
            ]
        )
        for source, count in sorted(result["decision_source_counts"].items()):
            lines.append(
                f'| `{source}` | {count:,} ({percent(ratio(count, result["llm_agent_trace_records"]))}) |'
            )
        lines.extend(["", "Fallback reasons are retained in the JSON report for audit and debugging.", ""])

    lines.extend(["## Player-model call coverage", ""])
    for result in results:
        lines.extend(
            [
                f'### {result["label"]}',
                "",
                "| Player and model | Fresh calls | Valid after checks |",
                "|---|---:|---:|",
            ]
        )
        for route, count in sorted(result["calls_by_player_and_model"].items()):
            valid = result["valid_calls_by_player_and_model"].get(route, 0)
            lines.append(f"| `{route}` | {count:,} | {valid:,} |")
        lines.append("")

    dual_outcomes = [
        (result, result["secondary_outcome"])
        for result in results
        if result["secondary_outcome"].get("model_a")
        and result["secondary_outcome"].get("model_b")
    ]
    if dual_outcomes:
        lines.extend(
            [
                "## Secondary matched outcome",
                "",
                "These outcomes are retained as controlled context, not as a general model leaderboard.",
                "",
                "| Experiment | Wins | Win rate | Match-level Wilson 95% CI | Match-level binomial p | Seed-clustered 95% CI | Seed-level sign p |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        for result, outcome in dual_outcomes:
            interval = outcome.get("model_a_win_rate_wilson_95_ci") or [0.0, 0.0]
            matched_seed = outcome.get("matched_seed_performance") or {}
            clustered_interval = matched_seed.get("cluster_bootstrap_95_ci") or [
                0.0,
                0.0,
            ]
            lines.append(
                f'| {result["label"]} | '
                f'{outcome["model_a"]} {outcome["model_a_wins"]} : '
                f'{outcome["model_b"]} {outcome["model_a_losses"]} | '
                f'{percent(float(outcome["model_a_win_rate"] or 0.0))} | '
                f'[{percent(float(interval[0]))}, {percent(float(interval[1]))}] | '
                f'{float(outcome["exact_binomial_pvalue_vs_0_5"] or 0.0):.4f} | '
                f'[{percent(float(clustered_interval[0]))}, '
                f'{percent(float(clustered_interval[1]))}] | '
                f'{float(matched_seed.get("exact_sign_pvalue_vs_0_5") or 0.0):.4f} |'
            )
        lines.append("")

    lines.extend(
        [
            "## Interpretation aligned with the research question",
            "",
            "1. **Inspection:** Per-step provenance and replay-link fields quantify whether an evaluator can connect state, decision source, score context, and execution time after a match.",
            "2. **Verification:** Raw-output parsing and schema checks expose where deterministic normalization was required before a proposal could enter the action planner.",
            "3. **Safe execution:** Action-array shape, action fallback, timeout, error, and completed-match metrics show whether verified proposals remained executable under controlled runs.",
            "4. **Evaluation:** Matched-seed outcomes demonstrate that the same trace-and-verification framework supports controlled backend evaluation; they do not establish a general LLM leaderboard.",
            "",
            "## Limitations",
            "",
            "The logs establish operational provenance and recorded verification events, not a complete causal explanation of agent behaviour. A zero action-fallback count means no downstream action failure was observed in these runs; it does not prove that every possible LLM proposal would be safe. Viewer-based inspection remains a qualitative complement to the quantitative coverage metrics.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def write_figures(output_dir: Path, results: Sequence[Dict]) -> List[str]:
    try:
        os.environ.setdefault(
            "MPLCONFIGDIR",
            str(Path(tempfile.gettempdir()) / "luxllm-agent-matplotlib"),
        )
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return []

    output_dir.mkdir(parents=True, exist_ok=True)
    labels = [result["label"] for result in results]
    colours = ["#2563eb", "#dc2626"]
    written = []

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    metric_names = [
        "Step trace",
        "Call trace",
        "Replay link",
        "Post-check",
        "Raw schema",
        "Risk filter",
    ]
    x = list(range(len(metric_names)))
    width = 0.34
    for index, result in enumerate(results):
        values = [
            result["agent_step_trace_completeness_rate"],
            result["decision_call_trace_completeness_rate"],
            result["replay_linkage_rate"],
            result["decision_log_validity_rate"],
            result["raw_schema_valid_rate"],
            result["risk_filter_changed_step_rate"],
        ]
        positions = [value + (index - 0.5) * width for value in x]
        ax.bar(positions, values, width=width, label=labels[index], color=colours[index % len(colours)])
    ax.set_ylim(0.0, 1.08)
    ax.set_ylabel("Coverage / validity / intervention rate")
    ax.set_xticks(x, metric_names)
    ax.legend(frameon=False, loc="upper center", bbox_to_anchor=(0.5, 1.14), ncol=2)
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    path = output_dir / "framework_evidence_rates.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    written.append(str(path))

    sources = sorted({key for result in results for key in result["decision_source_counts"]})
    fig, axes = plt.subplots(1, len(results), figsize=(10.5, 4.6), sharey=True)
    if len(results) == 1:
        axes = [axes]
    for ax, result, colour in zip(axes, results, colours):
        counts = [result["decision_source_counts"].get(source, 0) for source in sources]
        ax.barh(sources, counts, color=colour)
        ax.set_title(result["label"])
        ax.set_xlabel("LLM-agent trace steps")
        ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    path = output_dir / "decision_source_distribution.png"
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    written.append(str(path))
    return written


def parse_experiment(value: str) -> Tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("Use LABEL=PATH")
    label, path = value.split("=", 1)
    return label.strip(), Path(path).resolve()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", action="append", required=True, type=parse_experiment)
    parser.add_argument("--json-output", type=Path, required=True)
    parser.add_argument("--csv-output", type=Path, required=True)
    parser.add_argument("--markdown-output", type=Path, required=True)
    parser.add_argument("--figure-dir", type=Path, required=True)
    parser.add_argument("--analysis-commit", default="working-tree")
    args = parser.parse_args()

    results = [summarise_experiment(label, path) for label, path in args.experiment]
    for path in (args.json_output, args.csv_output, args.markdown_output):
        path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "research_question": (
            "How effectively can directly prompted LLMs make decisions in a partially "
            "observable, multi-agent, long-horizon, and rule-constrained strategy game "
            "such as Lux AI Season 3, and how can the project-specific Decision-Trace "
            "and Action-Verification (DTAV) method address the observed limitations?"
        ),
        "analysis_commit": args.analysis_commit,
        "experiments": results,
    }
    args.json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_csv(args.csv_output, results)
    write_markdown(args.markdown_output, results, args.analysis_commit)
    figures = write_figures(args.figure_dir, results)
    print(json.dumps({"outputs": [str(args.json_output), str(args.csv_output), str(args.markdown_output)], "figures": figures}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
