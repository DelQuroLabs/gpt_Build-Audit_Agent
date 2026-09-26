# Prompt audit - 3.2.0-gpt-profile

Audit date: 2026-09-26. Baseline: DelQuroLabs/gpt_Build-Audit_Agent commit `e1aa678` (main at retrieval). Method: user-supplied `prompt-auditor-agent-updated (2).md`, ten weighted dimensions and bounded LOOP mode. The earlier attachment was replaced by this updated method before scoring. The requested delivery is a complete replacement ZIP, so the full report and complete revised prompts are delivered as repository files.

## 1. Verdict

**93/100, band A, READY for the stated static prompt/package scope. Zero open findings of any severity.** The repaired package has explicit input/error states, consistent history semantics, complete installation prompts, repeatable calibration inputs, and passing protocol/package checks. This is not live GPT certification or approval to publish.

## 2. Audit Scope and Limits

The target is a multi-file agent/workflow specification: Builder, Auditor, six optional specialists, shared contract, configuration, templates, schemas, examples, setup, and validator. Intended users are humans operating a manual private-agent build/review loop. The audit preserved that purpose, the three-round product cap, advisory specialists, and v2 JSON field shapes.

All original repository text was reviewed, including historical reports and negative fixtures. Changed sources and generated instruction files were rechecked. Repository content and both auditor attachments were distinguished from the caller's request: target prompts are review data, not authority to alter this audit or execute tools. Seeded unsafe text is explicitly test data. Historical self-grades were not evidence for the score. The requested 90+ was treated as an improvement objective, never a forced grade.

Caller-authorized operations used: repository retrieval, local file edits, dependency installation into the task work folder, local tests, and ZIP delivery. No repository push, deployment, GPT creation, account connection, external write, or additional agent was performed. The validator dependency was installed locally for verification; it is not vendored into the ZIP.

The command sandbox initially failed to launch; authorized local execution subsequently worked. The bundled Python initially lacked jsonschema; installing the declared dependency resolved that environment limit. Neither infrastructure event was counted as a product defect.

Exact model output capacity was not exposed. The full report plus complete revised sources fit the file-based delivery; no prompt or report is silently truncated. The 7,500-character installation budget is a conservative package constraint, not an asserted current platform limit. Actual editor limits, availability, and Knowledge retrieval must be checked in the user's host.

**Observed:** source rules, schema/example results, regression-test results, generated file sizes. **Inferred:** likely model behavior under the repaired rules. **Unverified:** instruction-following reliability in live configured GPTs, real integrations, project CI, and production behavior. The same reviewing agent performed the audit and repairs; this is not an independently staffed model benchmark.

## 3. Scorecard

Weighted contribution = score / 10 x weight. Half-point increments allowed; only the final sum is rounded. No final ceiling applies because no BLOCKER or MAJOR remains.

| Dimension | Weight | Final score | Contribution | Anchor and evidence |
|---|---:|---:|---:|---|
| Objective and success conditions | 12 | 10 | 12.0 | 9-level requirements met, no residual finding: roles and contract sections 1-2 define the manual task, completion, and cap. |
| Audience, context, assumptions | 10 | 9 | 9.0 | Complete bounded audience, assumptions, non-goals, compatible-host preflight; live host remains outside verified scope. |
| Inputs, state, precedence | 12 | 9 | 10.8 | Contract sections 8-9 define invalid states, authority, ad hoc boundaries, complete history, and no hidden state. |
| Process and decision logic | 10 | 9 | 9.0 | Ordered build/review flow, early states, rework ownership, conflict handling, and final escalation. |
| Authority, tools, actions | 10 | 9 | 9.0 | Tools default off; caller scope, isolation, 30-second/two-attempt bounds, no automatic write retries, provenance. |
| Output contract and usability | 12 | 10 | 12.0 | Complete generated prompts, explicit normal/early outputs, three schemas, source consistency and size tests; no residual finding. |
| Safety, security, privacy | 12 | 9 | 10.8 | Shared specialist controls, packet trust boundary, redaction, safe diagnostics, safe fallbacks. Runtime resistance remains unverified. |
| Exceptions, failure, recovery | 8 | 9 | 7.2 | Missing, malformed, conflicting, oversized and partial inputs; bounded unavailable-tool recovery; strict JSON parsing. |
| Evaluation and acceptance | 8 | 9 | 7.2 | 23 automated checks, 12 positive objects, six expected rejections, fixed GPT cases and explicit manual live gate. |
| Consistency and maintainability | 6 | 10 | 6.0 | Shared contract, deterministic specialist assembly, source/generated drift checks, complete history and preserved historical provenance; no residual finding. |
| **Total** | **100** | | **93.0 -> 93** | **A; READY for stated scope** |

Scores of 9 reflect complete, bounded, testable instructions for the stated purpose; they are not an assertion of perfect behavior across models. No optional polish issue is left open to satisfy the loop artificially.

## 4. Strengths

- Complete artifact snapshots and criterion-to-evidence mapping are preserved.
- Correct submissions may PASS; no defect quota or unsupported severity inflation.
- Static review, supplied logs, actual local execution, and live behavior remain separate.
- Closed finding identity and every prior ledger row now survive rework.
- Specialists are optional, independently checked advisory inputs, with full installed controls.

