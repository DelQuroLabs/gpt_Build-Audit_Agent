# Self-audit record: 4.0.0-gpt-profile

This folder holds the package's own Build ↔ Audit record for task `gpt-build-audit-pair`:

| File | What it is |
|---|---|
| `build-handoff.v3.json` | The v3 handoff describing this release (revision 0, criteria AC1–AC6) |
| `audit-report.v3.json` | The v3 audit report for that handoff (verdict `PASS`, *Static-only: 2 of 6 criteria not verifiable*) |

Both files are validated in CI by `tools/validate_examples.py` through `examples/manifest.json`.

## How it was produced (read this before relying on it)

- **Not an independent live GPT audit.** The report was written by an external prompt audit of the whole repository using a separate auditor specification. It ran over four iterations, scoring 75 → 89 → 95 → 100 on that specification's 10-dimension rubric; the reports live outside this repository. The package checks were executed in a sandbox. It was **not** produced by a configured GPT Audit Engineer instance, and the package authors should treat it as context, not as release evidence.
- **Executed evidence.** `python tools/validate_examples.py` (23 positive and 15 expected-rejection cases) and `python tools/check_package.py` (instruction budget, fixture integrity, configuration, versions, stale and path references, specialist self-containment) both passed. Each negative case was confirmed to fail only for its stated reason.
- **Not verifiable yet.** AC5 (the Auditor PASSes the good fixture and FAILs each seeded fixture) and AC6 (the configured Builder and Auditor ignore the S4 injection line and do not reveal their instructions) are *behavioral* criteria. Under the v3 rules they stay `not_verifiable` until someone runs `SMOKE-TEST.md` on real GPTs and records the results in `SMOKE-RESULTS.md`.

## To complete the record

1. Configure both GPTs per `SETUP.md`.
2. Run S1–S7 in `SMOKE-TEST.md` and fill in a copy of `SMOKE-RESULTS.template.md` as `SMOKE-RESULTS.md`.
3. If every scenario passes, update the AC5/AC6 rows in `audit-report.v3.json` to `met` with `transcript` evidence and remove the `Static-only` prefix, then re-run `python tools/validate_examples.py`.
