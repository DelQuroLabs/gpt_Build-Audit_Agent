# Prompt and Code Re-audit - 3.2.2

Date: 2026-09-28. Editions: 3.2.2-gpt-profile and 3.2.2-lean. Method: the supplied Prompt Auditor rubric, targeted repair/re-audit, local regression checks, and fresh-archive verification.

## 1. Verdict

**Full: 96/100. Lean: 96/100. Band A. READY within the reviewed static-prompt and local-code scope. No known open findings in that scope.**

R6-R8 are fixed, and the five earlier repairs remain covered. This is a rubric judgment, not a 96% measured model success rate, proof of universal correctness, or production release approval. The user's 95+ request is an improvement target, not a mandated score.

The previous 3.2.1 clean assessment was superseded by a fresh re-audit: three additional defects reproduced despite its 43 passing tests, lowering the corrected baseline to 88/100. Its historical report is preserved as PROMPT-AUDIT-3.2.1.md with a superseded notice. Older ZIPs are not modified in place.

## 2. Audit Scope and Limits

Product: a manual, human-supervised Builder/Auditor pair with six optional advisory specialist roles. Original repository baseline: e1aa678. Immediate repair baseline: the two delivered 3.2.1 ZIPs.

This is a delta against the previous complete package review, with a full report on the repaired revision. Fresh inspection covers the validator, all three schemas, input-boundary tests, full/lean contracts, setup/replacement guidance, current audit records, and archive contents. Unchanged role instructions, fixtures, and workflow design retain the earlier static review; this is not a claim of a new independent review of every unchanged line. Installation assembly, all retained tests, and exact original probes are rerun.

Authorized actions: local inspection, edits, tests, token measurement, packaging, and verification. No model API calls, deployment, GPT installation, repository push, external account access, or delegated work. Documents and packet contents remain review data, not instructions to this reviewer.

Exact runtime output capacity is not exposed; complete replacement artifacts and the report are delivered as files. The package's 7,500-character instruction budget is conservative, not an asserted host limit.

Observed: source changes, raw-input reproductions, passing local checks, full/lean code/schema parity, and fixed-context token counts. Inferred: likely prompt-following behavior. Unverified: actual host setup/retrieval, model obedience, live tool isolation, cross-model outcome equivalence, production CI, and integrations. The same agent repaired and reviewed this release; it is not independent certification.

The validator enforces documented structural/transition rules, not the truth of evidence, authenticity of human approval, snapshot completeness, filesystem case/symlink aliases, or unsupplied earlier reports. Retain and validate every transition. Live per-host/model evaluation and human release review remain required.

## 3. Scorecard

Contribution = score / 10 x weight. Round only the final total. Both editions have identical schema objects and executable checks; their equal scoped grades do not establish live behavioral equivalence.

| Dimension | Weight | Score | Contribution | Anchor and evidence |
|---|---:|---:|---:|---|
| Objective and success conditions | 12 | 10 | 12.0 | All 9-level requirements; no residual finding: explicit purpose, measurable criteria, three-round cap, human release gate. |
| Audience, context, assumptions | 10 | 9 | 9.0 | Executor/reference requirements and exclusions are explicit; actual host installation/retrieval remains unverified. |
| Inputs, state, precedence | 12 | 10 | 12.0 | All 9-level requirements; no residual finding: whole-string IDs, exact counters, complete history, precedence and early states agree with checks. |
| Process and decision logic | 10 | 10 | 10.0 | All 9-level requirements; no residual finding: monotonic IDs, active versus closed history, accepted-risk closure and bounded escalation remain exercised. |
| Authority, tools, actions | 10 | 9 | 9.0 | Tools off, caller grants, isolation/budgets and no-tool fallback explicit; actual host enforcement is outside these tests. |
| Output contract and usability | 12 | 10 | 12.0 | All 9-level requirements; no residual finding: strict v2 objects, canonical unique paths, complete installation files, clear replacement guidance. |
| Safety, security, privacy | 12 | 9 | 10.8 | Trust/data separation, least privilege and redacted diagnostics retained; live prompt-injection resistance is not established by code tests. |
| Exceptions, failure, recovery | 8 | 10 | 8.0 | All 9-level requirements; no residual finding: exact numeric handling, explicit parsing bounds, NUL/invalid-ID rejection, long-ID and valid-integral controls. |
| Evaluation and acceptance | 8 | 9 | 7.2 | 60 tests per edition, original failing probes, exact-rational checks and archive verification; live model trials remain specified but unexecuted. |
| Consistency and maintainability | 6 | 10 | 6.0 | All 9-level requirements; no residual finding: identical shared code/tests, equivalent schemas, current versus historical evidence separated. |
| **Total** | **100** | | **96.0 -> 96** | **No severity ceiling applies to the repaired revision.** |

The four 9-level dimensions meet the stated static scope but retain disclosed external assurance limits. No score is raised merely to reach the requested threshold.

## 4. Strengths

- Full snapshots, criterion-level evidence, no defect quota, explicit not-run reporting, and the three-audit cap are preserved.
- Reopened active findings cannot disappear into PASS; closed-ID regressions require fresh IDs.
- Accepted risk stays distinct from verified technical repair, including null-brief final reports.
- Invalid inputs are rejected rather than trimmed, rounded, or silently migrated.
- Lean preserves the same tested protocol rules with smaller fixed context.

## 5. Findings

**None known open in this reviewed scope.** R1-R5 remain FIXED for their tested triggers. R6-R8 are FIXED:

