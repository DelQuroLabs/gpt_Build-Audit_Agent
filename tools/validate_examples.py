#!/usr/bin/env python3
"""Validate Build <-> Audit v3 objects: bundled fixtures or a real packet.

Requires `jsonschema` (see tools/requirements.txt).

With no arguments, runs every positive and negative case in examples/manifest.json.
To validate a generated object, pass a .json file or a complete .md response; for
.md input the last fenced ```json block is used:

    python tools/validate_examples.py builder-response.md
    python tools/validate_examples.py builder-response.md --previous-report prior-audit.json
    python tools/validate_examples.py audit.json --handoff builder-response.md
    python tools/validate_examples.py audit.json --handoff h.json --previous-report prior.json
    python tools/validate_examples.py audit.json --handoff h.json --specialist security.json
    python tools/validate_examples.py specialist.json --handoff builder-response.md

Exit codes: 0 valid, 1 invalid, 2 unreadable input.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "build-audit-handoff": ROOT / "schemas/build-audit-handoff.v3.schema.json",
    "audit-report": ROOT / "schemas/audit-report.v3.schema.json",
    "specialist-report": ROOT / "schemas/specialist-report.v3.schema.json",
}
MANIFEST = ROOT / "examples/manifest.json"
STOP_CONDITION = re.compile(r"^(F[1-9][0-9]*): .+$")
STATIC_PREFIX = re.compile(r"^Static-only: (\d+) of (\d+) criteria not verifiable\.")
FENCED_JSON = re.compile(r"```json\s*\n(.*?)\n```", re.S)


class InputError(Exception):
    """Raised when an input file cannot be read or parsed."""


def load_document(path: Path) -> Any:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise InputError(f"{path}: {exc}") from exc
    if path.suffix.lower() == ".md":
        blocks = FENCED_JSON.findall(text)
        if not blocks:
            raise InputError(f"{path}: no fenced ```json block found")
        text = blocks[-1]
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise InputError(f"{path}: invalid JSON: {exc}") from exc


def contract_of(instance: Any) -> str | None:
    if isinstance(instance, dict) and instance.get("contract") in SCHEMAS:
        return instance["contract"]
    return None


def schema_errors(label: str, instance: Any) -> list[str]:
    contract = contract_of(instance)
    if contract is None:
        return [f"{label}: unknown contract; expected one of {sorted(SCHEMAS)}"]
    schema = json.loads(SCHEMAS[contract].read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    errors = []
    for error in Draft202012Validator(schema).iter_errors(instance):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"{label} at {location}: {error.message}")
    return errors


def _ids(rows: Any, key: str) -> list[str]:
    if not isinstance(rows, list):
        return []
    return [row[key] for row in rows if isinstance(row, dict) and isinstance(row.get(key), str)]


def _num(finding_id: str) -> int | None:
    match = re.fullmatch(r"[FS]([1-9][0-9]*)", finding_id)
    return int(match.group(1)) if match else None


# --------------------------------------------------------------------------- handoff
def handoff_errors(label: str, h: dict, previous: Any = None) -> list[str]:
    errors: list[str] = []
    criteria = _ids(h.get("acceptance_criteria"), "id")
    if len(criteria) != len(set(criteria)):
        errors.append(f"{label}: acceptance criterion IDs must be unique")
    paths = _ids(h.get("artifacts"), "path")
    if len(paths) != len(set(paths)):
        errors.append(f"{label}: artifact paths must be unique")
    if previous is not None:
        if contract_of(previous) != "audit-report":
            return errors + [f"{label}: --previous-report must be an audit-report object"]
        if h.get("task_id") != previous.get("task_id"):
            errors.append(f"{label}: task_id does not match the previous report")
        prev_rev = previous.get("build_revision")
        if not isinstance(prev_rev, int) or h.get("build_revision") != prev_rev + 1:
            errors.append(f"{label}: build_revision must be the previous report's build_revision + 1")
        if previous.get("verdict") != "FAIL" or previous.get("audit_round") not in (1, 2):
            errors.append(f"{label}: rework requires a previous FAIL on audit 1 or 2")
        brief = previous.get("rework_brief")
        must_fix = set(brief.get("must_fix", [])) if isinstance(brief, dict) else set()
        addresses = set(h.get("addresses", []) or [])
        if addresses != must_fix:
            errors.append(
                f"{label}: addresses {sorted(addresses)} must equal the previous must_fix {sorted(must_fix)}"
            )
    return errors


# --------------------------------------------------------------------------- specialist
def specialist_errors(label: str, s: dict, handoff: Any = None) -> list[str]:
    errors: list[str] = []
    findings = s.get("findings", [])
    ids = _ids(findings, "id")
    if isinstance(findings, list) and len(ids) == len(findings) and len(ids) != len(set(ids)):
        errors.append(f"{label}: specialist finding IDs must be unique within the report")
    recommended = s.get("recommended_to_auditor", [])
    if isinstance(recommended, list):
        missing = sorted(set(x for x in recommended if isinstance(x, str)) - set(ids))
        if missing:
            errors.append(f"{label}: recommended_to_auditor references missing finding ID(s): {missing}")
    if handoff is not None:
        if (s.get("task_id"), s.get("build_revision")) != (handoff.get("task_id"), handoff.get("build_revision")):
            errors.append(f"{label}: specialist task_id/build_revision do not match the Builder handoff")
    return errors


# --------------------------------------------------------------------------- audit
def audit_errors(
    label: str,
    a: dict,
    previous: Any = None,
    handoff: Any = None,
    specialists: list[tuple[str, Any]] | None = None,
    require_previous: bool = False,
) -> list[str]:
    errors: list[str] = []
    findings = a.get("findings", [])
    if not isinstance(findings, list) or any(not isinstance(f, dict) for f in findings):
        return errors
    by_id = {f["id"]: f for f in findings if isinstance(f.get("id"), str)}
    if len(by_id) != len(findings):
        errors.append(f"{label}: finding IDs must be present and unique")
    severe = {fid for fid, f in by_id.items() if f.get("severity") in {"BLOCKER", "MAJOR"}}

    round_ = a.get("audit_round")
    if isinstance(round_, int) and a.get("build_revision") != round_ - 1:
        errors.append(f"{label}: build_revision must equal audit_round - 1")
    if round_ == 1 and a.get("regression_check"):
        errors.append(f"{label}: audit 1 must have an empty regression_check")

    # Acceptance check.
    rows = [r for r in a.get("acceptance_check", []) if isinstance(r, dict)]
    row_ids = [r.get("criterion_id") for r in rows]
    if len(row_ids) != len(set(row_ids)):
        errors.append(f"{label}: acceptance_check criterion IDs must be unique")
    not_met = [r.get("criterion_id") for r in rows if r.get("result") == "not_met"]
    if not_met and not severe:
        errors.append(f"{label}: not_met criteria {not_met} require at least one BLOCKER/MAJOR finding")
    unverifiable = [r for r in rows if r.get("result") == "not_verifiable"]
    if a.get("verdict") in {"PASS", "PASS_WITH_NOTES"} and unverifiable:
        match = STATIC_PREFIX.match(a.get("summary", ""))
        if not match or (int(match.group(1)), int(match.group(2))) != (len(unverifiable), len(rows)):
            errors.append(
                f"{label}: summary must begin 'Static-only: {len(unverifiable)} of {len(rows)} criteria not verifiable.'"
            )

    if handoff is not None:
        if contract_of(handoff) != "build-audit-handoff":
            errors.append(f"{label}: --handoff must be a build-audit-handoff object")
        else:
            if (a.get("task_id"), a.get("build_revision")) != (handoff.get("task_id"), handoff.get("build_revision")):
                errors.append(f"{label}: task_id/build_revision do not match the Builder handoff")
            criteria = [c for c in handoff.get("acceptance_criteria", []) if isinstance(c, dict)]
            expected = [(c.get("id"), c.get("kind")) for c in criteria]
            actual = [(r.get("criterion_id"), r.get("kind")) for r in rows]
            if expected != actual:
                errors.append(
                    f"{label}: acceptance_check must have one row per handoff criterion, in order, with matching kind; "
                    f"expected {expected}, got {actual}"
                )
            gap_findings = [f for f in findings if f.get("category") == "verification_gap"
                            and f.get("severity") in {"BLOCKER", "MAJOR"}]
            required = {c.get("id") for c in criteria if c.get("evidence_required") is True}
            for r in unverifiable:
                if r.get("criterion_id") in required and (a.get("verdict") != "FAIL" or not gap_findings):
                    errors.append(
                        f"{label}: evidence_required criterion {r.get('criterion_id')} is not_verifiable; "
                        "verdict must be FAIL with a BLOCKER/MAJOR verification_gap finding"
                    )

    for spec_label, report in specialists or []:
        if contract_of(report) != "specialist-report":
            errors.append(f"{label}: {spec_label} is not a specialist-report object")
            continue
        listed = f"specialist-report:{report.get('specialist')}" in " ".join(
            a.get("scope_review", {}).get("reviewed_paths", []))
        matches = (report.get("task_id"), report.get("build_revision")) == (a.get("task_id"), a.get("build_revision"))
        if listed and not matches:
            errors.append(f"{label}: accepted specialist report {spec_label} has a different task_id/build_revision")

    brief = a.get("rework_brief")
    if isinstance(brief, dict):
        must_fix = [x for x in brief.get("must_fix", []) if isinstance(x, str)]
        deferred = [x for x in brief.get("deferred", []) if isinstance(x, str)]
        for fid in must_fix + deferred:
            if fid not in by_id:
                errors.append(f"{label}: rework ID {fid} is absent from findings")
            elif fid not in severe:
                errors.append(f"{label}: rework ID {fid} is not BLOCKER/MAJOR")
        if set(must_fix) & set(deferred):
            errors.append(f"{label}: IDs cannot be both must_fix and deferred: {sorted(set(must_fix) & set(deferred))}")
        untracked = severe - set(must_fix) - set(deferred)
        if untracked:
            errors.append(f"{label}: unresolved BLOCKER/MAJOR IDs omitted from rework tracking: {sorted(untracked)}")
        conditions = [c for c in brief.get("stop_conditions", []) if isinstance(c, str)]
        cond_ids = [m.group(1) for c in conditions if (m := STOP_CONDITION.fullmatch(c))]
        if len(cond_ids) != len(conditions):
            errors.append(f"{label}: each stop condition must use `F<n>: <observable check>` format")
        if len(cond_ids) != len(set(cond_ids)) or sorted(cond_ids) != sorted(must_fix):
            errors.append(f"{label}: provide exactly one stop condition for each must_fix ID")

    regression = [r for r in a.get("regression_check", []) if isinstance(r, dict)]
    reg_ids = [r.get("finding_id") for r in regression if isinstance(r.get("finding_id"), str)]
    if len(reg_ids) != len(set(reg_ids)):
        errors.append(f"{label}: regression_check finding IDs must be unique")

    if require_previous and round_ in (2, 3) and previous is None:
        errors.append(f"{label}: provide the immediately previous audit report with --previous-report")

    if previous is not None:
        if contract_of(previous) != "audit-report":
            return errors + [f"{label}: --previous-report must be an audit-report object"]
        prev_round = previous.get("audit_round")
        if a.get("task_id") != previous.get("task_id"):
            errors.append(f"{label}: task_id does not match the previous report")
        if prev_round not in (1, 2) or round_ != prev_round + 1:
            errors.append(f"{label}: audit_round must immediately follow a previous FAIL on round 1 or 2")
        if previous.get("verdict") != "FAIL":
            errors.append(f"{label}: the previous report must have verdict FAIL to continue rework")
        prev_brief = previous.get("rework_brief")
        if not isinstance(prev_brief, dict):
            return errors + [f"{label}: the previous FAIL report must contain a rework_brief"]
        prior_ids = [x for x in prev_brief.get("must_fix", []) + prev_brief.get("deferred", []) if isinstance(x, str)]
        if set(reg_ids) != set(prior_ids) or len(reg_ids) != len(prior_ids):
            errors.append(f"{label}: regression_check must contain exactly one status for every prior must_fix/deferred ID")
        status = {r.get("finding_id"): r.get("status") for r in regression}
        for fid in prior_ids:
            if status.get(fid) in {"open", "reopened", "not_verifiable"} and fid not in by_id:
                errors.append(f"{label}: prior {status.get(fid)} finding {fid} must remain in current findings")
        history = set(_ids(previous.get("findings"), "id")) | set(_ids(previous.get("regression_check"), "finding_id"))
        closed = {r.get("finding_id") for r in previous.get("regression_check", [])
                  if isinstance(r, dict) and r.get("status") == "fixed"}
        for row in prev_brief.get("frozen", []):
            if isinstance(row, dict) and isinstance(row.get("id"), str):
                history.add(row["id"])
                closed.add(row["id"])
        history.update(prior_ids)
        reused = set(by_id) & closed
        if reused:
            errors.append(f"{label}: reuses previously closed finding ID(s): {sorted(reused)}")
        numbers = [n for i in history if (n := _num(i)) is not None]
        if numbers:
            top = max(numbers)
            low = sorted(i for i in set(by_id) - history if (n := _num(i)) is not None and n <= top)
            if low:
                errors.append(f"{label}: new finding ID(s) must be greater than prior ID F{top}: {low}")
    return errors


# --------------------------------------------------------------------------- driver
def validate(
    label: str,
    instance: Any,
    previous: Any = None,
    handoff: Any = None,
    specialists: list[tuple[str, Any]] | None = None,
    require_previous: bool = False,
) -> list[str]:
    errors = schema_errors(label, instance)
    contract = contract_of(instance)
    if contract == "build-audit-handoff":
        errors += handoff_errors(label, instance, previous)
    elif contract == "audit-report":
        errors += audit_errors(label, instance, previous, handoff, specialists, require_previous)
    elif contract == "specialist-report":
        errors += specialist_errors(label, instance, handoff)
        if previous is not None:
            errors.append(f"{label}: --previous-report cannot be used with a specialist report")
    return errors


def _load_optional(value: str | None) -> Any:
    return load_document(ROOT / value) if value else None


def run_manifest() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    errors: list[str] = []
    for case in manifest["positive"]:
        label = case["file"]
        specialists = [(s, load_document(ROOT / s)) for s in case.get("specialists", [])]
        previous = _load_optional(case.get("previous"))
        if previous is not None:
            errors += validate(f"{case['previous']} (as previous)", previous)
        errors += validate(label, load_document(ROOT / label), previous,
                           _load_optional(case.get("handoff")), specialists)
    for case in manifest["negative"]:
        label = case["file"]
        specialists = [(s, load_document(ROOT / s)) for s in case.get("specialists", [])]
        observed = validate(label, load_document(ROOT / label), _load_optional(case.get("previous")),
                            _load_optional(case.get("handoff")), specialists)
        if not any(case["expect"] in e for e in observed):
            errors.append(f"{label}: expected rejection containing {case['expect']!r}; observed {observed or 'no errors'}")
    if errors:
        print("Invalid document(s):")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"Validated {len(manifest['positive'])} positive cases and "
          f"{len(manifest['negative'])} expected-rejection cases against the v3 schemas and protocol rules.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("file", nargs="?", type=Path, help="Handoff, audit report, or specialist report (.json or .md)")
    parser.add_argument("--previous-report", type=Path, help="Immediately previous audit report (rework rounds)")
    parser.add_argument("--handoff", type=Path, help="Builder handoff the report refers to (.json or .md)")
    parser.add_argument("--specialist", type=Path, action="append", default=[],
                        help="Specialist report supplied to the Auditor (repeatable)")
    args = parser.parse_args(argv)
    try:
        if args.file is None:
            if args.previous_report or args.handoff or args.specialist:
                parser.error("options require a file")
            return run_manifest()
        instance = load_document(args.file)
        previous = load_document(args.previous_report) if args.previous_report else None
        handoff = load_document(args.handoff) if args.handoff else None
        specialists = [(str(p), load_document(p)) for p in args.specialist]
    except InputError as exc:
        print(f"Could not read input: {exc}", file=sys.stderr)
        return 2
    errors = []
    if previous is not None:
        errors += validate(f"{args.previous_report} (as previous)", previous)
    errors += validate(str(args.file), instance, previous, handoff, specialists,
                       require_previous=contract_of(instance) == "audit-report")
    if errors:
        print("Invalid document(s):")
        for e in errors:
            print(f" - {e}")
        return 1
    print(f"Validated {args.file} against its v3 schema and protocol rules.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
