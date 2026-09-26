# Kickoff: GPT Builder, revision 0

Fill in every relevant field. Keep the spec to one sentence and put measurable behavior in the acceptance criteria. Paste complete current artifacts and platform context. Never paste secrets or personal data.

---

task_id: <short-kebab-id>
build_revision: 0

## Spec

<one sentence: which GPT, for which audience, with what inputs/outputs and main constraint>

## Audience and job

<who uses it, what they are trying to do, what success looks like>

## Acceptance criteria

| ID | Criterion (observable) | kind | evidence_required |
|---|---|---|---|
| AC1 | <artifact or behavior requirement> | artifact / behavioral | false / true |
| AC2 | <…> | | |

- `artifact`: checkable in the files (instructions, config, evals).
- `behavioral`: runtime GPT behavior. It is `met` only with a transcript or executed check.
- `evidence_required: true`: the audit FAILs unless a transcript or executed check demonstrates the criterion.

## Non-goals

- <explicitly out of scope>

## Constraints and standards

- Platform/editor/plan (Custom GPT Instructions limit: 8,000 characters):
- Language, tone, accessibility, and output format:
- Privacy, safety, compliance, or human-approval requirements:
- Knowledge sources, owners, freshness, and citation rules:
- Capabilities and Actions allowed or prohibited:
- Integrations allowed or prohibited:

## Current context and artifacts

<for each path: purpose and complete contents (current config, instructions, Knowledge, Action schemas, evals, transcripts), or `None (new GPT)`>

## Verification requirements

<required evals, live-platform checks, or transcripts; otherwise `not specified`>

## Mode

<`build` (default) or `plan-only`>

Proceed. Return the complete contents of every changed artifact and a `build-audit-handoff` v3 JSON block.
