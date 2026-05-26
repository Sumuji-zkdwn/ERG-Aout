# HMDG notes

This directory holds HMDG review artifacts that are not yet accepted as stable ERG kernel definitions.

Current machine-readable patch data is stored separately at `data/hmdg/concept_patch.json`.

Current rendered graph:

```text
node_count: 19
edge_count: 32
C001-C003: candidate ConceptBridge nodes
C003a-C003e: candidate ProofBridge nodes
R004: documentation-only RewriteNote, not a JSON node
C005: candidate ConceptBridge with audit_status source_checked
```

## Current concept-patch artifacts

- `concept_patch.md`: candidate concept bridge proposal generated from the original extracted path.
- `concept_patch_graph.md`: Mermaid and typed-edge view of the current candidate bridge graph, including C003 ProofBridge nodes and C005.
- `boundary_expansion.md`: initial generated review tasks for the three compressed boundary edges.
- `C001_kernel_to_criterion_expansion.md`: candidate expansion of Boundary 1.
- `C001_review_checklist.md`: review checklist for C001 before any status change.
- `C001_review_record.md`: first source-check review record for C001.
- `C002_criterion_to_constraint_expansion.md`: candidate expansion of Boundary 2.
- `C002_review_checklist.md`: review checklist for C002 before any status change.
- `C002_review_record.md`: first source-check review record for C002.
- `C003_constraint_to_eigenspace_expansion.md`: candidate high-risk expansion of Boundary 3.
- `C003_split_plan.md`: proposed proof-facing split for over-compressed C003.
- `C003_proofbridge_review_checklist.md`: review checklist for the C003 parent bridge and C003a-C003e ProofBridge nodes.
- `C003_proofbridge_review_record.md`: first proof-body review record for the C003 parent bridge and C003a-C003e ProofBridge nodes.
- `C004_scoping_note.md`: scoping note for the D008 -> D009 boundary before deciding against C004 as a ConceptBridge.
- `C004_source_check_record.md`: source-check record recommending that the scoped C004 boundary be treated as a rewrite note, not a ConceptBridge.
- `R004_global_span_rewrite_to_submodule_equality.md`: lightweight documentation-only rewrite note for the D008 -> D009 global-span step.
- `D009_D010_scoping_note.md`: scoping note for the ambient-to-restricted generalized-eigenspace boundary.
- `D009_D010_source_check_record.md`: source-check record recommending C005 as a candidate ConceptBridge for the ambient-to-restricted boundary.
- `C005_review_checklist.md`: review checklist before adding the ambient-to-restricted C005 candidate to JSON.
- `review_checklist_index.md`: navigation index and current review-state checklist across C001-C003, R004, and C005.
- `concept_bridge_review_summary.md`: status, risk, and next-review summary for C001-C003, R004, and C005.
- `concept_patch_schema_audit_extension.md`: proposed audit metadata schema for parent bridges and proof-facing subbridges.

## Current bridge chain summary

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

## Refreshing the rendered graph

After changing `data/hmdg/concept_patch.json` or the concept-patch renderer, refresh the rendered Markdown artifact from the repository root:

```bash
python prototypes/cognitive_math_graph_v0/render_concept_patch_graph.py \
  --input data/hmdg/concept_patch.json \
  --output docs/hmdg/concept_patch_graph.md
```

The rendered artifact should remain a review aid, not a source of new mathematical claims.

Before opening a generated-artifact PR, check at least:

```text
node_count / edge_count match the JSON
ConceptBridge and ProofBridge nodes remain visually distinguishable
ProofBridge nodes are not described as formal declaration dependencies
Mermaid renders in GitHub without obvious layout or syntax failure
```

## Status caution

No ConceptBridge, ProofBridge, or RewriteNote in this directory is accepted as a stable ERG kernel definition unless a separate accepted-status policy and review record are added.
