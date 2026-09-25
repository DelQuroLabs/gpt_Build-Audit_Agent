# Build ↔ Audit Agents v2.2.0

A manual, human-supervised workflow with two Custom GPTs: a **Builder** that proposes a minimal patch and an **Auditor** that reviews the complete submitted source against a spec. It is not an unattended agent loop or a replacement for repository CI.

## Package contents

| Path | Purpose |
|---|---|
| `builder-gpt.md` | Instructions for the Builder GPT |
| `auditor-gpt.md` | Instructions for the Auditor GPT |
| `contract.md` | Shared protocol v2 |
| `schemas/` | JSON Schemas for both handoff objects |
| `examples/` | Positive and negative protocol fixtures, source calibration samples, and a linked audit chain |
| `tools/` | Optional validator for bundled examples and generated protocol JSON |
| `CHANGELOG.md` | Summary of v2 changes |
| `standards.template.md` | Project standards to complete and attach to Auditor |
| `gpt-config.json` | Names, descriptions, starters, capability suggestions |
| `prompts/` | Kickoff, audit, rework, escalation prompts |
| `SMOKE-TEST.md` | Fixed good/bad fixtures and a linked audit chain to verify setup and calibration |

## Quick setup

1. Create a Builder GPT. Paste the content below the HTML comment in `builder-gpt.md`. Attach `contract.md` and `schemas/build-audit-handoff.v2.schema.json` if Knowledge supports it. Enable Code Interpreter for self-contained checks if available; keep Web Search, Canvas, and image generation off for deterministic code review. Leave Actions empty.
2. Create an Auditor GPT. Paste `auditor-gpt.md`. Attach `contract.md`, `schemas/audit-report.v2.schema.json`, and a completed `standards.md`. Enable Code Interpreter only for safe, self-contained execution; otherwise static review is still allowed.
3. Keep both GPTs private unless sharing is intentional. Do not paste secrets or proprietary code into a GPT shared beyond your approved audience.
4. Run the seeded test in `SMOKE-TEST.md` before using the loop on a real task.

The GPT editor and available capabilities may change; use the current UI labels. `Code Interpreter` is not the same thing as access to your repository or CI. It may not have your project files, dependencies, network access, or the project's test runner.

To validate generated protocol JSON locally, install `tools/requirements.txt` and pass the handoff or audit report to `tools/validate_examples.py`. For audit round 2 or 3, also pass the immediately previous report with `--previous-report`.

Running the validator with no arguments checks the bundled good examples as a linked audit chain and confirms that the included malformed reports are rejected.

## Run a task

Use one Builder conversation and one Auditor conversation per task. Title both with the same `task_id`. If either conversation must be reset mid-task, use the current-source and prior-report fields in the prompt files; never reset from an incomplete or stale packet.

1. Fill `prompts/kickoff.md` with one-sentence spec, observable acceptance criteria, and relevant source/context. Send to Builder.
2. If Builder asks a blocking question, resolve it before continuing. Otherwise copy its **entire response**, including current file contents, context snapshot, verification, and handoff JSON, to Auditor using `prompts/audit-request.md`.
3. `PASS` or `PASS_WITH_NOTES` means no blocking defect was found in the supplied scope. Apply the proposed patch, run real project tests/CI, and review before release.
4. On `FAIL` at audit 1 or 2, send the latest full source snapshot and complete audit response to Builder using `prompts/rework.md`. Then send the Builder's entire updated response to Auditor.
5. Audit 3 is final. If still `FAIL`, do not run another cycle; use `prompts/escalate.md` and make the human decision.

### Round accounting

| Audit round | Builder revision |
|---:|---:|
| 1 | 0 (initial) |
| 2 | 1 (first rework) |
| 3 | 2 (second rework, final audit) |

## Calibration and use

- A correct submission should be allowed to PASS. The Auditor has no defect quota.
- Missing runtime output is reported honestly; it is not automatically proof of a code defect. Follow test requirements in the spec and `standards.md`.
- Always include the latest current source. Never restart a rework from round-0 code after it has changed.
- For production code, the real repository's test suite, CI, security checks, and human review remain the release gate.
- `gpt-config.json` has suggested starters and capability settings; these are conveniences, not protocol.

See `SETUP.md` for click-by-click setup and `contract.md` for the normative handoff rules.
