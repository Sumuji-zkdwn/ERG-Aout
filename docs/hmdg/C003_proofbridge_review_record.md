# C003 ProofBridge review record

status: review record / candidate parent and subbridges kept
scope: `C003_constraint_to_eigenspace` and `C003a`-`C003e`
parent bridge: `C003_constraint_to_eigenspace`
source boundary: `LinearMap.ker_noncommProd_eq_of_supIndep_ker` -> `Submodule.inf_iSup_genEigenspace`
review checklist: `docs/hmdg/C003_proofbridge_review_checklist.md`
related artifacts:

```text
docs/hmdg/C003_constraint_to_eigenspace_expansion.md
docs/hmdg/C003_split_plan.md
data/hmdg/concept_patch.json
```

## Purpose

This document records the first proof-body review for C003 and its candidate ProofBridge subnodes.

It does not accept C003 as a stable ERG kernel definition.

It does not accept C003a-C003e as final proof decomposition nodes.

It does not prove `Submodule.inf_iSup_genEigenspace`.

It records whether the current candidate proof-facing decomposition is faithful enough to keep as a candidate review structure.

## Review metadata

```text
reviewer: GPT-assisted proof-body source check
date: 2026-05-26
mathlib source: leanprover-community/mathlib4
mathlib source commit/ref: 75adafcaf8c4a0fcde8e1508f503bed2263ab055
proof file path: Mathlib/LinearAlgebra/Eigenspace/Triangularizable.lean
proof declaration checked: Submodule.inf_iSup_genEigenspace
source theorem occurrence found: yes
source theorem: LinearMap.ker_noncommProd_eq_of_supIndep_ker
```

## Parent bridge check

Current parent bridge:

```text
C003 constraint_to_eigenspace
```

Observed target declaration shape:

```text
p ⊓ ⨆ μ, f.genEigenspace μ k = ⨆ μ, p ⊓ f.genEigenspace μ k
```

Observed proof-body fact:

```text
LinearMap.ker_noncommProd_eq_of_supIndep_ker
```

is used inside the proof of `Submodule.inf_iSup_genEigenspace`, in the local block proving injectivity of an auxiliary product map on a selected generalized-eigenspace component.

Review judgment:

```text
C003 parent bridge: faithful as high-level candidate parent
```

Reason:

The source theorem is not merely adjacent metadata. It appears in the proof body. However, the proof path from the source theorem to the final generalized-eigenspace intersection statement contains several distinct moves. Therefore C003 should remain a high-level parent bridge, not an atomic proof-facing step.

## C003a review

Subbridge:

```text
C003a iSup_component_extraction
```

Candidate role:

```text
iSup membership -> finite-support generalized-eigenspace component decomposition
```

Proof-body evidence found:

```text
obtain ⟨hm₀ : m ∈ p, hm₁ : m ∈ ⨆ μ, f.genEigenspace μ k⟩ := hm
obtain ⟨m, hm₂, rfl⟩ := (mem_iSup_iff_exists_finsupp _ _).mp hm₁
...
(mem_iSup_iff_exists_finsupp _ _).mpr ⟨m, fun μ ↦ mem_inf.mp ⟨this μ, hm₂ μ⟩, rfl⟩
```

Review judgment:

```text
C003a: faithful
```

Reason:

The proof explicitly turns membership in an indexed supremum into a finite-support object and later uses the same mechanism for reassembly. The C003a label faithfully captures the first extraction move.

## C003b review

Subbridge:

```text
C003b product_kernel_isolation
```

Candidate role:

```text
selected component -> auxiliary product over other support components
```

Proof-body evidence found:

```text
by_cases hμ : μ ∈ m.support
let l₀ : ℕ := m.support.sup l
let g : End K V := (m.support.erase μ).noncommProd _ fun μ₁ _ μ₂ _ _ ↦ h_comm μ₁ μ₂
have hfg : Commute f g := Finset.noncommProd_commute ...
have hg₀ : g (m.sum fun _μ mμ ↦ mμ) = g (m μ) := by ...
```

Review judgment:

```text
C003b: faithful
```

Reason:

The proof selects a component `μ`, builds an auxiliary product `g` over `m.support.erase μ`, and uses that product to isolate the selected component from the finite-support sum. The label is faithful.

## C003c review

Subbridge:

```text
C003c kernel_independence_to_injectivity
```

Candidate role:

```text
product-kernel decomposition + eigenspace independence -> injectivity on selected component
```

