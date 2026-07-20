# LuxLLM-Agent Project Closeout Standard

## Purpose

This document prevents unlimited project modification. Work stops when the
high-priority engineering and evidence criteria below are satisfied. Cosmetic
polish, additional models, larger repeated runs, leaderboard optimisation, and
new viewer features are outside this closeout.

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

## Explicit non-requirements

The following are not required to close the project:

- additional LLM backends;
- another repeated 50-run or 100-run experiment;
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
