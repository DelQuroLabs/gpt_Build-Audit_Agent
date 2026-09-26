# Build ↔ Audit Handoff Contract v3

Attach this file as Knowledge to the Builder, the Auditor, and any specialist. The three JSON Schemas in `schemas/` are normative, and every bundled example validates against them.

## 1. Purpose and limits

This is a manual, human-supervised review loop for **GPT design packages**: target instructions, configuration, Knowledge, Action schemas, behavior contract, setup notes, and evals. The Builder proposes artifacts; it never modifies a real GPT, repository, account, or system. The Auditor reviews only the complete material actually submitted. A model `PASS` is not a live-platform test, deployment approval, or safety certification. Before release, a human configures the GPT, runs the evals on it, and approves.

## 2. Round model

| Audit | Build revision | Meaning |
|---:|---:|---|
| 1 | 0 | Initial build and audit |
| 2 | 1 | First rework and audit |
| 3 | 2 | Second rework and final audit; escalate if still FAIL |

There is no audit 4 and no revision 3. One kebab-case `task_id` covers all rounds. Finding IDs (`F1`, `F2`, …) are allocated **only by the Auditor**, monotonically within a task. A continuing finding keeps its ID, and a closed ID (fixed or overruled) is never reused.

## 3. Audit packet contents

For every audit, copy the Builder's **entire latest response**. It must include:

1. The one-sentence spec and acceptance criteria (ID, text, kind, evidence_required).
2. The full current contents of every new or modified artifact (never a diff alone), with deletions marked.
3. The relevant unchanged context in `## Context snapshot`.
4. A verification table with result, environment, and evidence or the reason a check was not run.
5. The `build-audit-handoff` v3 JSON.
6. For rework: the latest complete snapshot and the latest Auditor report.
7. Optionally, complete specialist-report v3 objects for the same `task_id` and `build_revision`.

If required context (a snapshot, matching IDs, or the prior report) is too large or missing, the Auditor asks for the material. Missing standards or transcripts are disclosed as unavailable context, not a stop condition. With no handoff at all, the Auditor reviews what was supplied as `task_id: "adhoc"`, reconstructs numbered criteria from the user's request, and says so. The Builder never truncates required artifacts; it asks to split or narrow the task instead. Any agent that stops to ask replies only with an `## Input needed` section and emits no verdict, artifacts, or JSON.

## 4. Builder → Auditor JSON (`build-audit-handoff`, version 3)

- `task_id`, `build_revision` (0–2), `spec`.
- `acceptance_criteria[]`: `id` (`AC<n>`), `text`, `kind` (`behavioral` | `artifact`), `evidence_required` (boolean).
- `addresses[]`: empty at revision 0; on rework, exactly the prior `must_fix` IDs.
- `artifacts[]`: `path`, `status`, `lines_changed`, `summary`, `snapshot_included` (true for new or modified artifacts).
- `context_manifest[]`, `verification[]` (`pass | fail | not-run` with environment `agent_sandbox | project_ci | user_reported | static_only | not_run`), `self_audit[]`, `assumptions`, `flags`, `open_questions`, `confidence`, and optional `base_revision`.
- The Builder reports a regression it finds as a `flags` entry `regression: <description>`.

`not-run` is honest and permitted; never convert it into a pass.

## 5. Auditor → Builder JSON (`audit-report`, version 3)

The report echoes `task_id` and `build_revision` and adds `audit_round`, `verdict`, `summary`, `acceptance_check`, `scope_review`, `verification_assessment`, `findings`, `regression_check`, `what_held_up`, `open_questions`, `rework_brief`, `escalation`, and `round_limit_reached`.

### Acceptance rules (deterministic)

