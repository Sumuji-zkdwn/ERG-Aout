# C005 review checklist

status: review checklist / no bridge added
scope: proposed C005 only
candidate id: `C005_ambient_inf_to_restricted_genEigenspace`
candidate label: `ambient_intersection_to_restricted_eigenspace`
source boundary: `D009 Submodule.eq_iSup_inf_genEigenspace`
target boundary: `D010 Module.End.iSup_genEigenspace_restrict_eq_top`
related source-check record: `docs/hmdg/D009_D010_source_check_record.md`
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`

## Purpose

This checklist defines the review gate before adding C005 to the machine-readable HMDG graph.

It does not add C005 to `data/hmdg/concept_patch.json`.

It does not modify the rendered graph.

It does not promote C005 or any prior candidate node to accepted ERG kernel status.

## Candidate bridge under review

```text
D009 Submodule.eq_iSup_inf_genEigenspace
→ C005 ambient_intersection_to_restricted_eigenspace
→ D010 Module.End.iSup_genEigenspace_restrict_eq_top
```

Proposed bridge question:

```text
How does the ambient equality p = ⨆ μ, p ⊓ f.genEigenspace μ k become a top-supremum equality for the generalized eigenspaces of the restricted endomorphism on p?
```

## Evidence already recorded

The D009-D010 source-check record observed that the target proof body uses:

```text
have := congr_arg (Submodule.comap p.subtype) (Submodule.eq_iSup_inf_genEigenspace k h h')
have h_inj : Function.Injective p.subtype := Subtype.coe_injective
simp_rw [Submodule.inf_genEigenspace f p h, Submodule.comap_subtype_self,
  ← Submodule.map_iSup, Submodule.comap_map_eq_of_injective h_inj] at this
exact this.symm
```

This confirms that D009 is used directly, and that the proof performs a subtype/comap transfer into the restricted endomorphism context.

## Review questions

Before adding C005 to JSON, answer the following.

### 1. Boundary legitimacy

```text
Does D009 -> D010 represent a genuine cognitive/context transition rather than a purely local rewrite?
```

Current expected answer:

```text
yes
```

Reason:

```text
The step changes from an ambient submodule equality inside V to a top equality inside the restricted/subtype space p.
```

### 2. Source use

```text
Does the target proof directly call D009?
```

Current expected answer:

```text
yes: Submodule.eq_iSup_inf_genEigenspace k h h'
```

### 3. Transfer mechanism

```text
What is the main formal mechanism of the transition?
```

Current expected answer:

```text
Apply Submodule.comap p.subtype to the D009 equality, then rewrite by subtype/comap/map/iSup and restricted-genEigenspace lemmas.
```

### 4. Key restriction lemma

```text
Which lemma connects ambient intersections with restricted generalized eigenspaces?
```

Current expected answer:

```text
Submodule.inf_genEigenspace f p h
```

### 5. Subtype injectivity

```text
Is injectivity of p.subtype used?
```

Current expected answer:

```text
yes: h_inj : Function.Injective p.subtype := Subtype.coe_injective
```

### 6. Risk level

```text
What risk level should C005 have if added?
```

Current expected answer:

```text
medium-high
```

Reason:

```text
The step is smaller than C003 but heavier than R004, because it performs a context transfer between ambient and restricted spaces.
```

### 7. Node type

```text
Should this be represented as ConceptBridge, ProofBridge, RewriteNote, or direct theorem wrapper?
```

Current expected answer:

```text
ConceptBridge candidate
```

Reason:

```text
The step changes the mathematical viewpoint, not merely the surface form of a formula.
```

### 8. Acceptance status

```text
Should C005 be accepted as stable ERG kernel status when added?
```

Current expected answer:

```text
no
```

Reason:

```text
At most, C005 should be added as a candidate source-checked ConceptBridge. Accepted-status policy remains separate.
```

## Required constraints for a future JSON PR

If a later PR adds C005 to `data/hmdg/concept_patch.json`, it should preserve the following constraints.

```text
id: C005_ambient_inf_to_restricted_genEigenspace
type: ConceptBridge
label: ambient_intersection_to_restricted_eigenspace
from_phase: ambient eigenspace decomposition
to_phase: restricted endomorphism decomposition
from_role: eigenspace
to_role: eigenspace
status: candidate
audit_status: source_checked
```

Suggested lost/gained/shared tags:

```text
lost_tags: [lattice_operation]
gained_tags: [transfer]
shared_tags: [eigenspace]
```

Suggested token tasks:

```text
comap: pull the ambient equality back along p.subtype
subtype: track the inclusion from the restricted space p into V
restrict: change f into LinearMap.restrict f h
inf: rewrite intersection with p
map_iSup: move indexed supremum through map/comap structure
injective: use p.subtype injectivity for comap-map cancellation
genEigenspace: identify ambient and restricted generalized eigenspaces
```

Suggested evidence metadata:

```text
proof_file: Mathlib/LinearAlgebra/Eigenspace/Triangularizable.lean
proof_declaration: Module.End.genEigenspace_restrict_eq_top
used_declaration: Submodule.eq_iSup_inf_genEigenspace
key_transfer_lemma: Submodule.inf_genEigenspace f p h
source_check_record: docs/hmdg/D009_D010_source_check_record.md
```

## Stop conditions

Do not add C005 if any of the following become true in a later review:

```text
The proof route is found not to use D009 directly.
The transfer is better represented as a purely local rewrite note.
A more precise existing declaration should be used as the bridge target instead of D010.
The JSON schema cannot represent source-checked ConceptBridge metadata without misleading accepted-status semantics.
```

## Recommended review outcome

Current recommended outcome:

```text
ready_for_candidate_json_pr_after_checklist
```

Meaning:

```text
C005 may be added in a later PR as a candidate ConceptBridge, provided it is marked source-checked and not accepted.
```

## Non-goals

This checklist does not add C005.

This checklist does not update `data/hmdg/concept_patch.json`.

This checklist does not update `docs/hmdg/concept_patch_graph.md`.

This checklist does not decide accepted ERG kernel status.

This checklist does not modify C001-C003, C003a-C003e, or R004.
