# C003 ProofBridge review checklist

status: candidate review checklist
scope: `C003_constraint_to_eigenspace` and `C003a`-`C003e`
parent bridge: `C003_constraint_to_eigenspace`
source boundary: `LinearMap.ker_noncommProd_eq_of_supIndep_ker` -> `Submodule.inf_iSup_genEigenspace`
related artifacts:

```text
docs/hmdg/C003_constraint_to_eigenspace_expansion.md
docs/hmdg/C003_split_plan.md
data/hmdg/concept_patch.json
```

## Purpose

This document defines the review procedure for the C003 ProofBridge split before any status change is considered.

It does not accept C003 as a stable ERG kernel definition.

It does not accept C003a-C003e as final proof decomposition nodes.

It does not prove `Submodule.inf_iSup_genEigenspace`.

It is a checklist for verifying whether the current proof-facing subbridge sequence is faithful to the Lean proof body.

## Current candidate claim

C003 currently claims that the compressed boundary

```text
LinearMap.ker_noncommProd_eq_of_supIndep_ker
→ Submodule.inf_iSup_genEigenspace
```

should be represented as a high-level parent bridge:

```text
C003 constraint_to_eigenspace
```

with candidate proof-facing subbridges:

```text
C003a iSup_component_extraction
C003b product_kernel_isolation
C003c kernel_independence_to_injectivity
C003d invariant_submodule_surjectivity_transfer
C003e componentwise_reassembly
```

The intended review target is not merely whether the labels sound plausible.

The review target is whether these nodes correspond to recognizable moves in the actual proof body of:

```text
Submodule.inf_iSup_genEigenspace
```

## Required proof-body checks

Before changing any C003-related status, check the current Lean proof body directly.

Record:

```text
mathlib commit/ref:
proof file path:
proof declaration:
reviewed proof range:
source theorem occurrence found: yes/no
source theorem occurrence location:
```

The expected source theorem is:

```text
LinearMap.ker_noncommProd_eq_of_supIndep_ker
```

## Parent bridge check

Verify whether C003 should remain a parent phase bridge rather than an atomic proof step.

Acceptable evidence:

```text
The source theorem is actually used in or near the proof of Submodule.inf_iSup_genEigenspace.
The proof route from source theorem to target declaration contains multiple distinct human-facing operations.
The target proof cannot be faithfully summarized as one direct kernel-to-eigenspace move.
```

Warning signs:

```text
The source theorem is not actually used in the current proof body.
The source theorem occurs only in an unrelated helper theorem outside the reviewed target route.
The C003 parent label hides a different proof mechanism than the one currently represented.
```

## Subbridge checks

### C003a iSup_component_extraction

Candidate role:

```text
iSup membership -> finite-support generalized-eigenspace component decomposition
```

Check for proof-body evidence such as:

```text
mem_iSup_iff_exists_finsupp
Finsupp.support
finite-support representation
component selection from an indexed supremum
```

Record:

```text
C003a evidence found: yes/no/partial
proof markers found:
statement of local proof move:
faithful label: yes/no/needs revision
```

### C003b product_kernel_isolation

Candidate role:

```text
selected component -> auxiliary product over other support components
```

Check for proof-body evidence such as:

```text
noncommProd
support.erase μ
auxiliary product map g
shifted powers or product over other components
commutation conditions for the product
```

Record:

```text
C003b evidence found: yes/no/partial
proof markers found:
statement of local proof move:
faithful label: yes/no/needs revision
```

### C003c kernel_independence_to_injectivity

Candidate role:

```text
product-kernel decomposition + eigenspace independence -> injectivity on selected component
```

Check for proof-body evidence such as:

```text
LinearMap.ker_noncommProd_eq_of_supIndep_ker
supIndep or independent_genEigenspace
ker control
injective / injOn / ker disjointness
```

Record:

```text
C003c evidence found: yes/no/partial
source theorem used here: yes/no
proof markers found:
statement of local proof move:
faithful label: yes/no/needs revision
```

### C003d invariant_submodule_surjectivity_transfer

Candidate role:

```text
injectivity + finite-dimensionality + invariance of p -> recover component inside p
```

Check for proof-body evidence such as:

```text
MapsTo g p p
mapsTo_genEigenspace_of_comm
LinearMap.injOn_iff_surjOn
finite-dimensional transfer
p ⊓ f.genEigenspace μ k
```

Record:

```text
C003d evidence found: yes/no/partial
proof markers found:
statement of local proof move:
faithful label: yes/no/needs revision
```

### C003e componentwise_reassembly

Candidate role:

```text
each component lies in p -> rebuild target iSup membership
```

Check for proof-body evidence such as:

```text
mem_iSup_iff_exists_finsupp
mem_inf
Finsupp sum
componentwise reconstruction
final membership in the target iSup/intersection statement
```

Record:

```text
C003e evidence found: yes/no/partial
proof markers found:
statement of local proof move:
faithful label: yes/no/needs revision
```

## Chain-level review

After checking individual subbridges, check whether the chain order is faithful.

Current candidate chain:

```text
C003a -> C003b -> C003c -> C003d -> C003e
```

Acceptable evidence:

```text
The proof first decomposes iSup membership or component structure.
The proof then constructs an auxiliary product or isolates a selected component.
The source theorem is used in the kernel/injectivity control phase.
The proof then uses invariance and finite-dimensional transfer to recover the component inside p.
The proof finally reassembles the componentwise statement.
```

Warning signs:

```text
The source theorem is used before component extraction in a way the current chain cannot represent.
The auxiliary product and injectivity steps are inseparable and should be one node.
The finite-dimensional transfer is not present or belongs to a different theorem.
The final reassembly is not explicit enough to justify C003e.
```

## Review outcomes

Use one of the following review outcomes.

```text
keep_candidate_parent_and_subbridges
keep_parent_but_reword_subbridges
merge_some_subbridges
split_more_finely
reject_subbridge_split
needs_source_check
```

Do not use `accepted` in this file unless the repository has a separate accepted-status policy for HMDG nodes.

## Minimum review note template

```text
reviewer:
date:
mathlib commit/ref:
proof file path:
proof declaration checked: yes/no
source theorem occurrence found: yes/no
C003 parent bridge: faithful / revise / wrong
C003a: faithful / revise / missing / uncertain
C003b: faithful / revise / missing / uncertain
C003c: faithful / revise / missing / uncertain
C003d: faithful / revise / missing / uncertain
C003e: faithful / revise / missing / uncertain
chain order: faithful / revise / wrong / uncertain
recommended outcome:
notes:
```

## Non-goals

This checklist does not update `data/hmdg/concept_patch.json`.

This checklist does not change the renderer.

This checklist does not review C001 or C002.

This checklist does not add C004.

This checklist does not promote C003 or C003a-C003e to accepted ERG kernel definitions.