- `acceptance_check` has one row per handoff criterion, in the same order: `criterion_id`, `kind`, `result` (`met | not_met | not_verifiable`), `evidence_type` (`artifact_static | transcript | executed | none`), `evidence`, `limitation`.
- An `artifact` criterion may be `met` from static inspection. A `behavioral` criterion is `met` only with `transcript` or `executed` evidence. Otherwise it is `not_verifiable` with the limitation `specified, not demonstrated`.
- If the artifacts contradict or omit a required behavior, the row is `not_met` with `artifact_static` evidence.
- A `not_met` row requires at least one BLOCKER or MAJOR finding.
- An `evidence_required` criterion that is `not_verifiable` requires a BLOCKER/MAJOR `verification_gap` finding and a FAIL.
- A PASS or PASS_WITH_NOTES with any `not_verifiable` row has a `summary` beginning `Static-only: <n> of <m> criteria not verifiable.`

### Verdict payload rules

- `PASS`: no findings. `PASS_WITH_NOTES`: at least one MINOR/NIT finding and no BLOCKER/MAJOR. In both cases there is no `not_met` row, `rework_brief` and `escalation` are null, and `round_limit_reached` is false.
- `FAIL` at audit 1 or 2: `rework_brief` is an object and `escalation` is null.
- `FAIL` at audit 3: `rework_brief` is null, an `escalation` is required, and `round_limit_reached` is true.

The rework brief lists 1–8 highest-risk IDs in `must_fix` and the other unresolved BLOCKER/MAJOR IDs in `deferred`. `frozen` entries need a reason (verified fixed, or overruled by the human). Every `must_fix` ID gets exactly one stop condition `F<n>: <observable check>`.

Findings need a concrete trigger and supported evidence (`runtime_reproduced`, `static_proof`, or `provided_log`). Unverified suspicions belong in `open_questions`.

## 6. Specialist JSON (`specialist-report`, version 3)

This report is optional and advisory. It uses the same finding shape with provisional `S` IDs, plus `trigger_reasons`, `non_findings`, `recommended_to_auditor` (which must reference its own findings), and `research_brief` (required for the researcher and null otherwise; each fact is `verified` with a source or `unverified`). The Auditor uses a report only when its `task_id` and `build_revision` match, confirms every candidate in the Builder packet, and assigns its own `F` ID and severity, or drops the candidate with a reason. `S` IDs never enter the audit report. Accepted reports are listed in `scope_review.reviewed_paths` as `specialist-report:<role> (task <id>, revision <n>)`.

## 7. Invariants

1. **Evidence before verdict.** Try to falsify each criterion; never assume a defect count.
2. **Scope honesty.** Judge only supplied artifacts and declared standards, and disclose missing inputs.
3. **No fabricated execution.** Keep live execution, sandbox checks, supplied logs, static reasoning, and not-run distinct.
4. **Impact-based severity.** Builder disclosure does not lower severity; omission does not raise it.
5. **Closed stays closed.** Reopen a fixed or overruled item only with concrete new regression evidence.
6. **Monotonic tracking.** Carry forward open and deferred IDs. New IDs are only for new defects or regressions, and only the Auditor allocates them.
7. **Human release gate.** A model PASS is not a live test or a release approval.
8. **Conflict handling.** When the request, spec, standards, source, or prior report disagree, name the conflict and ask if it changes the build or verdict.
9. **Criterion traceability.** Every criterion has one machine-readable acceptance row.
10. **Specialist boundary.** Specialists suggest; they never issue verdicts, widen scope, or authorize actions.
11. **Platform fit.** Instruction artifacts meant for the Custom GPT Instructions field stay within 8,000 characters. This package's own instructions stay within 7,500.

## 8. GPT design checks the Auditor must consider

- instruction precedence, contradictory rules, output-format collisions, and hidden capability assumptions;
- platform support for browsing, files, memory, Actions, background work, and code execution, plus the Instructions length limit;
- Knowledge authority, freshness, citations, conflict behavior, and retrieved-content injection;
- Action permissions, auth, least privilege, data minimization, confirmation, validation, timeout/retry, and safe failure;
- privacy, secrets, consequential requests, uncertainty, refusal, and human escalation;
- eval coverage for ordinary, boundary, ambiguous, adversarial, tool-failure, output-contract, and regression cases.

Tooling: `python tools/validate_examples.py` checks schemas plus the cross-field and chain rules above, and `python tools/check_package.py` checks package integrity.
