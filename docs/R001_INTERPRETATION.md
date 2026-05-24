# R001 interpretation notes

Status: explanatory note.

This document explains how to read the current R001 sample graph and DOT projection views. It does not change the R001 kernel, JSON schema, or graph data format.
For edge-level interpretation details, see `docs/R001_SEMANTICS.md`.

## Current object

An R001 graph is currently a validated typed directed graph with four layers:

- `L_raw`: source-side messages, artifacts, and observations.
- `L_candidate`: candidate definitions, claims, examples, questions, and symbols.
- `L_accepted`: accepted kernel objects for the current round.
- `L_gitlog`: observations derived from git history.

The main accepted-layer distinction is:

- `extends_main`: the canonical accepted path.
- `extends_branch`: a non-canonical accepted branch.

## Why projection views are needed

A full R001 graph keeps raw structure, candidate structure, accepted structure, and git observations together. This is useful for preservation and checking, but it is visually dense.

Therefore, DOT output should be read through projections.

## Views

### `--view full`

Shows all nodes and edges. Use it as the storage/debug view.

### `--view accepted`

Shows only `L_accepted` nodes and the `extends_main` / `extends_branch` edges among them. Use it to inspect what has been accepted and what is main versus branch.

### `--view spine`

Shows only the `extends_main` canonical chain. Use it to inspect the current accepted line of development.

## Label modes

`--node-label short` and `--edge-label none|type` are presentation controls. They do not change graph identity.

Recommended human-first commands:

```powershell
python tool/export_r001_dot.py examples/r001/sample_r001_development_graph.json --view spine --node-label short --edge-label none -o r001_spine_clean.dot
dot -Tpng r001_spine_clean.dot -o r001_spine_clean.png

python tool/export_r001_dot.py examples/r001/sample_r001_development_graph.json --view accepted --node-label short --edge-label type -o r001_accepted_clean.dot
dot -Tpng r001_accepted_clean.dot -o r001_accepted_clean.png
```

Recommended debug command:

```powershell
python tool/export_r001_dot.py examples/r001/sample_r001_development_graph.json --view full --node-label id --edge-label id -o r001_full_debug.dot
dot -Tpng r001_full_debug.dot -o r001_full_debug.png
```

## Reading the current development sample

The spine view reads the accepted line:

```text
PR 10: r001 kernel
  -> PR 11: schema validator
  -> PR 14: validator hardening
  -> PR 16: sample graph
  -> PR 17: inspection cli
```

The accepted view adds branches. A branch is retained, but it is not part of the canonical spine.

The full view should be used when the question concerns how source artifacts, candidate objects, accepted nodes, and git observations relate.

## Current boundary

R001 currently supports writing small graph JSON files, validating them, inspecting them, exporting DOT, and viewing full / accepted / spine projections.

R001 does not yet support automatic source ingestion, automatic git-history graph generation, stored semantic labels in the schema, convergence scoring, GIF/DIF semantics, sigma, recency, or branch-degree semantics.

## Working interpretation

```text
R001 graph:
  preservation object

full view:
  storage/debug projection

accepted view:
  accepted-state projection

spine view:
  canonical-progress projection

clean labels:
  human-readable rendering layer
```
