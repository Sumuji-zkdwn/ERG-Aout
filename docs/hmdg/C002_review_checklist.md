# C002 review checklist

status: candidate review checklist
scope: `C002_criterion_to_constraint` only
source boundary: `LinearMap.injective_restrict_iff_disjoint` -> `LinearMap.comap_eq_sup_ker_of_disjoint`
related artifact: `docs/hmdg/C002_criterion_to_constraint_expansion.md`

## Purpose

This document defines the review procedure for C002 before any status change is considered.

It does not accept C002 as a stable ERG kernel definition.

It does not prove `LinearMap.comap_eq_sup_ker_of_disjoint`.

It is a checklist for deciding whether the existing candidate bridge is mathematically faithful enough to keep as one HMDG phase-level node.

## Current candidate claim

C002 currently claims that the compressed boundary

```text
LinearMap.injective_restrict_iff_disjoint
→ LinearMap.comap_eq_sup_ker_of_disjoint
```

can be read as the human-facing bridge:

```text
criterion_to_constraint
```

The intended cognitive transition is:

```text
injectivity/disjointness criterion on p
→ disjoint side condition usable in a theorem
→ analyze the preimage/comap of p under f
→ express the preimage as p plus the kernel of f
```

## Required source checks

Before changing C002's status, check the current mathlib declarations directly.

### Check 1: source declaration

Verify that `LinearMap.injective_restrict_iff_disjoint` is accurately described as a criterion connecting injectivity of a restricted map with disjointness from the original kernel.

Record:

```text
current declaration name:
current file path:
statement shape:
main hypotheses:
conclusion shape:
restricted map appears: yes/no
Disjoint p (LinearMap.ker f) or equivalent appears: yes/no
plain-language description faithful: yes/no/needs revision
```

### Check 2: target declaration

Verify that `LinearMap.comap_eq_sup_ker_of_disjoint` is accurately described as a theorem about the preimage/comap of a submodule under a linear map being equal to a supremum involving that submodule and the map kernel.

Record:

```text
current declaration name:
current file path:
statement shape:
main hypotheses:
conclusion shape:
uses comap: yes/no
uses sup/join: yes/no
uses LinearMap.ker: yes/no
plain-language description faithful: yes/no/needs revision
```

### Check 3: finite-dimensionality and base-field assumptions

C002 is riskier than C001 because the expansion note currently mentions division ring and finite-dimensionality.

Verify the exact assumptions of `LinearMap.comap_eq_sup_ker_of_disjoint`.

Record:

```text
base scalar assumptions:
module assumptions:
finite-dimensionality assumption present: yes/no
finite-dimensionality applies to p / M / other:
extra assumptions not named in the C002 explanation:
current explanation too strong / too weak / faithful:
```

Warning signs:

```text
The theorem requires assumptions that are not represented in the current C002 bridge.
The finite-dimensionality condition is attached to the wrong object.
The explanation suggests a dimension argument when the proof uses a different route.
The equality direction is described as obvious when it actually requires a nontrivial theorem.
```

## Bridge faithfulness checks

Check whether the transition from the source criterion to the target constraint is a faithful HMDG phase bridge.

Acceptable evidence:

```text
The target theorem uses a disjointness condition that matches the criterion side of C001/C002.
The bridge really changes task type from injectivity criterion to structural preimage equality.
The kernel directions are genuinely responsible for the `sup ker` term.
The target equality can reasonably be explained as controlled by disjointness plus required dimension/hypothesis conditions.
```

Warning signs:

```text
The extracted dependency edge is mostly formal and not a human-meaningful bridge.
The target theorem is better reached from a different nearby theorem than from the injective-restrict criterion.
The bridge label `criterion_to_constraint` hides two separate non-obvious moves.
The finite-dimensionality or scalar assumptions are central enough to require a separate node.
```

## Candidate split decision

The current candidate split is:

```text
criterion_to_disjoint_side_condition
→ disjoint_side_condition_to_comap_sup_ker
```

Use this decision rule:

```text
Keep C002 as one node if the review shows that the main human-facing transition is simply reusing disjointness as a structural side condition.
Split C002 if the move from disjointness to the comap/sup/kernel equality requires a separate theorem-level explanation.
Split C002 if finite-dimensionality or base-field assumptions are central enough that they must be visible as their own bridge.
```

## Review outcomes

Use one of the following review outcomes.

```text
keep_candidate_one_node
keep_candidate_but_reword
split_candidate
reject_candidate_bridge
needs_source_check
```

Do not use `accepted` in this file unless the repository has a separate accepted-status policy for HMDG nodes.

## Minimum review note template

```text
reviewer:
date:
mathlib commit/ref:
source declaration checked: yes/no
target declaration checked: yes/no
plain-language source description: faithful / revise / wrong
plain-language target description: faithful / revise / wrong
finite-dimensionality description: faithful / revise / wrong / not applicable
base/scalar assumptions represented: yes/no/needs revision
bridge granularity: keep one node / split / uncertain
recommended outcome:
notes:
```

## Non-goals

This checklist does not update `data/hmdg/concept_patch.json`.

This checklist does not change the renderer.

This checklist does not review C001 or C003.

This checklist does not promote C002 to an accepted ERG kernel definition.
