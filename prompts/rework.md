# Rework request (only after FAIL on audit 1 or 2)

Paste the Auditor's entire latest response, including its JSON. In the same message, paste the **latest complete artifact snapshot** from the previous Builder response. In a new Builder conversation, also include the original kickoff, the standards, and the finding-status ledger. Never restart from revision-0 artifacts after changes have been made.

---

Fix only the IDs in `rework_brief.must_fix`. Do not change `frozen` IDs or unrelated artifacts. Confirm the task ID, prior build revision, and audit round, then increment `build_revision` by one. Set handoff `addresses` to exactly the `must_fix` IDs. If the snapshot or required context is missing or stale, reply with `## Input needed` instead of guessing. Preserve unresolved `deferred` and `not_verifiable` items. Report any regression you find in `flags` as `regression: <description>`; the Auditor assigns IDs. Demonstrate each fix honestly with an eval, artifact evidence, or a static explanation. Return complete contents of every changed artifact and a `build-audit-handoff` v3 JSON block.

## Latest complete artifact snapshot

<paste every current artifact required for review>

## Original kickoff (required in a new conversation)

<paste the original kickoff fields>

## Standards

<paste the completed standards.md, or write `not specified`>

## Finding-status ledger (required in a new conversation)

<list every prior finding ID as fixed / open / deferred / not_verifiable / overruled, with evidence>

## Latest Auditor report

<paste the complete Auditor response>
