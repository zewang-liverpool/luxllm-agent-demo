# LuxLLM-Agent 论文人工查验与导师汇报清单

## 1. 使用说明

本清单用于 2026 年 7 月论文正式排版前的人工查验。

项目本地根目录：

```text
D:\PythonProject\lux_llm_agent
```

当前论文收口分支：

```text
codex/dissertation-final-closeout
```

人工查验标准：

- 必查项必须标记为 `PASS`，或者填写明确的问题与处理决定；
- 不要仅检查语言是否通顺，还要检查数字、结论、图表和研究问题是否一致；
- 暂时不要根据猜测大幅压缩论文，先向导师确认正式字数和格式要求；
- 查验结束后，将第 10 节的结果摘要发给导师；
- 如果发现问题，记录具体文件、章节和原文，不要只写“需要修改”。

建议记录格式：

```text
状态：PASS / FAIL / N/A
问题：
位置：
建议：
复查日期：
```

---

## 2. 查验前准备

| ID | 检查内容 | 操作或本地地址 | 通过标准 | 状态 |
| --- | --- | --- | --- | --- |
| P1 | 确认项目目录 | `D:\PythonProject\lux_llm_agent` | 目录能够正常打开 | ☐ |
| P2 | 确认当前分支 | 在项目目录执行 `git status -sb` | 显示 `codex/dissertation-final-closeout` | ☐ |
| P3 | 确认完整论文 | `D:\PythonProject\lux_llm_agent\docs\dissertation\full_dissertation_draft.md` | 文件能够打开，包含摘要、Chapter 1–7 和 References | ☐ |
| P4 | 确认分章节文件 | `D:\PythonProject\lux_llm_agent\docs\dissertation` | Chapter 1–7 文件均存在 | ☐ |
| P5 | 准备记录方式 | 本文件副本或单独的检查记录 | 每个 FAIL 都能记录具体位置 | ☐ |

---

## 3. 首页、摘要与基本信息

主要文件：

```text
D:\PythonProject\lux_llm_agent\docs\dissertation\front_matter.md
```

| ID | 检查内容 | 通过标准 | 状态 |
| --- | --- | --- | --- |
| F1 | 论文标题 | 与研究问题和 GitHub 项目名称一致 | ☐ |
| F2 | 作者姓名 | 显示 `Ze Wang`，拼写和大小写正确 | ☐ |
| F3 | 学校 | 显示 `University of Liverpool` | ☐ |
| F4 | 邮箱 | 显示 `Z.Wang300@liverpool.ac.uk` | ☐ |
| F5 | 导师姓名 | 显示 `Meng Fang` | ☐ |
| F6 | 项目模块 | 显示 `COMP702 MSc Project` | ☐ |
| F7 | 学号 | 显示 `201868809`，与项目反馈记录一致 | ☐ |
| F8 | 完整专业/学位名称 | 尚需按正式课程记录确认 | ☐ |
| F9 | 提交日期 | 正式版本必须使用学校要求的日期格式 | ☐ |
| F10 | 摘要研究方向 | 核心是 decision tracing 和 rule-based verification，而不是模型排名 | ☐ |
| F11 | 摘要主要实验 | 正确描述每个模型 100 场、合计 200 场主要实验 | ☐ |
| F12 | 摘要补充实验 | 正确描述 100 场直接双 LLM 对战为补充证据 | ☐ |
| F13 | 摘要不过度宣传 | 没有声称绝对安全、普遍优于其他模型或达到排行榜水平 | ☐ |
| F14 | Keywords | 与 LLM agents、decision tracing、verification、reproducibility 和 Lux AI S3 有关 | ☐ |

人工阅读要求：

1. 连续朗读摘要一次，检查是否能在两分钟内理解项目问题、方法、证据和结论。
2. 检查摘要中的每一个数字是否能在 Chapter 6 找到。
3. 标记任何过长、重复或一次包含过多数字的句子。

---

## 4. 研究问题与论文主线

需要对照的文件：

```text
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_1_introduction.md
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_3_requirements_methodology.md
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_6_evaluation.md
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_7_discussion_conclusion.md
```

主研究问题：

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

