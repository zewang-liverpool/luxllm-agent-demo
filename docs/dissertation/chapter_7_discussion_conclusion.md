# Chapter 7: Discussion and Conclusion

## 7.1 Introduction

This chapter discusses the main findings, contributions, limitations, and future work of LuxLLM-Agent.

The project set out to investigate the following research question:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

The previous chapters presented the system design, implementation, and evaluation of LuxLLM-Agent. The system was developed as a decision-trace and action-verification framework rather than only as a game-playing agent. It combines structured state summarisation, LLM-based strategic planning, rule-based action verification, fallback behaviour, strategy caching, decision trace logging, controlled-run evaluation, and replay-grounded visual inspection.

This chapter reflects on how well the project answered the research question, what the main findings were, what technical contributions were made, and what limitations remain.

---

## 7.2 Answering the Research Question

The main research question was:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

The project answers this question by showing that structured decision tracing and rule-based action verification can support LLM-based agents in three main ways.

First, structured decision tracing makes agent behaviour more inspectable. Instead of only recording final match scores, LuxLLM-Agent records decision source, LLM mode, model name, fallback status, cached-plan usage, risk-filter behaviour, LLM errors, latency, unit intents, and score context. This allows the system to explain whether a decision came from a fresh LLM call, a cached LLM plan, fallback behaviour, rule fallback, or rule-based policy.

Second, rule-based action verification provides a controlled boundary between LLM reasoning and executable game actions. The LLM does not directly control Lux AI Season 3 units. Instead, it proposes high-level strategic intents, which are then parsed, checked, filtered, cached, repaired, or replaced before being converted into legal actions. This improves stability and reduces the risk of invalid LLM output affecting the environment.

Third, replay-grounded inspection connects decision traces to visual game behaviour. The LLM Decision Trace Overlay allows replay frames to be inspected together with the corresponding decision source, objective, fallback status, risk posture, and unit intents. This makes evaluation more informative than using final score alone.

Overall, the project demonstrates that structured decision tracing and rule-based verification can make LLM-based game agents more stable, inspectable, and evaluable.

---

## 7.3 Discussion of Main Findings

### 7.3.1 LLM-based agents require more than prompt engineering

One important finding is that prompt engineering alone is not sufficient for building reliable LLM-based agents in a dynamic game environment.

Lux AI Season 3 requires repeated action decisions under uncertainty. LLMs may produce useful high-level strategies, but they may also produce incomplete, stale, invalid, or impractical decisions. Therefore, the system requires additional mechanisms such as parsing, verification, fallback, caching, and rule-based action planning.

This supports the project’s central design principle:

> The LLM output is treated as a strategic proposal, not as a directly executable game action.

This principle helped make the system more robust and easier to evaluate.

---

### 7.3.2 Final scores alone are not enough for evaluation

Another important finding is that final match outcomes are not enough to evaluate LLM-based agents.

A win or loss does not explain:

* whether the LLM was used;

* whether the decision came from a fresh LLM call or cached plan;

* whether fallback behaviour replaced the LLM;

* whether a rule-based verifier changed the action;

* whether a strategy was valid but weak;

* whether latency affected execution.

For this reason, LuxLLM-Agent records decision-source and trace metrics. These metrics provide a richer view of agent behaviour.

The evaluation showed that qwen3:32b and DeepSeek-R1-32B produced different gameplay outcomes, but both completed 50 controlled runs with zero LLM errors. This shows why gameplay outcome and execution stability should be analysed separately.

---

### 7.3.3 The framework can support multiple LLM backends

The project compared qwen3:32b and DeepSeek-R1-32B under the same LuxLLM-Agent framework.

The main 50-run results were:

| Model           | Runs | player_0 wins | player_1 wins | player_0 win rate | LLM errors |
| --------------- | ---: | ------------: | ------------: | ----------------: | ---------: |
| qwen3:32b       |   50 |            35 |            15 |               70% |          0 |
| deepseek-r1:32b |   50 |            26 |            24 |               52% |          0 |

The qwen3:32b-backed configuration achieved a stronger gameplay outcome in the current evaluation. However, the stronger dissertation-level finding is that both models completed controlled 50-run evaluations with zero LLM errors.

This suggests that the framework can support different reasoning-oriented LLM backends while maintaining stable execution through structured decision tracing, verification, fallback, and caching.

---

### 7.3.4 Strategy caching is necessary but introduces trade-offs

The evaluation showed that large LLM calls can be expensive. In the DeepSeek-R1-32B 50-run evidence, the average LLM latency was approximately 4143.595 ms and the maximum latency was 10581.076 ms.

This supports the use of strategy caching. Without caching, the system would need to call the LLM too frequently, making execution slow and impractical.

However, caching also introduces a trade-off. Cached decisions may become stale when the game state changes. This means that caching improves efficiency but may reduce adaptiveness.

