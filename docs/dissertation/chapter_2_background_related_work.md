# Chapter 2: Background and Related Work

## 2.1 Introduction

This chapter introduces the background and related work relevant to LuxLLM-Agent.

The project investigates how structured decision tracing and rule-based action verification can support the inspection and evaluation of LLM-based agents in Lux AI Season 3. To place the project in context, this chapter discusses several related areas:

* large language models as agents;
* LLMs for planning and decision making;
* game AI and sequential decision making;
* hybrid LLM-rule systems;
* action verification and safety boundaries;
* explainability and decision traceability;
* evaluation of LLM-based agents;
* Lux AI Season 3 as an experimental environment.

The purpose of this chapter is not to provide a complete survey of all LLM-agent research. Instead, it identifies the concepts needed to understand the design choices of LuxLLM-Agent and explains how this project is positioned relative to prior work.

---

## 2.2 Large Language Models as Agents

Large language models are increasingly used as components of agent systems. In these systems, the model is not only used to answer a single question, but also to support planning, reasoning, tool use, environment interaction, and decision making.

A typical LLM-based agent follows an interaction loop:

```text
Observation
    |
    v
State interpretation
    |
    v
Reasoning or planning
    |
    v
Action selection
    |
    v
Environment update
```

This loop is different from ordinary text generation because the model must respond to a changing environment over time. In a sequential decision-making task, each decision may affect future states.

Recent work has explored several forms of LLM-based agents. ReAct shows that language models can interleave reasoning traces with task-specific actions in interactive decision-making settings (Yao et al., 2023a). Reflexion studies language agents that use verbal feedback and memory to improve future decisions (Shinn et al., 2023). Toolformer explores how language models can be extended through external tool use (Schick et al., 2023). Generative Agents demonstrates how LLMs can be integrated into architectures involving memory, reflection, and planning in interactive environments (Park et al., 2023). CAMEL studies communicative LLM-based agents in multi-agent settings (Li et al., 2023).

These works show that LLMs can be useful beyond single-turn text generation. They can support interaction, reasoning, planning, memory, and external system use. However, they also show that LLM-based agents usually require surrounding system structures. The model output often needs to be interpreted, constrained, checked, or connected to external tools and environments.

LuxLLM-Agent follows this broader direction. However, it does not treat the LLM as a direct game controller. Instead, the LLM is used to produce strategic proposals, while deterministic components handle parsing, verification, fallback, action planning, logging, and evaluation.

---

## 2.3 LLMs for Planning and Decision Making

Planning is an important part of intelligent agent behaviour. A planning system must decide what objective to pursue, which actions to take, and how to adapt when the environment changes.

LLMs can support planning because they can generate high-level strategies from structured context. For example, an LLM may suggest that an agent should explore unknown areas, secure a scoring location, avoid risk, or prioritise a particular target.

However, LLM-based planning has several challenges.

First, the LLM may not fully understand the environment rules. It may suggest actions that sound reasonable in natural language but are not legal in the game.

Second, the LLM may produce plans that are too abstract. A plan such as "explore the map" still needs to be converted into unit-level actions.

Third, LLM decisions may be unstable across steps. If the model is called repeatedly, it may change strategy too frequently.

Fourth, LLM calls may be slow, especially when using large local or HPC-hosted models.

Prior work supports the idea that LLM planning needs grounding and control. SayCan argues that language-model knowledge should be grounded in feasible actions or affordances before execution (Ahn et al., 2022). Voyager shows that an LLM-powered embodied agent can combine environment feedback, executable skills, and self-verification (Wang et al., 2023). Tree of Thoughts suggests that LLM reasoning can be improved by considering and evaluating multiple reasoning paths rather than relying only on a single left-to-right generation (Yao et al., 2023b).

LuxLLM-Agent applies a related principle in Lux AI Season 3. The LLM does not directly output final game actions. Instead, it proposes a structured strategic plan. This plan is parsed, checked, cached when appropriate, and converted into executable actions by rule-based and planning components.

The core design principle is:

> The LLM output is treated as a strategic proposal, not as a directly executable game action.

This principle makes the system more stable and easier to inspect.

---

## 2.4 Game AI and Sequential Decision Making

Game AI has long been used as a testbed for artificial intelligence. Games provide clear rules, measurable outcomes, controlled environments, and replayable behaviour.

Classic and modern game AI research has used games to study sequential decision making, planning, search, and learning. DQN demonstrated that deep reinforcement learning could learn policies directly from high-dimensional Atari game inputs (Mnih et al., 2015). Monte Carlo Tree Search has been widely studied as a search-based planning approach for games and other sequential decision problems (Browne et al., 2012). More complex strategy-game systems such as AlphaStar and OpenAI Five show that games can involve long horizons, partial observability, complex action spaces, and multi-agent interaction (Vinyals et al., 2019; Berner et al., 2019).

