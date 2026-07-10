# Evaluation Metrics

## 1. Overview

LuxLLM-Agent is evaluated as a decision-trace and action-verification framework for LLM-based agents in Lux AI Season 3.

The evaluation is not based only on whether the agent wins or loses. Final match outcome is useful, but it does not explain how the agent made decisions, when the LLM was used, when fallback was needed, or whether the framework remained stable.

Therefore, the project uses multiple categories of evaluation metrics:

* gameplay outcome metrics;

* LLM execution metrics;

* decision provenance metrics;

* fallback and verification metrics;

* latency and runtime metrics;

* replay-grounded inspection metrics;

* qualitative failure-analysis metrics.

This supports the main research question:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

---

## 2. Evaluation Goals

The evaluation has four main goals.

### 2.1 Measure gameplay outcome

The system should report basic match results, including wins, losses, rewards, and win rate.

### 2.2 Measure LLM execution stability

The system should show whether the LLM backend can complete controlled runs without parser errors, timeouts, or runtime failures.

### 2.3 Measure decision provenance

The system should show where actions come from: fresh LLM decisions, cached LLM plans, fallback, rule fallback, or rule-based player logic.

### 2.4 Support replay-grounded inspection

The system should connect aggregate metrics to replay frames and decision traces so that behaviour can be inspected qualitatively.

These goals make the evaluation suitable for a dissertation project rather than a simple leaderboard.

---

## 3. Gameplay Outcome Metrics

Gameplay outcome metrics describe the final results of controlled matches.

Important metrics include:

| Metric                  | Description                              |
| ----------------------- | ---------------------------------------- |
| Total runs              | Number of controlled matches             |
| player_0 wins           | Number of matches won by player_0        |
| player_1 wins           | Number of matches won by player_1        |
| Draws                   | Number of matches without a clear winner |
| player_0 win rate       | player_0 wins divided by total runs      |
| Average player_0 reward | Mean reward for player_0                 |
| Average player_1 reward | Mean reward for player_1                 |
| Total player_0 reward   | Sum of player_0 rewards                  |
| Total player_1 reward   | Sum of player_1 rewards                  |

Current 50-run comparison:

| Model           | Runs | player_0 wins | player_1 wins | player_0 win rate | LLM errors |
| --------------- | ---: | ------------: | ------------: | ----------------: | ---------: |
| qwen3:32b       |   50 |            35 |            15 |               70% |          0 |
| deepseek-r1:32b |   50 |            26 |            24 |               52% |          0 |

These results are useful, but they are not sufficient by themselves. They must be interpreted together with decision-source, fallback, latency, and trace metrics.

---

## 4. LLM Execution Metrics

LLM execution metrics describe how the LLM backend behaves during evaluation.

Important metrics include:

| Metric              | Description                                       |
| ------------------- | ------------------------------------------------- |
| Fresh LLM calls     | Number of new LLM calls made during a match       |
| LLM strategy used   | Number of times a usable LLM strategy was applied |
| Cached LLM turns    | Number of turns using a previous LLM plan         |
| LLM errors          | Number of LLM or parser failures                  |
| Timed out           | Whether LLM generation exceeded the time limit    |
| Average LLM latency | Mean LLM response time                            |
| Maximum LLM latency | Highest observed LLM response time                |

DeepSeek-R1-32B 50-run values:

| Metric                    |        Value |
| ------------------------- | -----------: |
| Average fresh LLM calls   |         33.2 |
| Average LLM strategy used |        27.24 |
| Average cached LLM turns  |       412.62 |
| Average LLM errors        |          0.0 |
| Average LLM latency       |  4143.595 ms |
| Maximum LLM latency       | 10581.076 ms |

These metrics show that LLM calls are expensive and that strategy caching is necessary for practical execution.

---

## 5. Decision Provenance Metrics

Decision provenance metrics show where agent decisions come from.

Important decision sources include:

| Decision source | Meaning                                             |
| --------------- | --------------------------------------------------- |
| `llm_fresh`     | A fresh LLM decision was used                       |
| `cached_llm`    | A previous LLM plan was reused                      |
| `fallback`      | General fallback behaviour was used                 |
| `rule_fallback` | Rule-based fallback repaired or replaced a decision |
| `rule_player`   | Rule-based player logic produced the action         |
| `rule_only`     | Rule-only mode was active                           |

Decision provenance is central to the project because it allows the system to answer questions such as:

* How often did the LLM actually influence behaviour?

* How often was a cached plan reused?

* How often did rule-based fallback take over?

* Did the system remain stable when the LLM was not used?

* Did final outcomes depend mostly on LLM strategy or rule-based support?

---

## 6. DeepSeek-R1-32B Decision Source Distribution

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

This shows that the framework combines fresh LLM decisions, cached LLM plans, rule-player actions, and fallback actions within a traceable execution pipeline.

---

## 7. Fallback and Verification Metrics

Fallback and verification metrics describe how often the system intervenes between LLM strategy and action execution.

Important fields include:

| Metric               | Description                                         |
| -------------------- | --------------------------------------------------- |
| fallback_used        | Whether fallback was used at a step                 |
| fallback_reason      | Reason for fallback                                 |
| action_fallback_used | Whether action-level fallback occurred              |
| rule_fallback        | Whether rule fallback was the decision source       |
| llm_valid            | Whether the LLM output was valid                    |
| llm_error            | LLM or parsing error                                |
| timed_out            | Whether LLM generation timed out                    |
| risk_filter_changed  | Whether the risk filter changed the selected action |
| stale_decision       | Whether a cached decision may be stale              |