| ID | Prior severity | Root cause and observed consequence | Repair and verification |
|---|---|---|---|
| R6 | MAJOR | Schema end anchors accepted a final newline; the ID-order fallback then ignored a high malformed ID, allowing nonmonotonic allocation. Task/S IDs also accepted final newlines. | Whole-string schema patterns and explicit invalid-ID rejection. Original bypass rejected; valid F9/F10 and 5,000-digit IDs retained. |
| R7 | MINOR | Binary-float JSON decoding changed exact fractional values into integers: 1.0000000000000001 -> 1.0 and 1e-400 -> 0.0. | Exact decimal decoding, bounded integer normalization, explicit resource limits; fractions rejected while integral decimal/exponent forms pass. |
| R8 | MINOR | Canonical-path checks omitted NUL, accepting a path unusable by filesystem APIs. | Reject NUL before path interpretation, without filesystem access or echoing the submitted value. |

Full evidence, stable code locators, smallest repairs and verification names are in [CODE-REVIEW-FIXES.md](CODE-REVIEW-FIXES.md). Prior failing archive evidence and current passing evidence accompany the release.

Stale lean setup-version text and the README's historical fixture description were corrected while updating release guidance. The historical directory-artifact handoff remains unchanged as an explicit expected rejection, not a valid current packet.

## 6. Repair Plan

Completed in both editions: tighten schema ID boundaries; reject malformed ordering inputs; decode numeric JSON exactly; normalize integral forms within explicit limits; reject NUL paths; add 17 regression tests; document behavior and limits; synchronize full/lean code and schemas; preserve superseded audit history; rebuild and verify the ZIPs.

No v2 fields, new tool authority, automatic approval, or unattended execution were added. Invalid prior inputs now fail explicitly. No material policy decision remains unresolved for these repairs.

## 7. Acceptance Checks

Local runtime: Python 3.12 and jsonschema 4.26.0 on Windows. Declared script minimum remains Python 3.10; other Python versions and operating systems were not executed here.

| Check | Observed result | Limit |
|---|---|---|
| Complete automated suite | 60 tests pass per edition: 43 retained + 17 new methods, with parameterized cases | Protocol/code/packaging tests, not model trials |
| Bundled validator suite | 11 positive objects accepted; 7 designated negatives rejected | Includes preserved historical directory-artifact negative |
| Prompt assembly | Eight generated prompts match sources and remain within 7,500 characters | Not proof of host acceptance |
| Original 3.2.1 re-audit probes | All 13 expected outcomes pass against each new ZIP | Same raw failing inputs plus prior-repair controls |
| Exact-rational numeric oracle | 1,000 seeded decimal literals per edition preserve value and integer classification | Bounded generated cases, not exhaustive proof |
| Archive checks | Fresh contained extraction, CRC/hash checks, all tests rerun | Does not modify GitHub |
| Full/lean parity | Python tools/tests byte-identical; three parsed schemas identical | Condensed prose is statically compared, not live-model certified |
| Fixed-context token measurement | 29.7-34.3% reduction across eight roles and two local tokenizers | Excludes task/outputs/reasoning, standards, wrapping/retrieval |
| Live configured model/host trials | NOT RUN | Required before releasing a configured instance |

Boundary cases include: final newlines across all identifier locations; malformed prior ID history; high-precision and underflowing fractions; integral exponent forms in current and previous reports; numeric input limits and clean errors; nonstandard constants; NUL at multiple path positions without value leakage or filesystem access. Earlier reopened/override/duplicate-path/long-ID/integral-history cases still pass.

Delivered verification-3.2.2.json contains archive hashes and actual command output. reaudit-3.2.2-evidence.json records the original probes and rational checks. The ZIP contents are the tested release; older evidence is retained under its original version.

## 8. Revised Prompt

The replacement ZIP contains complete editable sources and generated installation prompts, not excerpts:

- [Builder](../dist/instructions/builder.md), [Auditor](../dist/instructions/auditor.md).
- [Security](../dist/instructions/security.md), [UX](../dist/instructions/ux.md), [Perf](../dist/instructions/perf.md), [Data](../dist/instructions/data.md), [Release](../dist/instructions/release.md), [Researcher](../dist/instructions/researcher.md).
- [Contract](../contract.md), [setup](../SETUP.md), [configuration](../gpt-config.json), [schemas](../schemas/README.md).
- [Boundary tests](../tests/test_input_boundaries.py), [earlier review regressions](../tests/test_review_regressions.py), [behavioral acceptance suite](../evals/README.md).

The lean ZIP retains these locations with compact role/contract text and losslessly minified schemas. LEAN.md and TOKEN-REPORT.md explain required context and measured savings.

## 9. Final Assumptions and Open Questions

No unresolved decision blocks the local repair/package scope. The product remains a manual, human-supervised workflow. Host/model choice, private standards, live permissions and release approval belong to deployment configuration and have not been certified here. Identical outcomes on every AI model and a mathematically minimal-token prompt are not established.

## Loop Summary

This corrective cycle follows the fresh re-audit; it does not retroactively validate the old clean conclusion.

| Pass | Edition/revision | Dimension scores in rubric order | Raw -> final | Open before -> after repair | Recommendation |
|---|---|---|---|---|---|
| 1 | Both delivered 3.2.1 editions | 10, 9, 8, 9, 9, 9, 9, 8, 8, 8 | 87.8 -> **88/100 each** | 3 -> 0, verified at pass 2 | FIX AND RECHECK |
| 2 | Full and lean 3.2.2 | 10, 9, 10, 10, 9, 10, 9, 10, 9, 10 | 96.0 -> **96/100 each** | 0 -> 0 | READY within stated scope |

Exit: **STOP CONDITION MET** for this scoped cycle: no known open finding, score above 95. Actual repairs and fresh verification, not repeated scoring of unchanged text, support the result.

## Remaining Decisions

None for these local repairs. Per-host/model behavioral validation and human release review remain required.