This trade-off is important for future work. A better system could use event-triggered LLM refreshes to update strategy when important changes occur.

---

### 7.3.5 Replay-grounded inspection improves interpretability

The LLM Decision Trace Overlay showed that decision traces can be connected to replay frames.

The overlay generation produced:

| Metric                    | Value |
| ------------------------- | ----: |
| Replay frames             |   506 |
| Decision trace rows       |  1009 |
| LLM decision rows         |    23 |
| Matched step trace frames |   505 |
| Matched exact LLM frames  |    23 |
| Matched recent LLM frames |   506 |

This means that the viewer can align nearly all replay frames with decision trace information and associate frames with recent LLM plans.

This improves interpretability because the user can inspect what the agent was doing, which decision source was active, what the LLM objective was, whether fallback was used, and how the score context evolved.

The overlay therefore turns the viewer from a simple replay tool into a replay-grounded decision inspection interface.

---

## 7.4 Technical Contributions

The project makes several technical contributions.

### 7.4.1 Structured LLM decision pipeline

The project implements a structured LLM decision pipeline that transforms raw observations into structured state summaries, sends them to an LLM, parses the returned strategy, verifies it, and converts it into executable actions.

This contribution is important because it avoids direct execution of arbitrary LLM outputs.

---

### 7.4.2 Rule-based action verification

The system includes a rule-based verification layer that checks whether LLM-generated plans are valid and executable.

The verifier helps ensure that the final action respects the current game state and environment constraints.

---

### 7.4.3 Fallback and strategy caching

The system implements fallback and caching mechanisms to improve stability and reduce latency.

Fallback allows the agent to continue acting when the LLM is unavailable or unsuitable. Caching allows recent LLM strategies to be reused across multiple steps.

---

### 7.4.4 Decision provenance logging

The system records decision-source information such as `llm_fresh`, `cached_llm`, `fallback`, `rule_fallback`, and `rule_player`.

This allows the project to analyse how behaviour was produced rather than only measuring final outcomes.

---

### 7.4.5 Replay-grounded decision trace overlay

The project adds an LLM Decision Trace Overlay to the Season 3 viewer. This overlay displays step-aligned decision information during replay playback.

This is a practical contribution because it makes the system easier to inspect, demonstrate, and evaluate.

---

### 7.4.6 Controlled multi-model evaluation

The project evaluates both qwen3:32b and DeepSeek-R1-32B under the same framework. This strengthens the project by showing that the system is not tied to only one LLM backend.

---

## 7.5 Limitations

The project has several limitations.

### 7.5.1 The system is not a leaderboard-level Lux AI agent

LuxLLM-Agent is designed for inspection and evaluation, not maximum leaderboard performance. The system demonstrates how LLM decisions can be traced, verified, and inspected, but it does not claim to be an optimal Lux AI Season 3 agent.

This limitation is important because the project should be assessed as a research and engineering artefact, not only as a competition bot.

---

### 7.5.2 Fallback complicates attribution

Fallback improves stability, but it makes attribution harder.

If a match is won, the result may not be due only to the LLM. It may also depend on rule-based fallback, cached plans, action verification, and the action planner.

Therefore, final outcomes should be interpreted as the result of a hybrid LLM-rule system.

---

### 7.5.3 Cached plans may become stale

Strategy caching reduces LLM latency, but cached plans may become stale when the game state changes. For example, a cached objective may no longer be suitable if the opponent moves, a target becomes less valuable, or a unit’s energy changes.

This limitation suggests the need for better event-triggered plan refresh mechanisms.

---

### 7.5.4 Limited number of model backends

The project compares qwen3:32b and DeepSeek-R1-32B. This provides useful evidence, but the evaluation does not cover all possible LLMs.

A larger evaluation could include additional models and more runs.

---

### 7.5.5 Trace alignment requires careful labelling

The replay overlay depends on alignment between replay frames and decision logs. If replay data and trace logs are generated from different runs, the overlay must be clearly labelled as an inspection prototype rather than an exact reconstruction of one run.

Future versions should include shared run identifiers across replay frames and trace logs.

---

### 7.5.6 Failure-case analysis is representative rather than exhaustive

The failure-case analysis identifies important representative cases, but it is not an exhaustive automatic classification of all failure modes.

A stronger future version could automatically mine logs for fallback-heavy steps, stale-cache cases, and weak decision outcomes.

---

## 7.6 Threats to Validity

### 7.6.1 Internal validity

The system is a hybrid of LLM and rule-based components. This makes it difficult to isolate the effect of the LLM alone.

The evaluation addresses this by recording decision sources, fallback behaviour, and cached-plan usage, but full causal attribution remains difficult.

