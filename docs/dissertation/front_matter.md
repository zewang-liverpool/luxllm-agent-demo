# LuxLLM-Agent: A Decision-Trace and Action-Verification Framework for Inspecting and Evaluating LLM-based Agents in Lux AI Season 3

**Author:** Ze Wang

**Institution:** University of Liverpool

**Email:** Z.Wang300@liverpool.ac.uk

**Project:** COMP702 Final-Year Project

**Date:** July 2026

---

## Abstract

Large language models can provide high-level planning in sequential environments, but their outputs are not automatically valid, timely, or attributable to executable actions. This dissertation presents LuxLLM-Agent, a decision-trace and action-verification framework for inspecting and evaluating LLM-based agents in Lux AI Season 3. The framework converts raw observations into structured summaries, constrains model responses to bounded strategic intents, applies deterministic normalization and rule-based checks, constructs legal action arrays, records decision provenance, and links execution evidence to replay state.

The primary evaluation uses 50 matched Lux environment seeds with role swapping for each of two local 32B backends, Qwen3 and DeepSeek-R1, producing 200 completed matches. Across 206,591 structured trace records, agent-step and LLM-call field completeness, replay linkage, and action-array shape validity were all 100%. All 4,591 LLM calls were valid after deterministic checks; 520 Qwen responses required normalization. Risk filtering changed proposed targets on 5,590 Qwen steps and 7,090 DeepSeek steps. No LLM timeout, API error, or downstream action fallback was observed in the formal runs. Qwen won 63/100 matches and DeepSeek won 60/100, but their matched outcome difference was not statistically supported.

The results show that structured traces make decision source and verifier intervention auditable, while rule-based verification provides a controlled boundary between model proposals and environment actions. The project does not claim a universal model ranking or leaderboard-level policy. Its contribution is a reproducible framework and evidence pipeline for examining how LLM-supported decisions are produced, checked, executed, and inspected.

**Keywords:** LLM agents; decision tracing; action verification; reproducibility; Lux AI Season 3; replay inspection

---
