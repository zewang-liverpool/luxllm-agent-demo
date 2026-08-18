# CA2 PPT 人工制作指南（2026-08-18）

## 1. PPT 的任务与时间分配

这份 PPT 面向 COMP702 两位评审老师。它不是完整论文，也不是逐文件的项目说明。它需要在十分钟内回答四个问题：

1. 这是哪一种游戏，为什么 LLM 直接决策具有挑战？
2. 本项目提出了什么方法？
3. 软件如何让评审看到“提议—检查—执行”的过程？
4. 正式实验是否支持该方法有效？

建议使用 7 页，PPT 讲解约 4 分钟，Viewer 演示约 3 分钟，代码演示约 1 分钟，结论约 1 分钟，总时长控制在 9:00–9:30。

## 2. 建议的 7 页结构及可直接填入的英文内容

### Slide 1 — Title and ethics（约 20 秒）

标题：

> LuxLLM-Agent
> Decision Trace + Action Verification (DTAV)

副标题：

> Ze Wang · 201868809
> Supervisor: Dr Meng Fang
> COMP702 · Lux AI Season 3

伦理声明：

> ETHICAL CATEGORY: A0
> No human/animal-derived data or human participants. University of Liverpool ethical guidance followed.

本页不放截图。标题、姓名、导师和伦理类别必须清楚可读。

### Slide 2 — Game challenge and research question（约 50 秒）

标题：

> Lux AI Season 3 makes direct LLM decision-making difficult

左侧正文：

> GAME CHARACTERISTICS
>
> - Partially observable world state
> - Multiple units requiring coordinated actions
> - Long-horizon exploration and scoring
> - Strict action and resource constraints

研究问题：

> RESEARCH QUESTION
> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent and rule-constrained strategy game such as Lux AI Season 3, and how can the DTAV method address the observed limitations?

右侧放“玩家视角中期对局截图”。截图必须显示地图、双方分数、当前阶段、单位数和回放进度，不要使用 `0 : 0` 的第 1 帧。

### Slide 3 — Controlled method comparison（约 50 秒）

标题：

> The experiment compares direct prompting with the project-specific DTAV method

左侧：

> DIRECT PROMPT
>
> Compact observation
> → LLM response
> → minimum legal-action adapter
> → environment action

右侧：

> DTAV
>
> Compact observation
> → structured LLM proposal
> → validation, normalisation, cache and risk checks
> → verified or fallback action
> → trace and replay evidence

底部方法控制条件：

> Same Qwen3-32B model, 50 matched seeds, swapped player roles, temperature, prompt budget and call schedule.

本页使用 PowerPoint 原生箭头和文字即可，不需要截图。必须明确：DTAV 是本项目的方法名称，不是一个公认的通用术语。

### Slide 4 — Viewer and live demonstration（约 30 秒，随后切换到 Viewer 演示约 3 分钟）

标题：

> The Viewer links each proposal to the action that reached the game

左侧正文：

> 1 · PROPOSAL
> Source, model, objective, reason and unit intents.
>
> 2 · DETERMINISTIC CHECKS
> Schema result, normalisation, risk posture and fallback reason.
>
> 3 · EXECUTED STATE
> Replay score and action summary show what reached the environment.

右侧放“DTAV Inspector 干预/回退截图”。当前保留的 Viewer 回放适合展示 proposal rejected 与 deterministic fallback；应准确标注为验证器干预示例，不要称为有效 fresh LLM decision。正式调用有效率由 Slide 6 的实验报告与图表证明。

演示顺序：

1. 切到 Viewer 的 Player View。
2. 播放数秒，指出地图、分数、阶段和回放进度。
3. 打开 DTAV Inspector。
4. 依次点击 `Proposal attempt`、`Fallback checkpoint` 和 `Final frame`。
5. 解释这是项目生成的操作审计记录，不是模型隐藏的 chain-of-thought。

### Slide 5 — Selected implementation boundaries（约 35 秒，随后代码演示约 1 分钟）

标题：

> Three code boundaries keep execution control outside the LLM

三列内容：

> STATE — `state_summarizer.py`
> Converts raw observations and memory into bounded strategic features.

> DECIDE — `llm_decider.py`
> Requests structured intents and parses, validates and normalises responses.

> EXECUTE — `agent.py`
> Applies cache, verifier, risk filter and fallback before legal actions.

本页可以不放代码截图。讲完后切换到编辑器，只展示三个短位置：状态摘要字段、JSON/intent 检查入口、执行前 verifier/fallback 分支。不要滚动浏览整个文件。

### Slide 6 — Formal empirical results（约 60 秒）

标题：

> A matched comparison favours DTAV under the tested setup

顶部方法说明：

> Qwen3-32B; 50 matched seeds; roles swapped; 100 matches per method.

三个大数字：

> 48%
> DIRECT PROMPT
> 48 wins / 100 matches

> 63%
> DTAV
> 63 wins / 100 matches

> +15 pp
> MATCHED EFFECT
> 95% CI +6 to +25; McNemar p = .0059

本页可在下方或右下角补充小图：

> Post-check validity: 86.1% → 99.9%
> Rule-fallback steps: 95.5% → 5.6%

不要把 `p = .0059` 讲成“证明在所有环境中 DTAV 都更好”。只说明在记录的模型、种子和配置下，匹配比较支持 DTAV。

### Slide 7 — Answer and limitations（约 45 秒）

标题：

> DTAV improves usable decisions while keeping the action path inspectable

