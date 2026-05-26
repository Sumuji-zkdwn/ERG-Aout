# C003 constraint_to_eigenspace expansion

status: candidate expansion / high-risk bridge / audit-updated
source boundary: `LinearMap.ker_noncommProd_eq_of_supIndep_ker` -> `Submodule.inf_iSup_genEigenspace`
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`
related issue: `#68`

## Purpose

This note expands only Boundary 3 from `docs/hmdg/boundary_expansion.md`.

It is not an accepted mathematical proof of the final target theorem. It is a candidate cognitive bridge explaining how kernel/sup-independence constraints begin to connect to generalized eigenspace decompositions.

This bridge is less direct than C001 and C002. It remains a high-risk HMDG candidate, but the reason has been refined after proof-body audit.

## Audit update

Issue `#68` checked the current proof body of `Submodule.inf_iSup_genEigenspace` in `Mathlib/LinearAlgebra/Eigenspace/Triangularizable.lean`.

The audit found that the proof does directly use:

```text
LinearMap.ker_noncommProd_eq_of_supIndep_ker
```

inside the proof of an auxiliary injectivity statement:

```text
have hg₃ : InjOn g ↑(f.genEigenspace μ k) := by
  apply LinearMap.injOn_of_disjoint_ker subset_rfl
  have this := f.independent_genEigenspace k
  ...
  rw [LinearMap.ker_noncommProd_eq_of_supIndep_ker, ← Finset.sup_eq_iSup]
  ...
```

Therefore C003 should no longer be treated as merely a possible formal dependency artifact.

Updated assessment:

```text
The dependency is real at proof level.
The current C003 bridge is still high-risk because it compresses several proof moves into one cognitive node.
```

## Source declaration in plain language

`LinearMap.ker_noncommProd_eq_of_supIndep_ker` says that for a finite-dimensional vector space over a division ring, if a finite family of endomorphisms commutes pairwise and the kernels are `SupIndep`, then the kernel of their finite noncommutative product is the supremum of their individual kernels.

Plainly:

```text
Under commutation and independence assumptions, the kernel of the product is exactly the sum/supremum of the kernels of the factors.
```

This is a structural kernel theorem. It explains when a kernel of a product decomposes cleanly into the kernels of its factors.

## Target declaration in plain language

`Submodule.inf_iSup_genEigenspace` says that if a submodule `p` is invariant under an endomorphism `f`, then, in finite dimension, intersecting `p` with the supremum of generalized eigenspaces can be moved inside the indexed supremum:

```text
p ⊓ ⨆ μ, (f.genEigenspace μ) k
=
⨆ μ, p ⊓ (f.genEigenspace μ) k
```

Plainly:

```text
The part of p lying in the total generalized-eigenspace sum is the sum of the parts of p lying in each generalized eigenspace.
```

This is an eigenspace/lattice theorem. It explains how an invariant submodule interacts with a generalized eigenspace decomposition.

## Boundary-crossing operation

The boundary-crossing operation is:

```text
kernel of product decomposes as sup of kernels
→ kernels of polynomial-like factors behave as spectral components
→ sup-independence controls clean decomposition
→ invariant submodule p can be intersected with the eigenspace supremum componentwise
```

The bridge is not a direct one-step theorem application. It is a phase transition:

```text
kernel/lattice constraints
→ spectral component decomposition
→ generalized eigenspace lattice identity
```

## Why this bridge is high-risk

C001 and C002 each connect neighboring declarations whose plain-language meanings are close.

C003 is different. The source theorem talks about kernels of finite products of commuting endomorphisms. The target theorem talks about intersections of an invariant submodule with a supremum of generalized eigenspaces.

The audit confirms that the proof of `Submodule.inf_iSup_genEigenspace` really uses `LinearMap.ker_noncommProd_eq_of_supIndep_ker`. The high-risk status is therefore not because the dependency is imaginary.

The high-risk status is because the human-facing bridge is over-compressed.

The proof route contains several distinct moves:

```text
1. decompose an element of p ∩ iSup genEigenspace into finitely supported generalized-eigenspace components;
2. isolate one component μ using a product over the other support components;
3. use kernel-product decomposition and independence to prove injectivity on the μ component;
4. use finite-dimensional injective/surjective transfer on p ∩ genEigenspace μ;
5. conclude the μ component lies in p;
6. rebuild the iSup membership componentwise.
```

A single node named `constraint_to_eigenspace` hides most of this route.

## Token expansion

### ker

`ker` tracks the zero-preimage condition.

In the source theorem, kernels of individual factors combine to describe the kernel of the whole product.

In the target proof region, generalized eigenspaces are treated through kernel-like conditions such as powers of shifted endomorphisms.

### noncommProd

`noncommProd` indicates a finite product of endomorphisms where multiplication order matters in general.

In the proof of `Submodule.inf_iSup_genEigenspace`, an auxiliary product `g` is built from the support components other than the selected component `μ`.

The theorem requires commutation hypotheses so that this product behaves well enough for kernel decomposition.

### eq

