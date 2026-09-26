"""Protocol regression checks; these do not execute or grade a language model."""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_examples as validator


def sample(name):
    return validator.load_json(ROOT / "examples" / name)


def errors(packet, prior=None):
    schema = validator.get_schema(packet)
    return (validator.schema_errors("test", packet, schema[1])
            + validator.protocol_errors("test", packet, prior))


class AuditHistoryTests(unittest.TestCase):
    def setUp(self):
        self.prior = sample("audit-rework.v2.json")
        self.current = sample("audit-escalation.v2.json")
        self.current["regression_check"] = [
            {"finding_id": "F1", "status": "fixed", "evidence": "Original range correction remains present."},
            {"finding_id": "F2", "status": "open", "evidence": "Boolean window is still accepted."},
        ]

    def test_frozen_history_is_required_and_accepted(self):
        self.assertEqual(errors(self.current, self.prior), [])
        self.current["regression_check"].pop(0)
        self.assertTrue(errors(self.current, self.prior))

    def test_fixed_cannot_remain_an_active_finding(self):
        prior = sample("audit-fail.v2.json")
        current = sample("audit-rework.v2.json")
        current["findings"].append(copy.deepcopy(prior["findings"][0]))
        current["rework_brief"]["deferred"].append("F1")
        self.assertTrue(errors(current, prior))

    def test_frozen_cannot_also_be_active(self):
        current = sample("audit-fail.v2.json")
        current["rework_brief"]["frozen"] = [{"id": "F1", "reason": "Claimed fixed while still active."}]
        self.assertTrue(errors(current))

    def test_frozen_requires_history_evidence(self):
        current = sample("audit-rework.v2.json")
        current["rework_brief"]["frozen"].append({"id": "F99", "reason": "Invented closure."})
        self.assertTrue(errors(current, sample("audit-fail.v2.json")))

    def test_new_regression_uses_new_id(self):
        current = copy.deepcopy(self.current)
        finding = copy.deepcopy(current["findings"][0])
        finding["id"] = "F3"
        finding["evidence_detail"] = "New regression of closed F1; original identity remains closed."
        current["findings"].append(finding)
        current["regression_check"][0] = {
            "finding_id": "F1", "status": "reopened",
            "evidence": "New regression is tracked as F3; final window was removed again.",
        }
        self.assertEqual(errors(current, self.prior), [])

    def test_closed_id_reuse_still_rejected(self):
        self.current["findings"][0]["id"] = "F1"
        self.assertTrue(errors(self.current, self.prior))

    def test_minor_history_cannot_disappear(self):
        prior = sample("audit-fail.v2.json")
        minor = copy.deepcopy(prior["findings"][0])
        minor.update(id="F2", severity="MINOR")
        prior["findings"].append(minor)
        current = sample("audit-rework.v2.json")
        current["findings"][0]["id"] = "F3"
        current["rework_brief"]["must_fix"] = ["F3"]
        current["rework_brief"]["stop_conditions"] = ["F3: Boolean input is rejected."]
        self.assertTrue(errors(current, prior))

    def test_schema_valid_prior_chain_is_accepted(self):
        self.assertEqual(errors(self.prior, sample("audit-fail.v2.json")), [])


class InputTests(unittest.TestCase):
    def test_schema_diagnostics_do_not_echo_invalid_values(self):
        packet = sample("build-handoff.v2.json")
        packet["confidence"] = "SYNTHETIC-SECRET-NOT-REAL"
        messages = errors(packet)
        self.assertTrue(messages)
        self.assertNotIn("SYNTHETIC-SECRET-NOT-REAL", " ".join(messages))

    def test_explicit_human_overrule_is_not_marked_fixed(self):
        prior = sample("audit-fail.v2.json")
        current = sample("audit-rework.v2.json")
        current["regression_check"][0]["status"] = "not_verifiable"
        current["regression_check"][0]["evidence"] = "Explicit human acceptance; not a technical fix."
        current["rework_brief"]["frozen"][0]["reason"] = "human-overruled: user accepted F1; owner project lead; review 2026-10-01; risk retained."
        self.assertEqual(errors(current, prior), [])
        current["rework_brief"]["frozen"][0]["reason"] = "Pretend fixed without evidence."
        self.assertTrue(errors(current, prior))

    def test_json_byte_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "oversized.json"
            path.write_bytes(b" " * (2 * 1024 * 1024 + 1))
            with self.assertRaisesRegex(ValueError, "2 MiB"):
                validator.load_json(path)

    def test_cli_schema_error_does_not_echo_invalid_id(self):
        packet = sample("audit-fail.v2.json")
        packet["findings"][0]["id"] = "SYNTHETIC-SECRET-NOT-REAL"
        packet["rework_brief"]["must_fix"] = ["SYNTHETIC-SECRET-NOT-REAL"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid-id.json"
            path.write_text(json.dumps(packet), encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "tools/validate_examples.py"), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("SYNTHETIC-SECRET-NOT-REAL", result.stdout + result.stderr)

    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.json"
            path.write_text('{"contract":"audit-report","contract":"build-audit-handoff"}', encoding="utf-8")
            with self.assertRaises(ValueError):
                validator.load_json(path)

    def test_nonstandard_json_numbers_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nan.json"
            path.write_text('{"value":NaN}', encoding="utf-8")
            with self.assertRaises(ValueError):
                validator.load_json(path)

    def test_invalid_encoding_is_a_clean_cli_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_bytes(b"\xff\xfe\x00")
            result = subprocess.run([sys.executable, str(ROOT / "tools/validate_examples.py"), str(path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("Traceback", result.stderr)

    def test_malformed_types_do_not_crash_protocol_check(self):
        for value in (None, [], {}, False, 1, "bad"):
            for field in ("findings", "regression_check", "rework_brief", "audit_round", "verdict"):
                packet = sample("audit-fail.v2.json")
                packet[field] = value
                result = errors(packet)
                if (field == "regression_check" and value == []) or (field == "audit_round" and type(value) is int and value == 1):
                    self.assertEqual(result, [])
                else:
                    self.assertTrue(result, (field, value))


if __name__ == "__main__":
    unittest.main()
