# C004 source-check record

status: source-check record / rewrite note recommended
scope: possible C004 boundary only
candidate boundary: `Submodule.inf_iSup_genEigenspace` -> `Submodule.eq_iSup_inf_genEigenspace`
related scoping note: `docs/hmdg/C004_scoping_note.md`
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`

## Purpose

This document records the source check for the possible C004 boundary.

It does not add C004 to `data/hmdg/concept_patch.json`.

It does not modify the rendered graph.

It does not promote any ConceptBridge or ProofBridge to accepted status.

It decides whether the scoped C004 boundary should become a new ConceptBridge candidate, a rewrite note, or be merged into an existing explanation.

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
D008 Submodule.inf_iSup_genEigenspace
→ D009 Submodule.eq_iSup_inf_genEigenspace
```

Provisional candidate id from the scoping note:

```text
C004_inf_iSup_to_eq_iSup
```

Provisional label from the scoping note:

```text
intersection_distribution_to_submodule_equality
```

## Source declaration checked

Declaration:

```text
Submodule.inf_iSup_genEigenspace
```

Observed theorem shape:

```text
p ⊓ ⨆ μ, f.genEigenspace μ k = ⨆ μ, p ⊓ f.genEigenspace μ k
```

Human-facing reading:

```text
The invariant submodule p can be intersected with the indexed supremum of generalized eigenspaces componentwise.
```

## Target declaration checked

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
h : ∀ x ∈ p, f x ∈ p
h' : ⨆ μ, f.genEigenspace μ k = ⊤
```

Human-facing reading:

```text
If the generalized eigenspaces span the whole ambient space, then p is the supremum of its componentwise intersections with those generalized eigenspaces.
```

## Target proof-body check

Observed proof body:

```text
rw [← inf_iSup_genEigenspace h, h', inf_top_eq]
```

This proof uses:

```text
Submodule.inf_iSup_genEigenspace directly: yes
h' : ⨆ μ, f.genEigenspace μ k = ⊤ directly: yes
inf_top_eq or equivalent rewrite: yes
```

The proof route is:

```text
p
= p ⊓ ⊤
= p ⊓ ⨆ μ, f.genEigenspace μ k
= ⨆ μ, p ⊓ f.genEigenspace μ k
```

## Decision

Recommended outcome:

```text
record_as_rewrite_note_only
```

Reason:

The source and target declarations are mathematically close, and the proof body is a direct rewrite using:

```text
← inf_iSup_genEigenspace h
h'
inf_top_eq
```

This is meaningful for human reading, but it does not currently justify adding a new ConceptBridge node to the JSON graph.

The boundary is better documented as a lightweight rewrite step:

```text
componentwise intersection decomposition
+ global spanning hypothesis
+ p ⊓ ⊤ = p
→ equality for p itself
```

## Why not add C004 as a ConceptBridge now

Do not add C004 as a ConceptBridge yet because:

```text
The proof-body transition is a direct three-rewrite step.
The source and target remain in the same eigenspace/lattice phase.
The cognitive burden is much smaller than C003.
Adding a ConceptBridge node here may over-segment a simple theorem application.
```

## Why not merge into C003e entirely

Do not fully merge this into C003e because:

```text
C003e explains reassembly inside Submodule.inf_iSup_genEigenspace.
The D008 -> D009 step additionally uses the global spanning hypothesis h' and inf_top_eq.
This is a distinct rewrite after C003, but not a full new bridge.
```

## Recommended representation

Recommended documentation-level representation:

```text
D008 Submodule.inf_iSup_genEigenspace
→ R004 global_span_rewrite_to_submodule_equality
→ D009 Submodule.eq_iSup_inf_genEigenspace
```

where `R004` is a rewrite note, not a ConceptBridge.

Candidate rewrite-note label:

```text
global_span_rewrite_to_submodule_equality
```

If the repository later adds rewrite-note support, R004 can be represented separately from ConceptBridge and ProofBridge nodes.

## Follow-up options

Recommended next options:

```text
1. Add a lightweight C004 rewrite note document, without changing JSON.
2. Or extend the schema to support RewriteNote nodes before representing R004 machine-readably.
3. Do not add C004 as a ConceptBridge unless a later review decides that rewrite steps should be graph nodes.
```

## Non-goals

This record does not add C004.

This record does not update `data/hmdg/concept_patch.json`.

This record does not update `docs/hmdg/concept_patch_graph.md`.

This record does not claim C001-C003 are accepted.

This record does not claim the remaining D009 -> D010 boundary has been reviewed.