Lux AI Season 3 is smaller than environments such as StarCraft II or Dota 2, but it still includes several relevant properties:

* repeated decision making;
* multi-agent interaction;
* hidden or uncertain information;
* unit-level control;
* scoring opportunities;
* resource and target selection;
* replayable match evidence.

This makes Lux AI Season 3 suitable for studying LLM-assisted agent decision making. The environment is complex enough to require strategic reasoning, but structured enough to support logging, evaluation, and replay analysis.

In this project, Lux AI Season 3 is used not only as a game environment, but also as an experimental setting for studying how LLM-based decisions can be verified, traced, and inspected.

---

## 2.5 Hybrid LLM-rule Agent Architectures

A purely LLM-controlled agent may be difficult to make reliable in a rule-based game environment. The model may generate an invalid target, refer to a non-existent unit, produce a plan that cannot be executed, or change its strategy too frequently.

Hybrid LLM-rule architectures address this problem by combining LLM reasoning with deterministic rule-based components.

In a hybrid architecture, the LLM may handle:

* high-level planning;
* objective selection;
* risk posture;
* unit-level intent generation;
* explanation of strategy.

Rule-based components may handle:

* action legality;
* movement constraints;
* fallback behaviour;
* local tactical decisions;
* safety filtering;
* environment-specific execution.

This type of design is related to prior work where LLMs are embedded inside larger systems rather than used alone. Toolformer studies LLMs that use external APIs and tools (Schick et al., 2023). SayCan combines high-level language-model reasoning with executable skill constraints (Ahn et al., 2022). Voyager connects LLM planning with executable code skills, feedback, and self-verification in Minecraft (Wang et al., 2023). ReAct connects reasoning and acting in interactive tasks (Yao et al., 2023a).

LuxLLM-Agent is also a hybrid system, but its focus is different. It does not train a new language model, create a general-purpose tool-using model, or implement a lifelong-learning agent. Instead, it builds a practical framework for using LLM strategic proposals inside Lux AI Season 3 with verification, fallback, caching, and decision trace logging.

This architecture has two advantages.

First, it improves stability. The agent can still act if the LLM is disabled, invalid, slow, or unavailable.

Second, it improves inspectability. Since the system records whether actions come from fresh LLM decisions, cached LLM plans, fallback, or rules, the behaviour can be analysed more carefully.

---

## 2.6 Action Verification and Safety Boundaries

Action verification is the process of checking whether a proposed action is legal, safe, and appropriate before execution.

In LLM-based agents, action verification is important because the model output cannot be assumed to be correct. An LLM may produce an action that violates environment constraints, refers to unavailable information, or gives a plan that cannot be converted into legal game actions.

This problem is closely related to the idea of grounding. SayCan argues that language-model outputs need to be grounded in feasible skills or affordances before a robot executes them (Ahn et al., 2022). Voyager also highlights the importance of executable skills, feedback, and self-verification for embodied LLM agents (Wang et al., 2023). Toolformer is relevant because it shows that LLMs can be embedded into systems that decide when and how to use external tools, rather than operating only as standalone text generators (Schick et al., 2023).

In LuxLLM-Agent, the safety boundary is implemented through:

* structured output parsing;
* rule-based action verification;
* fallback behaviour;
* strategy caching;
* risk-aware action filtering;
* action planning.

The core principle is:

> The LLM output is treated as a strategic proposal, not as a directly executable game action.

This principle reduces the risk of invalid LLM output affecting the environment. It also makes the system easier to evaluate because the pipeline records when a plan is accepted, cached, replaced, or supported by fallback.

Action verification is therefore not only a reliability mechanism. It is also part of the project’s evaluation framework.

---

## 2.7 Explainability, Traceability, and Decision Provenance

Explainability is important for systems where users need to understand how decisions are made. In agent systems, this is especially important because behaviour emerges over time through repeated interactions with the environment.

For LLM-based agents, explainability can be difficult. A final action may be influenced by a model response, cached strategy, fallback rule, local verifier, or action planner. Without logs, it is difficult to know which component produced the final behaviour.

Prior work has shown the value of recording or exposing intermediate agent information. ReAct uses reasoning traces alongside actions, which can make agent trajectories easier to interpret (Yao et al., 2023a). Generative Agents uses memory, reflection, and planning as part of an agent architecture (Park et al., 2023). Reflexion uses verbal reflections and feedback records to improve later decisions (Shinn et al., 2023).

LuxLLM-Agent focuses on decision traceability and decision provenance.

Decision traceability means that the system records information about decisions over time. Decision provenance means that the system identifies the source of a decision.

In LuxLLM-Agent, important decision sources include:

```text
llm_fresh
cached_llm
fallback
rule_fallback
rule_player
rule_only
```

These decision sources allow the project to analyse whether behaviour came from a fresh LLM call, a cached LLM plan, fallback, or rule-based logic.

