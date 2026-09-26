# Kickoff — GPT Builder, initial revision 0

Fill every relevant field. Keep the spec to one canonical sentence; put measurable behavior in acceptance criteria. Attach or paste complete current artifacts and platform context.

---

task_id: <short-kebab-id>
build_revision: 0

## Spec

<one sentence: build or change what GPT for which audience, with what inputs/outputs and main constraint>

## Audience and job

<who uses it, what they are trying to accomplish, and what success looks like>

## Acceptance criteria

1. <observable behavior or artifact requirement>
2. <observable behavior or artifact requirement>

## Non-goals

- <explicitly out of scope>

## Constraints and standards

- Platform/editor/plan:
- Required language, tone, accessibility, and output format:
- Privacy, safety, compliance, or human-approval requirements:
- Knowledge sources, owners, freshness, and citation rules:
- Capabilities/actions allowed or prohibited:
- Dependencies or integrations allowed/prohibited:

## Current context and artifacts

<for each path: give the path, purpose, and complete contents. Include current GPT config, instructions, Knowledge docs, Action schemas, evals, transcripts, or relevant unchanged interfaces.>

## Verification requirements

<required evals, live-platform checks, schema checks, or project commands; otherwise say not specified>

## Mode

<build by default; use plan-only for a design without artifacts. Build mode proposes the package; it does not authorize external execution, writes, or publication.>

Proceed with the task. For a complete build, return full changed artifacts and a `build-audit-handoff` v2 JSON block. Apply early response states from contract.md when blocked; plan-only has no handoff.