The reported controlled runs also keep the LLM-assisted configuration in the `player_0` role against a rule-controlled `player_1`. Without matched-seed role swapping, possible player-side and environment effects remain confounded with planner and model effects. The reported win rates are descriptive because no confidence intervals or hypothesis tests are provided.

---

### 7.6.2 External validity

The project focuses on Lux AI Season 3. The findings may not directly generalise to other games or agent environments.

However, the general framework idea of combining LLM strategic planning with rule-based verification and decision tracing may be transferable to other sequential decision-making tasks.

---

### 7.6.3 Construct validity

The evaluation uses metrics such as win rate, LLM errors, latency, fallback count, and decision-source distribution. These metrics are useful, but they do not fully capture strategic quality.

For example, a valid LLM plan may still be strategically weak. This is why the project also includes replay-grounded inspection and failure-case analysis.

---

### 7.6.4 Reliability

The project uses scripts, logs, JSON/JSONL evidence files, and version-controlled documentation to improve reproducibility.

However, some runs depend on local or HPC configurations, such as installed LLM backends and hardware availability. This should be acknowledged when reporting results.

---

## 7.7 Future Work

Several future improvements are possible.

### 7.7.1 Event-triggered LLM refresh

The current system uses strategy caching to reduce LLM calls. Future work could trigger new LLM decisions when important events occur, such as:

* a unit reaching a target;

* a score change;

* an enemy becoming visible;

* a relic candidate being confirmed or rejected;

* risk filter intervention increasing;

* a cached plan becoming too old.

This could reduce stale-plan behaviour.

---

### 7.7.2 Stronger utility scoring

Future versions could combine LLM strategy with rule-based utility scoring.

For example, target selection could consider:

* distance;

* expected reward;

* uncertainty;

* enemy risk;

* energy cost;

* opportunity cost.

This would make the system more strategically grounded.

---

### 7.7.3 Better verifier logging

The current system records decision-source and fallback information. Future work could log more detailed verifier information, such as:

* rejected LLM intents;

* rejected target locations;

* before-and-after risk-filter changes;

* alternative candidate actions;

* verifier confidence or reason codes.

This would make failure analysis more precise.

---

### 7.7.4 Multi-run viewer support

The current overlay focuses on Run008. Future work could support multiple replays and allow users to select a run from the viewer.

This would make the visual inspection system more general.

---

### 7.7.5 Cross-model trace comparison

Future work could compare qwen3:32b and DeepSeek-R1-32B traces visually.

For example, the viewer could show how different models choose objectives, use risk posture, trigger fallback, or rely on cached plans.

---

### 7.7.6 Larger-scale evaluation

Future evaluation could include more runs, more LLM backends, and more controlled ablations.

Possible ablations include:

* LLM enabled vs disabled;

* cache enabled vs disabled;

* risk filter enabled vs disabled;

* fallback-only vs LLM-supported;

* qwen3 vs DeepSeek vs additional models.

This would strengthen statistical confidence.

---

## 7.8 Lessons Learned

Several lessons were learned from the project.

First, integrating LLMs into game agents requires careful system design. The LLM cannot simply replace the agent policy. It must be surrounded by parsing, verification, fallback, caching, and logging.

Second, explainability must be designed into the system from the beginning. Decision traces and replay overlays are only possible because the system records decision provenance.

Third, engineering artefacts need structured documentation to become dissertation-quality projects. The technical documents, analysis documents, and dissertation chapters helped turn the implementation into a coherent academic project.

Fourth, limitations are valuable. By analysing fallback, caching, latency, and trace alignment issues, the project becomes more credible and academically stronger.

---

## 7.9 Conclusion

This dissertation presented LuxLLM-Agent, a decision-trace and action-verification framework for inspecting and evaluating LLM-based agents in Lux AI Season 3.

The system integrates LLM-based strategic planning with structured state summarisation, plan parsing, rule-based action verification, fallback behaviour, strategy caching, risk-aware filtering, decision trace logging, controlled-run evaluation, and replay-grounded visual inspection.

The evaluation showed that qwen3:32b and DeepSeek-R1-32B could both be integrated into the framework and complete 50 controlled Lux AI Season 3 runs with zero LLM errors. The qwen3:32b-backed configuration achieved a higher player_0 win rate in the current evidence, while the DeepSeek-R1-32B-backed configuration demonstrated stable execution with another reasoning-oriented LLM backend.

The key conclusion is that structured decision tracing and rule-based action verification can make LLM-based game agents more stable, inspectable, and evaluable. Rather than treating the LLM as a direct controller, LuxLLM-Agent treats the LLM as a strategic planner inside a controlled execution pipeline.

This makes the project more than a game-playing agent. It is a framework for understanding how LLM-based agents make decisions, how those decisions are verified, and how their behaviour can be evaluated through logs, metrics, and replay-grounded inspection.

