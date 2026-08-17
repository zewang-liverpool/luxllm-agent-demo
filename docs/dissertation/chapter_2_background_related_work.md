# Chapter 2: Background and Related Work

## 2.1 Introduction and Review Scope

This chapter establishes the academic context for LuxLLM-Agent and develops the argument for its three design priorities: bounded state representation, deterministic action verification, and replay-grounded decision tracing. The main research question is:

> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent, long-horizon, and rule-constrained strategy game such as Lux AI Season 3, and how can the project-specific Decision-Trace and Action-Verification (DTAV) method address the observed limitations?

The review is organised around the concepts needed to answer this question rather than around a chronological list of papers. It covers:

* LLMs as interactive agents;
* state representation under partial observability;
* language-model planning and its limitations;
* game AI and sequential decision making;
* hybrid LLM-rule architectures;
* grounding, action verification, and shielding;
* decision provenance and the limits of generated explanations;
* trajectory-level evaluation of LLM agents; and
* Lux AI Season 3 as an experimental environment.

The chapter is a focused narrative review, not a systematic literature review. Priority is given to peer-reviewed work from established AI, machine-learning, and human-computer-interaction venues, together with official Lux AI sources and model technical reports where necessary. The discussion does not assume that a method developed for robotics, reinforcement learning, or language interaction transfers directly to Lux AI. Instead, each comparison identifies both the relevant principle and the limits of the analogy.

---

## 2.2 LLMs as Components of Interactive Agents

An LLM-based agent differs from a single-turn text generator because it must repeatedly interpret observations, select objectives, act through an interface, and respond to the resulting state. A simplified interaction loop is:

```text
observation -> state representation -> proposal -> verification
            -> executable action -> environment transition -> new observation
```

This distinction matters because fluent text is not sufficient evidence of competent agent behaviour. The model must maintain useful context across turns, produce output that can be grounded in the environment, and tolerate the consequences of earlier decisions.

Several influential systems demonstrate different ways to embed an LLM within a broader agent architecture. ReAct interleaves model-generated reasoning and task actions, allowing observations from the environment to influence later steps (Yao et al., 2023a). Reflexion adds verbal feedback and memory so that an agent can adapt after failure (Shinn et al., 2023). Generative Agents combines memory, reflection, and planning to produce persistent behaviour in an interactive simulation (Park et al., 2023). Toolformer investigates how a language model can learn to invoke external tools rather than relying only on its internal parameters (Schick et al., 2023). CAMEL studies role-conditioned communication between LLM agents (Li et al., 2023).

These systems support the general claim that LLMs can contribute reasoning, planning, memory, or tool selection within an agent. They do not establish that unconstrained model output is a reliable controller. In each case, the model operates through an architecture that supplies prompts, memory, actions, tools, feedback, or environment interfaces.

LuxLLM-Agent adopts this architectural view but gives the LLM a deliberately bounded role. The model proposes high-level strategic intents; deterministic components parse, normalize, verify, cache, replace, and translate those intents before any action reaches the game environment. This separation is central to the project because it enables the proposal and the executed behaviour to be inspected independently.

---

## 2.3 State Representation under Partial Observability

### 2.3.1 Why raw observations are insufficient

Lux AI Season 3 is a sequential and partially observable environment. At each step, the agent sees only an observation of the underlying game state, while useful decisions may depend on earlier observations, inferred map structure, discovered relic locations, unit state, opponent visibility, score progression, and match phase.

Partially observable Markov decision processes formalise the general problem of acting when the complete environment state is unavailable (Kaelbling et al., 1998). An agent may therefore require a belief or memory derived from observation history rather than treating the latest observation as a complete state. LuxLLM-Agent does not implement a formal Bayesian belief-state solver, but the POMDP perspective explains why a current raw observation is not an adequate strategic prompt.

Passing the complete raw game state to an LLM would also create practical problems:

* the representation would be large and repetitive;
* implementation details could obscure strategically relevant facts;
* coordinates and unit identifiers could be difficult to use consistently;
* prompt length and inference latency would increase; and
* changes between adjacent steps would be difficult to distinguish.

### 2.3.2 Structured summaries as an interface

Embodied-agent research provides evidence that language-model plans become more useful when connected to a restricted environment interface. Huang et al. (2022) show that high-level language plans often fail to map directly to admissible actions and improve executability by translating them into an available action set. SayCan similarly combines language-model preferences with affordance values that represent which robot skills are feasible in the current situation (Ahn et al., 2022).

