#!/usr/bin/env python3
"""Check a formal-binding sidecar against an ERG graph and, optionally, a formal repository.

A formal-binding sidecar records which declarations in an external formal
repository (for example a Lean project) correspond to candidate/accepted ERG
nodes. See `docs/R005_FORMAL_BINDING.md`.

This helper is NOT a replacement for `tool/validate_r001_kernel.py`, and it is
NOT a proof checker:

- Structural checks always run (node existence, layer/type vs relation,
  required fidelity notes and non-claims, pinned commit and file hashes).
- With `--formal-repo OWNER/NAME=DIR`, the pinned commit is read from a local
  git clone: file bytes are hashed and each declaration is located textually
  (namespace + keyword + name). Proof validity stays the responsibility of the
  formal repository's own verification at that commit.
- Whether a declaration faithfully expresses the node's intuition is a human
  judgment recorded in `fidelity_note`; this tool cannot check it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

BINDING_VERSION = 1

BINDABLE_LAYERS = {"L_candidate", "L_accepted"}

DEFINITION_NODE_TYPES = {"CandidateDefinition", "CandSymbol", "KernelDefinition", "KConcept"}
PROPOSITION_NODE_TYPES = {
    "CandidateClaim",
    "CandidateExample",
    "CandidateFailureCase",
    "KernelClaim",
    "KernelExample",
    "KernelFailureCase",
}

# relation -> node types the relation may be attached to
RELATION_NODE_TYPES: Dict[str, Set[str]] = {
    "defines": DEFINITION_NODE_TYPES,
    "proves": PROPOSITION_NODE_TYPES,
    "proves_restricted": PROPOSITION_NODE_TYPES,
    "refutes": {"CandidateClaim"},
}

DEFINITIONAL_KINDS = {"def", "abbrev", "structure", "inductive", "class", "instance"}
PROPOSITIONAL_KINDS = {"theorem", "lemma"}
DECLARATION_KINDS = DEFINITIONAL_KINDS | PROPOSITIONAL_KINDS

# Unknown keys are rejected so that new semantics cannot be added silently.
TOP_KEYS = {"binding_version", "formal_source", "bindings", "unbound"}
SOURCE_KEYS = {"repository", "commit", "language", "files", "verification_record", "verification_note"}
BINDING_KEYS = {"id", "node", "relation", "declarations", "fidelity_note", "non_claims"}
DECLARATION_KEYS = {"name", "kind", "file"}
UNBOUND_KEYS = {"node", "reason"}

ID_PATTERN = re.compile(r"^[A-Za-z0-9_.:-]+$")
REPOSITORY_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
QUALIFIED_NAME_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_']*(\.[A-Za-z_][A-Za-z0-9_']*)+$")

LEAN_DECLARATION = re.compile(
    r"^\s*(?:@\[[^\]]*\]\s*)*"
    r"(?:(?:private|protected|noncomputable|partial|nonrec|unsafe)\s+)*"
    r"(theorem|lemma|def|abbrev|structure|inductive|instance|class)\s+"
    r"([^\s:({\[]+)"
)
LEAN_NAMESPACE = re.compile(r"^\s*namespace\s+([^\s]+)\s*$")
LEAN_SECTION = re.compile(r"^\s*(?:noncomputable\s+)?section(?:\s+([^\s]+))?\s*$")
LEAN_END = re.compile(r"^\s*end(?:\s+([^\s]+))?\s*$")


class StructureError(ValueError):
    """Raised when an input file cannot be read as the expected structure."""


@dataclass
class Report:
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    summary: List[str] = field(default_factory=list)


def load_json(path: Path, label: str) -> dict:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise StructureError(f"{label} file does not exist: {path}") from exc
    except json.JSONDecodeError as exc:
        raise StructureError(f"{label} is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise StructureError(f"{label} top-level JSON must be an object")
    return payload


def nonempty_string(value) -> bool:
    return isinstance(value, str) and bool(value.strip())


def unknown_keys(obj: dict, allowed: Set[str], where: str, report: Report) -> None:
    extra = sorted(set(obj) - allowed)
    if extra:
        report.errors.append(f"{where}: unknown keys {extra}")


# ---------------------------------------------------------------------------
# Structural checks
# ---------------------------------------------------------------------------


def check_structure(graph: dict, binding: dict, report: Report) -> Tuple[dict, List[dict], List[dict]]:
    nodes = graph.get("nodes")
    edges = graph.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        raise StructureError("graph must include list fields 'nodes' and 'edges'")
    node_map = {n["id"]: n for n in nodes if isinstance(n, dict) and "id" in n}

    unknown_keys(binding, TOP_KEYS, "binding file", report)
    if binding.get("binding_version") != BINDING_VERSION:
        report.errors.append(f"binding_version must be {BINDING_VERSION}")

    source = binding.get("formal_source")
    if not isinstance(source, dict):
        report.errors.append("formal_source must be an object")
        source = {}
    unknown_keys(source, SOURCE_KEYS, "formal_source", report)
    if not (isinstance(source.get("repository"), str) and REPOSITORY_PATTERN.match(source["repository"])):
        report.errors.append("formal_source.repository must be 'owner/name'")
    if not (isinstance(source.get("commit"), str) and COMMIT_PATTERN.match(source["commit"])):
        report.errors.append("formal_source.commit must be a full 40-character lowercase commit id")
    if not nonempty_string(source.get("language")):
        report.errors.append("formal_source.language must be a non-empty string")
    files = source.get("files")
    if not isinstance(files, dict) or not files:
        report.errors.append("formal_source.files must be a non-empty object {path: sha256}")
        files = {}
    for path, digest in files.items():
        if not nonempty_string(path) or path.startswith("/") or ".." in Path(path).parts:
            report.errors.append(f"formal_source.files has an unsafe path: {path!r}")
        if not (isinstance(digest, str) and SHA256_PATTERN.match(digest)):
            report.errors.append(f"formal_source.files['{path}'] must be a lowercase sha256")
    for key in ("verification_record", "verification_note"):
        if key in source and not nonempty_string(source[key]):
            report.errors.append(f"formal_source.{key} must be a non-empty string when present")

    bindings = binding.get("bindings")
    if not isinstance(bindings, list) or not bindings:
        report.errors.append("bindings must be a non-empty list")
        bindings = []
    unbound = binding.get("unbound", [])
    if not isinstance(unbound, list):
        report.errors.append("unbound must be a list when present")
        unbound = []

    seen_ids: Set[str] = set()
    relations_by_node: Dict[str, Set[str]] = {}
    for index, row in enumerate(bindings):
        where = f"bindings[{index}]"
        if not isinstance(row, dict):
            report.errors.append(f"{where} must be an object")
            continue
        unknown_keys(row, BINDING_KEYS, where, report)
        binding_id = row.get("id")
        if not (isinstance(binding_id, str) and ID_PATTERN.match(binding_id)):
            report.errors.append(f"{where}.id must match {ID_PATTERN.pattern}")
        elif binding_id in seen_ids:
            report.errors.append(f"binding id is duplicated: {binding_id}")
        else:
            seen_ids.add(binding_id)
            where = f"binding '{binding_id}'"

        node_id = row.get("node")
        node = node_map.get(node_id)
        relation = row.get("relation")
        if node is None:
            report.errors.append(f"{where}: node does not exist in graph: {node_id}")
        elif node.get("layer") not in BINDABLE_LAYERS:
            report.errors.append(
                f"{where}: node '{node_id}' is in {node.get('layer')}; only L_candidate/L_accepted may be bound"
            )
        if relation not in RELATION_NODE_TYPES:
            report.errors.append(f"{where}: relation must be one of {sorted(RELATION_NODE_TYPES)}")
        elif node is not None and node.get("type") not in RELATION_NODE_TYPES[relation]:
            report.errors.append(
                f"{where}: relation '{relation}' cannot be attached to node type '{node.get('type')}'"
            )
        if isinstance(node_id, str) and relation in RELATION_NODE_TYPES:
            relations_by_node.setdefault(node_id, set()).add(relation)

        declarations = row.get("declarations")
        if not isinstance(declarations, list) or not declarations:
            report.errors.append(f"{where}: declarations must be a non-empty list")
            declarations = []
        kinds: Set[str] = set()
        for dindex, decl in enumerate(declarations):
            dwhere = f"{where}.declarations[{dindex}]"
            if not isinstance(decl, dict):
                report.errors.append(f"{dwhere} must be an object")
                continue
            unknown_keys(decl, DECLARATION_KEYS, dwhere, report)
            if not (isinstance(decl.get("name"), str) and QUALIFIED_NAME_PATTERN.match(decl["name"])):
                report.errors.append(f"{dwhere}.name must be a fully qualified declaration name")
            if decl.get("kind") not in DECLARATION_KINDS:
                report.errors.append(f"{dwhere}.kind must be one of {sorted(DECLARATION_KINDS)}")
            else:
                kinds.add(decl["kind"])
            if decl.get("file") not in files:
                report.errors.append(f"{dwhere}.file must be listed in formal_source.files")
        if relation == "defines" and declarations and not kinds & DEFINITIONAL_KINDS:
            report.errors.append(f"{where}: 'defines' needs at least one definitional declaration")
        if relation in {"proves", "proves_restricted", "refutes"} and declarations and not kinds & PROPOSITIONAL_KINDS:
            report.errors.append(f"{where}: '{relation}' needs at least one theorem/lemma declaration")

        if not nonempty_string(row.get("fidelity_note")):
            report.errors.append(f"{where}: fidelity_note must state how the declaration matches the node")
        non_claims = row.get("non_claims", [])
        if not isinstance(non_claims, list) or not all(nonempty_string(c) for c in non_claims):
            report.errors.append(f"{where}: non_claims must be a list of non-empty strings")
            non_claims = []
        if relation == "proves_restricted" and not non_claims:
            report.errors.append(f"{where}: 'proves_restricted' requires at least one non_claims entry")

    unbound_nodes: Set[str] = set()
    for index, row in enumerate(unbound):
        where = f"unbound[{index}]"
        if not isinstance(row, dict):
            report.errors.append(f"{where} must be an object")
            continue
        unknown_keys(row, UNBOUND_KEYS, where, report)
        node_id = row.get("node")
        node = node_map.get(node_id)
        if node is None:
            report.errors.append(f"{where}: node does not exist in graph: {node_id}")
        elif node.get("layer") not in BINDABLE_LAYERS:
            report.errors.append(f"{where}: node '{node_id}' is not a candidate/accepted node")
        if not nonempty_string(row.get("reason")):
            report.errors.append(f"{where}: reason must explain why no formal counterpart is bound")
        if node_id in unbound_nodes:
            report.errors.append(f"{where}: node listed twice as unbound: {node_id}")
        if isinstance(node_id, str):
            unbound_nodes.add(node_id)

    for node_id, relations in sorted(relations_by_node.items()):
        if node_id in unbound_nodes:
            report.errors.append(f"node '{node_id}' is both bound and listed as unbound")
        if "refutes" in relations and relations & {"proves", "proves_restricted"}:
            report.errors.append(f"node '{node_id}' is bound as both proved and refuted")

    # Signals for human review. These never change graph status.
    outgoing_acceptance = {
        e.get("source") for e in edges if isinstance(e, dict) and e.get("type") == "accepted_from_candidate"
    }
    for node_id, relations in sorted(relations_by_node.items()):
        node = node_map.get(node_id)
        if node is None:
            continue
        layer = node.get("layer")
        if layer == "L_candidate" and node_id in outgoing_acceptance and "refutes" in relations:
            report.warnings.append(
                f"promoted candidate '{node_id}' is refuted by the formal source; "
                "its accepted counterpart should be reviewed (for example superseded)"
            )
        if layer == "L_candidate" and node_id not in outgoing_acceptance:
            if "proves" in relations:
                report.notes.append(
                    f"promotion candidate: '{node_id}' has formal evidence ('proves'); acceptance remains a review decision"
                )
            elif "proves_restricted" in relations:
                report.notes.append(
                    f"restricted evidence: '{node_id}' is proved only under recorded restrictions; "
                    "carry its non_claims if it is promoted"
                )
            elif "refutes" in relations:
                report.notes.append(f"refuted candidate: '{node_id}' should not be promoted as stated")
            elif "defines" in relations:
                report.notes.append(
                    f"promotion candidate (definition): '{node_id}' has a formal definition ('defines'); "
                    "acceptance remains a review decision"
                )

    # An accepted node promoted from a bound candidate inherits that candidate's binding.
    inherited = {
        e.get("target")
        for e in edges
        if isinstance(e, dict)
        and e.get("type") == "accepted_from_candidate"
        and e.get("source") in relations_by_node
    }
    for node_id in sorted(inherited & set(relations_by_node)):
        report.notes.append(
            f"accepted node '{node_id}' is bound directly and also inherits its candidate's binding"
        )
    classified = set(relations_by_node) | unbound_nodes | inherited
    unclassified = sorted(
        n["id"]
        for n in nodes
        if isinstance(n, dict)
        and n.get("layer") in BINDABLE_LAYERS
        and n.get("type") in DEFINITION_NODE_TYPES | PROPOSITION_NODE_TYPES | {"CandidateQuestion"}
        and n.get("id") not in classified
    )
    if unclassified:
        report.notes.append(
            "nodes neither bound nor listed as unbound: " + ", ".join(unclassified)
        )

    report.summary.append(f"bindings: {len(bindings)}")
    report.summary.append(f"bound nodes: {len(relations_by_node)}")
    report.summary.append(f"unbound nodes: {len(unbound_nodes)}")
    report.summary.append(f"accepted nodes covered via their candidate: {len(inherited - set(relations_by_node))}")
    relation_counts: Dict[str, int] = {}
    for row in bindings:
        if isinstance(row, dict) and row.get("relation") in RELATION_NODE_TYPES:
            relation_counts[row["relation"]] = relation_counts.get(row["relation"], 0) + 1
    report.summary.append(
        "relations: " + (", ".join(f"{k}={v}" for k, v in sorted(relation_counts.items())) or "(none)")
    )
    return source, [b for b in bindings if isinstance(b, dict)], unbound


# ---------------------------------------------------------------------------
# Formal repository checks
# ---------------------------------------------------------------------------


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True)


def strip_lean_comments(source: str) -> str:
    """Blank out Lean comments and string literals, keeping line structure."""
    out: List[str] = []
    i, depth, in_string = 0, 0, False
    while i < len(source):
        c, pair = source[i], source[i : i + 2]
        if depth:
            if pair == "/-":
                depth += 1
                out.append("  ")
                i += 2
            elif pair == "-/":
                depth -= 1
                out.append("  ")
                i += 2
            else:
                out.append("\n" if c == "\n" else " ")
                i += 1
            continue
        if in_string:
            if c == "\\":
                out.append("  ")
                i += 2
                continue
            if c == '"':
                in_string = False
            out.append("\n" if c == "\n" else " ")
            i += 1
            continue
        if pair == "/-":
            depth = 1
            out.append("  ")
            i += 2
        elif pair == "--":
            end = source.find("\n", i)
            end = len(source) if end < 0 else end
            out.append(" " * (end - i))
            i = end
        elif c == '"':
            in_string = True
            out.append(" ")
            i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def lean_declarations(source: str) -> Dict[str, str]:
    """Map fully qualified declaration names to their keyword (textual scan)."""
    found: Dict[str, str] = {}
    scopes: List[Tuple[str, str]] = []  # (kind, name) with kind in {"namespace", "section"}
    for line in strip_lean_comments(source).splitlines():
        match = LEAN_NAMESPACE.match(line)
        if match:
            scopes.append(("namespace", match.group(1)))
            continue
        match = LEAN_SECTION.match(line)
        if match:
            scopes.append(("section", match.group(1) or ""))
            continue
        match = LEAN_END.match(line)
        if match:
            if scopes:
                scopes.pop()
            continue
        match = LEAN_DECLARATION.match(line)
        if match:
            kind, name = match.groups()
            if name.startswith("_root_."):
                full = name[len("_root_.") :]
            else:
                prefix = [n for k, n in scopes if k == "namespace"]
                full = ".".join(prefix + [name])
            found.setdefault(full, kind)
    return found


def same_kind(expected: str, actual: str) -> bool:
    theoremish = {"theorem", "lemma"}
    return expected == actual or (expected in theoremish and actual in theoremish)


def check_formal_repo(
    source: dict, bindings: List[dict], repo: Path, main_ref: Optional[str], report: Report
) -> bool:
    commit = source.get("commit", "")
    if not (repo / ".git").exists() and git(repo, "rev-parse", "--git-dir").returncode != 0:
        report.errors.append(f"formal repository clone is not a git repository: {repo}")
        return False
    if git(repo, "cat-file", "-e", f"{commit}^{{commit}}").returncode != 0:
        report.errors.append(f"pinned commit {commit} is not present in the formal repository clone")
        return False
    if main_ref:
        if git(repo, "rev-parse", "--verify", "--quiet", f"{main_ref}^{{commit}}").returncode != 0:
            report.errors.append(f"main ref '{main_ref}' is not present in the formal repository clone")
        elif git(repo, "merge-base", "--is-ancestor", commit, main_ref).returncode != 0:
            report.errors.append(f"pinned commit {commit} is not contained in '{main_ref}'")

    record = source.get("verification_record")
    if record and git(repo, "cat-file", "-e", f"{commit}:{record}").returncode != 0:
        report.errors.append(f"verification_record does not exist at the pinned commit: {record}")

    declared: Dict[str, Dict[str, str]] = {}
    for path, digest in sorted(source.get("files", {}).items()):
        shown = git(repo, "show", f"{commit}:{path}")
        if shown.returncode != 0:
            report.errors.append(f"formal file does not exist at the pinned commit: {path}")
            continue
        actual = hashlib.sha256(shown.stdout).hexdigest()
        if actual != digest:
            report.errors.append(f"formal file hash mismatch at the pinned commit: {path} ({actual})")
        declared[path] = lean_declarations(shown.stdout.decode("utf-8", errors="replace"))

    located = 0
    for row in bindings:
        for decl in row.get("declarations", []) if isinstance(row.get("declarations"), list) else []:
            if not isinstance(decl, dict) or decl.get("file") not in declared:
                continue
            name, kind = decl.get("name"), decl.get("kind")
            actual_kind = declared[decl["file"]].get(name)
            if actual_kind is None:
                report.errors.append(
                    f"binding '{row.get('id')}': declaration '{name}' not found in {decl['file']} at {commit[:12]}"
                )
            elif not same_kind(kind, actual_kind):
                report.errors.append(
                    f"binding '{row.get('id')}': declaration '{name}' is a '{actual_kind}', not a '{kind}'"
                )
            else:
                located += 1
    report.summary.append(f"declarations located at {commit[:12]}: {located}")
    report.notes.append(
        "formal source checked textually at the pinned commit; proof validity is delegated to the "
        "formal repository's own verification at that commit"
    )
    return True


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_repo_mapping(values: List[str]) -> Dict[str, Path]:
    mapping: Dict[str, Path] = {}
    for value in values:
        if "=" not in value:
            raise StructureError(f"--formal-repo must be OWNER/NAME=DIR, got {value!r}")
        name, directory = value.split("=", 1)
        if not REPOSITORY_PATTERN.match(name):
            raise StructureError(f"--formal-repo repository must be OWNER/NAME, got {name!r}")
        mapping[name] = Path(directory)
    return mapping


def run(
    graph_path: Path,
    binding_path: Path,
    formal_repos: Dict[str, Path],
    main_ref: Optional[str],
    require_formal_check: bool,
) -> Report:
    report = Report()
    graph = load_json(graph_path, "graph")
    binding = load_json(binding_path, "binding")
    source, bindings, _ = check_structure(graph, binding, report)
    repository = source.get("repository")
    if repository in formal_repos:
        check_formal_repo(source, bindings, formal_repos[repository], main_ref, report)
    elif require_formal_check:
        report.errors.append(f"formal repository '{repository}' was not checked (no --formal-repo given)")
    else:
        report.notes.append(
            f"formal repository '{repository}' not checked; pass --formal-repo {repository}=DIR to check "
            "file hashes and declaration names at the pinned commit"
        )
    return report


def print_report(report: Report) -> None:
    print("INVALID FORMAL BINDING" if report.errors else "VALID FORMAL BINDING")
    if report.errors:
        print("ERRORS")
        for line in report.errors:
            print(f"- {line}")
    for title, lines in (("WARNINGS", report.warnings), ("NOTES", report.notes), ("SUMMARY", report.summary)):
        print(title)
        for line in lines or ["none"]:
            print(f"- {line}")
    print("- note: this checker records correspondence; it is neither a validator nor a proof checker")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check an ERG formal-binding sidecar")
    parser.add_argument("graph", type=Path, help="Path to ERG graph JSON")
    parser.add_argument("binding", type=Path, help="Path to formal-binding JSON")
    parser.add_argument(
        "--formal-repo",
        action="append",
        default=[],
        metavar="OWNER/NAME=DIR",
        help="Local git clone of a formal repository (repeatable)",
    )
    parser.add_argument("--formal-main-ref", help="Require the pinned commit to be contained in this ref")
    parser.add_argument(
        "--require-formal-check",
        action="store_true",
        help="Fail when the binding's formal repository was not checked",
    )
    args = parser.parse_args()

    try:
        repos = parse_repo_mapping(args.formal_repo)
        report = run(args.graph, args.binding, repos, args.formal_main_ref, args.require_formal_check)
    except StructureError as exc:
        print("INVALID FORMAL BINDING")
        print("ERRORS")
        print(f"- {exc}")
        return 1
    print_report(report)
    return 1 if report.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
