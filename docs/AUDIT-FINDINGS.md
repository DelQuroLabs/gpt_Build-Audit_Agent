# Closed finding ledger

All seven findings are closed in 3.2.0. IDs belong to this external prompt audit; they are distinct from the package's illustrative F1/F2 protocol IDs. Baseline locators refer to commit e1aa678; final locators refer to the delivered files. Severity uses the attached auditor's scale, including POLISH (none found).

## [MAJOR] F-01 - Incomplete input can collide with mandatory report output

Location: baseline builder-gpt.md Shared protocol and Output format; auditor-gpt.md Protocol and scope and Output format.

Evidence: Observed: Builder says every build/rework ends with valid JSON while permitting missing/oversized inputs; Auditor says use task_id "adhoc" when a handoff is missing and still requires a completed report. `absent: no mention of a distinct non-report response for absent target, missing schema, or invalid rework state; affects Inputs, Output, Exceptions`. Inferred: an empty/incomplete submission can receive invented identity, artifacts, or an unsupported verdict. Unverified: actual model responses.

Impact: misleading completed handoffs/audits and reset history.

Root cause: no precedence-defined early output states.

Recommended fix: define early states before normal output and restrict ad hoc to complete initial reviews.

Replacement text: "Early responses contain no handoff/report JSON, no verdict, and consume no revision or round." Installed in contract section 8 and both core intake sections.

Verification: B2/B3/A3/A4/A8/A9 manual cases have explicit pass/fail outcomes; static trace confirms correct branches and no handoff exception conflict. Live behavior unverified.

Effort: M. Pass 2 FIXED; Pass 3 FIXED.

## [MAJOR] F-02 - Finding history rules contradict validator behavior

Location: baseline auditor-gpt.md Regression check; contract invariants 5/10; tools/validate_examples.py protocol_errors; examples/audit-escalation.v2.json.

Evidence: Observed: prompt demands every "must-fix, deferred, and frozen ID" while validator requires exactly prior must_fix/deferred. It accepts a fixed finding left active and arbitrary frozen IDs; closed regressions conflict with ID reuse prohibition. Observed execution: focused assertions reproduced all these paths plus missing minor history. Inferred: correct reports rejected and inconsistent history accepted.

Impact: broken third-round handoff or falsely closed unresolved findings.

Root cause: prompts, examples, and validator implement different lifecycle rules.

Recommended fix: one complete historical union, disjoint active/frozen states, evidenced closure, Auditor-owned IDs, and fresh IDs for closed regressions.

Replacement text: "Every later report's regression_check contains exactly one row for each ID in the union of the previous report's findings, regression rows, must_fix, deferred, and frozen entries." See contract section 9 for closure and human-overrule handling.

Verification: frozen-history positive/omission negative, fixed-active, invented-frozen, minor-history, new-regression, closed-reuse, and linked CLI tests pass. Complete final example retains F1 and F2.

Effort: M. Pass 2 FIXED; Pass 3 FIXED.

## [MAJOR] F-03 - Specialists depend on unavailable shared instructions

Location: baseline specialists/ux-gpt.md Output, other role Output sections, researcher-gpt.md, gpt-config.json optional_specialists.

Evidence: Observed: "Same section structure as Security specialist" and "Standard specialist sections" refer to files not loaded by the prescribed setup. Several installed role sources lack explicit injection/privacy/tool controls. Inferred: incomplete report structure and inconsistent treatment of submitted instructions across roles. Unverified: live outputs.

Impact: unsafe or unusable advisory reports despite valid-looking role configuration.

Root cause: shared behavior is referenced but not installed.

Recommended fix: assemble a required common block with each role, with consistent schema, permissions, evidence, early states, and output rules.

Replacement text: "Install the complete dist/instructions/<role>.md file, which combines common.md with the role source." The common source is included in full in each generated prompt.

Verification: package tests assert every specialist installation file includes the complete common block and matches its sources; all required reference paths exist. S1-S3 are fixed live acceptance cases, not claimed executions.

Effort: M. Pass 2 FIXED; Pass 3 FIXED.

## [MAJOR] F-04 - Reviewer tool availability is confused with authorization

Location: baseline gpt-config.json capability notes, auditor-gpt.md trust boundary, specialists/researcher-gpt.md Capabilities note.

Evidence: Observed: configuration suggests enabling capabilities when the target GPT spec requires them; Researcher says "If Web Search is enabled ... use it"; Auditor permits safe self-contained checks without a concrete execution budget. `absent: no mention of bounded attempts/time for the reviewing agents' own checks; affects Authority, Exceptions`. Inferred: product requirements or tool availability can be mistaken for permission to act.

