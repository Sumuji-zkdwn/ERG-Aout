#!/usr/bin/env python3
"""Check expected file scope for R003 parallel Codex branches.

This is a review aid, not a security boundary. It reports scope drift when a
known branch pattern modifies files outside its assigned scope.
"""

from __future__ import annotations

import argparse
import fnmatch
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class BranchScope:
    branch: str
    role: str
    allowed_patterns: tuple[str, ...]


SCOPES: tuple[BranchScope, ...] = (
    BranchScope("codex/r003-worker-pr-template", "Worker", (".github/PULL_REQUEST_TEMPLATE.md",)),
    BranchScope("codex/r003-worker-runner-output", "Worker", ("tool/run_r003_automation_checks.py",)),
    BranchScope("codex/r003-worker-unattended-guide", "Worker", ("docs/R003_UNATTENDED_OPERATION.md",)),
    BranchScope("codex/r003-critic-audit", "Critic", ("docs/R003_AUTOMATION_AUDIT_*.md",)),
    BranchScope("codex/r003-integrator-handoff", "Integrator", ("docs/R003_HANDOFF_*.md",)),
)


def run(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command),
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def current_branch() -> str:
    env_branch = os.environ.get("GITHUB_HEAD_REF")
    if env_branch:
        return env_branch
    result = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def changed_files(base_ref: str) -> List[str]:
    result = run(["git", "diff", "--name-only", f"{base_ref}...HEAD"])
    if result.returncode != 0:
        print("WARNING: could not compute changed files", file=sys.stderr)
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def match_scope(branch: str) -> BranchScope | None:
    for scope in SCOPES:
        if branch == scope.branch:
            return scope
    return None


def is_allowed(path: str, patterns: Sequence[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def main() -> int:
    parser = argparse.ArgumentParser(description="Check R003 branch file scope")
    parser.add_argument("--base-ref", default="origin/main", help="Base ref for changed files")
    parser.add_argument("--branch", default=None, help="Branch name override")
    args = parser.parse_args()

    branch = args.branch or current_branch()
    files = changed_files(args.base_ref)
    scope = match_scope(branch)

    print("R003 branch scope check")
    print(f"- branch: {branch or '(unknown)'}")
    print(f"- changed files: {len(files)}")

    if not scope:
        print("- scope: unregistered branch pattern")
        print("- result: NOTE")
        print("This branch is not one of the R003 predefined parallel-work branches.")
        return 0

    print(f"- role: {scope.role}")
    print("- expected patterns:")
    for pattern in scope.allowed_patterns:
        print(f"  - {pattern}")

    drifted = [path for path in files if not is_allowed(path, scope.allowed_patterns)]

    if not drifted:
        print("- result: PASS")
        print("All changed files match the assigned branch scope.")
        return 0

    print("- result: FAIL")
    print("Scope drift detected. Split the PR or add a clear scope note in the PR body.")
    print("- out-of-scope files:")
    for path in drifted:
        print(f"  - {path}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
