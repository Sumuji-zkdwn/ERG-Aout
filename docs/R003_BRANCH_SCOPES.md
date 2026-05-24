# R003 Branch Scopes

Status: operational branch and file-scope assignment for parallel Codex work.

This document assigns branch-name patterns to expected file scopes for unattended R003 Codex runs.

The intent is to make scope drift visible in review and CI.

## 1. Branch naming rule

Use one branch per role and task.

```text
codex/r003-worker-pr-template
codex/r003-worker-runner-output
codex/r003-worker-unattended-guide
codex/r003-critic-audit
codex/r003-integrator-handoff
```

Avoid generic branch names for unattended runs.

## 2. Assigned scopes

| Branch | Role | Expected files |
|---|---|---|
| `codex/r003-worker-pr-template` | Worker | `.github/PULL_REQUEST_TEMPLATE.md` |
| `codex/r003-worker-runner-output` | Worker | `tool/run_r003_automation_checks.py` |
| `codex/r003-worker-unattended-guide` | Worker | `docs/R003_UNATTENDED_OPERATION.md` |
| `codex/r003-critic-audit` | Critic | `docs/R003_AUTOMATION_AUDIT_*.md` |
| `codex/r003-integrator-handoff` | Integrator | `docs/R003_HANDOFF_*.md` |

## 3. Base branch rule

Preferred order:

```text
1. Merge PR #61.
2. Create Worker/Critic/Integrator branches from updated main.
3. Run parallel Codex work.
```

If branches are created before PR #61 is merged, treat them as stacked work from the PR #61 head branch.

## 4. Scope interpretation

A branch is scope-clean when it modifies only the files assigned above.

A branch is scope-drifted when it modifies additional files.

Scope drift does not mean the work is wrong. It means the PR should explain the reason or be split.

## 5. Scope note format

If a PR intentionally touches files outside its assigned scope, the PR body should include:

```text
Scope note: intentional scope expansion
Reason: <why this branch touched additional files>
Risk level: soft-gated
```

Without this note, scope drift should be treated as a review finding.

## 6. Recommended overnight queue

```text
Worker A:
  branch: codex/r003-worker-pr-template
  expected file: .github/PULL_REQUEST_TEMPLATE.md

Worker B:
  branch: codex/r003-worker-runner-output
  expected file: tool/run_r003_automation_checks.py

Worker C:
  branch: codex/r003-worker-unattended-guide
  expected file: docs/R003_UNATTENDED_OPERATION.md

Critic D:
  branch: codex/r003-critic-audit
  expected file pattern: docs/R003_AUTOMATION_AUDIT_*.md

Integrator E:
  branch: codex/r003-integrator-handoff
  expected file pattern: docs/R003_HANDOFF_*.md
```

## 7. Boundary

This file-scope rule is an operational guardrail.

It does not replace R003 Automation Policy.

It does not prove semantic correctness.

It only makes parallel Codex work easier to audit.
