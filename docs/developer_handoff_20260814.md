# LuxLLM-Agent 开发交接文档

更新时间：2026-08-14（Europe/London）

本地项目根目录：`D:\PythonProject\lux_llm_agent`

GitHub：<https://github.com/zewang-liverpool/luxllm-agent-demo>

## 0. 接手前必须先知道的事情

当前技术开发和正式 GPU 实验已经达到项目定义的收口标准。接下来工作的重点不是继续无限增加模型或重复实验，而是：

1. 完成 CA2 视频、演示排练和 Q&A 准备；
2. 人工核对毕业论文事实、引用、图表和学校格式；
3. 以 GitHub 当前审查分支为交接基线，修改前先同步并运行验证；
4. 只在测试失败、证据不一致、导师指出事实错误或出现提交阻断问题时重新修改核心代码。

### 当前 Git 交接基线

- 当前分支：`codex/dissertation-final-closeout`
- 当前准确提交请运行 `git log -1 --oneline`；不要依赖本文中的历史哈希。
- 在该分支合并前，只克隆 GitHub `main` 可能无法得到最新的论文、Viewer 和 CA2 收口内容。
- 最新状态和问题修复摘要见 `docs/project_review_summary_20260814.md`。
- `.tmp/` 是生成和渲染产生的临时目录，不应提交。
- 接手人不得执行 `git reset --hard`、`git clean -fd`、强制切换覆盖文件或删除未跟踪文件。

在任何修改前先执行：

```powershell
cd D:\PythonProject\lux_llm_agent
git status -sb
git diff --stat
git log -1 --oneline
.venv\Scripts\python.exe -m pytest -q
.venv\Scripts\python.exe scripts\smoke_test.py
```

## 1. 项目身份、范围与研究问题

项目名称：

> LuxLLM-Agent: A Decision-Trace and Action-Verification Framework for Inspecting and Evaluating LLM-based Agents in Lux AI Season 3

主研究问题：

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

项目所有者：Ze Wang，University of Liverpool，`Z.Wang300@liverpool.ac.uk`

导师：Meng Fang，University of Liverpool，`mfang@liverpool.ac.uk`

### 项目应保持的定位

这是一个面向 Lux AI Season 3 的 LLM Agent 检查与评估框架。它的核心不是证明某个 LLM 是最强游戏模型，而是证明以下流程可以被记录、验证、复现和分析：

```text
Lux observation
  -> structured state summary
  -> bounded LLM unit-intent proposal
  -> parsing and deterministic normalization
  -> rule/risk verification
  -> legal action construction
  -> decision trace logging
  -> replay-grounded inspection and aggregate evaluation
```

LLM 只提出受限的高层单位意图，不直接输出最终可执行 Lux 动作。确定性代码保留执行控制权，并负责解析、规范化、缓存、回退、风险过滤和动作数组构造。

### 子研究问题

- RQ1：如何把原始 Lux AI Season 3 observation 转换为适合 LLM 战略决策的紧凑结构化输入？
- RQ2：规则验证、回退和策略缓存如何降低无效或不稳定的 LLM 决策？
- RQ3：基于 replay 对齐的 decision trace 如何支持对决策来源、动作执行和结果关系的分析？

## 2. 当前完成度

| 工作项 | 状态 | 说明 |
|---|---|---|
| 核心 Agent 管线 | 完成 | 状态摘要、LLM 决策、规范化、缓存、回退、风险过滤、动作规划均已实现 |
| 可复现安装 | 完成 | Windows/Linux setup、依赖清单和锁定环境已保留 |
| 自动化测试 | 完成 | 2026-08-14 本机验证为 `28 passed in 0.31s`；smoke test 与证据校验同时通过 |
| CI | 完成 | GitHub Actions 覆盖 Python 3.10/3.11 的无 GPU 检查 |
| 正式单模型实验 | 完成 | Qwen 与 DeepSeek 各 100 场，共 200 场 |
| 双 LLM 直接对战 | 完成 | 100 场、50 个 matched seeds、角色互换 |
| 原始运行证据 | 完成 | 三个大型归档及解压结果均保存在本地 |
| 证据分析与一致性校验 | 完成 | 机器可读报告、干预审计、验证脚本均已保留 |
| Replay viewer | 完成 | 可本地直接启动，无需 GPU 或 Ollama |
| 毕业论文草稿 | 主体完成，待人工收口 | 七章和完整合并稿已存在；需事实、引用、格式和最终 PDF 检查 |
| CA2 材料 | 自动准备完成，待本人完成 | PPT、旁白、Q&A、交互式清单已生成；需本人排练、录音、检查和提交 |

