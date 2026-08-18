# CA2 PPT image asset manifest

This folder contains the project-grounded images prepared for the CA2 slide deck.

| File | Recommended use | What it shows | Important wording |
|---|---|---|---|
| `01_player_view_midgame.png` | Main Slide 2 image | Player View at a non-zero mid-match state, with map, score, phase, ships, HUD and replay controls visible | Describe this as the player-facing replay view. |
| `02_dtav_inspector_intervention.png` | Main Slide 4 image | A replay-linked DTAV Inspector example in which a recorded proposal is rejected and deterministic fallback supplies the executed action | Describe this as an intervention/fallback example. Do **not** call it a valid fresh LLM decision. |
| `03_framework_evidence_rates.png` | Main Slide 6 supporting chart | Trace completeness, replay linkage, post-check validity and related evidence rates for Direct Prompt and DTAV | Use the large 48%, 63% and +15 pp outcome numbers as the visual focus; this chart is supporting evidence. |
| `04_decision_source_distribution.png` | Backup/Q&A slide | Distribution of fresh LLM, cached LLM and rule-fallback decision sources | Explain that the direct-prompt baseline follows the same scheduled-call protocol; its 95.5% rule-fallback-step rate is not a 95.5% LLM-call failure rate. |

All four images are based on the current project Viewer or retained formal experiment evidence. Avoid stretching them; crop proportionally if needed.
