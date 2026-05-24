#!/usr/bin/env python3
"""Inspect a validated R001 graph."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

from validate_r001_kernel import validate


def canonical_chain(edges: List[dict]) -> List[str]:
    extends_main: List[Tuple[str, str]] = [
        (edge["source"], edge["target"]) for edge in edges if edge.get("type") == "extends_main"
    ]
    if not extends_main:
        return []

    indegree: Dict[str, int] = {}
    outgoing: Dict[str, str] = {}
    nodes = set()
    for src, dst in extends_main:
        indegree[dst] = indegree.get(dst, 0) + 1
        outgoing[src] = dst
        nodes.add(src)
        nodes.add(dst)

    starts = [node for node in nodes if indegree.get(node, 0) == 0]
    if len(starts) != 1:
        return []

    chain = []
    cur = starts[0]
    seen = set()
    while cur not in seen:
        seen.add(cur)
        chain.append(cur)
        nxt = outgoing.get(cur)
        if nxt is None:
            break
        cur = nxt
    return chain


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect R001 graph structure")
    parser.add_argument("graph", type=Path, help="Path to graph JSON")
    args = parser.parse_args()

    payload = json.loads(args.graph.read_text(encoding="utf-8"))
    errors = validate(payload)
    if errors:
        print("INVALID")
        for err in errors:
            print(f"- {err}")
        return 1

    nodes = payload.get("nodes", [])
    edges = payload.get("edges", [])

    layer_counts = Counter(node.get("layer", "<missing>") for node in nodes)
    edge_type_counts = Counter(edge.get("type", "<missing>") for edge in edges)
    main_chain = canonical_chain(edges)
    branch_edges = [
        (edge.get("source", "<missing>"), edge.get("target", "<missing>"))
        for edge in edges
        if edge.get("type") == "extends_branch"
    ]

    print("VALID")
    print("node counts by layer")
    for layer in sorted(layer_counts):
        print(f"- {layer}: {layer_counts[layer]}")

    print("edge counts by type")
    for edge_type in sorted(edge_type_counts):
        print(f"- {edge_type}: {edge_type_counts[edge_type]}")

    print("extends_main canonical chain")
    if main_chain:
        print(f"- {' -> '.join(main_chain)}")
    else:
        print("- <none>")

    print("extends_branch edges")
    if branch_edges:
        for src, dst in branch_edges:
            print(f"- {src} -> {dst}")
    else:
        print("- <none>")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
