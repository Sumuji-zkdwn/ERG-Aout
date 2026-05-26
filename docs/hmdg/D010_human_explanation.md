# Human explanation for D010

status: human-facing explanation / not a proof / not accepted ERG kernel status
target declaration: `Module.End.iSup_genEigenspace_restrict_eq_top`
current graph endpoint: `D010`
related graph file: `docs/hmdg/concept_patch_graph.md`
related summary: `docs/hmdg/concept_bridge_review_summary.md`
related source-check record: `docs/hmdg/D009_D010_source_check_record.md`

## Purpose

This document explains the target theorem in ordinary mathematical language.

It is meant to answer:

```text
What is the theorem saying?
Why do D008, D009, R004, and C005 appear near the end?
What does the proof do at a human-readable level?
What is the difference between the ambient-space statement and the restricted-space statement?
```

This document does not prove the theorem formally.

This document does not accept any HMDG node as a stable ERG kernel definition.

This document does not change `data/hmdg/concept_patch.json`.

## One-sentence explanation

If a linear map `f` has enough generalized eigenspaces to span the whole ambient space, then the same kind of generalized-eigenspace spanning statement remains true after restricting `f` to any invariant submodule `p`.

## The mathematical situation

We have an ambient vector space or module:

```text
V
```

We have a linear endomorphism:

```text
f : V -> V
```

We also have a submodule:

```text
p ⊆ V
```

The important assumption is that `p` is invariant under `f`:

```text
if x ∈ p, then f x ∈ p
```

This means that once a vector starts inside `p`, applying `f` does not push it outside `p`.

Because of this, we can restrict `f` to `p` and treat it as a linear endomorphism of `p` itself:

```text
f restricted to p : p -> p
```

In Lean/mathlib notation, this is represented by something like:

```text
LinearMap.restrict f h
```

where `h` is the invariance proof saying that `f` maps `p` into itself.

## What generalized eigenspaces mean here

For a scalar `μ`, the generalized eigenspace of `f` is the collection of vectors that are eventually killed by repeatedly applying:

```text
f - μI
```

In ordinary linear algebra terms, these are the vectors belonging to the generalized eigenvalue component for `μ`.

The theorem starts from the assumption that the generalized eigenspaces of `f` span the whole ambient space:

```text
⨆ μ, f.genEigenspace μ k = ⊤
```

Human-facing reading:

```text
Every vector in V can be built from the generalized eigenspace components of f.
```

## What the target theorem says

The target theorem says that the same spanning property holds inside the invariant submodule `p` after restricting `f` to `p`:

```text
⨆ μ, Module.End.genEigenspace (LinearMap.restrict f h) μ k = ⊤
```

Human-facing reading:

```text
Every vector in p can be built from the generalized eigenspace components of the restricted map f|p.
```

So the theorem is not just about the whole space `V`.

It says that the decomposition survives when we pass to an invariant subspace/submodule.

## Ambient-space view versus restricted-space view

There are two different viewpoints.

The first viewpoint stays inside the ambient space `V`.

It says:

```text
p = ⨆ μ, p ⊓ f.genEigenspace μ k
```

Human-facing reading:

```text
The submodule p is the sum of its intersections with the ambient generalized eigenspaces of f.
```

This is D009:

```text
D009 Submodule.eq_iSup_inf_genEigenspace
```

The second viewpoint treats `p` as its own space.

It says:

```text
⨆ μ, Module.End.genEigenspace (LinearMap.restrict f h) μ k = ⊤
```

Human-facing reading:

```text
Inside p itself, the generalized eigenspaces of the restricted map span all of p.
```

This is D010:

```text
D010 Module.End.iSup_genEigenspace_restrict_eq_top
```

The mathematical content near the end of the proof is the conversion from the first viewpoint to the second viewpoint.

That conversion is what C005 records.

## Why R004 appears before D009

Before reaching D009, the proof uses the fact that the ambient generalized eigenspaces span the whole space:

```text
⨆ μ, f.genEigenspace μ k = ⊤
```

Since `p = p ⊓ ⊤`, we can rewrite:

```text
p
= p ⊓ ⊤
= p ⊓ ⨆ μ, f.genEigenspace μ k
= ⨆ μ, p ⊓ f.genEigenspace μ k
```

This is the D008 -> D009 step.

It was recorded as:

```text
R004 global_span_rewrite_to_submodule_equality
```

It is not treated as a full ConceptBridge, because it is mainly a direct rewrite using the global-spanning hypothesis.

## Why C005 appears between D009 and D010

D009 still talks about `p` as a submodule sitting inside `V`:

```text
p = ⨆ μ, p ⊓ f.genEigenspace μ k
```

D010 talks about the restricted map on `p`:

```text
⨆ μ, Module.End.genEigenspace (LinearMap.restrict f h) μ k = ⊤
```

So the proof must translate:

