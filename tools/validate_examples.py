#!/usr/bin/env python3
"""Validate bundled examples or a real Build ↔ Audit v2 packet/report.

Requires the optional `jsonschema` package. With no arguments, validates the
Builder, Auditor, and specialist examples. To validate a generated object, pass its JSON file. For an
audit round after the first, also pass the immediately previous audit report:

    python tools/validate_examples.py handoff.json
    python tools/validate_examples.py current-audit.json --previous-report prior-audit.json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "build-audit-handoff": ROOT / "schemas/build-audit-handoff.v2.schema.json",
    "audit-report": ROOT / "schemas/audit-report.v2.schema.json",
    "specialist-report": ROOT / "schemas/specialist-report.v2.schema.json",
}
EXAMPLES = [
    (ROOT / "examples/build-handoff.v2.json", None),
    (ROOT / "examples/audit-pass.v2.json", None),
    (ROOT / "examples/audit-notes.v2.json", None),
    (ROOT / "examples/audit-fail.v2.json", None),
    (ROOT / "examples/audit-rework.v2.json", ROOT / "examples/audit-fail.v2.json"),
    (ROOT / "examples/audit-escalation.v2.json", ROOT / "examples/audit-rework.v2.json"),
    (ROOT / "examples/specialist-security.v2.json", None),
    (ROOT / "examples/specialist-ux.v2.json", None),
    (ROOT / "examples/specialist-researcher.v2.json", None),
    (ROOT / "examples/audit-with-specialist-promotion.v2.json", None),
    (ROOT / "self-audit/audit-pass.v2.json", None),
]
NEGATIVE_EXAMPLES = [
    (ROOT / "self-audit/build-handoff.v2.json", None,
     "artifact paths must be canonical repository-relative"),
    (ROOT / "examples/invalid/audit-round1-regression.v2.json", None,
     "audit 1 must have an empty regression_check"),
    (ROOT / "examples/invalid/audit-closed-id-reuse.v2.json",
     ROOT / "examples/audit-rework.v2.json", "reuses previously closed finding ID(s)"),
    (ROOT / "examples/invalid/audit-not-verifiable-omitted.v2.json",
     ROOT / "examples/audit-rework.v2.json", "prior not_verifiable finding F2 must remain in current findings"),
    (ROOT / "examples/invalid/audit-nonmonotonic-id.v2.json",
     ROOT / "examples/invalid/audit-id-gap-reuse-prior.v2.json",
     "new finding ID(s) must be greater than prior ID F3"),
    (ROOT / "examples/invalid/specialist-researcher-missing-brief.v2.json", None,
     "research_brief"),
    (ROOT / "examples/invalid/specialist-orphan-recommendation.v2.json", None,
     "recommended_to_auditor references missing finding ID(s)"),
]
STOP_CONDITION = re.compile(r"^(F[1-9][0-9]*): .+$")


def load_json(path: Path) -> Any:
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate JSON object key")
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError("nonstandard JSON numeric constant")

    if path.stat().st_size > 2 * 1024 * 1024:
        raise ValueError("JSON input exceeds the 2 MiB validation limit")
    with path.open(encoding="utf-8-sig") as handle:
        return json.load(handle, object_pairs_hook=unique_object, parse_constant=reject_constant)


def get_schema(instance: Any) -> tuple[str, Path] | None:
    if not isinstance(instance, dict):
        return None
    contract = instance.get("contract")
    if not isinstance(contract, str):
        return None
    schema_path = SCHEMAS.get(contract)
    if schema_path is None:
        return None
    return contract, schema_path


def schema_errors(label: str, instance: Any, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    errors = []
    for error in validator.iter_errors(instance):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        # Validation diagnostics must not echo arbitrary submitted values.
        detail = f"failed {error.validator} constraint"
        if error.validator == "required" and isinstance(error.instance, dict):
            missing = [key for key in error.validator_value if key not in error.instance]
            detail += "; missing required fields: " + ", ".join(missing)
        errors.append(f"{label} at {location}: {detail}")
    return errors


def _rows(value: Any) -> list[dict]:
    return [row for row in value if isinstance(row, dict)] if isinstance(value, list) else []


def _ids(value: Any) -> list[str]:
    return [item for item in value if isinstance(item, str)] if isinstance(value, list) else []


def _id_order(value: str) -> tuple[int, str]:
    """Compare decimal IDs without Python's bounded string-to-int conversion."""
    match = re.fullmatch(r"F([1-9][0-9]*)", value)
    digits = match.group(1) if match else ""
    return len(digits), digits


