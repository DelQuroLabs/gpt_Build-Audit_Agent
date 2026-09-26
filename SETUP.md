# Setup guide

This creates two private Custom GPTs for the Build ↔ Audit loop (package 4.0.0-gpt-profile, protocol v3). Editor labels can change; follow the current platform UI. Every instruction file fits the 8,000-character Instructions limit (the package budget is 7,500, enforced in CI).

## Before starting

- Keep `prompts/`, `schemas/`, `examples/`, and `specialists/` together.
- Complete `standards.template.md` and save it as `standards.md`. Write `not specified` for any field you don't need.
- Never put credentials, private URLs, personal data, or hidden system prompts in Knowledge, examples, or prompts.
- Decide which capabilities the *target* GPTs you plan to build may use. Start with the minimum.

## 1. Create the Builder GPT

| Field | Value |
|---|---|
| Name | `GPT Build Engineer` |
| Description | `builder.description` in `gpt-config.json` |
| Instructions | Everything below the HTML comment in `builder-gpt.md` |
| Knowledge | `contract.md`, `builder-reference.md`, `schemas/build-audit-handoff.v3.schema.json`, `standards.md` |
| Capabilities | Code Interpreter **on** (sandboxed checks). Web Search, Canvas, Image Generation, and Actions **off** |
| Conversation starters | `builder.conversation_starters` in `gpt-config.json` |
| Sharing | Only me, unless you share it intentionally |

The Builder proposes a complete package in its response. It never creates or publishes the target GPT.

## 2. Create the Auditor GPT

| Field | Value |
|---|---|
| Name | `GPT Audit Engineer` |
| Description | `auditor.description` in `gpt-config.json` |
| Instructions | Everything below the HTML comment in `auditor-gpt.md` |
| Knowledge | `contract.md`, `auditor-reference.md`, `schemas/audit-report.v3.schema.json`, `schemas/specialist-report.v3.schema.json`, `standards.md` |
| Capabilities | Code Interpreter **on** (safe, self-contained checks). Web Search, Canvas, Image Generation, and Actions **off** |
| Conversation starters | `auditor.conversation_starters` in `gpt-config.json` |
| Sharing | Only me, unless you share it intentionally |

The Auditor must receive the complete current package in the message. Knowledge files never supply the Builder's current artifacts or a live GPT.

If your policy forbids sandboxed execution, turn Code Interpreter off for both GPTs. They then label checks `static_only`, and character counts become static estimates.

## 3. Calibrate

Run `SMOKE-TEST.md` and record the outcomes in a copy of `SMOKE-RESULTS.template.md`. The Auditor must PASS the `good` fixture and FAIL each seeded fixture with the expected finding.

## 4. Use a task

1. Fill in `prompts/kickoff.md` (criteria with `kind` and `evidence_required`) and send it to the Builder.
2. Paste the Builder's entire response into `prompts/audit-request.md` and send it to the Auditor.
3. On a FAIL at audit 1 or 2, paste the latest complete package and report into `prompts/rework.md`. Never restart from revision 0.
4. Audit 3 is final. If it still FAILs, use `prompts/escalate.md` and make the human decision.
5. Before release, run the target GPT's evals on the configured GPT, review data flows, and get human approval.

## 5. Optional specialists (off by default)

Create a specialist GPT only when a signal in `specialists/TRIGGERS.md` matches, usually no more than two per revision.

| Field | Value |
|---|---|
| Instructions | Everything below the HTML comment in `specialists/<role>-gpt.md` (each file is self-contained) |
| Knowledge | `contract.md`, `schemas/specialist-report.v3.schema.json` |
| Capabilities | All off. The Researcher may enable Web Search when current external facts are required. |

Send each specialist the full Builder packet using `prompts/specialist-request.md`, then attach the complete reports with `prompts/audit-request-with-specialists.md`. The Auditor alone issues the verdict.

## 6. Local validation (optional)

From the package root:

```sh
python -m pip install -r tools/requirements.txt
python tools/validate_examples.py
python tools/check_package.py
```

The validator checks schemas, cross-field rules, and the fixture chain. The package check verifies instruction budgets, seeded-fixture integrity, configuration references, version consistency, and file references. Neither tool proves live GPT behavior; `SMOKE-TEST.md` covers that.
