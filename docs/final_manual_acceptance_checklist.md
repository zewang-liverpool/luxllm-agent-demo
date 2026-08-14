# LuxLLM-Agent Final Manual Acceptance Checklist

## Acceptance rule

The project is ready for final submission when every mandatory item below is marked PASS, or when an intentionally excluded item has a written justification. Perform the checks from:

```text
D:\PythonProject\lux_llm_agent
```

Record the date, tester, and any observation directly in a copy of this checklist.

## A. Repository and reproducibility

| ID | Check | Local path or command | Pass condition | Status |
| --- | --- | --- | --- | --- |
| A1 | Correct branch | `git status --short --branch` | Shows `main...origin/main` and no tracked changes | ☐ |
| A2 | Clean clone instructions | `D:\PythonProject\lux_llm_agent\docs\reproducibility_guide.md` | Setup steps are understandable and paths exist | ☐ |
| A3 | Dependency declarations | `requirements.txt`, `requirements-dev.txt`, `environment.yml`, `pyproject.toml` | All files exist and agree on supported Python | ☐ |
| A4 | Windows setup | `powershell -ExecutionPolicy Bypass -File scripts\setup.ps1` | Virtual environment and dependencies install without error | ☐ |
| A5 | Automated tests | `.venv\Scripts\python.exe -m pytest -q` | All tests pass | ☐ |
| A6 | Smoke test | `.venv\Scripts\python.exe scripts\smoke_test.py` | All smoke checks pass | ☐ |
| A7 | CI definition | `.github\workflows\ci.yml` | GitHub Actions check is green on `main` | ☐ |
| A8 | No large raw evidence tracked | `git ls-files archive results docs/demo_videos` | No `.tar.gz`, formal raw result directory, or MP4 is tracked | ☐ |

## B. Evidence integrity

| ID | Check | Local path | Pass condition | Status |
| --- | --- | --- | --- | --- |
| B1 | Qwen archive retained | `D:\PythonProject\lux_llm_agent\archive\barkla_transfer\9755477_qwen3_32b_paired.tar.gz` | File exists; SHA-256 is `C25D30A0B4CD826EFF0A4F28F26457DA03352FA6E164F62A7973646A08ED277D` | ☐ |
| B2 | DeepSeek archive retained | `D:\PythonProject\lux_llm_agent\archive\barkla_transfer\9756874_deepseek-r1_32b_paired.tar.gz` | File exists; SHA-256 is `285BFEAF7D1725EB2A619D60D6BACE3924ED260E11D9CB969D50F5EE5779C180` | ☐ |
| B3 | Direct dual-LLM archive retained | `D:\PythonProject\lux_llm_agent\archive\barkla_transfer\9845992_qwen3_32b_vs_deepseek-r1_32b.tar.gz` | File exists; SHA-256 is `2B16B3C03EDA364F599F2EEF8884669124A1398D5BA1AAB7DE4709D9CF8A4EA7` | ☐ |
| B4 | Primary formal report | `reports\final_trace_evaluation.md` | Reports 200 matches and 206,591 trace records | ☐ |
| B5 | Dual-LLM report | `reports\dual_llm_trace_evaluation.md` | Reports 100 matches, 106,317 trace records, and 4,676 valid calls | ☐ |
| B6 | Machine-readable reports | `reports\final_trace_evaluation.json`, `reports\dual_llm_trace_evaluation.json` | Both open as valid JSON | ☐ |
| B7 | Metrics tables | `reports\final_trace_metrics.csv`, `reports\dual_llm_trace_metrics.csv` | Open and agree with the Markdown reports | ☐ |
| B8 | Claims remain bounded | `paper\main.tex`, Chapter 6, Chapter 7 | No universal model-ranking or proof-of-safety claim | ☐ |

## C. Dissertation

| ID | Check | Local path | Pass condition | Status |
| --- | --- | --- | --- | --- |
| C1 | Canonical assembled draft | `docs\dissertation\full_dissertation_draft.md` | Contains front matter and Chapters 1-7 | ☐ |
| C2 | Research question consistency | Chapters 1, 3, 6, and 7 | Exact main research question is consistent | ☐ |
| C3 | Formal experiment consistency | Chapters 1, 3, 6, and 7 | Uses 100 matches/backend and matched role swapping as primary evidence | ☐ |
| C4 | Historical evidence labelled | Chapter 6 | Earlier fixed-role 50-run results are explicitly historical | ☐ |
| C5 | Citations | Chapter 2 and final university document | Every in-text citation appears in the final bibliography | ☐ |
| C6 | Figures and tables | University-formatted dissertation | Every figure/table is numbered, captioned, legible, and referenced in text | ☐ |
| C7 | Front-page metadata | University-formatted dissertation | Student ID, degree/programme, module, supervisor, and submission date match official records | ☐ |
| C8 | Language and encoding | Full document | No mojibake characters such as `鈥` or malformed quotation marks | ☐ |
| C9 | Final PDF | User-selected university submission path | Opens correctly; page numbers, contents, references, and margins are correct | ☐ |

## D. Demonstration

| ID | Check | Local path or URL | Pass condition | Status |
| --- | --- | --- | --- | --- |
| D1 | Demo runbook | `docs\final_demo_runbook.md` | Presenter can follow it without additional instructions | ☐ |
| D2 | Local server | `python -m http.server 8000` | Starts without a port error | ☐ |
| D3 | Viewer | `http://localhost:8000/docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html` | Presentation Mode opens by default; the board is unobstructed; all three stages are visible without panel scrolling at 1280×720 | ☐ |
| D4 | Replay data | `logs\isometric_replay_frames_v09n11.json` | Viewer timeline has data | ☐ |
| D5 | Trace overlay data | `data\run008_decision_trace_overlay.json` | Trace panel displays step-aligned information | ☐ |
| D6 | Backup video | `docs\demo_videos\LuxLLM_Agent_Final_Demo_Run008_Isometric_Visualization.mp4` | H.264/AAC video plays with sound for 75.33 seconds | ☐ |
| D7 | Timing rehearsal | `docs\final_demo_runbook.md` | Complete presentation takes 7-10 minutes | ☐ |
| D8 | Q&A rehearsal | Runbook question section | Presenter can answer all five questions clearly, including the direct LLM-versus-LLM scope question | ☐ |
| D9 | Supervisor UI feedback | Viewer header and trace panel | `Lux AI Season 3` is prominent; `Proposal Context`, `Rule Verification`, and `Executed State` are visually distinct; rejected proposals are not labelled valid | ☐ |

## E. GitHub and final package

| ID | Check | Location | Pass condition | Status |
| --- | --- | --- | --- | --- |
| E1 | GitHub main | `https://github.com/zewang-liverpool/luxllm-agent-demo` | Latest reproducibility PR is present on `main` | ☐ |
| E2 | README links | GitHub README | Internal tracked links open | ☐ |
| E3 | Release video | GitHub Releases | Final demo video is accessible, or local-only status is documented | ☐ |
| E4 | License | `LICENSE` | License is present and matches README | ☐ |
| E5 | Submission backup | User-selected backup locations | Final PDF, source, video, and evidence checksums exist in at least two locations | ☐ |

## Final sign-off

```text
Tester:
Date:
Repository commit:
Dissertation PDF path:
Demo video path:
Outstanding non-blocking issues:
Final decision: PASS / FAIL
```
