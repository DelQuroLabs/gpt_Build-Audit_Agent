# Rework request — only after FAIL on audit 1 or 2

Paste the Auditor's entire latest response below, including its JSON. In the same message, provide the **latest complete current artifact snapshot** from the previous Builder response. If using a new Builder conversation, also include the original spec/acceptance criteria, platform standards, and the current finding-status ledger. Never restart from round-0 artifacts after changes have been made.

---

Fix only IDs in `rework_brief.must_fix`. Do not change frozen or unrelated scope. Confirm matching task/revision and a previous FAIL on audit 1 or 2 before incrementing revision by one. Missing/stale/invalid inputs return INPUT REQUIRED without handoff JSON. Preserve all prior finding, regression, and frozen history, including minor notes. Flag new issues for the Auditor; do not allocate F IDs. Demonstrate fixes with actual evals, artifact evidence, or labeled static explanation. Return complete changed artifacts and a `build-audit-handoff` v2 JSON block only when complete.

## Latest complete current artifact snapshot

<paste every current artifact required for review here>

## Original spec and acceptance criteria (required when starting a new conversation)

<paste original kickoff fields here>

## Platform/project standards

<paste the completed standards or say `not specified`>

## Finding-status ledger (required when starting a new conversation)

<list every prior finding ID as fixed/open/deferred/not-verifiable/overruled, with evidence>

## Latest Auditor report

<paste complete Auditor response here>
