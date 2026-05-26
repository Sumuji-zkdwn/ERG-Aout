# C004 scoping note

status: scoping note / no bridge added
scope: possible next boundary after C003
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`
source path data: `data/hmdg/concept_patch.json`

## Purpose

This document scopes the possible C004 step before adding any new ConceptBridge or ProofBridge node.

It does not add C004 to `data/hmdg/concept_patch.json`.

It does not modify the rendered graph.

It does not claim a new accepted ERG kernel definition.

It exists because the first-pass C001-C003 review gate has been satisfied, but C004 is not automatic.

## Current review gate status

The first-pass review outcomes are recorded as:

```text
C001 review outcome: keep_candidate_one_node
C002 review outcome: keep_candidate_but_reword
C003 ProofBridge review outcome: keep_candidate_parent_and_subbridges
```

Current gate state:

```text
review_gate_satisfied_but_not_automatic
```

Meaning:

```text
The repository may now scope the next bridge.
The repository should not add the next bridge without explicitly stating its boundary, role shift, risk, and review requirements.
```

## Candidate C004 boundary

The next unexpanded adjacent declaration boundary in the extracted path is:

```text
D008 Submodule.inf_iSup_genEigenspace
→ D009 Submodule.eq_iSup_inf_genEigenspace
```

Candidate bridge id, if later adopted:

```text
C004_inf_iSup_to_eq_iSup
```

Candidate bridge label, if later adopted:

```text
intersection_distribution_to_submodule_equality
```

This label is provisional.

## Source declaration

```text
Submodule.inf_iSup_genEigenspace
```

Observed role from the path data:

```text
role: eigenspace
tags: eigenspace, lattice_operation
path_index: 8
```

Known theorem shape from the proof file:

```text
p ⊓ ⨆ μ, f.genEigenspace μ k = ⨆ μ, p ⊓ f.genEigenspace μ k
```

Human-facing reading:

```text
Intersecting p with the supremum of generalized eigenspaces can be rewritten as the supremum of the intersections of p with each generalized eigenspace, under the theorem hypotheses.
```

## Target declaration

```text
Submodule.eq_iSup_inf_genEigenspace
```

Observed role from the path data:

```text
role: eigenspace
tags: eigenspace, lattice_operation
path_index: 9
```

Known theorem shape from the proof file:

```text
p = ⨆ μ, p ⊓ f.genEigenspace μ k
```

under hypotheses including:

```text
h : ∀ x ∈ p, f x ∈ p
h' : ⨆ μ, f.genEigenspace μ k = ⊤
```

Human-facing reading:

```text
If all generalized eigenspaces span the whole ambient space, then the invariant submodule p is the supremum of its componentwise intersections with the generalized eigenspaces.
```

## Candidate role shift

C004 would not be a kernel-to-eigenspace bridge like C003.

The likely role shift is internal to the eigenspace/lattice phase:

```text
componentwise intersection decomposition
→ equality for the whole invariant submodule p
```

Possible cognitive transition:

```text
p ⊓ ⨆ μ genEigenspace μ
→ use global spanning hypothesis ⨆ μ genEigenspace μ = ⊤
→ rewrite p ⊓ ⊤ as p
→ conclude p = ⨆ μ, p ⊓ genEigenspace μ
```

## Preliminary risk assessment

Risk level:

```text
low_to_medium
```

Reason:

```text
The source and target declarations are close.
The target proof appears to use the source theorem directly, then rewrites with the global spanning hypothesis and inf_top_eq.
The main risk is not proof-depth but over-labeling a simple rewrite as a new ConceptBridge.
```

Potential reason to add C004:

```text
It records a meaningful phase transition from a decomposition of p ∩ total generalized-eigenspace span to a decomposition of p itself.
```

Potential reason not to add C004:

```text
The boundary may be a direct rewrite step rather than a human-significant ConceptBridge.
It may be better represented as a lightweight rewrite note, not a ConceptBridge node.
```

## Candidate node-type decision

Do not decide yet.

Possible outcomes:

```text
add_C004_as_ConceptBridge
record_as_rewrite_note_only
merge_into_C003e_explanation
needs_source_check
```

Current recommendation:

```text
needs_source_check
```

Reason:

```text
Before adding C004 to JSON, verify the exact current declaration statement and proof body for Submodule.eq_iSup_inf_genEigenspace.
```

## Required source checks before adding C004

Check the current mathlib source for:

```text
Submodule.inf_iSup_genEigenspace
Submodule.eq_iSup_inf_genEigenspace
```

Record:

```text
mathlib commit/ref:
source declaration checked: yes/no
target declaration checked: yes/no
target proof body checked: yes/no
uses Submodule.inf_iSup_genEigenspace directly: yes/no
uses h' : ⨆ μ, f.genEigenspace μ k = ⊤ directly: yes/no
uses inf_top_eq or equivalent rewrite: yes/no
bridge should be ConceptBridge / rewrite note / merge into C003e / uncertain
```

## Non-goals

This note does not add C004.

This note does not update `data/hmdg/concept_patch.json`.

This note does not update `docs/hmdg/concept_patch_graph.md`.

This note does not claim C001-C003 are accepted.

This note does not claim that the remaining path has been explained.
