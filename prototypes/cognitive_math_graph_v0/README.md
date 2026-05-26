# Cognitive Math Graph v0

Purpose:
  Prototype a Human Mathematical Dependency Graph (HMDG) workflow.

This is not yet a mathlib extractor. It is a runnable seed prototype that uses a hand-built Jordan normal form cognitive DAG to test the core idea:

```text
formal/cognitive dependency DAG
→ role and edge weighting
→ technical-node penalty
→ weighted longest path
→ main cognitive path + side branches + node cards
```

The goal is not to produce another explanation of Jordan normal form. The goal is to test whether a mathematical concept can be represented as a generation path whose structure is readable before adding prose explanations.

## Run

From the repository root:

```bash
python prototypes/cognitive_math_graph_v0/scripts/run_sample.py
```

Outputs are written to:

```text
prototypes/cognitive_math_graph_v0/outputs/sample_jordan/
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

## Design stance

- Do not classify primarily by mathematical field.
- Classify nodes by cognitive role: object, operation, failure, repair, invariant, quotient, decomposition, normal_form, etc.
- Classify edges by semantic relation: requires, constructs, detects_failure, repairs, measures, normalizes_to, etc.
- Use weighted longest paths, not shortest paths.
- Penalize technical/implementation-support nodes.
- Treat side branches as useful revisits without letting them create cycles in the main DAG.

## Next step

Replace the hand-built CSV graph with a mathlib / LeanDojo / GraphML / GEXF input adapter, then run the same weighted-longest-path logic against real formal dependency data.
