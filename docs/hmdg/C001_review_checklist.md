# C001 review checklist

status: candidate review checklist
scope: `C001_kernel_to_criterion` only
source boundary: `LinearMap.ker_restrict` -> `LinearMap.injective_restrict_iff_disjoint`
related artifact: `docs/hmdg/C001_kernel_to_criterion_expansion.md`

## Purpose

This document defines the review procedure for C001 before any status change is considered.

It does not accept C001 as a stable ERG kernel definition.

It does not prove the final target theorem.

It is a checklist for deciding whether the existing candidate bridge is mathematically faithful enough to keep as one HMDG phase-level node.

## Current candidate claim

C001 currently claims that the compressed boundary

```text
LinearMap.ker_restrict
→ LinearMap.injective_restrict_iff_disjoint
```

can be read as the human-facing bridge:

```text
kernel_to_criterion
```

The intended cognitive transition is:

```text
kernel of restricted map
→ zero-kernel condition for injectivity
→ no nonzero element in p ∩ ker f
→ disjointness of p and ker f
```

## Required source checks

Before changing C001's status, check the current mathlib declarations directly.

### Check 1: source declaration

Verify that `LinearMap.ker_restrict` is accurately described as a statement about the kernel of a restricted map being obtained from the original kernel through the restricted domain/subtype/comap structure.

Record:

```text
current declaration name:
current file path:
statement shape:
main hypotheses:
conclusion shape:
uses comap/subtype/restrict structure: yes/no
plain-language description faithful: yes/no/needs revision
```

### Check 2: target declaration

Verify that `LinearMap.injective_restrict_iff_disjoint` is accurately described as an injectivity criterion for a restricted map in terms of disjointness between the submodule and the original kernel.

Record:

```text
current declaration name:
current file path:
statement shape:
main hypotheses:
conclusion shape:
uses Disjoint with LinearMap.ker: yes/no
plain-language description faithful: yes/no/needs revision
```

### Check 3: theorem proximity

Check whether the source and target declarations are close enough that one ConceptBridge node is appropriate.

Acceptable evidence:

```text
Both declarations operate on the same restricted-map/kernel theme.
The target can be reached by adding the standard linear-map fact: injective iff kernel is bottom.
The disjointness condition is the lattice-level form of the restricted kernel being trivial.
```

Warning signs:

```text
The target uses extra hypotheses not represented in the C001 explanation.
The source declaration has a materially different statement shape than described.
The target theorem is not actually about the same restriction/comap situation.
The bridge hides a nontrivial theorem that should be its own ConceptBridge.
```

## Candidate split decision

The current candidate split is:

```text
kernel_to_zero_kernel
zero_kernel_to_disjointness
```

Use this decision rule:

```text
Keep C001 as one node if the proof route mainly uses standard kernel/injectivity/disjointness translations.
Split C001 if the proof route requires a separate non-obvious lattice transformation or a theorem whose role is not visible from the current bridge label.
```

## Review outcomes

Use one of the following review outcomes.

```text
keep_candidate_one_node
keep_candidate_but_reword
split_candidate
reject_candidate_bridge
needs_source_check
```

Do not use `accepted` in this file unless the repository has a separate accepted-status policy for HMDG nodes.

## Minimum review note template

```text
reviewer:
date:
mathlib commit/ref:
source declaration checked: yes/no
target declaration checked: yes/no
plain-language source description: faithful / revise / wrong
plain-language target description: faithful / revise / wrong
bridge granularity: keep one node / split / uncertain
recommended outcome:
notes:
```

## Non-goals

This checklist does not update `data/hmdg/concept_patch.json`.

This checklist does not change the renderer.

This checklist does not review C002 or C003.

This checklist does not promote C001 to an accepted ERG kernel definition.