## 3. 已验证的主要实证结果

### 3.1 主要实验：LLM-assisted agent 对共享规则基线

实验协议：每个模型使用 50 个相同环境种子，每个种子进行两次角色互换，因此每个模型 100 场，共 200 场。

| 指标 | Qwen3-32B | DeepSeek-R1-32B |
|---|---:|---:|
| 完成比赛 | 100 | 100 |
| LLM 胜场 | 63 | 60 |
| Structured trace records | 103,286 | 103,305 |
| LLM calls | 2,286 | 2,305 |
| 规范化后结构有效 | 2,286 / 2,286 | 2,305 / 2,305 |
| 原始 schema 有效 | 1,766 / 2,286（77.3%） | 2,305 / 2,305（100%） |
| 需要确定性规范化 | 520 | 0 |
| 风险过滤改变的 step | 5,590 | 7,090 |
| LLM timeout / error | 0 / 0 | 0 / 0 |
| Action-array shape validity | 100% | 100% |

总计：200/200 比赛完成、206,591 条 trace、4,591/4,591 次 LLM 调用在检查和规范化后有效。

解释边界：Qwen 63% 和 DeepSeek 60% 是受控配置下的次要 outcome。配对比较没有支持通用模型排名；项目的主要证据是 trace completeness、decision provenance、normalization、verifier intervention、action validity 和 replay linkage。

### 3.2 补充实验：Qwen-assisted 对 DeepSeek-assisted

实验协议：50 个 matched seeds、角色互换，共 100 场。双方均进行独立 LLM 调用、验证和日志记录。

| 指标 | 结果 |
|---|---:|
| 完成比赛 | 100 / 100 |
| Qwen 胜场 | 54 |
| DeepSeek 胜场 | 46 |
| Structured trace records | 106,317 |
| Fresh LLM calls | 4,676 |
| 规范化后结构有效 | 4,676 / 4,676 |
| 原始 schema 有效 | 4,105 / 4,676（87.8%） |
| 需要确定性规范化 | 571 |
| 风险过滤改变的 step | 15,721 |
| 风险过滤改变的 targets | 85,805 |
| LLM timeout / error | 0 / 0 |
| Exact seed-level sign p-value | 0.5034 |

该实验用于证明两个 LLM-assisted agent 同时对战时，框架仍能进行双侧 tracing 和 verification。54:46 不应描述为 Qwen 的通用优势。

## 4. 五分钟接手路径

接手人按以下顺序阅读即可建立正确心智模型：

1. `D:\PythonProject\lux_llm_agent\docs\developer_handoff_20260814.md`：本交接文档。
2. `D:\PythonProject\lux_llm_agent\README.md`：项目定位、架构和正式结果总览。
3. `D:\PythonProject\lux_llm_agent\docs\project_closeout_standard.md`：什么时候停止修改。
4. `D:\PythonProject\lux_llm_agent\docs\reproducibility_guide.md`：安装、测试、运行和证据再生成。
5. `D:\PythonProject\lux_llm_agent\docs\technical\system_architecture.md`：系统架构。
6. `D:\PythonProject\lux_llm_agent\docs\technical\llm_decision_pipeline.md`：LLM 决策管线。
7. `D:\PythonProject\lux_llm_agent\reports\final_trace_evaluation.md`：主要正式证据。
8. `D:\PythonProject\lux_llm_agent\reports\dual_llm_trace_evaluation.md`：双 LLM 补充证据。
9. `D:\PythonProject\lux_llm_agent\docs\dissertation\dissertation_draft_index.md`：论文结构和章节入口。
10. `D:\PythonProject\lux_llm_agent\docs\ca2\README.md`：CA2 文件入口。

## 5. 环境安装与本地验收

### 5.1 Windows

