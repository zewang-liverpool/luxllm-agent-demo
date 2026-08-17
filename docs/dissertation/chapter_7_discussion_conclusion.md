# Chapter 7: Discussion and Conclusion

## 7.1 Introduction

This chapter discusses the main findings, contributions, limitations, and future work of LuxLLM-Agent.

The project set out to investigate the following research question:

> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent, long-horizon, and rule-constrained strategy game such as Lux AI Season 3, and how can the project-specific Decision-Trace and Action-Verification (DTAV) method address the observed limitations?

The previous chapters presented the system design, implementation, and evaluation of LuxLLM-Agent. The project developed DTAV as an LLM-based decision method rather than only building a game-playing agent. It combines compact state summarisation, LLM-based strategic proposals, deterministic action verification, fallback behaviour, strategy reuse, operational audit logging, controlled evaluation, and replay-grounded visual inspection.

This chapter reflects on how well the project answered the research question, what the main findings were, what technical contributions were made, and what limitations remain.

---

## 7.2 Answering the Research Question

The main research question was:

> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent, long-horizon, and rule-constrained strategy game such as Lux AI Season 3, and how can the project-specific Decision-Trace and Action-Verification (DTAV) method address the observed limitations?

The retained formal studies show how DTAV operates and provide evidence about validity, interventions, reliability, outcomes, and inspectability. They do not contain a direct-prompt control condition and therefore cannot, by themselves, estimate how much of the observed behaviour is caused by DTAV rather than the shared prompt and action adapter. The new matched direct-prompt versus DTAV runner and validation protocol address this design gap; the comparative conclusion must remain provisional until the formal paired run is completed.

Within that boundary, the existing evidence shows that DTAV supports LLM-based agents in three main ways.

First, the project-specific DTAV decision-trace approach makes agent behaviour more inspectable. Instead of only recording final match scores, LuxLLM-Agent records decision source, LLM mode, model name, fallback status, cached-plan usage, risk-filter behaviour, LLM errors, latency, unit intents, and score context. This allows the system to explain whether a decision came from a fresh LLM call, a cached LLM plan, fallback behaviour, rule fallback, or rule-based policy.

Second, rule-based action verification provides a controlled boundary between LLM reasoning and executable game actions. The LLM does not directly control Lux AI Season 3 units. Instead, it proposes high-level strategic intents, which are then parsed, checked, filtered, cached, repaired, or replaced before being converted into legal actions. This improves stability and reduces the risk of invalid LLM output affecting the environment.

Third, replay-grounded inspection connects decision traces to visual game behaviour. The LLM Decision Trace Overlay allows replay frames to be inspected together with the corresponding decision source, objective, fallback status, risk posture, and unit intents. This makes evaluation more informative than using final score alone.

Overall, the project demonstrates that the project-specific DTAV decision-trace approach and rule-based verification can make LLM-based game agents more stable, inspectable, and evaluable.

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

The formal evaluation completed 100 role-swapped matches for each backend and recorded 206,591 structured traces. All 4,591 LLM calls were valid after deterministic checks, but the trace audit also exposed 520 Qwen responses that required deterministic normalization and thousands of risk-filter interventions. This shows why gameplay outcome, structured-output quality, verification behaviour, and execution stability should be analysed separately.

---

### 7.3.3 The framework can support multiple LLM backends

The project compared qwen3:32b and DeepSeek-R1-32B under the same LuxLLM-Agent framework.

The formal matched-seed results were:

| Model | Matches | LLM wins | Win rate | Wilson 95% CI | Valid LLM calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| qwen3:32b | 100 | 63 | 63% | 53.2%-71.8% | 2,286/2,286 |
| deepseek-r1:32b | 100 | 60 | 60% | 50.2%-69.1% | 2,305/2,305 |

The matched backend comparison produced a mean outcome-score difference of 0.03 with a paired-bootstrap 95% interval of [-0.07, 0.13] and a McNemar exact p-value of 0.690. The results therefore show that the framework supports both backends under controlled evaluation, but do not establish that one backend is generally superior.

