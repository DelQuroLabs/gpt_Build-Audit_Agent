# Smoke test results

Copy this file to `SMOKE-RESULTS.md` and fill it in after each run of `SMOKE-TEST.md`. Keep transcripts (or shared-chat links) so that every `pass` is backed by evidence. Never paste secrets or personal data.

- Package version:
- Date:
- Operator:
- Builder GPT (name and model shown in the editor):
- Auditor GPT (name and model shown in the editor):
- Instruction files pasted from commit:

| Test | Result (pass / fail / not run) | Transcript or link | Notes |
|---|---|---|---|
| S1 Builder packet | | | |
| S2 Correct-sample audit | | | |
| S3a seeded-question-limit | | | |
| S3b seeded-action-no-auth | | | |
| S3c seeded-knowledge-obey | | | |
| S3d seeded-capability-overclaim | | | |
| S3e seeded-format-collision | | | |
| S4 Prompt injection (Auditor) | | | |
| S4 Prompt injection (Builder) | | | |
| S5 Rework and round accounting | | | |
| S6 Specialist flow | | | |
| S7 Offline checks | | | |

## Failures and follow-up

<For each failure: what happened, the suspected instruction section, and the change you made. Re-run the affected tests after the change.>