def _is_integer(value: Any) -> bool:
    return Draft202012Validator.TYPE_CHECKER.is_type(value, "integer")


def _is_overrule(value: Any) -> bool:
    return (isinstance(value, str) and value.startswith("human-overruled:")
            and bool(value.removeprefix("human-overruled:").strip()))


def handoff_protocol_errors(label: str, instance: Any) -> list[str]:
    """Check portable file identity without accessing or resolving submitted paths."""
    if not isinstance(instance, dict) or instance.get("contract") != "build-audit-handoff":
        return []
    errors = []
    paths = []
    for row in _rows(instance.get("artifacts")):
        path = row.get("path")
        if not isinstance(path, str):
            continue  # The schema handles missing and non-string paths.
        paths.append(path)
        if (not path or "\\" in path or PureWindowsPath(path).drive
                or PurePosixPath(path).is_absolute()
                or any(part in ("", ".", "..") for part in path.split("/"))):
            errors.append(f"{label}: artifact paths must be canonical repository-relative paths using / separators")
    if len(paths) != len(set(paths)):
        errors.append(f"{label}: artifact paths must be unique; one operation per file")
    return errors


def protocol_errors(
    label: str,
    instance: Any,
    previous_report: Any = None,
    *,
    require_previous: bool = False,
) -> list[str]:
    """Validate identity, complete history, and transitions without executing payloads."""
    if not isinstance(instance, dict):
        return []
    if instance.get("contract") == "specialist-report":
        return specialist_protocol_errors(label, instance)
    if instance.get("contract") == "build-audit-handoff":
        return handoff_protocol_errors(label, instance)
    if instance.get("contract") != "audit-report":
        return []

    errors: list[str] = []

    def reject(message: str) -> None:
        errors.append(f"{label}: {message}")

    findings = _rows(instance.get("findings"))
    finding_ids = [row["id"] for row in findings if isinstance(row.get("id"), str)]
    by_id = dict(zip(finding_ids, [row for row in findings if isinstance(row.get("id"), str)]))
    if len(finding_ids) != len(findings) or len(set(finding_ids)) != len(finding_ids):
        reject("finding IDs must be present and unique")
    current_ids = set(finding_ids)
    audit_round = instance.get("audit_round")
    if _is_integer(audit_round) and instance.get("build_revision") != audit_round - 1:
        reject("build_revision must equal audit_round - 1")

    regression = _rows(instance.get("regression_check"))
    regression_ids = [row["finding_id"] for row in regression if isinstance(row.get("finding_id"), str)]
    regression_by_id = {row["finding_id"]: row for row in regression if isinstance(row.get("finding_id"), str)}
    if len(set(regression_ids)) != len(regression_ids):
        reject("regression_check finding IDs must be unique")
    if audit_round == 1 and regression:
        reject("audit 1 must have an empty regression_check")

    brief = instance.get("rework_brief")
    frozen_by_id: dict[str, dict] = {}
    if isinstance(brief, dict):
        must_fix = _ids(brief.get("must_fix"))
        deferred = _ids(brief.get("deferred"))
        frozen = _rows(brief.get("frozen"))
        frozen_ids = [row["id"] for row in frozen if isinstance(row.get("id"), str)]
        frozen_by_id = {row["id"]: row for row in frozen if isinstance(row.get("id"), str)}
        if len(set(frozen_ids)) != len(frozen_ids):
            reject("frozen finding IDs must be unique")
        if audit_round == 1 and frozen_ids:
            reject("audit 1 cannot freeze findings without prior history")
        if current_ids & set(frozen_ids):
            reject("frozen IDs cannot also be active findings")
        if set(must_fix) & set(deferred):
            reject("IDs cannot be both must_fix and deferred")
        for finding_id in must_fix + deferred:
            if finding_id not in by_id:
                reject(f"rework ID {finding_id} is absent from findings")
            elif by_id[finding_id].get("severity") not in ("BLOCKER", "MAJOR"):
                reject(f"rework ID {finding_id} is not BLOCKER/MAJOR")
        unresolved = {row["id"] for row in findings
                      if isinstance(row.get("id"), str) and row.get("severity") in ("BLOCKER", "MAJOR")}
        if unresolved - set(must_fix) - set(deferred):
            reject("unresolved BLOCKER/MAJOR IDs omitted from rework tracking")
        if instance.get("verdict") == "FAIL" and audit_round in (1, 2) and not must_fix:
            reject("FAIL on audit 1 or 2 must assign at least one ID to must_fix")
        conditions = _ids(brief.get("stop_conditions"))
        condition_ids = [m.group(1) for text in conditions if (m := STOP_CONDITION.fullmatch(text))]
        if len(condition_ids) != len(conditions):
            reject("each stop condition must use F<n>: <observable check> format")
        if len(condition_ids) != len(must_fix) or set(condition_ids) != set(must_fix):
            reject("provide exactly one stop condition for each must_fix ID")

    for row in regression:
        if row.get("status") == "fixed" and row.get("finding_id") in current_ids:
            reject("a fixed finding cannot remain active")
        finding_id = row.get("finding_id")
        reason = frozen_by_id.get(finding_id, {}).get("reason") if isinstance(finding_id, str) else None
        if _is_overrule(row.get("evidence")) or _is_overrule(reason):
            if row.get("status") != "not_verifiable":
                reject("human-overruled findings must use not_verifiable, not a technical-fix status")
            if row.get("finding_id") in current_ids:
                reject("human-overruled IDs cannot also be active findings")

    if previous_report is None:
        if require_previous and audit_round in (2, 3):
            reject("provide the immediately previous audit report with --previous-report")
        return errors
    if not isinstance(previous_report, dict) or previous_report.get("contract") != "audit-report":
        reject("--previous-report must be an audit-report object")
        return errors

    previous_round = previous_report.get("audit_round")
    previous_revision = previous_report.get("build_revision")
    if instance.get("task_id") != previous_report.get("task_id"):
        reject("task_id does not match the previous report")
    if not _is_integer(previous_round) or previous_round not in (1, 2) or audit_round != previous_round + 1:
        reject("audit_round must immediately follow a previous FAIL on round 1 or 2")
    if not _is_integer(previous_revision) or instance.get("build_revision") != previous_revision + 1:
        reject("build_revision must increase by exactly one from the previous report")
    if previous_report.get("verdict") != "FAIL":
        reject("the previous report must have verdict FAIL to continue rework")
    previous_brief = previous_report.get("rework_brief")
    if not isinstance(previous_brief, dict):
        reject("the previous FAIL report must contain a rework_brief")
        return errors

    prior_findings = {row["id"] for row in _rows(previous_report.get("findings"))
                      if isinstance(row.get("id"), str)}
    prior_regression = _rows(previous_report.get("regression_check"))
    prior_frozen = {row["id"] for row in _rows(previous_brief.get("frozen"))
                    if isinstance(row.get("id"), str)}
    prior_overruled = {
        row["id"] for row in _rows(previous_brief.get("frozen"))
        if isinstance(row.get("id"), str) and _is_overrule(row.get("reason"))
    }
    # A reopened row can still describe an active defect. Frozen history, not
    # that status alone, identifies a closed ID whose regression needs a new ID.
    prior_closed = prior_frozen | {
        row["finding_id"] for row in prior_regression
        if isinstance(row.get("finding_id"), str) and row.get("status") == "fixed"
    }
    history = prior_findings | prior_frozen | set(_ids(previous_brief.get("must_fix"))) | set(_ids(previous_brief.get("deferred")))
    history.update(row["finding_id"] for row in prior_regression if isinstance(row.get("finding_id"), str))
    if set(regression_ids) != history or len(regression_ids) != len(history):
        reject("regression_check must contain exactly one status for every prior finding, regression, and frozen ID")
    if current_ids & prior_closed:
        reject(f"reuses previously closed finding ID(s): {sorted(current_ids & prior_closed)}")
    highest_prior = max(history, key=_id_order, default="F0")
    new_ids = current_ids - history
    if any(_id_order(item) <= _id_order(highest_prior) for item in new_ids):
        reject(f"new finding ID(s) must be greater than prior ID {highest_prior}")

    for finding_id in history:
        row = regression_by_id.get(finding_id, {})
        status = row.get("status")
        if (finding_id in prior_overruled and status == "not_verifiable"
                and not (_is_overrule(row.get("evidence"))
                         or _is_overrule(frozen_by_id.get(finding_id, {}).get("reason")))):
            reject(f"prior human-overruled finding {finding_id} must retain its accepted-risk disclosure")
        if finding_id in prior_closed:
            if status == "open":
                reject("a closed finding requires a new ID and reopened status for a new regression")
            if status == "reopened":
                evidence = row.get("evidence", "")
                refs = set(re.findall(r"\bF[1-9][0-9]*\b", evidence)) if isinstance(evidence, str) else set()
                if not refs & new_ids:
                    reject(f"reopened closed finding {finding_id} must reference a new current finding ID in evidence")
        elif status in ("open", "reopened", "not_verifiable"):
            override = frozen_by_id.get(finding_id, {}).get("reason", "")
            overruled = (status == "not_verifiable"
                         and (_is_overrule(row.get("evidence")) or _is_overrule(override)))
            if finding_id not in current_ids and not overruled:
                reject(f"prior {status} finding {finding_id} must remain in current findings")

    if isinstance(brief, dict):
        expected_frozen = prior_closed | {
            item for item, row in regression_by_id.items()
            if row.get("status") == "fixed" or (
                row.get("status") == "not_verifiable" and _is_overrule(row.get("evidence")))
        }
        if expected_frozen - set(frozen_by_id):
            reject("rework_brief.frozen must retain closed history and newly fixed IDs")
        for finding_id, frozen in frozen_by_id.items():
            row = regression_by_id.get(finding_id, {})
            reason = frozen.get("reason", "")
            overruled = (row.get("status") == "not_verifiable" and _is_overrule(reason))
            if _is_overrule(row.get("evidence")) and not overruled:
                reject(f"frozen ID {finding_id} must retain its human-overruled decision")
            if finding_id not in history or (finding_id not in expected_frozen and not overruled):
                reject(f"frozen ID {finding_id} needs prior history and closure evidence")
    return errors


