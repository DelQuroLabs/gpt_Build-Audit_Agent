# Prompt and code re-audit - 3.2.1

Date: 2026-09-27. Editions: 3.2.1-gpt-profile and 3.2.1-lean. Method: the user-supplied Prompt Auditor's ten weighted dimensions, a fresh corrective audit cycle, targeted code review, and local regression checks. The 95+ request is an improvement target, not a mandated grade.

## 1. Verdict

**Full: 96/100. Lean: 96/100. Band A; READY for the stated static prompt and local-code scope. Zero known open findings in that scope.** All five confirmed review defects are repaired. This is a rubric assessment, not a measured 96% model success rate, a guarantee of no undiscovered defects, or production release approval.

The earlier 3.2.0 93/100 and zero-issue conclusion was overconfident: its 23 tests missed these cases. The preserved report is labeled superseded, not used as evidence for the new grade.

## 2. Audit Scope and Limits

Target: Builder, Auditor, six advisory specialist instructions, shared contract, configuration, schemas, templates, setup, calibration examples, validator, tests, and generated installation prompts. Audience: humans operating a bounded, manual private-agent workflow. Original repository baseline remains commit e1aa678; this repair baseline is the two delivered 3.2.0 editions.

The full and lean role instructions and contracts were compared, all three parsed schema objects match, and executable tools/tests are identical across editions. The original full-repository review is retained; this re-audit reread the current workflow surfaces and fully inspected the repaired code and its tests. Historical reports and seeded negative fixtures are data, not current release evidence. No target text or attached document overrides the caller or host.

Authorized actions: local inspection, edits, tests, packaging, and a public official-documentation check on evaluation methodology. No model API call, GPT installation, repository push, deployment, account connection, or delegated agent work. The command sandbox failed to initialize; authorized local execution worked. That infrastructure failure is not a product defect.

Exact response capacity was not exposed; complete revised artifacts and the full report are delivered as files without truncation. The conservative installation budget remains 7,500 characters, not an asserted host limit.

Observed: code, prompts, schema equivalence, fixture results, actual test output, and local token counts. Inferred: likely instruction-following behavior. Unverified: real host setup, retrieval, live tool isolation, model obedience, cross-model outcome equivalence, production CI, and integration behavior. The same agent made and reviewed these repairs; this is not independent certification.

The validator proves structural and specified transition rules only. It cannot authenticate human approval, prove prose evidence or snapshots true, resolve filesystem case/symlink aliases, or reconstruct unsupplied earlier reports. Retain and validate every transition. Host/model-specific behavioral tests and human release approval remain required.

## 3. Scorecard

Contribution = dimension score / 10 x weight. Round the final sum only. Both editions receive the same scores because they preserve the same reviewed contract and executable checks, not because live model equivalence was demonstrated.

| Dimension | Weight | Score | Contribution | Anchor and evidence |
|---|---:|---:|---:|---|
| Objective and success conditions | 12 | 10 | 12.0 | All 9-level requirements; no residual finding: explicit manual purpose, measurable criteria, three-round cap, human release boundary. |
| Audience, context, assumptions | 10 | 9 | 9.0 | Clear user/host requirements and exclusions; actual installation and reference retrieval still require per-host validation. |
| Inputs, state, precedence | 12 | 10 | 12.0 | All 9-level requirements; no residual finding: active/closed history, integral numbers, canonical file identity, trust precedence and early states agree with tests. |
| Process and decision logic | 10 | 10 | 10.0 | All 9-level requirements; no residual finding: regression transitions, final override representation, bounded rework and escalation are explicit and exercised. |
| Authority, tools, actions | 10 | 9 | 9.0 | Explicit caller grants, tools off, isolation/budgets/provenance and no-tool fallback; actual host enforcement remains unverified. |
| Output contract and usability | 12 | 10 | 12.0 | All 9-level requirements; no residual finding: schema branches, final accepted-risk evidence, consistent complete installation files and replacement guidance. |
| Safety, security, privacy | 12 | 9 | 10.8 | Least privilege, data/instruction separation, redaction and safe input diagnostics; live injection resistance is not established by static review. |
| Exceptions, failure, recovery | 8 | 10 | 8.0 | All 9-level requirements; no residual finding: no long-ID crash, valid decimal integers accepted, contradictory file operations rejected, strict JSON/capacity/no-tool paths. |
| Evaluation and acceptance | 8 | 9 | 7.2 | 43 local tests per edition, CLI transition cases and fixed behavioral cases; live per-model trials are specified, not executed. |
| Consistency and maintainability | 6 | 10 | 6.0 | All 9-level requirements; no residual finding: v2 shapes retained, shared tested implementation, current/historical reports separated, deterministic prompt assembly. |
| **Total** | **100** | | **96.0 -> 96** | **No severity ceiling applies to the repaired revision.** |

The four 9-level dimensions meet the scoped requirements but have external assurance limits. Those limits are disclosed, not hidden by a score or presented as tested capabilities.

## 4. Strengths

- Complete snapshots, criterion-level evidence, no defect quota, and honest not-run reporting remain intact.
- A reopened active blocker cannot disappear into PASS, and closed IDs cannot be reused.
- Explicit accepted risk fits PASS, PASS_WITH_NOTES, and final FAIL without a false technical-fix claim.
- Plain Markdown/JSON workflow is provider-neutral; unsupported hosts fail explicitly instead of silently dropping required context.
- Lean context remains smaller without changing the executable validator or schema structures.

## 5. Findings

