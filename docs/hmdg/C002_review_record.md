# C002 review record

status: review record / candidate kept with caution
scope: `C002_criterion_to_constraint` only
source boundary: `LinearMap.injective_restrict_iff_disjoint` -> `LinearMap.comap_eq_sup_ker_of_disjoint`
review checklist: `docs/hmdg/C002_review_checklist.md`
related expansion: `docs/hmdg/C002_criterion_to_constraint_expansion.md`

## Purpose

This document records the first source-check review for C002.

It does not accept C002 as a stable ERG kernel definition.

It does not prove `LinearMap.comap_eq_sup_ker_of_disjoint`.

It records whether the current candidate bridge is faithful enough to keep as a candidate one-node HMDG phase bridge, while preserving the risk note about finite-dimensionality and theorem assumptions.

## Review metadata

```text
reviewer: GPT-assisted source check
date: 2026-05-26
mathlib source: mathlib4 docs for Mathlib.Algebra.Module.Submodule.Ker and Mathlib.LinearAlgebra.FiniteDimensional.Basic
source declaration checked: yes
target declaration checked: yes
```

## Source declaration check

Declaration:

```text
LinearMap.injective_restrict_iff_disjoint
```

Observed statement shape:

```text
Function.Injective ⇑(f.restrict hf) ↔ Disjoint p f.ker
```

Relevant hypotheses observed:

```text
R is a Ring
M is an AddCommGroup module over R
p : Submodule R M
f : M →ₗ[R] M
hf : ∀ x ∈ p, f x ∈ p
```

Review judgment:

```text
plain-language source description: faithful
```

Reason:

The source declaration is correctly described as an injectivity criterion for the restricted map in terms of disjointness between the preserved submodule `p` and the original kernel `f.ker`.

## Target declaration check

Declaration:

```text
LinearMap.comap_eq_sup_ker_of_disjoint
```

Observed statement shape:

```text
Submodule.comap f p = p ⊔ f.ker
```

Relevant hypotheses observed:

```text
K is a DivisionRing
V is an AddCommGroup module over K
p : Submodule K V
FiniteDimensional K ↥p
f : V →ₗ[K] V
h : ∀ x ∈ p, f x ∈ p
h' : Disjoint p f.ker
```

Review judgment:

```text
plain-language target description: faithful with caution
```

Reason:

The existing C002 expansion correctly describes the target as a theorem about the full preimage/comap of `p` under `f` being equal to the supremum of `p` and the kernel of `f`.

However, the finite-dimensionality assumption must be represented carefully. The observed declaration assumes:

```text
[FiniteDimensional K ↥p]
```

not necessarily finite-dimensionality of the whole ambient module `V`.

## Finite-dimensionality and scalar assumptions

Review judgment:

```text
finite-dimensionality description: revise slightly / keep caution
base/scalar assumptions represented: needs explicit note
```

Reason:

The expansion note says "over a division ring and for a finite-dimensional submodule p," which is faithful. But later explanation phrases such as "finite-dimensionality supplies dimension/rank control" should be read cautiously unless the proof route is separately reviewed.

The declaration-level fact confirmed here is only:

```text
K is a DivisionRing
p is finite-dimensional as a K-module
```

This review does not verify the internal proof mechanism of the target theorem.

## Bridge granularity check

Current bridge label:

```text
criterion_to_constraint
```

Candidate internal move:

```text
injectivity/disjointness criterion on p
→ disjoint side condition usable in a theorem
→ analyze the preimage/comap of p under f
→ express the preimage as p plus the kernel of f
```

Review judgment:

```text
bridge granularity: keep one node with caution
recommended outcome: keep_candidate_but_reword
```

Reason:

The bridge is mathematically meaningful: the source produces or identifies the disjointness condition, while the target uses that condition as a hypothesis to derive a structural preimage equality.

However, C002 is broader than C001. It changes task type from an injectivity criterion to a preimage decomposition theorem, and it depends on extra assumptions, especially:

```text
DivisionRing K
FiniteDimensional K ↥p
```

Therefore C002 can remain a single HMDG phase-level candidate for now, but the surrounding explanation should avoid implying that the equality follows merely by an obvious dimension argument.

## Review outcome

```text
keep_candidate_but_reword
```

## Recommended wording adjustment

Prefer:

```text
C002 reuses the disjointness side condition from the injectivity criterion as a hypothesis in a finite-dimensional submodule theorem that identifies the full preimage of p as p ⊔ f.ker.
```

Avoid:

```text
Disjointness alone gives the equality.
```

Avoid unless proof-reviewed:

```text
The hard direction is proved by a dimension argument.
```

## Required follow-up

Do not mark C002 as accepted yet.

If C002 is later revised, update `docs/hmdg/C002_criterion_to_constraint_expansion.md` to make the finite-dimensionality and scalar assumptions explicit.

If the repository later adds an accepted-status policy, this review record can be used as supporting evidence only after that wording adjustment is made.

## Non-goals

This review does not update `data/hmdg/concept_patch.json`.

This review does not change the renderer.

This review does not review C001 or C003.

This review does not promote C002 to an accepted ERG kernel definition.
