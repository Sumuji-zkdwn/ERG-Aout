#!/usr/bin/env python3
"""Render an HMDG concept patch as a small graph report.

Input:
  prototypes/cognitive_math_graph_v0/outputs/real_graph/concept_patch.json

Output:
  prototypes/cognitive_math_graph_v0/outputs/real_graph/concept_patch_graph.md

The report includes a Mermaid flowchart, typed adjacency list, and node table.
It is meant for quick inspection before accepting or refining candidate concept
bridges.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def safe_id(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9_]", "_", text)


def short_label(label: str, max_len: int = 48) -> str:
    if len(label) <= max_len:
        return label
    return label[: max_len - 3] + "..."


def mermaid_node(node: dict) -> str:
    node_id = safe_id(node["id"])
    label = short_label(node.get("label", node["id"]))
    node_type = node.get("type", "")
    role = node.get("role") or f"{node.get('from_role', '')}->{node.get('to_role', '')}"
    text = f"{node['id']}\\n{label}\\n{node_type} / {role}"
    if node_type == "ConceptBridge":
        return f"    {node_id}{{\"{text}\"}}"
    return f"    {node_id}[\"{text}\"]"


def mermaid_edge(edge: dict) -> str:
    source = safe_id(edge["source"])
    target = safe_id(edge["target"])
    edge_type = edge.get("type", "edge")
    if edge_type == "original_boundary_edge":
        return f"    {source} -. {edge_type} .-> {target}"
    return f"    {source} -- {edge_type} --> {target}"


def render_report(patch: dict) -> str:
    nodes = patch.get("nodes", [])
    edges = patch.get("edges", [])
    label_by_id = {node["id"]: node.get("label", node["id"]) for node in nodes}

    lines = [
        "# HMDG concept patch graph",
        "",
        f"target: `{patch.get('target', '')}`",
        f"path_length: {patch.get('path_length', '')}",
        f"node_count: {len(nodes)}",
        f"edge_count: {len(edges)}",
        "",
        "## Mermaid graph",
        "",
        "```mermaid",
        "flowchart LR",
    ]

    for node in nodes:
        # Keep all declarations and concept bridges visible. Declaration labels may be long,
        # so labels are shortened only in the graph, not in the tables below.
        lines.append(mermaid_node(node))
    for edge in edges:
        lines.append(mermaid_edge(edge))
    lines.append("```")

    lines += ["", "## Typed adjacency list", ""]
    for edge in edges:
        src = f"{edge['source']}:{label_by_id.get(edge['source'], '')}"
        dst = f"{edge['target']}:{label_by_id.get(edge['target'], '')}"
        lines.append(f"- `{src}` -[{edge.get('type', '')}]-> `{dst}`")

    lines += ["", "## Concept bridge table", ""]
    lines.append("| id | label | phase edge | role shift | score | status |")
    lines.append("|---|---|---|---|---:|---|")
    for node in nodes:
        if node.get("type") != "ConceptBridge":
            continue
        phase_edge = f"{node.get('from_phase', '')} -> {node.get('to_phase', '')}"
        role_shift = f"{node.get('from_role', '')} -> {node.get('to_role', '')}"
        lines.append(
            f"| `{node['id']}` | `{node.get('label', '')}` | {phase_edge} | {role_shift} | {node.get('score', '')} | {node.get('status', '')} |"
        )

    lines += ["", "## Declaration table", ""]
    lines.append("| id | path index | role | label |")
    lines.append("|---|---:|---|---|")
    for node in nodes:
        if node.get("type") != "Declaration":
            continue
        lines.append(
            f"| `{node['id']}` | {node.get('path_index', '')} | {node.get('role', '')} | `{node.get('label', '')}` |"
        )

    lines += [
        "",
        "## Reading note",
        "",
        "Solid edges are proposed bridge expansions. Dotted edges preserve the original compressed boundary edge for auditability.",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="prototypes/cognitive_math_graph_v0/outputs/real_graph/concept_patch.json")
    parser.add_argument("--output", default="prototypes/cognitive_math_graph_v0/outputs/real_graph/concept_patch_graph.md")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    patch = json.loads(input_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_report(patch), encoding="utf-8")
    print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()
