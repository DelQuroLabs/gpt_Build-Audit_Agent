# Specialist triggers

Run a specialist only when at least one **signal** below matches the current Builder packet. Prefer concrete artifact evidence and explicit human requests over hunches.

## Signal table

| Signal (check the Builder packet) | Specialist |
|---|---|
| `actions/` or an OpenAPI schema is present; any Action auth other than none; an Action sends user data off-platform | Security |
| Knowledge may contain personal, customer, financial, health, or credential data; sharing is broader than "Only me" | Security |
| Instructions tell the GPT to follow, execute, or prioritize content from Knowledge, files, web, or Action responses | Security |
| Acceptance criteria govern conversation flow, clarifying questions, refusal copy, language, accessibility, or output readability | UX |
| Spec states latency, cost, or token budgets; very large Knowledge sets; multi-step Action chains; retries on write Actions | Perf |
| Knowledge source replacement or restructuring, a freshness/versioning policy change, or an Action that writes or deletes records | Data |
| Sharing scope change (Only me → link, workspace, or Store), a version bump or rollback plan, or a human ship-checklist request | Release |
| Spec depends on current external facts: platform limits, vendor API behavior, pricing, policy, law, or license | Researcher |

## Parallelism and cap

- Run matching specialists **in parallel** on the **same** packet (same `task_id` and `build_revision`).
- Never chain specialists into each other.
- Default cap: two specialists per revision. A release review may pair Release with Security.

## Skip when…

| Situation | Action |
|---|---|
| No signal matches | Core pair only |
| The specialist would only restate Auditor checks | Skip; the Auditor owns it |
| The packet lacks the artifacts the specialist needs | The specialist reports a scope limitation and `open_questions`; it does not guess |

## Human checklist (30 seconds)

1. Does a row in the signal table match? If not, stop.
2. Is the full Builder response available, not just the JSON? If not, fix the packet first.
3. Will the Auditor receive this report for the same revision? If not, don't run it.

Worked example: `examples/specialist-security.v3.json` was triggered by the Action in the `seeded-action-no-auth` fixture. The `good` fixture has no Action, so no Security trigger fires.
