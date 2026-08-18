# Chapter 1: Introduction

## 1.1 Background

Large language models have increasingly been explored as components of autonomous agents. Their ability to process structured information, generate plans, and produce natural-language explanations makes them attractive for complex decision-making tasks. However, using an LLM as part of an interactive agent is different from using it for static text generation. In a game or simulation environment, the agent must repeatedly observe the state, make decisions, produce valid actions, and adapt to changes over time.

This project studies LLM-based agent design in the context of Lux AI Season 3. Lux AI Season 3 is a partially observable, adversarial multi-agent, long-horizon, and rule-constrained strategy game. An agent must coordinate multiple units, retain useful information across a long sequence, explore hidden areas, discover scoring opportunities, react to an opponent, and continually produce actions in an exact environment schema. It is not a social-interaction task; its value as a test case comes from sequential uncertainty, multi-unit coordination, competition, and strict execution constraints.

A directly prompted LLM is difficult to use in this setting. It may produce invalid or incomplete responses, lose relevant state, fail to coordinate units, propose stale plans, or violate the action schema. Large LLMs may also be too slow to call at every game step. This motivates a controlled comparison between direct prompting and a project-specific method that summarises state, requests bounded proposals, verifies those proposals, falls back to rule-based behaviour when necessary, and records an operational audit trail for later inspection.

This dissertation presents LuxLLM-Agent and the project-specific Decision-Trace and Action-Verification (DTAV) method for LLM decision making in Lux AI Season 3. DTAV is the name of the method developed in this project rather than an established term in the literature.

---

## 1.2 Motivation

The motivation for this project comes from the gap between LLM reasoning ability and reliable agent execution.

LLMs can be useful for high-level planning. For example, an LLM may suggest that an agent should explore unknown areas, move toward candidate scoring locations, or adopt a low-risk strategy. However, these suggestions are not automatically executable game actions. They must be translated into valid unit-level actions that satisfy the environment rules.

This creates several practical challenges:

* raw game observations are too detailed for direct LLM use;

* LLM output may be malformed or incomplete;

* LLM-generated plans may be strategically reasonable but impossible to execute;

* LLM calls may introduce high latency;

* cached LLM plans may become stale;

* fallback behaviour may be needed when the LLM is unavailable or unsuitable;

* final win/loss results do not explain how decisions were made.

These challenges motivated the design of a hybrid LLM-rule system. In this project, the LLM is not treated as a direct action controller. Instead, it is treated as a strategic planner whose outputs are parsed, verified, cached, repaired, or replaced before execution.

The project is also motivated by the need for inspectable evaluation. If an LLM-based agent wins or loses a match, the final score alone does not explain whether the LLM contributed, whether fallback was used, or whether actions came from cached plans. For this reason, LuxLLM-Agent records decision-source information and provides a replay-grounded viewer with an LLM Decision Trace Overlay.

---

## 1.3 Problem Statement

The main problem addressed by this project is whether direct LLM prompting can support reliable decision making in this type of game and whether DTAV can address the limitations observed under controlled conditions.

A simple LLM agent may directly ask the model for actions and execute the output. This approach is risky in Lux AI Season 3 because actions must be legal, timely, and consistent with the current game state. Invalid or delayed decisions can make the agent unreliable. At the same time, using only a final match score as evaluation hides important behaviour, such as fallback usage, cached decisions, and rule-based corrections.

Therefore, the project addresses the following problem:

> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent, long-horizon, and rule-constrained strategy game such as Lux AI Season 3, and how can the project-specific DTAV method address the observed limitations?

This problem is both practical and research-oriented. It requires implementing a working agent system, but it also requires designing evaluation methods that reveal how the agent behaves internally.

---

## 1.4 Aim and Objectives

The aim of the project is:

> To design and evaluate an LLM-based decision method that helps an agent operate reliably in Lux AI Season 3 while making the route from observation to proposal, verification, executed action, and replay outcome inspectable.

To keep the investigation focused, this aim is divided into three objectives.

### Objective 1: Establish a direct-prompting baseline

Use compact Lux observations with fixed model settings, matched seeds, role swapping, and a minimal action adapter to measure how directly prompted LLM decisions behave.

### Objective 2: Implement the DTAV method

Apply deterministic normalisation, strategy reuse, rule-based checks, fallback, and risk-aware filtering to LLM proposals before constructing executable actions.

### Objective 3: Compare reliability and inspectability

Compare direct prompting and DTAV using validity, fallback and intervention rates, reliability, latency, match outcomes, and replay-linked visual inspection.

---

## 1.5 Research Question

The main research question is:

> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent, long-horizon, and rule-constrained strategy game such as Lux AI Season 3, and how can the project-specific Decision-Trace and Action-Verification (DTAV) method address the observed limitations?

The three objectives above operationalise this single research question. They are not presented as separate competing research questions.

### Evaluation focus 1: Direct-prompt feasibility

Measure whether directly prompted model outputs remain valid, current, and usable under the game's observation, coordination, horizon, and action constraints.

This establishes the unassisted comparison point for the method evaluation.

### Evaluation focus 2: DTAV interventions

Measure when DTAV normalises, reuses, filters, or replaces a proposal and distinguish proposal validity from the action that finally reaches the environment.

This identifies which limitations require deterministic intervention.

### Evaluation focus 3: Controlled comparison and inspection

Compare direct prompting and DTAV under the same model, seed, role, temperature, prompt-budget, and call-schedule controls, then link recorded events to replay states.

This connects quantitative differences with inspectable examples.

---

## 1.6 Project Contributions

This project makes several contributions.

### 1.6.1 A project-specific LLM decision method

The project implements DTAV, which connects state summarisation, LLM strategic proposals, parsing, action verification, fallback, caching, action planning, logging, and visualisation.

