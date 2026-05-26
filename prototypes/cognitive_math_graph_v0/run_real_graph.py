#!/usr/bin/env python3
"""Run HMDG weighted-longest-path extraction on a real dependency graph.

Supported inputs:
  - .gexf
  - .graphml
  - .csv edge list

This is intentionally lightweight. It does not download data by itself.
Place external graph files under:
  prototypes/cognitive_math_graph_v0/data/external/

Example:
  python prototypes/cognitive_math_graph_v0/run_real_graph.py \
    --input prototypes/cognitive_math_graph_v0/data/external/mathlib4_dependency_graph.gexf \
    --target-substring LinearMap \
    --target-substring ker
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
    "mk", "rec", "caseson", "noConfusion", "injEq", "congr", "rfl",
]

ROLE_PATTERNS = [
    ("kernel_image", ["ker", "kernel", "range", "image", "map", "comap"]),
    ("quotient", ["quot", "quotient", "quotientmap"]),
    ("invariant", ["dim", "rank", "finrank", "eigen", "spectrum", "minimalPolynomial"]),
    ("decomposition", ["directsum", "iscompl", "sup", "inf", "decomp", "span"]),
    ("normal_form", ["normal", "jordan", "block"]),
    ("failure_repair", ["nilpotent", "generalized", "chain"]),
    ("definition", ["def", "mk", "of", "to"]),
]


def norm_name(x) -> str:
    return str(x).strip()


def classify(name: str) -> str:
    low = name.lower()
    if any(pattern.lower() in low for pattern in TECHNICAL_PATTERNS):
        return "technical"
    for role, patterns in ROLE_PATTERNS:
        if any(pattern.lower() in low for pattern in patterns):
            return role
    return "unknown"


def weight(name: str) -> int:
    return NODE_WEIGHT.get(classify(name), 1)


def read_csv_edges(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV has no header")
        columns = set(reader.fieldnames)
        candidates = [
            ("source", "target"),
            ("src", "dst"),
            ("from", "to"),
            ("from_id", "to_id"),
            ("source_id", "target_id"),
        ]
        pair = next((p for p in candidates if p[0] in columns and p[1] in columns), None)
        if pair is None:
            raise ValueError(f"Could not find source/target columns in {reader.fieldnames}")
        src_col, dst_col = pair
        edges = []
        nodes = set()
        for row in reader:
            src = norm_name(row[src_col])
            dst = norm_name(row[dst_col])
            if not src or not dst:
                continue
            edges.append((src, dst))
            nodes.add(src)
            nodes.add(dst)
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


def build_adjacency(nodes, edges):
    out_edges = defaultdict(list)
    in_edges = defaultdict(list)
    for src, dst in edges:
        out_edges[src].append(dst)
        in_edges[dst].append(src)
    for node in nodes:
        out_edges[node]
        in_edges[node]
    return out_edges, in_edges


def ancestors(target, in_edges):
    seen = set()
    stack = [target]
    while stack:
        node = stack.pop()
        for parent in in_edges[node]:
            if parent not in seen:
                seen.add(parent)
                stack.append(parent)
    return seen


def induced(nodes_keep, out_edges):
    edges = []
    for src in nodes_keep:
        for dst in out_edges[src]:
            if dst in nodes_keep:
                edges.append((src, dst))
    return build_adjacency(nodes_keep, edges), edges


def try_condense_if_needed(nodes, edges):
    try:
        order = topological_sort(nodes, *build_adjacency(nodes, edges))
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
    mapping = condensed.graph["mapping"]
    groups = defaultdict(list)
    for original, component in mapping.items():
        groups[str(component)].append(original)
    new_nodes = set(groups.keys())
    new_edges = [(str(u), str(v)) for u, v in condensed.edges]
    return new_nodes, new_edges, groups, True


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


def weighted_longest_path(nodes, out_edges, in_edges, target, component_members=None):
    order = topological_sort(nodes, out_edges, in_edges)
    neg_inf = -10**18
    dp = {node: neg_inf for node in nodes}
    pred = {node: None for node in nodes}

    def node_score(node):
        members = component_members.get(node, [node]) if component_members else [node]
        # Use max member weight so one meaningful declaration can carry the component.
        return max(weight(member) for member in members)

    for node in nodes:
        if not in_edges[node]:
            dp[node] = node_score(node)
    for src in order:
        if dp[src] == neg_inf:
            continue
        for dst in out_edges[src]:
            score = dp[src] + node_score(dst)
            if score > dp[dst]:
                dp[dst] = score
                pred[dst] = src

    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = pred[cur]
    path.reverse()
    return path, dp[target]


def choose_target(nodes, substrings):
    if not substrings:
        raise ValueError("Provide at least one --target-substring")
    matches = []
    for node in nodes:
        low = node.lower()
        if all(term.lower() in low for term in substrings):
            matches.append(node)
    matches.sort(key=lambda n: (classify(n) == "technical", len(n), n))
    if not matches:
        raise ValueError(f"No target matched substrings: {substrings}")
    return matches[0], matches[:25]


def render_output(out_dir, input_path, target, matches, path, score, total_nodes, total_edges, ancestor_count, condensed, component_members=None):
    out_dir.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Real graph HMDG extraction",
        "",
        f"input: `{input_path}`",
        f"target: `{target}`",
        f"candidate_matches_preview: {len(matches)} shown",
        "",
        "## Candidate matches",
        "",
    ]
    for item in matches:
        lines.append(f"- `{item}` / role={classify(item)} / weight={weight(item)}")
    lines += [
        "",
        "## Main weighted longest path",
        "",
        f"score: {score}",
        f"length: {len(path)}",
        "",
    ]
    for index, node in enumerate(path, 1):
        members = component_members.get(node, [node]) if component_members else [node]
        display = members[0] if len(members) == 1 else f"SCC({len(members)}): " + ", ".join(members[:3])
        lines.append(f"{index:03d}. `{display}` / role={classify(display)}")
    (out_dir / "real_main_path.md").write_text("\n".join(lines), encoding="utf-8")

    data = {
        "input": str(input_path),
        "target": target,
        "score": score,
        "path": path,
        "total_nodes": total_nodes,
        "total_edges": total_edges,
        "ancestor_count": ancestor_count,
        "condensed": condensed,
        "candidate_matches": matches,
        "component_members": component_members,
    }
    (out_dir / "real_graph_result.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to GEXF, GraphML, or CSV edge list")
    parser.add_argument("--target-substring", action="append", required=True, help="Substring that target declaration name must contain; repeatable")
    parser.add_argument("--out-dir", default="prototypes/cognitive_math_graph_v0/outputs/real_graph")
    args = parser.parse_args()

    input_path = Path(args.input)
    nodes, edges = read_graph(input_path)
    out_edges, in_edges = build_adjacency(nodes, edges)
    target, matches = choose_target(nodes, args.target_substring)

    keep = ancestors(target, in_edges) | {target}
    (sub_out, sub_in), sub_edges = induced(keep, out_edges)
    sub_nodes = set(keep)
    dag_nodes, dag_edges, component_members, condensed = try_condense_if_needed(sub_nodes, sub_edges)
    dag_out, dag_in = build_adjacency(dag_nodes, dag_edges)

    if condensed:
        # Find the condensed component containing the original target.
        target_component = next(comp for comp, members in component_members.items() if target in members)
    else:
        target_component = target

    path, score = weighted_longest_path(dag_nodes, dag_out, dag_in, target_component, component_members)
    render_output(
        Path(args.out_dir),
        input_path,
        target,
        matches,
        path,
        score,
        len(nodes),
        len(edges),
        len(keep),
        condensed,
        component_members,
    )

    print("Done.")
    print(f"input nodes: {len(nodes)}")
    print(f"input edges: {len(edges)}")
    print(f"target: {target}")
    print(f"ancestor nodes: {len(keep)}")
    print(f"condensed: {condensed}")
    print(f"path length: {len(path)}")
    print(f"score: {score}")
    print(f"output: {args.out_dir}")


if __name__ == "__main__":
    main()
