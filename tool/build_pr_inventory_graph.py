#!/usr/bin/env python3
"""Build an R001-valid ERG graph and an evidence sidecar for a PR inventory round.

Input: the PR comparison JSON produced by primitive-lean `tools/deps/pr_compare.py`
plus that repository's structural inventory. Output:
  graph.json         R001 graph (validate with tool/validate_r001_kernel.py)
  evidence.md        per-candidate evidence and the rule that produced each proposal

Layering follows docs/R001_SEMANTICS.md:
  L_raw        one RawArtifact per open PR, plus the kernel dependency report
  L_candidate  one CandidateClaim per PR content, one CandidateQuestion per
               unresolved version choice; proposed decisions are candidate data
  L_accepted   only content already merged into main (KernelDecision chain)
  L_gitlog     the main commit the inventory was measured against
No open PR is moved to L_accepted. Proposals are not decisions.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MERGED_MAIN = [  # first-parent order of merges into primitive-lean main
    ("accepted.primitive_lean.baseline", "initial assembly (Elastica + linear input, 465 theorems)"),
    ("accepted.primitive_lean.pr68", "PR #68 orbit-trace"),
    ("accepted.primitive_lean.pr3", "PR #3 history derivation stack (incl. #28)"),
    ("accepted.primitive_lean.pr74", "PR #74 operator self-extension stack"),
]


def propose(r, struct, version_conflicts):
    """Return (proposal, rule) for one PR. Purely mechanical; see module docstring."""
    n = r["number"]
    k = r["kernel"]
    ci = r["ci"]
    ci_fail = any(c["conclusion"] == "failure" for c in ci)
    ci_ok = any(c["conclusion"] == "success" and "integration" in c["name"].lower() for c in ci) or \
        (ci and all(c["conclusion"] == "success" for c in ci))
    if k["status"] == "no_lean_content":
        return "tooling", "no Lean source of its own"
    if r["identical_to"]:
        return "absorb", f"own Lean units are byte-identical to PR(s) {r['identical_to']}"
    if n in version_conflicts:
        return "choose_version", f"same path, different bytes as PR(s) {version_conflicts[n]}"
    if k["status"] != "ok":
        return "defer", f"kernel extraction {k['status']} ({k.get('failed_steps')})"
    if ci_fail and not ci_ok:
        return "defer", "latest recorded CI on this head failed"
    if "(open)" in r["title"].lower() or " open" in r["title"].lower().split(":")[-1]:
        return "defer", "title marks the result as open"
    if k["theorems_using_main_any_edge"] == 0:
        return "branch", "kernel ok; no new theorem references any main declaration"
    return "integrate", "kernel ok; references main; no duplicate or version conflict"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--compare", required=True)
    ap.add_argument("--structure", required=True)
    ap.add_argument("--main-commit", required=True)
    ap.add_argument("--outdir", required=True)
    a = ap.parse_args()
    C = json.loads(Path(a.compare).read_text())
    S = json.loads(Path(a.structure).read_text())
    rows = {int(k): v for k, v in C["prs"].items()}

    P = {p["number"]: p for p in S["prs"]}
    own_units = {n: {(u["path"], u["blob"]) for u in p["own_units"]} for n, p in P.items()}
    version_conflicts = {}
    for x in S["same_path_different_bytes"]:
        owners = [m for v in x["versions"].values() for m in v]
        for n in owners:
            version_conflicts.setdefault(n, set()).update(m for m in owners if m != n)
    for n, r in rows.items():
        # Absorbed: every own unit of n reappears byte-identically in another PR m that is
        # larger, or equal in size but closer to main (fewer commits behind; then higher number).
        keepers = []
        for m in P:
            if m == n or not own_units[n] or not own_units[n] <= own_units[m]:
                continue
            larger = len(own_units[m]) > len(own_units[n])
            closer = (len(own_units[m]) == len(own_units[n]) and
                      (P[m]["behind_main"], -m) < (P[n]["behind_main"], -n))
            if larger or closer:
                keepers.append(m)
        r["identical_to"] = sorted(keepers)
    nodes, edges, ev = [], [], []

    def node(i, layer, t):
        nodes.append(dict(id=i, layer=layer, type=t))

    def edge(t, s, d):
        edges.append(dict(id=f"e{len(edges)+1:04d}", type=t, source=s, target=d))

    node("raw.primitive_lean.kernel_dependency_report", "L_raw", "RawArtifact")
    node(f"git.primitive_lean.main.{a.main_commit[:7]}", "L_gitlog", "GitCommit")
    prev = None
    for i, _ in MERGED_MAIN:
        node(i, "L_accepted", "KernelDecision")
        if prev:
            edge("extends_main", prev, i)
        prev = i
    edge("observes_kernel_change", f"git.primitive_lean.main.{a.main_commit[:7]}", prev)

    questions = {}
    for n, r in sorted(rows.items()):
        raw = f"raw.primitive_lean.pr{n}"
        cand = f"cand.primitive_lean.pr{n}.content"
        node(raw, "L_raw", "RawArtifact")
        node(cand, "L_candidate", "CandidateClaim")
        edge("introduces", raw, cand)
        proposal, rule = propose(r, S, {k: sorted(v) for k, v in version_conflicts.items()})
        r["proposal"], r["rule"] = proposal, rule
        if proposal == "choose_version":
            key = tuple(sorted({n, *version_conflicts[n]}))
            if key not in questions:
                qid = "cand.primitive_lean.question.version_" + "_".join(f"pr{m}" for m in key)
                questions[key] = qid
                node(qid, "L_candidate", "CandidateQuestion")
            edge("introduces", raw, questions[key])
        ev.append(r)

    graph = dict(nodes=nodes, edges=edges)
    out = Path(a.outdir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=1) + "\n")
    (out / "evidence.json").write_text(json.dumps(dict(main_commit=a.main_commit, scope=C["scope"], prs=ev),
                                                  ensure_ascii=False, indent=1) + "\n")
    print(json.dumps(dict(nodes=len(nodes), edges=len(edges),
                          proposals={p: sum(r["proposal"] == p for r in ev) for p in
                                     ("integrate", "branch", "absorb", "choose_version", "defer", "tooling")})))


if __name__ == "__main__":
    main()