Proof-body evidence found:

```text
have hg₃ : InjOn g ↑(f.genEigenspace μ k) := by
  apply LinearMap.injOn_of_disjoint_ker subset_rfl
  have this := f.independent_genEigenspace k
  ...
  rw [LinearMap.ker_noncommProd_eq_of_supIndep_ker, ← Finset.sup_eq_iSup]
  ...
  have := Finset.supIndep_iff_disjoint_erase.mp (this.supIndep' m.support) μ hμ
```

Review judgment:

```text
C003c: faithful
source theorem used here: yes
```

Reason:

This is the exact local region where `LinearMap.ker_noncommProd_eq_of_supIndep_ker` enters the target proof. It is used with generalized-eigenspace independence and disjointness machinery to prove `InjOn g` on the selected generalized eigenspace. The label is faithful.

## C003d review

Subbridge:

```text
C003d invariant_submodule_surjectivity_transfer
```

Candidate role:

```text
injectivity + finite-dimensionality + invariance of p -> recover component inside p
```

Proof-body evidence found:

```text
have hg₁ : MapsTo g p p := ...
have hg₂ : MapsTo g ↑(f.genEigenspace μ k) ↑(f.genEigenspace μ k) :=
  f.mapsTo_genEigenspace_of_comm hfg μ k
have hg₄ : SurjOn g
    ↑(p ⊓ f.genEigenspace μ k) ↑(p ⊓ f.genEigenspace μ k) := by
  have : MapsTo g
      ↑(p ⊓ f.genEigenspace μ k) ↑(p ⊓ f.genEigenspace μ k) :=
    hg₁.inter_inter hg₂
  rw [← LinearMap.injOn_iff_surjOn this]
  exact hg₃.mono inter_subset_right
```

Review judgment:

```text
C003d: faithful with minor wording caution
```

Reason:

The proof does use invariance/maps-to facts for `p` and for the selected generalized eigenspace, then converts injectivity into surjectivity on the intersection. The candidate label is faithful. The wording should be careful that finite-dimensionality is not manually invoked at this line, but is part of the available theorem/instance context behind `LinearMap.injOn_iff_surjOn`.

## C003e review

Subbridge:

```text
C003e componentwise_reassembly
```

Candidate role:

```text
each component lies in p -> rebuild target iSup membership
```

Proof-body evidence found:

```text
suffices ∀ μ, (m μ : V) ∈ p by
  exact (mem_iSup_iff_exists_finsupp _ _).mpr ⟨m, fun μ ↦ mem_inf.mp ⟨this μ, hm₂ μ⟩, rfl⟩
...
obtain ⟨y, ⟨hy₀ : y ∈ p, hy₁ : y ∈ f.genEigenspace μ k⟩, hy₂ : g y = g (m μ)⟩ := ...
rwa [← hg₃ hy₁ hm₂ hy₂]
```

Review judgment:

```text
C003e: faithful
```

Reason:

The proof goal is reduced to showing each finite-support component lies in `p`, and then reconstructs target membership through `mem_iSup_iff_exists_finsupp` and `mem_inf`. The label is faithful.

## Chain-level review

Current candidate chain:

```text
C003a -> C003b -> C003c -> C003d -> C003e
```

Review judgment:

```text
chain order: faithful
```

Reason:

The proof-body order matches the proposed chain well:

```text
1. Extract a finite-support component decomposition from iSup membership.
2. Select μ and construct an auxiliary product over the other support components.
3. Use product-kernel decomposition plus generalized-eigenspace independence to prove injectivity.
4. Use maps-to/invariance and injective-to-surjective transfer on the intersection.
5. Recover the selected component inside p and reassemble the componentwise iSup statement.
```

## Review outcome

```text
keep_candidate_parent_and_subbridges
```

## Required follow-up

Do not mark C003 or C003a-C003e as accepted yet.

If the repository later adds accepted-status policy, this review record can be used as supporting evidence, but it is not itself an acceptance event.

Minor wording follow-up:

```text
C003d should mention that finite-dimensional transfer is mediated through LinearMap.injOn_iff_surjOn in the existing theorem context, rather than claiming a separate explicit dimension calculation at that line.
```

## Non-goals

This review does not update `data/hmdg/concept_patch.json`.

This review does not change the renderer.

This review does not add C004.

This review does not promote C003 or C003a-C003e to accepted ERG kernel definitions.
