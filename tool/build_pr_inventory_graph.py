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


def propose(r, version_conflicts):
    """Return (proposal, rule) for one PR. Mechanical; rules are applied in this order."""
    n, k = r["number"], r["kernel"]
    if k["status"] == "no_lean_content":
        return "tooling", "no Lean source of its own (tools, docs, demos or Python checks only)"
    if k["status"] != "ok":
        steps = k.get("failed_steps") or {}
        why = "the head's own proof check failed" if steps.get("proof_only") else k["status"]
        return "defer", f"kernel extraction not possible: {why}"
    if r["identical_to"]:
        return "absorb", f"all own Lean units reappear byte-identically in PR(s) {r['identical_to']}"
    if n in version_conflicts:
        return "choose_version", f"same file path with different bytes in PR(s) {version_conflicts[n]}"
    if "(open)" in r["title"].lower():
        return "defer", "the PR title marks the result as open"
    if k["theorems_using_main_any_edge"] == 0:
        return "branch", "compiles; none of its new theorems references a declaration that is in main"
    return "integrate", "compiles; references main; no duplicate or version conflict"


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
    for r in rows.values():
        r["behind_main_commits"] = r["behind_main"]

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
            if rows[m]["kernel"]["status"] != "ok":
                continue  # never propose absorbing into a PR whose own proofs do not check
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
        proposal, rule = propose(r, {k: sorted(v) for k, v in version_conflicts.items()})
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
    (out / "evidence.md").write_text(evidence_md(ev, a.main_commit), encoding="utf-8")
    print(json.dumps(dict(nodes=len(nodes), edges=len(edges),
                          proposals={p: sum(r["proposal"] == p for r in ev) for p in
                                     ("integrate", "branch", "absorb", "choose_version", "defer", "tooling")})))


LABEL = {"integrate": "本線候補", "branch": "分岐", "absorb": "吸収", "choose_version": "版の選択",
         "defer": "保留", "tooling": "道具類"}


def evidence_md(ev, main_commit):
    L = ["# 根拠表：primitive-lean 未統合 PR の棚卸し", "",
         f"`main` = `{main_commit[:7]}` に対する測定。判定案は候補であり、採否は人が決める。", "",
         "列の意味：新定理・新定義 = `main` にない宣言のうち、この PR 固有のファイルに属するもの（カーネル受理済み）。"
         "main 参照 = 推移的依存に `main` の宣言を含む定理の数。main 定理を証明に使用 = 証明項の連鎖に `main` の定理を含む定理の数。"
         "初期層 = 初期層に到達する定理の数。遅れ = PR のヘッドに含まれない `main` のコミット数。", "",
         "| PR | 判定案 | 新定理 | 新定義 | main 参照 | main 定理を証明に使用 | 初期層 | 遅れ | 規則 |",
         "|---|---|---:|---:|---:|---:|---:|---:|---|"]
    for r in sorted(ev, key=lambda r: (list(LABEL).index(r["proposal"]), r["number"])):
        k = r["kernel"]
        g = (lambda x: k.get(x, "—")) if k["status"] == "ok" else (lambda x: "—")
        L.append(f"| #{r['number']} | {LABEL[r['proposal']]} | {g('new_theorems')} | {g('new_definitions')} | "
                 f"{g('theorems_using_main_any_edge')} | {g('theorems_using_main_theorem_in_proof')} | "
                 f"{g('theorems_reaching_initial')} | {r['behind_main']} | {r['rule']} |")
    L += ["", "## 補足", ""]
    for r in sorted(ev, key=lambda r: r["number"]):
        notes = []
        k = r["kernel"]
        if k.get("files_without_declarations"):
            notes.append("宣言が帰属しないファイル: " + ", ".join(f"`{f}`" for f in k["files_without_declarations"]))
        if k.get("names_shared_with_other_prs"):
            notes.append("同名の宣言を持つ PR: " + ", ".join(f"#{m}" for m in k["names_shared_with_other_prs"]))
        if notes:
            L.append(f"- #{r['number']}: " + "。".join(notes))
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
