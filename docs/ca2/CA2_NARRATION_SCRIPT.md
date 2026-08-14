# CA2 video narration script

Target duration: **9:20**. Hard rehearsal limit: **9:40**. The final submitted video must remain below 10:00.

The spoken text is written in natural presentation English. Text in square brackets is a screen action and is not spoken.

## 0:00–0:35 — Title and ethical compliance

[Show slide 1.]

Hello. My name is Ze Wang, and this is my COMP702 project, LuxLLM-Agent: a decision-trace and action-verification framework for inspecting and evaluating LLM-based agents in Lux AI Season 3. My supervisor is Dr Meng Fang.

The project uses no human participants and no personal data. It runs only in a game-AI environment, and I have followed the University's ethical guidance. The confirmed data and participant category codes are shown on this title slide.

## 0:35–1:35 — Problem, motivation, and research question

[Advance to slide 2.]

Large language models can propose useful high-level game strategies, but a fluent proposal is not necessarily valid, current, safe to execute, or easy to inspect. A simple win rate cannot explain whether an action came from a fresh LLM response, a cached strategy, a deterministic fallback, or a verifier intervention.

This motivated my main research question: How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

The central goal is therefore not to claim the strongest Lux game-playing bot or to rank general-purpose language models. It is to build an inspectable hybrid pipeline in which the LLM proposes strategy while deterministic code retains execution control and records evidence about what happened.

## 1:35–2:10 — Design and contribution

[Advance to slide 3.]

The framework has three broad stages. First, the state summariser converts the raw observation and retained game memory into a compact, structured prompt. Second, the LLM response is parsed, schema-checked, normalised when possible, cached when appropriate, and filtered using deterministic game rules. Invalid or unavailable proposals can be replaced by an observable rule-based fallback. Third, the action planner constructs legal Lux actions and writes per-step provenance, verification, timing, score, and replay-link fields.

The important design boundary is that the LLM never sends arbitrary actions directly to the environment. This separation makes failures visible and keeps the final action path deterministic after the strategic proposal.

## 2:10–2:25 — Viewer inspection structure

[Advance to slide 4.]

The Viewer presents the recorded path in three parts: the proposal context, the rule-verification result, and the executed state. I will now demonstrate how these remain linked to the replay frame.

## 2:25–5:10 — Software demonstration

[Switch to the replay viewer at `docs/viewers/s3_isometric_battle_viewer_v09n12d_trace_overlay.html`. Load the prepared replay if it is not already loaded.]

This is the replay-grounded inspection interface. Presentation Mode removes file and timeline controls from the recording view, reserves the right column for the Decision-to-Action Inspector, and keeps the Lux AI Season 3 board visible. The three stages connect recorded decision context, deterministic verification, and the executed state.

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

I evaluated the framework in two controlled settings. In the primary evaluation, Qwen3-32B and DeepSeek-R1-32B each played 100 matches against the same rule-based opponent, using 50 matched seeds with the LLM role swapped. All 200 matches completed. The runs produced 206,591 structured trace records, with complete step traces, LLM-call traces, and replay linkage.

Across the primary runs, all 4,591 fresh calls were valid after the recorded checks. Qwen had 520 normalisation interventions, while DeepSeek had none. The risk filter changed proposed targets on 5,590 Qwen steps and 7,090 DeepSeek steps. There were no LLM timeouts, API errors, action fallbacks, or invalid action-array shapes in these formal runs. These results show that the framework can expose both successful proposal flow and deterministic interventions.

Following my supervisor's suggestion, I also ran direct model-versus-model matches as supplementary evidence. A Qwen-assisted agent and a DeepSeek-assisted agent played 100 matches over 50 matched seeds with roles swapped. Qwen won 54 and DeepSeek won 46; the seed-level sign-test p-value was approximately 0.503, so this is not evidence of a general model ranking. More importantly for the research question, all 4,676 fresh calls were valid after checks and the experiment produced 106,317 complete structured traces while both sides used the same tracing and verification framework.

## 8:25–9:20 — Limitations and conclusion

[Advance to slide 7.]

There are several limitations. Operational traces show recorded provenance and interventions, but they are not a complete causal explanation of model reasoning. Zero action fallback in these runs does not prove that every possible future proposal is safe. The experiments use two local 32-billion-parameter models and a controlled Lux setup, so their outcome cannot be generalised to all models, games, or hardware. Viewer inspection is also a qualitative complement to, rather than a replacement for, quantitative measures.

In conclusion, LuxLLM-Agent answers the research question by combining three forms of evidence: structured per-step decision provenance, deterministic verification before execution, and replay-grounded inspection. This makes it possible to evaluate not only whether an LLM-based agent won, but how its proposals were checked, changed, reused, or replaced. Thank you.

## Rehearsal rule

If the first complete rehearsal is longer than 9:40, shorten pauses and remove the second paragraph of the direct model-versus-model section. Do not speed-read and do not exceed 10:00.
