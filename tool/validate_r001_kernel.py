#!/usr/bin/env python3
"""Validate R001 ERG graph constraints.

Some enforced constraints (for example `extends_main`/`extends_branch` and
cross-layer endpoint checks) correspond to the edge semantics documented in
`docs/R001_SEMANTICS.md`.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "r001_graph.schema.json"

ALLOWED_CROSS_LAYER_ENDPOINTS = {
    "reply": ("L_raw", "L_raw"),
    "mentions": ("L_raw", "L_accepted"),
    "introduces": ("L_raw", "L_candidate"),
    "accepted_from_candidate": ("L_candidate", "L_accepted"),
    "observes_kernel_change": ("L_gitlog", "L_accepted"),
}

ALLOWED_NODE_TYPES_BY_LAYER = {
    "L_raw": {"RawMessage", "RawArtifact", "RawObservation"},
    "L_candidate": {
        "CandidateDefinition",
        "CandidateClaim",
        "CandidateExample",
        "CandidateFailureCase",
        "CandidateQuestion",
        "CandSymbol",
    },
    "L_accepted": {
        "KernelDefinition",
        "KernelAxiom",
        "KernelExample",
        "KernelFailureCase",
        "KernelDecision",
        "KConcept",
        "KernelClaim",  # R005: accepted counterpart of CandidateClaim
    },
    "L_gitlog": {"GitCommit", "GitFileDelta", "GitTagOrRound", "GitDecisionNote"},
}


def maybe_validate_schema(payload: dict) -> List[str]:
    errors: List[str] = []
    try:
        import jsonschema  # type: ignore
    except Exception:
        return errors

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    for err in validator.iter_errors(payload):
        location = "/".join(str(p) for p in err.path)
        errors.append(f"schema error at '{location}': {err.message}")
    return errors


def detect_cycle(edges: List[Tuple[str, str]]) -> bool:
    graph: Dict[str, List[str]] = {}
    for src, dst in edges:
        graph.setdefault(src, []).append(dst)

    visiting: Set[str] = set()
    visited: Set[str] = set()

    def dfs(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for nxt in graph.get(node, []):
            if dfs(nxt):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    for n in list(graph.keys()):
        if dfs(n):
            return True
    return False


def validate(payload: dict) -> List[str]:
    errors: List[str] = []
    errors.extend(maybe_validate_schema(payload))

    nodes = payload.get("nodes", [])
    edges = payload.get("edges", [])

    node_ids = [n.get("id") for n in nodes if isinstance(n, dict)]
    duplicated_node_ids = sorted({node_id for node_id in node_ids if node_ids.count(node_id) > 1})
    if duplicated_node_ids:
        errors.append(f"node ids must be unique (duplicates: {', '.join(duplicated_node_ids)})")

    edge_ids = [e.get("id") for e in edges if isinstance(e, dict)]
    duplicated_edge_ids = sorted({edge_id for edge_id in edge_ids if edge_ids.count(edge_id) > 1})
    if duplicated_edge_ids:
        errors.append(f"edge ids must be unique (duplicates: {', '.join(duplicated_edge_ids)})")

    node_map = {n["id"]: n for n in nodes if isinstance(n, dict) and "id" in n}

    for e in edges:
        src_id = e.get("source")
        dst_id = e.get("target")
        if src_id not in node_map:
            errors.append(f"edge '{e.get('id', '<unknown>')}' source node does not exist: {src_id}")
        if dst_id not in node_map:
            errors.append(f"edge '{e.get('id', '<unknown>')}' target node does not exist: {dst_id}")

    for n in nodes:
        layer = n.get("layer")
        node_type = n.get("type")
        allowed_types = ALLOWED_NODE_TYPES_BY_LAYER.get(layer)
        if allowed_types is None:
            continue
        if node_type not in allowed_types:
            errors.append(
                f"node '{n.get('id', '<unknown>')}' has invalid type '{node_type}' for layer '{layer}'"
            )

    extends_main = [(e["source"], e["target"]) for e in edges if e.get("type") == "extends_main"]
    extends_branch = [e for e in edges if e.get("type") == "extends_branch"]

    if detect_cycle(extends_main):
        errors.append("extends_main must be acyclic")

    indegree: Dict[str, int] = {}
    outdegree: Dict[str, int] = {}
    main_nodes: Set[str] = set()
    for src, dst in extends_main:
        indegree[dst] = indegree.get(dst, 0) + 1
        outdegree[src] = outdegree.get(src, 0) + 1
        main_nodes.add(src)
        main_nodes.add(dst)

        src_node = node_map.get(src, {})
        dst_node = node_map.get(dst, {})
        if src_node.get("layer") != "L_accepted" or dst_node.get("layer") != "L_accepted":
            errors.append("extends_main endpoints must both be in L_accepted")

    if extends_main:
        bad_in = [n for n, d in indegree.items() if d > 1]
        bad_out = [n for n, d in outdegree.items() if d > 1]
        if bad_in or bad_out:
            errors.append("extends_main must form a single linear path (no fan-in/fan-out)")

        starts = [n for n in main_nodes if indegree.get(n, 0) == 0]
        ends = [n for n in main_nodes if outdegree.get(n, 0) == 0]
        if len(starts) != 1 or len(ends) != 1:
            errors.append("extends_main must have exactly one start and one end node")

        # Connectivity check: all main nodes in one component reachable from start.
        if len(starts) == 1:
            seen: Set[str] = set()
            cur = starts[0]
            while cur not in seen:
                seen.add(cur)
                nxts = [dst for src, dst in extends_main if src == cur]
                if not nxts:
                    break
                cur = nxts[0]
            if seen != main_nodes:
                errors.append("extends_main must be one connected canonical chain")

    for e in extends_branch:
        src = node_map.get(e.get("source"), {})
        dst = node_map.get(e.get("target"), {})
        if src.get("layer") != "L_accepted" or dst.get("layer") != "L_accepted":
            errors.append("extends_branch endpoints must both be in L_accepted")
            continue
        if e.get("target") in main_nodes:
            errors.append("extends_branch does not modify canonical path (target must not be canonical)")

    for e in edges:
        etype = e.get("type")
        if etype not in ALLOWED_CROSS_LAYER_ENDPOINTS:
            continue
        src = node_map.get(e.get("source"), {})
        dst = node_map.get(e.get("target"), {})
        expected_src, expected_dst = ALLOWED_CROSS_LAYER_ENDPOINTS[etype]
        if src.get("layer") != expected_src or dst.get("layer") != expected_dst:
            errors.append(
                f"cross-layer policy violation for '{etype}': expected "
                f"{expected_src} -> {expected_dst}"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate R001 kernel graph")
    parser.add_argument("graph", type=Path, help="Path to graph JSON")
    args = parser.parse_args()

    payload = json.loads(args.graph.read_text(encoding="utf-8"))
    errors = validate(payload)
    if errors:
        print("INVALID")
        for e in errors:
            print(f"- {e}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
