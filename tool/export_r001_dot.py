#!/usr/bin/env python3
"""Export a validated R001 graph as Graphviz DOT."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Set, Tuple

from validate_r001_kernel import validate


LAYER_ORDER = ["L_raw", "L_candidate", "L_accepted", "L_gitlog"]
VIEW_CHOICES = ["full", "accepted", "spine"]
NODE_LABEL_CHOICES = ["id", "short"]
EDGE_LABEL_CHOICES = ["id", "type", "none"]
EDGE_TYPE_SHORT_NAMES = {
    "extends_main": "main",
    "extends_branch": "branch",
    "accepted_from_candidate": "accepts",
    "observes_kernel_change": "observes",
}


def dot_quote(value: object) -> str:
    text = str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def humanize_tail(value: str) -> str:
    return value.replace("_", " ")


def short_node_name(node_id: str) -> str:
    pr_match = re.fullmatch(r"acc\.pr(\d+)\.(.+)", node_id)
    if pr_match:
        return f"PR {pr_match.group(1)}: {humanize_tail(pr_match.group(2))}"

    git_match = re.fullmatch(r"git\.pr(\d+)\.merged", node_id)
    if git_match:
        return f"PR {git_match.group(1)} merged"

    prefix_replacements = [
        ("acc.branch.", "branch: "),
        ("cand.", "cand: "),
        ("raw.user.", "user: "),
        ("raw.codex.", "codex: "),
        ("git.", "git: "),
    ]
    for prefix, label in prefix_replacements:
        if node_id.startswith(prefix):
            return label + humanize_tail(node_id[len(prefix):])

    return humanize_tail(node_id)


def dot_node_label(node: dict, label_mode: str = "id") -> str:
    node_id = str(node.get("id", "<missing>"))
    node_type = node.get("type", "<missing>")

    if label_mode == "short":
        return short_node_name(node_id)
    if label_mode == "id":
        return f"{node_id}\\n({node_type})"
    raise ValueError(f"unknown node label mode: {label_mode}")


def dot_edge_attributes(edge: dict, edge_label: str = "id") -> str:
    edge_type = str(edge.get("type", "<missing>"))
    edge_id = str(edge.get("id", "<missing>"))

    if edge_label == "none":
        return ""
    if edge_label == "type":
        return f" [label={dot_quote(EDGE_TYPE_SHORT_NAMES.get(edge_type, edge_type))}]"
    if edge_label == "id":
        return f" [label={dot_quote(edge_type + chr(10) + edge_id)}]"
    raise ValueError(f"unknown edge label mode: {edge_label}")


def canonical_chain(edges: List[dict]) -> List[str]:
    extends_main: List[Tuple[str, str]] = [
        (edge["source"], edge["target"]) for edge in edges if edge.get("type") == "extends_main"
    ]
    if not extends_main:
        return []

    indegree: Dict[str, int] = {}
    outgoing: Dict[str, str] = {}
    nodes: Set[str] = set()
    for src, dst in extends_main:
        indegree[dst] = indegree.get(dst, 0) + 1
        outgoing[src] = dst
        nodes.add(src)
        nodes.add(dst)

    starts = [node for node in nodes if indegree.get(node, 0) == 0]
    if len(starts) != 1:
        return []

    chain: List[str] = []
    cur = starts[0]
    seen: Set[str] = set()
    while cur not in seen:
        seen.add(cur)
        chain.append(cur)
        nxt = outgoing.get(cur)
        if nxt is None:
            break
        cur = nxt
    return chain


def filtered_payload(payload: dict, view: str) -> dict:
    nodes: List[dict] = payload.get("nodes", [])
    edges: List[dict] = payload.get("edges", [])

    if view == "full":
        return {"nodes": nodes, "edges": edges}

    if view == "accepted":
        accepted_ids = {node["id"] for node in nodes if node.get("layer") == "L_accepted"}
        accepted_nodes = [node for node in nodes if node.get("id") in accepted_ids]
        accepted_edges = [
            edge
            for edge in edges
            if edge.get("type") in {"extends_main", "extends_branch"}
            and edge.get("source") in accepted_ids
            and edge.get("target") in accepted_ids
        ]
        return {"nodes": accepted_nodes, "edges": accepted_edges}

    if view == "spine":
        chain_ids = set(canonical_chain(edges))
        spine_nodes = [node for node in nodes if node.get("id") in chain_ids]
        spine_edges = [
            edge
            for edge in edges
            if edge.get("type") == "extends_main"
            and edge.get("source") in chain_ids
            and edge.get("target") in chain_ids
        ]
        return {"nodes": spine_nodes, "edges": spine_edges}

    raise ValueError(f"unknown view: {view}")


def emit_dot(
    payload: dict,
    view: str = "full",
    node_label: str = "id",
    edge_label: str = "id",
) -> str:
    projected = filtered_payload(payload, view)
    nodes: List[dict] = projected.get("nodes", [])
    edges: List[dict] = projected.get("edges", [])

    nodes_by_layer: Dict[str, List[dict]] = defaultdict(list)
    for node in nodes:
        nodes_by_layer[node.get("layer", "<missing>")].append(node)

    lines: List[str] = []
    lines.append("digraph R001 {")
    lines.append(f"  label={dot_quote('R001 view: ' + view)};")
    lines.append("  labelloc=t;")
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
            lines.append(
                f"    {dot_quote(node_id)} [label={dot_quote(dot_node_label(node, node_label))}];"
            )
        lines.append("  }")
        lines.append("")

    for edge in sorted(edges, key=lambda item: item.get("id", "")):
        source = edge.get("source", "<missing>")
        target = edge.get("target", "<missing>")
        attrs = dot_edge_attributes(edge, edge_label)
        lines.append(f"  {dot_quote(source)} -> {dot_quote(target)}{attrs};")

    lines.append("}")
    return "\n".join(lines) + "\n"


def load_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export a validated R001 graph as Graphviz DOT")
    parser.add_argument("graph", type=Path, help="Path to R001 graph JSON")
    parser.add_argument("-o", "--output", type=Path, help="Optional output .dot path")
    parser.add_argument(
        "--view",
        choices=VIEW_CHOICES,
        default="full",
        help="Projection view to export: full, accepted, or spine",
    )
    parser.add_argument(
        "--node-label",
        choices=NODE_LABEL_CHOICES,
        default="id",
        help="Node label mode: id preserves raw node ids; short uses compact display names",
    )
    parser.add_argument(
        "--edge-label",
        choices=EDGE_LABEL_CHOICES,
        default="id",
        help="Edge label mode: id preserves full labels; type shows compact edge types; none hides labels",
    )
    args = parser.parse_args(argv)

    payload = load_payload(args.graph)
    errors = validate(payload)
    if errors:
        print("INVALID", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    dot_text = emit_dot(
        payload,
        view=args.view,
        node_label=args.node_label,
        edge_label=args.edge_label,
    )
    if args.output:
        args.output.write_text(dot_text, encoding="utf-8")
    else:
        print(dot_text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
