# CA2 Q&A preparation

Use these as concise answers, then open the named evidence if a marker asks for detail.

## 1. What is the original contribution?

The contribution is not a new general LLM or a claim of state-of-the-art Lux performance. It is an integrated inspection and evaluation framework that separates strategic LLM proposals from deterministic execution, records the provenance and verification path at every step, and links those records to replay inspection and controlled metrics.

Evidence to open: `docs/technical/system_architecture.md`, `src/agent/agent.py`, and the replay viewer.

## 2. Does the LLM directly control the units?

No. The model proposes structured high-level unit intents. The parser, schema checks, cache, risk filter, fallback logic, and action planner decide what can become an executable Lux action. This boundary is deliberate because fluent text is not equivalent to a legal or current action.

Evidence to open: `src/agent/llm_decider.py` and `src/agent/action_planner.py`.

## 3. What exactly does the verifier verify?

It verifies the structured form and allowed intents, applies deterministic normalisation where supported, checks target and risk conditions, and ensures the final action array has the required shape. The trace records whether the source was fresh LLM, cached LLM, or rule fallback, plus intervention reasons.

## 4. Does a trace explain the model's internal reasoning?

No. It records operational provenance: the summarised input, returned structured proposal, validation result, fallback or intervention, and executed action. This supports audit and debugging, but it is not a complete causal explanation of the model's internal computation.

## 5. Why use matched seeds and role swapping?

Lux outcomes can be affected by the environment seed and player role. Each seed is therefore used in paired matches with the LLM role swapped. The analysis reports role-specific outcomes and paired or seed-clustered statistics instead of treating every match as unrelated evidence.

## 6. What do the main empirical results show?

The primary evaluation completed 200 matches and produced 206,591 structured trace records. Step trace, call trace, and replay linkage were complete. All 4,591 fresh calls were valid after the recorded checks, including 520 Qwen responses that required deterministic normalisation. The risk filter also changed proposed targets on thousands of steps. These are framework and inspectability results; win rate is secondary.

Evidence to open: `reports/final_trace_evaluation.md`.

## 7. What does 100% post-check validity mean?

It does not mean every raw model output was perfect. It means every proposal admitted to the downstream planner was valid after the recorded parser and normalisation checks. Raw Qwen schema validity was 77.3%, and 520 responses required normalisation. The report deliberately separates raw validity from post-check validity.

## 8. Why run LLM-versus-LLM matches?

They were added as supplementary evidence after supervisor feedback. They show that the same tracing and verification framework can instrument two concurrent LLM-assisted agents under matched seeds and role swaps. They do not replace the main framework evaluation and are not presented as a general model leaderboard.

## 9. Did Qwen beat DeepSeek in the direct matches?

Qwen won 54 of 100 matches and DeepSeek won 46, but the seed-level sign-test p-value was approximately 0.503 and the interval includes parity. The correct conclusion is that no reliable difference was established in this controlled sample.

Evidence to open: `reports/dual_llm_trace_evaluation.md`.

## 10. Is the system formally safe?

No formal safety guarantee is claimed. The experiments observed complete action-array shape validity and no downstream action fallback, but that does not prove all possible future proposals are safe. The project provides deterministic checks, observable fallback, and evidence of behaviour under the recorded conditions.

## 11. How reproducible is the project?

The repository contains pinned or declared dependencies, environment setup instructions, smoke tests, unit tests, continuous integration, one-command experiment entry points, fixed seed policies, provenance metadata, and evidence validators. Large raw archives are managed outside GitHub with checksums, while analysed reports are stored in the repository.

Evidence to open: `docs/reproducibility_guide.md`, `scripts/setup.sh`, `.github/workflows/ci.yml`, and `tools/validate_project_evidence.py`.

## 12. Why not call the LLM at every step?

Repeated calls would add high latency and cost without necessarily improving short-horizon actions. A verified strategy cache allows the system to reuse recent strategic intent, while the trace makes this reuse explicit. In the formal primary runs, about 89.9% of LLM-agent steps used cached decisions.

## 13. What are the main limitations?

The evidence comes from one game environment, two local 32B backends, and controlled experiment settings. Traces are operational rather than complete causal explanations. The interface still requires qualitative human interpretation, and the empirical outcomes are not hardware-independent or universally generalisable.

## 14. What did you personally implement?

Answer this in the first person and be precise: identify your work on the state summariser, structured decision interface, verification and fallback path, trace schema, experiment runners, analysis tools, replay viewer, tests, and documentation. Do not claim third-party Lux or model implementations as your own.

## 15. What would you improve next?

I would add controlled ablations for individual verifier components, improve the viewer's guided comparison workflow, evaluate more model sizes and latency budgets, and test whether independent evaluators can reach consistent conclusions from the traces.
