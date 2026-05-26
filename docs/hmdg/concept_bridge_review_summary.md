# HMDG concept bridge review summary

status: candidate review summary / C003 proof-bridge materialized
scope: C001-C003 only
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`
related issue: `#68`
related PRs: `#72`, `#73`, `#74`, `#75`, `#76`

## Purpose

This document summarizes the current HMDG ConceptBridge expansion set produced after the real-graph pipeline, the three boundary expansion PRs, and the C003 proof-facing subbridge pass.

It does not promote any candidate bridge to an accepted ERG kernel definition.

It is meant to answer:

```text
What has been expanded?
Which bridges are relatively safe?
Which bridges are high-risk?
What was decided about C003?
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

C003 is now also represented as a parent bridge with candidate proof-facing subbridges:

```text
C003 constraint_to_eigenspace
  ├─ C003a iSup_component_extraction
  ├─ C003b product_kernel_isolation
  ├─ C003c kernel_independence_to_injectivity
  ├─ C003d invariant_submodule_surjectivity_transfer
  └─ C003e componentwise_reassembly
```

## Artifact index

```text
concept_patch.md
  Candidate ConceptBridge proposal generated from the path.

concept_patch_graph.md
  Mermaid and typed-edge view of the candidate bridge graph, including C003 ProofBridge nodes.

boundary_expansion.md
  Initial generated review tasks for the three compressed boundary edges.

C001_kernel_to_criterion_expansion.md
  Candidate expansion of Boundary 1.

C002_criterion_to_constraint_expansion.md
  Candidate expansion of Boundary 2.

C003_constraint_to_eigenspace_expansion.md
  Candidate high-risk expansion of Boundary 3, updated after proof-body audit.

C003_split_plan.md
  Proposed proof-facing split for over-compressed C003.

concept_patch_schema_audit_extension.md
  Audit metadata schema plan for parent bridges and proof-facing subbridges.

concept_bridge_review_summary.md
  This overview document.
```

Machine-readable patch data is stored at:

```text
data/hmdg/concept_patch.json
```

The rendered graph can be refreshed from the repository root with:

```bash
python prototypes/cognitive_math_graph_v0/render_concept_patch_graph.py \
  --input data/hmdg/concept_patch.json \
  --output docs/hmdg/concept_patch_graph.md
```

## Bridge summary table

| Bridge | Source | Target | Role shift | Current status | Risk |
|---|---|---|---|---|---|
| C001 `kernel_to_criterion` | `LinearMap.ker_restrict` | `LinearMap.injective_restrict_iff_disjoint` | kernel -> criterion | candidate expansion | lower |
| C002 `criterion_to_constraint` | `LinearMap.injective_restrict_iff_disjoint` | `LinearMap.comap_eq_sup_ker_of_disjoint` | criterion -> constraint | candidate expansion | medium |
| C003 `constraint_to_eigenspace` | `LinearMap.ker_noncommProd_eq_of_supIndep_ker` | `Submodule.inf_iSup_genEigenspace` | constraint -> eigenspace | candidate parent bridge / proof-used / over-compressed / split into candidate ProofBridge nodes | high |

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
Review it for mathematical faithfulness before any accepted-status promotion.
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
High-risk candidate HMDG parent bridge.
Proof-level dependency confirmed.
Over-compression represented explicitly.
Candidate ProofBridge subnodes added, but not accepted.
```

Reason:

The source and target declarations are much farther apart than in C001 or C002. The source theorem is about kernels of finite products of commuting endomorphisms under `SupIndep` assumptions. The target theorem is about distributing an invariant submodule intersection across an indexed supremum of generalized eigenspaces.

Issue `#68` checked the current proof body of `Submodule.inf_iSup_genEigenspace`. The proof does directly use `LinearMap.ker_noncommProd_eq_of_supIndep_ker` while proving injectivity of an auxiliary product map on a selected generalized-eigenspace component.

Therefore the concern is no longer mainly:

```text
Maybe C003 is only a formal dependency artifact.
```

The refined concern is:

```text
C003 is real at proof level, but it compresses too many human-facing moves into one bridge.
```

The current representation keeps two levels separate:

```text
C003 = high-level candidate ConceptBridge parent
C003a-C003e = candidate proof-facing explanatory ProofBridge nodes
```

Proof-facing subbridge set:

```text
C003a iSup_component_extraction
C003b product_kernel_isolation
C003c kernel_independence_to_injectivity
C003d invariant_submodule_surjectivity_transfer
C003e componentwise_reassembly
```

Important limitation:

```text
The split is represented in JSON and rendered Markdown.
The split has not been mathematically accepted as final.
The summaries and proof markers still need review against the Lean proof body.
```

Default recommendation:

```text
Keep C003 as a high-level parent bridge.
Keep C003a-C003e as candidate proof-facing subbridges.
Do not treat C003 as an atomic proof-facing bridge.
Do not add C004 until C003a-C003e have at least one pass of proof-body review.
```

## Current machine-readable state

The machine-readable patch now records:

```text
C003 audit_status: proof_used_but_over_compressed
C003 is_parent_bridge: true
C003 subbridges: [C003a, C003b, C003c, C003d, C003e]
C003a-C003e type: ProofBridge
C003a-C003e layer: proof_facing_explanation
C003a-C003e status: candidate
```

The rendered graph now records:

```text
node_count: 18
edge_count: 29
ProofBridge table: present
ConceptBridge audit status / subbridges columns: present
```

## Overall status

Confirmed project-level status:

```text
The repository now contains a real-graph HMDG pipeline.
The repository now contains candidate ConceptBridge artifacts for C001-C003.
The repository now contains human-readable expansion notes for C001-C003.
The repository now records that C003 is proof-used but over-compressed.
The repository now represents C003a-C003e as candidate proof-facing ProofBridge nodes.
The repository now renders ConceptBridge and ProofBridge nodes separately.
The repository now documents how to refresh the rendered graph.
No candidate bridge has been accepted as a stable ERG kernel definition.
No final theorem explanation has been claimed.
```

## Recommended next review order

```text
1. Review C001 for mathematical faithfulness.
2. Review C002 for finite-dimensionality and theorem-hypothesis accuracy.
3. Review C003a-C003e against the Lean proof body.
4. Only after that, decide whether to generate C004 or expand the remaining declaration path.
```

## Stop condition

Do not add new ConceptBridge nodes until C003a-C003e have at least one proof-body review pass.

Reason:

```text
The graph has enough structure to inspect.
Adding more nodes now would increase graph size before increasing trust.
```

The current priority is trust calibration, not graph expansion.

## Non-goals

This document does not prove any mathlib theorem.

This document does not modify the accepted ERG schema.

This document does not assert that the generated dependency path is the unique human explanation path.

This document does not resolve whether HMDG should operate at proof-operation granularity or cognitive-phase granularity.

This document does not accept C003a-C003e as final proof decomposition nodes.
