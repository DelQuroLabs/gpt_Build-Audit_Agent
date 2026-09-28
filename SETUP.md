# Setup Guide - GPT Build <-> Audit Pair 3.2.2

This is a manual, human-supervised pair of private agents. The package proposes and audits GPT design artifacts; it does not install a target GPT, run an unattended loop, or publish anything.

## 1. Check the host

Confirm your actual platform supports installing private instructions and loading reference files. Editor labels, availability, and limits are host-dependent; live setup is not verified by this package. If the required features are absent, stop setup or choose a compatible host explicitly. Never truncate a prompt or assume Knowledge was retrieved.

The complete ready-to-paste prompts are in `dist/instructions/`. Paste each file's entire contents, without adding its source files again. All are within this package's conservative 7,500-character budget; verify the host's actual limit too. `gpt-config.json` records the source and installation paths. Tools default off.

## 2. Configure the core pair

Complete `standards.template.md` as `standards.md`; use `not specified` for optional fields. No credentials or private personal data. Unspecified standards impose no extra requirements.

| Role | Complete Instructions file | Required references |
|---|---|---|
| Builder | dist/instructions/builder.md | contract.md; schemas/build-audit-handoff.v2.schema.json |
| Auditor | dist/instructions/auditor.md | contract.md; schemas/build-audit-handoff.v2.schema.json; schemas/audit-report.v2.schema.json |
| Auditor with specialists | same Auditor file | also schemas/specialist-report.v2.schema.json |

Use names, descriptions, and starters from `gpt-config.json`. Supply completed standards to both roles. Keep sharing private. Attach references as Knowledge where supported, or supply their complete contents in the session. Before a task, confirm the role can access the required references; otherwise it must return CONFIG REQUIRED.

Leave browsing, execution, Actions, image generation, and Canvas off. Enable an optional tool only for an explicitly authorized review check and supported isolation/limits. A capability requested for the target GPT does not authorize the reviewing agents. Static review is valid and must not be called a live test.

## 3. Calibrate and operate

Run the fixed inputs in `SMOKE-TEST.md` and `evals/README.md`. Retain actual transcripts separately from static package checks. All applicable behavioral cases must pass before sharing a configured instance.

1. Send `prompts/kickoff.md` to Builder; receive the full revision-0 packet.
2. Send the entire packet through `prompts/audit-request.md`.
3. For FAIL on audit 1 or 2, send the complete latest packet, original criteria, and full latest report through `prompts/rework.md`.
4. Preserve all history, including frozen/minor IDs. Audit 3/revision 2 is final. Use `prompts/escalate.md` if it fails.
5. Early responses (INPUT REQUIRED, CONFIG REQUIRED, CAPACITY LIMIT, PLAN ONLY, SAFE ALTERNATIVE, ROUND LIMIT) do not consume rounds or emit completed JSON.
6. Release remains a human decision after live target testing. A model PASS is not deployment approval.

## 4. Optional specialists

Use `specialists/TRIGGERS.md`; choose only useful roles, usually at most two. The complete prompts in `dist/instructions/{security,ux,perf,data,release,researcher}.md` already include `specialists/common.md`. Do not install a role source by itself.

Each specialist requires `contract.md` and `schemas/specialist-report.v2.schema.json`. Use the same complete Builder packet/task/revision. Feed its advisory report to the Auditor through `prompts/audit-request-with-specialists.md`, including the previous full report on later rounds. Specialists never own the verdict or assign F IDs.

Researcher browsing needs an authorized public-source question and host support; otherwise facts remain Unverified. No private packet text in searches. Other specialist tools remain off.

## 5. Local verification and maintenance

Python 3.10+ is required for the scripts. From the repository root:

```sh
python -m pip install -r tools/requirements.txt
python tools/package_instructions.py --check
python tools/validate_examples.py
python -m unittest discover -s tests -v
```

To edit prompts, change the source files named in `gpt-config.json`, then run `python tools/package_instructions.py`; commit source and generated files together. Never edit generated installation files alone. Changes to the positive GPT fixture require `python tools/build_calibration.py` to regenerate its one-defect companion.

The validator checks protocol objects and history, not agent judgment or live behavior. Supply `--previous-report prior.json` for later audit reports. Older v2 packets with incomplete frozen/minor history need correction; field shapes remain v2. Preserve prior artifacts and transcripts for rollback and repeat the live evals after host or prompt changes.