```powershell
cd D:\PythonProject\lux_llm_agent
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
.\.venv\Scripts\python.exe scripts\smoke_test.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools\validate_project_evidence.py
```

期望结果：

```text
28 passed
Project evidence validation passed.
```

可选的真实 Lux 规则策略 smoke match：

```powershell
.\.venv\Scripts\python.exe scripts\run_rule_smoke.py --seed 42
```

通过标准是 `status=complete`、return code 为 0、双方 reward 能被解析；具体比分可能受依赖版本影响。

### 5.2 Linux / Barkla2

```bash
cd ~/luxllm-agent
PYTHON_BIN=python3.11 bash scripts/setup.sh
.venv/bin/python scripts/smoke_test.py
.venv/bin/python -m pytest -q
```

正式 32B 重跑还需要 Barkla2、Ollama 和合适 GPU。当前项目已保留正式结果，不需要为了交接重新跑 GPU。

## 6. 核心代码位置

所有主要运行代码位于：`D:\PythonProject\lux_llm_agent\src\agent`

| 文件 | 职责 | 修改时重点回归 |
|---|---|---|
| `src/agent/main.py` | Agent 运行入口 | Lux runner/subprocess 协议 |
| `src/agent/agent.py` | 主运行编排和决策流程 | decision source、日志、缓存与 fallback 连接 |
| `src/agent/config.py` | 环境变量和运行配置 | 默认值、模型名、超时、采样参数 |
| `src/agent/lux_state.py` | Lux observation 状态表示 | 玩家视角、坐标和状态字段 |
| `src/agent/game_memory.py` | 跨 step 游戏记忆 | stale/confirmed 信息的生命周期 |
| `src/agent/state_summarizer.py` | 原始状态到紧凑战略摘要 | prompt 字段、token/字符规模、信息丢失 |
| `src/agent/llm_decider.py` | Ollama 调用、JSON 解析、schema 校验和规范化 | raw_text、parsed、valid、fallback_reason |
| `src/agent/action_planner.py` | 验证后 intent 到合法 action array | action shape、边界、能量和目标安全 |
| `src/agent/rule_policy.py` | 规则策略、回退和风险控制 | verifier intervention、fallback 可观察性 |
| `src/agent/baseline_agent.py` | 共享规则基线 | 对照实验公平性 |

