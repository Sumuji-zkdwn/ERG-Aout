#!/usr/bin/env python3
"""Export validated R001/R002 graph JSON to static PNG via matplotlib/networkx.

This helper is for manual review convenience only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from validate_r001_kernel import validate

MISSING_DEPS_MESSAGE = (
    "Missing optional dependency: matplotlib/networkx. Install with: "
    "python -m pip install matplotlib networkx"
)

VIEW_CHOICES = ["full", "accepted", "spine"]
LABEL_CHOICES = ["id", "short", "excerpt", "id_excerpt"]
LAYER_ORDER = ["L_raw", "L_candidate", "L_accepted", "L_gitlog"]
EDGE_STYLE = {
    "introduces": {"color": "#666666", "style": "solid", "width": 1.0},
    "accepted_from_candidate": {"color": "#1f77b4", "style": "solid", "width": 1.6},
    "extends_main": {"color": "#2ca02c", "style": "solid", "width": 2.2},
    "extends_branch": {"color": "#ff7f0e", "style": "dashed", "width": 1.6},
    "mentions": {"color": "#9467bd", "style": "dotted", "width": 1.2},
}


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
            return label + humanize_tail(node_id[len(prefix) :])

    return humanize_tail(node_id)


def canonical_chain(edges: List[dict]) -> List[str]:
    extends_main = [(e["source"], e["target"]) for e in edges if e.get("type") == "extends_main"]
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
    starts = sorted([n for n in nodes if indegree.get(n, 0) == 0])
    if len(starts) != 1:
        return []

    chain: List[str] = []
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


def split_markdown_row(line: str) -> List[str]:
    text = line.strip()
    if not text.startswith("|") or not text.endswith("|"):
        return []
    return [c.strip() for c in text[1:-1].split("|")]


def is_separator_row(cells: List[str]) -> bool:
    if not cells:
        return False
    allowed = set("-: ")
    return all(cell and set(cell) <= allowed and "-" in cell for cell in cells)


def load_sidecar_map(path: Path | None) -> Dict[str, str]:
    if path is None:
        return {}
    lines = path.read_text(encoding="utf-8").splitlines()

    header_cells: List[str] | None = None
    start_idx = -1
    for i, line in enumerate(lines):
        header = split_markdown_row(line)
        if header and i + 1 < len(lines):
            sep = split_markdown_row(lines[i + 1])
            if sep and len(sep) == len(header) and is_separator_row(sep):
                header_cells = header
                start_idx = i + 2
                break
    if header_cells is None or "raw_id" not in header_cells or "text_excerpt" not in header_cells:
        return {}

    raw_idx = header_cells.index("raw_id")
    excerpt_idx = header_cells.index("text_excerpt")

    mapping: Dict[str, str] = {}
    for j in range(start_idx, len(lines)):
        row = split_markdown_row(lines[j])
        if not row or len(row) != len(header_cells):
            break
        mapping[row[raw_idx]] = row[excerpt_idx]
    return mapping


def filtered_payload(payload: dict, view: str) -> Tuple[List[dict], List[dict]]:
    nodes = payload.get("nodes", [])
    edges = payload.get("edges", [])
    if view == "full":
        return nodes, edges
    if view == "accepted":
        accepted_ids = {n["id"] for n in nodes if n.get("layer") == "L_accepted"}
        return (
            [n for n in nodes if n.get("id") in accepted_ids],
            [
                e
                for e in edges
                if e.get("type") in {"extends_main", "extends_branch"}
                and e.get("source") in accepted_ids
                and e.get("target") in accepted_ids
            ],
        )
    if view == "spine":
        chain_ids = set(canonical_chain(edges))
        return (
            [n for n in nodes if n.get("id") in chain_ids],
            [
                e
                for e in edges
                if e.get("type") == "extends_main"
                and e.get("source") in chain_ids
                and e.get("target") in chain_ids
            ],
        )
    raise ValueError(f"unknown view: {view}")


def truncate_wrap(text: str, max_chars: int) -> str:
    clean = " ".join(text.split())
    clipped = clean if len(clean) <= max_chars else clean[: max_chars - 1] + "…"
    return "\n".join(textwrap.wrap(clipped, width=max(12, min(max_chars, 24)))) if clipped else ""


def node_label(node: dict, label_mode: str, sidecar: Dict[str, str], max_chars: int) -> str:
    node_id = str(node.get("id", "<missing>"))
    layer = node.get("layer")
    short = short_node_name(node_id)
    excerpt = sidecar.get(node_id, "")

    if label_mode == "id":
        base = node_id
    elif label_mode == "short":
        base = short
    elif label_mode == "excerpt":
        if layer == "L_raw" and excerpt:
            base = excerpt
        elif layer in {"L_candidate", "L_accepted", "L_gitlog"}:
            base = short
        else:
            base = node_id
    elif label_mode == "id_excerpt":
        if layer == "L_raw" and excerpt:
            base = f"{node_id}: {excerpt}"
        elif short != node_id:
            base = f"{node_id}: {short}"
        else:
            base = node_id
    else:
        raise ValueError(f"unknown label mode: {label_mode}")
    return truncate_wrap(base, max_chars)


def build_positions(nodes: List[dict], edges: List[dict], view: str) -> Dict[str, Tuple[float, float]]:
    pos: Dict[str, Tuple[float, float]] = {}
    by_id = {n["id"]: n for n in nodes}

    if view == "spine":
        chain = canonical_chain(edges)
        for i, nid in enumerate(chain):
            pos[nid] = (float(i), 0.0)
        return pos

    if view == "accepted":
        chain = canonical_chain(edges)
        index = {nid: i for i, nid in enumerate(chain)}
        for nid in sorted(by_id):
            pos[nid] = (float(index.get(nid, len(index))), 0.0)
        branch_count: Dict[str, int] = {}
        for edge in sorted(edges, key=lambda e: e.get("id", "")):
            if edge.get("type") != "extends_branch":
                continue
            src, dst = edge.get("source"), edge.get("target")
            if src in pos and dst in pos:
                branch_count[src] = branch_count.get(src, 0) + 1
                pos[dst] = (pos[src][0] + 0.2 * branch_count[src], -float(branch_count[src]))
        return pos

    layer_x = {"L_raw": 0.0, "L_candidate": 1.8, "L_accepted": 3.6, "L_gitlog": 5.2}
    bucket: Dict[str, List[str]] = {}
    for node in nodes:
        bucket.setdefault(node.get("layer", "unknown"), []).append(node["id"])
    for layer in sorted(bucket.keys(), key=lambda l: (LAYER_ORDER.index(l) if l in LAYER_ORDER else 999, l)):
        ids = sorted(bucket[layer])
        for i, nid in enumerate(ids):
            pos[nid] = (layer_x.get(layer, 7.0), -float(i))
    return pos


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Export validated R001/R002 graph JSON as PNG (matplotlib/networkx)")
    parser.add_argument("graph", type=Path, help="Path to graph JSON")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output PNG path")
    parser.add_argument("--sidecar", type=Path, help="Optional sidecar markdown path")
    parser.add_argument("--view", choices=VIEW_CHOICES, default="full")
    parser.add_argument("--label-mode", choices=LABEL_CHOICES, default="id")
    parser.add_argument("--max-label-chars", type=int, default=36)
    parser.add_argument("--figsize", nargs=2, type=float, metavar=("W", "H"), default=(14.0, 8.0))
    args = parser.parse_args(argv)

    try:
        import matplotlib.pyplot as plt
        import networkx as nx
    except Exception:
        print(MISSING_DEPS_MESSAGE, file=sys.stderr)
        return 1

    payload = json.loads(args.graph.read_text(encoding="utf-8"))
    errors = validate(payload)
    if errors:
        print("INVALID", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1

    sidecar = load_sidecar_map(args.sidecar)
    nodes, edges = filtered_payload(payload, args.view)

    g = nx.DiGraph()
    for node in sorted(nodes, key=lambda n: n.get("id", "")):
        nid = node["id"]
        g.add_node(nid, layer=node.get("layer", "unknown"), label=node_label(node, args.label_mode, sidecar, args.max_label_chars))
    for edge in sorted(edges, key=lambda e: e.get("id", "")):
        if edge.get("source") in g and edge.get("target") in g:
            g.add_edge(edge["source"], edge["target"], edge_type=edge.get("type", "unknown"))

    pos = build_positions(nodes, edges, args.view)
    for nid in g.nodes:
        pos.setdefault(nid, (0.0, 0.0))

    fig, ax = plt.subplots(figsize=tuple(args.figsize))
    ax.set_title(f"R001/R002 graph view: {args.view}")
    ax.axis("off")

    layer_style = {
        "L_raw": {"shape": "o", "color": "#d8e8ff"},
        "L_candidate": {"shape": "s", "color": "#fff0cc"},
        "L_accepted": {"shape": "D", "color": "#d5f5d5"},
        "L_gitlog": {"shape": "^", "color": "#f0d9ff"},
    }

    for layer in sorted({g.nodes[n].get("layer", "unknown") for n in g.nodes}, key=lambda l: (LAYER_ORDER.index(l) if l in LAYER_ORDER else 999, l)):
        nodelist = [n for n in g.nodes if g.nodes[n].get("layer") == layer]
        style = layer_style.get(layer, {"shape": "o", "color": "#efefef"})
        nx.draw_networkx_nodes(g, pos, nodelist=nodelist, node_shape=style["shape"], node_color=style["color"], edgecolors="#444", node_size=1700, ax=ax)

    labels = {n: g.nodes[n]["label"] for n in g.nodes}
    nx.draw_networkx_labels(g, pos, labels=labels, font_size=8, ax=ax)

    for edge_type in sorted({g.edges[e].get("edge_type", "unknown") for e in g.edges}):
        edgelist = [e for e in g.edges if g.edges[e].get("edge_type") == edge_type]
        st = EDGE_STYLE.get(edge_type, {"color": "#888", "style": "solid", "width": 1.0})
        nx.draw_networkx_edges(g, pos, edgelist=edgelist, edge_color=st["color"], style=st["style"], width=st["width"], arrows=True, arrowsize=12, ax=ax)

    from matplotlib.lines import Line2D

    layer_handles = [
        Line2D([0], [0], marker=layer_style[k]["shape"], color="w", label=k, markerfacecolor=layer_style[k]["color"], markeredgecolor="#444", markersize=8)
        for k in ["L_raw", "L_candidate", "L_accepted"]
        if any(g.nodes[n].get("layer") == k for n in g.nodes)
    ]
    edge_handles = [
        Line2D([0], [0], color=EDGE_STYLE.get(k, {"color": "#888"})["color"], linestyle=EDGE_STYLE.get(k, {"style": "solid"})["style"], label=k)
        for k in sorted({g.edges[e].get("edge_type", "unknown") for e in g.edges})
    ]
    if layer_handles or edge_handles:
        ax.legend(handles=layer_handles + edge_handles, loc="best", fontsize=8)

    fig.tight_layout()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=150)
    plt.close(fig)
    print(f"WROTE {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
