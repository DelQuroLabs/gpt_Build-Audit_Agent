#!/usr/bin/env python3
"""Package integrity checks that JSON Schema cannot express. Standard library only.

    python tools/check_package.py            # run every check
    python tools/check_package.py --write    # regenerate seeded fixtures, then check
    python tools/check_package.py --max 7500 # instruction budget per *-gpt.md file

Checks:
  1. Instruction budget: text below the paste marker in every *-gpt.md is <= --max characters
     (the Custom GPT Instructions field rejects more than 8,000).
  2. Seeded fixtures: every seeded packet equals the good packet with exactly one find/replace.
  3. Configuration: every file named in gpt-config.json exists; each GPT uses <= 20 Knowledge files.
  4. Version: gpt-config.json package_version is the first CHANGELOG entry and appears in README.md.
  5. Stale references: no retired v2 schema names or placeholder schema domains remain.
  6. Path references: every backticked repository path in Markdown, and every repository path in self-audit JSON, exists.
  7. Manifest: every file named in examples/manifest.json exists.
  8. Self-containment: every specialist includes the common rules block (trust boundary, output headings).
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = "-->"
PLATFORM_LIMIT = 8000
FIXTURE = ROOT / "examples/fixtures/requirements-brief-gpt"
# Names that refer to target-GPT artifacts, user-created files, or placeholders, not repository files.
NON_REPO_PATHS = {
    "standards.md", "instructions.md", "behavior-contract.md", "evals/cases.md", "README.md",
    "handoff.json", "h.json", "audit.json", "prior.json", "prior-audit.json", "current.json",
    "security.json", "specialist.json", "builder-response.md", "SMOKE-RESULTS.md",
}
STALE = ["v2.schema.json", "arena.example", "moving-average", "session-cookie"]
TEXT_SUFFIXES = {".md", ".json", ".py", ".yml", ".yaml", ".txt"}
HISTORY_FILES = {"CHANGELOG.md"}


def instruction_budget(limit: int) -> list[str]:
    errors = []
    files = sorted(ROOT.glob("*-gpt.md")) + sorted((ROOT / "specialists").glob("*-gpt.md"))
    if not files:
        errors.append("no *-gpt.md instruction files found")
    for path in files:
        text = path.read_text(encoding="utf-8")
        if MARKER not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing paste marker comment")
            continue
        count = len(text.split(MARKER, 1)[1].strip())
        if count > limit:
            errors.append(f"{path.relative_to(ROOT)}: {count} characters exceeds budget {limit}")
        print(f"  {path.relative_to(ROOT)}: {count} characters")
    return errors


def seeded_fixtures(write: bool) -> list[str]:
    errors = []
    manifest = json.loads((FIXTURE / "seeded/manifest.json").read_text(encoding="utf-8"))
    base = (FIXTURE / manifest["base"]).read_text(encoding="utf-8")
    for variant in manifest["variants"]:
        occurrences = base.count(variant["find"])
        if occurrences != 1:
            errors.append(f"seeded {variant['name']}: find text occurs {occurrences} times in base (need 1)")
            continue
        expected = base.replace(variant["find"], variant["replace"], 1)
        target = FIXTURE / "seeded" / f"{variant['name']}.md"
        if write:
            target.write_text(expected, encoding="utf-8")
        if not target.exists() or target.read_text(encoding="utf-8") != expected:
            errors.append(f"{target.relative_to(ROOT)}: differs from base + one replacement (run --write)")
        report = FIXTURE / "expected" / f"{variant['name']}.audit.json"
        if not report.exists():
            errors.append(f"{report.relative_to(ROOT)}: expected audit report missing")
            continue
        data = json.loads(report.read_text(encoding="utf-8"))
        exp = variant["expected"]
        severities = {f.get("severity") for f in data.get("findings", [])}
        results = {r.get("criterion_id"): r.get("result") for r in data.get("acceptance_check", [])}
        if data.get("verdict") != exp["verdict"] or exp["severity"] not in severities \
                or results.get(exp["criterion"]) != exp["acceptance_result"]:
            errors.append(f"{report.relative_to(ROOT)}: does not match manifest expectation {exp}")
    return errors


def configuration() -> list[str]:
    errors = []
    config = json.loads((ROOT / "gpt-config.json").read_text(encoding="utf-8"))
    groups = [config["builder"], config["auditor"]]
    for profile in config["optional_specialists"]["profiles"]:
        groups.append({"instructions_file": profile["instructions_file"],
                       "knowledge_files": config["optional_specialists"]["knowledge_files"]})
    for group in groups:
        if not (ROOT / group["instructions_file"]).exists():
            errors.append(f"gpt-config.json: missing {group['instructions_file']}")
        files = group.get("knowledge_files", [])
        if len(files) > 20:
            errors.append(f"gpt-config.json: {group['instructions_file']} lists {len(files)} Knowledge files (> 20)")
        for name in files:
            exists = (ROOT / name).exists() or (name == "standards.md" and (ROOT / "standards.template.md").exists())
            if not exists:
                errors.append(f"gpt-config.json: Knowledge file {name} does not exist")
    for key in ("trigger_matrix_file", "report_schema"):
        if not (ROOT / config["optional_specialists"][key]).exists():
            errors.append(f"gpt-config.json: missing {config['optional_specialists'][key]}")
    return errors


def version() -> list[str]:
    config = json.loads((ROOT / "gpt-config.json").read_text(encoding="utf-8"))
    ver = config["package_version"]
    errors = []
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    first = re.search(r"^## (\S+)", changelog, re.M)
    if not first or first.group(1) != ver:
        errors.append(f"CHANGELOG.md: first entry {first.group(1) if first else None} != package_version {ver}")
    if ver not in (ROOT / "README.md").read_text(encoding="utf-8"):
        errors.append(f"README.md: does not mention package_version {ver}")
    if config.get("protocol_version") != 3:
        errors.append("gpt-config.json: protocol_version must be 3")
    return errors


def repo_text_files() -> list[Path]:
    return [p for p in ROOT.rglob("*") if p.is_file() and p.suffix in TEXT_SUFFIXES
            and ".git" not in p.parts and p.name != "check_package.py"]


def stale_references() -> list[str]:
    errors = []
    for path in repo_text_files():
        if path.name in HISTORY_FILES:
            continue
        text = path.read_text(encoding="utf-8")
        for needle in STALE:
            if needle in text:
                errors.append(f"{path.relative_to(ROOT)}: stale reference {needle!r}")
    return errors


def path_references() -> list[str]:
    errors = []
    pattern = re.compile(r"`([A-Za-z0-9_.\-/]+\.(?:md|json|py|txt|yml))`")
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts or path.name in HISTORY_FILES or "fixtures" in path.parts:
            continue
        for ref in pattern.findall(path.read_text(encoding="utf-8")):
            if ref in NON_REPO_PATHS or ref.startswith("path/to") or "<" in ref:
                continue
            candidates = [ROOT / ref, path.parent / ref, ROOT / "schemas" / ref, ROOT / "specialists" / ref,
                          ROOT / "tools" / ref, FIXTURE / ref]
            if not any(c.exists() for c in candidates):
                errors.append(f"{path.relative_to(ROOT)}: references missing file `{ref}`")
    # Repository paths quoted inside the self-audit JSON records must also exist.
    json_pattern = re.compile(r"\b((?:self-audit|examples|schemas|tools|prompts|specialists|docs)/[A-Za-z0-9_.\-/]+\.(?:md|json|py|txt|yml))")
    for path in sorted((ROOT / "self-audit").glob("*.json")):
        for ref in json_pattern.findall(path.read_text(encoding="utf-8")):
            if not (ROOT / ref).exists():
                errors.append(f"{path.relative_to(ROOT)}: references missing file `{ref}`")
    return errors


def manifest_files() -> list[str]:
    manifest = json.loads((ROOT / "examples/manifest.json").read_text(encoding="utf-8"))
    errors = []
    for case in manifest["positive"] + manifest["negative"]:
        for key in ("file", "previous", "handoff"):
            if case.get(key) and not (ROOT / case[key]).exists():
                errors.append(f"examples/manifest.json: missing {case[key]}")
        for name in case.get("specialists", []):
            if not (ROOT / name).exists():
                errors.append(f"examples/manifest.json: missing {name}")
    return errors


def specialist_blocks() -> list[str]:
    errors = []
    required = ["# Common specialist rules", "untrusted data", "## Input needed", "## Trigger and scope",
                "## Specialist report", "specialist-report.v3.schema.json"]
    for path in sorted((ROOT / "specialists").glob("*-gpt.md")):
        text = path.read_text(encoding="utf-8")
        for needle in required:
            if needle not in text:
                errors.append(f"{path.relative_to(ROOT)}: missing {needle!r}")
        role = path.name.removesuffix("-gpt.md")
        if f'"specialist": "{role}"' not in text:
            errors.append(f"{path.relative_to(ROOT)}: does not declare \"specialist\": \"{role}\"")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--max", type=int, default=7500, help="instruction budget (default 7500)")
    parser.add_argument("--write", action="store_true", help="regenerate seeded fixtures before checking")
    args = parser.parse_args(argv)
    if args.max > PLATFORM_LIMIT:
        parser.error(f"--max cannot exceed the platform limit of {PLATFORM_LIMIT}")
    checks = [
        ("instruction budget", lambda: instruction_budget(args.max)),
        ("seeded fixtures", lambda: seeded_fixtures(args.write)),
        ("configuration", configuration),
        ("version", version),
        ("stale references", stale_references),
        ("path references", path_references),
        ("manifest files", manifest_files),
        ("specialist self-containment", specialist_blocks),
    ]
    failures = 0
    for name, check in checks:
        print(f"[{name}]")
        errors = check()
        for error in errors:
            print(f"  FAIL {error}")
        failures += len(errors)
        if not errors:
            print("  ok")
    print("Package checks passed." if failures == 0 else f"{failures} package check failure(s).")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