def specialist_protocol_errors(label: str, instance: Any) -> list[str]:
    """Check specialist finding identity and recommendation references."""
    if not isinstance(instance, dict) or instance.get("contract") != "specialist-report":
        return []

    errors: list[str] = []
    findings = instance.get("findings", [])
    if not isinstance(findings, list) or any(not isinstance(item, dict) for item in findings):
        return errors  # The JSON Schema reports malformed findings safely.

    finding_ids = [item.get("id") for item in findings if isinstance(item.get("id"), str)]
    if len(finding_ids) != len(findings):
        return errors  # The JSON Schema reports missing or malformed IDs.
    if len(finding_ids) != len(set(finding_ids)):
        errors.append(f"{label}: specialist finding IDs must be unique within the report")

    recommended = instance.get("recommended_to_auditor", [])
    if not isinstance(recommended, list) or any(not isinstance(item, str) for item in recommended):
        return errors  # The JSON Schema reports malformed recommendations safely.
    missing = sorted(set(recommended) - set(finding_ids))
    if missing:
        errors.append(f"{label}: recommended_to_auditor references missing finding ID(s): {missing}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path, help="A generated v2 handoff or audit report JSON file")
    parser.add_argument("--previous-report", type=Path,
                        help="The immediately previous audit report when validating audit round 2 or 3")
    args = parser.parse_args(argv)

    using_examples = args.file is None
    if using_examples and args.previous_report is not None:
        parser.error("--previous-report requires a generated audit report file")

    errors: list[str] = []
    documents: list[tuple[Path, Any, Any]] = []
    negative_documents: list[tuple[Path, Any, Any, str]] = []
    try:
        if using_examples:
            documents = [
                (path, load_json(path), load_json(previous_path) if previous_path else None)
                for path, previous_path in EXAMPLES
            ]
            negative_documents = [
                (path, load_json(path), load_json(previous_path) if previous_path else None, expected_error)
                for path, previous_path, expected_error in NEGATIVE_EXAMPLES
            ]
        else:
            documents = [(args.file, load_json(args.file), None)]
    except (OSError, ValueError, UnicodeError, RecursionError) as exc:
        print(f"Could not read JSON input: {exc}", file=sys.stderr)
        return 2

    previous: Any = None
    if args.previous_report is not None:
        try:
            previous = load_json(args.previous_report)
        except (OSError, ValueError, UnicodeError, RecursionError) as exc:
            print(f"Could not read previous report: {exc}", file=sys.stderr)
            return 2
        previous_schema = get_schema(previous)
        if previous_schema is None or previous_schema[0] != "audit-report":
            errors.append(f"{args.previous_report}: expected an audit-report JSON object")
        else:
            prior_schema_errors = schema_errors(str(args.previous_report), previous, previous_schema[1])
            errors.extend(prior_schema_errors)
            if not prior_schema_errors:
                errors.extend(protocol_errors(str(args.previous_report), previous))
        if errors:
            print("Invalid previous report:")
            for error in errors:
                print(f" - {error}")
            return 1

    if not using_examples and documents and args.previous_report is not None:
        path, instance, _ = documents[0]
        documents[0] = (path, instance, previous)

    for path, instance, example_previous in documents:
        schema_info = get_schema(instance)
        if schema_info is None:
            errors.append(f"{path}: unknown contract; expected build-audit-handoff, audit-report, or specialist-report")
            continue
        contract, schema_path = schema_info
        instance_schema_errors = schema_errors(str(path), instance, schema_path)
        errors.extend(instance_schema_errors)
        if instance_schema_errors:
            continue
        if args.previous_report is not None and contract != "audit-report":
            errors.append(f"{path}: --previous-report can only be used with an audit-report JSON file")
        if contract == "audit-report":
            errors.extend(protocol_errors(
                str(path), instance, example_previous,
                require_previous=not using_examples,
            ))
        elif contract == "specialist-report":
            errors.extend(specialist_protocol_errors(str(path), instance))
        elif contract == "build-audit-handoff":
            errors.extend(handoff_protocol_errors(str(path), instance))

    for path, instance, example_previous, expected_error in negative_documents:
        negative_errors: list[str] = []
        schema_info = get_schema(instance)
        if schema_info is None:
            negative_errors.append("unknown contract")
        else:
            negative_errors.extend(schema_errors(str(path), instance, schema_info[1]))
            if schema_info[0] == "audit-report":
                negative_errors.extend(protocol_errors(str(path), instance, example_previous))
            elif schema_info[0] == "specialist-report":
                negative_errors.extend(specialist_protocol_errors(str(path), instance))
            elif schema_info[0] == "build-audit-handoff":
                negative_errors.extend(handoff_protocol_errors(str(path), instance))
        if not any(expected_error in error for error in negative_errors):
            errors.append(
                f"{path}: expected validator rejection containing {expected_error!r}; "
                f"observed {negative_errors or 'no errors'}"
            )

    if errors:
        print("Invalid document(s):")
        for error in errors:
            print(f" - {error}")
        return 1

    count = len(documents)
    if using_examples:
        print(
            f"Validated {count} bundled examples and {len(negative_documents)} expected-rejection fixtures "
            "against Draft 2020-12 schemas and protocol cross-field rules."
        )
    else:
        print(f"Validated {args.file} against its Draft 2020-12 schema and protocol cross-field rules.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
