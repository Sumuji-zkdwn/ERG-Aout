#!/usr/bin/env python3
"""Run conservative R003 automation checks.

This runner is intended for unattended PR checks. It does not generate new
classification content and does not modify repository files. It runs existing
R001/R002 validators and emits a compact automation risk summary based on
changed file paths when git diff information is available.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class CheckResult:
    name: str
    command: List[str]
    returncode: int
    stdout: str
    stderr: str

    @property
    def ok(self) -> bool:
        return self.returncode == 0


def run_command(name: str, command: Sequence[str]) -> CheckResult:
    completed = subprocess.run(
        list(command),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return CheckResult(
        name=name,
        command=list(command),
        returncode=completed.returncode,
        stdout=completed.stdout.strip(),
        stderr=completed.stderr.strip(),
    )


def existing(paths: Iterable[str]) -> List[Path]:
    return [ROOT / path for path in paths if (ROOT / path).exists()]


def graph_jsons() -> List[Path]:
    paths: List[Path] = []
    for folder in [ROOT / "examples" / "r001", ROOT / "examples" / "r002"]:
        if folder.exists():
            paths.extend(sorted(folder.glob("*.json")))
    return paths


def sidecar_pairs() -> List[tuple[Path, Path]]:
    candidates = [
        (
            "examples/r002/larger_manual_conversation_example.json",
            "examples/r002/larger_manual_conversation_raw_text_sidecar.md",
        ),
        (
            "examples/r002/real_log_pilot_01.json",
            "examples/r002/real_log_pilot_01_raw_text_sidecar.md",
        ),
    ]
    pairs: List[tuple[Path, Path]] = []
    for graph, sidecar in candidates:
        graph_path = ROOT / graph
        sidecar_path = ROOT / sidecar
        if graph_path.exists() and sidecar_path.exists():
            pairs.append((graph_path, sidecar_path))
    return pairs


def changed_files(base_ref: Optional[str]) -> List[str]:
    if not base_ref:
        return []
    result = run_command("changed files", ["git", "diff", "--name-only", f"{base_ref}...HEAD"])
    if not result.ok:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def risk_summary(files: Sequence[str]) -> str:
    schema_changed = any(path.startswith("schema/") for path in files)
    validator_changed = any(
        path == "tool/validate_r001_kernel.py" or path.startswith("tool/check_") for path in files
    )
    graph_changed = any(path.startswith("examples/") and path.endswith(".json") for path in files)
    sidecar_changed = any(path.startswith("examples/") and path.endswith("_sidecar.md") for path in files)
    policy_changed = any(path.startswith("docs/R00") or path == "README.md" for path in files)
    unredacted_risk = any("raw_text" in path or "sidecar" in path for path in files)

    if not files:
        risk_level = "unknown (no git diff available)"
    elif schema_changed or validator_changed or graph_changed or policy_changed:
        risk_level = "soft-gated"
    else:
        risk_level = "routine"

    lines = [
        "Automation risk summary:",
        f"- Risk level: {risk_level}",
        f"- Schema changed: {'yes' if schema_changed else 'no'}",
        f"- Validator/checker behavior changed: {'yes' if validator_changed else 'no'}",
        f"- Graph examples changed: {'yes' if graph_changed else 'no'}",
        "- Accepted nodes changed: unknown from path summary; inspect graph diff if graph examples changed",
        "- Main spine changed: unknown from path summary; inspect graph diff if graph examples changed",
        f"- Real-log/raw sidecar changed: {'yes' if sidecar_changed else 'no'}",
        "- New theory claim accepted as established: unknown; inspect docs/graph diff",
        f"- Unredacted source text risk: {'possible' if unredacted_risk else 'not indicated by path summary'}",
        f"- Changed files counted: {len(files)}",
    ]
    if files:
        lines.append("- Changed files:")
        lines.extend(f"  - {path}" for path in files)
    return "\n".join(lines)


def build_checks() -> List[tuple[str, List[str]]]:
    python = sys.executable
    checks: List[tuple[str, List[str]]] = []

    for graph in graph_jsons():
        checks.append((f"validate {graph.relative_to(ROOT)}", [python, "tool/validate_r001_kernel.py", str(graph.relative_to(ROOT))]))

    r002_graphs = existing(
        [
            "examples/r002/larger_manual_conversation_example.json",
            "examples/r002/real_log_pilot_01.json",
            "examples/r001/manual_conversation_to_erg_example.json",
            "examples/r001/manual_conversation_cpr_origin_example.json",
        ]
    )
    for graph in r002_graphs:
        checks.append((
            f"mapping consistency {graph.relative_to(ROOT)}",
            [python, "tool/check_r002_mapping_consistency.py", str(graph.relative_to(ROOT))],
        ))

    for graph, sidecar in sidecar_pairs():
        checks.append((
            f"sidecar consistency {graph.relative_to(ROOT)}",
            [
                python,
                "tool/check_r002_sidecar_consistency.py",
                str(graph.relative_to(ROOT)),
                str(sidecar.relative_to(ROOT)),
            ],
        ))
        checks.append((
            f"candidate review table {graph.relative_to(ROOT)}",
            [
                python,
                "tool/export_r002_candidate_review_table.py",
                str(graph.relative_to(ROOT)),
                "--sidecar",
                str(sidecar.relative_to(ROOT)),
            ],
        ))

    semantics_graph = ROOT / "examples/r001/sample_r001_development_graph.json"
    semantics_doc = ROOT / "docs/R001_SEMANTICS.md"
    coverage_tool = ROOT / "tool/check_r001_semantics_coverage.py"
    if semantics_graph.exists() and semantics_doc.exists() and coverage_tool.exists():
        checks.append((
            "semantics coverage",
            [python, "tool/check_r001_semantics_coverage.py", "examples/r001/sample_r001_development_graph.json", "docs/R001_SEMANTICS.md"],
        ))

    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description="Run R003 unattended automation checks")
    parser.add_argument("--base-ref", default="origin/main", help="Base ref for changed-file risk summary")
    parser.add_argument("--no-diff", action="store_true", help="Skip changed-file risk summary")
    args = parser.parse_args()

    files = [] if args.no_diff else changed_files(args.base_ref)
    print(risk_summary(files))
    print()

    checks = build_checks()
    if not checks:
        print("No checks discovered.")
        return 1

    failed: List[CheckResult] = []
    for name, command in checks:
        result = run_command(name, command)
        status = "PASS" if result.ok else "FAIL"
        print(f"[{status}] {name}")
        print("  $ " + " ".join(command))
        if result.stdout:
            for line in result.stdout.splitlines():
                print(f"  | {line}")
        if result.stderr:
            for line in result.stderr.splitlines():
                print(f"  ! {line}")
        print()
        if not result.ok:
            failed.append(result)

    print("R003 automation check summary:")
    print(f"- checks run: {len(checks)}")
    print(f"- failed: {len(failed)}")

    if failed:
        print("- failed checks:")
        for result in failed:
            print(f"  - {result.name}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
