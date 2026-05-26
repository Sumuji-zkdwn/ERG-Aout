# HMDG review checklist index

status: review navigation index / C001-C003, R004, and C005 outcomes updated
scope: HMDG review checklists and post-review navigation

## Purpose

This document is a navigation index for HMDG review work.

It does not accept any ConceptBridge, ProofBridge, or RewriteNote node.

It does not prove any mathlib theorem.

It defines the current review state and the next decision point after the C005 candidate addition.

## Current review targets

```text
C001 kernel_to_criterion
C002 criterion_to_constraint
C003 constraint_to_eigenspace parent bridge
C003a-C003e proof-facing ProofBridge nodes
R004 global_span_rewrite_to_submodule_equality documentation-only rewrite note
C005 ambient_intersection_to_restricted_eigenspace candidate ConceptBridge
```

## Current review outcomes

```text
C001 review outcome: keep_candidate_one_node
C002 review outcome: keep_candidate_but_reword
C003 ProofBridge review outcome: keep_candidate_parent_and_subbridges
C004 scoped boundary outcome: record_as_rewrite_note_only
R004 representation: documentation-only RewriteNote
D009-D010 source-check outcome: keep_as_C005_candidate_after_review
C005 checklist outcome: ready_for_candidate_json_pr_after_checklist
C005 JSON status: candidate / source_checked
```

Interpretation:

```text
C001 has been source-checked and remains a one-node candidate ConceptBridge.
C002 has been source-checked and remains a one-node candidate ConceptBridge, but its explanation required rewording to keep target assumptions visible.
C003 has been proof-body checked and remains a high-level parent ConceptBridge with C003a-C003e candidate ProofBridge subnodes.
R004 records the D008 -> D009 global-span rewrite as a documentation-only note, not a JSON ConceptBridge node.
C005 has been source-checked and added to JSON as a candidate ConceptBridge for the ambient-to-restricted generalized-eigenspace transfer.
No C001-C003, C003a-C003e, R004, or C005 item has been promoted to accepted status.
```

## Review files

| Target | Checklist / scoping | Review record | Related expansion / representation | Current status |
|---|---|---|---|---|
| C001 `kernel_to_criterion` | `C001_review_checklist.md` | `C001_review_record.md` | `C001_kernel_to_criterion_expansion.md` | Reviewed; outcome `keep_candidate_one_node`. |
| C002 `criterion_to_constraint` | `C002_review_checklist.md` | `C002_review_record.md` | `C002_criterion_to_constraint_expansion.md` | Reviewed; outcome `keep_candidate_but_reword`; expansion reworded after review. |
| C003 parent + C003a-C003e | `C003_proofbridge_review_checklist.md` | `C003_proofbridge_review_record.md` | `C003_constraint_to_eigenspace_expansion.md`, `C003_split_plan.md` | Proof-body reviewed; outcome `keep_candidate_parent_and_subbridges`. |
| C004 scoped boundary | `C004_scoping_note.md` | `C004_source_check_record.md` | no C004 JSON node | Source-checked; outcome `record_as_rewrite_note_only`. |
| R004 `global_span_rewrite_to_submodule_equality` | no checklist required after C004 source-check | `C004_source_check_record.md` | `R004_global_span_rewrite_to_submodule_equality.md` | Documentation-only RewriteNote; not represented as JSON node. |
| D009-D010 scoped boundary | `D009_D010_scoping_note.md` | `D009_D010_source_check_record.md` | C005 candidate path | Source-checked; outcome `keep_as_C005_candidate_after_review`. |
| C005 `ambient_intersection_to_restricted_eigenspace` | `C005_review_checklist.md` | `D009_D010_source_check_record.md` | `data/hmdg/concept_patch.json`, `concept_patch_graph.md` | Added as candidate ConceptBridge with `audit_status: source_checked`. |

## Review order status

The current review and expansion pass is recorded:

```text
1. C001 review — done; keep_candidate_one_node
2. C002 review — done; keep_candidate_but_reword; explanation reworded
3. C003 ProofBridge review — done; keep_candidate_parent_and_subbridges
4. C004 scoping — done; source check recommended rewrite note only
5. R004 rewrite note — done; documentation-only, no JSON node
6. D009-D010 scoping — done; source check recommended C005 candidate
7. C005 review checklist — done; ready_for_candidate_json_pr_after_checklist
8. C005 JSON candidate addition — done; candidate / source_checked
9. Next decision: run docs/hmdg consistency pass before further graph expansion
```

Reason:

```text
C001 is the smallest and lowest-risk bridge and has passed a source-check review as a one-node candidate.
C002 introduced additional theorem-hypothesis and finite-dimensionality risks; source-check review preserved it as a candidate but required rewording.
C003 is proof-used, over-compressed, and now proof-body reviewed as a parent ConceptBridge plus candidate ProofBridge subnodes.
C004 was scoped and source-checked, but the proof-body transition was a direct rewrite, so it was recorded as R004 instead of a ConceptBridge.
C005 was scoped, source-checked, checklist-reviewed, and then added as a candidate source-checked ConceptBridge because it performs an ambient-to-restricted context transfer.
```

## Review outcome vocabulary

For C001, C002, and C005-style ConceptBridge review, use one of:

```text
keep_candidate_one_node
keep_candidate_but_reword
keep_as_candidate_after_review
ready_for_candidate_json_pr_after_checklist
split_candidate
reject_candidate_bridge
needs_source_check
```

Recorded ConceptBridge outcomes so far:

```text
C001: keep_candidate_one_node
C002: keep_candidate_but_reword
C005: ready_for_candidate_json_pr_after_checklist; added as candidate / source_checked
```

For C003 ProofBridge review, use one of:

```text
keep_candidate_parent_and_subbridges
keep_parent_but_reword_subbridges
merge_some_subbridges
split_more_finely
reject_subbridge_split
needs_source_check
```

Recorded ProofBridge outcome so far:

```text
C003: keep_candidate_parent_and_subbridges
```

For rewrite-note decisions, use one of:

```text
record_as_rewrite_note_only
promote_to_concept_bridge_candidate
merge_into_prior_bridge_explanation
needs_source_check
```

Recorded rewrite-note outcome so far:

```text
C004 scoped boundary: record_as_rewrite_note_only
R004: documentation-only RewriteNote
```

Do not use `accepted` unless a separate accepted-status policy and review record have been added.

## Post-C005 consistency checkpoint

The current post-C005 state is:

```text
C001-C003 reviewed and retained as candidates.
R004 recorded as a rewrite note, not a ConceptBridge.
C005 source-checked and added as a candidate ConceptBridge.
The rendered graph matches the current JSON counts: node_count 19, edge_count 32.
```

Next safe decision:

```text
Search docs/hmdg for stale wording such as C001-C003 only, before C004, or next C004.
Update only navigation/status docs if stale wording is found.
Do not expand the graph again until the documentation state is coherent.
```

This is a trust-calibration checkpoint, not a claim that the current graph is accepted.

## Non-goals

This index does not modify `data/hmdg/concept_patch.json`.

This index does not modify rendered graph output.

This index does not promote any node to accepted status.
