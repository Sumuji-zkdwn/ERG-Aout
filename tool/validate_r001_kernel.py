#!/usr/bin/env python3
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Dict, List, Set, Tuple

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "r001_graph.schema.json"
ALLOWED_CROSS_LAYER_ENDPOINTS = {
    "reply": ("L_raw", "L_raw"),
    "mentions": ("L_raw", "L_accepted"),
    "introduces": ("L_raw", "L_candidate"),
    "accepted_from_candidate": ("L_candidate", "L_accepted"),
    "observes_kernel_change": ("L_gitlog", "L_accepted"),
}
ALLOWED_NODE_TYPES_BY_LAYER = {
    "L_raw": {"RawMessage", "RawArtifact", "RawObservation"},
    "L_candidate": {"CandidateDefinition", "CandidateClaim", "CandidateExample", "CandidateFailureCase", "CandidateQuestion", "CandSymbol"},
    "L_accepted": {"KernelDefinition", "KernelAxiom", "KernelExample", "KernelFailureCase", "KernelDecision", "KConcept"},
    "L_gitlog": {"GitCommit", "GitFileDelta", "GitTagOrRound", "GitDecisionNote"},
}

def maybe_validate_schema(payload: dict) -> List[str]:
    try:
        import jsonschema  # type: ignore
    except Exception:
        return []
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    return [f"schema error at '{'/'.join(str(p) for p in e.path)}': {e.message}" for e in validator.iter_errors(payload)]

def detect_cycle(edges: List[Tuple[str, str]]) -> bool:
    graph: Dict[str, List[str]] = {}
    for s, d in edges: graph.setdefault(s, []).append(d)
    visiting, visited = set(), set()
    def dfs(n: str) -> bool:
        if n in visiting: return True
        if n in visited: return False
        visiting.add(n)
        for m in graph.get(n, []):
            if dfs(m): return True
        visiting.remove(n); visited.add(n); return False
    return any(dfs(n) for n in list(graph))

def validate(payload: dict) -> List[str]:
    errors = maybe_validate_schema(payload)
    nodes, edges = payload.get("nodes", []), payload.get("edges", [])
    node_ids, edge_ids = set(), set()
    for i, n in enumerate(nodes):
        if not isinstance(n, dict): continue
        nid = n.get("id")
        if nid in node_ids: errors.append(f"duplicate node id: '{nid}'")
        elif isinstance(nid, str): node_ids.add(nid)
        layer, ntype = n.get("layer"), n.get("type")
        if isinstance(layer, str) and isinstance(ntype, str):
            allowed = ALLOWED_NODE_TYPES_BY_LAYER.get(layer)
            if allowed is not None and ntype not in allowed:
                errors.append(f"node type '{ntype}' is not allowed in layer '{layer}' at nodes[{i}]")
    node_map = {n["id"]: n for n in nodes if isinstance(n, dict) and "id" in n}
    for e in edges:
        if not isinstance(e, dict): continue
        eid = e.get("id")
        if eid in edge_ids: errors.append(f"duplicate edge id: '{eid}'")
        elif isinstance(eid, str): edge_ids.add(eid)
        src, dst = e.get("source"), e.get("target")
        if src not in node_map: errors.append(f"edge '{eid}' source does not exist in nodes: '{src}'")
        if dst not in node_map: errors.append(f"edge '{eid}' target does not exist in nodes: '{dst}'")

    extends_main = [(e["source"], e["target"]) for e in edges if isinstance(e, dict) and e.get("type") == "extends_main"]
    main_nodes: Set[str] = set()
    for s, d in extends_main:
        main_nodes.add(s); main_nodes.add(d)
        if node_map.get(s, {}).get("layer") != "L_accepted" or node_map.get(d, {}).get("layer") != "L_accepted":
            errors.append("extends_main endpoints must both be in L_accepted")
    if detect_cycle(extends_main): errors.append("extends_main must be acyclic")
    indeg: Dict[str, int] = {}; outdeg: Dict[str, int] = {}
    for s, d in extends_main:
        indeg[d] = indeg.get(d, 0) + 1; outdeg[s] = outdeg.get(s, 0) + 1
    if extends_main:
        if any(v > 1 for v in indeg.values()) or any(v > 1 for v in outdeg.values()):
            errors.append("extends_main must form a single linear path (no fan-in/fan-out)")
        starts = [n for n in main_nodes if indeg.get(n, 0) == 0]
        ends = [n for n in main_nodes if outdeg.get(n, 0) == 0]
        if len(starts) != 1 or len(ends) != 1: errors.append("extends_main must have exactly one start and one end node")

    for e in [x for x in edges if isinstance(x, dict) and x.get("type") == "extends_branch"]:
        s, d = node_map.get(e.get("source"), {}), node_map.get(e.get("target"), {})
        if s.get("layer") != "L_accepted" or d.get("layer") != "L_accepted":
            errors.append("extends_branch endpoints must both be in L_accepted")
        elif e.get("target") in main_nodes:
            errors.append("extends_branch does not modify canonical path (target must not be canonical)")

    for e in edges:
        if not isinstance(e, dict): continue
        t = e.get("type")
        if t in ALLOWED_CROSS_LAYER_ENDPOINTS:
            es, ed = ALLOWED_CROSS_LAYER_ENDPOINTS[t]
            s, d = node_map.get(e.get("source"), {}), node_map.get(e.get("target"), {})
            if s.get("layer") != es or d.get("layer") != ed:
                errors.append(f"cross-layer policy violation for '{t}': expected {es} -> {ed}")
    return errors

def main() -> int:
    p = argparse.ArgumentParser(); p.add_argument("graph", type=Path); a = p.parse_args()
    errors = validate(json.loads(a.graph.read_text(encoding="utf-8")))
    if errors:
        print("INVALID"); [print(f"- {e}") for e in errors]; return 1
    print("VALID"); return 0

if __name__ == "__main__":
    raise SystemExit(main())
