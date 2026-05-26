# HMDG review checklist index

status: review navigation index / C001-C003 outcomes updated
scope: C001-C003 review checklists

## Purpose

This document is a navigation index for HMDG review work.

It does not accept any ConceptBridge or ProofBridge node.

It does not prove any mathlib theorem.

It defines the current review state and the next decision point after the first review pass.

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
C003 ProofBridge review outcome: keep_candidate_parent_and_subbridges
```

Interpretation:

```text
C001 has been source-checked and remains a one-node candidate ConceptBridge.
C002 has been source-checked and remains a one-node candidate ConceptBridge, but its explanation required rewording to keep target assumptions visible.
C003 has been proof-body checked and remains a high-level parent ConceptBridge with C003a-C003e candidate ProofBridge subnodes.
No C001-C003 node has been promoted to accepted status.
```

## Review files

| Target | Checklist | Review record | Related expansion | Current status |
|---|---|---|---|---|
| C001 `kernel_to_criterion` | `C001_review_checklist.md` | `C001_review_record.md` | `C001_kernel_to_criterion_expansion.md` | Reviewed; outcome `keep_candidate_one_node`. |
| C002 `criterion_to_constraint` | `C002_review_checklist.md` | `C002_review_record.md` | `C002_criterion_to_constraint_expansion.md` | Reviewed; outcome `keep_candidate_but_reword`; expansion reworded after review. |
| C003 parent + C003a-C003e | `C003_proofbridge_review_checklist.md` | `C003_proofbridge_review_record.md` | `C003_constraint_to_eigenspace_expansion.md`, `C003_split_plan.md` | Proof-body reviewed; outcome `keep_candidate_parent_and_subbridges`. |

## Review order status

The initial review pass is now recorded:

```text
1. C001 review — done; keep_candidate_one_node
2. C002 review — done; keep_candidate_but_reword; explanation reworded
3. C003 ProofBridge review — done; keep_candidate_parent_and_subbridges
4. Next decision: decide whether C004 or further path expansion is safe
```

Reason:

```text
C001 is the smallest and lowest-risk bridge and has passed a source-check review as a one-node candidate.
C002 introduced additional theorem-hypothesis and finite-dimensionality risks; source-check review preserved it as a candidate but required rewording.
C003 is proof-used, over-compressed, and now proof-body reviewed as a parent ConceptBridge plus candidate ProofBridge subnodes.
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

Recorded outcome so far:

```text
C003: keep_candidate_parent_and_subbridges
```

Do not use `accepted` unless a separate accepted-status policy and review record have been added.

## Stop condition before C004

The first-pass review outcomes are now recorded:

```text
C001 review outcome: recorded
C002 review outcome: recorded
C003 ProofBridge review outcome: recorded
```

Current C004 status:

```text
review_gate_satisfied_but_not_automatic
```

Meaning:

```text
C004 is no longer blocked by missing C001-C003 review records.
However, C004 should still be introduced only by an explicit next-step PR that states its scope, source/target boundary, risk level, and whether it is a ConceptBridge or some other node type.
```

This is a trust-calibration checkpoint, not a claim that the current graph is accepted.

## Non-goals

This index does not modify `data/hmdg/concept_patch.json`.

This index does not modify rendered graph output.

This index does not promote any node to accepted status.