```text
p ⊓ f.genEigenspace μ k
```

into the corresponding generalized eigenspace of the restricted map:

```text
Module.End.genEigenspace (LinearMap.restrict f h) μ k
```

This is not just a cosmetic rewrite.

It changes the mathematical setting from:

```text
submodule p inside V
```

to:

```text
p as its own ambient space
```

That is why the D009 -> D010 boundary was recorded as:

```text
C005 ambient_intersection_to_restricted_eigenspace
```

## Human-readable proof route

The proof route can be read as follows.

First, use the ambient decomposition result:

```text
p = ⨆ μ, p ⊓ f.genEigenspace μ k
```

Second, pull this equality back along the subtype map:

```text
p.subtype : p -> V
```

This is the map that includes an element of `p` into the original ambient space `V`.

Third, observe that pulling `p` back along its own inclusion gives the whole restricted space:

```text
Submodule.comap p.subtype p = ⊤
```

Human-facing reading:

```text
Every element of p, viewed as an element of p, lies in p.
```

Fourth, rewrite each ambient intersection:

```text
p ⊓ f.genEigenspace μ k
```

as the corresponding generalized eigenspace for the restricted map:

```text
Module.End.genEigenspace (LinearMap.restrict f h) μ k
```

Fifth, after this conversion, the equality says:

```text
⊤ = ⨆ μ, Module.End.genEigenspace (LinearMap.restrict f h) μ k
```

Finally, reverse the equality to get the target statement:

```text
⨆ μ, Module.End.genEigenspace (LinearMap.restrict f h) μ k = ⊤
```

## Correspondence with the checked proof body

The source-check record observed the proof shape:

```text
have := congr_arg (Submodule.comap p.subtype) (Submodule.eq_iSup_inf_genEigenspace k h h')
have h_inj : Function.Injective p.subtype := Subtype.coe_injective
simp_rw [Submodule.inf_genEigenspace f p h, Submodule.comap_subtype_self,
  ← Submodule.map_iSup, Submodule.comap_map_eq_of_injective h_inj] at this
exact this.symm
```

Human-facing reading of each line:

```text
1. Take the D009 equality and apply comap along p.subtype.
2. Record that the subtype inclusion p -> V is injective.
3. Rewrite ambient intersections as restricted generalized eigenspaces.
4. Rewrite the left side as top in the restricted space.
5. Move the indexed supremum through the map/comap structure.
6. Reverse the equality to match the target theorem statement.
```

The key transfer lemma recorded for this boundary is:

```text
Submodule.inf_genEigenspace f p h
```

This is the lemma that makes the phrase:

```text
ambient intersection with p
```

match the phrase:

```text
generalized eigenspace of the restricted map
```

## How the HMDG nodes should be read

The current human explanation chain is:

```text
D003 -> C001 -> D004 -> C002 -> D005 -> ... -> D007 -> C003 -> D008 -> R004 -> D009 -> C005 -> D010
```

Reading:

```text
D003-D005 region:
  kernel, restriction, injectivity, disjointness, and comap/sup constraints.

C003 region:
  the difficult bridge from kernel/product/sup-independence constraints to generalized eigenspace decomposition.

D008:
  componentwise intersection of p with the supremum of generalized eigenspaces.

R004:
  use the global-spanning hypothesis to rewrite p as the sum of these componentwise intersections.

D009:
  p equals the supremum of p ∩ ambient generalized eigenspaces.

C005:
  convert the ambient intersection statement into a restricted-endomorphism statement.

D010:
  the generalized eigenspaces of the restricted map span the whole restricted space.
```

## Why this theorem matters conceptually

The theorem says that generalized-eigenspace decomposability is stable under invariant submodules.

Informally:

```text
If the whole system can be decomposed into generalized eigen-components,
then any part of the system that is closed under the dynamics also decomposes in the same way internally.
```

The important phrase is:

```text
closed under the dynamics
```

This is exactly the invariance assumption:

```text
x ∈ p -> f x ∈ p
```

Without that assumption, the restricted map would not even be a well-defined endomorphism of `p`.

## What this explanation does not claim

This explanation does not claim that the HMDG path is the unique human explanation of the theorem.

This explanation does not claim that C001, C002, C003, C003a-C003e, R004, or C005 are accepted ERG kernel definitions.

This explanation does not replace the Lean proof.

This explanation does not claim that R004 is a JSON node.

This explanation does not claim that C005 is accepted; C005 is only a source-checked candidate ConceptBridge.

## Short version for future recall

```text
The target theorem says that if f's generalized eigenspaces span V, then the generalized eigenspaces of f restricted to any f-invariant submodule p span p. D009 first expresses p as the sum of p's intersections with the ambient generalized eigenspaces. C005 then transports this ambient intersection statement along p.subtype and rewrites it as a statement about generalized eigenspaces of the restricted endomorphism.
```
