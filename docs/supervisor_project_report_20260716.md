# LuxLLM-Agent Overall Project Progress Report

- **Project title:** LuxLLM-Agent: A Decision-Trace and Action-Verification Framework for Inspecting and Evaluating LLM-based Agents in Lux AI Season 3
- **Student:** Ze Wang
- **Institution:** University of Liverpool
- **Email:** Z.Wang300@liverpool.ac.uk
- **Supervisor:** Meng Fang
- **Repository:** https://github.com/zewang-liverpool/luxllm-agent-demo
- **Development branch:** `codex/dissertation-demo-finalization`
- **Report date:** 16 July 2026

## 1. Executive Summary

LuxLLM-Agent is an artefact-based MSc project investigating how an LLM can be integrated into a sequential game agent without allowing unconstrained model text to directly control executable actions. The project is organised around the following research question:

> How can structured decision tracing and rule-based action verification support the inspection and evaluation of LLM-based agents in Lux AI Season 3?

The implemented system treats the LLM as a bounded strategic planner. Raw Lux observations are summarised, the model proposes structured unit intents, deterministic code parses and normalises the response, a rule-based verifier applies safety and risk checks, and an action planner constructs legal Lux action arrays. The system records decision provenance and links it to replay state for later inspection.

The current technical scope is complete. Two formal 32B-model experiments produced 200 completed matched-seed, role-swapped matches and 206,591 structured trace records. All 4,591 LLM calls were valid after deterministic checks, all recorded action arrays had the expected shape, and no model timeout, API error, or downstream action fallback was observed. The project now has reproducible setup scripts, automated tests, continuous integration, evidence-consistency checks, a replay viewer, a backup demonstration video, and a finite closeout standard.

The main result is not a universal ranking of Qwen and DeepSeek. The main result is that structured traces and deterministic verification make model proposals observable, auditable, and executable under the recorded experimental conditions.

## 2. Project Objectives

The project has pursued seven objectives:

1. implement a working Lux AI Season 3 agent;
2. transform raw observations into structured strategic summaries;
3. integrate local LLM backends as high-level planners;
4. verify, normalise, cache, repair, or replace model proposals before execution;
5. record decision sources, verifier interventions, latency, errors, and outcomes;
6. evaluate multiple backends using controlled seeds and swapped player roles;
7. connect decision evidence to a visual replay interface.

All seven objectives have an implemented and tested artefact.

## 3. System Design

The principal execution path is:

```text
Lux observation
    -> structured state summary
    -> bounded LLM strategic proposal
    -> JSON parsing and deterministic normalization
    -> rule-based and risk-aware verification
    -> fallback or cached strategy when required
    -> deterministic action planning
    -> legal Lux action array
    -> decision trace, match evidence, and replay inspection
```

This separation is important because LLM output may be malformed, incomplete, stale, strategically weak, or too slow to request at every game step. The LLM therefore proposes intent, while deterministic code retains control of environment actions.

## 4. Main Technical Contributions

### 4.1 Structured state and intent interface

The agent converts low-level Lux observations into a compact state representation and constrains model responses to a finite set of strategic intents. This creates a stable interface between probabilistic model generation and deterministic game logic.

### 4.2 Rule-based action verification

Model proposals are checked and filtered before action construction. The verifier records whether a proposal was normalised, whether a risk condition was detected, how many proposed targets were changed, and why the intervention occurred.

### 4.3 Decision provenance

Every LLM-controlled agent step is classified as one of the following sources:

- fresh LLM decision;
- cached LLM strategy;
- rule fallback.

This prevents a final match result from being incorrectly attributed entirely to the LLM.

### 4.4 Replay-grounded inspection

The viewer connects replay state to step, match, score, model, decision source, fallback status, risk-filter status, and unit intents. It provides a worked qualitative example of how recorded traces can be inspected after a match.

### 4.5 Reproducible evaluation pipeline

The project includes:

- Windows and Linux setup scripts;
- dependency declarations and a verified lock file;
- unit, smoke, and end-to-end rule-only tests;
- a matched-seed role-swap experiment runner;
- Barkla2 Slurm support;
- statistical analysis and model-comparison tools;
- deterministic trace and verifier-audit tools;
- GitHub Actions continuous integration.

## 5. Formal Experimental Design

The primary experiment uses Qwen3-32B and DeepSeek-R1-32B served locally through Ollama on Barkla2 GPU resources.

For each backend:

- 50 Lux environment seeds were used;
- each seed was evaluated with the LLM as `player_0`;
- the same seed was evaluated with the LLM as `player_1`;
- 100 matches were therefore completed per backend;
- temperature was fixed at 0.0;
- seed, role, model, environment, Python, package, and Ollama metadata were retained.

