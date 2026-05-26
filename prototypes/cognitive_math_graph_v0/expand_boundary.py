#!/usr/bin/env python3
"""Generate boundary-specific expansion tasks from an HMDG real path.

This post-processor reads real_graph_result.json and turns phase boundaries
into explicit expansion tasks. It is meant to answer: if this path is still too
compressed, exactly which edge should be expanded next and what should be
explained there?
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROLE_PHASE = {
    "kernel": "kernel setup",
    "image": "image/range setup",
    "quotient": "quotient step",
    "criterion": "criterion bridge",
    "constraint": "constraint bridge",
    "transfer": "transfer/restriction step",
    "lattice_operation": "lattice operation step",
    "eigenspace": "eigenspace conclusion",
    "invariant": "invariant step",
    "decomposition": "decomposition step",
    "normal_form": "normal-form step",
    "failure_repair": "failure/repair step",
    "technical": "technical residue",
    "unknown": "unknown step",
}

ROLE_QUESTION = {
    ("kernel", "criterion"): "Why does the kernel statement become an injectivity/disjointness criterion?",
    ("criterion", "constraint"): "How is the criterion converted into structural side conditions such as disjointness, kernel equality, or lattice conditions?",
    ("constraint", "eigenspace"): "How do the kernel/disjointness constraints become a statement about generalized eigenspace decomposition?",
    ("kernel", "constraint"): "Which kernel fact is being strengthened into a side-condition statement?",
    ("transfer", "kernel"): "How does restriction or transfer preserve the kernel statement?",
}

TOKEN_HINTS = {
    "ker": "track the zero-preimage condition",
    "restrict": "check what changes under restriction",
    "codrestrict": "check what changes under codomain restriction",
    "domrestrict": "check what changes under domain restriction",
    "injective": "translate kernel-zero into injectivity",
    "iff": "split the equivalence into both directions",
    "disjoint": "identify which subobjects must intersect trivially",
    "comap": "follow the pullback/comap operation",
    "sup": "track join/supremum operations",
    "inf": "track meet/infimum operations",
    "commute": "check why commutation is needed",
    "noncommprod": "track product of endomorphisms without assuming commutativity",
    "supindep": "track independence of a family of subobjects",
    "geneigenspace": "connect constraints to generalized eigenspaces",
    "isup": "track indexed supremum over components",
    "eq": "identify the equality to prove",
    "bot": "interpret bottom as zero/trivial subobject",
    "top": "interpret top as whole space/module",
}


def split_decl_name(name: str) -> list[str]:
    tail = name.split(".")[-1]
    return [p for p in re.split(r"[_']+", tail) if p]


def phase_for_role(role: str) -> str:
    return ROLE_PHASE.get(role, "unknown step")


def primary_role(tags: list[str]) -> str:
    return tags[0] if tags else "unknown"


def chunk_path(path_display, path_role_tags):
    chunks = []
    current = None
    for index, node in enumerate(path_display, start=1):
        tags = path_role_tags.get(node, ["unknown"])
        role = primary_role(tags)
        phase = phase_for_role(role)
        item = {"index": index, "node": node, "role": role, "tags": tags}
        if current is None or current["phase"] != phase:
            current = {"phase": phase, "items": []}
            chunks.append(current)
        current["items"].append(item)
    return chunks


def boundaries(chunks):
    out = []
    for i in range(len(chunks) - 1):
        left = chunks[i]
        right = chunks[i + 1]
        src = left["items"][-1]
        dst = right["items"][0]
        left_tags = set(src["tags"])
        right_tags = set(dst["tags"])
        lost = sorted(left_tags - right_tags)
        gained = sorted(right_tags - left_tags)
        shared = sorted(left_tags & right_tags)
        score = 2 * len(lost) + 2 * len(gained) + (1 if src["role"] != dst["role"] else 0)
        out.append({
            "boundary_index": i + 1,
            "score": score,
            "from_phase": left["phase"],
            "to_phase": right["phase"],
            "from_node": src["node"],
            "to_node": dst["node"],
            "from_role": src["role"],
            "to_role": dst["role"],
            "from_tags": src["tags"],
            "to_tags": dst["tags"],
            "lost_tags": lost,
            "gained_tags": gained,
            "shared_tags": shared,
        })
    return out


def token_tasks(src: str, dst: str) -> list[str]:
    tokens = []
    seen = set()
    for token in split_decl_name(src) + split_decl_name(dst):
        key = token.lower()
        if key in TOKEN_HINTS and key not in seen:
            tokens.append(f"{token}: {TOKEN_HINTS[key]}")
            seen.add(key)
    return tokens


def guiding_question(boundary) -> str:
    pair = (boundary["from_role"], boundary["to_role"])
    if pair in ROLE_QUESTION:
        return ROLE_QUESTION[pair]
    return f"What operation turns `{boundary['from_node']}` into `{boundary['to_node']}`?"


def render_boundary_task(boundary):
    lost = ",".join(boundary["lost_tags"]) or "none"
    gained = ",".join(boundary["gained_tags"]) or "none"
    shared = ",".join(boundary["shared_tags"]) or "none"
    lines = [
        f"### Boundary {boundary['boundary_index']}",
        "",
        f"score: {boundary['score']}",
        f"phase_edge: `{boundary['from_phase']}` -> `{boundary['to_phase']}`",
        f"node_edge: `{boundary['from_node']}` -> `{boundary['to_node']}`",
        f"role_shift: {boundary['from_role']} -> {boundary['to_role']}",
        f"shared_tags: {shared}",
        f"lost_tags: {lost}",
        f"gained_tags: {gained}",
        "",
        "#### Expansion question",
        "",
        guiding_question(boundary),
        "",
        "#### Expansion tasks",
        "",
        "1. State the exact source theorem/declaration in plain language.",
        "2. State the exact target theorem/declaration in plain language.",
        "3. Identify the operation that crosses the boundary.",
        "4. Expand each token hint below into one sentence.",
        "5. Decide whether an intermediate concept node is missing between the two declarations.",
        "",
        "#### Token tasks",
        "",
    ]
    tasks = token_tasks(boundary["from_node"], boundary["to_node"])
    if tasks:
        for task in tasks:
            lines.append(f"- {task}")
    else:
        lines.append("- No token tasks detected by current heuristics.")
    lines += [
        "",
        "#### Candidate missing concept node",
        "",
        f"`{boundary['from_role']}_to_{boundary['to_role']}`",
        "",
    ]
    return lines


def render_report(data, selected):
    path_display = data.get("path_display") or data.get("path") or []
    path_role_tags = data.get("path_role_tags") or {node: ["unknown"] for node in path_display}
    chunks = chunk_path(path_display, path_role_tags)
    bnds = boundaries(chunks)
    if selected is not None:
        bnds = [b for b in bnds if b["boundary_index"] == selected]

    lines = [
        "# HMDG boundary expansion tasks",
        "",
        f"target: `{data.get('target', '')}`",
        f"path_length: {len(path_display)}",
        f"boundary_count: {len(boundaries(chunks))}",
        "",
    ]
    if not bnds:
        lines.append("No matching boundary found.")
        return "\n".join(lines)
    for b in bnds:
        lines.extend(render_boundary_task(b))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="prototypes/cognitive_math_graph_v0/outputs/real_graph/real_graph_result.json")
    parser.add_argument("--output", default="prototypes/cognitive_math_graph_v0/outputs/real_graph/boundary_expansion.md")
    parser.add_argument("--boundary", type=int, help="Expand one boundary only, e.g. --boundary 3")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    report = render_report(data, args.boundary)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Wrote: {output_path}")


if __name__ == "__main__":
    main()