**None known open in the reviewed scope.** R1-R5 are FIXED; their observed triggers, locations, repairs, and regression checks are in [CODE-REVIEW-FIXES.md](CODE-REVIEW-FIXES.md).

The historical self-audit handoff's directory-level artifact entry is preserved unchanged and now expected to be rejected. It is not a valid live handoff. This is part of R3's artifact-identity repair, not a hidden exception to validation.

## 6. Repair Plan

Completed: distinguish active reopened IDs from closed history; record final human overrules in regression evidence; reject duplicate/noncanonical artifact paths; compare arbitrary decimal IDs without integer conversion; use JSON Schema integer semantics for round continuity; add positive and negative CLI regression cases; update full and compact contracts, historical labels, setup/replacement guidance, and live acceptance checks.

No new field shape, tool authority, deployment feature, or automatic approval was introduced. Existing human risk acceptance remains permitted, with an unambiguous representation in every verdict branch. No material policy decision remains unresolved for these repairs.

## 7. Acceptance Checks

Local environment: Python 3.12 and jsonschema 4.26.0; declared runtime is Python 3.10+, but other Python versions and operating systems were not executed here.

| Check | Observed result | Scope |
|---|---|---|
| python -m unittest discover -s tests -v | 43 tests passed in each edition | 23 retained tests plus 20 new tests, including parameterized CLI transitions and malformed inputs. |
| python tools/validate_examples.py | 11 positive objects and seven expected rejections | Schema and semantic rules, including the preserved invalid historical directory artifact. |
| python tools/package_instructions.py --check | Eight complete prompts match sources; all within 7,500 characters | Installation consistency, not live host acceptance. |
| Same tools/tests in both editions | Byte-identical | No forked validator behavior in lean. |
| Three schema objects in both editions | Structurally identical | Lean minification is lossless. |
| Fixed-context measurement | 29.9-34.5% reduction across eight roles and two tokenizers | Instructions + contract + required schemas only; task/output/reasoning tokens excluded. |
| Actual configured model/host behavioral trials | NOT RUN | Required before releasing a configured instance. |

The release delivery also includes separately captured ZIP extraction/test evidence and hashes. The source checks above are not a substitute for those archive checks.

Regression coverage includes: all four next-round statuses with retained/omitted reopened findings; fresh IDs for closed regressions; accepted-risk closure at rounds 2/3, with minor findings and final FAIL; empty or mislabeled overrides; prior decision disclosure; duplicate/conflicting paths and path aliases; 5,000-digit IDs; decimal numeric ordering; valid integral floats; and rejection of booleans/fractions. These are deterministic tests, not simulated model transcripts.

The behavioral suite adds H2-H5 and a repeatable per-host/model record with three fresh trials per applicable case/edition, retaining failures rather than rerolling them. It is a small release screen, not a statistical guarantee. Model variability is why behavioral evaluations complement code tests; see [OpenAI evaluation best practices](https://developers.openai.com/api/docs/guides/evaluation-best-practices), consulted 2026-09-27. This repository does not depend on a hosted evaluation API.

## 8. Revised Prompt

Complete editable sources, generated prompts, schemas, and tests are included in the replacement ZIP, not excerpts:

- [Builder](../dist/instructions/builder.md) and [Auditor](../dist/instructions/auditor.md).
- [Security](../dist/instructions/security.md), [UX](../dist/instructions/ux.md), [Perf](../dist/instructions/perf.md), [Data](../dist/instructions/data.md), [Release](../dist/instructions/release.md), [Researcher](../dist/instructions/researcher.md).
- [Contract](../contract.md), [configuration](../gpt-config.json), [setup](../SETUP.md), [behavioral tests](../evals/README.md), [review regressions](../tests/test_review_regressions.py).

Lean retains these locations with condensed instructions and contract. Its TOKEN-REPORT.md records measurements and exclusions; LEAN.md explains which context must remain available.

## 9. Final Assumptions and Open Questions

No unresolved decision blocks the local repair/package scope. Assumption: the product remains a manual human-supervised agent pair. Actual model/host, integration permissions, private standards, and release approval are configuration decisions outside this audit. Universal identical model outcomes and a mathematically minimal token prompt are not established.

## Loop Summary

This is a fresh corrective cycle requested after code review, not a retroactive claim that the old clean assessment was correct. Scores use the attached rubric; ceilings never raise a score.

| Pass | Edition/revision | Dimension scores in rubric order | Raw -> final | Open before -> after repair | Recommendation |
|---|---|---|---|---|---|
| 1 | Both 3.2.0 copies, corrected baseline | 10, 9, 6, 6, 9, 6, 9, 6, 6, 6 | 74.4 -> **74/100** | 5 -> 0, verified at pass 2 | FIX AND RECHECK |
| 2 | Full 3.2.1 and lean 3.2.1 | 10, 9, 10, 10, 9, 10, 9, 10, 9, 10 | 96.0 -> **96/100 each** | 0 -> 0 | READY within stated scope |

Baseline scores of 6 map to R1/R2/R5 (state/process), R2/R3 (output), R4/R5 (exceptions), all five missing regression cases (evaluation), and contract/validator disagreement (consistency). Five MAJOR findings impose a maximum of 79; the baseline raw score is already lower. Code-review High/Medium priorities and the prompt rubric's MAJOR labels are different scales.

Exit: **STOP CONDITION MET** for this scoped repair cycle: no known open finding, score above the requested 95 threshold. The loop did not substitute repeated unchanged scoring for implementation.

## Remaining Decisions

None for these local repairs. Human per-host/model validation and release remain required.