| ID | 检查内容 | 通过标准 | 状态 |
| --- | --- | --- | --- |
| R1 | 研究问题文本 | Chapters 1、3、6、7 的含义一致 | ☐ |
| R2 | Chapter 1 | 清楚解释为什么只看胜率不足以评估 LLM agent | ☐ |
| R3 | Chapter 3 | 每个实验指标都对应研究问题或子问题 | ☐ |
| R4 | Chapter 6 | 结果重点是可检查性、验证器介入和执行证据 | ☐ |
| R5 | Chapter 7 | 逐项回答研究问题，不只是重复实验数字 | ☐ |
| R6 | 双 LLM 实验定位 | 明确属于补充 operational evidence | ☐ |
| R7 | 模型比较边界 | 没有把项目改写成 Qwen 与 DeepSeek 的排行榜研究 | ☐ |
| R8 | 主要贡献 | 框架、追踪、验证、回退、缓存和回放检查构成连贯贡献 | ☐ |

人工提问：

- 如果评审问“这个项目的原创贡献是什么”，Chapter 1 和 Chapter 7 是否能支持同一个简短答案？
- 如果评审删除所有胜率数字，论文是否仍有清楚的技术贡献和实验结论？
- 双 LLM 对战是否加强了原研究问题，而没有取代原研究问题？

---

## 5. 章节逐项阅读

### 5.1 Chapter 1：Introduction

文件：

```text
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_1_introduction.md
```

| 检查内容 | 通过标准 | 状态 |
| --- | --- | --- |
| 背景和动机 | 说明 Lux AI S3 的复杂性和直接使用 LLM 的风险 | ☐ |
| 目标与贡献 | 目标、研究问题、贡献之间没有冲突 | ☐ |
| 项目范围 | 明确不是 leaderboard-level agent | ☐ |
| 主要与补充实验 | 200 场主要实验和 100 场补充实验区分清楚 | ☐ |
| 章节结构 | 与最终 Chapter 1–7 顺序一致 | ☐ |

### 5.2 Chapter 2：Background and Related Work

文件：

```text
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_2_background_related_work.md
```

| 检查内容 | 通过标准 | 状态 |
| --- | --- | --- |
| 文献相关性 | 每组文献都与 LLM agents、game AI、verification 或 traceability 有直接关系 | ☐ |
| 不是文献列表 | 每段都包含比较、联系或研究空缺 | ☐ |
| 项目定位 | 清楚说明 LuxLLM-Agent 与 ReAct、Toolformer、Voyager 等工作的区别 | ☐ |
| 引用一致性 | 每个作者年份引用都出现在 References | ☐ |
| 避免无来源事实 | 重要技术或学术判断有引用或被明确写成项目设计选择 | ☐ |

### 5.3 Chapter 3：Requirements and Methodology

文件：

```text
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_3_requirements_methodology.md
```

| 检查内容 | 通过标准 | 状态 |
| --- | --- | --- |
| 功能需求 | 与最终代码功能一致 | ☐ |
| 非功能需求 | 可复现性、稳定性和可检查性都有验证方式 | ☐ |
| 主要实验设计 | 50 seeds × 2 roles × 2 backends = 200 matches 表述正确 | ☐ |
| 双 LLM 设计 | 50 seeds × 2 role assignments = 100 matches 表述正确 | ☐ |
| 公平性控制 | seed matching、role swapping、temperature 和模型配置交代清楚 | ☐ |
| 统计方法 | Wilson CI、paired/bootstrap、McNemar 或 sign test 的使用场景正确 | ☐ |
| 证据管理 | 说明摘要报告进 GitHub、大型原始证据本地保存 | ☐ |

### 5.4 Chapter 4：System Design

文件：

```text
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_4_system_design.md
```

| 检查内容 | 通过标准 | 状态 |
| --- | --- | --- |
| Figure 4.1 | 架构图顺序与代码实现一致 | ☐ |
| LLM 边界 | LLM 只提出 bounded strategic proposal | ☐ |
| 确定性组件 | parser、normalizer、verifier、planner 和 fallback 职责清楚 | ☐ |
| Trace pipeline | 能说明决策如何进入日志和 Viewer | ☐ |
| 设计理由 | 不只是列模块，还解释为什么这样设计 | ☐ |

### 5.5 Chapter 5：Implementation

文件：

```text
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_5_implementation.md
```

