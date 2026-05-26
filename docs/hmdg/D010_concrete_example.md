# Concrete example for D010

status: human-facing concrete example / not a proof / not accepted ERG kernel status
related explanation: `docs/hmdg/D010_human_explanation.md`
target declaration: `Module.End.iSup_genEigenspace_restrict_eq_top`
main point: D009 and D010 say the same decomposition from two viewpoints

## Purpose

This document gives a small concrete example for the D010 target theorem.

It is meant to make the difference between these two viewpoints visible:

```text
D009:
  View p from the big space V.

D010:
  View p as its own smaller space.
```

## Example setup

Let the big space be the ordinary plane:

```text
V = R²
```

Write vectors as:

```text
(x, y)
```

Define a linear map:

```text
f(x, y) = (2x, 3y)
```

This map stretches the x-direction by 2 and the y-direction by 3.

So the two eigenspaces in the big space are:

```text
E₂ = x-axis = { (x, 0) }
E₃ = y-axis = { (0, y) }
```

The whole plane decomposes as:

```text
R² = E₂ ⊕ E₃
```

Human reading:

```text
Every vector (x, y) is the sum of an x-axis part and a y-axis part:
(x, y) = (x, 0) + (0, y)
```

## Choose an invariant subspace p

Now choose:

```text
p = x-axis = { (x, 0) }
```

This `p` is invariant under `f`.

Reason:

```text
If (x, 0) is on the x-axis,
then f(x, 0) = (2x, 0),
which is still on the x-axis.
```

So `f` does not push vectors in `p` outside of `p`.

Therefore we can restrict `f` to `p`:

```text
f|p : p -> p
```

In this example:

```text
f|p(x, 0) = (2x, 0)
```

Inside `p`, this is just multiplication by 2.

## D009 viewpoint: look at p from the big space V

D009 says:

```text
p = sum of (p ∩ big eigenspaces of f)
```

In this example, the big eigenspaces are:

```text
E₂ = x-axis
E₃ = y-axis
```

Now intersect each one with `p`:

```text
p ∩ E₂ = x-axis ∩ x-axis = x-axis
p ∩ E₃ = x-axis ∩ y-axis = {0}
```

So:

```text
p = (p ∩ E₂) + (p ∩ E₃)
  = x-axis + {0}
  = x-axis
```

This is the D009-style statement.

Human reading:

```text
From the big plane V, p is made from the x-eigenspace part that lies in p.
The y-eigenspace contributes nothing to p.
```

## D010 viewpoint: look at p as its own space

Now forget the whole plane for a moment.

Treat `p` itself as the space.

Inside `p`, the restricted map is:

```text
f|p(x, 0) = (2x, 0)
```

So the whole space `p` is the eigenspace for eigenvalue 2 of the restricted map.

In symbols:

```text
p = eigenspace of f|p for eigenvalue 2
```

This is the D010-style statement.

Human reading:

```text
Inside the x-axis world, everything is an eigenvector of f|p with eigenvalue 2.
So the generalized eigenspaces of f|p span all of p.
```

## What C005 translates

C005 is the translation between these two statements.

D009 says:

```text
p ∩ E₂ = x-axis
```

D010 says:

```text
eigenspace of f|p for eigenvalue 2 = x-axis
```

So in this example, C005 is the identification:

```text
p ∩ (eigenspace of f in V for eigenvalue 2)
=
eigenspace of f|p inside p for eigenvalue 2
```

Concretely:

```text
x-axis ∩ x-axis
=
x-axis
```

The left side is the big-space viewpoint.

The right side is the restricted-space viewpoint.

## What R004 does in this example

R004 uses the fact that the whole plane decomposes as:

```text
V = E₂ + E₃
```

Then it intersects that decomposition with `p`:

```text
p = p ∩ V
  = p ∩ (E₂ + E₃)
  = (p ∩ E₂) + (p ∩ E₃)
```

For this example:

```text
x-axis = (x-axis ∩ x-axis) + (x-axis ∩ y-axis)
       = x-axis + {0}
       = x-axis
```

So R004 is not the hard part.

It just says:

```text
If V is decomposed, then intersect the decomposition with p.
```

## Why invariance matters

The example worked because the x-axis is invariant under `f`.

If we choose a subspace that is not invariant, then `f|p` may not even be a map from `p` to `p`.

For example, take:

```text
p = diagonal line = { (t, t) }
```

Then:

```text
f(t, t) = (2t, 3t)
```

This is usually not on the diagonal line, because:

```text
2t ≠ 3t
```

unless `t = 0`.

So the diagonal line is not closed under `f`.

Therefore `f|p : p -> p` is not available in the same way.

That is why the theorem requires:

```text
x ∈ p -> f x ∈ p
```

## Minimal takeaway

For the invariant x-axis example:

```text
Big-space statement:
  p is the part of the big eigenspace decomposition that lies on the x-axis.

Restricted-space statement:
  if we live only on the x-axis, the restricted map has its own eigenspace decomposition.
```

These two statements describe the same object from different viewpoints.

That viewpoint change is C005.

## Connection to the real target theorem

The real theorem uses generalized eigenspaces and arbitrary invariant submodules.

The example used ordinary eigenspaces in `R²` because it is easier to see.

The structural idea is the same:

```text
ambient generalized eigenspace ∩ invariant submodule
=
generalized eigenspace of the restricted map
```

Once that identification is made, the D009 statement becomes the D010 statement.
