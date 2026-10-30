# R003 Automation Policy

Status: proposed R003 operating policy.

This document fixes the next operating direction after R002: automate the repetitive work by default, while making over-claiming, privacy leakage, and canonical-spine damage easy to detect.

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
Do not block structural changes merely because they are structural.
Make high-risk effects explicit, isolated, and reversible.
Hard-stop only leakage and false acceptance of unverified theory.
```

The user should not need to monitor every node classification, candidate promotion proposal, label choice, sidecar line, or exported artifact.

Automation is acceptable when the result remains:

- traceable to source nodes or sidecar rows;
- validated by the existing R001 validator where applicable;
- checked by R002 supplemental tools where applicable;
- explicit about uncertainty and non-goals;
- limited to small, reviewable PRs;
- reversible if the proposed structure later proves wrong.

## 4. Risk levels

R003 uses three risk levels.

### 4.1 Routine automation

Routine automation can proceed normally when checks pass and no boundary claim changes.

Examples:

- regenerating tables or visual outputs;
- running validators/checkers;
- adding status summaries;
- adding read-only helper scripts;
- proposing candidate mappings from bounded inputs.

### 4.2 Soft-gated automation

Soft-gated work can still be automated, but should be isolated in a focused PR and made explicit in the PR risk summary.

Soft-gated does not mean prohibited.

Examples:

- schema changes;
- validator behavior changes;
- main-spine extensions;
- main-spine rewrites;
- new edge types;
- new accepted nodes;
- boundary-document changes;
- new automation runners;
- larger mapping examples.

These are not automatically bad. They just change the operating surface and should not be hidden inside unrelated routine work.

### 4.3 Hard stops

The following should be treated as hard stops unless explicitly requested and separately justified:

- private, sensitive, or long unredacted source text added to the repository;
- unverified theory promoted as if it were established accepted kernel truth;
- failed validation/checker results represented as passing;
- hidden destructive rewrite of the existing canonical spine without an explicit PR note.

The purpose of the hard-stop category is narrow: prevent leakage, false certainty, and silent corruption.

## 5. Work that may be automated by default

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

## 6. Work that may be automated but should be isolated in a PR

The following may be generated automatically, but should be isolated in a focused PR with an explicit risk note:

- adding new `L_accepted` nodes;
- extending the `extends_main` spine;
- replacing or retargeting part of the `extends_main` spine;
- adding `extends_branch` accepted branches;
- renaming accepted nodes or candidate nodes;
- adding real-log-derived sidecar excerpts;
- adding a new checker or exporter;
- changing documentation that defines R001/R002/R003 boundaries;
- introducing a new edge type in examples;
- changing example graphs used as canonical demonstrations;
- changing schema or validator behavior.

The PR body should state:

- what was generated;
- what was validated;
- what was not semantically proven;
- whether any accepted spine or sidecar content changed;
- whether schema or validator behavior changed;
- whether the change is reversible.

## 7. Work that should not be silently automated

The following must not be silently merged into the main kernel path:

- reinterpretation of `accepted` as truth or final correctness;
- automatic full conversation ingestion treated as authoritative;
- automatic concept extraction treated as authoritative;
- convergence scoring treated as established;
- GIF/DIF, sigma, recency, branch_degree, or semantic importance scoring treated as implemented;
- large unredacted raw log storage;
- private or sensitive source text copied into sidecars without minimization;
- replacing the main spine while presenting it as a routine extension.

Important distinction:

Schema changes, validator changes, and main-spine changes are not forbidden. They are soft-gated. They may be automated if isolated, described, validated, and made reversible.

If automation produces hard-stop content, it should be placed in a proposal, draft PR, or explicit deferred note rather than the accepted kernel path.

## 8. Main-spine safety rule

`extends_main` defines the current procedural canonical spine, so changes to it should be visible.

Automation may propose main-spine extensions or rewrites.

For routine operation, prefer the conservative rule:

```text
If the new accepted node is a direct continuation of the current procedural phase, extend the spine.
If it is uncertain, exploratory, or competing, use branch or candidate first.
If a rewrite is proposed, isolate it in its own PR and state exactly what edge changed.
```

The automation should avoid:

- hiding insertion into the middle of the main spine;
- hiding retargeted `extends_main` edges;
- moving branch targets onto the main spine without saying so;
- using main-spine placement to imply semantic truth.

A main-spine change should be mentioned explicitly in the PR body.

## 9. Accepted-promotion safety rule

Automation may propose candidate-to-accepted promotion.

Promotion should be procedural, not metaphysical:

- every accepted promotion should have an `accepted_from_candidate` path when possible;
- accepted nodes should have source traceability via candidate and raw anchors;
- uncertain claims may still be promoted as procedural decisions if clearly marked as such;
- boundary decisions may be accepted only as procedural decisions, not theoretical proofs;
- if the node introduces new theory, it should not be described as established unless the PR explicitly justifies that acceptance.

## 10. Sidecar and privacy safety rule

Sidecar files exist to preserve traceability without changing the graph schema.

Automation may create or update sidecars, but should minimize raw text.

For real-log-derived sidecars:

- prefer short excerpts or summaries;
- mark source as redacted or bounded when appropriate;
- avoid personal, private, or sensitive details unless explicitly required;
- do not store long raw logs by default;
- ensure every `raw_id` exactly matches an `L_raw` node id;
- run the sidecar consistency checker.

## 11. Required automated checks

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

For schema or validator changes, add focused positive and negative examples or state why no example change is required.

The R003 runner treats graph JSON files named `invalid_*.json` as negative
fixtures: the R001 validator must report `INVALID` with a diagnostic and exit
with status 1. A valid result, a crash, or another exit status fails the check.
Other graph examples must validate successfully. Run
`python -m unittest discover -s tests -v` to exercise this convention, including
the named invariant for each existing negative fixture.

## 12. Risk labels for PR summaries

Every automation PR should include a compact risk summary:

```text
Automation risk summary:
- Risk level: routine / soft-gated / hard-stop avoided
- Schema changed: yes/no
- Validator behavior changed: yes/no
- Accepted nodes changed: yes/no
- Main spine changed: yes/no
- Real-log sidecar changed: yes/no
- New theory claim accepted as established: yes/no
- Unredacted source text added: yes/no
- Checks run: ...
- Known uncertainty: ...
```

This is more important than requiring the user to inspect every node.

## 13. User review minimization

The user should only need to inspect PRs when at least one of the following is true:

- a hard-stop risk appears;
- schema changed;
- validator behavior changed;
- accepted spine changed;
- a new theory claim was promoted as established;
- real-log sidecar content expanded beyond short excerpts or summaries;
- automation produced warnings;
- the PR changes the stated scope of R001/R002/R003.

Even then, the expected review is not line-by-line classification approval. The expected review is checking the risk summary and deciding whether the automated change should remain routine, be revised, or be split further.

Otherwise, routine generated artifacts may be reviewed primarily through validator/checker output and PR summaries.

## 14. Current boundary

R003 may automate operation around R001/R002 artifacts.

R003 does not yet claim that ERG semantic classification is solved.

R003 does not yet claim reliable automatic memory reconstruction.

R003 does not yet claim convergence, GIF/DIF, sigma, recency, branch_degree, or semantic importance scoring.

R003 is an automation-safety layer around the existing graph workflow.

## 15. Next concrete step

The next concrete implementation step should be a small automation checklist or CI-style runner that executes the existing validators/checkers/exporters and emits the risk summary format above.

That implementation may later grow to handle schema, validator, and main-spine changes automatically, as long as those changes are isolated and reported as soft-gated work.
