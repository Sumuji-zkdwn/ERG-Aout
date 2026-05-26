# HMDG_SPEC_v0

HMDG = Human Mathematical Dependency Graph.

## Purpose

The goal is not to divide mathematics into fields.

The goal is to transform a formal or semi-formal dependency graph into a graph that exposes how a human can generate a concept without losing the intermediate structure.

This prototype treats mathematical understanding as a structured path through objects, operations, failures, repairs, invariants, decompositions, quotients, and normal forms.

## Core rules

1. Field names are not primary structure.
2. Nodes are classified by cognitive role.
3. Edges are classified by semantic relation.
4. Use weighted longest paths, not shortest paths.
5. Raw formal dependency graphs are not automatically human understanding orders.
6. Technical / implementation / simp / typeclass nodes should be penalized.
7. Failure / repair / invariant / quotient / decomposition / normal_form nodes should be emphasized.
8. Output should be node cards, typed edges, main path, and branches before prose explanation.
9. Revisit edges should not be allowed to create cycles in the main path DAG; represent them as side branches or condense SCCs.
10. Mathematical fields may appear later as clusters, but should not be injected as the initial partition.

## Node roles

```text
object
operation
constraint
failure
repair
kernel
image
quotient
invariant
decomposition
transfer
normal_form
example
technical
unknown
```

## Edge types

```text
requires
defines
constructs
detects_failure
repairs
measures
quotients_by
decomposes_into
normalizes_to
transfers_to
compresses
expands
technical_support
unknown
```

## Weighted longest path

For a target node `T`, the main cognitive path is the maximum-score path ending at `T`:

```text
score(path) = sum(node_weight) + sum(edge_weight)
```

This is not a proof-shortening path.

It is intended as a concept-generation spine.

## Branches

Branches are nodes adjacent to the main path but not selected as the spine.

Branches can hold examples, counterexamples, alternative constructions, technical anchors, or revisits.

## Current v0 sample

Target:

```text
jordan_normal_form
```

Expected main path:

```text
vector_space
→ linear_map
→ eigenvalue
→ eigenvector
→ diagonalization
→ failure_not_enough_eigenvectors
→ generalized_eigenvector
→ generalized_eigenspace
→ nilpotent_operator
→ kernel_growth_sequence
→ dimension_difference
→ jordan_chain
→ chain_basis
→ jordan_block
→ jordan_normal_form
```

## Next implementation step

Add an adapter for mathlib / LeanDojo / GraphML / GEXF dependency data, then use this same weighted-longest-path extraction on real formal dependency graphs.