The LLM Decision Trace Overlay extends this idea by showing decision trace information during replay playback. This makes the system more inspectable than a standard replay viewer.

---

## 2.8 Evaluation of LLM-based Agents

Evaluating LLM-based agents is more complex than evaluating ordinary text generation systems.

A text generation system may be evaluated using output quality, correctness, or human preference. An agent system must also be evaluated by how it behaves in an environment over time.

For game agents, common evaluation metrics include:

* win rate;
* reward;
* number of completed matches;
* score difference;
* failure rate.

However, these metrics are not sufficient for LLM-based agents. A final win or loss does not explain how the decision was made.

This is especially important for hybrid systems. In LuxLLM-Agent, an executed action may come from a fresh LLM plan, a cached LLM plan, fallback logic, or rule-based behaviour. Therefore, evaluation should include both outcome metrics and process metrics.

LuxLLM-Agent uses a broader evaluation approach, including:

* gameplay outcome metrics;
* LLM execution metrics;
* decision-source metrics;
* fallback and verification metrics;
* latency metrics;
* replay-grounded inspection metrics;
* qualitative failure-case analysis.

This evaluation approach supports the dissertation research question because it focuses on inspection and evaluation rather than only performance.

The project’s primary controlled evidence uses 50 matched environment seeds with role swapping for qwen3:32b and DeepSeek-R1-32B (Yang et al., 2025; DeepSeek-AI et al., 2025). Each backend completed 100 matches. The design makes role effects and seed effects visible and supports paired comparison without treating the outcome as a hardware-independent model ranking.

This shows why evaluation should distinguish between execution stability, strategic quality, and final outcome.

---

## 2.9 Replay-based Analysis and Visual Inspection

Replay-based analysis is useful in game AI because it allows behaviour to be inspected after a match. A replay can show how units moved, how the score changed, and how the game state evolved.

However, a normal replay does not show why an agent made a decision.

For LLM-based agents, this is a limitation. A user may see a unit move toward a target, but the replay alone does not reveal whether the action came from an LLM plan, a cached strategy, fallback logic, or rule-based movement.

LuxLLM-Agent addresses this by adding an LLM Decision Trace Overlay to the Season 3 viewer.

The overlay displays:

* frame and step;
* phase;
* decision source;
* LLM model;
* objective;
* risk posture;
* fallback status;
* risk filter status;
* score context;
* unit intents.

This turns replay analysis into replay-grounded decision inspection.

The overlay is important for the project because it connects implementation, evaluation, and demonstration. It provides visual evidence that the system can trace and inspect LLM-agent behaviour.

---

## 2.10 Lux AI Season 3 as an Evaluation Environment

Lux AI Season 3 was selected because it provides a structured but challenging environment for agent evaluation.

The official competition description presents Lux AI Season 3 as a NeurIPS 2024 multi-agent 1v1 competition designed around adaptation to changing game dynamics (Tao et al., 2024). The official Season 3 specification describes a two-team game on a 2D map, arranged as a best-of-5 match sequence, with each match lasting 100 time steps. The official Lux-Design-S3 repository provides the environment, kits, and specifications used by this project (Lux AI Challenge, 2024).

These properties make Lux AI Season 3 suitable for this project because it includes:

* sequential decision making;
* hidden or uncertain information;
* repeated action selection;
* multiple controllable units;
* scoring and exploration;
* opponent interaction;
* replay-based analysis;
* measurable outcomes.

The environment also exposes the limitations of direct LLM control. Since actions must be legal and timely, the LLM cannot simply output arbitrary text. It must be integrated into a controlled action pipeline.

This makes Lux AI Season 3 a suitable environment for investigating the project’s research question.

---

## 2.11 Positioning of LuxLLM-Agent

LuxLLM-Agent is positioned as a framework for inspecting and evaluating LLM-based agents, rather than as a pure competition bot.

Its main distinguishing features are:

* structured state summarisation;
* LLM-based strategic planning;
* rule-based verification;
* fallback and caching;
* risk-aware filtering;
* decision-source logging;
* controlled multi-run evaluation;
* replay-grounded decision trace overlay.

This positioning is important because the project’s contribution is not only that an LLM can be connected to Lux AI Season 3. The contribution is that LLM decisions can be structured, verified, traced, evaluated, and visually inspected.

This distinguishes the project from a simple LLM wrapper around an existing rule-based agent.

---

## 2.12 Summary

This chapter introduced the background and related work relevant to LuxLLM-Agent.

LLMs can support high-level planning, but they are difficult to use as direct controllers in sequential game environments. Game agents require valid actions, stable execution, and repeated decision making. Therefore, a hybrid architecture is needed.

LuxLLM-Agent addresses this by combining LLM strategic planning with rule-based verification, fallback, strategy caching, risk-aware filtering, decision trace logging, controlled evaluation, and replay-grounded inspection.

The next chapter presents the project requirements and methodology in more detail. The consolidated reference list appears after Chapter 7.

