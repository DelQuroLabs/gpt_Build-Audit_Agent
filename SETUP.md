# Setup Guide — Build ↔ Audit Agents v2.2.0

This package creates two private Custom GPTs. Exact editor labels and plan availability can change; follow the current GPT editor UI. Optionally validate the bundled examples with `pip install -r tools/requirements.txt` and `python tools/validate_examples.py`. You can validate generated handoffs and reports too; for audit round 2 or 3, provide the immediately previous report with `--previous-report`.

## Before you start

- Extract this ZIP so the `prompts/` and `schemas/` folders stay in place.
- Fill in `standards.template.md` and save the result as `standards.md`.
- Do not include credentials or secrets in prompts, examples, or uploaded Knowledge files.

## 1. Builder GPT

Create a GPT and configure:

- **Name:** Code Builder
- **Description:** from `gpt-config.json`
- **Instructions:** paste everything below the HTML comment in `builder-gpt.md`
- **Knowledge:** `contract.md`; also attach `schemas/build-audit-handoff.v2.schema.json` if supported
- **Capabilities:** Code Interpreter on only if useful/available; Web Search, Canvas, and Image Generation off; no Actions
- **Conversation starters:** copy from `gpt-config.json`
- **Sharing:** Only me unless you intentionally want to share

The Builder does not access or edit your local repository. It proposes code in the response. Agent-sandbox checks, when available, are not project CI.

## 2. Auditor GPT

Create a second GPT:

- **Name:** Code Auditor
- **Description:** from `gpt-config.json`
- **Instructions:** paste everything below the HTML comment in `auditor-gpt.md`
- **Knowledge:** `contract.md`, `schemas/audit-report.v2.schema.json`, and your completed `standards.md`
- **Capabilities:** Code Interpreter on only if useful/available; Web Search, Canvas, and Image Generation off; no Actions
- **Conversation starters:** copy from `gpt-config.json`
- **Sharing:** Only me unless intentional

The Auditor must receive the actual current source in the Builder response. Knowledge files do not magically provide your repository.

## 3. Project standards

Complete the stack, test commands, approved dependencies, security, error-handling, and performance sections in `standards.template.md`. Remove unanswered placeholders or mark them `not specified`; do not leave vague rules that the Auditor might treat as requirements. Upload the finished `standards.md` to the Auditor.

## 4. Smoke-test calibration

Follow `SMOKE-TEST.md`. Verify both:

1. a correct sample is not forced to FAIL; and
2. a deliberately defective sample is caught for its seeded defect.

If the Auditor reports a defect in the correct sample, inspect its trigger and evidence instead of treating any FAIL as proof the setup is right. If it misses the seeded off-by-one defect, check that the complete sample and `contract.md` were included.

## 5. Normal workflow

Use one Builder and one Auditor conversation per task, with a shared kebab-case `task_id`. Use the prompt files under `prompts/`. The audit schedule is fixed: audit 1/revision 0, audit 2/revision 1, audit 3/revision 2. A FAIL on audit 3 escalates to a human; do not start audit 4.

A GPT PASS covers only the supplied files and evidence. Apply the patch to the real repository, run project tests/CI, inspect the actual diff, and obtain human approval before shipping.