LuxLLM-Agent applies the interface principle at the input as well as the output. Its state summarizer converts environment observations and retained game knowledge into a compact schema containing strategically relevant fields. The aim is not to produce a lossless copy of the environment. It is to create a bounded interface between a numerical game state and a language model.

This design supports the first research objective, but it introduces an important trade-off. Compression improves prompt stability and inspectability, while omitted information may remove evidence required for a better strategy. The summarizer must therefore be evaluated as part of the agent rather than treated as a neutral preprocessing step. LuxLLM-Agent records prompt-related and state-related information so that later inspection can distinguish a poor proposal from a potentially incomplete representation.

---

## 2.4 Language Models for Planning: Potential and Limitations

### 2.4.1 Evidence supporting high-level planning

Language models can express high-level objectives in a form that is useful to an agent. ReAct demonstrates that language reasoning can be combined with observations and actions in interactive tasks (Yao et al., 2023a). Huang et al. (2022) show that LMs can decompose natural-language goals into intermediate steps when the plans are subsequently mapped to admissible actions. Tree of Thoughts explores deliberate reasoning through the generation and evaluation of multiple candidate reasoning paths (Yao et al., 2023b). Voyager combines an LLM with environment feedback, an executable skill library, and iterative verification in Minecraft (Wang et al., 2023).

Together, these studies suggest a useful role for an LLM as a source of semantic decomposition, heuristic guidance, or high-level strategy. This is the role used by LuxLLM-Agent: the model selects bounded intents such as exploring stale information, moving towards a candidate target, or exploiting a confirmed scoring location.

### 2.4.2 Evidence against direct autonomous planning

Positive demonstrations must be balanced against evidence that fluent plans are not necessarily executable plans. Valmeekam et al. (2023) evaluate LLMs on planning domains and report limited autonomous plan correctness, while finding more promise when LLM output is used as heuristic guidance or checked by external verifiers. Huang et al. (2022) likewise report that naively generated plans often fail to match admissible environment actions.

These findings challenge a design in which the model directly controls the environment. They also motivate three decisions in LuxLLM-Agent:

1. the LLM produces a small structured proposal rather than a full low-level plan;
2. deterministic logic checks and repairs the proposal before use; and
3. a rule policy remains available when a proposal is invalid, stale, unavailable, or unsuitable.

Strategy caching addresses a further sequential problem. Calling the model at every environment step may increase latency and cause rapid changes in objective. Reusing a previously verified strategy for a bounded interval can improve continuity, but a cached plan can itself become stale. The decision trace must therefore record whether a plan is fresh, cached, or replaced.

The literature does not justify the claim that LLM planning is generally reliable. It supports a narrower conclusion: LLMs can provide useful high-level guidance when their output is grounded, verified, and evaluated within a larger execution system.

---

## 2.5 Game AI and Sequential Decision Making

Games are established testbeds for sequential decision making because they provide explicit rules, measurable outcomes, controllable experiments, and replayable trajectories. Different traditions illustrate the range of methods used in game AI.

Monte Carlo Tree Search represents explicit search over possible future decisions and has been applied across many game and planning settings (Browne et al., 2012). DQN demonstrated that deep reinforcement learning could learn policies from high-dimensional Atari observations (Mnih et al., 2015). AlphaStar and OpenAI Five extended learning-based game agents to complex strategy games with long horizons, partial observability, large action spaces, and multi-agent interaction (Vinyals et al., 2019; Berner et al., 2019).

LuxLLM-Agent is not a replacement for search or reinforcement learning and does not claim their performance or formal properties. These systems are relevant because they show that game outcomes emerge from repeated decisions under controlled rules, and that evaluation must account for the environment, opponent, position, and experimental protocol.

Lux AI Season 3 offers a smaller but still meaningful setting:

* decisions repeat across steps and matches;
* information is incomplete and changes over time;
* multiple units require coordinated action;
* the opponent influences the value of a plan;
* player role and environment seed can affect results; and
* complete matches can be replayed and compared.

These properties make the environment suitable for studying a hybrid LLM-based agent. They also require controlled evaluation. A raw win percentage without matched seeds, role swapping, provenance, or failure information would conflate model behaviour with environment and system effects.

---

## 2.6 Hybrid LLM-Rule Architectures