This design is stronger than the earlier fixed-role experiments because it makes seed and player-role effects directly analysable.

## 6. Match Outcome Evidence

| Model | Matches | LLM wins | LLM losses | Win rate | Wilson 95% CI |
| --- | ---: | ---: | ---: | ---: | ---: |
| Qwen3-32B | 100 | 63 | 37 | 63% | 53.2%-71.8% |
| DeepSeek-R1-32B | 100 | 60 | 40 | 60% | 50.2%-69.1% |

Qwen won 29/50 matches as `player_0` and 34/50 as `player_1`. DeepSeek won 30/50 in each role.

The direct matched backend comparison covered 100 seed-role strata:

- Qwen-only wins: 14;
- DeepSeek-only wins: 11;
- mean Qwen-minus-DeepSeek outcome-score difference: 0.03;
- paired-bootstrap 95% interval: [-0.07, 0.13];
- McNemar exact p-value: 0.690.

The comparison does not provide evidence for a general model ranking. It demonstrates that the same framework can support controlled evaluation of both backends.

## 7. Primary Decision-Trace and Verification Evidence

| Metric | Qwen3-32B | DeepSeek-R1-32B |
| --- | ---: | ---: |
| Completed matches | 100 | 100 |
| Structured trace records | 103,286 | 103,305 |
| Agent-step trace completeness | 100% | 100% |
| LLM-call trace completeness | 100% | 100% |
| Replay-linkage coverage | 100% | 100% |
| LLM calls | 2,286 | 2,305 |
| Post-check valid LLM calls | 2,286 (100%) | 2,305 (100%) |
| Raw schema-valid calls | 1,766 (77.3%) | 2,305 (100%) |
| Deterministic normalizations | 520 | 0 |
| Cached-decision steps | 45,399 | 45,380 |
| Observable rule-fallback steps | 2,815 | 2,815 |
| Risk-filter changed steps | 5,590 | 7,090 |
| Risk-filter changed targets | 31,128 | 34,379 |
| Action-array shape validity | 100% | 100% |
| LLM timeouts / API errors | 0 / 0 | 0 / 0 |
| Downstream action fallback steps | 0 | 0 |

These results address the research question more directly than win rate:

- trace completeness supports post-match inspection;
- replay linkage connects decisions to state and outcome context;
- raw-schema and normalization metrics expose model-format weaknesses;
- risk-filter metrics show that deterministic verification changed proposed targets;
- action-shape and completion metrics show executable behaviour in the observed runs.

## 8. Direct Verifier Intervention Audit

An additional deterministic offline audit was run over the retained formal logs without making new model calls.

### 8.1 Normalization

All 520 Qwen normalization events were string-intent shorthand responses. Without the implemented normalization path, these 520 calls would fail the strict raw object schema. All were valid after deterministic normalization. No corresponding normalization was required for DeepSeek in the formal run.

### 8.2 Risk filtering

| Model | Changed steps | Changed targets | Mean targets changed per affected step |
| --- | ---: | ---: | ---: |
| Qwen3-32B | 5,590 | 31,128 | 5.57 |
| DeepSeek-R1-32B | 7,090 | 34,379 | 4.85 |

Most interventions occurred while cached model strategies were active:

- Qwen cached-strategy intervention steps: 5,153;
- DeepSeek cached-strategy intervention steps: 6,569.

Every affected step retained the recorded reason that the original target was inside the visible-enemy risk radius and a safer target was selected.

This demonstrates that the verifier was operational. It does not prove that every individual intervention improved the final score, and the project explicitly avoids that causal claim.

## 9. Reproducibility and Software Quality

Previous reproducibility weaknesses have been addressed:

- complete runtime source is tracked under `src/agent/`;
- dependency files and a verified Windows lock file are included;
- setup scripts can rebuild a stale `.venv` referencing a removed Python installation;
- 23 automated tests pass;
- the dependency-free smoke runner compiles source, validates viewer data, checks evidence consistency, and runs the tests;
- a real rule-only Lux match completes successfully at seed 42;
- GitHub Actions tests Python 3.10 and 3.11;
- CI now deliberately creates a broken Linux virtual environment and verifies that `setup.sh` repairs it;
- formal evidence and verifier-audit metrics are checked mechanically for agreement;
- obsolete claims such as “Barkla experiment pending” or “roles were not swapped” are rejected by the consistency validator.

The two transferred experiment archives have also been verified locally:

```text
Qwen SHA-256:
C25D30A0B4CD826EFF0A4F28F26457DA03352FA6E164F62A7973646A08ED277D

DeepSeek SHA-256:
285BFEAF7D1725EB2A619D60D6BACE3924ED260E11D9CB969D50F5EE5779C180
```

