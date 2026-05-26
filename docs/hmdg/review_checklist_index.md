# HMDG review checklist index

status: review navigation index
scope: C001-C003 review checklists

## Purpose

This document is a navigation index for HMDG review work.

It does not accept any ConceptBridge or ProofBridge node.

It does not prove any mathlib theorem.

It defines the order in which the current review checklists should be used.

## Current review targets

```text
C001 kernel_to_criterion
C002 criterion_to_constraint
C003 constraint_to_eigenspace parent bridge
C003a-C003e proof-facing ProofBridge nodes
```

## Review files

| Target | Checklist | Related expansion | Current review focus |
|---|---|---|---|
| C001 `kernel_to_criterion` | `C001_review_checklist.md` | `C001_kernel_to_criterion_expansion.md` | Check whether the kernel/injectivity/disjointness bridge is faithful and whether it should remain one node. |
| C002 `criterion_to_constraint` | `C002_review_checklist.md` | `C002_criterion_to_constraint_expansion.md` | Check whether the disjointness-to-comap/sup/kernel bridge is faithful, especially finite-dimensionality and scalar assumptions. |
| C003 parent + C003a-C003e | `C003_proofbridge_review_checklist.md` | `C003_constraint_to_eigenspace_expansion.md`, `C003_split_plan.md` | Check whether the candidate ProofBridge chain matches the actual Lean proof body. |

## Recommended order

Use this order unless a later issue gives a stronger reason to reorder:

```text
1. C001 review
2. C002 review
3. C003 ProofBridge review
4. Only after these reviews, decide whether C004 or further path expansion is safe
```

Reason:

```text
C001 is the smallest and lowest-risk bridge.
C002 introduces additional theorem-hypothesis and finite-dimensionality risks.
C003 is proof-used but over-compressed and now has proof-facing subbridge candidates.
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
C001 review outcome
C002 review outcome
C003 ProofBridge review outcome
```

This is a trust-calibration stop condition, not a claim that the current graph is wrong.

## Non-goals

This index does not modify `data/hmdg/concept_patch.json`.

This index does not modify rendered graph output.

This index does not promote any node to accepted status.
