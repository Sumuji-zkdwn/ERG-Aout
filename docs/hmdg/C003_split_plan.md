# C003 split plan

status: candidate split plan
parent bridge: `C003 constraint_to_eigenspace`
related issue: `#68`
related PR: `#69`

## Purpose

This document records the proposed split of C003 after the proof-body audit.

It does not modify the machine-readable ConceptBridge graph.

It does not add C004.

It exists to decide whether C003 should remain one high-level phase node, or whether it should be represented by smaller proof-facing bridge nodes.

## Current parent bridge

```text
D007 LinearMap.ker_noncommProd_eq_of_supIndep_ker
→ C003 constraint_to_eigenspace
→ D008 Submodule.inf_iSup_genEigenspace
```

Current assessment:

```text
C003 is proof-used, but over-compressed.
```

The proof of `Submodule.inf_iSup_genEigenspace` directly uses `LinearMap.ker_noncommProd_eq_of_supIndep_ker`, so the bridge is not merely a formal dependency artifact.

However, one bridge node hides several proof-facing moves.

## Proof-local route

The audited proof route can be summarized as:

```text
p ∩ iSup genEigenspace membership
→ finite-support component decomposition
→ choose one μ component
→ build an auxiliary product g over the other support components
→ use product-kernel decomposition and generalized-eigenspace independence
→ prove g is injective on the selected μ component
→ use invariance of p and finite-dimensional injective/surjective transfer
→ show the selected component lies in p
→ reassemble all components into iSup μ, p ∩ genEigenspace μ
```

## Proposed subbridges

### C003a iSup_component_extraction

Role:

```text
iSup membership -> finite-support component decomposition
```

Human-facing meaning:

An element of `p ⊓ ⨆ μ, f.genEigenspace μ k` is treated as a finite sum of generalized-eigenspace components.

Proof-local markers:

```text
mem_iSup_iff_exists_finsupp
Finsupp support
component m μ
```

Why it matters:

The target theorem is componentwise. The proof must first expose the hidden components inside the indexed supremum.

### C003b product_kernel_isolation

Role:

```text
selected component μ -> auxiliary product over the other components
```

Human-facing meaning:

To isolate one generalized-eigenspace component, the proof builds an auxiliary endomorphism `g` as a product of shifted powers corresponding to the other support components.

Proof-local markers:

```text
m.support.erase μ
noncommProd
g
commutation of shifted powers
```

Why it matters:

The product is designed to kill the unwanted components while preserving enough information about the selected component.

### C003c kernel_independence_to_injectivity

Role:

```text
product-kernel decomposition + eigenspace independence -> injectivity on selected component
```

Human-facing meaning:

The proof controls the kernel of the auxiliary product `g`. Since the kernel does not overlap the selected generalized-eigenspace component in the wrong way, `g` is injective on that component.

Proof-local markers:

```text
LinearMap.injOn_of_disjoint_ker
f.independent_genEigenspace k
LinearMap.ker_noncommProd_eq_of_supIndep_ker
Finset.supIndep_iff_disjoint_erase
```

Why it matters:

This is the exact place where the C003 source theorem enters the target proof.

### C003d invariant_submodule_surjectivity_transfer

Role:

```text
injectivity + finite-dimensionality + invariance of p -> recover a component inside p
```

Human-facing meaning:

The auxiliary map `g` preserves both `p` and the selected generalized eigenspace. Since it is injective on the relevant finite-dimensional component, it is also surjective there, allowing the proof to find a representative inside `p`.

Proof-local markers:

```text
MapsTo g p p
mapsTo_genEigenspace_of_comm
LinearMap.injOn_iff_surjOn
p ⊓ f.genEigenspace μ k
```

Why it matters:

This is where the invariant-submodule condition becomes active. Without this step, kernel decomposition alone would not show that the selected component lies in `p`.

### C003e componentwise_reassembly

Role:

```text
each component lies in p -> rebuild target iSup membership
```

Human-facing meaning:

After proving every finite-support generalized-eigenspace component lies in `p`, the proof reassembles the original element as an element of `⨆ μ, p ⊓ f.genEigenspace μ k`.

Proof-local markers:

```text
mem_iSup_iff_exists_finsupp
mem_inf
Finsupp sum
```

Why it matters:

This completes the move from global intersection to componentwise intersection.

## Proposed chain

```text
D007 LinearMap.ker_noncommProd_eq_of_supIndep_ker
→ C003c kernel_independence_to_injectivity
```

and inside the target proof narrative:

```text
C003a iSup_component_extraction
→ C003b product_kernel_isolation
→ C003c kernel_independence_to_injectivity
→ C003d invariant_submodule_surjectivity_transfer
→ C003e componentwise_reassembly
→ D008 Submodule.inf_iSup_genEigenspace
```

This is not the same as a simple declaration dependency path.

It is a proof-facing explanation route extracted from the audited proof body.

## Relationship to parent C003

C003 should remain as a high-level phase label:

```text
constraint_to_eigenspace
```

But C003 should not be treated as an atomic proof step.

Recommended representation:

```text
C003:
  status: candidate_phase_node
  audit_status: proof_used_but_over_compressed
  subbridges:
    - C003a iSup_component_extraction
    - C003b product_kernel_isolation
    - C003c kernel_independence_to_injectivity
    - C003d invariant_submodule_surjectivity_transfer
    - C003e componentwise_reassembly
```

## Decision proposal

Adopt the split at the documentation level first.

Do not immediately modify `data/hmdg/concept_patch.json`.

Reason:

```text
The JSON currently represents the candidate graph generated from the real dependency path.
The C003a-C003e sequence is proof-facing explanatory structure, not yet part of the generated graph schema.
```

## Next steps after accepting this plan

```text
1. Add audit metadata fields to the machine-readable concept patch schema.
2. Represent C003 as a parent candidate phase node.
3. Represent C003a-C003e as optional proof-facing subnodes.
4. Render parent/subnode distinction in Mermaid output.
5. Only then consider continuing beyond C003 toward C004.
```

## Non-goals

This document does not create C004.

This document does not alter `data/hmdg/concept_patch.json`.

This document does not claim that C003a-C003e are accepted ERG kernel definitions.

This document does not prove `Submodule.inf_iSup_genEigenspace`.
