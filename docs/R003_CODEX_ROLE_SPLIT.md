# R003 Codex Role Split

Status: proposed unattended-operation role model.

This document defines how to run multiple Codex tasks in parallel without treating every task as an unrestricted implementer.

The goal is to reproduce the useful pattern observed in the GPT/Codex workflow: Codex can generate and modify quickly, while a separate role suppresses over-claiming, leakage, hidden scope expansion, and unreviewed canonical-spine changes.

## 1. Core idea

Do not run all Codex agents with the same role.

Use at least three roles:

```text
Worker   = produces a small scoped change
Critic   = audits Worker PRs and looks for risk
Integrator = reconciles passed PRs and keeps queue/order clean
```

Optional role:

```text
Archivist = summarizes completed PRs into status/handoff notes
```

The Worker role may edit files.

The Critic role should usually avoid editing implementation files. It should review, comment, or create a follow-up note.

The Integrator role should prefer documentation, ordering, conflict resolution, and status updates rather than new theory.

## 2. Role permissions

## 2.1 Worker

Worker may:

- implement one assigned task;
- create or update one focused PR;
- add tests/checks relevant to that task;
- update directly related docs;
- run `tool/run_r003_automation_checks.py`.

Worker must not:

- broaden the task scope;
- merge unrelated cleanup;
- promote unverified theory as established;
- add unredacted raw logs;
- silently rewrite `extends_main`;
- modify schema/validator/main-spine in the same PR as unrelated routine work.

## 2.2 Critic

Critic may:

- inspect Worker PRs;
- compare changes against `docs/R003_AUTOMATION_POLICY.md`;
- check the Automation risk summary;
- identify leakage, over-claiming, hidden spine edits, and failed checks;
- request split PRs when scope is mixed;
- leave review comments or create a short audit document.

Critic must not:

- rewrite the Worker PR into a different feature;
- add new theory while reviewing;
- silently fix risky changes without recording the risk;
- treat style preferences as correctness failures unless readability blocks review.

## 2.3 Integrator

Integrator may:

- order PRs by dependency;
- resolve documentation conflicts;
- update status/handoff docs after PRs pass;
- identify which PRs should be merged first;
- mark blocked PRs and explain why.

Integrator must not:

- bypass hard-stop risks;
- collapse multiple soft-gated changes into one unreviewable PR;
- convert a Critic warning into accepted theory without a separate focused PR.

## 2.4 Archivist

Archivist may:

- summarize merged PRs;
- update status documents;
- maintain a timeline of what changed;
- record known caveats and deferred work.

Archivist must not:

- add new semantics;
- reinterpret accepted nodes as truth;
- rewrite source history.

## 3. Parallel overnight pattern

A safe overnight run should use separate tasks and non-overlapping file scopes.

Example:

```text
Task W1: Worker improves runner output readability only.
Task W2: Worker adds PR template for Automation risk summary only.
Task W3: Worker adds unattended operation guide only.
Task C1: Critic audits all open Worker PRs against R003 policy.
Task I1: Integrator summarizes merge order and conflicts after Workers finish.
```

Do not assign two Workers to the same file unless the task is explicitly conflict resolution.

## 4. File-scope separation

Prefer this mapping:

```text
Worker A: tool/run_r003_automation_checks.py only
Worker B: .github/PULL_REQUEST_TEMPLATE.md only
Worker C: docs/R003_UNATTENDED_OPERATION.md only
Worker D: docs/status or handoff docs only
Critic: comments / audit docs only
Integrator: README + status references only, after Workers finish
```

Avoid parallel edits to:

- `README.md`;
- `docs/R003_AUTOMATION_POLICY.md`;
- `schema/r001_graph.schema.json`;
- `tool/validate_r001_kernel.py`;
- graph JSON examples;
- real-log sidecars.

If these must change, isolate them as soft-gated PRs.

## 5. Worker prompt template

```text
Follow docs/R003_AUTOMATION_POLICY.md and docs/R003_CODEX_ROLE_SPLIT.md.

Role: Worker.
Assigned scope: <one narrow task>.
Allowed files: <explicit file list>.
Do not modify files outside the allowed list.

Create one focused PR.
Run:
python tool/run_r003_automation_checks.py --base-ref origin/main

Include an Automation risk summary in the PR body.
Hard-stop only leakage, unverified theory promoted as established truth, failed checks represented as passing, or hidden destructive canonical-spine rewrites.
If the task requires touching schema, validator, main spine, or real-log sidecar content, stop and convert the work into a soft-gated proposal PR instead.
```

## 6. Critic prompt template

```text
Follow docs/R003_AUTOMATION_POLICY.md and docs/R003_CODEX_ROLE_SPLIT.md.

Role: Critic.
Do not implement new features.
Audit the specified PR(s) only.

Check:
- Does the PR exceed its assigned scope?
- Does it contain leakage or excessive raw text?
- Does it promote unverified theory as established?
- Does it hide schema, validator, accepted-node, or main-spine changes?
- Does it represent failed checks as passing?
- Is the Automation risk summary accurate?
- Should the PR be split?

Output either:
- APPROVE WITH NOTES, or
- REQUEST CHANGES, with concrete reasons.

Do not add new semantics while reviewing.
```

## 7. Integrator prompt template

```text
Follow docs/R003_AUTOMATION_POLICY.md and docs/R003_CODEX_ROLE_SPLIT.md.

Role: Integrator.
Inspect the current open PRs.
Do not implement new features unless necessary for conflict resolution.

Produce:
1. recommended merge order;
2. blocked PRs and why;
3. conflicts or overlapping file scopes;
4. PRs that need Critic review;
5. status/handoff doc updates needed after merge.

If you edit files, keep the PR documentation-only and include an Automation risk summary.
```

## 8. Overnight queue example

Use this queue when unattended:

```text
Queue 1 / Worker:
Add .github/PULL_REQUEST_TEMPLATE.md with Automation risk summary fields.
Allowed files: .github/PULL_REQUEST_TEMPLATE.md only.

Queue 2 / Worker:
Improve tool/run_r003_automation_checks.py output readability without changing check semantics.
Allowed files: tool/run_r003_automation_checks.py only.

Queue 3 / Worker:
Add docs/R003_UNATTENDED_OPERATION.md explaining overnight Codex operation.
Allowed files: docs/R003_UNATTENDED_OPERATION.md only.

Queue 4 / Critic:
Audit all open PRs created by Queue 1-3 against R003 policy and role split.
Allowed action: comments or docs/R003_AUTOMATION_AUDIT_<date>.md only.

Queue 5 / Integrator:
After Queue 1-4, summarize merge order and conflicts.
Allowed action: comment or docs/R003_HANDOFF_<date>.md only.
```

## 9. Suppression rule

The Critic does not need to prove the Worker is wrong.

The Critic only needs to prove that the PR is not safely reviewable under the current operating policy.

Suppress or request changes when:

- the scope is too broad;
- the risk summary is inaccurate;
- hard-stop content appears;
- checks were skipped without explanation;
- a soft-gated change is hidden inside routine work;
- the PR makes the repository look more certain than it is.

## 10. Current boundary

This role split is an operating discipline.

It does not claim that Codex can solve ERG semantic classification.

It does not claim that Critic review is mathematically complete.

It is a practical way to make parallel automation less likely to over-claim, leak, or silently damage the procedural spine.
