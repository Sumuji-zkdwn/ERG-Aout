# C001 review record

status: review record / candidate kept
scope: `C001_kernel_to_criterion` only
source boundary: `LinearMap.ker_restrict` -> `LinearMap.injective_restrict_iff_disjoint`
review checklist: `docs/hmdg/C001_review_checklist.md`
related expansion: `docs/hmdg/C001_kernel_to_criterion_expansion.md`

## Purpose

This document records the first source-check review for C001.

It does not accept C001 as a stable ERG kernel definition.

It does not prove the final target theorem.

It records whether the current candidate bridge is faithful enough to keep as a candidate one-node HMDG phase bridge.

## Review metadata

```text
reviewer: GPT-assisted source check
date: 2026-05-26
mathlib source: mathlib4 docs for Mathlib.Algebra.Module.Submodule.Ker
mathlib source commit/ref observed from docs source link: 7a3d8788dff5626ff387af2e05ac3fd444f5981b
source declaration checked: yes
target declaration checked: yes
```

## Source declaration check

Declaration:

```text
LinearMap.ker_restrict
```

Observed statement shape:

```text
(f.restrict hf).ker = Submodule.comap p.subtype f.ker
```

Relevant hypotheses observed:

```text
R is a Semiring
M and M₁ are AddCommMonoid modules over R
p : Submodule R M
q : Submodule R M₁
f : M →ₗ[R] M₁
hf : ∀ x ∈ p, f x ∈ q
```

Review judgment:

```text
plain-language source description: faithful
```

Reason:

The existing C001 expansion describes `ker_restrict` as saying that the kernel of the restricted map is obtained by pulling back the original kernel through the restricted domain/subtype. This matches the observed conclusion:

```text
(f.restrict hf).ker = Submodule.comap p.subtype f.ker
```

The phrase "restriction does not invent a new kernel; it filters the original kernel through the restricted domain" is faithful at the HMDG explanation level.

## Target declaration check

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
plain-language target description: faithful
```

Reason:

The existing C001 expansion describes the target declaration as an injectivity criterion for a restricted endomorphism in terms of disjointness between the preserved submodule and the original kernel. This matches the observed conclusion:

```text
Function.Injective ⇑(f.restrict hf) ↔ Disjoint p f.ker
```

## Bridge granularity check

Current bridge label:

```text
kernel_to_criterion
```

Candidate internal move:

```text
kernel of restricted map
→ zero-kernel condition for injectivity
→ no nonzero element in p ∩ ker f
→ disjointness of p and ker f
```

Review judgment:

```text
bridge granularity: keep one node
recommended outcome: keep_candidate_one_node
```

Reason:

The source and target declarations are close in mathematical content. The source computes the kernel of a restricted map by comapping the original kernel through the subtype of `p`. The target packages the zero-kernel condition for the same kind of restricted map as disjointness between `p` and `f.ker`.

The bridge contains multiple proof-level operations, but at the HMDG phase level they form one standard cognitive transition:

```text
kernel computation for a restriction
→ injectivity criterion for the same restriction
```

A split into

```text
kernel_to_zero_kernel
zero_kernel_to_disjointness
```

is possible, but it is not necessary for the current graph level unless future proof-operation granularity is required.

## Review outcome

```text
keep_candidate_one_node
```

## Required follow-up

Do not mark C001 as accepted yet.

If the repository later adds an accepted-status policy, this review record can be used as supporting evidence for C001, but it is not itself an acceptance event.

## Non-goals

This review does not update `data/hmdg/concept_patch.json`.

This review does not change the renderer.

This review does not review C002 or C003.

This review does not promote C001 to an accepted ERG kernel definition.
