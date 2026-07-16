"""Validate that tracked project claims agree with the formal evidence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from assemble_dissertation import DISSERTATION_DIR, OUTPUT, PARTS


ROOT = Path(__file__).resolve().parents[1]
FORMAL_REPORT = ROOT / "reports" / "final_trace_evaluation.json"
VERIFIER_AUDIT = ROOT / "reports" / "verifier_intervention_audit.json"

CANONICAL_CLAIM_FILES = (
    ROOT / "README.md",
    DISSERTATION_DIR / "chapter_1_introduction.md",
    DISSERTATION_DIR / "chapter_3_requirements_methodology.md",
    DISSERTATION_DIR / "chapter_5_implementation.md",
    DISSERTATION_DIR / "chapter_6_evaluation.md",
    DISSERTATION_DIR / "chapter_7_discussion_conclusion.md",
    OUTPUT,
)

FORBIDDEN_STALE_CLAIMS = (
    "Pending Barkla2 run",
    "Without matched-seed role swapping",
    "no confidence intervals or hypothesis tests are provided",
    "Current main evidence includes:",
)


def expected_full_draft() -> str:
    sections = [
        (DISSERTATION_DIR / name).read_text(encoding="utf-8").strip()
        for name in PARTS
    ]
    return "\n\n---\n\n".join(sections) + "\n"


def find_forbidden_claims(text: str) -> List[str]:
    return [claim for claim in FORBIDDEN_STALE_CLAIMS if claim in text]


def validate() -> List[str]:
    errors: List[str] = []
    for path in (FORMAL_REPORT, VERIFIER_AUDIT, *CANONICAL_CLAIM_FILES):
        if not path.is_file():
            errors.append(f"missing required file: {path.relative_to(ROOT)}")
    if errors:
        return errors

    formal = json.loads(FORMAL_REPORT.read_text(encoding="utf-8"))
    audit = json.loads(VERIFIER_AUDIT.read_text(encoding="utf-8"))
    experiments = formal.get("experiments", [])
    audited = audit.get("experiments", [])
    if len(experiments) != 2:
        errors.append(f"formal report should contain 2 experiments, found {len(experiments)}")
    if len(audited) != len(experiments):
        errors.append("verifier audit experiment count does not match formal report")

    total_matches = sum(int(item.get("completed_matches", 0)) for item in experiments)
    total_calls = sum(int(item.get("decision_log_calls", 0)) for item in experiments)
    total_records = sum(int(item.get("trace_records", 0)) for item in experiments)
    if total_matches != 200:
        errors.append(f"formal completed-match total should be 200, found {total_matches}")
    if total_calls != 4591:
        errors.append(f"formal LLM-call total should be 4,591, found {total_calls}")
    if total_records != 206591:
        errors.append(f"formal trace-record total should be 206,591, found {total_records}")

    audit_by_label = {item.get("label"): item for item in audited}
    for item in experiments:
        label = item.get("label")
        other = audit_by_label.get(label)
        if other is None:
            errors.append(f"verifier audit is missing experiment: {label}")
            continue
        comparisons = (
            ("decision_log_calls", "llm_calls"),
            ("raw_schema_valid_calls", "raw_schema_valid_calls"),
            ("normalization_interventions", "normalization_interventions"),
            ("risk_filter_changed_steps", "risk_filter_changed_steps"),
            ("risk_filter_changed_targets", "risk_filter_changed_targets"),
        )
        for formal_key, audit_key in comparisons:
            if item.get(formal_key) != other.get(audit_key):
                errors.append(
                    f"{label}: {formal_key}={item.get(formal_key)!r} "
                    f"does not match audit {audit_key}={other.get(audit_key)!r}"
                )

    required_tokens = {
        DISSERTATION_DIR / "chapter_1_introduction.md": (
            "200 formal matches",
            "206,591",
            "4,591",
        ),
        DISSERTATION_DIR / "chapter_6_evaluation.md": (
            "200 matches overall",
            "206,591",
            "4,591",
        ),
        DISSERTATION_DIR / "chapter_7_discussion_conclusion.md": (
            "206,591",
            "4,591",
        ),
    }
    for path, tokens in required_tokens.items():
        text = path.read_text(encoding="utf-8")
        for token in tokens:
            if token not in text:
                errors.append(f"{path.relative_to(ROOT)} is missing formal token: {token}")

    for path in CANONICAL_CLAIM_FILES:
        text = path.read_text(encoding="utf-8")
        for claim in find_forbidden_claims(text):
            errors.append(f"{path.relative_to(ROOT)} contains stale claim: {claim}")

    if OUTPUT.read_text(encoding="utf-8") != expected_full_draft():
        errors.append(
            "docs/dissertation/full_dissertation_draft.md is stale; "
            "run: python tools/assemble_dissertation.py"
        )
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Project evidence validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Project evidence validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
