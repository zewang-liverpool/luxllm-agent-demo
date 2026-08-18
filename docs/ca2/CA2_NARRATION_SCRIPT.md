# CA2 video narration script

Target duration: **9:20**. Hard rehearsal limit: **9:40**. The final submitted video must remain below 10:00.

The spoken text is written in natural presentation English. Text in square brackets is a screen action and is not spoken.

## 0:00–0:35 — Title and ethical compliance

[Show slide 1.]

Hello. My name is Ze Wang, and this is my COMP702 project, LuxLLM-Agent: a Decision-Trace and Action-Verification method for LLM decision making in Lux AI Season 3. My supervisor is Dr Meng Fang.

The project uses no human participants and no personal data. It runs only in a game-AI environment, and I have followed the University's ethical guidance. The confirmed data and participant category codes are shown on this title slide.

## 0:35–1:35 — Problem, motivation, and research question

[Advance to slide 2.]

Large language models can propose useful high-level game strategies, but a fluent proposal is not necessarily valid, current, safe to execute, or easy to inspect. A simple win rate cannot explain whether an action came from a fresh LLM response, a cached strategy, a deterministic fallback, or a verifier intervention.

Lux AI Season 3 is a partially observable, adversarial multi-agent, long-horizon, and rule-constrained strategy game. This motivated my main research question: How effectively can directly prompted LLMs make decisions in this type of game, and how can my project-specific Decision-Trace and Action-Verification, or DTAV, method address the observed limitations?

The central goal is therefore not to claim the strongest Lux bot or to rank general-purpose language models. DTAV is the name of the method developed in this project, not an established field term. Its trace is a predefined operational audit record, not hidden chain of thought.

## 1:35–2:10 — Design and contribution

[Advance to slide 3.]

The framework has three broad stages. First, the state summariser converts the raw observation and retained game memory into a compact, structured prompt. Second, the LLM response is parsed, schema-checked, normalised when possible, cached when appropriate, and filtered using deterministic game rules. Invalid or unavailable proposals can be replaced by an observable rule-based fallback. Third, the action planner constructs legal Lux actions and writes per-step provenance, verification, timing, score, and replay-link fields.

The important design boundary is that the LLM never sends arbitrary actions directly to the environment. This separation makes failures visible and keeps the final action path deterministic after the strategic proposal.

## 2:10–2:25 — Viewer inspection structure

[Advance to slide 4.]

The Viewer presents the recorded path in three parts: the proposal context, the rule-verification result, and the executed state. I will now demonstrate how these remain linked to the replay frame.

## 2:25–5:10 — Software demonstration

[Switch to the replay viewer at `docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html`. Load the prepared replay if it is not already loaded.]

This is the replay interface in its default player view, where the board, match state, scores, units, timeline, and playback controls are primary. I will now open Inspection View. It removes secondary file controls, reserves the right column for the project-specific DTAV Inspector, and keeps the board visible. The three stages connect the recorded LLM proposal, deterministic checks, and the executed state.

[Click **Proposal attempt**. Point to the red proposal-status badge, decision source, and fallback reason.]

This historical Run008 frame records a proposal attempt, but the proposal was not admitted to execution because this replay used the force-rule-only configuration. The interface therefore labels it as rejected and shows that deterministic fallback supplied the action. It does not mislabel the proposal as valid.

[Click **Fallback checkpoint** and point to the three-stage flow.]

The second checkpoint shows the same control boundary later in the replay. The proposal context remains inspectable, the schema and fallback fields explain the verifier outcome, and the executed-state card reports what actually reached the environment.

[Click **Final frame**, then open **Final**.]

The evidence summary deliberately separates this qualitative replay from the formal experiments. It reports the primary matched-seed evaluation and the supplementary direct dual-LLM evaluation without presenting either as a general model ranking. The detailed risk-filter and normalisation counts are shown later from the aggregate reports.

