#!/usr/bin/env python3
"""Self-contained HMDG v0 runner.

This prototype extracts a weighted longest cognitive path from a small
hand-built Jordan normal form DAG. It is intentionally independent of mathlib
for v0; a later adapter can replace NODES/EDGES with formal graph input.
"""

from __future__ import annotations

from collections import defaultdict, deque
from pathlib import Path
import json

TARGET = "jordan_normal_form"

NODES = {
    "vector_space": "object",
    "linear_map": "operation",
    "composition_power": "operation",
    "kernel": "kernel",
    "image": "image",
    "quotient": "quotient",
    "invariant_subspace": "constraint",
    "eigenvalue": "invariant",
    "eigenvector": "object",
    "diagonalization": "decomposition",
    "failure_not_enough_eigenvectors": "failure",
    "shifted_operator_N_A_minus_lambda_I": "operation",
    "generalized_eigenvector": "repair",
    "generalized_eigenspace": "decomposition",
    "nilpotent_operator": "operation",
    "kernel_growth_sequence": "invariant",
    "dimension_difference": "invariant",
    "jordan_chain": "repair",
    "chain_basis": "decomposition",
    "jordan_block": "normal_form",
    "jordan_normal_form": "normal_form",
    "two_by_two_jordan_example": "example",
    "repeated_eigenvalue_but_diagonalizable": "example",
    "minimal_polynomial": "invariant",
    "direct_sum": "decomposition",
    "simp_api_noise": "technical",
    "typeclass_instance_noise": "technical",
}

GLOSS = {
    "vector_space": "stage where linear maps act",
    "linear_map": "operation preserving addition and scalar multiplication",
    "eigenvalue": "scalar behavior exposed on a direction",
    "eigenvector": "direction satisfying Av=lambda v",
    "diagonalization": "ideal decomposition by eigenvector basis",
    "failure_not_enough_eigenvectors": "diagonalization fails because eigenvectors do not span",
    "generalized_eigenvector": "repair by allowing (A-lambda I)^r v = 0",
    "generalized_eigenspace": "space recovered by generalized eigenvectors",
    "nilpotent_operator": "pure model of repeated action eventually becoming zero",
    "kernel_growth_sequence": "ker N, ker N^2, ker N^3, ...",
    "dimension_difference": "reads how many chains survive to each depth",
    "jordan_chain": "sequence flowing into an eigenvector",
    "chain_basis": "basis assembled from Jordan chains",
    "jordan_block": "matrix form of one chain",
    "jordan_normal_form": "direct sum of Jordan blocks",
}

EDGES = [
    ("vector_space", "linear_map", "requires"),
    ("linear_map", "composition_power", "constructs"),
    ("linear_map", "kernel", "measures"),
    ("linear_map", "image", "measures"),
    ("kernel", "quotient", "quotients_by"),
    ("linear_map", "invariant_subspace", "requires"),
    ("linear_map", "eigenvalue", "measures"),
    ("eigenvalue", "eigenvector", "defines"),
    ("eigenvector", "diagonalization", "decomposes_into"),
    ("diagonalization", "failure_not_enough_eigenvectors", "detects_failure"),
    ("eigenvalue", "shifted_operator_N_A_minus_lambda_I", "constructs"),
    ("failure_not_enough_eigenvectors", "generalized_eigenvector", "repairs"),
    ("shifted_operator_N_A_minus_lambda_I", "generalized_eigenvector", "defines"),
    ("generalized_eigenvector", "generalized_eigenspace", "constructs"),
    ("generalized_eigenspace", "nilpotent_operator", "transfers_to"),
    ("nilpotent_operator", "kernel_growth_sequence", "measures"),
    ("kernel_growth_sequence", "dimension_difference", "measures"),
    ("dimension_difference", "jordan_chain", "constructs"),
    ("jordan_chain", "chain_basis", "decomposes_into"),
    ("chain_basis", "jordan_block", "normalizes_to"),
    ("jordan_block", "jordan_normal_form", "normalizes_to"),
    ("jordan_block", "two_by_two_jordan_example", "constructs"),
    ("failure_not_enough_eigenvectors", "two_by_two_jordan_example", "constructs"),
    ("repeated_eigenvalue_but_diagonalizable", "diagonalization", "constructs"),
    ("kernel_growth_sequence", "minimal_polynomial", "measures"),
    ("minimal_polynomial", "jordan_normal_form", "measures"),
    ("direct_sum", "generalized_eigenspace", "decomposes_into"),
    ("simp_api_noise", "jordan_normal_form", "technical_support"),
    ("typeclass_instance_noise", "jordan_normal_form", "technical_support"),
]

