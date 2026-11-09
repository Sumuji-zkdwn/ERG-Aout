import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tool.check_formal_binding import lean_declarations
from tool.run_r003_automation_checks import ROOT, build_checks, run_command

CHECKER = str(ROOT / "tool/check_formal_binding.py")
REPO = "Owner/formal"

LEAN_SOURCE = """/-! Fixture. `theorem not_a_decl` inside a comment must be ignored. -/
noncomputable section
namespace Demo

def Idem (K : Nat → Nat) : Prop := ∀ x, K (K x) = K x

-- theorem commented_out : True := trivial

theorem idem_id : Idem id := fun _ => rfl

end Demo
"""

GRAPH = {
    "nodes": [
        {"id": "raw.1", "layer": "L_raw", "type": "RawArtifact"},
        {"id": "cand.def", "layer": "L_candidate", "type": "CandidateDefinition"},
        {"id": "cand.claim", "layer": "L_candidate", "type": "CandidateClaim"},
        {"id": "cand.q", "layer": "L_candidate", "type": "CandidateQuestion"},
    ],
    "edges": [
        {"id": "e1", "type": "introduces", "source": "raw.1", "target": "cand.def"},
        {"id": "e2", "type": "introduces", "source": "raw.1", "target": "cand.claim"},
        {"id": "e3", "type": "introduces", "source": "raw.1", "target": "cand.q"},
    ],
}


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid", *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


class FormalBindingTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.repo = self.tmp / "formal"
        self.repo.mkdir()
        git(self.repo, "init", "-q", "-b", "main")
        (self.repo / "Demo.lean").write_text(LEAN_SOURCE, encoding="utf-8")
        git(self.repo, "add", "Demo.lean")
        git(self.repo, "commit", "-q", "-m", "fixture")
        self.commit = git(self.repo, "rev-parse", "HEAD")
        import hashlib

        self.digest = hashlib.sha256(LEAN_SOURCE.encode("utf-8")).hexdigest()
        self.graph = copy.deepcopy(GRAPH)
        self.binding = {
            "binding_version": 1,
            "formal_source": {
                "repository": REPO,
                "commit": self.commit,
                "language": "Lean 4",
                "files": {"Demo.lean": self.digest},
            },
            "bindings": [
                {
                    "id": "fb.def",
                    "node": "cand.def",
                    "relation": "defines",
                    "declarations": [{"name": "Demo.Idem", "kind": "def", "file": "Demo.lean"}],
                    "fidelity_note": "same definition",
                },
                {
                    "id": "fb.claim",
                    "node": "cand.claim",
                    "relation": "proves",
                    "declarations": [{"name": "Demo.idem_id", "kind": "theorem", "file": "Demo.lean"}],
                    "fidelity_note": "same statement",
                    "non_claims": [],
                },
            ],
            "unbound": [{"node": "cand.q", "reason": "open question"}],
        }

    def tearDown(self):
        self._tmp.cleanup()

    def check(self, *extra, formal=True):
        graph_path = self.tmp / "g.json"
        binding_path = self.tmp / "g.formal_binding.json"
        graph_path.write_text(json.dumps(self.graph), encoding="utf-8")
        binding_path.write_text(json.dumps(self.binding), encoding="utf-8")
        args = [sys.executable, CHECKER, str(graph_path), str(binding_path)]
        if formal:
            args += ["--formal-repo", f"{REPO}={self.repo}", "--formal-main-ref", "main"]
        result = subprocess.run(args + list(extra), capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr

    def assertInvalid(self, diagnostic, *extra, formal=True):
        code, out = self.check(*extra, formal=formal)
        self.assertEqual(code, 1, out)
        self.assertTrue(out.startswith("INVALID FORMAL BINDING"), out)
        self.assertIn(diagnostic, out)

    def test_valid_binding_passes_and_suggests_promotion(self):
        code, out = self.check("--require-formal-check")
        self.assertEqual(code, 0, out)
        self.assertIn("promotion candidate: 'cand.claim'", out)
        self.assertIn("declarations located at", out)

    def test_structural_mode_reports_unchecked_source(self):
        code, out = self.check(formal=False)
        self.assertEqual(code, 0, out)
        self.assertIn("not checked", out)

    def test_require_formal_check_fails_without_clone(self):
        self.assertInvalid("was not checked", "--require-formal-check", formal=False)

    def test_hash_mismatch_fails(self):
        self.binding["formal_source"]["files"]["Demo.lean"] = "0" * 64
        self.assertInvalid("hash mismatch")

    def test_missing_and_commented_declarations_fail(self):
        for name in ("Demo.missing", "Demo.commented_out", "Demo.not_a_decl", "idem_id"):
            with self.subTest(name=name):
                self.binding["bindings"][1]["declarations"][0]["name"] = name
                expected = "fully qualified" if "." not in name else "not found"
                self.assertInvalid(expected)

    def test_kind_mismatch_fails(self):
        self.binding["bindings"][0]["declarations"][0]["kind"] = "abbrev"
        self.assertInvalid("is a 'def', not a 'abbrev'")

    def test_commit_outside_main_fails(self):
        git(self.repo, "checkout", "-q", "-b", "side")
        (self.repo / "Demo.lean").write_text(LEAN_SOURCE + "\n", encoding="utf-8")
        git(self.repo, "commit", "-q", "-am", "side")
        self.binding["formal_source"]["commit"] = git(self.repo, "rev-parse", "HEAD")
        self.assertInvalid("is not contained in 'main'")

    def test_restricted_proof_requires_non_claims(self):
        self.binding["bindings"][1]["relation"] = "proves_restricted"
        self.assertInvalid("requires at least one non_claims entry")
        self.binding["bindings"][1]["non_claims"] = ["only for id"]
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn("restricted evidence: 'cand.claim'", out)

    def test_relation_must_fit_node_type_and_layer(self):
        self.binding["bindings"][0]["node"] = "cand.claim"
        self.assertInvalid("cannot be attached to node type 'CandidateClaim'")
        self.binding["bindings"][0]["node"] = "raw.1"
        self.assertInvalid("only L_candidate/L_accepted may be bound")

    def test_proof_relation_needs_a_theorem(self):
        self.binding["bindings"][1]["declarations"] = [
            {"name": "Demo.Idem", "kind": "def", "file": "Demo.lean"}
        ]
        self.assertInvalid("needs at least one theorem/lemma declaration")

    def test_bound_and_unbound_conflict_fails(self):
        self.binding["unbound"].append({"node": "cand.claim", "reason": "x"})
        self.assertInvalid("both bound and listed as unbound")

    def test_proved_and_refuted_conflict_fails(self):
        refute = copy.deepcopy(self.binding["bindings"][1])
        refute.update(id="fb.refute", relation="refutes")
        self.binding["bindings"].append(refute)
        self.assertInvalid("bound as both proved and refuted")

    def test_missing_fidelity_note_and_unknown_keys_fail(self):
        self.binding["bindings"][1]["fidelity_note"] = " "
        self.assertInvalid("fidelity_note must state")
        self.binding["bindings"][1]["fidelity_note"] = "ok"
        self.binding["bindings"][1]["accepted"] = True
        self.assertInvalid("unknown keys ['accepted']")

    def promote_claim(self):
        self.graph["nodes"].append({"id": "acc.claim", "layer": "L_accepted", "type": "KernelExample"})
        self.graph["edges"].append(
            {"id": "e4", "type": "accepted_from_candidate", "source": "cand.claim", "target": "acc.claim"}
        )

    def test_refuted_candidate_is_flagged_not_promoted(self):
        self.binding["bindings"][1]["relation"] = "refutes"
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn("refuted candidate: 'cand.claim'", out)
        self.assertNotIn("promotion candidate: 'cand.claim'", out)

    def test_refuting_an_already_promoted_candidate_warns(self):
        self.promote_claim()
        self.binding["bindings"][1]["relation"] = "refutes"
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn("promoted candidate 'cand.claim' is refuted", out)

    def test_promoted_candidate_is_not_suggested_again(self):
        self.promote_claim()
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertNotIn("promotion candidate: 'cand.claim'", out)
        self.assertNotIn("neither bound", out)
        self.assertIn("accepted nodes covered via their candidate: 1", out)

    def test_unpromoted_definition_is_suggested(self):
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.assertIn("promotion candidate (definition): 'cand.def'", out)

    def test_kernel_claim_can_be_bound_directly(self):
        self.graph["nodes"].append({"id": "acc.k", "layer": "L_accepted", "type": "KernelClaim"})
        extra = dict(self.binding["bindings"][1], id="fb.k", node="acc.k")
        self.binding["bindings"].append(extra)
        code, out = self.check()
        self.assertEqual(code, 0, out)
        self.binding["bindings"][-1]["relation"] = "refutes"
        self.assertInvalid("cannot be attached to node type 'KernelClaim'")


class KernelClaimValidatorTests(unittest.TestCase):
    def validate(self, layer):
        graph = {"nodes": [{"id": "n", "layer": layer, "type": "KernelClaim"}], "edges": []}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "g.json"
            path.write_text(json.dumps(graph), encoding="utf-8")
            return run_command("kernel claim", [sys.executable, "tool/validate_r001_kernel.py", str(path)])

    def test_kernel_claim_only_in_accepted_layer(self):
        self.assertEqual(self.validate("L_accepted").returncode, 0)
        result = self.validate("L_candidate")
        self.assertEqual(result.returncode, 1)
        self.assertIn("has invalid type 'KernelClaim'", result.stdout)


class LeanScannerTests(unittest.TestCase):
    def test_namespaces_sections_and_comments(self):
        source = (
            "namespace A\nsection\n@[simp] theorem t : True := trivial\nend\n"
            "namespace B\nprivate noncomputable def d := 1\nend B\n"
            "/- nested /- lemma hidden : True := trivial -/ -/\n"
            "lemma l : True := trivial\nend A\ntheorem top : True := trivial\n"
        )
        self.assertEqual(
            lean_declarations(source),
            {"A.t": "theorem", "A.B.d": "def", "A.l": "lemma", "top": "theorem"},
        )


class RunnerIntegrationTests(unittest.TestCase):
    def test_runner_checks_f0_binding_and_skips_it_as_graph(self):
        names = [c.name for c in build_checks()]
        self.assertIn("formal binding examples/r005/f0_chat.formal_binding.json", names)
        self.assertIn("validate examples/r005/f0_chat.json", names)
        self.assertFalse(any(n.startswith("validate") and n.endswith(".formal_binding.json") for n in names))

    def test_f0_example_is_structurally_valid(self):
        check = next(c for c in build_checks() if c.name.startswith("formal binding"))
        result = run_command(check.name, check.command)
        self.assertTrue(result.ok, result.stdout + result.stderr)
        self.assertIn("unbound nodes: 2", result.stdout)
        self.assertIn("accepted nodes covered via their candidate: 5", result.stdout)


if __name__ == "__main__":
    unittest.main()
