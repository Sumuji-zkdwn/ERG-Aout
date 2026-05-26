#!/usr/bin/env python3
"""Create a human-readable cognitive report from HMDG real graph output.

This is a lightweight post-processor over real_graph_result.json.
It does not prove the target theorem. It turns the extracted formal path into
an interpretable skeleton: phases, node cards, and phase-to-phase edges.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
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

ROLE_GLOSS = {
    "kernel": "focuses on where a linear map sends inputs to zero",
    "image": "focuses on reachable outputs or ranges",
    "quotient": "passes to a quotient or quotient-like representation",
    "criterion": "turns a property into a checkable iff/equivalence condition",
    "constraint": "uses side conditions such as disjointness, independence, or commutation",
    "transfer": "moves structure through restriction, codomain restriction, map, or comap",
    "lattice_operation": "uses order/lattice operations such as sup, inf, top, or bot",
    "eigenspace": "moves inside generalized eigenspace structure",
    "invariant": "uses a preserved numerical or structural invariant",
    "decomposition": "breaks an object into spans, sums, complements, or components",
    "normal_form": "moves toward a canonical or normal-form representation",
    "failure_repair": "repairs failure of a simple condition using generalized structure",
    "technical": "likely proof-engine or infrastructure residue",
    "unknown": "not classified by current heuristics",
}

TOKEN_GLOSS = {
    "ker": "kernel / zero-preimage",
    "restrict": "restriction",
    "codrestrict": "codomain restriction",
    "domrestrict": "domain restriction",
    "injective": "injectivity",
    "disjoint": "disjointness",
    "comap": "pullback-like transfer",
    "sup": "join/supremum",
    "inf": "meet/infimum",
    "commute": "commutation condition",
    "noncommprod": "noncommutative product",
    "supindep": "sup-independence",
    "geneigenspace": "generalized eigenspace",
    "isup": "indexed supremum",
    "eq": "equality statement",
    "bot": "bottom subobject / zero-like object",
    "top": "top subobject / whole object",
    "iff": "if and only if criterion",
}


def split_decl_name(name: str) -> list[str]:
    tail = name.split(".")[-1]
    parts = re.split(r"[_']+", tail)
    return [p for p in parts if p]


def token_glosses(name: str) -> list[str]:
    parts = split_decl_name(name)
    out = []
    for part in parts:
        key = part.lower()
        if key in TOKEN_GLOSS:
            out.append(f"{part}: {TOKEN_GLOSS[key]}")
    return out


def primary_role(tags: list[str]) -> str:
    return tags[0] if tags else "unknown"


def phase_for_role(role: str) -> str:
    return ROLE_PHASE.get(role, "unknown step")


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


def phase_gloss(chunk):
    roles = Counter(item["role"] for item in chunk["items"])
    tag_counts = Counter(tag for item in chunk["items"] for tag in item["tags"])
    dominant_role = roles.most_common(1)[0][0]
    dominant_tags = ", ".join(tag for tag, _count in tag_counts.most_common(4))
    return f"This phase {ROLE_GLOSS.get(dominant_role, ROLE_GLOSS['unknown'])}. Dominant tags: {dominant_tags}."


def render_report(data, chunks):
    lines = [
        "# HMDG cognitive reading report",
        "",
        "## Status",
        "",
        "This is not a proof explanation. It is a cognitive skeleton extracted from a formal dependency path.",
        "Use it to decide what should be expanded next, not as a final mathematical exposition.",
        "",
        "## Target",
        "",
        f"target: `{data.get('target', '')}`",
        f"edge_direction: `{data.get('edge_direction', '')}`",
        f"ancestor_count: {data.get('ancestor_count', '')}",
        f"path_length: {len(data.get('path_display', []))}",
        f"score: {data.get('score', '')}",
        "",
        "## Cognitive spine",
        "",
    ]

    spine = " -> ".join(chunk["phase"] for chunk in chunks)
    lines.append(spine)

    lines += ["", "## Phase interpretation", ""]
    for i, chunk in enumerate(chunks, start=1):
        lines.append(f"### {i:02d}. {chunk['phase']}")
        lines.append("")
        lines.append(phase_gloss(chunk))
        lines.append("")
        first = chunk["items"][0]["node"]
        last = chunk["items"][-1]["node"]
        if first == last:
            lines.append(f"Formal anchor: `{first}`")
        else:
            lines.append(f"Formal anchors: `{first}` -> `{last}`")
        lines.append("")

    lines += ["## Node cards", ""]
    for chunk in chunks:
        lines.append(f"### {chunk['phase']}")
        lines.append("")
        for item in chunk["items"]:
            node = item["node"]
            tags = ",".join(item["tags"])
            lines.append(f"#### {item['index']:03d}. `{node}`")
            lines.append("")
            lines.append(f"primary_role: {item['role']}")
            lines.append(f"tags: {tags}")
            glosses = token_glosses(node)
            if glosses:
                lines.append("token hints:")
                for gloss in glosses:
                    lines.append(f"- {gloss}")
            else:
                lines.append("token hints: none from current heuristic dictionary")
            lines.append("")

    lines += ["## Phase DAG", ""]
    for i in range(len(chunks) - 1):
        src = chunks[i]["phase"]
        dst = chunks[i + 1]["phase"]
        lines.append(f"- `{src}` -> `{dst}`")

    lines += [
        "",
        "## Next expansion target",
        "",
        "The best next expansion target is usually the first phase boundary that is not cognitively obvious.",
        "For this path, inspect the bridge from `kernel setup` to `criterion bridge`, then from `constraint bridge` to `eigenspace conclusion`.",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        default="prototypes/cognitive_math_graph_v0/outputs/real_graph/real_graph_result.json",
        help="Path to real_graph_result.json",
    )
    parser.add_argument(
        "--output",
        default="prototypes/cognitive_math_graph_v0/outputs/real_graph/cognitive_report.md",
        help="Output markdown path",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    data = json.loads(input_path.read_text(encoding="utf-8"))

    path_display = data.get("path_display") or data.get("path") or []
    path_role_tags = data.get("path_role_tags") or {node: ["unknown"] for node in path_display}

    chunks = chunk_path(path_display, path_role_tags)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_report(data, chunks), encoding="utf-8")

    print(f"Wrote: {output_path}")
    print("cognitive spine:")
    print(" -> ".join(chunk["phase"] for chunk in chunks))


if __name__ == "__main__":
    main()