These metrics support the project's action-verification argument. The system does not simply trust the LLM output. It checks, replaces, or repairs decisions when necessary.

---

## 8. Risk-aware Filter Metrics

The risk-aware action filter records whether rule-based safety logic changed an action.

Important fields include:

```text

risk_filter_enabled

risk_filter_changed

risk_filter_reason

risk_filter_changed_targets

risk_filter_events_count

risk_filter_visible_enemy_units

risk_filter_evaluated_units

```

These fields help answer:

* Did the system detect risky actions?

* Did the risk filter intervene?

* How often did it change targets?

* Were enemy units visible when actions were changed?

* Did risk filtering affect the final action?

This provides evidence that the system has an action-verification layer beyond LLM strategic planning.

---

## 9. Replay-grounded Inspection Metrics

Replay-grounded inspection connects aggregate metrics to visual frames.

The LLM Decision Trace Overlay uses:

```text

data/run008_decision_trace_overlay.json

docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html

```

The current overlay generation result is:

| Metric                    | Value |
| ------------------------- | ----: |
| Replay frames             |   506 |
| Decision trace rows       |  1009 |
| LLM decision rows         |    23 |
| Matched step trace frames |   505 |
| Matched exact LLM frames  |    23 |
| Matched recent LLM frames |   506 |

These metrics show that the replay viewer can connect visual frames to decision-trace records.

This supports qualitative evaluation because a user can inspect a specific frame and see:

* current phase;

* decision source;

* LLM model;

* objective;

* fallback status;

* risk filter status;

* score context;

* unit intents.

---

## 10. Model Comparison Metrics

The project compares qwen3:32b and deepseek-r1:32b under the same framework.

The purpose is not to rank LLMs generally. Instead, the comparison evaluates whether the framework can support multiple reasoning-oriented LLM backends.

Important comparison dimensions include:

| Dimension                    | Purpose                             |
| ---------------------------- | ----------------------------------- |
| Win/loss                     | Compare gameplay outcome            |
| Rewards                      | Compare score-level performance     |
| LLM errors                   | Compare execution stability         |
| LLM latency                  | Compare runtime cost                |
| Fresh LLM calls              | Compare inference usage             |
| Cached LLM turns             | Compare cache reliance              |
| Fallback count               | Compare verifier/fallback behaviour |
| Decision-source distribution | Compare how behaviour is produced   |

A strong dissertation interpretation is:

> Both qwen3:32b and deepseek-r1:32b completed 50 controlled runs with zero LLM errors. This suggests that the LuxLLM-Agent framework can support different reasoning-oriented LLM backends while preserving stable execution through structured decision tracing, rule-based verification, fallback, and caching.

---

## 11. Qualitative Failure-analysis Metrics

Quantitative metrics are not enough for a high-quality dissertation. The project should also include failure-case analysis.

Each failure case should include:

| Field                | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| Match or run ID      | Which run the case came from                                |
| Step or frame        | When the case occurred                                      |
| Observed state       | What the agent could see                                    |
| LLM plan             | What the LLM proposed                                       |
| Decision source      | Fresh LLM, cached LLM, fallback, or rule                    |
| Verifier behaviour   | Whether the system accepted, repaired, or rejected the plan |
| Outcome              | What happened after the decision                            |
| Interpretation       | What the case reveals                                       |
| Possible improvement | How the system could be improved                            |

Example failure categories:

* LLM plan was reasonable but game outcome was poor.

* Cached plan became stale.

* Rule fallback replaced an unusable LLM decision.

* Risk filter avoided a dangerous move.

* Agent lost despite stable LLM execution.

This form of analysis demonstrates critical reflection, which is important for a 70+ COMP702 project.

---

## 12. Recommended Evaluation Structure for the Dissertation

The dissertation evaluation chapter should be organised as follows:

```text

1. Evaluation setup

2. Rule-only baseline

3. qwen3:32b 50-run result

4. deepseek-r1:32b 50-run result

5. LLM backend comparison

6. Decision-source analysis

7. LLM latency and error analysis

8. Replay-grounded inspection using the overlay

9. Failure-case analysis

10. Summary of findings

```

This structure avoids the weakness of only reporting final scores. It shows that the project evaluates the system from multiple angles.

---

## 13. Interpretation Guidelines

When writing the dissertation, the results should be interpreted carefully.

### 13.1 Do not overclaim model superiority

The project should not claim that one LLM is generally better than another. The experiments are specific to LuxLLM-Agent, Lux AI Season 3, and the current rule-verification pipeline.

### 13.2 Emphasise framework stability

A stronger claim is that the framework can support multiple LLM backends with zero LLM errors in controlled 50-run settings.

### 13.3 Explain fallback carefully

Fallback count may be measured at different levels, such as unit-level fallback or decision-source fallback. The dissertation should distinguish these where possible.

### 13.4 Connect metrics to design

The evaluation should explain how metrics relate to system design. For example, cached LLM turns support the strategy-cache design, while decision-source distribution supports decision traceability.

### 13.5 Include limitations

A high-mark dissertation should discuss limitations openly. For example, the system is not an optimal Lux AI agent, and the overlay depends on available trace logs.

---

## 14. Summary

The LuxLLM-Agent evaluation uses a multi-dimensional metric framework.

It includes gameplay outcomes, LLM execution stability, decision provenance, fallback behaviour, risk filtering, latency, replay-grounded inspection, and qualitative failure analysis.

This evaluation design supports the dissertation argument that LuxLLM-Agent is not merely an LLM game-playing agent. It is a framework for inspecting and evaluating LLM-based agents through structured decision tracing and rule-based action verification.