核心调用链修改后至少运行：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\smoke_test.py
.\.venv\Scripts\python.exe scripts\run_mock_llm_smoke.py
.\.venv\Scripts\python.exe scripts\run_mock_dual_llm_smoke.py
```

## 7. 实验和分析脚本位置

目录：`D:\PythonProject\lux_llm_agent\scripts`

| 文件 | 用途 |
|---|---|
| `scripts/setup.ps1` | Windows 环境创建/修复 |
| `scripts/setup.sh` | Linux/Barkla2 环境创建/修复 |
| `scripts/smoke_test.py` | 编译、viewer 数据和单测总 smoke |
| `scripts/run_rule_smoke.py` | 无 LLM 的真实 Lux end-to-end smoke |
| `scripts/mock_ollama_server.py` | 本地确定性 mock Ollama |
| `scripts/run_mock_llm_smoke.py` | 单 LLM 管线 smoke |
| `scripts/run_mock_dual_llm_smoke.py` | 双 LLM 管线 smoke |
| `scripts/run_paired_experiment.py` | matched-seed、role-swapped 单 LLM 实验 |
| `scripts/run_dual_llm_experiment.py` | Qwen vs DeepSeek 双 LLM 实验 |
| `scripts/barkla_paired_experiment.sbatch` | Barkla2 单 LLM 正式任务 |
| `scripts/barkla_dual_llm_experiment.sbatch` | Barkla2 双 LLM 正式任务 |

分析工具目录：`D:\PythonProject\lux_llm_agent\tools`

| 文件 | 用途 |
|---|---|
| `tools/evaluation_stats.py` | 统计区间与配对分析 |
| `tools/analyse_trace_evidence.py` | 从正式 logs 生成 trace Markdown/JSON/CSV/figure |
| `tools/audit_verifier_interventions.py` | 审计 schema normalization 和 risk-filter intervention |
| `tools/validate_project_evidence.py` | 检查报告、文档和正式证据一致性 |
| `tools/validate_dual_llm_result.py` | 检查双 LLM 结果完整性和双方 fresh calls |
| `tools/compare_paired_experiments.py` | 比较两个 paired 实验 |
| `tools/recompute_reported_metrics.py` | 重新计算已报告指标 |
| `tools/assemble_dissertation.py` | 从 front matter 和七章确定性合并完整论文 Markdown |
| `tools/build_run008_decision_trace_overlay.py` | 构建 Run008 trace overlay 数据 |
| `tools/build_v09n12d_trace_overlay_viewer.py` | 构建当前 viewer |
| `tools/fix_v09n12d_trace_overlay_layout.py` | 修复 viewer overlay 布局 |

## 8. 测试与 CI 位置

| 路径 | 覆盖内容 |
|---|---|
| `tests/test_agent_core.py` | 核心 Agent、解析、fallback、timeout、配置 |
| `tests/test_experiment_runner.py` | paired/dual runner 行为和结果组织 |
| `tests/test_evaluation_stats.py` | 统计计算 |
| `tests/test_trace_evidence.py` | trace 指标、干预审计和分析 |
| `tests/test_project_consistency.py` | 项目声明、路径和证据一致性 |
| `.github/workflows/ci.yml` | GitHub Actions 无 GPU 自动测试 |

新增功能应优先在相应测试文件添加回归测试。CI 故意不下载模型或执行 GPU inference。

## 9. 正式证据、原始归档和报告位置

### 9.1 原始解压结果（本地，不应推送 GitHub）

- Qwen：`D:\PythonProject\lux_llm_agent\archive\barkla_results\9755477_qwen3_32b_paired`
- DeepSeek：`D:\PythonProject\lux_llm_agent\archive\barkla_results\9756874_deepseek-r1_32b_paired`
- 双 LLM：`D:\PythonProject\lux_llm_agent\archive\barkla_results\dual_llm_9845992\results\9845992_qwen3_32b_vs_deepseek-r1_32b`

每个正式实验目录的关键内容是：

```text
environment.json
match_history.jsonl
summary.json
runs/<seed-role>/result.json
runs/<seed-role>/logs/*.jsonl
```

### 9.2 原始压缩包（本地备份，不应推送 GitHub）

- `archive/barkla_transfer/9755477_qwen3_32b_paired.tar.gz`，SHA-256：`C25D30A0B4CD826EFF0A4F28F26457DA03352FA6E164F62A7973646A08ED277D`
- `archive/barkla_transfer/9756874_deepseek-r1_32b_paired.tar.gz`，SHA-256：`285BFEAF7D1725EB2A619D60D6BACE3924ED260E11D9CB969D50F5EE5779C180`
- `archive/barkla_transfer/9845992_qwen3_32b_vs_deepseek-r1_32b.tar.gz`，SHA-256：`2B16B3C03EDA364F599F2EEF8884669124A1398D5BA1AAB7DE4709D9CF8A4EA7`
- Barkla2 可复现代码包：`archive/barkla_transfer/luxllm-agent-repro-c7880e7.zip`
- Barkla2 双 LLM 代码包：`archive/barkla_transfer/luxllm-agent-dual-3f7a7f5.zip`

不要将约 500 MB 的原始归档加入 Git。GitHub 只保存经过审查的紧凑报告和图。

### 9.3 Git 可追踪的正式报告

主要实验：

- `reports/final_trace_evaluation.md`
- `reports/final_trace_evaluation.json`
- `reports/final_trace_metrics.csv`
- `reports/verifier_intervention_audit.md`
- `reports/verifier_intervention_audit.json`
- `reports/verifier_intervention_audit.csv`
- `reports/figures/decision_source_distribution.png`
- `reports/figures/framework_evidence_rates.png`

双 LLM 补充实验：

- `reports/dual_llm_trace_evaluation.md`
- `reports/dual_llm_trace_evaluation.json`
- `reports/dual_llm_trace_metrics.csv`
- `reports/dual_llm_verifier_audit.md`
- `reports/dual_llm_verifier_audit.json`
- `reports/dual_llm_verifier_audit.csv`
- `reports/dual_llm_figures/decision_source_distribution.png`
- `reports/dual_llm_figures/framework_evidence_rates.png`

其他验收材料：

- `reports/reproducibility_validation.md`
- `reports/final_capture_verification.md`
- `reports/recomputed_metrics.md`
- `reports/recomputed_metrics.json`

### 9.4 本地离线再生成

无需 GPU 或 Ollama：

```powershell
cd D:\PythonProject\lux_llm_agent
.\.venv\Scripts\python.exe tools\audit_verifier_interventions.py
.\.venv\Scripts\python.exe tools\validate_project_evidence.py
```

双 LLM 报告完整再生成命令见：

`D:\PythonProject\lux_llm_agent\docs\reproducibility_guide.md` 的 “Offline Evidence Audit” 部分。

## 10. Viewer、replay 和演示文件位置

### 当前 viewer

- HTML：`D:\PythonProject\lux_llm_agent\docs\viewers\s3_isometric_battle_viewer_v09n12d_trace_overlay.html`
- 标准 replay 数据：`D:\PythonProject\lux_llm_agent\data\isometric_replay_frames.json`
- 决策 overlay：`D:\PythonProject\lux_llm_agent\data\run008_decision_trace_overlay.json`
- 原始/构建期 replay frames：`D:\PythonProject\lux_llm_agent\logs\isometric_replay_frames_v09n11.json`

启动方式：

```powershell
cd D:\PythonProject\lux_llm_agent
.\.venv\Scripts\python.exe -m http.server 8000
```

浏览器打开：

```text
http://localhost:8000/docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html
```

不要直接双击 HTML 作为最终验证方式，因为浏览器对本地 JSON 请求可能有限制。

### 演示文件

- 最终演示 runbook：`docs/final_demo_runbook.md`
- 人工验收清单：`docs/final_manual_acceptance_checklist.md`
- 主要备份/插入视频：`docs/demo_videos/LuxLLM_Agent_Final_Demo_Run008_Isometric_Visualization.mp4`
- 演示视频目录：`D:\PythonProject\lux_llm_agent\docs\demo_videos`

该 75.33 秒视频只能作为 CA2 的插入或 viewer 故障备份，不能单独作为完整 CA2 作业提交。

## 11. 毕业论文文件位置

论文 Markdown 根目录：`D:\PythonProject\lux_llm_agent\docs\dissertation`

### 规范源文件

- `front_matter.md`
- `chapter_1_introduction.md`
- `chapter_2_background_related_work.md`
- `chapter_3_requirements_methodology.md`
- `chapter_4_system_design.md`
- `chapter_5_implementation.md`
- `chapter_6_evaluation.md`
- `chapter_7_discussion_conclusion.md`
- `references.md`

### 导航和计划

- `dissertation_draft_index.md`：章节状态和资料索引。
- `full_dissertation_draft.md`：由工具生成的完整合并稿，不应与分章分别手工维护。
- `chapter_2_reference_plan.md`：文献和引用强化计划。
- `figures_and_tables_plan.md`：图表计划。
- `supervisor_review_summary.md`：给导师的审阅摘要。

### 人工检查和反馈响应

- `literature_and_citation_manual_checklist_20260728.md`
- `literature_and_citation_manual_checklist_20260728.html`
- `manual_review_and_supervisor_update_checklist_20260725.md`
- `manual_review_and_supervisor_update_checklist_20260725.html`
- `specification_feedback_response_20260728.md`
- `specification_grade_and_improvement_report_20260728.md`
- `project_freeze_checklist.md`

### 合并论文

修改分章后执行：

```powershell
cd D:\PythonProject\lux_llm_agent
.\.venv\Scripts\python.exe tools\assemble_dissertation.py
git diff -- docs\dissertation\full_dissertation_draft.md
```

提交前要人工检查：研究问题与 aim 数量、文献引用真实性、正文 citation 与 references 双向匹配、结果数字与 `reports/` 一致、图表标题、局限性措辞、学校模板、字数和 PDF 视觉效果。

### 旧 conference paper 资产

- LaTeX 主文件：`D:\PythonProject\lux_llm_agent\paper\main.tex`
- 已编译 PDF：`D:\PythonProject\lux_llm_agent\paper\main.pdf`
- BibTeX 数据：`D:\PythonProject\lux_llm_agent\paper\anthology.bib`、`custom.bib`
- Overleaf 说明：`D:\PythonProject\lux_llm_agent\paper\README.md`

当前任务是硕士毕设论文和 CA2，不要把 conference paper 投稿格式当作毕业论文模板。

## 12. CA2 文件位置与当前人工任务

CA2 根目录：`D:\PythonProject\lux_llm_agent\docs\ca2`

| 文件 | 用途 |
|---|---|
| `LuxLLM_Agent_CA2_Presentation.pptx` | 七页最终 CA2 PPT，使用当前 Viewer 和正式实验数据 |
| `CA2_NARRATION_SCRIPT.md` | 约 9 分 20 秒的英文旁白和屏幕操作脚本 |
| `CA2_QA_PREPARATION.md` | 评审可能提问及短答案 |
| `CA2_RECORDING_AND_SUBMISSION_CHECKLIST.html` | 可在浏览器勾选并保存状态的交互式人工清单 |
| `CA2_AUTOMATED_READINESS.md` | 自动验收结果 |
| `source-notes.txt` | PPT 使用的证据和资产来源 |
| `README.md` | CA2 包说明 |

伦理声明已确认为 `A0`：

- A：不使用来源于人类或动物的数据；
- 0：任何活动均不使用人类参与者。

自动部分已通过：测试、证据验证、PPT 生成、渲染、overflow 检查、伦理类别和视频文件完整性。

仍需项目本人完成：

1. 用自己的声音排练和录制；
2. 确保最终视频少于 10 分钟，建议控制在 9:20–9:40；
3. 人工检查音量、画面、字幕/文字可读性、代码和 viewer 操作是否流畅；
4. 在 Canvas 核对实际 deadline、格式和上传入口；
5. 上传后重新下载或在线播放确认文件可用；
6. 参加约 10–15 分钟 Q&A，并记录评审的口头反馈用于论文修订。

## 13. 技术文档和分析材料位置

系统设计：`D:\PythonProject\lux_llm_agent\docs\technical`

- `system_architecture.md`
- `llm_decision_pipeline.md`
- `action_verification_and_fallback.md`
- `decision_trace_overlay.md`
- `evaluation_metrics.md`

分析：`D:\PythonProject\lux_llm_agent\docs\analysis`

- `qwen3_vs_deepseek_analysis.md`
- `failure_case_analysis.md`

项目总体汇报：

- `D:\PythonProject\lux_llm_agent\docs\supervisor_project_report_20260716.md`

可复现性与收口：

- `docs/reproducibility_guide.md`
- `docs/project_closeout_standard.md`
- `docs/final_demo_runbook.md`
- `docs/final_manual_acceptance_checklist.md`

## 14. 接下来应做什么

### P0：立即处理

1. 人工审查当前未提交 diff，尤其是所有论文数字、引用和 CA2 表述。
2. 确认 `.tmp/` 和其他生成缓存不进入提交。
3. 在当前分支提交论文收口和 CA2 材料，推送并建立 PR；合并前再运行 smoke、pytest 和 evidence validator。
4. 按 `docs/ca2/CA2_NARRATION_SCRIPT.md` 排练 viewer、报告和三段核心代码展示。
5. 录制 CA2，完成交互式清单并准备 Q&A。

### P1：论文人工收口

1. 向导师或 module team 确认 University dissertation template、引用格式、页数/字数和提交文件要求。
2. 逐条完成人工文献与 citation checklist。
3. 确认所有正式数字只引用 `reports/final_*` 和 `reports/dual_llm_*`；历史固定角色 50-run 结果必须标为历史材料。
4. 将 Markdown 转入学校要求的最终格式，生成 PDF 后逐页检查。

### P2：只有导师明确要求才做

- 新增模型；
- 新的 50/100-run GPU 实验；
- UI 新功能；
- 用户研究；
- leaderboard 优化；
- live 32B demo。

## 15. 修改停止标准

以下条件已经满足时停止技术扩展：

- clean setup 能恢复环境；
- smoke 和 28 项测试通过；
- 200 场主要实验和 100 场双 LLM 实验都完整保留；
- trace、schema validity、normalization、risk intervention、action shape、timeout/error 和 replay linkage 都有可再生证据；
- viewer、报告和规范文档一致；
- 双 LLM 实验被解释为补充 framework evidence，而不是模型 leaderboard。

只有以下情况才重新打开代码开发：

- 测试或可复现检查失败；
- 导师指出事实错误或明确缺失比较；
- 报告与原始证据出现实质不一致；
- 出现阻止 CA2 或 dissertation 提交的问题。

其他情况下应继续提交准备，而不是不断优化。

## 16. Git 交接和提交流程

### 当前机器上继续开发

```powershell
cd D:\PythonProject\lux_llm_agent
git switch codex/dissertation-final-closeout
git status -sb
.\.venv\Scripts\python.exe scripts\smoke_test.py
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe tools\validate_project_evidence.py
```

审查完成后只暂存明确需要的文件，不要执行 `git add .`：

```powershell
git add docs\dissertation docs\ca2 docs\final_demo_runbook.md docs\final_manual_acceptance_checklist.md docs\developer_handoff_20260814.md
git status --short
git diff --cached --stat
git diff --cached --check
```

然后再由项目所有者确认 commit、push 和 PR。原始归档、`.tmp/`、大视频和本地缓存不要加入本次提交。

### 交给另一台机器

最稳妥的方法是先把当前分支的已审查改动提交并推送，再让接手人：

```powershell
git clone https://github.com/zewang-liverpool/luxllm-agent-demo.git
cd luxllm-agent-demo
git fetch origin
git switch --track origin/codex/dissertation-final-closeout
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1
```

如果分支尚未推送，则必须额外传递本地工作区或 patch；只发送 GitHub `main` 链接会遗漏当前论文和 CA2 改动。大型 Barkla 原始归档也必须通过独立存储传递，不能依赖 GitHub。

## 17. 快速定位全部文件

本文件列出的是所有开发、验证、论文和提交所需的操作性文件。若需查看仓库中每一个文件：

```powershell
cd D:\PythonProject\lux_llm_agent
rg --files
```

只查看 Git 跟踪文件：

```powershell
git ls-files
```

按关键词定位实现或声明：

```powershell
rg -n "llm_valid|fallback_reason|risk_filter|decision_source" src scripts tools tests docs reports
rg -n "63|60|54|46|206,591|106,317" README.md docs reports
```

## 18. 接手验收清单

- [ ] 已确认本地根目录和当前分支。
- [ ] 已阅读 README、收口标准、可复现指南和本交接文档。
- [ ] 已查看未提交改动，没有覆盖或删除它们。
- [ ] `scripts/smoke_test.py` 通过。
- [ ] `pytest -q` 显示 28 项通过。
- [ ] `tools/validate_project_evidence.py` 通过。
- [ ] viewer 能通过本地 HTTP server 加载 replay 和 trace。
- [ ] 已理解主要实验是 200 场，双 LLM 是 100 场补充证据。
- [ ] 已理解项目研究重点是 inspection 和 verification，不是模型排名。
- [ ] 已理解不需要重新跑 GPU，除非出现规定的 reopening condition。
- [ ] 已区分 GitHub 跟踪报告与本地大型原始归档。
- [ ] 已确定下一项任务属于 CA2、论文人工收口或真正的阻断修复。

## 19. 可直接转发给接手人的短消息

> 项目根目录是 `D:\PythonProject\lux_llm_agent`，GitHub 是 <https://github.com/zewang-liverpool/luxllm-agent-demo>。请先阅读 `docs/developer_handoff_20260814.md`、`docs/project_review_summary_20260814.md`、`README.md`、`docs/project_closeout_standard.md` 和 `docs/reproducibility_guide.md`。当前技术实现和 300 场正式/补充实验均已完成，主要任务是 CA2 和毕业论文收口。请从 GitHub 的 `codex/dissertation-final-closeout` 分支或其合并后的 `main` 开始，不要用清理命令覆盖现有工作。开始工作前先运行 `git status -sb`、`scripts/smoke_test.py`、`pytest -q` 和 `tools/validate_project_evidence.py`。没有测试失败、证据冲突、导师明确要求或提交阻断时，不要再增加 GPU 实验或扩展模型范围。
