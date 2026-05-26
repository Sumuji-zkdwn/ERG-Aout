#!/usr/bin/env python3
"""Render an HMDG concept patch as a small graph report.

Input:
  prototypes/cognitive_math_graph_v0/outputs/real_graph/concept_patch.json

Output:
  prototypes/cognitive_math_graph_v0/outputs/real_graph/concept_patch_graph.md

The report includes a Mermaid flowchart, typed adjacency list, and node tables.
It is meant for quick inspection before accepting or refining candidate concept
bridges and proof-facing subbridges.
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


def md_cell(value: object) -> str:
    """Render a value safely inside a Markdown table cell."""
    if value is None:
        return ""
    if isinstance(value, list):
        value = ", ".join(str(item) for item in value)
    return str(value).replace("\n", " ").replace("|", r"\|")


def node_type(node: dict) -> str:
    """Return the HMDG node type, accepting both current and proposed keys."""
    return node.get("type") or node.get("kind") or ""


def mermaid_node(node: dict) -> str:
    node_id = safe_id(node["id"])
    label = short_label(node.get("label", node["id"]))
    ntype = node_type(node)
    role = node.get("role") or f"{node.get('from_role', '')}->{node.get('to_role', '')}"
    audit_status = node.get("audit_status")
    layer = node.get("layer")
    status_note = audit_status or layer or node.get("status", "")
    text = f"{node['id']}\\n{label}\\n{ntype} / {role}"
    if status_note:
        text = f"{text}\\n{status_note}"

    if ntype == "ConceptBridge":
        return f"    {node_id}{{\"{text}\"}}"
    if ntype == "ProofBridge":
        return f"    {node_id}([\"{text}\"])"
    return f"    {node_id}[\"{text}\"]"


def mermaid_edge(edge: dict) -> str:
    source = safe_id(edge["source"])
    target = safe_id(edge["target"])
    edge_type = edge.get("type", "edge")
    if edge_type == "original_boundary_edge":
        return f"    {source} -. {edge_type} .-> {target}"
    if edge_type in {"parent_has_subbridge", "subbridge_uses_declaration", "subbridge_explains_target_step"}:
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
        # Keep all declarations, concept bridges, and proof bridges visible.
        # Long labels are shortened only in the graph, not in the tables below.
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
    lines.append("| id | label | phase edge | role shift | score | status | audit status | subbridges |")
    lines.append("|---|---|---|---|---:|---|---|---|")
    for node in nodes:
        if node_type(node) != "ConceptBridge":
            continue
        phase_edge = f"{node.get('from_phase', '')} -> {node.get('to_phase', '')}"
        role_shift = f"{node.get('from_role', '')} -> {node.get('to_role', '')}"
        lines.append(
            f"| `{node['id']}` | `{md_cell(node.get('label', ''))}` | {md_cell(phase_edge)} | "
            f"{md_cell(role_shift)} | {md_cell(node.get('score', ''))} | {md_cell(node.get('status', ''))} | "
            f"{md_cell(node.get('audit_status', ''))} | {md_cell(node.get('subbridges', []))} |"
        )

    proof_bridge_nodes = [node for node in nodes if node_type(node) == "ProofBridge"]
    if proof_bridge_nodes:
        lines += ["", "## Proof bridge table", ""]
        lines.append("| id | label | parent | role | status | summary | proof markers |")
        lines.append("|---|---|---|---|---|---|---|")
        for node in proof_bridge_nodes:
            lines.append(
                f"| `{node['id']}` | `{md_cell(node.get('label', ''))}` | `{md_cell(node.get('parent', ''))}` | "
                f"{md_cell(node.get('role', ''))} | {md_cell(node.get('status', ''))} | "
                f"{md_cell(node.get('summary', ''))} | {md_cell(node.get('proof_markers', []))} |"
            )

    lines += ["", "## Declaration table", ""]
    lines.append("| id | path index | role | label |")
    lines.append("|---|---:|---|---|")
    for node in nodes:
        if node_type(node) != "Declaration":
            continue
        lines.append(
            f"| `{node['id']}` | {node.get('path_index', '')} | {md_cell(node.get('role', ''))} | `{md_cell(node.get('label', ''))}` |"
        )

    lines += [
        "",
        "## Reading note",
        "",
        "Solid edges are proposed bridge expansions. Dotted edges preserve compressed boundary edges or show non-declaration explanatory links for auditability.",
        "",
        "`ConceptBridge` nodes are high-level cognitive phase bridges. `ProofBridge` nodes are candidate proof-facing explanatory subbridges and should not be read as declarations extracted from the formal dependency graph.",
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
