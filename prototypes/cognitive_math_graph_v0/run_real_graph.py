#!/usr/bin/env python3
"""Run HMDG weighted-longest-path extraction on a real dependency graph.

Supported inputs:
  - .gexf
  - .graphml
  - .csv edge list

The runner can auto-detect edge direction by comparing target ancestor counts
in the original graph and the reversed graph. This is important because some
formal dependency graphs use theorem -> dependency edges, while this extractor
needs prerequisite -> theorem edges for ancestor-based path extraction.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict, deque
from pathlib import Path

NODE_WEIGHT = {
    "definition": 5,
    "kernel_image": 6,
    "quotient": 6,
    "invariant": 6,
    "decomposition": 6,
    "normal_form": 7,
    "failure_repair": 6,
    "technical": -8,
    "unknown": 1,
}

TECHNICAL_PATTERNS = [
    "simp", "inst", "coe", "ofnat", "decidable", "classical", "subtype",
    "mk", "rec", "caseson", "noconfusion", "injeq", "congr", "rfl",
]

ROLE_PATTERNS = [
    ("kernel_image", ["ker", "kernel", "range", "image", "map", "comap"]),
    ("quotient", ["quot", "quotient", "quotientmap"]),
    ("invariant", ["dim", "rank", "finrank", "eigen", "spectrum", "minimalpolynomial"]),
    ("decomposition", ["directsum", "iscompl", "sup", "inf", "decomp", "span"]),
    ("normal_form", ["normal", "jordan", "block"]),
    ("failure_repair", ["nilpotent", "generalized", "chain"]),
    ("definition", ["def", "mk", "of", "to"]),
]


def norm_name(x) -> str:
    return str(x).strip()


def classify(name: str) -> str:
    low = name.lower()
    if any(pattern in low for pattern in TECHNICAL_PATTERNS):
        return "technical"
    for role, patterns in ROLE_PATTERNS:
        if any(pattern in low for pattern in patterns):
            return role
    return "unknown"


def weight(name: str) -> int:
    return NODE_WEIGHT.get(classify(name), NODE_WEIGHT["unknown"])


def read_csv_edges(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header")
        columns = set(reader.fieldnames)
        pairs = [
            ("source", "target"), ("src", "dst"), ("from", "to"),
            ("from_id", "to_id"), ("source_id", "target_id"),
        ]
        pair = next((p for p in pairs if p[0] in columns and p[1] in columns), None)
        if pair is None:
            raise ValueError(f"Could not find source/target columns in {reader.fieldnames}")
        src_col, dst_col = pair
        nodes, edges = set(), []
        for row in reader:
            src, dst = norm_name(row[src_col]), norm_name(row[dst_col])
            if src and dst:
                nodes.update([src, dst])
                edges.append((src, dst))
    return nodes, edges


def read_networkx_graph(path: Path):
    try:
        import networkx as nx
    except ImportError as exc:
        raise SystemExit("networkx is required for GEXF/GraphML input. Install with: pip install networkx") from exc
    suffix = path.suffix.lower()
    if suffix == ".gexf":
        graph = nx.read_gexf(path)
    elif suffix in {".graphml", ".xml"}:
        graph = nx.read_graphml(path)
    else:
        raise ValueError(f"Unsupported NetworkX graph extension: {path.suffix}")
    nodes = {norm_name(n) for n in graph.nodes}
    edges = [(norm_name(u), norm_name(v)) for u, v in graph.edges]
    return nodes, edges


def read_graph(path: Path):
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return read_csv_edges(path)
    if suffix in {".gexf", ".graphml", ".xml"}:
        return read_networkx_graph(path)
    raise ValueError(f"Unsupported input extension: {path.suffix}")


def reverse_edges(edges):
    return [(dst, src) for src, dst in edges]


def build_adjacency(nodes, edges):
    out_edges, in_edges = defaultdict(list), defaultdict(list)
    for src, dst in edges:
        out_edges[src].append(dst)
        in_edges[dst].append(src)
    for node in nodes:
        out_edges[node]
        in_edges[node]
    return out_edges, in_edges


def ancestors(target, in_edges):
    seen, stack = set(), [target]
    while stack:
        node = stack.pop()
        for parent in in_edges[node]:
            if parent not in seen:
                seen.add(parent)
                stack.append(parent)
    return seen


def choose_target(nodes, substrings, exact=None):
    if exact:
        if exact not in nodes:
            raise ValueError(f"Exact target not found: {exact}")
        return exact, [exact]
    if not substrings:
        raise ValueError("Provide --target-exact or at least one --target-substring")
    matches = [n for n in nodes if all(term.lower() in n.lower() for term in substrings)]
    matches.sort(key=lambda n: (classify(n) == "technical", len(n), n))
    if not matches:
        raise ValueError(f"No target matched substrings: {substrings}")
    return matches[0], matches[:50]


def pick_direction(nodes, edges, target, mode):
    if mode == "as-is":
        out_edges, in_edges = build_adjacency(nodes, edges)
        keep = ancestors(target, in_edges) | {target}
        return edges, "as-is", len(keep)
    if mode == "reverse":
        rev = reverse_edges(edges)
        out_edges, in_edges = build_adjacency(nodes, rev)
        keep = ancestors(target, in_edges) | {target}
        return rev, "reverse", len(keep)

    out_a, in_a = build_adjacency(nodes, edges)
    count_a = len(ancestors(target, in_a) | {target})
    rev = reverse_edges(edges)
    out_r, in_r = build_adjacency(nodes, rev)
    count_r = len(ancestors(target, in_r) | {target})
    if count_r > count_a:
        return rev, "reverse", count_r
    return edges, "as-is", count_a


def induced(nodes_keep, out_edges):
    edges = []
    for src in nodes_keep:
        for dst in out_edges[src]:
            if dst in nodes_keep:
                edges.append((src, dst))
    return set(nodes_keep), edges


def topological_sort(nodes, out_edges, in_edges):
    indeg = {node: len(in_edges[node]) for node in nodes}
    queue = deque([node for node, degree in indeg.items() if degree == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for dst in out_edges[node]:
            indeg[dst] -= 1
            if indeg[dst] == 0:
                queue.append(dst)
    if len(order) != len(nodes):
        raise ValueError("Graph is not a DAG")
    return order


def condense_if_needed(nodes, edges):
    try:
        topological_sort(nodes, *build_adjacency(nodes, edges))
        return nodes, edges, {node: [node] for node in nodes}, False
    except ValueError:
        pass
    try:
        import networkx as nx
    except ImportError as exc:
        raise SystemExit("Graph is cyclic and networkx is required for SCC condensation.") from exc
    graph = nx.DiGraph()
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)
    condensed = nx.condensation(graph)
    groups = defaultdict(list)
    for original, component in condensed.graph["mapping"].items():
        groups[str(component)].append(original)
    new_edges = [(str(u), str(v)) for u, v in condensed.edges]
    return set(groups.keys()), new_edges, dict(groups), True


def weighted_longest_path(nodes, out_edges, in_edges, target, component_members):
    order = topological_sort(nodes, out_edges, in_edges)
    neg_inf = -10**18
    dp, pred = {node: neg_inf for node in nodes}, {node: None for node in nodes}

    def node_score(node):
        return max(weight(member) for member in component_members.get(node, [node]))

    for node in nodes:
        if not in_edges[node]:
            dp[node] = node_score(node)
    for src in order:
        if dp[src] == neg_inf:
            continue
        for dst in out_edges[src]:
            score = dp[src] + node_score(dst)
            if score > dp[dst]:
                dp[dst], pred[dst] = score, src

    path, cur = [], target
    while cur is not None:
        path.append(cur)
        cur = pred[cur]
    path.reverse()
    return path, dp[target]


def render_output(out_dir, *, input_path, target, matches, path, score, total_nodes, total_edges, ancestor_count, edge_direction, condensed, component_members):
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Real graph HMDG extraction", "",
        f"input: `{input_path}`",
        f"target: `{target}`",
        f"edge_direction: `{edge_direction}`",
        f"ancestor_count: {ancestor_count}",
        f"candidate_matches_preview: {len(matches)} shown", "",
        "## Candidate matches", "",
    ]
    for item in matches:
        lines.append(f"- `{item}` / role={classify(item)} / weight={weight(item)}")
    lines += ["", "## Main weighted longest path", "", f"score: {score}", f"length: {len(path)}", ""]
    for index, node in enumerate(path, 1):
        members = component_members.get(node, [node])
        display = members[0] if len(members) == 1 else f"SCC({len(members)}): " + ", ".join(members[:3])
        lines.append(f"{index:03d}. `{display}` / role={classify(display)}")
    if len(path) <= 1:
        lines += ["", "## Warning", "", "Path length is 1. Try `--edge-direction reverse` or a less primitive target."]
    (out_dir / "real_main_path.md").write_text("\n".join(lines), encoding="utf-8")

    data = {
        "input": str(input_path),
        "target": target,
        "score": score,
        "path": path,
        "total_nodes": total_nodes,
        "total_edges": total_edges,
        "ancestor_count": ancestor_count,
        "edge_direction": edge_direction,
        "condensed": condensed,
        "candidate_matches": matches,
        "component_members": component_members,
    }
    (out_dir / "real_graph_result.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to GEXF, GraphML, or CSV edge list")
    parser.add_argument("--target-substring", action="append", help="Substring target name must contain; repeatable")
    parser.add_argument("--target-exact", help="Exact target declaration name")
    parser.add_argument("--edge-direction", choices=["auto", "as-is", "reverse"], default="auto")
    parser.add_argument("--list-targets-only", action="store_true")
    parser.add_argument("--out-dir", default="prototypes/cognitive_math_graph_v0/outputs/real_graph")
    args = parser.parse_args()

    input_path = Path(args.input)
    nodes, raw_edges = read_graph(input_path)
    target, matches = choose_target(nodes, args.target_substring or [], args.target_exact)
    if args.list_targets_only:
        for item in matches:
            print(item)
        return

    edges, edge_direction, ancestor_count = pick_direction(nodes, raw_edges, target, args.edge_direction)
    out_edges, in_edges = build_adjacency(nodes, edges)
    keep = ancestors(target, in_edges) | {target}
    sub_nodes, sub_edges = induced(keep, out_edges)
    dag_nodes, dag_edges, component_members, condensed = condense_if_needed(sub_nodes, sub_edges)
    dag_out, dag_in = build_adjacency(dag_nodes, dag_edges)
    target_component = target if not condensed else next(comp for comp, members in component_members.items() if target in members)
    path, score = weighted_longest_path(dag_nodes, dag_out, dag_in, target_component, component_members)

    render_output(
        Path(args.out_dir),
        input_path=input_path,
        target=target,
        matches=matches,
        path=path,
        score=score,
        total_nodes=len(nodes),
        total_edges=len(raw_edges),
        ancestor_count=ancestor_count,
        edge_direction=edge_direction,
        condensed=condensed,
        component_members=component_members,
    )

    print("Done.")
    print(f"input nodes: {len(nodes)}")
    print(f"input edges: {len(raw_edges)}")
    print(f"target: {target}")
    print(f"edge direction: {edge_direction}")
    print(f"ancestor nodes: {ancestor_count}")
    print(f"condensed: {condensed}")
    print(f"path length: {len(path)}")
    print(f"score: {score}")
    print(f"output: {args.out_dir}")


if __name__ == "__main__":
    main()
