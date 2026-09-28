"""Raw-input regressions from the 3.2.1 re-audit; no model or network needed."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, localcontext
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import validate_examples as validator


def sample(name):
    return validator.load_json(ROOT / "examples" / name)


def raw_field(packet, field, literal):
    packet = copy.deepcopy(packet)
    packet[field] = "RAW_NUMBER_PLACEHOLDER"
    return json.dumps(packet).replace('"RAW_NUMBER_PLACEHOLDER"', literal)


class InputBoundaryTests(unittest.TestCase):
    def check_cli(self, current, previous=None, *, code=0, message=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "current.json"
            path.write_text(current if isinstance(current, str) else json.dumps(current), encoding="utf-8")
            command = [sys.executable, str(ROOT / "tools/validate_examples.py"), str(path)]
            if previous is not None:
                prior_path = Path(directory) / "previous.json"
                prior_path.write_text(previous if isinstance(previous, str) else json.dumps(previous), encoding="utf-8")
                command += ["--previous-report", str(prior_path)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        self.assertNotIn("Traceback", output)
        self.assertNotIn("PRIVATE_PATH_MARKER", output)
        self.assertEqual(result.returncode, code, output[:2000])
        if message:
            self.assertIn(message, output)

    def test_all_schema_identifier_patterns_match_complete_strings(self):
        patterns = []

        def visit(node):
            if isinstance(node, dict):
                if "pattern" in node:
                    patterns.append(node["pattern"])
                for child in node.values():
                    visit(child)
            elif isinstance(node, list):
                for child in node:
                    visit(child)

        for schema in validator.SCHEMAS.values():
            visit(validator.load_json(schema))
        self.assertGreaterEqual(len(patterns), 10)
        for pattern in patterns:
            valid = "F1: observable check" if ": " in pattern else (
                "F1" if pattern.startswith("^F") else "S1" if pattern.startswith("^S") else "task-name")
            check = Draft202012Validator({"type": "string", "pattern": pattern})
            self.assertTrue(check.is_valid(valid), pattern)
            for suffix in ("\n", "\r", "\r\n", "\x00", "\u2028", "\u2029"):
                with self.subTest(pattern=pattern, suffix=repr(suffix)):
                    # Stop-condition descriptions allow arbitrary non-newline text,
                    # but their IDs and all other identifiers must end exactly.
                    if ": " in pattern and suffix not in ("\n", "\r\n"):
                        continue
                    self.assertFalse(check.is_valid(valid + suffix))

    def test_task_id_trailing_newline_is_rejected_in_every_contract(self):
        for name in ("audit-pass.v2.json", "build-handoff.v2.json", "specialist-security.v2.json"):
            with self.subTest(name=name):
                packet = sample(name)
                packet["task_id"] += "\n"
                self.check_cli(packet, code=1, message="failed pattern constraint")

    def test_specialist_newline_id_and_matching_recommendation_are_rejected(self):
        packet = sample("specialist-security.v2.json")
        packet["findings"][0]["id"] = "S1\n"
        packet["recommended_to_auditor"] = ["S1\n"]
        self.check_cli(packet, code=1, message="failed pattern constraint")

    def test_newline_history_cannot_bypass_monotonic_ids(self):
        prior = sample("audit-fail.v2.json")
        finding = copy.deepcopy(prior["findings"][0])
        finding.update(id="F100\n", severity="MINOR")
        prior["findings"].append(finding)
        self.check_cli(prior, code=1, message="failed pattern constraint")
        current = sample("audit-rework.v2.json")
        current["regression_check"].append({"finding_id": "F100\n", "status": "fixed", "evidence": "Checked."})
        current["rework_brief"]["frozen"].append({"id": "F100\n", "reason": "Checked."})
        self.check_cli(current, prior, code=1, message="Invalid previous report")
        prior["findings"][-1]["id"] = "F100"
        current["regression_check"][-1]["finding_id"] = "F100"
        current["rework_brief"]["frozen"][-1]["id"] = "F100"
        self.check_cli(current, prior, code=1, message="greater than prior ID F100")

    def test_id_order_rejects_invalid_ids_instead_of_using_zero(self):
        for value in ("F0", "F01", "F1\n", "F1 ", "X1", ""):
            with self.subTest(value=repr(value)):
                with self.assertRaisesRegex(ValueError, "complete F<n> form"):
                    validator._id_order(value)

    def test_high_precision_fractional_audit_round_is_rejected(self):
        packet = sample("audit-pass.v2.json")
        for literal in ("1.0000000000000001", "0.99999999999999999", "1.5"):
            with self.subTest(literal=literal):
                self.check_cli(raw_field(packet, "audit_round", literal), code=1, message="failed type constraint")

    def test_underflowing_fractional_revision_is_rejected(self):
        packet = sample("audit-pass.v2.json")
        for literal in ("1e-400", "-1e-400", "1e-10000"):
            with self.subTest(literal=literal):
                self.check_cli(raw_field(packet, "build_revision", literal), code=1, message="failed type constraint")

    def test_fractional_previous_report_is_rejected_before_history_checks(self):
        current = sample("audit-rework.v2.json")
        prior = raw_field(sample("audit-fail.v2.json"), "audit_round", "1.0000000000000001")
        self.check_cli(current, prior, code=1, message="Invalid previous report")

    def test_integral_number_spellings_remain_valid(self):
        packet = sample("audit-pass.v2.json")
        for literal in ("1.0", "1e0", "0.1e1", "10e-1", "1.0000000000000000"):
            with self.subTest(literal=literal):
                self.check_cli(raw_field(packet, "audit_round", literal))
        for literal in ("0.0", "-0.0", "0e-10000", "0e10000"):
            with self.subTest(literal=literal):
                self.check_cli(raw_field(packet, "build_revision", literal))

    def test_integral_exponents_remain_valid_across_history(self):
        prior = raw_field(sample("audit-fail.v2.json"), "audit_round", "10e-1")
        current = raw_field(sample("audit-rework.v2.json"), "audit_round", "0.2e1")
        self.check_cli(current, prior)

    def test_json_loader_keeps_fractional_values_exact(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "numbers.json"
            path.write_text("[1.0000000000000001, 1e-400, 1.0, 0e10000]", encoding="utf-8")
            values = validator.load_json(path)
        self.assertEqual(values, [Decimal("1.0000000000000001"), Decimal("1e-400"), 1, 0])
        self.assertIsInstance(values[0], Decimal)
        self.assertIsInstance(values[1], Decimal)
        self.assertIs(type(values[2]), int)

    def test_exact_decoding_does_not_depend_on_decimal_precision(self):
        with localcontext() as context:
            context.prec = 2
            self.assertEqual(validator._exact_number("1.0000000000000001"), Decimal("1.0000000000000001"))
            self.assertEqual(validator._exact_number("123456789.0"), 123456789)

    def test_numeric_size_boundaries_are_explicit_and_bounded(self):
        self.assertEqual(validator._exact_number("9" * 4096), 10 ** 4096 - 1)
        self.assertEqual(validator._exact_number("1e4095"), 10 ** 4095)
        self.assertEqual(validator._exact_number("1e-10000"), Decimal("1e-10000"))
        for literal in ("9" * 4097, "1e4096", "1e-10001", "0e10001", "1e" + "9" * 100):
            with self.subTest(literal=literal[:30]):
                with self.assertRaises(ValueError):
                    validator._exact_number(literal)

    def test_oversized_numbers_return_read_error_without_traceback(self):
        packet = sample("audit-pass.v2.json")
        for literal in ("9" * 4097, "1e4096", "1e-10001", "1e" + "9" * 100):
            with self.subTest(literal=literal[:30]):
                self.check_cli(raw_field(packet, "audit_round", literal), code=2, message="Could not read JSON input")

    def test_nonstandard_numeric_constants_remain_rejected(self):
        for literal in ("NaN", "Infinity", "-Infinity"):
            with self.subTest(literal=literal):
                self.check_cli(raw_field(sample("audit-pass.v2.json"), "audit_round", literal),
                               code=2, message="nonstandard JSON numeric constant")

    def test_null_artifact_paths_are_rejected_without_echo(self):
        for path in ("\x00PRIVATE_PATH_MARKER.py", "src/PRIVATE_PATH_MARKER\x00.py", "PRIVATE_PATH_MARKER.py\x00"):
            with self.subTest(path=repr(path)):
                packet = sample("build-handoff.v2.json")
                packet["artifacts"][0]["path"] = path
                self.check_cli(packet, code=1, message="canonical repository-relative")

    def test_null_path_rejection_does_not_access_the_filesystem(self):
        packet = sample("build-handoff.v2.json")
        packet["artifacts"][0]["path"] = "src/invalid\x00.py"
        with patch.object(Path, "stat", side_effect=AssertionError("No filesystem access allowed")), \
                patch.object(Path, "resolve", side_effect=AssertionError("No filesystem access allowed")):
            self.assertTrue(validator.handoff_protocol_errors("test", packet))


if __name__ == "__main__":
    unittest.main()
