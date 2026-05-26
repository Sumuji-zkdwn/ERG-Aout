# HMDG concept bridge review summary

status: candidate review summary / C001-C003, R004, and C005 recorded
scope: C001-C003, R004 documentation note, C005 candidate
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`
related issue: `#68`
related PRs: `#72`, `#73`, `#74`, `#75`, `#76`, `#78`, `#79`, `#80`, `#81`, `#82`, `#83`, `#84`, `#85`, `#86`, `#87`, `#88`, `#89`, `#90`, `#91`, `#92`, `#93`, `#94`

## Purpose

This document summarizes the current HMDG ConceptBridge expansion set produced after the real-graph pipeline, the three initial boundary expansion PRs, the C003 proof-facing subbridge pass, the R004 rewrite-note decision, and the C005 source-checked candidate addition.

It does not promote any candidate bridge to an accepted ERG kernel definition.

It is meant to answer:

```text
What has been expanded?
Which review outcomes have been recorded?
Which bridges remain candidates?
What was decided about R004?
What was added as C005?
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
→ R004 global_span_rewrite_to_submodule_equality
→ D009 Submodule.eq_iSup_inf_genEigenspace
→ C005 ambient_intersection_to_restricted_eigenspace
→ D010 Module.End.iSup_genEigenspace_restrict_eq_top
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

R004 is not currently a machine-readable graph node. It is recorded as a documentation-only rewrite note.

## Current review outcomes

```text
C001 review outcome: keep_candidate_one_node
C002 review outcome: keep_candidate_but_reword
C003 ProofBridge review outcome: keep_candidate_parent_and_subbridges
C004 scoped boundary outcome: record_as_rewrite_note_only
R004 representation: documentation-only RewriteNote
D009-D010 source-check outcome: keep_as_C005_candidate_after_review
C005 checklist outcome: ready_for_candidate_json_pr_after_checklist
C005 JSON status: candidate / source_checked
```

Interpretation:

```text
C001 has been source-checked and remains a one-node candidate ConceptBridge.
C002 has been source-checked and remains a one-node candidate ConceptBridge, but its explanation was reworded to preserve target theorem assumptions.
C003 has been proof-body checked and remains a high-level parent ConceptBridge with C003a-C003e candidate ProofBridge subnodes.
R004 records the D008 -> D009 global-span rewrite, but is not represented as a JSON node.
C005 has been source-checked and added to JSON as a candidate ConceptBridge for the ambient-to-restricted generalized-eigenspace transfer.
No C001-C003, C003a-C003e, R004, or C005 item has been promoted to accepted status.
```

## Artifact index

```text
concept_patch.md
  Candidate ConceptBridge proposal generated from the path.

concept_patch_graph.md
  Mermaid and typed-edge view of the candidate bridge graph, including C003 ProofBridge nodes and C005.

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

C004_scoping_note.md
  Scoping note for D008 -> D009 before deciding against C004 as a ConceptBridge.

C004_source_check_record.md
  Source-check record recommending that the scoped C004 boundary be treated as a rewrite note, not a ConceptBridge.

R004_global_span_rewrite_to_submodule_equality.md
  Documentation-only rewrite note for D008 -> D009.

D009_D010_scoping_note.md
  Scoping note for the ambient-to-restricted generalized-eigenspace boundary.

D009_D010_source_check_record.md
  Source-check record recommending C005 as a candidate ConceptBridge.

C005_review_checklist.md
  Review checklist before adding C005 to JSON.

review_checklist_index.md
  Navigation index and current review outcome index for early bridge review.

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
| R004 `global_span_rewrite_to_submodule_equality` | `Submodule.inf_iSup_genEigenspace` | `Submodule.eq_iSup_inf_genEigenspace` | eigenspace rewrite -> submodule equality | `record_as_rewrite_note_only` | documentation-only RewriteNote / not JSON node | low-medium |
| C005 `ambient_intersection_to_restricted_eigenspace` | `Submodule.eq_iSup_inf_genEigenspace` | `Module.End.iSup_genEigenspace_restrict_eq_top` | ambient eigenspace -> restricted eigenspace | `ready_for_candidate_json_pr_after_checklist` | candidate ConceptBridge / source_checked / added to JSON | medium-high |

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

