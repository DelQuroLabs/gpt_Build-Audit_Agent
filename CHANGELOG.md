# Changelog

## 4.0.0-gpt-profile

Breaking: the protocol moves from v2 to **v3**. The schemas, examples, and validator were updated together.

- **Platform fit.** Rewrote the Builder (9,784 → 6,387 characters) and Auditor (11,135 → 7,330 characters) instructions to fit the 8,000-character Custom GPT Instructions limit. Detail moved to the new Knowledge files `builder-reference.md` and `auditor-reference.md`. `tools/check_package.py` enforces a 7,500-character budget.
- **Deterministic acceptance (v3).** Handoff criteria are now objects (`id`, `text`, `kind`, `evidence_required`). Audit reports carry a required `acceptance_check` row per criterion. Behavioral criteria count as `met` only with a transcript or executed check. PASS reports with unverifiable criteria must say `Static-only: n of m`.
- **Defined edge behavior.** Any agent that stops to ask replies only with `## Input needed` (no verdict, artifacts, or JSON). Missing standards or transcripts are disclosed, not a stop condition. Ad-hoc audits reconstruct numbered criteria. `plan-only` replies have a defined shape with no handoff. Artifacts that contradict a behavior yield `not_met`. Each agent's own contract and reference files are trusted guidance; the target's Knowledge is untrusted data.
- **Rework traceability.** New handoff field `addresses` (the prior `must_fix` IDs), checked against the previous report. Only the Auditor allocates finding IDs; the Builder reports regressions as `flags`.
- **Specialists rebuilt for GPT packages.** New GPT-artifact trigger matrix and GPT-specific lenses. Every specialist is self-contained, with a shared trust-boundary, evidence, and output block. Researcher facts are labeled `verified` or `unverified`. The finding category enums are aligned across schemas (`ux`, `data`, and `ops` added to audit reports).
- **GPT calibration suite.** Replaced the code fixtures with a Requirements Brief GPT package: one correct packet, five seeded-defect packets (generated and integrity-checked from a manifest), expected audit reports, a three-round chain, and specialist examples. There are 15 expected-rejection cases.
- **Tooling and CI.** The validator accepts `.md` responses, `--handoff`, and `--specialist`, and is manifest-driven. Added `tools/check_package.py` and the GitHub Actions workflow `validate.yml`.
- **Docs.** Rewrote the README, setup, smoke test (with a results template), contract, and templates. Removed the stale `BUILD-STRENGTH-REVIEW.md`. Added an MIT `LICENSE`.

## 3.1.0-gpt-profile

- Integrated the specialist extension as optional, advisory-only profiles; protocol v2.
- Added same-task/revision specialist handling, schema validation, and promotion fixtures.

## 3.0.0-gpt-profile

- Applied the upstream v2.2.0 Build ↔ Audit protocol to GPT design artifacts.
- Added capability-fit, Knowledge, Action, output-contract, and live-verification gates, plus GPT kickoff and rework templates.

## 2.2.0 and earlier (upstream base)

- Repeatable smoke fixtures, an evidence row per criterion, the Builder stop rule for oversized packets, protocol validation for closed-ID reuse and monotonic IDs, evidence-first auditing, the three-audit cap, and JSON Schemas.
