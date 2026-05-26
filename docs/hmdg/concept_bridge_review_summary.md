# HMDG concept bridge review summary

status: candidate review summary / first C001-C003 review pass recorded
scope: C001-C003 only
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`
related issue: `#68`
related PRs: `#72`, `#73`, `#74`, `#75`, `#76`, `#78`, `#79`, `#80`, `#81`, `#82`, `#83`, `#84`, `#85`, `#86`

## Purpose

This document summarizes the current HMDG ConceptBridge expansion set produced after the real-graph pipeline, the three boundary expansion PRs, the C003 proof-facing subbridge pass, and the first C001-C003 review pass.

It does not promote any candidate bridge to an accepted ERG kernel definition.

It is meant to answer:

```text
What has been expanded?
Which review outcomes have been recorded?
Which bridges remain candidates?
What was decided about C003?
What is the next safe decision point?
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

C003 is also represented as a parent bridge with candidate proof-facing subbridges:

```text
C003 constraint_to_eigenspace
  ├─ C003a iSup_component_extraction
  ├─ C003b product_kernel_isolation
  ├─ C003c kernel_independence_to_injectivity
  ├─ C003d invariant_submodule_surjectivity_transfer
  └─ C003e componentwise_reassembly
```

## Current review outcomes

```text
C001 review outcome: keep_candidate_one_node
C002 review outcome: keep_candidate_but_reword
C003 ProofBridge review outcome: keep_candidate_parent_and_subbridges
```

Interpretation:

```text
C001 has been source-checked and remains a one-node candidate ConceptBridge.
C002 has been source-checked and remains a one-node candidate ConceptBridge, but its explanation was reworded to preserve target theorem assumptions.
C003 has been proof-body checked and remains a high-level parent ConceptBridge with C003a-C003e candidate ProofBridge subnodes.
No C001-C003 node has been promoted to accepted status.
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

C001_review_checklist.md
  Review checklist for C001 before any status change.

C001_review_record.md
  First source-check review record for C001.

C002_criterion_to_constraint_expansion.md
  Candidate expansion of Boundary 2, reworded after source-check review.

C002_review_checklist.md
  Review checklist for C002 before any status change.

C002_review_record.md
  First source-check review record for C002.

C003_constraint_to_eigenspace_expansion.md
  Candidate high-risk expansion of Boundary 3.

C003_split_plan.md
  Proposed proof-facing split for over-compressed C003.

C003_proofbridge_review_checklist.md
  Review checklist for the C003 parent bridge and C003a-C003e ProofBridge nodes.

C003_proofbridge_review_record.md
  First proof-body review record for the C003 parent bridge and C003a-C003e ProofBridge nodes.

review_checklist_index.md
  Navigation index and current review outcome index for C001-C003.

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

| Bridge | Source | Target | Role shift | Review outcome | Current status | Risk |
|---|---|---|---|---|---|---|
| C001 `kernel_to_criterion` | `LinearMap.ker_restrict` | `LinearMap.injective_restrict_iff_disjoint` | kernel -> criterion | `keep_candidate_one_node` | candidate ConceptBridge / source-checked | lower |
| C002 `criterion_to_constraint` | `LinearMap.injective_restrict_iff_disjoint` | `LinearMap.comap_eq_sup_ker_of_disjoint` | criterion -> constraint | `keep_candidate_but_reword` | candidate ConceptBridge / source-checked / expansion reworded | medium |
| C003 `constraint_to_eigenspace` | `LinearMap.ker_noncommProd_eq_of_supIndep_ker` | `Submodule.inf_iSup_genEigenspace` | constraint -> eigenspace | `keep_candidate_parent_and_subbridges` | candidate parent ConceptBridge / proof-body checked / has candidate ProofBridge subnodes | high |

## C001 review summary

C001 explains how a statement about the kernel of a restricted linear map becomes an injectivity/disjointness criterion.

Core transition:

```text
kernel of restricted map
→ zero-kernel condition for injectivity
→ no nonzero element in p ∩ ker f
→ disjointness of p and ker f
```

Observed source-check result:

```text
LinearMap.ker_restrict:
(f.restrict hf).ker = Submodule.comap p.subtype f.ker

LinearMap.injective_restrict_iff_disjoint:
Function.Injective ⇑(f.restrict hf) ↔ Disjoint p f.ker
```

Review outcome:

```text
keep_candidate_one_node
```

Current assessment:

