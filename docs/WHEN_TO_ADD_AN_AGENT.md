# When to add an agent

This package defaults to **two GPTs**: Builder and Auditor. Extra GPTs are optional specialists under `specialists/`.

## The bar (all must pass)

1. **Named failure mode.** In one sentence: without this agent, GPT packages systematically ship with problem X.
2. **Distinct evidence.** It sees something the Auditor's general pass tends to miss.
3. **Observable trigger.** A signal written in `specialists/TRIGGERS.md` that a human can check in the Builder packet.
4. **Typed output.** `specialist-report` v3 only.
5. **Exit criterion.** You know when it is done for the current revision.
6. **Non-writer, non-verdict.** It never produces a package and never issues PASS or FAIL.

If any item fails, extend `standards.template.md`, `auditor-reference.md`, or the smoke fixtures instead of adding a GPT.

## Agents that usually do not earn their place

| Tempting role | Why skip |
|---|---|
| Second Auditor | Same evidence class; tighten the Auditor and standards instead |
| Style or tone bot | Put tone rules in the behavior contract and evals |
| Prompt "polisher" | No trigger; it fights the smallest-change rule |
| Project-manager GPT | The human and the kickoff template already scope the task |
| Summary-only manager | The human copies packets; a summary adds no new evidence |

## Adding one

1. Write `specialists/<role>-gpt.md` with the Common specialist rules block (copy it from any existing specialist).
2. Add the role to the `specialist` enum in `schemas/specialist-report.v3.schema.json`.
3. Add a trigger row to `TRIGGERS.md`, a profile to `gpt-config.json`, and a positive example to `examples/manifest.json`.
4. Run `python tools/validate_examples.py` and `python tools/check_package.py`.
