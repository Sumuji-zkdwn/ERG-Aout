# C001 kernel_to_criterion expansion

status: candidate expansion
source boundary: `LinearMap.ker_restrict` -> `LinearMap.injective_restrict_iff_disjoint`
target theorem path: `Module.End.iSup_genEigenspace_restrict_eq_top`

## Purpose

This note expands only Boundary 1 from `docs/hmdg/boundary_expansion.md`.

It is not an accepted mathematical proof of the final target theorem. It is a candidate cognitive bridge explaining why a statement about the kernel of a restricted linear map can become an injectivity/disjointness criterion.

## Source declaration in plain language

`LinearMap.ker_restrict` says that if a linear map `f : M -> M₁` maps a submodule `p` into a submodule `q`, then the kernel of the restricted map `f.restrict hf` is the comap of the original kernel `LinearMap.ker f` along the subtype map `p.subtype`.

Plainly:

```text
The elements of p killed by the restricted map are exactly the elements of p whose underlying elements are killed by f.
```

Equivalently, restriction does not invent a new kernel. It only filters the original kernel through the restricted domain.

## Target declaration in plain language

`LinearMap.injective_restrict_iff_disjoint` says that, for an endomorphism `f : M ->ₗ[R] M` preserving a submodule `p`, the restricted map `f.restrict hf` is injective if and only if `p` is disjoint from `LinearMap.ker f`.

Plainly:

```text
The restriction of f to p is injective exactly when p contains no nonzero vector killed by f.
```

## Boundary-crossing operation

The boundary-crossing operation is:

```text
kernel of restricted map
→ zero-kernel condition for injectivity
→ no nonzero element in p ∩ ker f
→ disjointness of p and ker f
```

So the bridge is not merely a change of vocabulary. It converts an equality describing a restricted kernel into a criterion for injectivity by reading kernel equality at bottom/trivial intersection level.

## Token expansion

### ker

`ker` tracks the zero-preimage condition: to be in the kernel is to be mapped to zero.

In `ker_restrict`, the relevant kernel is the kernel after restricting the domain to `p` and the codomain to `q`.

### restrict

`restrict` changes the domain being tested from all of `M` to only the submodule `p`.

After restriction, the only possible witnesses to non-injectivity are pairs or differences of elements inside `p`.

### injective

`injective` is detected by whether the restricted map has only the trivial kernel.

For linear maps, injectivity is equivalent to saying that the only element mapped to zero is zero.

### iff

`iff` means the criterion must work in both directions.

Forward direction: if the restricted map is injective, then no nonzero element of `p` can lie in the original kernel.

Backward direction: if `p` has trivial intersection with the original kernel, then no nonzero element of the restricted domain can be killed, so the restricted map is injective.

### disjoint

`disjoint` identifies the lattice-level form of the zero-kernel condition.

Here, saying that `p` is disjoint from `ker f` means that their intersection contains only the zero submodule.

## Atomic bridge steps

```text
B001. Start with a linear map f preserving a submodule p.
B002. The restricted map f.restrict hf has domain p.
B003. An element of ker(f.restrict hf) is an element x of p such that f(x) = 0.
B004. Such an x is precisely an element of p whose underlying element lies in ker f.
B005. Therefore ker(f.restrict hf) is the pullback/comap of ker f along p.subtype.
B006. A linear map is injective exactly when its kernel is bottom/trivial.
B007. Thus f.restrict hf is injective exactly when the only element of p lying in ker f is zero.
B008. The statement that p and ker f meet only at zero is expressed as Disjoint p (ker f).
B009. Therefore the kernel computation becomes the injectivity/disjointness criterion.
```

## HMDG edge interpretation

```text
D003: LinearMap.ker_restrict
  role: kernel
  cognitive content: locate the kernel after restriction by pulling back the original kernel.

C001: kernel_to_criterion
  role: bridge
  cognitive content: interpret zero-kernel of the restricted map as a trivial-intersection condition.

D004: LinearMap.injective_restrict_iff_disjoint
  role: criterion
  cognitive content: package the trivial-intersection condition as an iff criterion for injectivity.
```

## Why the intermediate concept node is justified

The direct edge from `LinearMap.ker_restrict` to `LinearMap.injective_restrict_iff_disjoint` is mathematically compact.

A human reader must perform at least three transformations:

```text
kernel equality
→ kernel equals bottom / injectivity
→ restricted-domain zero witness
→ disjointness between p and ker f
```

These transformations are not visible from the declaration names alone. Therefore `kernel_to_criterion` is a justified ConceptBridge candidate.

## Review status

Accepted as HMDG candidate expansion: no.

Ready for mathematical review: yes.

Required review questions:

1. Is the plain-language description of `LinearMap.ker_restrict` faithful to the current mathlib declaration?
2. Is the plain-language description of `LinearMap.injective_restrict_iff_disjoint` faithful to the current mathlib declaration?
3. Is `kernel_to_criterion` too broad, or should it be split into `kernel_to_zero_kernel` and `zero_kernel_to_disjointness`?
4. Should this bridge be kept as a single HMDG concept node for readability, even if it internally contains multiple proof operations?

## Non-goals

This file does not expand C002 or C003.

This file does not claim that `Module.End.iSup_genEigenspace_restrict_eq_top` has been explained.

This file does not promote any candidate bridge into an accepted ERG kernel definition.