[Briefly show the final result or match summary, then close it.]

The final score is retained, but it is only one part of the evidence. The framework also preserves decision provenance, verification outcomes, latency, fallback events, and replay linkage.

## 5:10–5:25 — Implementation boundaries

[Advance to slide 5.]

Three code boundaries make this control flow inspectable: the state summariser, the structured LLM decider, and the deterministic execution boundary in the agent.

## 5:25–6:35 — Selected source code

[Open `src/agent/state_summarizer.py` and show the function that constructs the compact state summary.]

The state summariser is responsible for reducing raw observations into stable strategic features. It extracts information such as the match phase, score context, unit positions and energy, known relics, candidate scoring locations, exploration state, and risk context. This bounds the information sent to the model and makes the prompt easier to inspect.

[Open `src/agent/llm_decider.py`. Show structured parsing and validation.]

The LLM decider requests structured intents and validates the returned schema. The formal experiments exposed an important distinction: post-check validity is not the same as raw schema validity. For Qwen, 520 responses required deterministic normalisation before use; those interventions are counted instead of being silently ignored.

[Open `src/agent/agent.py` or `src/agent/action_planner.py`. Show the verifier, risk-filter, or fallback call path.]

The agent and action planner then apply rule checks, caching, risk filtering, and fallback before constructing the action array expected by Lux. This is the main implementation boundary that prevents free-form model text from directly controlling the game.

## 6:35–8:25 — Empirical evaluation

[Advance to slide 6.]

The main experiment directly compares scheduled prompting with DTAV. Both conditions used Qwen3-32B, the same 50 seeds, role swapping, temperature, prompt budget, compact observation, and LLM-call schedule, producing 100 matches per method. Direct prompting won 48 matches and DTAV won 63. In the matched analysis, DTAV-only wins outnumbered direct-prompt-only wins 21 to 6. The McNemar exact p-value was 0.0059, and the paired-bootstrap interval estimated a DTAV advantage of 6 to 25 percentage points under this configuration.

The process evidence explains the observed limitation. Direct prompting produced usable structured calls 86.1% of the time and used the visible rule path on 95.5% of agent steps because strategy reuse was disabled. DTAV reached 99.9% post-check structured validity, reused an accepted strategy on 89.8% of steps, and recorded risk-filter changes on 11.2%. Both conditions retained complete traces and replay linkage, valid action-array shape, similar fresh-call latency, and no timeout, API error, or downstream action fallback.

The baseline still includes the minimum parser and legal-action adapter required by Lux, so it is not unrestricted text sent directly to the game. The comparison evaluates DTAV as a complete method bundle; it does not prove which individual component caused the difference or that DTAV is universally superior. Earlier Qwen, DeepSeek, and direct model-versus-model studies remain supporting evidence that the same inspection framework operates across controlled backends and simultaneous LLM players.

## 8:25–9:20 — Limitations and conclusion

[Advance to slide 7.]

There are several limitations. Operational traces show recorded provenance and interventions, but they are not a complete causal explanation of model reasoning. Zero action fallback in these runs does not prove that every possible future proposal is safe. The experiments use two local 32-billion-parameter models and a controlled Lux setup, so their outcome cannot be generalised to all models, games, or hardware. Viewer inspection is also a qualitative complement to, rather than a replacement for, quantitative measures.

In conclusion, the matched comparison shows that directly prompted LLM decisions remain possible through the minimum executable interface, but they are less usable and depend more heavily on rule fallback. Under the recorded configuration, DTAV improved structured-call validity, strategy continuity, and match outcomes while preserving a complete, inspectable path from proposal to action. The evaluation therefore considers not only whether an agent won, but whether its proposals were valid and how they were checked, changed, reused, or replaced. Thank you.

## Rehearsal rule

If the first complete rehearsal is longer than 9:40, shorten pauses and remove the second paragraph of the direct model-versus-model section. Do not speed-read and do not exceed 10:00.