NODE_WEIGHT = {
    "object": 2,
    "operation": 3,
    "constraint": 2,
    "failure": 6,
    "repair": 6,
    "kernel": 5,
    "image": 4,
    "quotient": 5,
    "invariant": 6,
    "decomposition": 5,
    "transfer": 3,
    "normal_form": 7,
    "example": 2,
    "technical": -6,
    "unknown": 1,
}

EDGE_WEIGHT = {
    "requires": 1,
    "defines": 3,
    "constructs": 4,
    "detects_failure": 6,
    "repairs": 6,
    "measures": 5,
    "quotients_by": 4,
    "decomposes_into": 5,
    "normalizes_to": 6,
    "transfers_to": 3,
    "compresses": 2,
    "expands": 4,
    "technical_support": -6,
    "unknown": 0,
}


def build_graph():
    out_edges = defaultdict(list)
    in_edges = defaultdict(list)
    for src, dst, typ in EDGES:
        out_edges[src].append((dst, typ))
        in_edges[dst].append((src, typ))
    return out_edges, in_edges


def topological_sort(out_edges, in_edges):
    indeg = {node: len(in_edges[node]) for node in NODES}
    queue = deque([node for node, degree in indeg.items() if degree == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for dst, _typ in out_edges[node]:
            indeg[dst] -= 1
            if indeg[dst] == 0:
                queue.append(dst)
    if len(order) != len(NODES):
        raise RuntimeError("Graph is not a DAG; move revisit edges to branches or condense SCCs.")
    return order


def weighted_longest_path(target):
    out_edges, in_edges = build_graph()
    order = topological_sort(out_edges, in_edges)
    neg_inf = -10**18
    dp = {node: neg_inf for node in NODES}
    pred = {node: None for node in NODES}
    for node in NODES:
        if not in_edges[node]:
            dp[node] = NODE_WEIGHT.get(NODES[node], 1)
    for src in order:
        if dp[src] == neg_inf:
            continue
        for dst, typ in out_edges[src]:
            score = dp[src] + EDGE_WEIGHT.get(typ, 0) + NODE_WEIGHT.get(NODES[dst], 1)
            if score > dp[dst]:
                dp[dst] = score
                pred[dst] = src
    path = []
    cur = target
    while cur is not None:
        path.append(cur)
        cur = pred[cur]
    path.reverse()
    return path, dp[target], out_edges, in_edges


def side_branches(path, out_edges, in_edges):
    main = set(path)
    branches = {}
    for node in path:
        items = []
        for src, _typ in in_edges[node]:
            if src not in main:
                items.append(src)
        for dst, _typ in out_edges[node]:
            if dst not in main:
                items.append(dst)
        if items:
            branches[node] = items[:3]
    return branches


def write_outputs(path, score, branches):
    out_dir = Path(__file__).resolve().parent / "outputs" / "sample_jordan"
    out_dir.mkdir(parents=True, exist_ok=True)

    main_lines = ["# Main cognitive path", ""]
    for index, node in enumerate(path, 1):
        main_lines += [
            f"## {index:03d}. {node}",
            "",
            f"- role: `{NODES[node]}`",
            f"- gloss: {GLOSS.get(node, '')}",
        ]
        if node in branches:
            main_lines.append("- side_branches:")
            for branch in branches[node]:
                main_lines.append(f"  - `{branch}` / role=`{NODES[branch]}`")
        main_lines.append("")
    (out_dir / "main_path.md").write_text("\n".join(main_lines), encoding="utf-8")

    edge_type = {(src, dst): typ for src, dst, typ in EDGES}
    typed = ["# Typed edge list on main path", ""]
    for src, dst in zip(path, path[1:]):
        typed.append(f"- `{src}` -- `{edge_type[(src, dst)]}` --> `{dst}`")
    (out_dir / "typed_edges.md").write_text("\n".join(typed), encoding="utf-8")

    audit = [
        "# Audit report",
        "",
        f"target: `{TARGET}`",
        f"total_nodes: {len(NODES)}",
        f"total_edges: {len(EDGES)}",
        f"main_path_length: {len(path)}",
        f"main_path_score: {score}",
        f"branch_points: {len(branches)}",
        "",
        "## Main path IDs",
        "",
    ]
    audit += [f"- {node}: role={NODES[node]}" for node in path]
    (out_dir / "audit_report.md").write_text("\n".join(audit), encoding="utf-8")

    graph = {"nodes": NODES, "edges": EDGES, "main_path": path, "score": score, "branches": branches}
    (out_dir / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")


def main():
    path, score, out_edges, in_edges = weighted_longest_path(TARGET)
    branches = side_branches(path, out_edges, in_edges)
    write_outputs(path, score, branches)
    print("Done.")
    print(f"target: {TARGET}")
    print(f"score: {score}")
    print(f"path length: {len(path)}")
    for index, node in enumerate(path, 1):
        print(f"{index:03d}. {node} [{NODES[node]}]")


if __name__ == "__main__":
    main()
