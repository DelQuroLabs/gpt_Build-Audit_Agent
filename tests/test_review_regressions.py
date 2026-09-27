"""End-to-end regressions from the 3.2.0 code review, using synthetic packets."""
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

OVERRIDE = ("human-overruled: supplied human decision accepts F1; rationale: bounded demo risk; "
            "owner: project lead; review: 2026-10-01; accepted risk is not a technical fix.")


def sample(name):
    return validator.load_json(ROOT / "examples" / name)


def reopened_report():
    report = sample("audit-fail.v2.json")
    report.update(audit_round=2, build_revision=1)
    report["regression_check"] = [
        {"finding_id": "F1", "status": "reopened", "evidence": "F1 remains unresolved and active."},
    ]
    return report


def closing_report(previous, status="fixed", evidence="The supplied check confirms the correction."):
    report = sample("audit-pass.v2.json")
    report.update(task_id=previous["task_id"], audit_round=previous["audit_round"] + 1,
                  build_revision=previous["build_revision"] + 1)
    report["regression_check"] = [{"finding_id": "F1", "status": status, "evidence": evidence}]
    return report


class ReviewRegressionTests(unittest.TestCase):
    def check_cli(self, current, previous=None, *, valid=True, message=None):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "current.json"
            path.write_text(json.dumps(current), encoding="utf-8")
            command = [sys.executable, str(ROOT / "tools/validate_examples.py"), str(path)]
            if previous is not None:
                prior_path = Path(directory) / "previous.json"
                prior_path.write_text(json.dumps(previous), encoding="utf-8")
                command += ["--previous-report", str(prior_path)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        self.assertNotIn("Traceback", output)
        self.assertEqual(result.returncode, 0 if valid else 1, output[:2000])
        if message:
            self.assertIn(message, output)

    def test_reopened_active_finding_cannot_disappear_into_pass(self):
        prior = reopened_report()
        self.check_cli(prior, sample("audit-fail.v2.json"))
        current = closing_report(prior, "not_verifiable", "No fix or human override supplied.")
        self.check_cli(current, prior, valid=False, message="must remain in current findings")

    def test_active_reopened_transition_matrix(self):
        prior = reopened_report()
        for status in ("fixed", "open", "not_verifiable", "reopened"):
            for retained in (False, True):
                with self.subTest(status=status, retained=retained):
                    current = closing_report(prior, status)
                    if retained:
                        current.update(verdict="FAIL", round_limit_reached=True,
                                       findings=copy.deepcopy(prior["findings"]),
                                       escalation=sample("audit-escalation.v2.json")["escalation"])
                    self.check_cli(current, prior, valid=(retained != (status == "fixed")))

    def test_last_finding_can_be_explicitly_overruled_at_round_two_or_three(self):
        for prior in (sample("audit-fail.v2.json"), reopened_report()):
            with self.subTest(round=prior["audit_round"]):
                current = closing_report(prior, "not_verifiable", OVERRIDE)
                self.check_cli(current, prior)

    def test_overrule_with_remaining_minor_finding(self):
        prior = sample("audit-fail.v2.json")
        current = closing_report(prior, "not_verifiable", OVERRIDE)
        minor = copy.deepcopy(prior["findings"][0])
        minor.update(id="F2", severity="MINOR")
        current.update(verdict="PASS_WITH_NOTES", findings=[minor])
        self.check_cli(current, prior)

    def test_overrule_at_final_fail_with_another_active_finding(self):
        prior = reopened_report()
        current = closing_report(prior, "not_verifiable", OVERRIDE)
        other = copy.deepcopy(prior["findings"][0])
        other["id"] = "F2"
        current.update(verdict="FAIL", findings=[other], round_limit_reached=True,
                       escalation=sample("audit-escalation.v2.json")["escalation"])
        self.check_cli(current, prior)

    def test_empty_overrule_cannot_close_a_finding(self):
        prior = sample("audit-fail.v2.json")
        current = closing_report(prior, "not_verifiable", "human-overruled:   ")
        self.check_cli(current, prior, valid=False, message="must remain in current findings")

    def test_overrule_cannot_be_mislabeled_fixed(self):
        prior = sample("audit-fail.v2.json")
        self.check_cli(closing_report(prior, "fixed", OVERRIDE), prior,
                       valid=False, message="must use not_verifiable")

    def test_overrule_cannot_remain_active(self):
        prior = sample("audit-fail.v2.json")
        current = reopened_report()
        current["regression_check"][0].update(status="not_verifiable", evidence=OVERRIDE)
        self.check_cli(current, prior, valid=False, message="cannot also be active")

    def test_continuing_fail_freezes_accepted_risk(self):
        prior = sample("audit-fail.v2.json")
        current = sample("audit-rework.v2.json")
        current["regression_check"][0].update(status="not_verifiable", evidence=OVERRIDE)
        current["rework_brief"]["frozen"][0]["reason"] = OVERRIDE
        self.check_cli(current, prior)
        current["rework_brief"]["frozen"] = []
        self.check_cli(current, prior, valid=False, message="must retain closed history")

    def test_prior_overrule_stays_disclosed_at_closure(self):
        prior = sample("audit-rework.v2.json")
        prior["regression_check"][0].update(status="not_verifiable", evidence=OVERRIDE)
        prior["rework_brief"]["frozen"][0]["reason"] = OVERRIDE
        self.check_cli(prior, sample("audit-fail.v2.json"))
        current = closing_report(prior, "not_verifiable", OVERRIDE)
        current["regression_check"].append({"finding_id": "F2", "status": "fixed", "evidence": "F2 fix verified."})
        self.check_cli(current, prior)
        current["regression_check"][0]["evidence"] = "No longer inspected."
        self.check_cli(current, prior, valid=False, message="accepted-risk disclosure")

    def test_closed_history_and_new_regression_remain_distinct(self):
        prior = sample("audit-rework.v2.json")
        current = closing_report(prior, "reopened", "New regression of closed F1 is tracked as F3.")
        current["regression_check"].append({"finding_id": "F2", "status": "fixed", "evidence": "F2 fix verified."})
        finding = copy.deepcopy(prior["findings"][0])
        finding["id"] = "F3"
        current.update(verdict="FAIL", findings=[finding], round_limit_reached=True,
                       escalation=sample("audit-escalation.v2.json")["escalation"])
        self.check_cli(current, prior)
        current["findings"][0]["id"] = "F1"
        self.check_cli(current, prior, valid=False, message="reuses previously closed")

    def test_new_ids_are_monotonic_across_decimal_length_changes(self):
        prior = sample("audit-fail.v2.json")
        prior["findings"][0]["id"] = "F9"
        prior["rework_brief"]["must_fix"] = ["F9"]
        prior["rework_brief"]["stop_conditions"] = ["F9: Check passes."]
        current = sample("audit-rework.v2.json")
        current["regression_check"][0]["finding_id"] = "F9"
        current["rework_brief"]["frozen"][0]["id"] = "F9"
        current["findings"][0]["id"] = "F10"
        current["rework_brief"]["must_fix"] = ["F10"]
        current["rework_brief"]["stop_conditions"] = ["F10: Check passes."]
        self.check_cli(current, prior)
        current["findings"][0]["id"] = "F8"
        current["rework_brief"]["must_fix"] = ["F8"]
        current["rework_brief"]["stop_conditions"] = ["F8: Check passes."]
        self.check_cli(current, prior, valid=False, message="greater than prior ID F9")

    def test_duplicate_conflicting_artifact_paths_are_rejected(self):
        packet = sample("build-handoff.v2.json")
        duplicate = copy.deepcopy(packet["artifacts"][0])
        duplicate.update(status="deleted", snapshot_included=False)
        packet["artifacts"].append(duplicate)
        self.check_cli(packet, valid=False, message="artifact paths must be unique")

    def test_duplicate_identical_artifact_paths_are_rejected(self):
        packet = sample("build-handoff.v2.json")
        packet["artifacts"].append(copy.deepcopy(packet["artifacts"][0]))
        self.check_cli(packet, valid=False, message="artifact paths must be unique")

    def test_artifact_paths_are_portable_and_unambiguous(self):
        for path in ("./file.py", "a/../file.py", "a//file.py", "a/", "/file.py",
                     "C:/file.py", "C:file.py", "a\\file.py", "../file.py"):
            with self.subTest(path=path):
                packet = sample("build-handoff.v2.json")
                packet["artifacts"][0]["path"] = path
                self.check_cli(packet, valid=False, message="canonical repository-relative")

    def test_unique_nested_artifact_paths_are_accepted(self):
        packet = sample("build-handoff.v2.json")
        packet["artifacts"][0]["path"] = "src/my module.py"
        self.check_cli(packet)

    def test_long_schema_valid_id_does_not_crash(self):
        prior = sample("audit-fail.v2.json")
        long_id = "F" + "9" * 5000
        prior["findings"][0]["id"] = long_id
        prior["rework_brief"]["must_fix"] = [long_id]
        prior["rework_brief"]["stop_conditions"] = [long_id + ": Check passes."]
        current = closing_report(prior)
        current["regression_check"][0]["finding_id"] = long_id
        self.check_cli(current, prior)

    def test_id_order_preserves_numeric_order_without_conversion(self):
        ids = ["F100", "F2", "F10", "F9", "F1", "F" + "9" * 5000, "F" + "1" * 5001]
        self.assertEqual(sorted(ids, key=validator._id_order),
                         ["F1", "F2", "F9", "F10", "F100", ids[-2], ids[-1]])

    def test_integral_float_history_is_accepted(self):
        prior = sample("audit-fail.v2.json")
        current = closing_report(prior)
        prior.update(audit_round=1.0, build_revision=0.0)
        self.assertEqual(validator.schema_errors("prior", prior, validator.SCHEMAS["audit-report"]), [])
        self.check_cli(current, prior)
        current.update(audit_round=2.0, build_revision=1.0)
        self.check_cli(current, prior)

    def test_boolean_and_fractional_history_still_rejected(self):
        for value in (True, 1.5):
            prior = sample("audit-fail.v2.json")
            current = closing_report(prior)
            prior["audit_round"] = value
            self.check_cli(current, prior, valid=False, message="Invalid previous report")


if __name__ == "__main__":
    unittest.main()
