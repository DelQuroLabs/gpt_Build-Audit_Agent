# Confirmed code-review repairs - 3.2.1

Date: 2026-09-27. Applies to full and lean editions. All five are FIXED by the same implementation and tests. Prior code-review priorities are retained; the prompt rubric classifies each as MAJOR because valid workflow paths could produce materially wrong or unusable results. This is not live-model certification.

## R1 - Active reopened blocker lost into PASS

Priority: High/P1. Location: tools/validate_examples.py, protocol_errors, prior_closed and history transitions. Original location: line 223 in 3.2.0.

Observed before repair: round 1 F1 FAIL -> round 2 F1 active/reopened FAIL -> round 3 empty PASS with F1 not_verifiable was accepted. Root cause: every reopened row was treated as closed, even when its ID was still active. Impact: unresolved blocker could vanish without repair or accepted risk.

Repair: only frozen history or a prior fixed row establishes closure. Continuing reopened findings remain active until fixed or explicitly overruled. Previously closed IDs still require a fresh, higher ID for a new regression.

Replacement contract text: "reopened alone does not close an active ID." Implementation: removed reopened from the prior_closed status set.

Verification: test_reopened_active_finding_cannot_disappear_into_pass rejects the reproduced false PASS; test_active_reopened_transition_matrix checks retained/omitted IDs against all four statuses; test_closed_history_and_new_regression_remain_distinct preserves fresh-ID behavior. All passed in both editions. Effort: M. No dependent live behavior claimed.

## R2 - Last human override could not close consistently

Priority: Medium/P2. Location: tools/validate_examples.py, _is_overrule and protocol_errors; contract.md, Complete finding history. Original location: line 249.

Observed before repair: PASS with an accepted-risk decision and null rework_brief was rejected; adding the prescribed frozen record violated the PASS schema. Root cause: the validator recognized decisions only in a FAIL-only brief. Impact: the documented human-acceptance path could not close the last finding or work consistently on final FAIL.

Repair: not_verifiable regression evidence can hold the full human-overruled decision when the brief is null. Continuing FAIL also freezes the decision; older FAIL packets with the full record only in frozen remain accepted. Reject empty prefixes, technical-fix labeling of accepted risk, and accepted-risk IDs still active. Preserve prior decision disclosure on later not-verifiable rows.

Replacement contract: record human-overruled: in regression evidence with supplied decision, rationale, owner, review/expiry date, and an explicit not-a-technical-fix statement. Null-brief verdicts remain null; no schema field was added. The validator cannot authenticate human approval or determine whether prose evidence is true; a prefix is never authority to invent approval.

Verification: last finding closes at rounds 2/3; PASS_WITH_NOTES with another minor and final FAIL with another blocker work; empty/mislabeled/active overrides and lost disclosure are rejected. Legacy frozen-only acceptance remains covered by test_explicit_human_overrule_is_not_marked_fixed. All passed. Effort: M.

## R3 - Conflicting operations for one artifact accepted

Priority: Medium/P2. Location: tools/validate_examples.py, handoff_protocol_errors and CLI dispatch; contract.md, Builder JSON. Original dispatch location: line 362.

Observed before repair: the same path appeared as new/snapshot true and deleted/snapshot false; the CLI accepted both. Root cause: handoffs had schema checks but no artifact-identity semantic check. Impact: consumers had to guess which operation applied.

Repair: require exactly one artifact row per unique canonical repository-relative path. Reject absolute/drive/backslash paths, empty components, dot/dot-dot aliases, and directory-style paths. Validation never accesses submitted paths; actual case/symlink equivalence still needs repository review.

Replacement contract: "A file has one operation, never simultaneous new/modified/deleted entries."

Verification: conflicting and identical duplicates are rejected; nine ambiguous path forms are rejected; a unique nested path with a space remains accepted. The historical self-audit/build-handoff.v2.json used prompts/ as an artifact; it is preserved unchanged as an expected rejection, not silently exempted or rewritten. All passed. Effort: S.

## R4 - Schema-valid long ID crashed the validator

Priority: Medium/P2. Location: tools/validate_examples.py, _id_order and monotonic-ID comparison. Original location: _number, line 114.

Observed before repair: F followed by 5,000 digits passed the string schema but raised an uncaught Python integer-conversion ValueError. Root cause: unbounded protocol strings were converted to bounded decimal integers. Impact: a valid report produced a traceback rather than validation.

Repair: compare positive decimal digit strings by length and then lexical order. Do not disable Python's integer-conversion protection or narrow the v2 schema to hide the crash.

Replacement implementation: return (len(digits), digits) from _id_order; use this key consistently for historical maxima and new-ID ordering.

Verification: the 5,000-digit prior ID closes through the CLI without traceback; F9 -> F10 allocation passes and F9 -> F8 is rejected; very long magnitudes sort correctly. All passed. Effort: S.

## R5 - Integral JSON floats rejected in history

Priority: Medium/P2. Location: tools/validate_examples.py, _is_integer and continuity checks. Original location: line 207.

Observed before repair: prior audit_round 1.0/build_revision 0.0 passed JSON Schema but failed Python exact-int history checks. Root cause: semantic validation used a narrower type definition than its schema. Impact: legitimate generated JSON was unusable in rework.

Repair: use Draft202012Validator.TYPE_CHECKER for integer semantics. Preserve strict rejection of booleans and fractional numbers.

Replacement contract: "Whole-number JSON values such as 1 and 1.0 have the same schema meaning for rounds/revisions; booleans and fractional values do not."

Verification: integral previous and current round/revision numbers pass the CLI; True and 1.5 remain rejected before semantic history validation. All passed. Effort: S.

## Release evidence and limits

Both editions pass 43 unit tests, including 20 new tests with parameterized CLI cases. The example suite accepts 11 positive objects and rejects seven designated negatives. Sources and generated prompts agree. Full/lean Python files are identical; schemas are structurally identical.

No live model, host setup, external integration, older Python, or second operating system was tested. See PROMPT-AUDIT.md for the weighted 96/100 assessment and scope. The old 3.2.0 ZIPs are superseded by 3.2.1, not silently updated in place.
