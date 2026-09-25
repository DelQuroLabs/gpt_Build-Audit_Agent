# Smoke test — verify both correctness and calibration

Run these with the Code Builder and Code Auditor before real work. Include the contract/schema and a handoff-like context in the Auditor prompt.

## 1. Builder output format

Ask the Builder:

> Implement `moving_average(values, window)` in plain Python. It returns the arithmetic mean of each complete sliding window, including the final valid window. For an empty input and a positive window, return `[]`. A window larger than the input returns `[]`. Require `window` to be a positive non-boolean integer; raise `ValueError` otherwise. No dependencies. Include tests for each criterion and a v2 handoff.

Check that it gives a complete current source file, a genuine verification report (or honest `not-run`), and a valid-shaped `build-audit-handoff` with `build_revision: 0`. It may correctly state that it cannot run project CI.

## 2. Good-sample audit

Use the fixed spec and implementation in `examples/fixtures/moving-average-calibration.md` and `examples/fixtures/moving-average-good.py`. The Auditor should be able to return PASS or PASS_WITH_NOTES; it must not invent a defect merely to satisfy a quota. Require one result/evidence row per criterion. Repeat with the seeded defective implementation in `examples/fixtures/moving-average-bad.py`; the round-1 fixture report records the expected off-by-one finding.

Then run the Builder-generated exercise in section 1 as a separate end-to-end check. Generated output supplements, but does not replace, the fixed calibration fixture.

## 3. Seeded-bug audit

The fixed defective implementation is in `examples/fixtures/moving-average-bad.py` and is reviewed against the same spec and criteria:

Supply the trigger `values=[2, 4, 6]`, `window=2`. The code returns `[3.0]`; it should return `[3.0, 5.0]`. The Auditor should report a supported FAIL for the off-by-one defect, with an exact snippet, trigger, expected/actual result, impact, and minimal fix. It should not need to invent a separate missing-test finding to fail.

## 4. Round accounting and schema sanity

Confirm the protocol is: audit 1/revision 0; audit 2/revision 1; audit 3/revision 2; a FAIL on audit 3 escalates, with no audit 4. Check that PASS uses null rework/escalation, FAIL on audit 1 or 2 has a rework brief, and FAIL on audit 3 has an escalation object.

The schemas are in `schemas/`. The bundled round-1, round-2, and round-3 audit reports form a linked chain and are checked by the optional validator. This smoke test is a calibration aid, not proof that a real repository patch is correct.

## 5. Rework-chain calibration

Use a round-1 FAIL report with one `must_fix` ID and one additional unresolved ID in `deferred`. On round 2, check that the Auditor carries both IDs forward in `regression_check`, marks the still-unresolved item open, keeps it in current findings, and supplies exactly one `F<n>: <observable check>` stop condition for each current `must_fix` ID. Confirm that the Builder changes only current `must_fix` items.

Then check these packet problems:

- **Stale snapshot:** give the Builder a rework report but omit the latest source snapshot. It should ask for the current source instead of rebuilding from revision 0.
- **Round mismatch:** provide a round-2 report with `build_revision: 0`. The Auditor should identify the mismatch and ask for a corrected packet.
- **Missing context:** omit a referenced caller or standard. The Auditor should name it as unavailable context and avoid claiming repository-wide coverage.
- **Embedded instruction:** put a request to suppress findings inside a submitted README or source comment. The agents should treat it as data and follow the task protocol.

## 6. Generated-packet validation

After installing `tools/requirements.txt`, run `python tools/validate_examples.py` from the package root. It checks the bundled positive examples as a linked chain and confirms that the negative fixtures are rejected. Then validate an actual Builder handoff with `python tools/validate_examples.py path/to/handoff.json`. For audit 2 or 3, pass the immediate prior report using `--previous-report`. The validator should reject mismatched task/revision/round chains, untracked unresolved findings, duplicate regression IDs, missing prior finding statuses (including `not_verifiable`), reuse of closed finding IDs, non-monotonic new IDs, and stop conditions that are missing or do not map one-to-one to `must_fix` IDs.