研究问题回答：

> Under the recorded configuration, direct prompting produced many responses that could not sustain strategy without rule fallback. DTAV improved structured-call usability and strategy continuity while retaining a complete operational audit path from proposal through verification to executed action and replay state.

限制：

> LIMITATIONS
>
> - One game environment and one model in the method comparison
> - A method-bundle comparison, not an isolation of every component
> - Operational traces explain the recorded decision path, not hidden model reasoning

结束句：

> The contribution is therefore an inspectable and reproducible LLM-based method for this type of strategy game, rather than a general model ranking.

## 3. 已准备好的两张 Viewer 图片

### Screenshot A — Player View mid-game

已经保存为：

`D:\PythonProject\lux_llm_agent\docs\ca2\ppt_assets_20260818\01_player_view_midgame.png`

截图要求：

- 浏览器窗口建议为 1920×1080，缩放设置为 80% 或 90%。
- DTAV Inspector 关闭，地图和右侧 Player HUD 同时完整显示。
- 停在中期帧，例如总进度的 40%–70%。
- 分数、单位数或回放阶段不能全部为零。
- 下方播放控制栏完整可见。
- 不显示浏览器地址栏、Windows 通知、个人账号或其他窗口。
- 确认右侧面板没有多余大块空白，文字没有被裁切。

用途：Slide 2。

### Screenshot B — DTAV Inspector intervention/fallback example

已经保存为：

`D:\PythonProject\lux_llm_agent\docs\ca2\ppt_assets_20260818\02_dtav_inspector_intervention.png`

截图要求：

- 打开 Inspector，同时保留 Player HUD；两个面板不得互相遮挡。
- 本图显示保留回放中的 `proposal rejected` 与 `deterministic fallback`，用于展示系统如何记录干预。
- Proposal 区域显示 model、objective、reason 和 recorded unit intents。
- Deterministic Checks 显示 rejected/fallback 原因；不要将本图描述成有效 LLM 调用。
- Executed State 应显示非零或有意义的 replay score/action summary。
- 截图必须包含 Inspector 标题、三个切换按钮以及三段信息中的主要字段。
- 正式实验中的 post-check validity 应引用 `reports/direct_prompt_vs_dtav_trace_analysis.json` 和 Slide 6 图表，而不是由这张历史回放截图推断。

用途：Slide 4。

## 4. 可选的补充截图

### Screenshot C — Rejected proposal and fallback

建议保存为：

`D:\PythonProject\lux_llm_agent\docs\ca2\screenshots\03_dtav_fallback_example.png`

选择一个 proposal rejected、normalised 或 fallback 的帧，用于 Q&A 备用，不必放入主 PPT。它可以证明系统不只是记录成功结果，也记录干预和替换原因。

### Screenshot D — Three focused code snippets

如果不方便在视频中实时打开编辑器，可分别截取：

- `src/agent/state_summarizer.py`：构建 compact observation 的位置。
- `src/agent/llm_decider.py`：JSON 请求、解析和 intent validation 的位置。
- `src/agent/agent.py`：verifier、risk filter、cache 或 fallback 的执行分支。

截图中每次只保留约 15–25 行代码，编辑器字体至少 18–20 px。不要使用整屏包含大量无关代码的截图。

## 5. 已有结果图片和证据文件

以下文件可以直接使用，不需要重新截图：

- `D:\PythonProject\lux_llm_agent\reports\direct_prompt_vs_dtav_figures\framework_evidence_rates.png`
- `D:\PythonProject\lux_llm_agent\reports\direct_prompt_vs_dtav_figures\decision_source_distribution.png`
- `D:\PythonProject\lux_llm_agent\reports\direct_prompt_vs_dtav_comparison.json`
- `D:\PythonProject\lux_llm_agent\reports\direct_prompt_vs_dtav_trace_analysis.json`

主 PPT 优先使用 `framework_evidence_rates.png`。`decision_source_distribution.png` 信息更技术化，建议作为 Q&A 备用或论文图，不要让它挤占主结果页。

## 6. 人工制作顺序

1. 复制 `LuxLLM_Agent_CA2_Presentation_20260818.pptx` 为一个新的工作副本。
2. 先只填入上述英文文字，不放截图。
3. 将每页标题保持为单行；如果换行，缩短标题而不是缩小字号。
4. 按要求重新截取 Player View 和 Inspector 两张图片。
5. 将 Screenshot A 放入 Slide 2，将 Screenshot B 放入 Slide 4。
6. 在 Slide 6 填入正式结果，并核对 `48%`、`63%`、`+15 pp`、`p=.0059`。
7. 全屏播放 PPT，逐页检查截图是否模糊、文字是否裁切、页码是否一致。
8. 进行一次完整彩排；若超过 9:30，先删减口头解释，不要加快到难以听清。

## 7. 停止修改标准

满足以下条件后停止继续设计 PPT：

- 7 页均能在 1920×1080 全屏下清晰阅读。
- 两张 Viewer 截图来自非零、有意义的回放帧。
- 研究问题明确关注直接提示 LLM 在该类游戏中的能力与限制。
- DTAV 被准确表述为本项目的方法。
- 正式实验数字与 `reports/` 中的 JSON 一致。
- 完整彩排不超过 9:30。
- Reviewer 能从 PPT 和现场演示中看到 proposal、checks、executed action 和 replay result 的连接。

达到这些条件后，不再增加页面、动画、模型或实验，直接进入正式录制。
