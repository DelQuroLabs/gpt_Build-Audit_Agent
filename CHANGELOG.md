# Changelog

## 3.2.2-gpt-profile

- Fixed three re-audit defects: trailing-newline identifiers, fractional values rounded into integers, and NUL artifact paths.
- Added 17 input-boundary regression tests; all 60 tests pass in both editions. The earlier five repairs remain covered.
- Enforced whole-string schema patterns, exact decimal JSON decoding with explicit resource limits, and NUL rejection without filesystem access.
- Preserved v2 field shapes, valid integral numeric spellings, and long string finding IDs. Numeric input limits are documented in contract.md and schemas/README.md.
- Superseded the 3.2.1 clean assessment; retained its audit as history and corrected stale setup/fixture guidance. Current scope and results are in docs/PROMPT-AUDIT.md.

## 3.2.1-gpt-profile

- Fixed all five confirmed 3.2.0 code-review findings in the validator; added 20 regression tests for a total of 43.
- Distinguished active reopened defects from closed history; final accepted-risk decisions now fit null-brief reports without being labeled technical fixes.
- Enforced unique canonical artifact paths, compared arbitrarily long decimal IDs without integer conversion, and accepted schema-valid integral JSON numbers.
- Kept v2 schema shapes. Clarified semantic compatibility and preserved the historical folder-artifact packet as an expected rejection instead of rewriting its evidence.
- Retained the old audit as superseded history; current evidence and scope are in docs/PROMPT-AUDIT.md and docs/CODE-REVIEW-FIXES.md.

## 3.2.0-gpt-profile

- Defined early response states, required references, explicit tool budgets, and no-tool behavior.
- Aligned full finding history, frozen states, new regression IDs, and Builder/Auditor ownership across prompts, contract, validator, and examples.
- Added complete generated installation prompts with shared specialist controls and a conservative size budget.
- Added fixed GPT calibration packets, manual behavioral cases, and executable validator regressions.
- Hardened JSON parsing; tools default off. Retained v2 field shapes with stricter history validation.
- See docs/PROMPT-AUDIT-3.2.0.md for this historical audit; its clean conclusion was superseded by the code review.

## 3.1.0-gpt-profile

- Integrated the value-gated specialist extension as optional, advisory-only profiles; the Builder/Auditor protocol remains v2.
- Added same-task/revision specialist handling, schema validation, cross-field checks, and promotion fixtures.
- Clarified package integration, trigger discipline, and the limits of the available verification evidence.

## 3.0.0-gpt-profile

- Applied the upstream v2.2.0 Build ↔ Audit protocol to GPT design artifacts, not only code patches.
- Added Builder gates for capability/platform fit, Knowledge governance, Actions/data flows, output contracts, uncertainty, and live-verification limits.
- Added Auditor attack cases for retrieved-content injection, tool failure, privacy, consequential actions, unsupported capability claims, and output-format collisions.
- Added GPT-specific kickoff and rework templates, standards, configuration, and a self-application record.
- Kept protocol objects and JSON Schemas at version 2 for interoperability.

## 2.2.0 upstream base

- Made the smoke test repeatable with fixed good/bad source fixtures and a linked three-round audit chain.
- Required an evidence and result row for every Auditor acceptance criterion.
- Added a Builder stop rule for packets too large to include completely.
- Aligned the audit-report task ID pattern with the handoff schema and prohibited round-1 regression rows.
- Extended protocol validation for fixed example chains, not-verifiable findings, closed-ID reuse, and monotonic new finding IDs.

## 2.1.0 upstream base

- Corrected the Auditor starter so it asks for complete current source; the diff is supplemental.
- Added explicit handling for conflicts among the request, acceptance criteria, standards, source, and prior reports.
- Tightened rework stop conditions so each `must_fix` ID has one observable check.
- Extended the validator to accept generated handoffs and reports, check prior-report chains, and track unresolved rework IDs.

## 2.0.0 upstream base

- Replaced the Auditor's assumed-defect posture with evidence-first adversarial review.
- Separated build revision from audit round and fixed the cap at three audits total.
- Distinguished execution environment and verification evidence from code-defect severity.
- Required complete current source/context in every audit packet and fixed fresh-conversation rework state.
- Added explicit trust boundaries for untrusted source artifacts and prompt-injection attempts.
- Defined PASS as limited to supplied scope, not as CI/merge approval.
- Added JSON Schemas, a calibrated good/bad smoke test, and consistent package paths.