| 检查内容 | 通过标准 | 状态 |
| --- | --- | --- |
| Figure 5.1 | 实现流程与当前代码一致 | ☐ |
| 文件路径 | 文中列出的关键文件在本地存在 | ☐ |
| LLM 输出处理 | schema check、normalization、fallback 描述准确 | ☐ |
| 双玩家隔离 | 双 LLM 日志和模型路由的实现说明准确 | ☐ |
| 代码细节 | 足以说明实现，但没有大段无解释地复制源代码 | ☐ |

### 5.6 Chapter 6：Evaluation

文件：

```text
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_6_evaluation.md
```

| 检查内容 | 通过标准 | 状态 |
| --- | --- | --- |
| 主要实验完成数 | 200/200 | ☐ |
| Qwen 结果 | 63 wins / 100 matches | ☐ |
| DeepSeek 结果 | 60 wins / 100 matches | ☐ |
| 主要 trace 数 | 206,591 | ☐ |
| 主要 LLM calls | 4,591/4,591 post-check valid | ☐ |
| Qwen normalization | 520 | ☐ |
| Risk-filter steps | Qwen 5,590；DeepSeek 7,090 | ☐ |
| 双 LLM 完成数 | 100/100 | ☐ |
| 双 LLM 胜负 | Qwen 54；DeepSeek 46；draw 0 | ☐ |
| 双 LLM trace 数 | 106,317 | ☐ |
| 双 LLM calls | 4,676/4,676 valid | ☐ |
| 双 LLM normalization | 571 | ☐ |
| 双 LLM risk-filter steps | 15,721 | ☐ |
| 统计解释 | 非显著结果没有被解释成模型优劣证明 | ☐ |
| 历史数据 | 早期固定角色 50-run 明确标记为 historical evidence | ☐ |
| 限制 | 讨论 hybrid attribution、模型数量、环境范围和 latency | ☐ |

数字对照报告：

```text
D:\PythonProject\lux_llm_agent\reports\final_trace_evaluation.md
D:\PythonProject\lux_llm_agent\reports\final_trace_evaluation.json
D:\PythonProject\lux_llm_agent\reports\verifier_intervention_audit.md
D:\PythonProject\lux_llm_agent\reports\dual_llm_trace_evaluation.md
D:\PythonProject\lux_llm_agent\reports\dual_llm_verifier_audit.md
```

### 5.7 Chapter 7：Discussion and Conclusion

文件：

```text
D:\PythonProject\lux_llm_agent\docs\dissertation\chapter_7_discussion_conclusion.md
```

| 检查内容 | 通过标准 | 状态 |
| --- | --- | --- |
| 回答研究问题 | 结论直接回答 tracing 和 verification 如何提供支持 | ☐ |
| 结论边界 | 不宣称普遍安全、最佳模型或因果性能优势 | ☐ |
| 技术贡献 | 能与 Chapter 1 的贡献逐项对应 | ☐ |
| 限制 | 具体、诚实且与实验有关 | ☐ |
| Future work | 是合理延伸，不把未完成事项包装成已完成贡献 | ☐ |
| 最终结论 | 能在一段中概括项目价值 | ☐ |

---

## 6. 图表与 Viewer 人工检查

### 6.1 论文图表

| ID | 文件或位置 | 检查内容 | 状态 |
| --- | --- | --- | --- |
| V1 | Chapter 4 Figure 4.1 | 架构图能正常渲染，文字清晰 | ☐ |
| V2 | Chapter 5 Figure 5.1 | 决策流程图能正常渲染，箭头顺序正确 | ☐ |
| V3 | `D:\PythonProject\lux_llm_agent\reports\figures\framework_evidence_rates.png` | Figure 6.1 可读，坐标和图例正确 | ☐ |
| V4 | `D:\PythonProject\lux_llm_agent\reports\figures\decision_source_distribution.png` | Figure 6.2 可读，模型和来源分类正确 | ☐ |
| V5 | `D:\PythonProject\lux_llm_agent\paper\figures\figure_s3_replay_viewer.png` | Figure 6.3 清楚显示 Season 3 Viewer | ☐ |
| V6 | Chapter 6 | 三张图片均有编号、caption，并在正文中被解释 | ☐ |
| V7 | 全文表格 | 表格没有超出页面，数字小数位一致 | ☐ |

### 6.2 Viewer

启动命令：

```powershell
cd D:\PythonProject\lux_llm_agent
python -m http.server 8000
```

