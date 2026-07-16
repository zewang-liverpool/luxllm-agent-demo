"""Audit normalization and risk-filter interventions in formal experiment logs."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Dict, Iterable, Iterator, List, Sequence, Tuple

from analyse_trace_evidence import raw_intent_shape


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXPERIMENTS = (
    ("Qwen3-32B", ROOT / "archive" / "barkla_results" / "9755477_qwen3_32b_paired"),
    (
        "DeepSeek-R1-32B",
        ROOT / "archive" / "barkla_results" / "9756874_deepseek-r1_32b_paired",
    ),
)


def iter_jsonl(path: Path) -> Iterator[Dict]:
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                yield json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc


def reason_fragments(reason: object) -> List[str]:
    """Return unique, ordered verifier reason fragments for one trace step."""
    seen = set()
    result = []
    for fragment in str(reason or "unspecified").split(";"):
        normalized = " ".join(fragment.strip().split())
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result or ["unspecified"]


def parse_experiment(value: str) -> Tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("use LABEL=PATH")
    label, raw_path = value.split("=", 1)
    if not label.strip() or not raw_path.strip():
        raise argparse.ArgumentTypeError("use a non-empty LABEL=PATH")
    return label.strip(), Path(raw_path).expanduser().resolve()


def audit_experiment(label: str, root: Path, sample_limit: int = 3) -> Dict:
    if not root.is_dir():
        raise FileNotFoundError(root)

    decision_files = sorted(root.glob("runs/*/logs/llm_decisions.jsonl"))
    trace_files = sorted(root.glob("runs/*/logs/decision_trace.jsonl"))
    if not decision_files or not trace_files:
        raise ValueError(f"{root}: expected formal run logs were not found")

    calls = 0
    raw_schema_valid = 0
    normalization_types = Counter()
    normalization_samples = []

    for path in decision_files:
        run_name = path.parents[1].name
        for record in iter_jsonl(path):
            if not record.get("llm_called"):
                continue
            calls += 1
            raw_text = str(record.get("raw_text", ""))
            shape = raw_intent_shape(raw_text)
            raw_schema_valid += int(shape["raw_schema_valid"])
            types = []
            if shape["string_shorthand"]:
                types.append("string_intent_shorthand")
            if shape["prefixed_unit_key"]:
                types.append("prefixed_unit_key")
            for item in types:
                normalization_types[item] += 1
            if types and len(normalization_samples) < sample_limit:
                normalization_samples.append(
                    {
                        "run": run_name,
                        "step": record.get("step"),
                        "types": types,
                        "raw_text": raw_text[:500],
                        "post_check_valid": bool(record.get("llm_valid")),
                    }
                )

    llm_agent_steps = 0
    risk_changed_steps = 0
    risk_changed_targets = 0
    changed_target_counts = []
    risk_by_source = Counter()
    risk_by_phase = Counter()
    risk_by_reason = Counter()
    risk_by_cache_state = Counter()
    visible_enemy_counts = Counter()
    risk_samples = []

    for path in trace_files:
        run_name = path.parents[1].name
        for record in iter_jsonl(path):
            if record.get("event") != "agent_step_trace" or not record.get("llm_enabled"):
                continue
            llm_agent_steps += 1
            if not record.get("risk_filter_changed"):
                continue
            risk_changed_steps += 1
            changed = int(record.get("risk_filter_changed_targets", 0) or 0)
            risk_changed_targets += changed
            changed_target_counts.append(changed)
            risk_by_source[str(record.get("decision_source") or "unknown")] += 1
            risk_by_phase[str(record.get("phase") or "unknown")] += 1
            cache_state = "cached" if record.get("cache_used") else "fresh_or_rule"
            risk_by_cache_state[cache_state] += 1
            visible_enemy_counts[
                str(int(record.get("risk_filter_visible_enemy_units", 0) or 0))
            ] += 1
            for fragment in reason_fragments(record.get("risk_filter_reason")):
                risk_by_reason[fragment] += 1
            if len(risk_samples) < sample_limit:
                risk_samples.append(
                    {
                        "run": run_name,
                        "step": record.get("step"),
                        "match_idx": record.get("match_idx"),
                        "step_in_match": record.get("step_in_match"),
                        "decision_source": record.get("decision_source"),
                        "phase": record.get("phase"),
                        "cache_used": bool(record.get("cache_used")),
                        "changed_targets": changed,
                        "visible_enemy_units": int(
                            record.get("risk_filter_visible_enemy_units", 0) or 0
                        ),
                        "reason": record.get("risk_filter_reason"),
                    }
                )

    normalization_interventions = sum(normalization_types.values())
    strict_rejections = calls - raw_schema_valid
    return {
        "label": label,
        "experiment_directory": root.name,
        "llm_calls": calls,
        "raw_schema_valid_calls": raw_schema_valid,
        "raw_schema_valid_rate": raw_schema_valid / calls if calls else 0.0,
        "strict_schema_rejections_without_normalization": strict_rejections,
        "normalization_interventions": normalization_interventions,
        "normalization_types": dict(normalization_types),
        "normalization_samples": normalization_samples,
        "llm_agent_steps": llm_agent_steps,
        "risk_filter_changed_steps": risk_changed_steps,
        "risk_filter_changed_step_rate": (
            risk_changed_steps / llm_agent_steps if llm_agent_steps else 0.0
        ),
        "risk_filter_changed_targets": risk_changed_targets,
        "mean_changed_targets_per_intervention_step": (
            mean(changed_target_counts) if changed_target_counts else 0.0
        ),
        "max_changed_targets_in_one_step": max(changed_target_counts, default=0),
        "risk_interventions_by_decision_source": dict(risk_by_source),
        "risk_interventions_by_phase": dict(risk_by_phase),
        "risk_interventions_by_reason": dict(risk_by_reason),
        "risk_interventions_by_cache_state": dict(risk_by_cache_state),
        "risk_interventions_by_visible_enemy_count": dict(visible_enemy_counts),
        "risk_filter_samples": risk_samples,
    }


def percent(value: float) -> str:
    return f"{100.0 * value:.1f}%"


def write_markdown(path: Path, results: Sequence[Dict]) -> None:
    lines = [
        "# Verifier Intervention Audit",
        "",
        "This deterministic offline audit uses the retained formal experiment logs. "
        "It measures observable normalization and risk-filter interventions without "
        "making new model calls.",
        "",
        "## Summary",
        "",
        "| Metric | " + " | ".join(item["label"] for item in results) + " |",
        "|---|" + "|".join("---:" for _ in results) + "|",
    ]
    metrics = [
        ("LLM calls", lambda r: f'{r["llm_calls"]:,}'),
        (
            "Raw schema-valid calls",
            lambda r: f'{r["raw_schema_valid_calls"]:,} ({percent(r["raw_schema_valid_rate"])})',
        ),
        (
            "Would fail strict schema without normalization",
            lambda r: f'{r["strict_schema_rejections_without_normalization"]:,}',
        ),
        ("Normalization interventions", lambda r: f'{r["normalization_interventions"]:,}'),
        (
            "Risk-filter changed steps",
            lambda r: f'{r["risk_filter_changed_steps"]:,} ({percent(r["risk_filter_changed_step_rate"])})',
        ),
        ("Risk-filter changed targets", lambda r: f'{r["risk_filter_changed_targets"]:,}'),
        (
            "Mean changed targets per intervention step",
            lambda r: f'{r["mean_changed_targets_per_intervention_step"]:.2f}',
        ),
    ]
    for name, formatter in metrics:
        lines.append("| " + name + " | " + " | ".join(formatter(r) for r in results) + " |")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "1. A raw-schema rejection count is a deterministic formatting counterfactual: "
            "these responses would not pass the strict raw schema without the implemented "
            "normalization path.",
            "2. A risk-filter intervention records that the deterministic verifier changed "
            "one or more proposed targets before action construction.",
            "3. These counts demonstrate operational use of the verifier. They do not, by "
            "themselves, prove that an intervention improved match outcome.",
            "",
        ]
    )

    for result in results:
        lines.extend(
            [
                f'## {result["label"]}',
                "",
                "### Normalization types",
                "",
                "| Type | Calls |",
                "|---|---:|",
            ]
        )
        for name, count in sorted(result["normalization_types"].items()):
            lines.append(f"| `{name}` | {count:,} |")
        if not result["normalization_types"]:
            lines.append("| None observed | 0 |")

        lines.extend(
            [
                "",
                "### Risk-filter interventions by decision source",
                "",
                "| Decision source | Steps |",
                "|---|---:|",
            ]
        )
        for name, count in sorted(
            result["risk_interventions_by_decision_source"].items(),
            key=lambda item: (-item[1], item[0]),
        ):
            lines.append(f"| `{name}` | {count:,} |")

        lines.extend(
            [
                "",
                "### Risk-filter interventions by phase",
                "",
                "| Phase | Steps |",
                "|---|---:|",
            ]
        )
        for name, count in sorted(
            result["risk_interventions_by_phase"].items(),
            key=lambda item: (-item[1], item[0]),
        ):
            lines.append(f"| `{name}` | {count:,} |")

        lines.extend(
            [
                "",
                "### Recorded verifier reasons",
                "",
                "| Reason | Steps |",
                "|---|---:|",
            ]
        )
        for name, count in sorted(
            result["risk_interventions_by_reason"].items(),
            key=lambda item: (-item[1], item[0]),
        ):
            lines.append(f"| {name} | {count:,} |")
        lines.append("")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, results: Sequence[Dict]) -> None:
    fields = [
        "label",
        "experiment_directory",
        "llm_calls",
        "raw_schema_valid_calls",
        "raw_schema_valid_rate",
        "strict_schema_rejections_without_normalization",
        "normalization_interventions",
        "llm_agent_steps",
        "risk_filter_changed_steps",
        "risk_filter_changed_step_rate",
        "risk_filter_changed_targets",
        "mean_changed_targets_per_intervention_step",
        "max_changed_targets_in_one_step",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for result in results:
            writer.writerow({field: result[field] for field in fields})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--experiment",
        action="append",
        type=parse_experiment,
        help="Experiment as LABEL=PATH; repeat for multiple experiments.",
    )
    parser.add_argument(
        "--output-prefix",
        type=Path,
        default=ROOT / "reports" / "verifier_intervention_audit",
    )
    parser.add_argument("--sample-limit", type=int, default=3)
    args = parser.parse_args()

    experiments = args.experiment or list(DEFAULT_EXPERIMENTS)
    results = [
        audit_experiment(label, path, max(0, args.sample_limit))
        for label, path in experiments
    ]
    output_prefix = args.output_prefix.resolve()
    output_prefix.parent.mkdir(parents=True, exist_ok=True)
    json_path = output_prefix.with_suffix(".json")
    md_path = output_prefix.with_suffix(".md")
    csv_path = output_prefix.with_suffix(".csv")
    json_path.write_text(
        json.dumps(
            {
                "scope": "offline verifier intervention audit",
                "causal_claim": False,
                "experiments": results,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    write_markdown(md_path, results)
    write_csv(csv_path, results)
    print(json_path)
    print(md_path)
    print(csv_path)


if __name__ == "__main__":
    main()
