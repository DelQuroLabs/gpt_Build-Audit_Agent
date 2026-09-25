# Rework request — only after FAIL on audit 1 or 2

Paste the Auditor's entire latest response below, including its JSON. In the same message, provide the **latest current source snapshot** from the previous Builder response. If using a new Builder conversation, also include the original canonical spec, acceptance criteria, constraints, and the current finding-status ledger. Never restart from round-0 source after changes have been made.

---

Fix only IDs in `rework_brief.must_fix`. Do not change `frozen` IDs or unrelated files. Confirm the task ID, prior `build_revision`, and `audit_round`; increment `build_revision` by one. If the source snapshot or required context is missing or stale, ask for it instead of guessing. Never truncate the latest source snapshot to fit; ask to split or narrow the task if the complete handoff cannot fit. Demonstrate each fix honestly, include complete current contents of changed files, and emit a `build-audit-handoff` v2 JSON block.

## Latest current source snapshot

<paste current complete source and context here>

## Original spec and acceptance criteria (required when starting a new conversation)

<paste original kickoff fields here>

## Finding-status ledger (required when starting a new conversation)

<list prior finding IDs as fixed/open/deferred/overruled with evidence>

## Latest Auditor report

<paste complete Auditor response here>
