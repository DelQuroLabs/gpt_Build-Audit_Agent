# JSON Schemas

These files define the v2 JSON objects emitted at the end of each agent response:

- `build-audit-handoff.v2.schema.json` — Builder output
- `audit-report.v2.schema.json` — Auditor output
- `specialist-report.v2.schema.json` — optional advisory specialist output; it does not change either core v2 contract

All three use JSON Schema Draft 2020-12. `tools/validate_examples.py` checks structure, one-to-one stop conditions, complete finding/frozen/minor history, unique IDs, task/revision/round transitions, closure consistency, and monotonic allocation. On later rounds supply `--previous-report`. Closed regressions need a fresh current ID referenced in the old row's evidence. Structural validation cannot authenticate human overrides or prove that prose evidence is true.

The normative semantic rules are in `../contract.md`. Version 3.2.0 retains v2 JSON shapes while enforcing complete history; older incomplete histories must be corrected. JSON inputs are UTF-8 (optional BOM), limited to 2 MiB each; duplicate keys and nonstandard numeric constants are rejected. Early response statuses are prose, not valid completed v2 reports, and should not be passed to the JSON validator.