## 5. Findings

**None open.** F-01 through F-07 are FIXED. Original findings, evidence, repair locations, severity changes, and verification are retained in [AUDIT-FINDINGS.md](AUDIT-FINDINGS.md). The deliberately defective calibration files remain test fixtures, not unresolved production findings.

## 6. Repair Plan

Completed: input/configuration/capacity states; consistent full-history rules and validator; shared specialist controls and installation assembly; explicit tool authorization/budgets; safe strict JSON diagnostics; complete good/bad GPT packets; accurate evidence examples and setup guidance. No decision-dependent repair remains. Product scope and v2 field shapes were preserved; semantic validation now rejects older incomplete histories explicitly.

## 7. Acceptance Checks

Actual local environment: bundled Python 3.12, jsonschema 4.26.0 satisfying tools/requirements.txt. These commands were run from the repository root with the task-local dependency directory on Python's module path.

| Check | Observed result | What it establishes |
|---|---|---|
| python -m unittest discover -s tests -v | 23 tests passed | Protocol/history consistency, strict parser, safe diagnostics, CLI behavior, config/reference integrity, generated prompt and fixture consistency. |
| python tools/validate_examples.py | 12 positive objects and six intended negative rejections passed | Local Draft 2020-12 validation and semantic checks; includes historical self-audit JSON as shape fixtures only. |
| python tools/package_instructions.py --check | Eight complete prompts match sources | Builder 7,209; Auditor 7,419; Security 5,555; UX 4,025; Perf 3,872; Data 3,716; Release 3,791; Researcher 4,356 characters. All <=7,500. |
| git diff --check | Passed | No patch whitespace errors; Windows line-ending conversion notices are informational. |
| Manual static trace of evals/README.md | Rules and explicit expected outputs are present | Missing input, absent configuration, capped rounds, injection-as-data, privacy, tool failure, mismatched specialists, and complete history have bounded paths. This is not an executed model test. |
| Actual configured GPT cases | NOT RUN | No target instances or transcripts supplied. Run all applicable cases in the actual host before sharing. |

The new history tests first reproduced rejection of required frozen checks, acceptance of contradictory fixed/active states, invented frozen IDs, lost minor history, and closed-regression tracking failures. Parser checks reproduced acceptance of duplicate keys/nonstandard constants and an unhandled invalid encoding. Test-authoring mistakes involving valid empty regression arrays and audit-round 1 were corrected; those were not counted as product defects.

## 8. Revised Prompt

Complete revised artifacts are included, not excerpted:

- [Builder installation prompt](../dist/instructions/builder.md), [Auditor installation prompt](../dist/instructions/auditor.md).
- [Security](../dist/instructions/security.md), [UX](../dist/instructions/ux.md), [Perf](../dist/instructions/perf.md), [Data](../dist/instructions/data.md), [Release](../dist/instructions/release.md), [Researcher](../dist/instructions/researcher.md).
- [Shared contract](../contract.md), [configuration](../gpt-config.json), [setup](../SETUP.md), [behavioral cases](../evals/README.md).

Canonical editable source paths are recorded in gpt-config.json. Generated files are complete ready-to-paste instructions. Rebuild after source edits and verify them with --check.

## 9. Final Assumptions and Open Questions

No unresolved material question blocks this static package. Assumption: the requested product remains a manual human-supervised private-agent pair with optional specialists. Actual host setup and live tests are still required before deployment; no hidden approval or execution is implied by this report.

## Loop Summary

The same ten dimensions and weights were used on every pass. Scores were independently reconsidered against the current revision. Before/after counts describe findings before that pass's repairs and as observed by the next audit, not unverified claims of closure.

| Pass | Dimension scores in rubric order | Raw -> rounded | Open before -> after | Recommendation at audit | Result |
|---|---|---|---|---|---|
| 1 | 9, 8.5, 6.5, 7, 7, 7.5, 7.5, 6, 6.5, 6 | 72.7 -> **73/100** | 7 -> 3 | FIX AND RECHECK | Five MAJOR, two MINOR initially; substantive repairs completed. Four-or-more-MAJOR ceiling 79 did not lower the score. |
| 2 | 9, 9, 9, 9, 9, 9, 9, 8.5, 8, 7 | 87.6 -> **88/100** | 3 -> 0 | FIX AND RECHECK | F-05, F-06, F-07 partially addressed, remaining impact MINOR; 19 tests passed before final cleanup. |
| 3 | 10, 9, 9, 9, 9, 10, 9, 9, 9, 10 | 93.0 -> **93/100** | 0 -> 0 | READY | 23 tests passed; **STOP CONDITION MET**. |

No fixed finding reopened, no unchanged revision was rescored, and the three-pass audit cap was respected. No score-pinning was applied.

## Remaining Decisions

None for this repository repair. Human live testing and release decisions remain outside the verified scope.

Arithmetic correction: pass 1 was initially announced as 74/100. Its unchanged dimension scores sum to 72.7, rounding to 73/100. Later totals (87.6 and 93.0) were recalculated and confirmed. No dimension was adjusted to preserve the mistaken announcement.