浏览器地址：

```text
http://localhost:8000/docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html
```

| ID | 检查内容 | 通过标准 | 状态 |
| --- | --- | --- | --- |
| UI1 | Season 标识 | 页面明显显示 `Lux AI Season 3` | ☐ |
| UI2 | 三阶段结构 | `LLM Proposal`、`Rule Verification`、`Executed State` 清楚分开 | ☐ |
| UI3 | 回放操作 | 播放、暂停、时间轴和步数切换正常 | ☐ |
| UI4 | Trace 数据 | objective、intent、source、fallback 和 verifier 信息可见 | ☐ |
| UI5 | 布局 | Overlay 不遮挡主要比赛状态 | ☐ |
| UI6 | 字号与颜色 | 投影或屏幕共享时仍然清楚 | ☐ |
| UI7 | 数据加载 | 浏览器控制台和页面中没有明显加载错误 | ☐ |

---

## 7. 引用、语言与格式检查

参考文献文件：

```text
D:\PythonProject\lux_llm_agent\docs\dissertation\references.md
```

| ID | 检查内容 | 通过标准 | 状态 |
| --- | --- | --- | --- |
| L1 | 文内引用 | 每个作者年份引用都出现在参考文献 | ☐ |
| L2 | 未被引用的文献 | 没有大量与正文无关的参考文献 | ☐ |
| L3 | 引用格式 | 格式统一，最终按学校要求调整 | ☐ |
| L4 | 专有名词 | `Lux AI Season 3`、`LuxLLM-Agent`、`Qwen3`、`DeepSeek-R1` 拼写统一 | ☐ |
| L5 | 英式英语 | 尽量统一使用 analyse、behaviour、normalisation 等英式拼写 | ☐ |
| L6 | 时态 | 方法和实现描述时态一致；已完成实验使用过去时或现在完成语境合理 | ☐ |
| L7 | 第一人称 | `I`、`we` 或无主语写法符合学校要求且全文一致 | ☐ |
| L8 | 编码 | 没有乱码、异常引号或损坏字符 | ☐ |
| L9 | 重复 | 相同实验数字没有在多个章节被无意义重复 | ☐ |
| L10 | 缩写 | LLM、CI、JSONL 等首次出现时有解释 | ☐ |

---

## 8. 演示与答辩人工检查

演示 Runbook：

```text
D:\PythonProject\lux_llm_agent\docs\final_demo_runbook.md
```

备份视频：

```text
D:\PythonProject\lux_llm_agent\docs\demo_videos\LuxLLM_Agent_Final_Demo_Run008_Isometric_Visualization.mp4
```

| ID | 检查内容 | 通过标准 | 状态 |
| --- | --- | --- | --- |
| D1 | 视频播放 | 有画面和声音，能够完整播放 | ☐ |
| D2 | Season 说明 | 讲解时明确这是 Lux AI Season 3 | ☐ |
| D3 | 主线 | 先讲研究问题和框架，再讲胜率 | ☐ |
| D4 | UI 展示 | 明确指出 Proposal、Verification、Executed State | ☐ |
| D5 | 主要实验 | 能准确说出 200 matches、206,591 traces、4,591 calls | ☐ |
| D6 | 双 LLM 实验 | 能解释 100 matches 和为什么它只是补充证据 | ☐ |
| D7 | 统计解释 | 能说明 non-significant 不等于“两个模型完全相同” | ☐ |
| D8 | 运行风险 | 演示时不现场启动 32B 模型推理 | ☐ |
| D9 | 时间 | 完整演示控制在 7–10 分钟 | ☐ |
| D10 | 备用方案 | Viewer 失败时能立即切换到视频和报告 | ☐ |

建议至少口头练习以下问题：

1. What is the main contribution of this project?
2. Why not let the LLM directly execute actions?
3. How do you know the verifier actually intervened?
4. Does zero recorded failure prove the framework is safe?
5. Why is win rate not sufficient?
6. Is Qwen better than DeepSeek?
7. Why did you add LLM-versus-LLM matches?
8. Does the LLM-versus-LLM experiment change the research question?
9. How reproducible are the experiments?
10. What would you improve with more time?

---

## 9. 提交前仍需向导师确认的事项

以下事项没有可靠依据时不得自行猜测：

