# D009-D010 source-check record

status: source-check record / bridge candidate recommended
scope: D009 -> D010 boundary only
candidate boundary: `Submodule.eq_iSup_inf_genEigenspace` -> `Module.End.iSup_genEigenspace_restrict_eq_top`
related scoping note: `docs/hmdg/D009_D010_scoping_note.md`
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`

## Purpose

This document records the source check for the D009 -> D010 boundary.

It does not add C005 to `data/hmdg/concept_patch.json`.

It does not modify the rendered graph.

It does not promote any ConceptBridge, ProofBridge, or RewriteNote to accepted status.

It decides whether the scoped D009 -> D010 boundary should later become a new ConceptBridge candidate, a ProofBridge, a RewriteNote, or a direct theorem wrapper.

## Review metadata

```text
reviewer: GPT-assisted source check
date: 2026-05-26
mathlib source: leanprover-community/mathlib4
mathlib source commit/ref: 75adafcaf8c4a0fcde8e1508f503bed2263ab055
proof file path: Mathlib/LinearAlgebra/Eigenspace/Triangularizable.lean
source declaration checked: yes
target declaration checked: yes
target proof body checked: yes
```

## Candidate boundary

```text
D009 Submodule.eq_iSup_inf_genEigenspace
→ D010 Module.End.iSup_genEigenspace_restrict_eq_top
```

Provisional candidate id from the scoping note:

```text
C005_ambient_inf_to_restricted_genEigenspace
```

Provisional label from the scoping note:

```text
ambient_intersection_to_restricted_eigenspace
```

## Source declaration checked

Declaration:

```text
Submodule.eq_iSup_inf_genEigenspace
```

Observed theorem shape:

```text
p = ⨆ μ, p ⊓ f.genEigenspace μ k
```

Observed hypotheses:

```text
[FiniteDimensional K V]
h  : ∀ x ∈ p, f x ∈ p
h' : ⨆ μ, f.genEigenspace μ k = ⊤
```

Human-facing reading:

```text
If the ambient generalized eigenspaces of f span V, then the invariant submodule p is the supremum of its intersections with those ambient generalized eigenspaces.
```

## Target declaration checked

Declaration:

```text
Module.End.genEigenspace_restrict_eq_top
```

The documentation page also lists this theorem under the target theorem role of:

```text
Module.End.iSup_genEigenspace_restrict_eq_top
```

Observed theorem shape:

```text
⨆ μ, Module.End.genEigenspace (LinearMap.restrict f h) μ k = ⊤
```

Observed hypotheses:

```text
[FiniteDimensional K V]
h  : ∀ x ∈ p, f x ∈ p
h' : ⨆ μ, f.genEigenspace μ k = ⊤
```

Human-facing reading:

```text
If the ambient generalized eigenspaces of f span V, then the generalized eigenspaces of the restricted endomorphism on p span the whole restricted space.
```

## Target proof-body check

Observed proof body:

```text
have := congr_arg (Submodule.comap p.subtype) (Submodule.eq_iSup_inf_genEigenspace k h h')
have h_inj : Function.Injective p.subtype := Subtype.coe_injective
simp_rw [Submodule.inf_genEigenspace f p h, Submodule.comap_subtype_self,
  ← Submodule.map_iSup, Submodule.comap_map_eq_of_injective h_inj] at this
exact this.symm
```

Direct use of D009:

```text
yes: Submodule.eq_iSup_inf_genEigenspace k h h'
```

Main proof operations observed:

```text
1. Apply congr_arg (Submodule.comap p.subtype) to the D009 equality.
2. Use injectivity of p.subtype.
3. Rewrite ambient intersections with generalized eigenspaces into restricted generalized eigenspaces.
4. Rewrite p pulled back along its subtype into top of the restricted space.
5. Use map_iSup/comap_map behavior under injectivity to move the indexed supremum through the subtype/comap context.
6. Symmetrize the resulting equality.
```

## Important rewrite lemmas observed

```text
Submodule.inf_genEigenspace f p h
Submodule.comap_subtype_self
Submodule.map_iSup
Submodule.comap_map_eq_of_injective h_inj
```

The key restriction-transfer lemma appears to be:

```text
Submodule.inf_genEigenspace f p h
```

This is the lemma that connects the ambient intersection form with the generalized eigenspace of the restricted map.

## Human-facing transition

The proof starts from the ambient decomposition:

```text
p = ⨆ μ, p ⊓ f.genEigenspace μ k
```

Then it pulls this equality back along the subtype inclusion:

```text
p.subtype : p -> V
```

The left side becomes top in the restricted space:

```text
Submodule.comap p.subtype p = ⊤
```

The right side is rewritten so that the ambient intersections become restricted generalized eigenspaces:

```text
p ⊓ f.genEigenspace μ k
↔ Module.End.genEigenspace (LinearMap.restrict f h) μ k
```

So the result becomes:

```text
⊤ = ⨆ μ, Module.End.genEigenspace (LinearMap.restrict f h) μ k
```

and the final proof returns the symmetric form:

```text
⨆ μ, Module.End.genEigenspace (LinearMap.restrict f h) μ k = ⊤
```

## Decision

Recommended outcome:

```text
keep_as_C005_candidate_after_review
```

Recommended candidate id:

```text
C005_ambient_inf_to_restricted_genEigenspace
```

Recommended candidate label:

```text
ambient_intersection_to_restricted_eigenspace
```

Recommended bridge question:

```text
How does the ambient equality p = ⨆ μ, p ⊓ f.genEigenspace μ k become a top-supremum equality for the generalized eigenspaces of the restricted endomorphism on p?
```

## Why this is not merely a RewriteNote

Do not treat this as a lightweight RewriteNote only because:

```text
The proof is not a direct one-line rw like R004.
The step changes mathematical context from ambient submodule equality in V to top equality in the restricted subtype/submodule space p.
The proof uses comap along p.subtype and injectivity of the subtype map.
The proof relies on a restriction-transfer lemma for generalized eigenspaces.
The target statement is about the endomorphism LinearMap.restrict f h, not just about intersections inside V.
```

## Why this is still not accepted

Do not mark C005 as accepted because:

```text
This record only checks one target proof body.
The exact graph schema for adding post-R004 bridge nodes has not been updated.
The candidate needs a checklist or direct JSON-change PR before becoming machine-readable.
The relationship between the documentation name Module.End.genEigenspace_restrict_eq_top and the target path name Module.End.iSup_genEigenspace_restrict_eq_top should be handled carefully in labels.
```

## Suggested bridge structure for a later PR

Possible ConceptBridge node:

```text
id: C005_ambient_inf_to_restricted_genEigenspace
type: ConceptBridge
label: ambient_intersection_to_restricted_eigenspace
from_phase: ambient eigenspace decomposition
to_phase: restricted endomorphism decomposition
from_role: eigenspace
to_role: eigenspace/transfer
status: candidate
audit_status: source_checked
```

Possible token tasks:

```text
comap: pull the ambient equality back along p.subtype
subtype: track the inclusion from the restricted space p into V
restrict: change f into LinearMap.restrict f h
inf: rewrite intersection with p
map_iSup: move indexed supremum through map/comap structure
injective: use p.subtype injectivity for comap-map cancellation
genEigenspace: identify ambient and restricted generalized eigenspaces
```

Possible risk:

```text
medium-high
```

Reason:

```text
This is a real context-transfer step. It is smaller than C003 but heavier than R004.
```

## Follow-up options

Recommended next options:

```text
1. Add a C005 review checklist before modifying JSON.
2. Or add C005 as a candidate ConceptBridge to JSON with source_checked audit metadata.
3. If C005 is added to JSON, refresh the rendered graph and keep the node clearly marked as candidate.
```

## Non-goals

This record does not add C005.

This record does not update `data/hmdg/concept_patch.json`.

This record does not update `docs/hmdg/concept_patch_graph.md`.

This record does not claim C005 is accepted.

This record does not claim C001-C003 or R004 are accepted.
