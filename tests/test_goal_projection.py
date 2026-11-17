import json
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from itertools import combinations, product
from pathlib import Path

from tool.goal_projection import project


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tool/goal_projection.py"
SIDECAR = ROOT / "examples/goal_projection/f0_period_bound.goal.json"
FEATURES = ["returns_at_p", "first_p_distinct", "starts_at_zero"]
DROP_DISTINCT = SIDECAR.with_name("drop_distinct.form.json")


def least_return(mapping, start):
    """A first return, if any, occurs within the carrier size."""
    current = start
    for time in range(1, len(mapping) + 1):
        current = mapping[current]
        if current == start:
            return time
    return None


def observations(mapping, start, p):
    trajectory = [start]
    for _ in range(p):
        trajectory.append(mapping[trajectory[-1]])
    return trajectory[-1] == start, len(set(trajectory[:-1])) == p, start == 0


def convert_or_check(*args):
    return subprocess.run(
        [sys.executable, str(TOOL), str(SIDECAR), *map(str, args)],
        capture_output=True, text=True,
    )


def single_feature_form(feature):
    return {
        "features": [feature],
        "rows": [
            {"values": [False], "outcome": "outside_scope"},
            {"values": [True], "outcome": "covered"},
        ],
    }


class GoalProjectionTests(unittest.TestCase):
    def check_form(self, form):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "form.json"
            path.write_text(json.dumps(form), encoding="utf-8")
            return convert_or_check("--check", path)

    def test_reference_agrees_with_first_return_on_every_bounded_orbit(self):
        spec = json.loads(SIDECAR.read_text(encoding="utf-8"))
        self.assertEqual(spec["node"], "cand.f0.period_bound")
        self.assertEqual(spec["features"], FEATURES)
        outcomes = {tuple(row["values"]): row["outcome"] for row in spec["cases"]}
        self.assertEqual(len(spec["cases"]), 8)
        self.assertEqual(set(outcomes), set(product((False, True), repeat=3)))

        counts = Counter()
        false_positives = Counter()
        realized = set()
        for size in range(1, 4):
            for mapping in product(range(size), repeat=size):
                for start in range(size):
                    first = least_return(mapping, start)
                    for p in range(1, 5):
                        values = observations(mapping, start, p)
                        expected = "covered" if first == p else "outside_scope"
                        self.assertEqual(outcomes[values], expected, (mapping, start, p))
                        realized.add(values)
                        counts[expected] += 1
                        if expected == "outside_scope":
                            if values[0]:
                                false_positives["drop_distinct"] += 1
                            if values[1]:
                                false_positives["drop_return"] += 1
        self.assertEqual(realized, set(outcomes))
        self.assertEqual(counts, {"covered": 58, "outside_scope": 302})
        self.assertEqual(false_positives, {"drop_distinct": 116, "drop_return": 108})

    def test_minimum_projection_round_trips(self):
        result = convert_or_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        form = json.loads(result.stdout)
        self.assertCountEqual(form["features"], FEATURES[:2])
        rows = {tuple(row["values"]): row["outcome"] for row in form["rows"]}
        self.assertEqual(len(form["rows"]), 4)
        self.assertEqual(rows, {
            bits: "covered" if all(bits) else "outside_scope"
            for bits in product((False, True), repeat=2)
        })
        checked = self.check_form(form)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_each_missing_premise_is_detected(self):
        # A fixed point traversed twice returns; its two visited points coincide.
        # At a transient start, a length-one prefix is distinct; it never returns.
        for retained, mapping, start, p in [
            ("returns_at_p", (0,), 0, 2),
            ("first_p_distinct", (1, 1), 0, 1),
        ]:
            with self.subTest(retained=retained):
                values = observations(mapping, start, p)
                self.assertTrue(values[FEATURES.index(retained)])
                self.assertNotEqual(p, least_return(mapping, start))
                checked = self.check_form(single_feature_form(retained))
                self.assertEqual(checked.returncode, 1, checked.stdout + checked.stderr)
                witness = json.loads(checked.stdout)["counterexample"]
                self.assertTrue(witness["input"][retained])
                self.assertEqual(witness["expected"], "outside_scope")
                self.assertEqual(witness["actual"], "covered")

    def test_shipped_mutant_reports_repeated_singleton_cycle(self):
        checked = convert_or_check("--check", DROP_DISTINCT)
        self.assertEqual(checked.returncode, 1, checked.stdout + checked.stderr)
        self.assertEqual(json.loads(checked.stdout)["counterexample"], {
            "case": "singleton_0_identity_p2",
            "input": dict(zip(FEATURES, (True, False, True))),
            "expected": "outside_scope",
            "actual": "covered",
        })

    def test_projection_is_minimum_for_all_three_feature_binary_functions(self):
        assignments = list(product((False, True), repeat=3))
        names = ["a", "b", "c"]
        for labels in product(("yes", "no"), repeat=len(assignments)):
            outcomes = dict(zip(assignments, labels))
            form = project(names, outcomes)
            chosen = tuple(names.index(name) for name in form["features"])
            reduced = {tuple(row["values"]): row["outcome"] for row in form["rows"]}
            for bits, outcome in outcomes.items():
                self.assertEqual(reduced[tuple(bits[i] for i in chosen)], outcome)
            # Direct comparison of all inputs sharing the same projected values.
            # Every sufficient choice of indices must include the chosen ones.
            for width in range(4):
                for indices in combinations(range(3), width):
                    grouped = {}
                    for bits, outcome in outcomes.items():
                        key = tuple(bits[i] for i in indices)
                        grouped.setdefault(key, set()).add(outcome)
                    if all(len(group) == 1 for group in grouped.values()):
                        self.assertTrue(set(chosen) <= set(indices), (labels, indices))
        empty = project([], {(): "constant"})
        self.assertEqual(empty["features"], [])
        self.assertEqual(len(empty["rows"]), 1)
        self.assertEqual(tuple(empty["rows"][0]["values"]), ())
        self.assertEqual(empty["rows"][0]["outcome"], "constant")

    def test_an_incomplete_or_ill_typed_table_is_invalid(self):
        incomplete = single_feature_form("returns_at_p")
        incomplete["rows"].pop()
        non_boolean = single_feature_form("returns_at_p")
        non_boolean["rows"][0]["values"] = [0]
        for form in (incomplete, non_boolean):
            with self.subTest(form=form):
                checked = self.check_form(form)
                self.assertEqual(checked.returncode, 2, checked.stdout + checked.stderr)


if __name__ == "__main__":
    unittest.main()
