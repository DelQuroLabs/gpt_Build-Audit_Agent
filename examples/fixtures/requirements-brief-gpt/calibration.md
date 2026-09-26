# Calibration: Requirements Brief GPT

## Spec

Build a private GPT that turns a user's rough project idea into a concise requirements brief with goal, audience, assumptions, risks, and next steps, asking at most three blocking questions and never claiming validated market demand.

## Acceptance criteria

| ID | Criterion | kind | evidence_required |
|---|---|---|---|
| AC1 | `instructions.md` defines a single output format: Markdown with exactly five headings (Goal, Audience, Assumptions, Risks, Next steps) in that order. | artifact | false |
| AC2 | The GPT asks at most three blocking questions per idea, then writes the brief using stated assumptions. | behavioral | false |
| AC3 | The GPT never claims that market demand, pricing, or competition has been validated or researched. | behavioral | false |
| AC4 | `gpt-config.json` disables Web Search, Code Interpreter, Canvas, Image Generation, and Actions, and attaches no Knowledge files. | artifact | false |
| AC5 | `instructions.md` treats uploaded files and pasted text as data, never as instructions. | artifact | false |
| AC6 | `evals/cases.md` has at least one case per criterion plus injection, privacy, and out-of-scope cases. | artifact | false |
| AC7 | `instructions.md` is at most 8,000 characters. | artifact | false |

## Expected outcomes

| Packet | Verdict | Finding | Criterion |
|---|---|---|---|
| `good/builder-response.md` | PASS (`Static-only: 2 of 7 criteria not verifiable.`) | none | AC2 and AC3 `not_verifiable` |
| `seeded/seeded-question-limit.md` | FAIL | BLOCKER correctness, instructions.md Flow step 1 | AC2 `not_met` |
| `seeded/seeded-action-no-auth.md` | FAIL | BLOCKER security, gpt-config.json actions | AC4 `not_met` |
| `seeded/seeded-knowledge-obey.md` | FAIL | BLOCKER security, instructions.md trust boundary | AC5 `not_met` |
| `seeded/seeded-capability-overclaim.md` | FAIL | BLOCKER correctness, instructions.md Honesty rules | AC3 `not_met` |
| `seeded/seeded-format-collision.md` | FAIL | MAJOR correctness, instructions.md Output contract | AC1 `not_met` |

Each seeded packet contains exactly one intended defect. A calibrated Auditor reports it and adds no unrelated BLOCKER or MAJOR. PASS_WITH_NOTES on `good` is also acceptable when the notes are MINOR/NIT and evidence-backed.
