#!/usr/bin/env python3
"""Export R002 candidate review table from an existing graph JSON.

This helper is NOT a candidate generator.
It reads existing nodes/edges and prints a markdown table for manual review.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List, Tuple


class StructureError(ValueError):
    """Raised when input structure is incompatible with exporter expectations."""


def load_graph(path: Path) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StructureError(f"graph file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StructureError(f"invalid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise StructureError("top-level JSON must be an object")

    nodes = payload.get("nodes")
    edges = payload.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise StructureError("graph must include list fields: 'nodes' and 'edges'")

    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise StructureError(f"node at index {i} is not an object")
        for k in ("id", "layer", "type"):
            if k not in node:
                raise StructureError(f"node at index {i} missing required key: {k}")

    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            raise StructureError(f"edge at index {i} is not an object")
        for k in ("id", "type", "source", "target"):
            if k not in edge:
                raise StructureError(f"edge at index {i} missing required key: {k}")

    return payload


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


def load_sidecar_raw_excerpt(path: Path) -> Dict[str, str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise StructureError(f"sidecar file does not exist: {path}") from exc

    header_cells: List[str] | None = None
    i = 0
    while i < len(lines):
        header = split_markdown_row(lines[i])
        if header and i + 1 < len(lines):
            sep = split_markdown_row(lines[i + 1])
            if sep and len(sep) == len(header) and is_separator_row(sep):
                header_cells = header
                break
        i += 1

    if header_cells is None:
        raise StructureError("no markdown table header row found in sidecar")
    if "raw_id" not in header_cells or "text_excerpt" not in header_cells:
        raise StructureError("sidecar table must include 'raw_id' and 'text_excerpt' columns")

    raw_idx = header_cells.index("raw_id")
    excerpt_idx = header_cells.index("text_excerpt")

    by_raw: Dict[str, str] = {}
    row_idx = i + 2
    while row_idx < len(lines):
        row = split_markdown_row(lines[row_idx])
        if not row or len(row) != len(header_cells):
            break
        by_raw[row[raw_idx]] = row[excerpt_idx]
        row_idx += 1

    return by_raw


def esc(text: str) -> str:
    return text.replace("|", "\\|")


def collect_rows(graph: dict, raw_excerpt_map: Dict[str, str] | None) -> Tuple[List[dict], List[str]]:
    nodes = graph["nodes"]
    edges = graph["edges"]
    node_map = {n["id"]: n for n in nodes}

    intro_by_candidate: Dict[str, List[str]] = {}
    accepted_by_candidate: Dict[str, List[str]] = {}

    for e in edges:
        if e.get("type") == "introduces":
            intro_by_candidate.setdefault(e["target"], []).append(e["source"])
        if e.get("type") == "accepted_from_candidate":
            accepted_by_candidate.setdefault(e["source"], []).append(e["target"])

    warnings: List[str] = []
    rows: List[dict] = []

    candidate_ids = sorted(n["id"] for n in nodes if n.get("layer") == "L_candidate")
    for candidate_id in candidate_ids:
        raw_ids = sorted(intro_by_candidate.get(candidate_id, []))
        accepted_ids = sorted(accepted_by_candidate.get(candidate_id, []))

        introduced_by_raw = ", ".join(raw_ids) if raw_ids else "(none)"
        raw_excerpt = "(sidecar not provided)"
        if raw_excerpt_map is not None:
            if raw_ids:
                excerpts = [raw_excerpt_map.get(rid, "(raw_id not found in sidecar)") for rid in raw_ids]
                raw_excerpt = " / ".join(excerpts)
            else:
                raw_excerpt = "(no introducing raw)"

        if len(accepted_ids) == 0:
            status = "unaccepted"
            accepted_target = "(none)"
            accepted_type = "(none)"
            review_note = "candidate remains unaccepted"
        elif len(accepted_ids) == 1:
            status = "accepted"
            accepted_target = accepted_ids[0]
            accepted_type = str(node_map.get(accepted_ids[0], {}).get("type", "(unknown)"))
            review_note = "candidate promoted to accepted"
        else:
            status = "accepted_multiple"
            accepted_target = ", ".join(accepted_ids)
            accepted_types = [str(node_map.get(aid, {}).get("type", "(unknown)")) for aid in accepted_ids]
            accepted_type = ", ".join(accepted_types)
            review_note = "candidate has multiple accepted targets; review manually"
            warnings.append(
                f"candidate '{candidate_id}' has multiple accepted_from_candidate targets: {accepted_target}"
            )

        if not raw_ids:
            note = "candidate has no introducing raw; review manually"
            review_note = f"{review_note}; {note}" if review_note else note
            warnings.append(f"candidate '{candidate_id}' has no incoming introduces")

        rows.append(
            {
                "candidate_id": candidate_id,
                "introduced_by_raw": introduced_by_raw,
                "raw_excerpt": raw_excerpt,
                "status": status,
                "accepted_target": accepted_target,
                "accepted_type": accepted_type,
                "review_note": review_note,
            }
        )

    return rows, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Export R002 candidate review markdown table")
    parser.add_argument("graph", type=Path, help="Path to graph JSON")
    parser.add_argument("--sidecar", type=Path, help="Optional path to raw text sidecar markdown")
    args = parser.parse_args()

    try:
        graph = load_graph(args.graph)
        raw_excerpt_map = load_sidecar_raw_excerpt(args.sidecar) if args.sidecar else None
    except StructureError as exc:
        print("INVALID R002 CANDIDATE REVIEW INPUT")
        print(f"- {exc}")
        return 1

    rows, warnings = collect_rows(graph, raw_excerpt_map)

    print("# R002 Candidate Review Table")
    print()
    print("| candidate_id | introduced_by_raw | raw_excerpt | status | accepted_target | accepted_type | review_note |")
    print("|---|---|---|---|---|---|---|")
    for row in rows:
        print(
            "| {candidate_id} | {introduced_by_raw} | {raw_excerpt} | {status} | {accepted_target} | {accepted_type} | {review_note} |".format(
                **{k: esc(str(v)) for k, v in row.items()}
            )
        )

    print()
    print("## Warnings")
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- none")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
