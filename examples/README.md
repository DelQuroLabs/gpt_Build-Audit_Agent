# Examples and fixtures

Every case listed in `manifest.json` runs when you call `python tools/validate_examples.py` with no arguments (CI runs it on every push).

## GPT calibration suite: `fixtures/requirements-brief-gpt/`

| Path | Contents |
|---|---|
| `calibration.md` | Spec, criteria, and expected outcome for every fixture |
| `good/builder-response.md` | A complete, correct Builder response (revision 0) |
| `seeded/manifest.json` | Five single-change defects: find/replace text and expected finding |
| `seeded/<name>.md` | Generated packets: `good` plus exactly one replacement (`tools/check_package.py` verifies this) |
| `expected/*.audit.json` | The audit report a calibrated Auditor should produce for each packet |
| `standards-strict.md` | Stricter standards used by `audit-notes.v3.json` to demonstrate PASS_WITH_NOTES |

To regenerate seeded packets after editing `good/` or the manifest, run `python tools/check_package.py --write`, then update the expected reports if the evidence changed.

## Protocol examples

| Path | Demonstrates |
|---|---|
| `audit-notes.v3.json` | PASS_WITH_NOTES with a MINOR standards finding |
| `chain/` | Round 1 FAIL → rework handoff (`addresses`) → round 2 FAIL with a new ID → round 3 escalation |
| `specialist-security.v3.json` | A Security report triggered by the seeded Action |
| `specialist-ux.v3.json` | A UX report on the unbounded question flow |
| `specialist-researcher.v3.json` | A researcher brief with a verified, sourced platform fact |
| `audit-with-specialist-promotion.v3.json` | The Auditor confirming and promoting S1 to F1 |
| `invalid/` | 15 documents the validator must reject (expected errors in `manifest.json`), plus 3 valid helper documents they reference (`audit-id-gap-prior`, `handoff-evidence-required`, `specialist-security-wrong-revision`) |

Chain handoffs contain JSON only: they illustrate protocol continuity. The complete-packet requirement is exercised by the fixture suite.