Prior agent systems repeatedly show that an LLM is most useful when surrounded by environment-specific mechanisms. Toolformer connects model generation to external APIs (Schick et al., 2023). ReAct connects language reasoning to a restricted action interface and observations (Yao et al., 2023a). SayCan separates semantic task relevance from skill feasibility (Ahn et al., 2022). Voyager couples planning with executable programs, feedback, and verification (Wang et al., 2023).

The shared architectural pattern is not that rules and models perform identical work. It is that they provide different capabilities:

| LLM contribution | Deterministic contribution |
| --- | --- |
| semantic interpretation | schema enforcement |
| high-level objective selection | action legality and array construction |
| flexible strategic proposal | coordinate, unit, and target validation |
| context-dependent intent generation | risk filtering and local movement |
| natural-language rationale field | fallback and bounded execution |

This division has two advantages. First, it preserves a valid execution path when the LLM is unavailable or produces unusable output. Second, it creates observable boundaries: the system can record which component proposed, repaired, rejected, cached, or executed a decision.

The division also limits attribution. A winning action may result from an LLM proposal, deterministic normalization, a cached strategy, a risk-filter change, or rule fallback. Therefore, LuxLLM-Agent does not equate the final agent with the LLM backend. The unit of study is the hybrid decision pipeline.

---

## 2.7 Action Grounding, Verification, and Safety Boundaries

### 2.7.1 Grounding proposals in executable actions

SayCan is especially relevant to action grounding. It ranks high-level language instructions using both semantic usefulness and learned affordance values, so an instruction must be useful and executable before selection (Ahn et al., 2022). Huang et al. (2022) similarly translate language-generated steps to actions admitted by the environment. These methods support the principle that semantic plausibility alone is insufficient for control.

LuxLLM-Agent applies a related principle in a game-specific pipeline:

```text
LLM proposal
    -> JSON parsing
    -> schema and identifier normalization
    -> intent validation
    -> target and risk checks
    -> deterministic action planning
    -> Lux action array
```

The LLM is therefore a proposal generator, not an action authority.

### 2.7.2 Relationship to shielding

Safe reinforcement learning via shielding provides a stronger formal example of placing a corrective layer between a learned policy and an environment. Alshiekh et al. (2018) define a shield that monitors selected actions and corrects actions that would violate a temporal-logic safety specification. The concept is useful for LuxLLM-Agent because both architectures separate a learned decision source from a deterministic intervention layer.

The analogy must not be overstated. LuxLLM-Agent's verifier is not a formally synthesised shield, and the project does not prove temporal-logic safety or global optimality. Its checks cover implemented schemas, identifiers, action construction, observable risks, and fallback conditions. The empirical question is whether these checks operate as documented and leave auditable evidence, not whether they guarantee every desirable property for every possible state.

This distinction improves the precision of the DTAV intervention objective. The project evaluates:

* whether model output satisfies the bounded schema;
* whether deterministic normalization repairs specific deviations;
* whether risk verification changes proposed targets;
* whether fallback remains available;
* whether legal action arrays are constructed in the observed runs; and
* whether each intervention is recorded with its reason and provenance.

The relevant contribution is observable runtime control. It is narrower than formal safety, but stronger than merely stating that a verifier exists.

---

## 2.8 Decision Tracing, Provenance, and Explanation Limits

### 2.8.1 From generated text to operational provenance

ReAct exposes model-generated reasoning alongside actions, while Reflexion and Generative Agents retain textual records that influence later behaviour (Yao et al., 2023a; Shinn et al., 2023; Park et al., 2023). These works show the practical value of retaining intermediate agent information.

However, an agent log can support different kinds of claim:

1. **Generation record:** what text or structured proposal the model returned.
2. **Decision provenance:** which component supplied the plan used at a step.
3. **Transformation record:** how deterministic components altered the proposal.
4. **Execution record:** which action array was sent to the environment.
5. **Causal explanation:** why the model internally produced a particular proposal.

LuxLLM-Agent supplies the first four forms of evidence. It does not claim the fifth.

### 2.8.2 Why a rationale is not automatically a faithful explanation

Turpin et al. (2023) show that chain-of-thought explanations can omit factors that influenced a model's answer and can rationalise biased outputs. This is important because a plausible natural-language reason should not automatically be interpreted as a faithful account of the model's internal computation.

LuxLLM-Agent therefore treats any model-provided `reason` field as part of the proposal record, not as privileged access to internal reasoning. Its stronger evidence comes from externally observable events:

* the exact structured proposal;
* whether parsing and schema checks succeeded;
* whether normalization occurred;
* whether a cached or fallback source was used;
* whether risk filtering changed a target;
* the resulting unit intents and action array; and
* the replay state associated with the step.

This operational definition makes “traceability” more defensible. The trace can show what the system received and did, even when it cannot prove why the model generated the content.

### 2.8.3 Replay-grounded inspection

A normal game replay shows state transitions but not the decision pipeline that produced them. A text log shows pipeline events but can be difficult to interpret without spatial and temporal context. LuxLLM-Agent links these two evidence sources through a decision-trace overlay.

The overlay distinguishes sources such as:

```text
llm_fresh
cached_llm
fallback
rule_fallback
rule_player
rule_only
```

It also displays the proposal, verifier status, match phase, score context, unit intents, and executed state. This supports the comparison and inspection objective by allowing an assessor to move from a quantitative summary to a specific replay step and inspect the recorded transformation chain.

---

## 2.9 Evaluation of LLM-Based Agents

### 2.9.1 Why final success is insufficient

AgentBench evaluates LLMs across eight interactive environments and identifies long-term reasoning, decision making, and instruction following as important failure sources (Liu et al., 2024). It demonstrates the need to evaluate models through environment interaction rather than only static language tasks.

AgentBoard goes further by arguing that final success rate reveals little about behaviour during multi-turn interaction. It introduces fine-grained progress measures and interactive analysis for partially observable agent trajectories (Ma et al., 2024). This is closely aligned with the evaluation motivation of LuxLLM-Agent: a final win or loss cannot show whether the LLM output was valid, whether rules intervened, or which source controlled a particular step.

### 2.9.2 Outcome, process, and reliability evidence

For a hybrid LLM game agent, evaluation should separate at least three layers:

| Evidence layer | Example questions |
| --- | --- |
| Outcome | Did the agent complete the match, win, or score? |
| Process | Was the strategy fresh, cached, normalized, filtered, or replaced? |
| Reliability | Were calls valid, actions well formed, traces complete, and failures observable? |

These layers answer different questions. A high win rate cannot prove trace completeness. A 100% post-check validity rate cannot prove that raw model output was always conforming. A large intervention count proves that the verifier changed proposals, but not that every change improved the outcome.

### 2.9.3 Controlled comparison

Game evaluation must also control nuisance variables. LuxLLM-Agent uses matched environment seeds and role swapping so that each seed is evaluated with both player assignments. It reports uncertainty intervals and paired analyses rather than treating matches as context-free samples. Backend outcomes are secondary to the framework evidence because the hybrid pipeline, prompt, rule policy, environment, and inference settings all contribute to performance.

The direct LLM-versus-LLM experiment is similarly bounded. It tests whether provenance and verification remain attributable when both players use LLM proposals. It is not designed to establish a hardware-independent or generally applicable model ranking.

---

## 2.10 Lux AI Season 3 as an Evaluation Environment

Lux AI Season 3 was a NeurIPS 2024 multi-agent competition concerned with adaptation to changing game dynamics (Tao et al., 2024). The official Lux-Design-S3 repository provides the environment, kits, and specification used by this project (Lux AI Challenge, 2024). The specification defines a two-team game on a two-dimensional map, organised as a best-of-five sequence with 100 time steps per match.

The environment provides:

* sequential decisions under partial observability;
* repeated exploration and exploitation;
* multiple controllable units;
* resource, target, and movement constraints;
* direct opponent interaction;
* measurable scores and winners; and
* replayable state transitions.

These properties create a useful middle ground. The environment is substantially more structured than an open-ended embodied world, making deterministic action checks and repeated experiments feasible. At the same time, it is sufficiently dynamic to expose stale plans, role effects, opponent-dependent risks, and the limitations of direct language-model control.

The official environment is the experimental object; the replay viewer is an analysis tool built around retained evidence. This distinction prevents the project from treating a visual demonstration as a substitute for controlled evaluation.

---

## 2.11 Comparative Synthesis and Research Gap

### 2.11.1 Comparison with the most relevant prior work