```text
Relatively safe as a candidate HMDG bridge.
Keep as one HMDG phase-level candidate for now.
Do not mark accepted without a separate accepted-status policy.
```

## C002 review summary

C002 explains how an injectivity/disjointness criterion becomes a structural equality involving `comap`, `sup`, and `ker`.

Core transition:

```text
injectivity/disjointness criterion on p
→ disjoint side condition usable as a theorem hypothesis
→ finite-dimensional submodule theorem about the preimage/comap of p under f
→ express that preimage as p plus the kernel of f
```

Observed source-check result:

```text
LinearMap.injective_restrict_iff_disjoint:
Function.Injective ⇑(f.restrict hf) ↔ Disjoint p f.ker

LinearMap.comap_eq_sup_ker_of_disjoint:
Submodule.comap f p = p ⊔ f.ker
```

Important target assumptions observed:

```text
K is a DivisionRing
[FiniteDimensional K ↥p]
f maps p into p
Disjoint p f.ker
```

Review outcome:

```text
keep_candidate_but_reword
```

Current assessment:

```text
Moderate-risk candidate HMDG bridge.
Keep as one HMDG phase-level candidate for now.
Preserve the target theorem assumptions explicitly.
Do not imply that disjointness alone gives the equality.
```

The C002 expansion has been reworded after review to avoid overclaiming a proof mechanism.

## C003 review summary

C003 explains how kernel/product/sup-independence constraints connect to generalized eigenspace decomposition in the proof of `Submodule.inf_iSup_genEigenspace`.

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
Candidate ProofBridge subnodes added and first proof-body review recorded.
Still not accepted as a stable ERG kernel definition.
```

The proof body of `Submodule.inf_iSup_genEigenspace` was checked against:

```text
Mathlib/LinearAlgebra/Eigenspace/Triangularizable.lean
mathlib4 ref: 75adafcaf8c4a0fcde8e1508f503bed2263ab055
```

The source theorem occurrence is confirmed inside the C003c region:

```text
LinearMap.ker_noncommProd_eq_of_supIndep_ker
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

Review outcome:

```text
keep_candidate_parent_and_subbridges
```

Minor wording caution:

```text
C003d should describe finite-dimensional transfer as mediated through LinearMap.injOn_iff_surjOn in the existing theorem context, rather than as a separate explicit dimension calculation at that line.
```

## Current machine-readable state

The machine-readable patch records:

```text
C003 audit_status: proof_used_but_over_compressed
C003 is_parent_bridge: true
C003 subbridges: [C003a, C003b, C003c, C003d, C003e]
C003a-C003e type: ProofBridge
C003a-C003e layer: proof_facing_explanation
C003a-C003e status: candidate
```

The rendered graph records:

```text
node_count: 18
edge_count: 29
ProofBridge table: present
ConceptBridge audit status / subbridges columns: present
```

## Overall status

Confirmed project-level status:

```text
The repository contains a real-graph HMDG pipeline.
The repository contains candidate ConceptBridge artifacts for C001-C003.
The repository contains human-readable expansion notes for C001-C003.
The repository contains review checklists and review records for C001-C003.
The repository records that C003 is proof-used but over-compressed.
The repository represents C003a-C003e as candidate proof-facing ProofBridge nodes.
The repository renders ConceptBridge and ProofBridge nodes separately.
The repository documents how to refresh the rendered graph.
No candidate bridge has been accepted as a stable ERG kernel definition.
No final theorem explanation has been claimed.
```

## Next decision point

The first-pass review gate is now satisfied:

```text
C001 review outcome: recorded
C002 review outcome: recorded
C003 ProofBridge review outcome: recorded
```

Current C004 status:

```text
review_gate_satisfied_but_not_automatic
```

Meaning:

```text
C004 is no longer blocked by missing C001-C003 review records.
However, C004 should still be introduced only by an explicit next-step PR that states its scope, source/target boundary, risk level, and whether it is a ConceptBridge or some other node type.
```

Recommended next step:

```text
Create a C004 scoping note before adding any new ConceptBridge node.
```

The current priority remains trust calibration, not uncontrolled graph expansion.

## Non-goals

This document does not prove any mathlib theorem.

This document does not modify the accepted ERG schema.

This document does not assert that the generated dependency path is the unique human explanation path.

This document does not resolve whether HMDG should operate at proof-operation granularity or cognitive-phase granularity.

This document does not accept C001-C003 or C003a-C003e as final ERG kernel definitions.
