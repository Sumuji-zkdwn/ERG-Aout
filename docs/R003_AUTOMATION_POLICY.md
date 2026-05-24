# R003 Automation Policy

Status: proposed R003 operating policy.

This document fixes the next operating direction after R002: automate the repetitive work by default, while making over-claiming, privacy leakage, and canonical-spine damage hard to miss.

## 1. Purpose

R003 should not depend on the user watching every classification or mapping step.

R001/R002 already provide a validated graph shape, supplemental consistency checks, sidecar correspondence checks, candidate review tables, and visual/export helpers. R003 should use those mechanisms to let GPT/Codex perform routine work automatically while preserving conservative boundaries.

The goal is not to make automatic semantic judgment fully correct.

The goal is to make automatic runs produce traceable proposals, detectable risk signals, and small reviewable PRs.

## 2. Core interpretation

`accepted` must not be interpreted as truth.

For R003 operation:

```text
accepted = current procedural kernel member
```

This means an accepted node is a node that has passed the current repository procedure for being placed in the kernel layer. It does not mean the user personally certified it as true, final, or theoretically complete.

Similarly:

```text
extends_main = current procedural canonical spine
extends_branch = accepted but non-canonical retained branch
candidate = proposal object before procedural acceptance
unaccepted candidate = retained proposal not yet promoted
```

These are operational statuses, not final semantic guarantees.

## 3. Default automation stance

The default stance is:

```text
Automate routine generation, checking, exporting, and summarization.
Gate only boundary-changing or high-risk effects.
```

The user should not need to monitor every node classification, candidate promotion proposal, label choice, sidecar line, or exported artifact.

Automation is acceptable when the result remains:

- traceable to source nodes or sidecar rows;
- validated by the existing R001 validator where applicable;
- checked by R002 supplemental tools where applicable;
- explicit about uncertainty and non-goals;
- limited to small, reviewable PRs.

## 4. Work that may be automated by default

The following may be performed automatically in normal R003 runs:

- generate candidate mapping proposals from bounded inputs;
- add or update candidate review tables;
- run `tool/validate_r001_kernel.py` on all relevant examples;
- run `tool/check_r002_mapping_consistency.py` on R002/R003 mapping examples;
- run `tool/check_r002_sidecar_consistency.py` when sidecars are present;
- regenerate DOT/PNG or other read-only visual artifacts;
- add documentation that summarizes validator/checker/exporter results;
- update status or handoff documents to list completed artifacts and known caveats;
- create small examples that preserve the existing schema and validator behavior;
- add read-only helper tools that do not alter kernel semantics.

## 5. Work that may be automated but must be isolated in a PR

The following may be generated automatically, but should be isolated in a focused PR with an explicit risk note:

- adding new `L_accepted` nodes;
- extending the `extends_main` spine;
- adding `extends_branch` accepted branches;
- renaming accepted nodes or candidate nodes;
- adding real-log-derived sidecar excerpts;
- adding a new checker or exporter;
- changing documentation that defines R001/R002/R003 boundaries;
- introducing a new edge type in examples;
- changing example graphs used as canonical demonstrations.

The PR body should state:

- what was generated;
- what was validated;
- what was not semantically proven;
- whether any accepted spine or sidecar content changed;
- whether the change is schema-preserving.

## 6. Work that should not be silently automated

The following must not be silently merged into the main kernel path:

- schema changes;
- validator behavior changes;
- reinterpretation of `accepted` as truth or final correctness;
- automatic full conversation ingestion;
- automatic concept extraction treated as authoritative;
- convergence scoring treated as established;
- GIF/DIF, sigma, recency, branch_degree, or semantic importance scoring treated as implemented;
- large unredacted raw log storage;
- private or sensitive source text copied into sidecars without minimization;
- replacing the main spine rather than extending or branching from it.

If automation produces such content, it should be placed in a proposal, draft PR, or explicit deferred note rather than the accepted kernel path.

## 7. Main-spine safety rule

`extends_main` is the most dangerous relation because it defines the current procedural canonical spine.

Automation may propose main-spine extensions, but it should follow a conservative rule:

```text
Only extend the current main spine when the new accepted node is a direct continuation of the current procedural phase.
If there is uncertainty, use branch or candidate instead.
```

The automation should avoid:

- inserting nodes into the middle of the main spine;
- retargeting existing `extends_main` edges;
- moving branch targets onto the main spine;
- using main-spine placement to imply semantic truth.

A main-spine change should be mentioned explicitly in the PR body.

## 8. Accepted-promotion safety rule

Automation may propose candidate-to-accepted promotion.

However, promotion should be conservative:

- every accepted promotion should have an `accepted_from_candidate` path when possible;
- accepted nodes should have source traceability via candidate and raw anchors;
- uncertain claims should remain candidates;
- boundary decisions may be accepted only as procedural decisions, not theoretical proofs;
- if the node introduces new theory, it should first be marked as proposal, branch, or deferred unless the PR is explicitly about accepting that theory.

## 9. Sidecar and privacy safety rule

Sidecar files exist to preserve traceability without changing the graph schema.

Automation may create or update sidecars, but should minimize raw text.

For real-log-derived sidecars:

- prefer short excerpts or summaries;
- mark source as redacted or bounded when appropriate;
- avoid personal, private, or sensitive details unless explicitly required;
- do not store long raw logs by default;
- ensure every `raw_id` exactly matches an `L_raw` node id;
- run the sidecar consistency checker.

## 10. Required automated checks

For any PR touching R001/R002/R003 graph examples or sidecars, run the relevant subset of:

```bash
python tool/validate_r001_kernel.py <graph.json>
python tool/check_r002_mapping_consistency.py <graph.json>
python tool/check_r002_sidecar_consistency.py <graph.json> <sidecar.md>
python tool/export_r002_candidate_review_table.py <graph.json> --sidecar <sidecar.md>
```

If a visual exporter is touched or used:

```bash
python tool/export_r002_visual.py <graph.json> --sidecar <sidecar.md> -o <output.png> --view accepted --label-mode excerpt
```

If optional dependencies are unavailable, the PR body should state that the visual export was not fully generated and report the failure mode.

## 11. Risk labels for PR summaries

Every automation PR should include a compact risk summary:

```text
Automation risk summary:
- Schema changed: yes/no
- Validator behavior changed: yes/no
- Accepted nodes changed: yes/no
- Main spine changed: yes/no
- Real-log sidecar changed: yes/no
- New theory claim accepted: yes/no
- Unredacted source text added: yes/no
- Checks run: ...
- Known uncertainty: ...
```

This is more important than requiring the user to inspect every node.

## 12. User review minimization

The user should only need to inspect PRs when at least one of the following is true:

- schema changed;
- validator behavior changed;
- accepted spine changed;
- a new theory claim was promoted;
- real-log sidecar content expanded;
- automation produced warnings;
- the PR changes the stated scope of R001/R002/R003.

Otherwise, routine generated artifacts may be reviewed primarily through validator/checker output and PR summaries.

## 13. Current boundary

R003 may automate operation around R001/R002 artifacts.

R003 does not yet claim that ERG semantic classification is solved.

R003 does not yet claim reliable automatic memory reconstruction.

R003 does not yet claim convergence, GIF/DIF, sigma, recency, branch_degree, or semantic importance scoring.

R003 is an automation-safety layer around the existing graph workflow.

## 14. Next concrete step

The next concrete implementation step should be a small automation checklist or CI-style runner that executes the existing validators/checkers/exporters and emits the risk summary format above.

That implementation should not change the schema or the accepted semantics.