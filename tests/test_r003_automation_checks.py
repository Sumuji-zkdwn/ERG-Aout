import sys
import tempfile
import unittest
from pathlib import Path

from tool.run_r003_automation_checks import ROOT, build_checks, run_command


class NegativeFixtureTests(unittest.TestCase):
    def test_positive_graph_must_validate_successfully(self):
        for filename, expected in (("minimal_valid.json", True), ("invalid_duplicate_node_id.json", False)):
            with self.subTest(filename=filename):
                result = run_command(
                    filename,
                    [sys.executable, "tool/validate_r001_kernel.py", f"examples/r001/{filename}"],
                )
                self.assertEqual(result.ok, expected)

    def test_discovered_negative_fixtures_are_checked_for_rejection(self):
        checks = [c for c in build_checks() if c.expected_invalid]
        self.assertGreaterEqual(len(checks), 5)
        for check in checks:
            with self.subTest(name=check.name):
                result = run_command(check.name, check.command, expected_invalid=True)
                self.assertTrue(result.ok, result.stdout + "\n" + result.stderr)

    def test_each_negative_fixture_exercises_its_named_invariant(self):
        expected_diagnostics = {
            "invalid_cycle_and_policy.json": ("extends_main must be acyclic", "cross-layer policy violation"),
            "invalid_duplicate_node_id.json": ("node ids must be unique",),
            "invalid_extends_main_outside_accepted.json": ("extends_main endpoints must both be in L_accepted",),
            "invalid_missing_edge_endpoint.json": ("target node does not exist",),
            "invalid_node_type_for_layer.json": ("has invalid type",),
        }
        for filename, diagnostics in expected_diagnostics.items():
            with self.subTest(filename=filename):
                result = run_command(
                    filename,
                    [sys.executable, "tool/validate_r001_kernel.py", f"examples/r001/{filename}"],
                    expected_invalid=True,
                )
                self.assertTrue(result.ok)
                for diagnostic in diagnostics:
                    self.assertIn(diagnostic, result.stdout)

    def test_accepting_a_valid_graph_is_not_a_successful_negative_check(self):
        result = run_command(
            "valid graph treated as negative",
            [sys.executable, "tool/validate_r001_kernel.py", "examples/r001/minimal_valid.json"],
            expected_invalid=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertFalse(result.ok)

    def test_validator_crash_is_not_a_successful_negative_check(self):
        with tempfile.TemporaryDirectory() as directory:
            bad_json = Path(directory) / "invalid_broken.json"
            bad_json.write_text("{", encoding="utf-8")
            result = run_command(
                "malformed fixture",
                [sys.executable, str(ROOT / "tool/validate_r001_kernel.py"), str(bad_json)],
                expected_invalid=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(result.stderr)
        self.assertFalse(result.ok)


if __name__ == "__main__":
    unittest.main()
