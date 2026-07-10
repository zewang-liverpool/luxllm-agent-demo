# qwen3:32b vs DeepSeek-R1-32B Analysis

## 1. Overview

This document analyses the controlled 50-run evaluation results for two LLM backends used in LuxLLM-Agent:

* qwen3:32b;

* deepseek-r1:32b.

The purpose of this comparison is not to create a general-purpose LLM leaderboard. Instead, the comparison is used to evaluate whether the LuxLLM-Agent decision-trace and rule-based action-verification framework can support different reasoning-oriented LLM backends under the same Lux AI Season 3 setting.

This analysis supports the main research question:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

The comparison is also relevant to the dissertation evaluation chapter because it shows how different LLMs behave when placed inside the same structured decision pipeline.

---

## 2. Evaluation Context

LuxLLM-Agent separates LLM strategic planning from executable game actions.

The LLM produces high-level strategic proposals, while deterministic components handle:

* structured parsing;

* rule-based action verification;

* fallback behaviour;

* strategy caching;

* risk-aware action filtering;

* action planning;

* decision trace logging.

This means that the evaluation does not only measure raw model ability. It measures the behaviour of each model when used as part of the same controlled agent framework.

The comparison therefore focuses on:

* gameplay outcome;

* execution stability;

* LLM error rate;

* decision-source behaviour;

* fallback behaviour;

* latency and runtime cost;

* framework-level robustness.

---

## 3. Compared Models

| Model           | Role in project        |
| --------------- | ---------------------- |
| qwen3:32b       | Main LLM backend       |
| deepseek-r1:32b | Comparison LLM backend |

qwen3:32b is used as the main LLM backend in the project. DeepSeek-R1-32B is added as a comparison model to test whether the same framework can support another reasoning-oriented LLM.

This comparison helps avoid the weakness of evaluating the project using only one LLM backend.

---

## 4. 50-run Result Summary

| Model           | Runs | player_0 wins | player_1 wins | player_0 win rate | LLM errors |
| --------------- | ---: | ------------: | ------------: | ----------------: | ---------: |
| qwen3:32b       |   50 |            35 |            15 |               70% |          0 |
| deepseek-r1:32b |   50 |            26 |            24 |               52% |          0 |

Both models completed 50 controlled Lux AI Season 3 runs with zero LLM errors.

This is important because it suggests that the decision pipeline, parser, fallback logic, and action-verification framework can support multiple LLM backends without model-level execution failures.

---

## 5. Gameplay Outcome Analysis

qwen3:32b achieved a stronger gameplay outcome in the existing 50-run evidence:

```text

qwen3:32b:

player_0 wins = 35

player_1 wins = 15

player_0 win rate = 70%

```

DeepSeek-R1-32B produced a more balanced result:

```text

deepseek-r1:32b:

player_0 wins = 26

player_1 wins = 24

player_0 win rate = 52%

```

This indicates that qwen3:32b performed better in this specific LuxLLM-Agent evaluation setup. However, the result should not be interpreted as a general claim that qwen3:32b is always better than DeepSeek-R1-32B. The comparison is limited to:

* the current Lux AI Season 3 environment;

* the current LuxLLM-Agent decision pipeline;

* the current rule-based verifier and fallback system;

* the current prompting and strategy format;

* the current controlled-run configuration.

A stronger and more defensible interpretation is that different LLM backends lead to different gameplay outcomes while the framework remains stable.

---

## 6. DeepSeek-R1-32B Detailed Metrics

The DeepSeek-R1-32B 50-run experiment produced the following additional metrics:

| Metric                    |        Value |
| ------------------------- | -----------: |
| Total runs                |           50 |
| player_0 wins             |           26 |
| player_1 wins             |           24 |
| Average player_0 reward   |          2.7 |
| Average player_1 reward   |          2.3 |
| Average fresh LLM calls   |         33.2 |
| Average LLM strategy used |        27.24 |
| Average cached LLM turns  |       412.62 |
| Average fallback count    |       570.14 |
| Average LLM errors        |          0.0 |
| Average LLM latency       |  4143.595 ms |
| Maximum LLM latency       | 10581.076 ms |
| Average trace steps       |       1010.0 |

The zero LLM error rate is particularly important. It suggests that DeepSeek-R1-32B can be integrated into the LuxLLM-Agent framework without causing parsing or runtime instability in this 50-run setting.

The average latency of approximately 4.14 seconds also shows why strategy caching is necessary. Calling a large LLM at every step would be impractical, so the system relies on cached LLM plans and rule-based verification between fresh LLM calls.

---

## 7. Decision Source Analysis

The DeepSeek-R1-32B 50-run experiment produced the following decision-source distribution:

| Decision source | Count |
| --------------- | ----: |
| `rule_player`   | 25250 |
| `fallback`      |    94 |
| `rule_fallback` |  3163 |
| `llm_fresh`     |  1362 |
| `cached_llm`    | 20631 |

Derived values:

```text

Total decision-source events = 50500

LLM-related decision events:

llm_fresh + cached_llm = 1362 + 20631 = 21993

Fallback-related decision events:

fallback + rule_fallback = 94 + 3163 = 3257

```

Approximate rates:

