"""Check installation artifacts, fixture integrity, and CLI boundary behavior."""
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_calibration
import package_instructions
import validate_examples as validator


class PackageTests(unittest.TestCase):
    def test_installation_files_are_complete_and_current(self):
        outputs = package_instructions.assemble()
        self.assertEqual(len(outputs), 8)
        common = (ROOT / "specialists/common.md").read_text(encoding="utf-8").strip()
        for path, content in outputs.items():
            with self.subTest(path=path.name):
                self.assertLessEqual(len(content), package_instructions.INSTRUCTION_BUDGET)
                self.assertEqual(path.read_text(encoding="utf-8"), content)
                if path.stem not in ("builder", "auditor"):
                    self.assertTrue(content.startswith(common))

    def test_configuration_references_exist_and_tools_default_off(self):
        config = validator.load_json(ROOT / "gpt-config.json")
        profiles = [config["builder"], config["auditor"], *config["optional_specialists"]["profiles"]]
        for profile in profiles:
            for source in profile["instruction_sources"]:
                self.assertTrue((ROOT / source).is_file(), source)
            for key, enabled in profile["capabilities"].items():
                if key != "note":
                    self.assertIs(enabled, False, (profile["name"], key))
        references = set(config["builder"]["knowledge_files"] + config["auditor"]["knowledge_files"] + config["optional_specialists"]["knowledge_files"])
        for reference in references:
            path = "standards.template.md" if reference == "standards.md" else reference
            self.assertTrue((ROOT / path).is_file(), path)

    def test_bad_packet_has_exactly_the_declared_mutation(self):
        actual = build_calibration.TARGET.read_text(encoding="utf-8")
        self.assertEqual(actual, build_calibration.build())
        self.assertEqual(actual.count(build_calibration.BAD), 1)

    def test_gpt_packets_have_valid_handoff_and_complete_snapshots(self):
        for name in ("gpt-brief-good.md", "gpt-brief-bad.md"):
            text = (ROOT / "examples/fixtures" / name).read_text(encoding="utf-8")
            packet = json.loads(re.findall(r"```json\n(.*?)\n```", text, re.S)[-1])
            self.assertEqual(validator.schema_errors(name, packet, validator.SCHEMAS["build-audit-handoff"]), [])
            for artifact in packet["artifacts"]:
                self.assertTrue(artifact["snapshot_included"])
                self.assertIn("### " + artifact["path"] + " (new)", text)
            criteria = text.split("## Behavior contract\n", 1)[1].split("## Changes", 1)[0]
            for criterion in packet["acceptance_criteria"]:
                self.assertIn(criterion, criteria)

    def test_bundled_suite_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/validate_examples.py")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_later_report_requires_history_on_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/validate_examples.py"), str(ROOT / "examples/audit-rework.v2.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("--previous-report", result.stdout)

    def test_later_report_with_history_on_cli(self):
        result = subprocess.run([sys.executable, str(ROOT / "tools/validate_examples.py"), str(ROOT / "examples/audit-escalation.v2.json"), "--previous-report", str(ROOT / "examples/audit-rework.v2.json")], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
