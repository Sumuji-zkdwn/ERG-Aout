# HMDG review checklist index

status: review navigation index / C001-C002 outcome updated
scope: C001-C003 review checklists

## Purpose

This document is a navigation index for HMDG review work.

It does not accept any ConceptBridge or ProofBridge node.

It does not prove any mathlib theorem.

It defines the current review state and the order in which remaining review checklists should be used.

## Current review targets

```text
C001 kernel_to_criterion
C002 criterion_to_constraint
C003 constraint_to_eigenspace parent bridge
C003a-C003e proof-facing ProofBridge nodes
```

## Current review outcomes

```text
C001 review outcome: keep_candidate_one_node
C002 review outcome: keep_candidate_but_reword
C003 ProofBridge review outcome: not_yet_reviewed
```

Interpretation:

```text
C001 has been source-checked and remains a one-node candidate ConceptBridge.
C002 has been source-checked and remains a one-node candidate ConceptBridge, but its explanation required rewording to keep target assumptions visible.
C003 and C003a-C003e still require proof-body review before further path expansion.
```

## Review files

| Target | Checklist | Review record | Related expansion | Current status |
|---|---|---|---|---|
| C001 `kernel_to_criterion` | `C001_review_checklist.md` | `C001_review_record.md` | `C001_kernel_to_criterion_expansion.md` | Reviewed; outcome `keep_candidate_one_node`. |
| C002 `criterion_to_constraint` | `C002_review_checklist.md` | `C002_review_record.md` | `C002_criterion_to_constraint_expansion.md` | Reviewed; outcome `keep_candidate_but_reword`; expansion reworded after review. |
| C003 parent + C003a-C003e | `C003_proofbridge_review_checklist.md` | not yet recorded | `C003_constraint_to_eigenspace_expansion.md`, `C003_split_plan.md` | Not yet proof-body reviewed. |

## Recommended order

Use this order unless a later issue gives a stronger reason to reorder:

```text
1. C001 review — done; keep_candidate_one_node
2. C002 review — done; keep_candidate_but_reword; explanation reworded
3. C003 ProofBridge review — next
4. Only after these reviews, decide whether C004 or further path expansion is safe
```

Reason:

```text
C001 is the smallest and lowest-risk bridge and has passed a source-check review as a one-node candidate.
C002 introduced additional theorem-hypothesis and finite-dimensionality risks; source-check review preserved it as a candidate but required rewording.
C003 is proof-used but over-compressed and now has proof-facing subbridge candidates; it still needs proof-body review.
```

## Review outcome vocabulary

For C001 and C002, use one of:

```text
keep_candidate_one_node
keep_candidate_but_reword
split_candidate
reject_candidate_bridge
needs_source_check
```

Recorded outcomes so far:

```text
C001: keep_candidate_one_node
C002: keep_candidate_but_reword
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

Do not use `accepted` unless a separate accepted-status policy and review record have been added.

## Stop condition before C004

Do not generate C004 or expand the remaining declaration path until the following are recorded:

```text
C001 review outcome: recorded
C002 review outcome: recorded
C003 ProofBridge review outcome: not yet recorded
```

Current C004 status:

```text
blocked_by_C003_proof_body_review
```

This is a trust-calibration stop condition, not a claim that the current graph is wrong.

## Non-goals

This index does not modify `data/hmdg/concept_patch.json`.

This index does not modify rendered graph output.

This index does not promote any node to accepted status.