```text

LLM decision-source rate = 21993 / 50500 = approximately 43.55%

Fallback decision-source rate = 3257 / 50500 = approximately 6.45%

```

This shows that the DeepSeek-backed agent behaviour is not purely LLM-driven or purely rule-driven. Instead, it is produced by a hybrid pipeline involving:

* fresh LLM decisions;

* cached LLM decisions;

* rule-player behaviour;

* fallback behaviour;

* rule fallback.

This is useful for the dissertation because it demonstrates decision provenance. The system can explain where behaviour came from, instead of only reporting final scores.

---

## 8. LLM Error Analysis

Both qwen3:32b and deepseek-r1:32b completed their 50-run experiments with zero LLM errors.

| Model           | Runs | LLM errors |
| --------------- | ---: | ---------: |
| qwen3:32b       |   50 |          0 |
| deepseek-r1:32b |   50 |          0 |

This supports the claim that the system can integrate different LLM backends in a stable way.

However, zero LLM errors does not mean that all decisions were strategically optimal. It only means that the LLM interaction, parsing, and execution process did not produce recorded LLM failures in these experiments.

The dissertation should distinguish between:

* execution stability;

* strategic quality;

* gameplay outcome.

The framework appears stable, but model choice still affects strategic behaviour and win rate.

---

## 9. Latency Analysis

DeepSeek-R1-32B had an average LLM latency of:

```text

4143.595 ms

```

and a maximum LLM latency of:

```text

10581.076 ms

```

This confirms that large-model inference can be expensive during sequential decision-making tasks.

The latency result supports the design of:

* strategy caching;

* controlled LLM call intervals;

* fallback behaviour;

* rule-based action planning between LLM calls.

Without these mechanisms, the agent would need to call the LLM too frequently, making the system slower and less practical.

The latency results therefore support the technical design rather than only reporting runtime cost.

---

## 10. Framework-level Interpretation

The key interpretation is:

> LuxLLM-Agent can run different reasoning-oriented LLM backends through the same structured decision-trace and rule-based action-verification framework.

This is stronger than simply claiming that one model wins more matches.

The evidence shows that:

* qwen3:32b completed 50 controlled runs with zero LLM errors;

* deepseek-r1:32b completed 50 controlled runs with zero LLM errors;

* both models can use the same decision pipeline;

* both models can be evaluated using the same logging and evidence structure;

* gameplay outcomes differ across models;

* decision-source analysis can explain how behaviour is produced.

This supports the project’s central claim that LuxLLM-Agent is a framework for inspection and evaluation, not only a single-model game agent.

---

## 11. Dissertation Interpretation

For the COMP702 dissertation, the comparison should be framed carefully.

A weak interpretation would be:

```text

qwen3:32b is better than deepseek-r1:32b.

```

A stronger interpretation is:

```text

The same decision-trace and action-verification framework can support multiple reasoning-oriented LLM backends. The two models produced different gameplay outcomes, but both completed 50 controlled runs with zero LLM errors. This suggests that the framework separates model-level strategic behaviour from system-level execution stability.

```

This interpretation is better because it connects the results to the research question and system design.

---

## 12. Limitations

The comparison has several limitations.

First, the evaluation is specific to Lux AI Season 3 and the current LuxLLM-Agent implementation. It should not be treated as a general benchmark of qwen3:32b or DeepSeek-R1-32B.

Second, the two models may respond differently to prompt design. A model-specific prompt could improve one model more than another, but this project uses the same framework to keep the comparison controlled.

Third, win rate is influenced by the rule-based verifier, fallback logic, cache behaviour, and action planner. Therefore, the final result is not purely caused by the LLM.

Fourth, fallback counts require careful interpretation. Some fallback metrics may be unit-level or action-level, while decision-source fallback counts may represent higher-level decision provenance.

Fifth, the current comparison focuses mainly on aggregate 50-run results. A stronger future evaluation could include per-case qualitative analysis, such as identifying steps where a model produced a weak strategy or where fallback prevented an invalid action.

These limitations should be included in the dissertation to demonstrate critical reflection.

---

## 13. Implications for Future Work

The comparison suggests several possible future directions:

* test additional LLM backends;

* tune prompts per model;

* compare reasoning/action consistency;

* analyse failed matches in more detail;

* add viewer support for comparing traces from two different models;

* visualise fallback-heavy frames in the replay timeline;

* evaluate whether risk-aware filtering improves final outcomes.

However, for the current COMP702 project, qwen3:32b and DeepSeek-R1-32B already provide enough model comparison evidence. The priority should now be system documentation, failure-case analysis, and dissertation writing rather than adding more models.

---

## 14. Summary

The qwen3:32b and DeepSeek-R1-32B comparison strengthens LuxLLM-Agent as a dissertation project.

qwen3:32b achieved a higher win rate in the current 50-run evidence, while DeepSeek-R1-32B produced a closer 26-24 result. Both models completed 50 controlled runs with zero LLM errors.

The key conclusion is not that one model is universally better. Instead, the evidence shows that the LuxLLM-Agent framework can support different LLM backends while preserving stable execution, structured decision tracing, fallback handling, and replay-grounded evaluation.

