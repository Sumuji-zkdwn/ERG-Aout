# ERG-TAO Math Toy Model

このリポジトリは、ERG（Explicit Relational Graph）を数学的トイモデルとして固めるための外部ログである。

## Current accepted kernel

現時点の最小核は次の通り。

1. ERG is treated as a typed directed multigraph.
2. Nodes represent artifacts such as messages, propositions, definitions, examples, operations, files, commits, and decisions.
3. Edges represent typed relations such as `refines`, `rejects`, `depends_on`, `contradicts`, `implements`, `logs`, and `supersedes`.
4. A claim is not accepted merely because it appears in conversation.
5. A claim becomes stable only when it is represented in `docs/FORMALIZATION.md`, checked by a critic role, and reflected in `docs/CONVERGENCE.md`.

## Repository roles

- `README.md`: stable public-facing summary.
- `docs/FORMALIZATION.md`: current mathematical formalization.
- `docs/CONVERGENCE.md`: convergence criteria and observed changes.
- `logs/`: GPT/Codex round logs.
- `decisions/`: accepted decisions.
- `proposals/`: unaccepted proposals.
- `erg_store/`: optional generated JSONL graph data.

## Working rule

README is not a scratchpad.
Unstable ideas go to `proposals/` or `logs/`.
Accepted definitions are promoted only after review.

## R001 validator (minimal kernel check)

- Schema: `schema/r001_graph.schema.json`
- Validator: `tool/validate_r001_kernel.py`
- Inspector: `tool/inspect_r001_graph.py`
- Minimal examples: `examples/r001/minimal_valid.json`, `examples/r001/invalid_cycle_and_policy.json`, `examples/r001/invalid_duplicate_node_id.json`, `examples/r001/invalid_missing_edge_endpoint.json`, `examples/r001/invalid_extends_main_outside_accepted.json`, `examples/r001/invalid_node_type_for_layer.json`
- Handmade samples: `examples/r001/sample_conversation_graph.json`, `examples/r001/sample_r001_development_graph.json`

Validate:

```bash
python tool/validate_r001_kernel.py examples/r001/minimal_valid.json
python tool/validate_r001_kernel.py examples/r001/sample_conversation_graph.json
python tool/validate_r001_kernel.py examples/r001/sample_r001_development_graph.json
```

Inspect:

```bash
python tool/inspect_r001_graph.py examples/r001/sample_conversation_graph.json
python tool/inspect_r001_graph.py examples/r001/sample_r001_development_graph.json
```

The validator enforces only documented R001 invariants:
- `extends_main` acyclic + single linear canonical path.
- `extends_branch` cannot modify canonical path nodes.
- documented cross-layer endpoint policies only.

The inspector is a read-only helper. It first validates a R001 graph, then prints node counts by layer, edge counts by type, the `extends_main` canonical chain, and `extends_branch` edges.
