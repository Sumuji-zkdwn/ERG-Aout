#!/usr/bin/env python3
"""Check whether graph edge types are documented in semantics markdown."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Set

EDGE_HEADING_RE = re.compile(r"^#{2,3}\s+\d+\)\s+`([^`]+)`\s*$")


def extract_graph_edge_types(graph_path: Path) -> Set[str]:
    payload = json.loads(graph_path.read_text(encoding="utf-8"))
    edges = payload.get("edges", [])
    return {edge.get("type") for edge in edges if isinstance(edge.get("type"), str)}


def extract_semantics_edge_types(semantics_path: Path) -> Set[str]:
    edge_types: Set[str] = set()
    for line in semantics_path.read_text(encoding="utf-8").splitlines():
        match = EDGE_HEADING_RE.match(line.strip())
        if match:
            edge_types.add(match.group(1))
    return edge_types


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether all edge types used in an R001 graph are documented in a semantics markdown file"
    )
    parser.add_argument("graph", type=Path, help="Path to graph JSON")
    parser.add_argument("semantics", type=Path, help="Path to semantics markdown")
    args = parser.parse_args()

    graph_edge_types = extract_graph_edge_types(args.graph)
    semantics_edge_types = extract_semantics_edge_types(args.semantics)

    missing = sorted(graph_edge_types - semantics_edge_types)

    if missing:
        print("INVALID")
        print("missing edge types in semantics:")
        for edge_type in missing:
            print(f"- {edge_type}")
        return 1

    print("VALID")
    print(f"covered edge types: {len(graph_edge_types)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
