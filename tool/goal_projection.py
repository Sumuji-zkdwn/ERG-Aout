#!/usr/bin/env python3
"""Project a finite ERG goal table onto its essential Boolean features."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def read_object(path: Path) -> dict:
    def unique_keys(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError(f"{path}: duplicate JSON key {key!r}")
            obj[key] = value
        return obj

    obj = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
    if not isinstance(obj, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return obj


def fields(obj, expected):
    if not isinstance(obj, dict) or set(obj) != set(expected):
        raise ValueError(f"expected fields {', '.join(sorted(expected))}")


def label(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("expected a nonempty string")
    return value


def read_table(obj, *, source):
    """Require a total function on the declared cube, including the empty cube."""
    row_key = "cases" if source else "rows"
    features = obj["features"]
    if not isinstance(features, list) or len({label(f) for f in features}) != len(features):
        raise ValueError("features must be a list of distinct names")
    if not isinstance(obj[row_key], list):
        raise ValueError(f"{row_key} must be a list")
    outcomes = {}
    case_ids = {}
    seen_ids = set()
    for row in obj[row_key]:
        fields(row, ("id", "values", "outcome") if source else ("values", "outcome"))
        values = row["values"]
        if (not isinstance(values, list) or len(values) != len(features)
                or any(type(v) is not bool for v in values)):
            raise ValueError("each row needs one JSON boolean per feature")
        key = tuple(values)
        if key in outcomes:
            raise ValueError(f"duplicate input {values}")
        outcomes[key] = label(row["outcome"])
        if source:
            case_id = label(row["id"])
            if case_id in seen_ids:
                raise ValueError(f"duplicate case id {case_id!r}")
            seen_ids.add(case_id)
            case_ids[key] = case_id
    if len(outcomes) != 2 ** len(features):
        raise ValueError(f"{row_key} must cover every Boolean assignment")
    return features, outcomes, case_ids


def read_source(path: Path):
    obj = read_object(path)
    fields(obj, ("graph", "node", "goal", "features", "cases"))
    label(obj["goal"])
    graph = read_object(path.parent / label(obj["graph"]))
    node = label(obj["node"])
    nodes = graph.get("nodes")
    if not isinstance(nodes, list) or sum(
        isinstance(n, dict) and n.get("id") == node for n in nodes
    ) != 1:
        raise ValueError(f"expected one graph node with id {node!r}")
    return read_table(obj, source=True)


def project(features, outcomes):
    # A differing pair of neighbors forces that coordinate into every exact
    # projection. Flipping the other coordinates one at a time preserves the label.
    keep = []
    for i in sorted(range(len(features)), key=features.__getitem__):
        if any(
            not key[i] and result != outcomes[key[:i] + (True,) + key[i + 1:]]
            for key, result in outcomes.items()
        ):
            keep.append(i)
    reduced = {tuple(key[i] for i in keep): result for key, result in outcomes.items()}
    return {
        "features": [features[i] for i in keep],
        "rows": [{"values": list(key), "outcome": reduced[key]} for key in sorted(reduced)],
    }


def check(features, outcomes, case_ids, candidate):
    fields(candidate, ("features", "rows"))
    chosen, predictions, _ = read_table(candidate, source=False)
    unknown = set(chosen) - set(features)
    if unknown:
        raise ValueError(f"unknown features: {sorted(unknown)}")
    indices = [features.index(name) for name in chosen]
    for key, expected in outcomes.items():
        actual = predictions[tuple(key[i] for i in indices)]
        if actual != expected:
            return {
                "case": case_ids[key],
                "input": dict(zip(features, key)),
                "expected": expected,
                "actual": actual,
            }
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sidecar", type=Path)
    parser.add_argument("--check", type=Path, metavar="FORM",
                        help="compare an independently supplied form on every source input")
    args = parser.parse_args()
    try:
        features, outcomes, case_ids = read_source(args.sidecar)
        if args.check is None:
            result = project(features, outcomes)
            status = 0
        else:
            witness = check(features, outcomes, case_ids, read_object(args.check))
            result = {"equivalent": witness is None, "cases": len(outcomes)}
            if witness is not None:
                result["counterexample"] = witness
            status = int(witness is not None)
    except (OSError, ValueError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
