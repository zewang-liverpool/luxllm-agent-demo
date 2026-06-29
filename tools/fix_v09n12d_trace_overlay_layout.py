from pathlib import Path

path = Path("docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html")

html = path.read_text(encoding="utf-8", errors="replace")

html = html.replace(
    "right: 18px;\n    width: 360px;",
    "right: 280px;\n    width: 340px;"
)

html = html.replace(
    "right: 22px;\n    bottom: 16px;",
    "right: 300px;\n    bottom: 16px;"
)

path.write_text(html, encoding="utf-8")

print(f"Updated overlay layout in {path}")
