# JSON Schemas

The three Draft 2020-12 schemas define Builder handoffs, Auditor reports, and advisory specialist reports. Shapes remain protocol v2; contract.md defines additional semantic rules. Version 3.2.2 fixes input-boundary validation while retaining the five 3.2.1 repairs.

tools/validate_examples.py checks structure, unique IDs, complete history, round/revision continuity, one-to-one stop conditions, closure, monotonic allocation, and unique canonical artifact paths. Supply --previous-report for later audits. Task/F/S identifier patterns match the entire string, including rejection of trailing newlines; invalid IDs are never trimmed or normalized. Artifact paths reject NUL and ambiguous path forms without accessing the filesystem.

JSON input is UTF-8 with optional BOM, at most 2 MiB/file. Duplicate keys and nonstandard numeric constants are rejected. Numeric literals are decoded exactly: mathematically integral forms such as 1.0 and 10e-1 are accepted where integers are required; fractional values are never rounded into integers. Limits: 4,096 characters per numeric literal, absolute stored base-10 exponent <=10,000, and expanded integers <=4,096 digits. Exceeding a limit yields a read error (exit 2); schema/protocol violations yield exit 1; valid input yields exit 0. These limits do not bound string finding IDs.

Early response statuses are prose, not completed JSON reports. Closed regressions require a fresh F ID referenced by the old row. Accepted risk uses not_verifiable with human-overruled: decision evidence, not a technical fix. Continuing FAIL also freezes that decision; PASS/final FAIL retain a null brief.

Validation cannot authenticate human decisions, prose evidence, actual snapshots, case/symlink aliases, or an unsupplied earlier chain. Validate every transition, keep the chain, and retain human review.
