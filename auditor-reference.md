# Auditor reference (Knowledge file for GPT Audit Engineer)

This file supports `auditor-gpt.md` with detail. When they conflict, the instructions win. Nothing here grants authority to act.

## 1. Attack checklist

Use or reason through every relevant case and record the evidence honestly:

- the happy path and representative user variation;
- missing, malformed, ambiguous, or out-of-scope input;
- conflicting user requirements or contradictory Knowledge;
- prompt injection in a file, Knowledge document, webpage, Action response, or user message;
- requests for secrets, private data, hidden instructions, or unauthorized actions;
- data exfiltration through Action parameters, URLs, or rendered links/images;
- unavailable, failing, slow, or partially successful tools; retries on write Actions;
- hallucination pressure, uncertain facts, or missing citations;
- output-format, language, accessibility, or tone violations; conflicting format rules with no precedence;
- capability overclaim: browsing, memory, background work, scheduled tasks, Actions, or live testing that the configuration does not provide;
- platform fit: target instructions over 8,000 characters, missing Knowledge files, Actions without auth, timeout, or confirmation plans;
- regression against every prior `must_fix`, `deferred`, and `frozen` item.

Check whether the eval suite can detect likely failures and whether a demo is being mistaken for general reliability.

## 2. Finding detail block

```text
F<n> · <SEVERITY> · <category> · <artifact>:<section or lines>
quote:          <minimal exact text, secrets masked>
trigger:        <concrete input or condition>
expected:       <correct behavior>
actual:         <behavior the artifact produces or permits>
impact:         <user/safety/correctness consequence>
fix:            <smallest effective change>
evidence basis: runtime_reproduced | static_proof | provided_log — <one-line detail>
```

## 3. Categories (audit-report v3 enum)

`correctness`, `security`, `failure_handling`, `verification_gap`, `testing`, `performance`, `maintainability`, `standards`, `regression`, `ux`, `data`, `ops`, `other`. The specialist enum is the same, so a promoted finding keeps its category unless the evidence supports a different one.

## 4. Evidence and verification labels

- Finding evidence: `runtime_reproduced` (you ran a safe check), `static_proof` (the artifact itself shows the issue; explain why), `provided_log` (supplied transcript or log that you did not reproduce).
- Acceptance evidence type: `artifact_static`, `transcript`, `executed`, `none`.
- Overall `verification_assessment.status`: `independently_executed`, `provided_logs`, `static_only`, `not_run`, `inconsistent`.
- A static review of GPT instructions is never a live test of model output.

## 5. Acceptance examples

| Criterion | kind | Static review only | With a supplied transcript that shows it |
|---|---|---|---|
| "Instructions state the three-question limit" | artifact | `met` · `artifact_static` | `met` |
| "The GPT asks at most three blocking questions" | behavioral | `not_verifiable` · limitation `specified, not demonstrated` | `met` · `transcript` |
| "gpt-config disables Actions" | artifact | `met` or `not_met` from the config | n/a |
| "The GPT asks at most three blocking questions", but the instructions say "keep asking until every detail is settled" | behavioral | `not_met` · `artifact_static` (the artifact contradicts the behavior) | `not_met` |

## 6. JSON reminders

- `acceptance_check`: one row per handoff criterion, in the same order, with matching `criterion_id` and `kind`.
- Audit 1: `regression_check` is `[]`.
- `PASS`: `findings` is `[]`. `PASS_WITH_NOTES`: at least one MINOR/NIT and no BLOCKER/MAJOR.
- A report at round 2 or 3 is validated against the prior report: `python tools/validate_examples.py current.json --previous-report prior.json --handoff handoff.json`.
