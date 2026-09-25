# Changelog

## 2.2.0

- Made the smoke test repeatable with fixed good/bad source fixtures and a linked three-round audit chain.
- Required an evidence and result row for every Auditor acceptance criterion.
- Added a Builder stop rule for packets too large to include completely.
- Aligned the audit-report task ID pattern with the handoff schema and prohibited round-1 regression rows.
- Extended protocol validation for fixed example chains, not-verifiable findings, closed-ID reuse, and monotonic new finding IDs.

## 2.1.0

- Corrected the Auditor starter so it asks for complete current source; the diff is supplemental.
- Added explicit handling for conflicts among the request, acceptance criteria, standards, source, and prior reports.
- Tightened rework stop conditions so each `must_fix` ID has one observable check.
- Extended the validator to accept generated handoffs and reports, check prior-report chains, and track unresolved rework IDs.
- Added smoke-test scenarios for stale snapshots, round mismatches, missing context, and embedded instructions.

## 2.0.0

- Replaced the Auditor's assumed-defect posture with evidence-first adversarial review.
- Separated build revision from audit round and fixed the cap at three audits total.
- Distinguished execution environment and verification evidence from code-defect severity.
- Required complete current source/context in every audit packet and fixed fresh-conversation rework state.
- Added explicit trust boundaries for untrusted source artifacts and prompt-injection attempts.
- Defined PASS as limited to supplied scope, not as CI/merge approval.
- Added JSON Schemas, a calibrated good/bad smoke test, and consistent package paths.
