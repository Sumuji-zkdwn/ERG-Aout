#!/usr/bin/env python3
"""Create a chunk/phase report from HMDG real graph output.

Input:
  prototypes/cognitive_math_graph_v0/outputs/real_graph/real_graph_result.json

Output:
  prototypes/cognitive_math_graph_v0/outputs/real_graph/chunk_report.md

This is a post-processor. It does not change the extracted path. It groups
consecutive nodes by coarse cognitive role so the path can be read as phases
rather than as a flat theorem list.
"""

from __future__ import annotations

import argparse
import json
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


def phase_for_role(role: str) -> str:
    return ROLE_PHASE.get(role, "unknown step")


def chunk_path(path_display, path_roles, path_role_tags):
    chunks = []
    current = None
    for index, (node, role) in enumerate(zip(path_display, path_roles), start=1):
        phase = phase_for_role(role)
        entry = {
            "index": index,
            "node": node,
            "role": role,
            "tags": path_role_tags.get(node, [role]),
        }
        if current is None or current["phase"] != phase:
            current = {"phase": phase, "items": []}
            chunks.append(current)
        current["items"].append(entry)
    return chunks


def render_report(data, chunks):
    lines = [
        "# HMDG path chunk report",
        "",
        f"target: `{data.get('target', '')}`",
        f"edge_direction: `{data.get('edge_direction', '')}`",
        f"ancestor_count: {data.get('ancestor_count', '')}",
        f"path_length: {len(data.get('path_display', []))}",
        f"score: {data.get('score', '')}",
        "",
        "## Phase summary",
        "",
    ]

    for i, chunk in enumerate(chunks, start=1):
        roles = Counter(item["role"] for item in chunk["items"])
        role_text = ", ".join(f"{role}:{count}" for role, count in roles.items())
        lines.append(f"{i:02d}. {chunk['phase']} ({len(chunk['items'])} nodes; {role_text})")

    lines += ["", "## Chunks", ""]
    for i, chunk in enumerate(chunks, start=1):
        lines.append(f"### {i:02d}. {chunk['phase']}")
        lines.append("")
        for item in chunk["items"]:
            tags = ",".join(item["tags"])
            lines.append(f"- {item['index']:03d}. `{item['node']}` / role={item['role']} / tags={tags}")
        lines.append("")

    lines += [
        "## Reading note",
        "",
        "This report is structural, not a proof explanation. It identifies contiguous role phases in the extracted path.",
        "If a phase boundary looks wrong, adjust role tagging before changing the graph extraction algorithm.",
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
        default="prototypes/cognitive_math_graph_v0/outputs/real_graph/chunk_report.md",
        help="Output markdown path",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    data = json.loads(input_path.read_text(encoding="utf-8"))

    path_display = data.get("path_display") or data.get("path") or []
    path_roles = data.get("path_roles") or ["unknown"] * len(path_display)
    path_role_tags = data.get("path_role_tags") or {}

    chunks = chunk_path(path_display, path_roles, path_role_tags)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_report(data, chunks), encoding="utf-8")

    print(f"Wrote: {output_path}")
    print(f"chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks, start=1):
        print(f"{i:02d}. {chunk['phase']} ({len(chunk['items'])} nodes)")


if __name__ == "__main__":
    main()
