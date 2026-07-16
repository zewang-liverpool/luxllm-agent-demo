"""Assemble the canonical Markdown dissertation from its reviewed components."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISSERTATION_DIR = ROOT / "docs" / "dissertation"
PARTS = [
    "front_matter.md",
    "chapter_1_introduction.md",
    "chapter_2_background_related_work.md",
    "chapter_3_requirements_methodology.md",
    "chapter_4_system_design.md",
    "chapter_5_implementation.md",
    "chapter_6_evaluation.md",
    "chapter_7_discussion_conclusion.md",
    "references.md",
]
OUTPUT = DISSERTATION_DIR / "full_dissertation_draft.md"


def main() -> None:
    missing = [name for name in PARTS if not (DISSERTATION_DIR / name).is_file()]
    if missing:
        raise SystemExit("Missing dissertation components: " + ", ".join(missing))

    sections = [
        (DISSERTATION_DIR / name).read_text(encoding="utf-8").strip()
        for name in PARTS
    ]
    OUTPUT.write_text("\n\n---\n\n".join(sections) + "\n", encoding="utf-8")
    print(OUTPUT)


if __name__ == "__main__":
    main()