Impact: unintended execution/retrieval or repeated work beyond the user's review scope.

Root cause: reviewing-agent authority and target-product capability are not separated.

Recommended fix: default tools off; require caller scope, host permission, inspected isolated execution, bounded attempts/time, and explicit no-tool fallback.

Replacement text: "Requested capabilities of the product being built do not authorize the Builder, Auditor, or specialists to use their own tools." Contract section 10 supplies budgets and no external-write behavior.

Verification: configuration tests confirm all capability defaults false; static trace of T1/T2/S2 covers untrusted command, launch failure, and unavailable research paths. Live permission behavior remains unverified.

Effort: M. Pass 2 FIXED; Pass 3 FIXED.

## [MINOR] F-05 - JSON parsing and diagnostic output are not robust

Location: baseline tools/validate_examples.py load_json, schema_errors, and CLI error handlers.

Evidence: Observed execution: duplicate keys and NaN accepted; invalid text encoding produces a traceback. Pass 2 observation: schema diagnostics interpolate invalid submitted values. Inferred: ambiguous packet interpretation and potential value disclosure in logs. Tests use synthetic markers only.

Impact: bounded validation unreliability and unnecessary diagnostic exposure.

Root cause: default permissive parsing and raw validator diagnostics.

Recommended fix: strict unique-key/finite-JSON parsing, bounded input, clean decoding/depth errors, and constraint-only diagnostics before semantic checks of valid objects.

Replacement text: load_json rejects duplicate keys/nonstandard constants and input over 2 MiB; schema_errors reports constraint/location and missing schema-defined fields without submitted values.

Verification: strict parsing, invalid encoding, byte limit, invalid enum/ID redaction, malformed-type checks, and CLI tests pass.

Effort: S. Pass 2 PARTIALLY ADDRESSED (diagnostic exposure remained); Pass 3 FIXED.

## [MAJOR -> MINOR] F-06 - GPT calibration is not reproducible from complete inputs

Location: baseline SMOKE-TEST.md Correct-sample/Seeded-defect/Optional specialist flow; examples/specialist-researcher.v2.json.

Evidence: Observed: smoke instructions ask the operator to supply a correct package and refer to a session-cookie fixture whose complete source packet is absent. Research sample calls assumptions "Documented" while asking the reader to verify them. Inferred: operators cannot reproduce the intended positive/negative GPT checks and can confuse shape fixtures with verified facts.

Impact: failure to detect wrong PASS/FAIL behavior; overstated evidence.

Root cause: illustrative outcomes substitute for fixed complete inputs and provenance.

Recommended fix: supply complete good/bad GPT packets, exact behavioral cases, and explicit synthetic/unverified labeling on historical JSON examples.

Replacement text: "The historical JSON examples demonstrate payload shape; they are not complete Builder responses or proof of the quoted external sources." The researcher sample now prefixes unverified facts and does not claim retrieval.

Verification: good/bad packets have schema-valid handoffs and complete snapshots; negative fixture equals exactly its declared mutation; A1/A2 provide criterion-level expectations. Final researcher example inspected for accurate evidence labels. Live cases not run.

Effort: M. Pass 2 PARTIALLY ADDRESSED and reduced to MINOR (only stale research evidence wording remained); Pass 3 FIXED.

## [MINOR] F-07 - Installation guidance has no checked complete prompt artifact

Location: baseline README.md Setup, SETUP.md, role-file paste comments, gpt-config.json.

Evidence: Observed: original instruction bodies measured 9,914 and 11,252 characters; setup lacks a checked size budget and specialist source markers say to paste incomplete role files. Actual host limits are Unverified, so no claim of a proven platform-limit violation is made.

Impact: avoidable manual truncation or incomplete installation.

Root cause: no generated, completeness-checked installation output or single installation path.

Recommended fix: assemble complete artifacts with a conservative package budget, test drift, and direct setup to those artifacts; label role sources as source-only.

Replacement text: "Paste each file's entire contents, without adding its source files again." SETUP.md requires actual-host preflight and explains the 7,500-character package budget is not a platform assertion.

Verification: all eight generated prompts match sources and fit budget; source-only markers no longer direct incomplete specialist installation. Manual host setup remains unverified.

Effort: S. Pass 2 PARTIALLY ADDRESSED (source headers remained misleading); Pass 3 FIXED.