## R004 review summary

R004 explains the D008 -> D009 transition as a documentation-only rewrite note.

Core transition:

```text
p
= p ⊓ ⊤
= p ⊓ ⨆ μ, f.genEigenspace μ k
= ⨆ μ, p ⊓ f.genEigenspace μ k
```

Observed proof-body result:

```text
rw [← inf_iSup_genEigenspace h, h', inf_top_eq]
```

Review outcome:

```text
record_as_rewrite_note_only
```

Current assessment:

```text
Meaningful for human reading.
Too lightweight to add as a ConceptBridge.
Recorded as documentation-only R004.
Not present in data/hmdg/concept_patch.json.
```

## C005 review summary

C005 explains how an ambient equality for an invariant submodule becomes a top-supremum statement for generalized eigenspaces of the restricted endomorphism.

Core transition:

```text
ambient equality:
p = ⨆ μ, p ⊓ f.genEigenspace μ k

apply comap along p.subtype and rewrite:
Submodule.comap p.subtype p = ⊤
ambient intersections become restricted generalized eigenspaces

restricted equality:
⨆ μ, Module.End.genEigenspace (LinearMap.restrict f h) μ k = ⊤
```

Observed proof-body result:

```text
have := congr_arg (Submodule.comap p.subtype) (Submodule.eq_iSup_inf_genEigenspace k h h')
have h_inj : Function.Injective p.subtype := Subtype.coe_injective
simp_rw [Submodule.inf_genEigenspace f p h, Submodule.comap_subtype_self,
  ← Submodule.map_iSup, Submodule.comap_map_eq_of_injective h_inj] at this
exact this.symm
```

Review outcome:

```text
ready_for_candidate_json_pr_after_checklist
```

Current assessment:

```text
Medium-high-risk candidate HMDG bridge.
Source-check confirmed direct D009 use in the target proof.
C005 has been added to JSON as candidate / source_checked.
Do not mark accepted without a separate accepted-status policy.
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
C005 audit_status: source_checked
C005 status: candidate
C005 proof_use.confirmed: true
C005 used_declaration: Submodule.eq_iSup_inf_genEigenspace
C005 key_transfer_lemma: Submodule.inf_genEigenspace f p h
```

The rendered graph records:

```text
node_count: 19
edge_count: 32
ProofBridge table: present
ConceptBridge audit status / subbridges columns: present
C005 appears in the Mermaid graph, typed adjacency list, and ConceptBridge table.
```

## Overall status

Confirmed project-level status:

```text
The repository contains a real-graph HMDG pipeline.
The repository contains candidate ConceptBridge artifacts for C001-C003 and C005.
The repository contains human-readable expansion notes for C001-C003.
The repository contains review checklists and review records for C001-C003 and C005.
The repository records that C003 is proof-used but over-compressed.
The repository represents C003a-C003e as candidate proof-facing ProofBridge nodes.
The repository records R004 as a documentation-only rewrite note.
The repository renders ConceptBridge and ProofBridge nodes separately.
The repository documents how to refresh the rendered graph.
No candidate bridge has been accepted as a stable ERG kernel definition.
No final theorem explanation has been claimed.
```

## Next decision point

The post-C005 review state is now:

```text
C001-C003 reviewed and retained as candidates.
R004 recorded as a rewrite note, not a ConceptBridge.
C005 source-checked and added as a candidate ConceptBridge.
The rendered graph matches the current JSON counts: node_count 19, edge_count 32.
```

Recommended next step:

```text
Run a consistency pass over docs/hmdg after C005, especially review_checklist_index.md and any wording that still says C001-C003 only.
```

The current priority remains trust calibration, not uncontrolled graph expansion.

## Non-goals

This document does not prove any mathlib theorem.

This document does not modify the accepted ERG schema.

This document does not assert that the generated dependency path is the unique human explanation path.

This document does not resolve whether HMDG should operate at proof-operation granularity or cognitive-phase granularity.

This document does not accept C001-C003, C003a-C003e, R004, or C005 as final ERG kernel definitions.