| ID | 需要确认的问题 | 导师/课程答复 | 状态 |
| --- | --- | --- | --- |
| S1 | COMP702 dissertation 是否有正式 Word/PDF 模板？ |  | ☐ |
| S2 | 正文字数上限或建议范围是多少？ |  | ☐ |
| S3 | Abstract、References、Appendices 是否计入字数？ |  | ☐ |
| S4 | 是否必须包含 declaration、acknowledgements、list of figures 和 list of tables？ |  | ☐ |
| S5 | 使用哪种引用格式，例如 Harvard、IEEE 或学校指定格式？ |  | ☐ |
| S6 | 页面大小、页边距、字体、字号和行距要求是什么？ |  | ☐ |
| S7 | 是否要求匿名提交，封面能否出现姓名和导师姓名？ |  | ☐ |
| S8 | 最终文件命名规则是什么？ |  | ☐ |
| S9 | 是否只提交 PDF，还是同时提交源码、代码仓库或附件？ |  | ☐ |
| S10 | 大型实验原始数据是否需要提交，还是保留报告、哈希和获取说明即可？ |  | ☐ |
| S11 | 演示视频的分辨率、时长、文件大小和上传平台是否有硬性要求？ |  | ☐ |
| S12 | 当前项目完成度和实验范围是否足够进入最终论文排版阶段？ |  | ☐ |

---

## 10. 查验完成后的结果摘要

完成检查后填写：

```text
Review date:
Reviewer:
Branch:
Repository commit:

Dissertation content checks:
PASS:
FAIL:
N/A:

Evidence-number checks:
PASS:
FAIL:

Figure/viewer checks:
PASS:
FAIL:

Demo checks:
PASS:
FAIL:

Outstanding content issues:

Questions requiring supervisor confirmation:

Overall decision:
READY FOR SUPERVISOR REVIEW / REQUIRES REVISION
```

---

## 11. 给导师的简短汇报与格式询问

### 11.1 推荐英文版本

> Hi Dr Fang, I have now completed the main implementation and the current round of dissertation integration. The primary evaluation contains 200 matched-seed, role-swapped matches, and I have also completed the supplementary 100-match direct LLM-versus-LLM experiment you suggested. I am now manually reviewing the full dissertation draft, checking the reported quantities, figures, references, viewer, and demonstration materials.
>
> Could I please ask whether there is an official COMP702 dissertation template or any specific requirements for the word limit, title page, declaration, citation style, font, spacing, margins, appendices, and final file naming? I would also be grateful for your feedback on whether the current project scope and empirical evidence are sufficient for me to proceed to final formatting and proofreading.

### 11.2 更简短的 Discord 版本

> Hi Dr Fang, I have completed the current dissertation draft integration and I am now carrying out a full manual check of the content, experimental quantities, figures, references, viewer, and demo. Could I please ask whether COMP702 has an official dissertation template or specific requirements for the word limit, title page, citation style, formatting, appendices, and file naming? I would also appreciate your feedback on whether the current project scope and empirical evidence are sufficient for final formatting and proofreading.

### 11.3 中文对照

> Fang 老师您好，我已经完成了当前版本的论文内容整合，目前正在对论文内容、实验数字、图表、引用、Viewer 和演示材料进行完整的人工检查。请问 COMP702 是否有正式的论文模板，或者对字数、封面、声明、引用格式、字体、行距、页边距、附录和文件命名有具体要求？另外，也想请您评价一下目前项目的范围和实验证据是否已经足够进入最终排版和校对阶段。谢谢老师。

---

## 12. 人工查验停止条件

满足以下条件后，本轮人工查验即可停止：

1. 所有必查项为 `PASS`，或者已有明确的修正记录；
2. Chapter 1、3、6、7 对研究问题和实验设计的描述一致；
3. 所有关键实验数字与机器可读报告一致；
4. 三张 Chapter 6 图片和两个 Mermaid 图在最终格式中清晰可读；
5. Viewer 和备份视频能够正常使用；
6. 导师已经回复论文格式与字数要求；
7. 未发现影响结论的事实错误；
8. 不再新增实验或功能，除非导师指出具体证据缺口。

达到以上标准后，下一阶段只进行：

- 学校格式转换；
- Word/PDF 排版；
- 引用格式统一；
- 最终语言校对；
- 提交前备份和验收。