## 10. Demonstration and Supporting Artefacts

The project provides:

- a replay-grounded HTML viewer;
- Run008 trace-overlay data;
- a verified 75.33-second H.264/AAC backup video;
- evaluation figures and machine-readable reports;
- a timed 7-10 minute demonstration runbook;
- a final manual acceptance checklist;
- a reproducibility guide;
- a finite project closeout standard.

The formal 32B models do not need to be run live during a presentation. The viewer, recorded evidence, reports, and backup video provide a lower-risk demonstration path.

## 11. Limitations

The project retains several explicitly reported limitations:

1. only two 32B reasoning-oriented backends were evaluated;
2. both models were tested against one rule-based opponent;
3. results are specific to the recorded prompt, verifier, quantisation, Lux version, and environment configuration;
4. the system is hybrid, so match outcomes cannot be attributed solely to the LLM;
5. the viewer provides one detailed replay case rather than a formal human-user study;
6. hardware affects model latency;
7. recorded interventions demonstrate verifier operation, not causal improvement in match outcome;
8. zero observed downstream action fallback is not proof of safety for every possible future model output.

These limitations define the project scope and avoid overstating the results.

## 12. Current Completion Status

The project has reached technical closeout for the agreed MSc scope:

- core implementation: complete;
- real-model formal experiments: complete;
- matched role-swap evaluation: complete;
- trace and verifier evidence: complete;
- reproducibility hardening: complete;
- automated tests and CI: complete;
- viewer and demonstration package: complete;
- technical documentation: complete;
- project closeout standard: complete.

Further development is not planned unless a test fails, a factual inconsistency is identified, the supervisor requests a material correction, or a submission-blocking defect is discovered.

## 13. Remaining Non-development Work

The remaining work is review and presentation rather than feature development:

1. obtain supervisor feedback on the argument and limitations;
2. perform the final manual acceptance checklist;
3. rehearse the demonstration and questions;
4. verify the public GitHub release link for the video if required;
5. keep large raw runs and archives outside normal Git history;
6. merge the finalisation branch after GitHub CI passes.

## 14. Questions for Supervisor Feedback

The following points would benefit most from supervisor guidance:

1. Is the research question sufficiently answered by the combination of trace completeness, replay linkage, normalization evidence, and recorded verifier intervention?
2. Is the boundary between operational verifier evidence and causal performance claims sufficiently clear?
3. Is the matched-seed, role-swapped evaluation adequate for the MSc scope?
4. Should the historical fixed-role experiments remain as supporting development history, or be omitted from the final narrative?
5. Is the current limitation discussion appropriately critical and proportionate?

## 15. Conclusion

LuxLLM-Agent demonstrates a practical architecture for integrating local LLM planning into a sequential game agent while retaining deterministic control of executable actions. Its main contribution is a reproducible evidence framework: structured decision provenance makes behaviour inspectable, normalization exposes and repairs bounded output-format failures, risk-aware verification records changes to unsafe targets, and replay linkage connects decisions to game context.

The project therefore answers the research question at an operational artefact level. Structured decision tracing supports inspection and evaluation by preserving decision source and state context, while rule-based verification supports reliable execution by mediating between model proposals and legal actions.

---

## Suggested Three-minute Oral Summary

> My project is LuxLLM-Agent, a framework for inspecting and evaluating LLM-based agents in Lux AI Season 3. The central problem is that an LLM response should not be treated as an executable game action. The model can produce useful strategy, but its output may be malformed, stale, slow, or unsafe in the current state.
>
> I therefore use the LLM only as a bounded strategic planner. The system summarises the Lux state, requests structured unit intents, checks and normalises the response, applies rule-based risk verification, constructs legal actions deterministically, and records the complete decision provenance for replay inspection.
>
> I evaluated Qwen3-32B and DeepSeek-R1-32B using 50 matched seeds with role swapping, giving 100 matches per model and 200 matches overall. All matches completed. The evaluation produced 206,591 trace records and 4,591 valid post-check LLM calls. Trace completeness, replay linkage, and action-array shape validity were all 100%. Qwen required 520 deterministic normalizations. The risk filter changed more than 31,000 Qwen targets and 34,000 DeepSeek targets when proposed locations were inside the visible-enemy risk radius.
>
> Qwen won 63 matches and DeepSeek won 60, but the matched comparison was not statistically significant, so I do not claim that one model is generally better. The main conclusion is that structured traces make LLM-agent behaviour auditable, while rule-based verification creates a controlled boundary between model proposals and executable actions.
>
> The implementation, experiments, automated tests, CI, replay viewer, evidence audit, and reproducibility workflow are now technically complete. The remaining work is supervisor review, demonstration rehearsal, and final acceptance rather than further feature development.