| Work | Main contribution | Relevance to LuxLLM-Agent | Limitation relative to this project |
| --- | --- | --- | --- |
| ReAct (Yao et al., 2023a) | Interleaves reasoning and actions | Supports interactive proposal-action loops | Does not provide this project's game-specific verifier and replay-provenance audit |
| SayCan (Ahn et al., 2022) | Grounds language instructions in feasible robot skills | Strong precedent for separating semantic preference from executability | Robotics affordance model rather than Lux rules, trace metrics, and role-swapped game evaluation |
| Huang et al. (2022) | Maps high-level LM plans to admissible actions | Shows why raw language plans need an action interface | Focuses on embodied task planning rather than competitive multi-agent traces |
| Voyager (Wang et al., 2023) | Uses executable skills, environment feedback, and self-verification | Supports hybrid LLM-plus-execution architecture | Focuses on open-ended skill acquisition rather than controlled matched-seed evaluation |
| Valmeekam et al. (2023) | Critically evaluates autonomous LLM planning | Supports using LLMs as heuristic proposal sources with external verification | Evaluates symbolic planning domains rather than a real-time hybrid game agent |
| Shielding (Alshiekh et al., 2018) | Corrects unsafe learned-policy actions using formal specifications | Provides a conceptual basis for an intervention layer | LuxLLM-Agent does not provide formal shielding guarantees |
| AgentBench (Liu et al., 2024) | Benchmarks LLMs in interactive environments | Supports multi-environment agent evaluation and failure analysis | Emphasises benchmark performance rather than domain-specific proposal-to-action provenance |
| AgentBoard (Ma et al., 2024) | Adds fine-grained progress and trajectory analysis | Closest evaluation precedent for moving beyond final success | Does not implement the Lux-specific verification and replay linkage used here |
| Turpin et al. (2023) | Demonstrates unfaithful generated explanations | Motivates cautious interpretation of LLM rationale fields | Studies explanation faithfulness, not environment action provenance |

### 2.11.2 Identified gap

The reviewed literature provides strong individual precedents for interactive LLM agents, admissible-action grounding, external verification, shielding, trajectory-level evaluation, and visual analysis. Within this focused review, however, no single work combines all of the following in Lux AI Season 3:

1. a bounded structured representation of a partially observable game state;
2. an LLM used only for high-level strategic proposals;
3. deterministic normalization, risk checks, fallback, and action construction;
4. explicit provenance across fresh, cached, fallback, and rule decisions;
5. step-aligned linkage between proposals, verifier interventions, actions, and replay state; and
6. matched-seed, role-swapped evaluation with retained machine-readable evidence.

This gap defines the project's contribution. LuxLLM-Agent is not presented as a new foundation model, a formally safe controller, or a state-of-the-art competition agent. It is an artefact and evaluation framework that integrates these ideas so that LLM-assisted game behaviour can be inspected at the boundary between model proposal and environment execution.

### 2.11.3 Alignment with the research questions

| Research question | Main literature foundation | Project response |
| --- | --- | --- |
| Objective 1: Direct-prompt baseline | Partial observability; grounded environment interfaces; limits of autonomous planning (Kaelbling et al., 1998; Huang et al., 2022; Valmeekam et al., 2023) | Same compact state and call schedule with DTAV interventions disabled |
| Objective 2: DTAV interventions | Affordance grounding and shielding (Ahn et al., 2022; Alshiekh et al., 2018) | Parsing, normalisation, risk filtering, strategy reuse, fallback, and deterministic action construction |
| Objective 3: Comparison and inspection | Interactive and trajectory-level evaluation; explanation limits (Liu et al., 2024; Ma et al., 2024; Turpin et al., 2023) | Matched method comparison, provenance logs, verifier audits, and a replay-linked audit overlay |

This mapping ensures that the literature review motivates the actual methodology and evaluation rather than acting as a detached survey.

---

## 2.12 Summary

The literature supports a qualified case for LLM-based agents. LLMs can contribute semantic decomposition, strategic proposals, memory, and interaction, but direct autonomous planning remains unreliable. Environment-interacting agents therefore benefit from bounded interfaces, executable skills, deterministic checks, and fallback mechanisms.

Research on shielding provides a conceptual precedent for monitoring and correcting learned decisions, while also clarifying that LuxLLM-Agent's empirical verifier should not be confused with a formally verified safety shield. Research on AgentBench and AgentBoard shows why agent evaluation should include interactive trajectories and process evidence rather than only final success. Work on unfaithful chain-of-thought explanations further motivates the project's emphasis on observable proposal, transformation, and execution records instead of claims about private model reasoning.

These findings justify the architecture and evaluation used in the following chapters. Chapter 3 translates the identified gap into requirements and methodology. Chapters 4 and 5 describe the implementation, Chapter 6 evaluates outcomes and trace-and-verification evidence, and Chapter 7 answers the research questions while stating the limits of the claims.
