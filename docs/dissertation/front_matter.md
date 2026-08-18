# LuxLLM-Agent: A Decision-Trace and Action-Verification Method for LLM Decision-Making in Lux AI Season 3

**Author:** Ze Wang

**Student ID:** 201868809

**Institution:** University of Liverpool

**Email:** Z.Wang300@liverpool.ac.uk

**Supervisor:** Meng Fang

**Project:** COMP702 MSc Project

**Date:** July 2026

---

## Abstract

Large language models can provide high-level planning in sequential environments, but their outputs are not automatically valid, timely, or attributable to executable actions. This dissertation asks how effectively directly prompted LLMs can make decisions in Lux AI Season 3, a partially observable, adversarial multi-agent, long-horizon, and rule-constrained strategy game. It presents the project-specific Decision-Trace and Action-Verification (DTAV) method, which converts raw observations into compact summaries, constrains model responses to bounded strategic intents, applies deterministic normalisation and rule-based checks, constructs legal action arrays, records operational provenance, and links execution evidence to replay state. DTAV is a name introduced for the method in this project; its trace is a predefined audit record rather than hidden model chain of thought.

The primary evaluation uses 50 matched Lux environment seeds with role swapping for each of two local 32B backends, Qwen3 and DeepSeek-R1, producing 200 completed matches. Across 206,591 structured trace records, agent-step and LLM-call field completeness, replay linkage, and action-array shape validity were all 100%. All 4,591 LLM calls were valid after deterministic checks; 520 Qwen responses required normalization. Risk filtering changed proposed targets on 5,590 Qwen steps and 7,090 DeepSeek steps. No LLM timeout, API error, or downstream action fallback was observed in the formal runs. Qwen won 63/100 matches and DeepSeek won 60/100, but their matched outcome difference was not statistically supported. A supplementary direct Qwen-versus-DeepSeek experiment completed a further 100 role-swapped matches while both players used the framework; its complete traces and observable verifier interventions demonstrate simultaneous two-sided inspection without turning the study into a model-ranking exercise.

The results show that structured traces make decision source and verifier intervention auditable, while rule-based verification provides a controlled boundary between model proposals and environment actions. The project does not claim a universal model ranking or leaderboard-level policy. Its contribution is a reproducible framework and evidence pipeline for examining how LLM-supported decisions are produced, checked, executed, and inspected.

**Keywords:** LLM agents; decision tracing; action verification; reproducibility; Lux AI Season 3; replay inspection

---
