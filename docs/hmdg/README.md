# HMDG notes

This directory holds HMDG review artifacts that are not yet accepted as stable ERG kernel definitions.

Current concept-patch artifacts:

- `concept_patch.md`: candidate concept bridge proposal.
- `concept_patch_graph.md`: Mermaid and typed-edge view of the candidate bridge graph.
- `boundary_expansion.md`: review tasks for the three compressed boundary edges.
- `C001_kernel_to_criterion_expansion.md`: candidate expansion of Boundary 1 only.
- `C001_review_checklist.md`: review checklist for C001 before any status change.
- `C002_criterion_to_constraint_expansion.md`: candidate expansion of Boundary 2 only.
- `C002_review_checklist.md`: review checklist for C002 before any status change.
- `C003_constraint_to_eigenspace_expansion.md`: candidate high-risk expansion of Boundary 3 only.
- `C003_split_plan.md`: proposed proof-facing split for over-compressed C003.
- `C003_proofbridge_review_checklist.md`: review checklist for the C003 parent bridge and C003a-C003e ProofBridge nodes.
- `concept_bridge_review_summary.md`: status, risk, and next-review summary for C001-C003.
- `concept_patch_schema_audit_extension.md`: proposed audit metadata schema for parent bridges and proof-facing subbridges.

Machine-readable patch data is stored separately at `data/hmdg/concept_patch.json`.

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