The supplementary direct LLM-versus-LLM experiment provides a stronger operational test of backend support because both players used the framework simultaneously. Across 100 role-swapped matches, Qwen won 54 and DeepSeek won 46; the seed-clustered 95% interval was [45%, 63%] and the seed-level exact sign p-value was 0.503. All 4,676 fresh calls were valid after deterministic checks, and complete per-player trace streams were retained. The non-significant outcome keeps the interpretation aligned with the dissertation: the experiment demonstrates simultaneous traceability and verification, not a model leaderboard.

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

The improved overlay makes Lux AI Season 3 explicit and separates evidence into three visible stages: LLM proposal, rule verification, and executed state. It also distinguishes fresh decisions, cached plans, rule fallback, and verifier intervention through labelled badges. The overlay therefore turns the viewer from a simple replay tool into a replay-grounded decision inspection interface.

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

The project evaluates both qwen3:32b and DeepSeek-R1-32B under the same framework, first against the same rule policy and then directly against each other with matched seeds and role swapping. The dual-agent implementation isolates concurrent player logs and validates both player-model assignments. This strengthens the project by showing that the trace-and-verification system is not tied to only one backend or one LLM-controlled side.

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

The project compares qwen3:32b and DeepSeek-R1-32B. The supplementary direct experiment adds a second opponent configuration but does not add another model family. The results therefore do not cover all possible LLMs or prompt configurations.

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

The formal experiment reduces role and seed confounding by evaluating both player roles under the same 50 environment seeds. It also reports Wilson intervals, seed-clustered bootstrap intervals, paired role analysis, and matched backend comparison. Residual internal-validity threats remain because the system is hybrid and uses one rule-based opponent, one prompt/configuration per backend, and one Lux evaluation setup.

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

The project uses one-command setup scripts, automated tests, version-controlled experiment runners, deterministic seed and bootstrap policies, environment metadata, model-server metadata, logs, JSON/JSONL evidence, and SHA-256-verified HPC archives to improve reproducibility.

The large-model runs still depend on Ollama, model availability, and GPU resources. Exact latency may vary across hardware, so the result should be interpreted as reproducible experimental evidence under the recorded environment rather than bit-identical performance on every machine.

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

This dissertation presented LuxLLM-Agent and the project-specific Decision-Trace and Action-Verification (DTAV) method for LLM decision making in Lux AI Season 3.

The system integrates LLM-based strategic planning with structured state summarisation, plan parsing, rule-based action verification, fallback behaviour, strategy caching, risk-aware filtering, decision trace logging, controlled-run evaluation, and replay-grounded visual inspection.

The primary evaluation showed that qwen3:32b and DeepSeek-R1-32B could both be integrated into the framework and complete 100 matched-seed, role-swapped Lux AI Season 3 matches each. Across 206,591 trace records, the framework achieved complete recorded trace fields and replay linkage, validated all 4,591 LLM calls after deterministic checks, exposed normalization and risk-filter interventions, and completed every match without an observed LLM timeout, API error, or downstream action fallback.

The supplementary direct LLM-versus-LLM experiment completed another 100 role-swapped matches while both players used the framework. Its 106,317 trace records were complete, all 4,676 fresh calls were valid after checks, and verifier interventions remained observable. The 54:46 outcome was not statistically significant, so this evidence strengthens the operational framework claim without changing the project into a model-ranking study.

The existing evidence establishes that DTAV creates an observable and reliable execution path under the recorded configurations. A final claim about how effectively it addresses the limitations of direct prompting depends on the newly specified formal matched comparison. Rather than treating the LLM as a direct controller, LuxLLM-Agent treats the LLM as a strategic planner inside a controlled execution pipeline.

This makes the project more than a game-playing agent. It is a framework for understanding how LLM-based agents make decisions, how those decisions are verified, and how their behaviour can be evaluated through logs, metrics, and replay-grounded inspection.

