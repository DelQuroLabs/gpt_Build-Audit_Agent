# JSON Schemas (protocol v3)

These schemas define the JSON object at the end of each agent response. All use JSON Schema Draft 2020-12.

| Schema | Emitted by |
|---|---|
| `build-audit-handoff.v3.schema.json` | Builder: criteria objects, `addresses`, artifacts, verification |
| `audit-report.v3.schema.json` | Auditor: verdict, `acceptance_check`, findings, regression, rework/escalation |
| `specialist-report.v3.schema.json` | Optional specialists: advisory `S` findings and the researcher brief |

The schemas express single-object rules (for example: a PASS has no `not_met` row, a behavioral `met` needs transcript or executed evidence, revision 0 has empty `addresses`). `tools/validate_examples.py` adds the cross-object rules: one acceptance row per handoff criterion, the `evidence_required` → FAIL rule, the `Static-only` summary prefix, rework tracking, previous-report continuity, closed-ID reuse, monotonic IDs, `addresses` = prior `must_fix`, and specialist task/revision matching. The normative prose is in `../contract.md`.
