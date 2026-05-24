#!/usr/bin/env python3
"""Checklist-driven consistency helper for R002 manual mapping.

This helper is NOT a replacement for `tool/validate_r001_kernel.py`.
Use it after the validator as a manual-mapping aid for existing graph JSON.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple


class StructureError(ValueError):
    """Raised when JSON structure is not compatible with checker expectations."""


def load_graph(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StructureError(f"graph file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StructureError(f"invalid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise StructureError("top-level JSON must be an object")

    nodes = payload.get("nodes")
    edges = payload.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise StructureError("graph must include list fields: 'nodes' and 'edges'")

    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise StructureError(f"node at index {i} is not an object")
        for k in ("id", "layer", "type"):
            if k not in node:
                raise StructureError(f"node at index {i} missing required key: {k}")

    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            raise StructureError(f"edge at index {i} is not an object")
        for k in ("id", "type", "source", "target"):
            if k not in edge:
                raise StructureError(f"edge at index {i} missing required key: {k}")

    return payload


def canonical_spine(extends_main: List[Tuple[str, str]]) -> Set[str]:
    main_nodes: Set[str] = set()
    for src, dst in extends_main:
        main_nodes.add(src)
        main_nodes.add(dst)
    return main_nodes


def main() -> int:
    parser = argparse.ArgumentParser(description="Check R002 manual mapping consistency hints")
    parser.add_argument("graph", type=Path, help="Path to graph JSON")
    args = parser.parse_args()

    try:
        payload = load_graph(args.graph)
    except StructureError as exc:
        print("INVALID R002 MAPPING CONSISTENCY INPUT")
        print(f"- {exc}")
        return 1

    nodes = payload["nodes"]
    edges = payload["edges"]

    node_map: Dict[str, dict] = {n["id"]: n for n in nodes}
    raw_nodes = {n["id"] for n in nodes if n.get("layer") == "L_raw"}
    candidate_nodes = {n["id"] for n in nodes if n.get("layer") == "L_candidate"}
    accepted_nodes = {n["id"] for n in nodes if n.get("layer") == "L_accepted"}

    incoming: Dict[str, List[dict]] = {}
    outgoing: Dict[str, List[dict]] = {}
    for edge in edges:
        outgoing.setdefault(edge["source"], []).append(edge)
        incoming.setdefault(edge["target"], []).append(edge)

    warnings: List[str] = []

    for accepted_id in sorted(accepted_nodes):
        if not any(e.get("type") == "accepted_from_candidate" for e in incoming.get(accepted_id, [])):
            warnings.append(
                f"accepted node '{accepted_id}' has no incoming accepted_from_candidate"
            )

    for candidate_id in sorted(candidate_nodes):
        if not any(e.get("type") == "introduces" for e in incoming.get(candidate_id, [])):
            warnings.append(f"candidate node '{candidate_id}' has no incoming introduces")

    for candidate_id in sorted(candidate_nodes):
        if "unaccepted" in candidate_id and any(
            e.get("type") == "accepted_from_candidate" for e in outgoing.get(candidate_id, [])
        ):
            warnings.append(
                f"unaccepted candidate '{candidate_id}' has outgoing accepted_from_candidate"
            )

    extends_main_edges = [e for e in edges if e.get("type") == "extends_main"]
    extends_branch_edges = [e for e in edges if e.get("type") == "extends_branch"]

    for edge in extends_main_edges + extends_branch_edges:
        src = node_map.get(edge["source"], {})
        dst = node_map.get(edge["target"], {})
        if src.get("layer") != "L_accepted" or dst.get("layer") != "L_accepted":
            warnings.append(
                f"{edge['type']} edge '{edge['id']}' should connect accepted->accepted, got "
                f"{src.get('layer')}->{dst.get('layer')}"
            )

    main_spine_nodes = canonical_spine([(e["source"], e["target"]) for e in extends_main_edges])
    branch_targets = sorted({e["target"] for e in extends_branch_edges})
    for t in branch_targets:
        if t in main_spine_nodes:
            warnings.append(
                f"extends_branch target '{t}' appears in extends_main canonical spine"
            )

    has_mentions_raw_to_accepted = any(
        e.get("type") == "mentions"
        and e.get("source") in raw_nodes
        and e.get("target") in accepted_nodes
        for e in edges
    )
    has_acc_from_candidate = any(e.get("type") == "accepted_from_candidate" for e in edges)
    if has_mentions_raw_to_accepted and has_acc_from_candidate:
        warnings.append(
            "graph uses both raw->accepted mentions and candidate->accepted accepted_from_candidate; "
            "confirm they are not being semantically conflated"
        )

    for candidate_id in sorted(candidate_nodes):
        if not incoming.get(candidate_id):
            warnings.append(
                f"candidate '{candidate_id}' has no incoming edges at all (possibly missing raw->candidate introduces)"
            )

    for edge in [e for e in edges if e.get("type") == "accepted_from_candidate"]:
        src_layer = node_map.get(edge["source"], {}).get("layer")
        dst_layer = node_map.get(edge["target"], {}).get("layer")
        if src_layer != "L_candidate" or dst_layer != "L_accepted":
            warnings.append(
                f"accepted_from_candidate edge '{edge['id']}' should be candidate->accepted, got {src_layer}->{dst_layer}"
            )

    for edge in [e for e in edges if e.get("type") == "mentions"]:
        src_layer = node_map.get(edge["source"], {}).get("layer")
        dst_layer = node_map.get(edge["target"], {}).get("layer")
        if src_layer != "L_raw" or dst_layer != "L_accepted":
            warnings.append(
                f"mentions edge '{edge['id']}' should be raw->accepted, got {src_layer}->{dst_layer}"
            )

    unaccepted_candidates = sorted([n for n in candidate_nodes if "unaccepted" in n])

    print("VALID R002 MAPPING CONSISTENCY")
    if warnings:
        print("WARNINGS")
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("WARNINGS")
        print("- none")

    print("SUMMARY")
    print(f"- raw nodes: {len(raw_nodes)}")
    print(f"- candidate nodes: {len(candidate_nodes)}")
    print(f"- accepted nodes: {len(accepted_nodes)}")
    print(f"- unaccepted candidates: {', '.join(unaccepted_candidates) if unaccepted_candidates else '(none)'}")
    print(f"- main spine: {', '.join(sorted(main_spine_nodes)) if main_spine_nodes else '(none)'}")
    print(f"- branch targets: {', '.join(branch_targets) if branch_targets else '(none)'}")
    print("- note: this checker is a manual-mapping helper, not a validator replacement")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
