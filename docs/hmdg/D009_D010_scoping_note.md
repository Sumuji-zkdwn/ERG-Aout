# D009-D010 HMDG scoping note

status: scoping note / no bridge added
scope: D009 -> D010 boundary only
candidate boundary: `Submodule.eq_iSup_inf_genEigenspace` -> `Module.End.iSup_genEigenspace_restrict_eq_top`
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`
related prior note: `docs/hmdg/R004_global_span_rewrite_to_submodule_equality.md`

## Purpose

This document scopes the next unreviewed boundary after R004.

It does not add a new ConceptBridge to `data/hmdg/concept_patch.json`.

It does not add a RewriteNote.

It does not modify the rendered graph.

It records the decision problem before any machine-readable graph change.

## Candidate boundary

```text
D009 Submodule.eq_iSup_inf_genEigenspace
→ D010 Module.End.iSup_genEigenspace_restrict_eq_top
```

The currently scoped issue is not merely a global-span rewrite.

It appears to involve changing viewpoint from:

```text
ambient-space statement about p inside V
```

to:

```text
restricted-endomorphism statement on the subtype/submodule p itself
```

## Source-side reading: D009

Declaration:

```text
Submodule.eq_iSup_inf_genEigenspace
```

Human-facing reading:

```text
If the generalized eigenspaces of f span the whole ambient space V, then an f-invariant submodule p is the supremum of its componentwise intersections with the ambient generalized eigenspaces of f.
```

Shape:

```text
p = ⨆ μ, p ⊓ f.genEigenspace μ k
```

This is still a statement inside the ambient space `V`.

## Target-side reading: D010

Declaration:

```text
Module.End.iSup_genEigenspace_restrict_eq_top
```

Human-facing reading:

```text
If the generalized eigenspaces of f span the whole ambient space, then the generalized eigenspaces of the restriction of f to the invariant submodule p span the whole restricted space p.
```

Expected target shape:

```text
⨆ μ, (f.restrict h).genEigenspace μ k = ⊤
```

where `⊤` is top in the restricted/subtype space associated with `p`, not top in the original ambient space `V`.

## Apparent transition problem

The boundary appears to require identifying or transporting between:

```text
p ⊓ f.genEigenspace μ k
```

and something like:

```text
(f.restrict h).genEigenspace μ k
```

inside the restricted space.

This is a genuine representation shift:

```text
ambient intersection form
→ restricted-map generalized-eigenspace form
```

## Provisional candidate bridge

Possible candidate id:

```text
C005_ambient_inf_to_restricted_genEigenspace
```

Possible label:

```text
ambient_intersection_to_restricted_eigenspace
```

Possible role shift:

```text
eigenspace decomposition in V
→ eigenspace decomposition of f restricted to p
```

Possible bridge question:

```text
How does the equality p = ⨆ μ, p ⊓ f.genEigenspace μ k become a top-supremum statement for the generalized eigenspaces of the restricted endomorphism on p?
```

## Why this should not be added yet

Do not add C005 yet because:

```text
The proof body of D010 has not been checked in this review layer.
The exact theorem/lemma connecting ambient intersections to restricted generalized eigenspaces has not been recorded.
The boundary may be a direct application of an existing restriction lemma rather than a new ConceptBridge.
The target lives in a different lattice/subtype context, so over-simplified wording could be misleading.
```

## Source-check questions

A follow-up source-check record should answer at least:

```text
1. What is the exact proof body of Module.End.iSup_genEigenspace_restrict_eq_top?
2. Does it call Submodule.eq_iSup_inf_genEigenspace directly?
3. Which lemma identifies restricted generalized eigenspaces with ambient intersections?
4. Is the D009 -> D010 step a ConceptBridge, ProofBridge, RewriteNote, or direct theorem wrapper?
5. What assumptions are required for the transfer to the restricted endomorphism?
6. Does the theorem use `map`, `comap`, `subtype`, `codRestrict`, or an extensionality argument?
```

## Risk assessment

Current risk:

```text
medium-to-high
```

Reason:

```text
The step changes mathematical context from an ambient submodule equality to a restricted-endomorphism top equality.
This may be cognitively important, but the exact formal route is unknown until source/proof-body review is recorded.
```

## Current recommendation

Recommended outcome for this PR:

```text
record_scoping_note_only
```

Recommended next PR:

```text
Add a D009-D010 source-check record before adding C005 or any graph node.
```

## Non-goals

This note does not add C005.

This note does not decide whether D009 -> D010 is a ConceptBridge.

This note does not update `data/hmdg/concept_patch.json`.

This note does not update `docs/hmdg/concept_patch_graph.md`.

This note does not claim D010 has been proof-body reviewed.

This note does not accept C001-C003, C003a-C003e, R004, or any future C005 node as stable ERG kernel definitions.
