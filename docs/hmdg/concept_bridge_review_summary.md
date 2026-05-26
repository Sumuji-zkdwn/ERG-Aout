# HMDG concept bridge review summary

status: candidate review summary
scope: C001-C003 only
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`

## Purpose

This document summarizes the current HMDG ConceptBridge expansion set produced after the real-graph pipeline and the three boundary expansion PRs.

It does not promote any candidate bridge to an accepted ERG kernel definition.

It is meant to answer:

```text
What has been expanded?
Which bridges are relatively safe?
Which bridges are high-risk?
What should be reviewed next?
```

## Current expanded bridge chain

```text
D003 LinearMap.ker_restrict
→ C001 kernel_to_criterion
→ D004 LinearMap.injective_restrict_iff_disjoint
→ C002 criterion_to_constraint
→ D005 LinearMap.comap_eq_sup_ker_of_disjoint
→ ...
→ D007 LinearMap.ker_noncommProd_eq_of_supIndep_ker
→ C003 constraint_to_eigenspace
→ D008 Submodule.inf_iSup_genEigenspace
```

## Artifact index

```text
concept_patch.md
  Candidate ConceptBridge proposal generated from the path.

concept_patch_graph.md
  Mermaid and typed-edge view of the candidate bridge graph.

boundary_expansion.md
  Initial generated review tasks for the three compressed boundary edges.

C001_kernel_to_criterion_expansion.md
  Candidate expansion of Boundary 1.

C002_criterion_to_constraint_expansion.md
  Candidate expansion of Boundary 2.

C003_constraint_to_eigenspace_expansion.md
  Candidate high-risk expansion of Boundary 3.

concept_bridge_review_summary.md
  This overview document.
```

Machine-readable patch data is stored at:

```text
data/hmdg/concept_patch.json
```

## Bridge summary table

| Bridge | Source | Target | Role shift | Current status | Risk |
|---|---|---|---|---|---|
| C001 `kernel_to_criterion` | `LinearMap.ker_restrict` | `LinearMap.injective_restrict_iff_disjoint` | kernel -> criterion | candidate expansion | lower |
| C002 `criterion_to_constraint` | `LinearMap.injective_restrict_iff_disjoint` | `LinearMap.comap_eq_sup_ker_of_disjoint` | criterion -> constraint | candidate expansion | medium |
| C003 `constraint_to_eigenspace` | `LinearMap.ker_noncommProd_eq_of_supIndep_ker` | `Submodule.inf_iSup_genEigenspace` | constraint -> eigenspace | candidate high-risk expansion | high |

## C001 review summary

C001 explains how a statement about the kernel of a restricted linear map becomes an injectivity/disjointness criterion.

Core transition:

```text
kernel of restricted map
→ zero-kernel condition for injectivity
→ no nonzero element in p ∩ ker f
→ disjointness of p and ker f
```

Current assessment:

```text
Relatively safe as a candidate HMDG bridge.
```

Reason:

The source and target declarations are close in mathematical meaning. The human-facing bridge is a standard linear-algebra move: injectivity is detected by trivial kernel, and trivial kernel after restriction is expressed as disjointness from the original kernel.

Main open question:

```text
Should C001 remain one node, or split into:
  kernel_to_zero_kernel
  zero_kernel_to_disjointness
```

Default recommendation:

```text
Keep C001 as one HMDG phase-level node for now.
```

## C002 review summary

C002 explains how an injectivity/disjointness criterion becomes a structural equality involving `comap`, `sup`, and `ker`.

Core transition:

```text
injectivity/disjointness criterion on p
→ disjoint side condition usable in a theorem
→ analyze the preimage/comap of p under f
→ express the preimage as p plus the kernel of f
```

Current assessment:

```text
Moderate-risk candidate HMDG bridge.
```

Reason:

The source is a criterion, while the target is a structural lattice equality. The bridge is plausible because the disjointness condition from C001 becomes a side condition for controlling the preimage of a submodule under a linear map.

Main open question:

```text
Should C002 remain one node, or split into:
  criterion_to_disjoint_side_condition
  disjoint_side_condition_to_comap_sup_ker
```

Additional review issue:

```text
The role of finite-dimensionality must be checked against the actual theorem and proof route.
```

Default recommendation:

```text
Keep C002 as one HMDG phase-level node for readability, but mark the finite-dimensionality explanation as review-required.
```

## C003 review summary

C003 explains how kernel/product/sup-independence constraints begin to connect to generalized eigenspace decomposition.

Core transition:

```text
kernel of product decomposes as sup of kernels
→ kernels of polynomial-like factors behave as spectral components
→ sup-independence controls clean decomposition
→ invariant submodule p can be intersected with the eigenspace supremum componentwise
```

Current assessment:

```text
High-risk candidate HMDG bridge.
```

Reason:

The source and target declarations are much farther apart than in C001 or C002. The source theorem is about kernels of finite products of commuting endomorphisms under `SupIndep` assumptions. The target theorem is about distributing an invariant submodule intersection across an indexed supremum of generalized eigenspaces.

The cognitive bridge is plausible only if the actual proof route uses kernel decompositions as a meaningful path toward generalized eigenspace decompositions.

Main open question:

```text
Is this a genuine human-facing bridge, or mostly a formal dependency artifact?
```

Possible split:

```text
constraint_to_kernel_decomposition
→ kernel_decomposition_to_spectral_components
→ spectral_components_to_invariant_submodule_inf_iSup
```

Default recommendation:

```text
Do not promote C003 beyond candidate status without proof-source review.
```

## Overall status

Confirmed project-level status:

```text
The repository now contains a real-graph HMDG pipeline.
The repository now contains candidate ConceptBridge artifacts for C001-C003.
The repository now contains human-readable expansion notes for C001-C003.
No candidate bridge has been accepted as a stable ERG kernel definition.
No final theorem explanation has been claimed.
```

## Recommended next review order

```text
1. Review C001 for mathematical faithfulness.
2. Review C002 for finite-dimensionality and theorem-hypothesis accuracy.
3. Review C003 against the actual mathlib proof route.
4. Decide whether C003 must be split.
5. Only after that, consider generating C004 or expanding the remaining declaration path.
```

## Stop condition

Do not add new ConceptBridge nodes until at least C003 has been reviewed.

Reason:

```text
Adding more nodes now would increase graph size without increasing trust.
```

The current priority is trust calibration, not graph expansion.

## Non-goals

This document does not prove any mathlib theorem.

This document does not modify the accepted ERG schema.

This document does not assert that the generated dependency path is the unique human explanation path.

This document does not resolve whether HMDG should operate at proof-operation granularity or cognitive-phase granularity.
