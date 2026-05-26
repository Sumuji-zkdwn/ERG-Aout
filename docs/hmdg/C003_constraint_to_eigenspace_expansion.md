# C003 constraint_to_eigenspace expansion

status: candidate expansion / high-risk bridge
source boundary: `LinearMap.ker_noncommProd_eq_of_supIndep_ker` -> `Submodule.inf_iSup_genEigenspace`
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`

## Purpose

This note expands only Boundary 3 from `docs/hmdg/boundary_expansion.md`.

It is not an accepted mathematical proof of the final target theorem. It is a candidate cognitive bridge explaining how kernel/sup-independence constraints begin to connect to generalized eigenspace decompositions.

This bridge is less direct than C001 and C002. It should be treated as a high-risk HMDG candidate until reviewed against the actual proof graph.

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

The hidden mathematical content is likely the idea that generalized eigenspaces arise as kernels of powers or polynomial factors of an endomorphism. Therefore a theorem about kernels of products can contribute to a theorem about sums of generalized eigenspaces.

However, this file does not verify the exact proof route. It only records the cognitive bridge suggested by the extracted dependency path.

## Token expansion

### ker

`ker` tracks the zero-preimage condition.

In the source theorem, kernels of individual factors combine to describe the kernel of the whole product.

In the target region, generalized eigenspaces can be read as kernel-like spectral components.

### noncommProd

`noncommProd` indicates a finite product of endomorphisms where multiplication order matters in general.

The theorem requires commutation hypotheses so that the product behaves well enough for a clean kernel decomposition.

### eq

`eq` marks an exact structural identity, not just an inclusion.

The source theorem gives exact equality between a product-kernel and a supremum of kernels.

The target theorem gives exact equality between an intersection with a supremum and a supremum of intersections.

### supIndep

`supIndep` says that a family of submodules is independent with respect to supremum.

This is the structural condition that prevents the kernel components from overlapping in a way that would destroy a clean decomposition.

### inf

`inf` is the meet/intersection operation on submodules.

In the target theorem, `p ⊓ ...` asks for the part of a larger decomposition that lies inside the invariant submodule `p`.

### iSup

`iSup` is an indexed supremum.

In the target theorem, generalized eigenspace components are assembled by taking the supremum over eigenvalues.

### genEigenspace

`genEigenspace` is the generalized eigenspace associated with an eigenvalue and a generalized exponent parameter.

It functions as the spectral-component analogue of a kernel of a polynomial-like expression in the endomorphism.

## Atomic bridge steps

```text
B001. Start with a finite-dimensional vector space and endomorphisms acting on it.
B002. Kernels of endomorphisms are submodules.
B003. If the relevant endomorphisms commute, a finite product of them can be handled coherently.
B004. If the kernels are SupIndep, the product kernel decomposes as the supremum of the factor kernels.
B005. Generalized eigenspaces can be understood as kernel-like components associated with powers or polynomial factors of an endomorphism.
B006. Therefore a kernel-of-product theorem becomes relevant to eigenspace-sum structure.
B007. The target theorem introduces an invariant submodule p.
B008. Invariance means f sends elements of p back into p, so spectral behavior can be restricted to p.
B009. The question becomes how p intersects a supremum of generalized eigenspaces.
B010. The desired lattice movement is from p ⊓ ⨆ components to ⨆ componentwise intersections.
B011. Kernel decomposition and independence principles supply the conceptual model for why the componentwise decomposition should be valid.
B012. Thus a constraint/kernel theorem can serve as a bridge toward generalized eigenspace lattice decomposition.
```

## HMDG edge interpretation

```text
D007: LinearMap.ker_noncommProd_eq_of_supIndep_ker
  role: constraint
  cognitive content: decompose the kernel of a product into a supremum of independent kernel components.

C003: constraint_to_eigenspace
  role: bridge
  cognitive content: reinterpret kernel decomposition constraints as spectral-component decomposition principles.

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

A human reader must supply the spectral interpretation connecting generalized eigenspaces to kernel-like components. Therefore `constraint_to_eigenspace` is a justified candidate bridge.

## Possible split

C003 is likely too broad as a single proof-level node.

Possible finer bridge sequence:

```text
constraint_to_kernel_decomposition
→ kernel_decomposition_to_spectral_components
→ spectral_components_to_invariant_submodule_inf_iSup
```

However, keeping C003 as one HMDG phase node may be reasonable if the graph is meant to show high-level cognitive phase transitions rather than proof granularity.

## Review status

Accepted as HMDG candidate expansion: no.

Ready for mathematical review: partially.

This file needs stricter review than C001 and C002.

Required review questions:

1. Does the actual proof of `Submodule.inf_iSup_genEigenspace` use `LinearMap.ker_noncommProd_eq_of_supIndep_ker` directly, or is this edge an artifact of dependency extraction?
2. Is the phrase "generalized eigenspaces are kernel-like spectral components" sufficiently precise for HMDG documentation?
3. Should C003 be split into three smaller bridge nodes?
4. Is `supIndep` actually the right human-facing concept here, or merely a proof-level dependency?
5. Does the HMDG graph need an explicit intermediate node for polynomial factors of an endomorphism?

## Non-goals

This file does not expand C001 or C002.

This file does not prove `Submodule.inf_iSup_genEigenspace`.

This file does not claim that `Module.End.iSup_genEigenspace_restrict_eq_top` has been explained.

This file does not promote any candidate bridge into an accepted ERG kernel definition.
