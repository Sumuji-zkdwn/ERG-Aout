# R001 Status

この文書は、R001 の到達点と境界を固定し、R002 以降で追加する対象を明確化するためのステータス整理である。

## R001 で現在できること

R001 の範囲では、次が実装・文書化済みである。

- graph JSON validation
- extends_main / extends_branch validation
- DOT export
- full / accepted / spine projection
- short labels
- edge semantics document
- semantics coverage checker
- PR #28 までのR001作業を反映した development sample graph
- manual conversation examples
- manual example reading guide
- manual mapping rules extracted from existing examples

## R001 でまだできないこと

R001 の範囲では、次は未実装・未確立である。

- automatic conversation ingestion
- automatic concept extraction
- convergence scoring
- GIF/DIF semantics
- sigma semantics
- recency
- branch_degree
- semantic importance scoring

## R002 候補

manual conversation-to-ERG example は R001 内の手動適用例として追加済みである。

R002 以降では、これらの手動例と manual mapping rules をもとに、
半自動化・検査補助・より大きな会話ログへの適用を検討する。

現在の手動例:
- `examples/r001/manual_conversation_to_erg_example.json`
- `examples/r001/manual_conversation_cpr_origin_example.json`

関連文書:
- `docs/R001_MANUAL_EXAMPLE.md`
- `docs/R001_MANUAL_MAPPING_RULES.md`

## Scope note

本メモはステータス整理のみを目的とし、新しい理論主張を導入しない。
