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
- `docs/R001_STATUS.md`: R001 の到達点・境界・R002候補の整理。
- `docs/R001_CLOSEOUT.md`: R001 closeout（到達点・境界・R002へ渡す入力）の固定。
- `docs/R002_PLAN.md`: R001 closeout を受けた R002 開始計画（目的・入力・最小成果物・非目標）の固定。
- `docs/R002_MAPPING_CHECKLIST.md`: R002 の manual mapping 補助チェックリスト（候補抽出・判断・整合性確認）。
- `docs/R002_LARGER_MANUAL_EXAMPLE.md`: R002-C の最初の larger manual conversation example の読み方。
- `docs/R002_HANDOFF.md`: R002 初期成果物の handoff（確認事項・未解決点・次フェーズ候補・境界）の整理。
- `docs/R001_MANUAL_EXAMPLE.md`: `manual_conversation_to_erg_example.json` の companion reading note.
- `docs/R001_MANUAL_MAPPING_RULES.md`: 2つの manual conversation example から読める手動写像ルール。
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
- R002 mapping consistency helper: `tool/check_r002_mapping_consistency.py` (checklist-driven manual mapping aid; run validator first)
- Minimal examples: `examples/r001/minimal_valid.json`, `examples/r001/invalid_cycle_and_policy.json`, `examples/r001/invalid_duplicate_node_id.json`, `examples/r001/invalid_missing_edge_endpoint.json`, `examples/r001/invalid_extends_main_outside_accepted.json`, `examples/r001/invalid_node_type_for_layer.json`
- Handmade samples: `examples/r001/sample_conversation_graph.json`, `examples/r001/sample_r001_development_graph.json`, `examples/r001/manual_conversation_to_erg_example.json`, `examples/r001/manual_conversation_cpr_origin_example.json`
- Larger R002 sample: `examples/r002/larger_manual_conversation_example.json`

Validate:

```bash
python tool/validate_r001_kernel.py examples/r001/minimal_valid.json
python tool/validate_r001_kernel.py examples/r001/sample_conversation_graph.json
python tool/validate_r001_kernel.py examples/r001/sample_r001_development_graph.json
```

R002 mapping consistency helper (after validator):

```bash
python tool/check_r002_mapping_consistency.py examples/r002/larger_manual_conversation_example.json
```

Inspect:

```bash
python tool/inspect_r001_graph.py examples/r001/sample_conversation_graph.json
python tool/inspect_r001_graph.py examples/r001/sample_r001_development_graph.json
```


Coverage check (graph edge types vs semantics):

```bash
python tool/check_r001_semantics_coverage.py \
  examples/r001/sample_r001_development_graph.json \
  docs/R001_SEMANTICS.md
```

The validator enforces only documented R001 invariants:
- `extends_main` acyclic + single linear canonical path.
- `extends_branch` cannot modify canonical path nodes.
- documented cross-layer endpoint policies only.

The inspector is a read-only helper. It first validates a R001 graph, then prints node counts by layer, edge counts by type, the `extends_main` canonical chain, and `extends_branch` edges.
