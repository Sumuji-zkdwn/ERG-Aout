#!/usr/bin/env python3
"""Check consistency between graph L_raw ids and sidecar raw_id table.

This helper is NOT a replacement for `tool/validate_r001_kernel.py`.
Use it after the validator as a supplemental sidecar alignment check.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List, Set, Tuple


class StructureError(ValueError):
    """Raised when input structure is incompatible with checker expectations."""


def load_graph_raw_ids(path: Path) -> Set[str]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StructureError(f"graph file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StructureError(f"invalid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise StructureError("top-level JSON must be an object")

    nodes = payload.get("nodes")
    if not isinstance(nodes, list):
        raise StructureError("graph must include list field: 'nodes'")

    raw_ids: Set[str] = set()
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise StructureError(f"node at index {i} is not an object")
        if "id" not in node or "layer" not in node:
            raise StructureError(f"node at index {i} missing required key: id/layer")
        if node.get("layer") == "L_raw":
            raw_ids.add(str(node["id"]))
    return raw_ids


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


def parse_sidecar_raw_ids(path: Path) -> Tuple[List[str], List[str], List[str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise StructureError(f"sidecar file does not exist: {path}") from exc

    header_cells: List[str] | None = None
    raw_id_idx: int | None = None
    recommended_columns = [
        "raw_id",
        "turn_index",
        "speaker",
        "text_excerpt",
        "source_note",
        "mapping_note",
    ]

    sidecar_raw_ids: List[str] = []

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
        raise StructureError("no markdown table header row found")

    if "raw_id" not in header_cells:
        raise StructureError("markdown table header does not include 'raw_id' column")

    raw_id_idx = header_cells.index("raw_id")

    row_index = i + 2
    while row_index < len(lines):
        row = split_markdown_row(lines[row_index])
        if not row:
            break
        if len(row) != len(header_cells):
            break
        sidecar_raw_ids.append(row[raw_id_idx])
        row_index += 1

    missing_recommended = [c for c in recommended_columns if c not in header_cells]
    return sidecar_raw_ids, header_cells, missing_recommended


def main() -> int:
    parser = argparse.ArgumentParser(description="Check R002 graph raw ids vs sidecar raw_id consistency")
    parser.add_argument("graph", type=Path, help="Path to graph JSON")
    parser.add_argument("sidecar", type=Path, help="Path to raw text sidecar markdown")
    args = parser.parse_args()

    try:
        graph_raw_ids = load_graph_raw_ids(args.graph)
        sidecar_raw_ids, header_columns, missing_recommended = parse_sidecar_raw_ids(args.sidecar)
    except StructureError as exc:
        print("INVALID R002 SIDECAR CONSISTENCY INPUT")
        print(f"- {exc}")
        return 1

    sidecar_raw_set = set(sidecar_raw_ids)
    missing_in_sidecar = sorted(graph_raw_ids - sidecar_raw_set)
    extra_in_sidecar = sorted(sidecar_raw_set - graph_raw_ids)

    seen = set()
    duplicates = []
    for rid in sidecar_raw_ids:
        if rid in seen and rid not in duplicates:
            duplicates.append(rid)
        seen.add(rid)

    warnings: List[str] = []
    notes: List[str] = []

    if missing_in_sidecar:
        warnings.append(f"missing graph raw ids in sidecar: {', '.join(missing_in_sidecar)}")
    if extra_in_sidecar:
        warnings.append(f"extra sidecar raw_id not in graph: {', '.join(extra_in_sidecar)}")
    if duplicates:
        warnings.append(f"duplicate sidecar raw_id values: {', '.join(duplicates)}")
    if missing_recommended:
        warnings.append(
            "sidecar table missing recommended columns: " + ", ".join(missing_recommended)
        )

    notes.append("validate_r001_kernel.py checks graph JSON structure/invariants")
    notes.append("check_r002_sidecar_consistency.py checks L_raw id <-> sidecar raw_id correspondence")
    notes.append(f"sidecar columns: {', '.join(header_columns)}")

    print("VALID R002 SIDECAR CONSISTENCY")
    print("WARNINGS")
    if warnings:
        for warning in warnings:
            print(f"- {warning}")
    else:
        print("- none")

    print("NOTES")
    for note in notes:
        print(f"- {note}")

    print("SUMMARY")
    print(f"- graph raw ids: {len(graph_raw_ids)}")
    print(f"- sidecar raw ids: {len(sidecar_raw_ids)}")
    print(f"- missing in sidecar: {', '.join(missing_in_sidecar) if missing_in_sidecar else '(none)'}")
    print(f"- extra in sidecar: {', '.join(extra_in_sidecar) if extra_in_sidecar else '(none)'}")
    print(f"- duplicate sidecar raw_ids: {', '.join(duplicates) if duplicates else '(none)'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
