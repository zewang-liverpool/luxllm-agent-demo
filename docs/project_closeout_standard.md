# LuxLLM-Agent Project Closeout Standard

## Purpose

This document prevents unlimited project modification. Work stops when the
high-priority engineering and evidence criteria below are satisfied. The
14 August supervisor feedback adds one bounded comparison--direct prompting
versus DTAV--but does not reopen unlimited model, experiment, or UI expansion.

## Required stopping criteria

The project is considered technically closed when all of the following hold:

1. **Clean-environment recovery**
   - Windows and Linux setup scripts create a supported Python environment.
   - A broken or stale `.venv` is detected and rebuilt automatically.
   - The dependency-free smoke test passes from the selected environment.

2. **Automated verification**
   - All repository unit tests pass.
   - Python sources compile.
   - Demo replay and trace inputs load.
   - Git diff whitespace checks pass.

3. **Formal evidence completeness**
   - Both 100-match formal experiment directories are locally retained.
   - Their compact tracked report records 200 completed matches.
   - The supervisor-requested 100-match direct dual-LLM archive is locally
     retained and its tracked supplementary reports regenerate from raw logs.
   - Trace coverage, LLM-call validity, replay linkage, normalization,
     risk-filter intervention, action shape, timeout, and error metrics are
     reproducibly generated from the raw logs.

4. **Direct verifier evidence**
   - A deterministic offline audit reports which model responses required
     normalization.
   - It reports risk-filter interventions by model, decision source, phase,
     reason, and changed-target count.
   - It clearly distinguishes observed intervention from causal performance
     improvement.

5. **Evidence consistency**
   - Canonical project documents use the matched-seed, role-swapped formal
     experiment as primary evidence.
   - Historical fixed-role results are labelled as historical.
   - Known obsolete claims are rejected by an automated consistency check.

6. **Supervisor-requested supplementary scope**
   - Direct Qwen-versus-DeepSeek play is complete for 50 matched seeds with
     role swapping.
   - The result is reported as evidence of simultaneous tracing and
     verification, not as a universal model ranking.
   - No additional GPU experiment is required unless a retained result fails
     validation or the supervisor identifies a specific missing comparison.

7. **Direct-prompting comparison requested on 14 August 2026**
   - The repository exposes `dtav` and `direct_prompt` through the same paired
     runner and records the method in environment, match, call, and step logs.
   - Local unit, mock-LLM, smoke, and consistency tests pass.
   - One matched formal comparison is run with the same source commit, model,
     seeds, roles, temperature, generation budget, and call schedule.
   - Reporting distinguishes the unavoidable Lux action adapter/fallback from
     DTAV's normalisation, strategy reuse, and risk-aware filtering.
   - Development stops after the formal comparison is validated and integrated;
     extra models remain optional rather than required.

## Closure determination: 18 August 2026

The direct-prompt and DTAV formal jobs each completed 100 matches across 50
matched role-swapped seeds from source commit
`354c30beb1a179904fc52b53a577fe09c0fbfdf1`. Both result directories passed
`tools/validate_paired_method_result.py`; the automated paired comparison and
trace analysis completed; and the raw archive was transferred and verified by
SHA-256. The bounded experimental requirement is therefore closed. No further
GPU experiment is required for CA2 unless a retained result fails validation
or a supervisor identifies a specific factual gap.

## Explicit non-requirements

The following are not required to close the project:

- additional LLM backends;
- repeated experiments beyond the single direct-prompt versus DTAV comparison;
- live 32B inference during the demonstration;
- a leaderboard-level Lux policy;
- a formal human-subject user study;
- proof that every possible LLM proposal is safe;
- conversion into a university dissertation template.

## Reopening rule

After all required criteria pass, further code changes require one of:

- a failing test or reproducibility check;
- a supervisor-identified factual error;
- a material mismatch between tracked evidence and a reported claim;
- a submission-blocking defect.

Otherwise, the correct next action is submission preparation, not additional
development.
