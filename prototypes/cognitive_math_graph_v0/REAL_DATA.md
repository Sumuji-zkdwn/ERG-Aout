# Real Data Input Notes

This prototype does not commit large mathlib dependency files into the repository.

Instead, it provides a real-data loader that can consume external mathlib dependency graphs placed under:

```text
prototypes/cognitive_math_graph_v0/data/external/
```

## Source A: Mathlib4 Theorem Dependency Graph

Recommended first real dataset:

```text
Mathlib4 Theorem Dependency Graph
LeanDojo Benchmark 4, v10
Format: GEXF / GraphML-compatible NetworkX graph
Scale: about 137k nodes and 304k edges
Property: DAG
```

This graph is easier for v1 because edges are theorem-to-theorem proof dependencies and the graph is reported as a DAG.

Expected local path:

```text
prototypes/cognitive_math_graph_v0/data/external/mathlib4_dependency_graph.gexf
```

Run:

```bash
python prototypes/cognitive_math_graph_v0/run_real_graph.py \
  --input prototypes/cognitive_math_graph_v0/data/external/mathlib4_dependency_graph.gexf \
  --target-substring LinearMap \
  --target-substring ker
```

## Source B: MathlibGraph

Larger declaration/module/namespace graph:

```text
MathNetwork/MathlibGraph
Lean 4 / Mathlib graph at commit 534cf0b, 2026-02-02
Declaration layer: about 308k nodes and 8.4M edges
Module layer: about 7.5k nodes and 20k edges
Namespace layer: about 10k nodes and 332k edges
```

For a first run, prefer the module or namespace layer, because declaration-level CSV can be too large for an exploratory local run.

Expected local CSV paths can be any edge list with one of these source/target column pairs:

```text
source,target
src,dst
from,to
from_id,to_id
source_id,target_id
```

Run example:

```bash
python prototypes/cognitive_math_graph_v0/run_real_graph.py \
  --input prototypes/cognitive_math_graph_v0/data/external/edges.csv \
  --target-substring LinearAlgebra
```

## What the real loader does

The loader:

1. reads GEXF, GraphML, or CSV edge lists;
2. searches target nodes by substring;
3. extracts the ancestor subgraph of the chosen target;
4. condenses SCCs if the graph is not a DAG;
5. assigns rough cognitive role weights from declaration names;
6. penalizes likely technical nodes such as simp, inst, coercions, and typeclass artifacts;
7. extracts a weighted longest path ending at the target;
8. writes Markdown and JSON outputs.

## Important limitation

This is still not a human-verified cognitive graph.

It is a real-data extraction pass over formal dependency data. The result should be treated as a candidate HMDG spine, not as an accepted mathematical explanation.
