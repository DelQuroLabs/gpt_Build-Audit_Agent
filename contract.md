# Build ↔ Audit Handoff Contract v2

Attach this file to both GPTs. Attach the two JSON Schemas in `schemas/` as well if the GPT platform permits. The schemas are normative; examples must validate against them.

## 1. Purpose and limits

This is a manual, human-supervised review loop. The Builder proposes patches; it does not modify the user's repository. The Auditor reviews only the source/context actually submitted. Neither a GPT `PASS` nor an agent-sandbox run proves that the real working tree, project CI, deployment, or unprovided code is correct. Apply the patch, run the actual project checks, and retain human review before release.

## 2. Round model (unambiguous)

There are **three audit rounds total**:

| Audit | Build revision | Meaning |
|---:|---:|---|
| 1 | 0 | Initial build and audit |
| 2 | 1 | First rework and audit |
| 3 | 2 | Second rework and final audit; if still FAIL, escalate |

No audit 4 and no build revision 3. `build_revision` identifies the version of the proposed code; it appears in both JSON objects. `audit_round` identifies the review attempt and appears in the Auditor report; on an initial handoff the Auditor sets it to 1, then increments it using the prior report. A task has one kebab-case `task_id` across all rounds. Finding IDs use the form `F1`, `F2`, ...; allocate new IDs monotonically within a task and never reuse an ID after it is fixed, overruled, or otherwise closed. A continuing finding retains its ID.

## 3. Audit packet contents

For every audit, copy the Builder's **entire latest response**. It must include:

1. Canonical one-sentence spec and observable acceptance criteria.
2. Full current contents of every new/modified source file (never diff-only); deletions explicitly marked.
3. Complete relevant unchanged interfaces/callers/config in `## Context snapshot`.
4. Verification table with result, environment, and actual output or reason not run.
5. `build-audit-handoff` v2 JSON.
6. For rework: latest source snapshot and latest Auditor report. Do not reset to original round-0 code.

If context is too large or missing, the Auditor records the scope limitation and asks for the needed material; it must not claim full-repository coverage.

The Builder must not truncate required source to fit a response. If complete changed files and relevant context cannot fit in the handoff packet, it asks to split or narrow the task or requests the missing context, and does not claim a complete handoff.

## 4. Builder → Auditor JSON

The final fenced JSON object in each Builder response uses:

- `contract: "build-audit-handoff"`, `version: 2`.
- `task_id`, `build_revision` (0–2), one-sentence `spec`, `acceptance_criteria`.
- `artifacts`: one entry per changed file, including `path`, `status`, `lines_changed`, `summary`, and `snapshot_included`.
- `context_manifest`: supplied relevant context paths and their roles.
- `verification`: each check's command/input, `pass|fail|not-run`, execution environment, and evidence.
- `self_audit`, `assumptions`, `flags`, `open_questions`, and `confidence`.

`not-run` is honest and permitted. Never convert it into a claimed pass. Use `agent_sandbox` only for checks actually run in that sandbox; do not label it project CI. See `schemas/build-audit-handoff.v2.schema.json` for exact types and required fields.

## 5. Auditor → Builder JSON

The final fenced JSON object uses `contract: "audit-report"`, `version: 2`, and echoes `task_id` and `build_revision`, plus `audit_round`, `verdict`, `scope_review`, `verification_assessment`, `findings`, `regression_check`, `what_held_up`, and `open_questions`.

A finding needs a concrete trigger and supported evidence (`runtime_reproduced`, `static_proof`, or clearly labeled `provided_log`). Severity follows impact/likelihood. Unverified suspicions belong in `open_questions`, not in the findings table. A missing test is blocking only when the acceptance criteria or project standards require it, or when a high-risk core claim cannot otherwise be assessed.

### Verdict payload rules

- `PASS`: no findings; `PASS_WITH_NOTES`: one or more MINOR/NIT findings and no BLOCKER/MAJOR. Both use `rework_brief: null`, `escalation: null`, `round_limit_reached: false`.
- `FAIL` at audit 1 or 2: `rework_brief` is an object; `escalation: null`; `round_limit_reached: false`.
- `FAIL` at audit 3: `rework_brief: null`; `escalation` is required; `round_limit_reached: true`.

The rework brief contains 1–8 highest-risk IDs in `must_fix`. Any remaining unresolved BLOCKER/MAJOR IDs must be preserved in `deferred`. `frozen` entries require a reason (verified fixed or explicitly overruled by the human). Include exactly one observable stop condition per `must_fix` ID, using the format `F1: <observable check>`.

See `schemas/audit-report.v2.schema.json` for the machine-readable definition. The optional validator also checks cross-field and prior-report chain rules for generated packets.

## 6. Invariants

1. **Evidence before verdict:** attempt to falsify each acceptance criterion; do not assume a defect count.
2. **Scope honesty:** judge only supplied code/context and declared standards; disclose missing inputs.
3. **No fabricated execution:** distinguish runtime execution, user-supplied logs, static reasoning, and not-run.
4. **Severity is impact-based:** Builder disclosure does not lower severity; omission does not raise it.
5. **Closed stays closed:** reopen a fixed/overruled item only with concrete new regression evidence.
6. **Monotonic tracking:** carry forward open/deferred finding IDs; add new IDs only for new defects or regressions.
7. **Human release gate:** a model PASS is not a CI result or merge approval.
8. **Conflict handling:** when the request, spec, standards, source, or prior report disagree, identify the exact conflict and ask for a decision if it changes the implementation or verdict; never resolve it silently.
9. **Criterion traceability:** the Auditor reports a result and supporting source/test evidence for every acceptance criterion. `not verifiable` is disclosed as a limitation and is not by itself a defect.
10. **Finding identity:** new finding IDs must be greater than all IDs already used in the task; an ID for a closed finding cannot be reused for a later issue.
