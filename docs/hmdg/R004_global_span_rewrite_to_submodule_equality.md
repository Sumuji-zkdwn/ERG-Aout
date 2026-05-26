# R004 global-span rewrite note

status: rewrite note / documentation-only
scope: D008 -> D009 boundary after C004 source check
rewrite id: `R004_global_span_rewrite_to_submodule_equality`
source declaration: `Submodule.inf_iSup_genEigenspace`
target declaration: `Submodule.eq_iSup_inf_genEigenspace`
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`
related scoping note: `docs/hmdg/C004_scoping_note.md`
related source-check record: `docs/hmdg/C004_source_check_record.md`

## Purpose

This document records the D008 -> D009 transition as a lightweight rewrite note.

It does not add C004 as a ConceptBridge.

It does not modify `data/hmdg/concept_patch.json`.

It does not modify `docs/hmdg/concept_patch_graph.md`.

It does not promote any ConceptBridge, ProofBridge, or RewriteNote to accepted ERG kernel status.

## Boundary represented

```text
D008 Submodule.inf_iSup_genEigenspace
→ R004 global_span_rewrite_to_submodule_equality
→ D009 Submodule.eq_iSup_inf_genEigenspace
```

## Source theorem shape

```text
p ⊓ ⨆ μ, f.genEigenspace μ k = ⨆ μ, p ⊓ f.genEigenspace μ k
```

Human-facing reading:

```text
The invariant submodule p can be intersected with the indexed supremum of generalized eigenspaces componentwise.
```

## Target theorem shape

```text
p = ⨆ μ, p ⊓ f.genEigenspace μ k
```

Target hypotheses used at this rewrite step:

```text
h  : ∀ x ∈ p, f x ∈ p
h' : ⨆ μ, f.genEigenspace μ k = ⊤
```

Human-facing reading:

```text
If the generalized eigenspaces span the whole ambient space, then p itself is the supremum of its intersections with those generalized eigenspaces.
```

## Proof-body evidence

Observed proof-body shape:

```text
rw [← inf_iSup_genEigenspace h, h', inf_top_eq]
```

Rewrite route:

```text
p
= p ⊓ ⊤
= p ⊓ ⨆ μ, f.genEigenspace μ k
= ⨆ μ, p ⊓ f.genEigenspace μ k
```

## Why this is R004, not C004

This step is mathematically meaningful, but it is not currently treated as a new ConceptBridge.

Reasons:

```text
The transition is a direct rewrite step.
The source and target remain inside the same eigenspace/lattice phase.
The proof-body evidence is the short rewrite sequence using inf_iSup_genEigenspace, h', and inf_top_eq.
The cognitive burden is smaller than C003.
Adding a ConceptBridge node here would over-segment the current graph.
```

## Relation to C003e

C003e explains componentwise reassembly inside `Submodule.inf_iSup_genEigenspace`.

R004 is after that theorem.

It uses the global spanning hypothesis `h'` and the lattice identity `p ⊓ ⊤ = p` to turn the componentwise intersection decomposition into an equality for `p` itself.

So R004 should not be fully merged into C003e, but it also should not be promoted to a full ConceptBridge.

## Current representation policy

Current representation:

```text
RewriteNote: documentation-only
machine-readable JSON node: not added
rendered graph node: not added
accepted ERG kernel definition: no
```

Future option:

```text
If the repository later adds first-class RewriteNote support, R004 can be represented machine-readably as a RewriteNote node distinct from ConceptBridge and ProofBridge nodes.
```

## Non-goals

This document does not prove the target theorem.

This document does not review the remaining D009 -> D010 boundary.

This document does not decide whether rewrite notes should become graph nodes.

This document does not change the status of C001-C003.

This document does not accept C001-C003, C003a-C003e, or R004 as stable ERG kernel definitions.
