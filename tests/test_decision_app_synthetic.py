"""Run upstream R001/R002/R005 tools on a synthetic decision-app fixture."""
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
STEM = ROOT / "examples/r005/decision_app_synthetic"

class DecisionAppSmoke(unittest.TestCase):
    def check(self, script, *args):
        run = subprocess.run([sys.executable, str(ROOT / "tool" / script), *map(str,args)],
                             capture_output=True, text=True, cwd=ROOT, encoding="utf-8")
        self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
        if "WARNINGS" in run.stdout:
            block = run.stdout.split("WARNINGS", 1)[1].split("NOTES", 1)[0].strip()
            self.assertEqual(block, "- none", run.stdout)
        return run.stdout

    def test_official_checks(self):
        graph = STEM.with_suffix(".json")
        sidecar = STEM.with_name(STEM.name + "_raw_text_sidecar.md")
        binding = STEM.with_suffix(".formal_binding.json")
        self.check("validate_r001_kernel.py", graph)
        self.check("check_r002_mapping_consistency.py", graph)
        self.check("check_r002_sidecar_consistency.py", graph, sidecar)
        # R003 runner additionally checks the pinned formal repo with --require-formal-check.
        result = subprocess.run([sys.executable, str(ROOT / "tool/check_formal_binding.py"),
                                 str(graph), str(binding)], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_no_prediction_promoted(self):
        graph = json.loads(STEM.with_suffix(".json").read_text(encoding="utf-8"))
        promoted = {e["source"] for e in graph["edges"] if e["type"]=="accepted_from_candidate"}
        self.assertEqual(promoted, {"cand.record.1","cand.record.2","cand.record.3"})
        self.assertEqual(sum(e["type"]=="extends_main" for e in graph["edges"]), 2)
