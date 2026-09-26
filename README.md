# GPT Build ↔ Audit Agent

[![validate](https://github.com/DelQuroLabs/gpt_Build-Audit_Agent/actions/workflows/validate.yml/badge.svg)](https://github.com/DelQuroLabs/gpt_Build-Audit_Agent/actions/workflows/validate.yml)

**Version 4.0.0-gpt-profile · protocol v3 · MIT License**

A copy-paste-ready pair of private Custom GPTs that build and independently audit **GPT design packages**:

- **GPT Build Engineer** turns a goal into a complete, testable GPT package: instructions, configuration, Knowledge/Action plan, behavior contract, and evals.
- **GPT Audit Engineer** attacks that package against its acceptance criteria and returns an evidence-based verdict plus a bounded rework brief.

It is a manual, human-supervised loop. A model PASS is **not** a live-platform test, a deployment approval, or a substitute for human release review.

## What makes it reliable

- **Complete snapshots.** Every handoff carries the full current artifacts; a diff never replaces them.
- **Deterministic acceptance.** Every criterion gets a machine-readable `met | not_met | not_verifiable` row. Runtime-behavior criteria count as met only with a transcript or an executed check.
- **Honest evidence labels.** Static review, sandbox checks, supplied transcripts, and live tests are kept separate.
- **Bounded loop.** At most three audits, finding IDs allocated only by the Auditor and never reused, and escalation to a human after audit 3.
- **Trust boundaries everywhere.** The Builder, the Auditor, and all six specialists treat packets, Knowledge, and retrieved pages as data, never as instructions.
- **Fits the platform.** Every instruction file is at most 7,500 characters (the editor limit is 8,000). CI enforces this.
- **Calibrated.** A GPT fixture suite (one correct package plus five seeded defects, each with an expected audit report) and 15 expected-rejection cases run in CI.

## Package contents

| Path | Purpose |
|---|---|
| `builder-gpt.md` / `auditor-gpt.md` | Instructions to paste into the two GPTs |
| `builder-reference.md` / `auditor-reference.md` | Knowledge files with checklists and section details |
| `contract.md` | Shared handoff protocol (v3) |
| `schemas/` | JSON Schemas for the handoff, audit report, and specialist report |
| `gpt-config.json` | Names, descriptions, starters, capabilities, Knowledge lists, platform limits |
| `standards.template.md` | Project standards to complete as `standards.md` |
| `prompts/` | Kickoff, audit, rework, escalation, and specialist templates |
| `specialists/` | Optional trigger-gated reviewers (Security, UX, Perf, Data, Release, Researcher) |
| `docs/WHEN_TO_ADD_AN_AGENT.md` | The bar for adding another GPT |
| `examples/` | GPT fixture suite, a three-round chain, specialist examples, and negative cases |
| `SMOKE-TEST.md` / `SMOKE-RESULTS.template.md` | Live calibration procedure and results log |
| `self-audit/` | The package's own handoff and audit record |
| `tools/` | `validate_examples.py` (schemas and protocol) and `check_package.py` (integrity) |
| `.github/workflows/validate.yml` | CI running both tools on every push and pull request |

## Quick start

1. Follow [`SETUP.md`](SETUP.md) to create the two private GPTs (about 10 minutes).
2. Run [`SMOKE-TEST.md`](SMOKE-TEST.md) on the configured GPTs and record the results in `SMOKE-RESULTS.md`.
3. Fill in `prompts/kickoff.md` and send it to the Builder.
4. Paste the Builder's **entire** response into `prompts/audit-request.md` and send it to the Auditor.
5. On a FAIL at audit 1 or 2, use `prompts/rework.md`. After audit 3, stop; if it still FAILs, use `prompts/escalate.md`.
6. Optional: when `specialists/TRIGGERS.md` matches, run up to two specialists on the same packet and use `prompts/audit-request-with-specialists.md`.

A PASS or PASS_WITH_NOTES is a scoped review result. Publish only after a human tests the actual configured GPT (run its evals), reviews Knowledge and Action data flows, and approves.

## Local validation

```sh
python -m pip install -r tools/requirements.txt
python tools/validate_examples.py     # 23 positive and 15 negative cases
python tools/check_package.py         # budget, fixtures, config, versions, references
```

Validate a real packet (a `.md` response or a `.json` file):

```sh
python tools/validate_examples.py builder-response.md
python tools/validate_examples.py audit.json --handoff builder-response.md [--previous-report prior.json]
```

## Safety and release boundary

Never put secrets, credentials, private URLs, or personal data in prompts, Knowledge, or examples. Never let a target GPT treat retrieved text as higher-priority instructions. Never enable Actions without a documented data flow, auth model, confirmation rule, timeout, and failure plan. Before release, test the configured GPT with representative and adversarial cases, and keep a human decision for consequential behavior.

## Releasing

1. Update `package_version` in `gpt-config.json` and add a matching top entry to `CHANGELOG.md`. `check_package.py` enforces both.
2. Make sure CI is green, then tag the release: `git tag v<version> && git push --tags`.

## License

[MIT](LICENSE). You may use, modify, and redistribute this package, including commercially, as long as the copyright notice is kept.