`eq` marks an exact structural identity, not just an inclusion.

The source theorem gives exact equality between a product-kernel and a supremum of kernels.

The target theorem gives exact equality between an intersection with a supremum and a supremum of intersections.

### supIndep

`supIndep` says that a family of submodules is independent with respect to supremum.

In the proof region, independence of generalized eigenspaces is used with the kernel-product theorem to control the kernel of the auxiliary product and prove injectivity on one component.

### inf

`inf` is the meet/intersection operation on submodules.

In the target theorem, `p ⊓ ...` asks for the part of a larger decomposition that lies inside the invariant submodule `p`.

### iSup

`iSup` is an indexed supremum.

The target proof begins with membership in an indexed supremum, decomposes that membership into finitely supported components, and then rebuilds the componentwise `iSup` membership.

### genEigenspace

`genEigenspace` is the generalized eigenspace associated with an eigenvalue and a generalized exponent parameter.

In this proof region, generalized eigenspaces function as the spectral components that must be isolated one at a time.

## Atomic bridge steps

```text
B001. Start with an element m in p ⊓ ⨆ μ, f.genEigenspace μ k.
B002. Use membership in the iSup to express m as a finite support sum of generalized-eigenspace components.
B003. Fix one component μ.
B004. Build an auxiliary endomorphism g as a noncommutative product over the other support components.
B005. Use commutation of shifted powers of f to make g well-behaved.
B006. Use the fact that other components are killed by their corresponding factors.
B007. Use `LinearMap.ker_noncommProd_eq_of_supIndep_ker` to rewrite the kernel of g as a supremum of factor kernels.
B008. Use independence of generalized eigenspaces to show that this kernel is disjoint from the selected μ component.
B009. Conclude that g is injective on the selected generalized eigenspace component.
B010. Use invariance of p to show g maps p into p.
B011. Use finite-dimensional injective/surjective transfer on p ⊓ f.genEigenspace μ k.
B012. Recover a representative of the μ component inside p.
B013. Use injectivity to identify that representative with the original μ component.
B014. Conclude that each finite-support component lies in p.
B015. Reassemble the components to prove membership in ⨆ μ, p ⊓ f.genEigenspace μ k.
```

## HMDG edge interpretation

```text
D007: LinearMap.ker_noncommProd_eq_of_supIndep_ker
  role: constraint
  cognitive content: decompose the kernel of a product into a supremum of independent kernel components.

C003: constraint_to_eigenspace
  role: bridge
  cognitive content: use product-kernel decomposition and eigenspace independence to isolate a generalized-eigenspace component.

D008: Submodule.inf_iSup_genEigenspace
  role: eigenspace
  cognitive content: distribute the invariant submodule intersection across the supremum of generalized eigenspaces.
```

## Why the intermediate concept node is justified

The direct edge from `LinearMap.ker_noncommProd_eq_of_supIndep_ker` to `Submodule.inf_iSup_genEigenspace` is too compressed for a human reading.

The source theorem lives in the language of:

```text
kernel
noncommutative product
commutation
sup-independence
supremum of kernels
```

The target theorem lives in the language of:

```text
invariant submodule
intersection/inf
indexed supremum
generalized eigenspace
componentwise decomposition
```

The audit shows that the kernel-product theorem is genuinely used in the proof. However, the human bridge is not simply `constraint -> eigenspace`; it passes through component isolation, auxiliary products, injectivity, surjectivity, and reassembly.

## Recommended split

C003 is too broad as a single proof-level node.

Recommended finer bridge sequence:

```text
C003a iSup_component_extraction
C003b product_kernel_isolation
C003c kernel_independence_to_injectivity
C003d invariant_submodule_surjectivity_transfer
C003e componentwise_reassembly
```

Keeping C003 as one HMDG phase node may still be useful for a high-level cognitive graph, but proof-level documentation should not treat it as one atomic move.

## Review status

Accepted as HMDG candidate expansion: no.

Ready for mathematical review: partially.

Dependency artifact concern: mostly resolved. The source theorem is directly used in the target proof region.

Over-compression concern: still unresolved. C003 should likely be split before any accepted proof-facing graph is generated.

Required review questions:

1. Should C003 remain as a high-level phase node while also adding C003a-C003e as proof-facing subnodes?
2. Is the phrase "generalized eigenspaces are kernel-like spectral components" precise enough, or should it be replaced with the more proof-local phrase "components killed by powers of shifted endomorphisms"?
3. Is `supIndep` a human-facing concept in this bridge, or should the user-facing explanation emphasize disjointness/injectivity instead?
4. Should the current graph mark C003 as `over_compressed` rather than merely `high_risk`?
5. Should `data/hmdg/concept_patch.json` gain an audit status field before more bridges are generated?

## Non-goals

This file does not expand C001 or C002.

This file does not prove `Submodule.inf_iSup_genEigenspace`.

This file does not claim that `Module.End.iSup_genEigenspace_restrict_eq_top` has been fully explained.

This file does not promote any candidate bridge into an accepted ERG kernel definition.
