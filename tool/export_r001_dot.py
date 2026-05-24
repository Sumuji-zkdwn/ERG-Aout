#!/usr/bin/env python3
"""Export a validated R001 graph as Graphviz DOT."""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List

from validate_r001_kernel import validate


LAYER_ORDER = ["L_raw", "L_candidate", "L_accepted", "L_gitlog"]


def dot_quote(value: object) -> str:
    text = str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def dot_node_label(node: dict) -> str:
    return f"{node.get('id', '<missing>')}\\n({node.get('type', '<missing>')})"


def emit_dot(payload: dict) -> str:
    nodes: List[dict] = payload.get("nodes", [])
    edges: List[dict] = payload.get("edges", [])

    nodes_by_layer: Dict[str, List[dict]] = defaultdict(list)
    for node in nodes:
        nodes_by_layer[node.get("layer", "<missing>")].append(node)

    lines: List[str] = []
    lines.append("digraph R001 {")
    lines.append("  rankdir=LR;")
    lines.append("  graph [compound=true];")
    lines.append("  node [shape=box];")
    lines.append("  edge [fontsize=10];")
    lines.append("")

    ordered_layers = [layer for layer in LAYER_ORDER if layer in nodes_by_layer]
    ordered_layers.extend(sorted(layer for layer in nodes_by_layer if layer not in LAYER_ORDER))

    for layer in ordered_layers:
        cluster_name = "cluster_" + "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in layer)
        lines.append(f"  subgraph {cluster_name} {{")
        lines.append(f"    label={dot_quote(layer)};")
        for node in sorted(nodes_by_layer[layer], key=lambda item: item.get("id", "")):
            node_id = node.get("id", "<missing>")
            lines.append(f"    {dot_quote(node_id)} [label={dot_quote(dot_node_label(node))}];")
        lines.append("  }")
        lines.append("")

    for edge in sorted(edges, key=lambda item: item.get("id", "")):
        source = edge.get("source", "<missing>")
        target = edge.get("target", "<missing>")
        edge_type = edge.get("type", "<missing>")
        edge_id = edge.get("id", "<missing>")
        label = f"{edge_type}\\n{edge_id}"
        lines.append(f"  {dot_quote(source)} -> {dot_quote(target)} [label={dot_quote(label)}];")

    lines.append("}")
    return "\n".join(lines) + "\n"


def load_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export a validated R001 graph as Graphviz DOT")
    parser.add_argument("graph", type=Path, help="Path to R001 graph JSON")
    parser.add_argument("-o", "--output", type=Path, help="Optional output .dot path")
    args = parser.parse_args(argv)

    payload = load_payload(args.graph)
    errors = validate(payload)
    if errors:
        print("INVALID", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    dot_text = emit_dot(payload)
    if args.output:
        args.output.write_text(dot_text, encoding="utf-8")
    else:
        print(dot_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