### 1.6.2 Rule-based verification of LLM proposals

The system treats LLM output as a strategic proposal rather than a directly executable action. This creates a controlled boundary between LLM reasoning and environment execution.

### 1.6.3 Decision-source logging

The system records whether decisions come from fresh LLM calls, cached LLM plans, fallback behaviour, rule fallback, or rule-based policy. This makes agent behaviour more inspectable.

### 1.6.4 Controlled evaluation with multiple LLM backends

The project evaluates qwen3:32b and DeepSeek-R1-32B under the same framework using 50 matched environment seeds with role swapping. Each backend completed 100 matches against the same rule-based opponent, giving 200 formal matches in the primary evaluation. All 4,591 recorded LLM calls were valid after deterministic checks. A supplementary 100-match experiment then placed the two LLM-assisted agents directly against each other with model roles swapped for every seed. This second experiment tests whether the framework can retain separate, valid traces and verifier evidence for two concurrent LLM-controlled players; it is not used to claim a universal model ranking.

### 1.6.5 Replay-grounded decision trace overlay

The project implements an LLM Decision Trace Overlay for the Season 3 viewer. This overlay displays step-aligned decision information during replay playback, including decision source, objective, fallback status, risk posture, score context, and unit intents.

### 1.6.6 Dissertation-oriented analysis and documentation

The project includes technical documentation, evaluation analysis, model comparison, and failure-case analysis. These artefacts support a structured dissertation rather than only an engineering demo.

---

## 1.7 Project Scope

The scope of the project is limited to Lux AI Season 3 and the implemented LuxLLM-Agent method.

The project focuses on:

* LLM-assisted strategic planning;

* rule-based action verification;

* fallback and strategy caching;

* controlled multi-run evaluation;

* decision trace logging;

* replay-grounded inspection.

The project does not claim to produce a leaderboard-winning Lux AI agent. It also does not claim that qwen3:32b is universally better than DeepSeek-R1-32B. The model comparison is specific to the current framework, prompt design, environment, and evaluation setup.

The project is best understood as an artefact-based investigation of direct LLM decision making and a project-specific method for addressing observable reliability and inspection limitations in a bounded game environment.

---

## 1.8 Summary of Evaluation Evidence

The primary evaluation uses the same 50 environment seeds for each backend and swaps the LLM between `player_0` and `player_1`. This controls seed and role effects more directly than the earlier fixed-role experiments.

| Model | Matches | LLM wins | Win rate | Wilson 95% CI | Valid LLM calls |
| --- | ---: | ---: | ---: | ---: | ---: |
| qwen3:32b | 100 | 63 | 63% | 53.2%-71.8% | 2,286/2,286 |
| deepseek-r1:32b | 100 | 60 | 60% | 50.2%-69.1% | 2,305/2,305 |

Across both backends, the evaluation contains 206,591 structured trace records. Agent-step and LLM-call trace completeness, replay linkage, and action-array shape validity were all 100%. Qwen required 520 deterministic normalization interventions, while DeepSeek required none. The risk filter changed proposed targets on 5,590 Qwen steps and 7,090 DeepSeek steps, providing observable evidence that rule-based verification affected execution rather than merely existing in the architecture.

The Qwen-versus-DeepSeek matched comparison found a mean outcome-score difference of 0.03 with a paired-bootstrap 95% interval of [-0.07, 0.13] and a McNemar exact p-value of 0.690. Therefore, the results support controlled framework evaluation but do not establish a general ranking between the two models.

The supplementary direct experiment completed another 100 role-swapped matches. Qwen won 54 and DeepSeek won 46, with a seed-level exact sign p-value of 0.503. More importantly for the research question, all 4,676 fresh LLM calls were valid after deterministic checks, all 106,317 trace records were complete, and normalization and risk-filter interventions were recorded separately for both players. These results extend the operational evidence from one LLM-controlled side to two without changing the project focus from framework evaluation to model comparison.

---

## 1.9 Dissertation Structure

The rest of the dissertation is organised as follows.

### Chapter 2: Background and Related Work

This chapter introduces relevant background on LLM-based agents, game AI, hybrid rule-based and LLM systems, action verification, explainability, and evaluation methods.

### Chapter 3: Requirements and Methodology

This chapter presents the project requirements and methodology. It explains the functional and non-functional requirements, the choice of Lux AI Season 3, the LLM integration method, and the evaluation method.

### Chapter 4: System Design

This chapter presents the system architecture of LuxLLM-Agent. It explains state summarisation, LLM decision making, parsing, verification, fallback, caching, risk filtering, action planning, logging, and replay-grounded inspection.

### Chapter 5: Implementation

This chapter describes how the system was implemented in the project codebase. It explains the main runtime files, logging implementation, controlled-run evidence, replay generation, and LLM Decision Trace Overlay viewer.

### Chapter 6: Evaluation

This chapter evaluates the system using gameplay outcomes, LLM execution metrics, decision-source distribution, fallback analysis, latency analysis, replay-grounded inspection, and failure-case analysis.

### Chapter 7: Discussion and Conclusion

This chapter discusses the main findings, limitations, threats to validity, future work, and final conclusions.

---

## 1.10 Summary

This chapter introduced the LuxLLM-Agent project and explained its motivation, problem statement, aim, research question, objectives, contributions, scope, and dissertation structure.

The central argument is that LLM-based game agents should not be evaluated only by final match outcomes. Their decisions should also be structured, verified, traced, and inspected. LuxLLM-Agent addresses this by treating the LLM as a strategic planner inside a controlled execution pipeline, supported by rule-based verification, fallback, caching, decision-source logging, controlled evaluation, and replay-grounded visualisation.

The next chapter introduces the background and related work needed to situate this project.

