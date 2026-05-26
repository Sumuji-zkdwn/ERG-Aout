#!/usr/bin/env python3
"""Materialize HMDG boundary expansion tasks as concept-node patches.

This post-processor reads real_graph_result.json and proposes explicit HMDG
concept nodes between adjacent phase chunks. It turns a compressed formal edge

  declaration A -> declaration B

into a candidate cognitive bridge

  declaration A -> concept bridge -> declaration B

The output is a patch proposal, not an accepted mathematical formalization.
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


def primary_role(tags: list[str]) -> str:
    return tags[0] if tags else "unknown"


def phase_for_role(role: str) -> str:
    return ROLE_PHASE.get(role, "unknown step")


def concept_id(from_role: str, to_role: str, index: int) -> str:
    return f"C{index:03d}_{from_role}_to_{to_role}"


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


def token_tasks(src: str, dst: str) -> list[dict]:
    tasks = []
    seen = set()
    for token in split_decl_name(src) + split_decl_name(dst):
        key = token.lower()
        if key in TOKEN_HINTS and key not in seen:
            tasks.append({"token": token, "task": TOKEN_HINTS[key]})
            seen.add(key)
    return tasks


def guiding_question(from_role: str, to_role: str, src: str, dst: str) -> str:
    pair = (from_role, to_role)
    if pair in ROLE_QUESTION:
        return ROLE_QUESTION[pair]
    return f"What operation turns `{src}` into `{dst}`?"


def build_patch(data):
    path_display = data.get("path_display") or data.get("path") or []
    path_role_tags = data.get("path_role_tags") or {node: ["unknown"] for node in path_display}
    chunks = chunk_path(path_display, path_role_tags)

    nodes = []
    edges = []
    boundaries = []

    # Keep declaration nodes explicitly so the patch can be imported elsewhere.
    for index, decl in enumerate(path_display, start=1):
        tags = path_role_tags.get(decl, ["unknown"])
        nodes.append({
            "id": f"D{index:03d}",
            "type": "Declaration",
            "label": decl,
            "role": primary_role(tags),
            "tags": tags,
            "path_index": index,
        })

    decl_id_by_label = {node["label"]: node["id"] for node in nodes if node["type"] == "Declaration"}

    # Preserve the full extracted declaration path. Boundary bridge edges are
    # additional proposed expansions, not replacements for the original path.
    for index in range(len(path_display) - 1):
        src_label = path_display[index]
        dst_label = path_display[index + 1]
        edges.append({
            "source": decl_id_by_label[src_label],
            "target": decl_id_by_label[dst_label],
            "type": "main_path_edge",
            "label": "adjacent declarations in the extracted weighted longest path",
            "path_index": index + 1,
        })

    for i in range(len(chunks) - 1):
        left = chunks[i]
        right = chunks[i + 1]
        src = left["items"][-1]
        dst = right["items"][0]
        from_tags = set(src["tags"])
        to_tags = set(dst["tags"])
        lost = sorted(from_tags - to_tags)
        gained = sorted(to_tags - from_tags)
        shared = sorted(from_tags & to_tags)
        score = 2 * len(lost) + 2 * len(gained) + (1 if src["role"] != dst["role"] else 0)
        cid = concept_id(src["role"], dst["role"], i + 1)
        concept = {
            "id": cid,
            "type": "ConceptBridge",
            "label": f"{src['role']}_to_{dst['role']}",
            "from_phase": left["phase"],
            "to_phase": right["phase"],
            "from_role": src["role"],
            "to_role": dst["role"],
            "question": guiding_question(src["role"], dst["role"], src["node"], dst["node"]),
            "token_tasks": token_tasks(src["node"], dst["node"]),
            "score": score,
            "lost_tags": lost,
            "gained_tags": gained,
            "shared_tags": shared,
            "status": "candidate",
        }
        nodes.append(concept)
        edges.append({
            "source": decl_id_by_label[src["node"]],
            "target": cid,
            "type": "needs_bridge",
            "label": "compressed formal edge enters candidate concept bridge",
        })
        edges.append({
            "source": cid,
            "target": decl_id_by_label[dst["node"]],
            "type": "bridges_to",
            "label": "candidate concept bridge exits to next declaration",
        })
        edges.append({
            "source": decl_id_by_label[src["node"]],
            "target": decl_id_by_label[dst["node"]],
            "type": "original_boundary_edge",
            "label": "original adjacent phase boundary before expansion",
        })
        boundaries.append({
            "boundary_index": i + 1,
            "concept_id": cid,
            "from_node": src["node"],
            "to_node": dst["node"],
            "score": score,
        })

    return {
        "source": "real_graph_result.json",
        "target": data.get("target"),
        "path_length": len(path_display),
        "nodes": nodes,
        "edges": edges,
        "boundaries": boundaries,
    }


def render_markdown(patch):
    lines = [
        "# HMDG concept patch proposal",
        "",
        f"target: `{patch.get('target', '')}`",
        f"path_length: {patch.get('path_length', '')}",
        f"node_count: {len(patch['nodes'])}",
        f"edge_count: {len(patch['edges'])}",
        "",
        "## Concept bridge nodes",
        "",
    ]
    for node in patch["nodes"]:
        if node["type"] != "ConceptBridge":
            continue
        lines.append(f"### {node['id']} `{node['label']}`")
        lines.append("")
        lines.append(f"status: {node['status']}")
        lines.append(f"phase_edge: `{node['from_phase']}` -> `{node['to_phase']}`")
        lines.append(f"role_shift: {node['from_role']} -> {node['to_role']}")
        lines.append(f"score: {node['score']}")
        lines.append(f"question: {node['question']}")
        lines.append(f"shared_tags: {','.join(node['shared_tags']) or 'none'}")
        lines.append(f"lost_tags: {','.join(node['lost_tags']) or 'none'}")
        lines.append(f"gained_tags: {','.join(node['gained_tags']) or 'none'}")
        lines.append("")
        lines.append("token_tasks:")
        if node["token_tasks"]:
            for task in node["token_tasks"]:
                lines.append(f"- {task['token']}: {task['task']}")
        else:
            lines.append("- none")
        lines.append("")

    lines += ["## Typed edge list", ""]
    label_by_id = {node["id"]: node["label"] for node in patch["nodes"]}
    for edge in patch["edges"]:
        src = f"{edge['source']}:{label_by_id.get(edge['source'], '')}"
        dst = f"{edge['target']}:{label_by_id.get(edge['target'], '')}"
        lines.append(f"- `{src}` -[{edge['type']}]-> `{dst}`")

    lines += [
        "",
        "## Import note",
        "",
        "This patch is intentionally marked as candidate. Accepting a concept bridge requires mathematical review or another expansion pass.",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="prototypes/cognitive_math_graph_v0/outputs/real_graph/real_graph_result.json")
    parser.add_argument("--json-output", default="prototypes/cognitive_math_graph_v0/outputs/real_graph/concept_patch.json")
    parser.add_argument("--md-output", default="prototypes/cognitive_math_graph_v0/outputs/real_graph/concept_patch.md")
    args = parser.parse_args()

    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    patch = build_patch(data)

    json_output = Path(args.json_output)
    md_output = Path(args.md_output)
    json_output.parent.mkdir(parents=True, exist_ok=True)
    md_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(patch, ensure_ascii=False, indent=2), encoding="utf-8")
    md_output.write_text(render_markdown(patch), encoding="utf-8")

    print(f"Wrote: {json_output}")
    print(f"Wrote: {md_output}")
    print(f"concept bridges: {sum(1 for n in patch['nodes'] if n['type'] == 'ConceptBridge')}")


if __name__ == "__main__":
    main()
