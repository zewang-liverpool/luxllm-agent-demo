# Current Research Scope (Supervisor Feedback Integrated)

Updated: 14 August 2026

## Project title

**LuxLLM-Agent: A Decision-Trace and Action-Verification Method for LLM Decision-Making in Lux AI Season 3**

## Central research question

> How effectively can directly prompted LLMs make decisions in a partially observable, multi-agent, long-horizon, and rule-constrained strategy game such as Lux AI Season 3, and how can the project-specific Decision-Trace and Action-Verification (DTAV) method address the observed limitations?

## Why this game is a useful test case

Lux AI Season 3 requires an agent to act with incomplete observations, control
multiple units, retain useful state over a long sequence, compete with another
agent, and continually produce actions that satisfy an exact environment
schema. It is an adversarial multi-agent strategy game, not a social-deduction
or human-interaction study. These properties make direct LLM prompting
challenging and give the project a bounded problem setting.

## Project aim

To design and evaluate an LLM-based decision method that helps an agent operate
reliably in Lux AI Season 3 while making the route from observation to proposal,
verification, executed action, and replay outcome inspectable.

## Three research objectives

1. Establish a controlled direct-prompting baseline using compact Lux
   observations, the same model settings, matched seeds, role swapping, and a
   minimal action adapter.
2. Implement the project-specific DTAV method, in which LLM proposals can be
   normalised, reused, checked, filtered, or replaced before legal Lux actions
   are constructed.
3. Compare the baseline and DTAV using action validity, fallback and
   intervention rates, reliability, latency, match outcomes, and replay-linked
   inspection evidence.

## Terminology boundary

"Decision-Trace and Action-Verification (DTAV)" is the name of the method
developed in this project. "Structured decision tracing" must not be presented
as an established research term. The recorded trace is a predefined operational
audit record--not the model's hidden chain of thought--and links:

```text
game observation -> LLM proposal -> deterministic checks/modifications
-> executed action -> replay state and outcome
```

## Experimental comparison

The direct-prompt condition and DTAV condition use the same compact observation,
model, temperature, seed, role-swap protocol, and LLM call schedule. Direct
prompting disables output normalisation, strategy reuse, and risk-aware target
filtering. A minimal parser, official action adapter, and deterministic fallback
remain necessary to keep the Lux runner executable; their use is logged rather
than hidden.

Existing Qwen-versus-rule, DeepSeek-versus-rule, and Qwen-versus-DeepSeek results
remain supporting evidence. They do not substitute for the new direct-prompt
versus DTAV comparison and are not used to claim a universal model ranking.
