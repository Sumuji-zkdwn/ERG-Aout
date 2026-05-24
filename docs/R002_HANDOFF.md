# R002 Handoff Note

この文書は、R002 初期成果物（larger manual mapping の最初の固定）を受けて、
確認できたこと・未解決点・次フェーズ候補を整理し、次ラウンドへ引き渡すための handoff note である。

## 1) R002 でそろった成果物

- `docs/R002_PLAN.md`
- `docs/R002_MAPPING_CHECKLIST.md`
- `examples/r002/larger_manual_conversation_example.json`
- `docs/R002_LARGER_MANUAL_EXAMPLE.md`

## 2) R002 で確認できたこと

- R001 kernel JSON 形式のまま、少し大きめの manual conversation mapping を表現できる。
- existing validator / inspector をそのまま再利用できる。
- accepted main spine と branch を分けて保持できる。
- unaccepted candidates を candidate 層に残せる。
- full automatic ingestion や GIF/DIF / sigma / convergence scoring を、まだ非目標として分離できる。

## 3) R002 でまだ解決していないこと

- automatic conversation ingestion は未実装。
- automatic concept extraction は未実装。
- mapping candidate の自動生成は未実装。
- consistency check の自動化は未実装。
- larger_manual_conversation_example.json に関する defer 系 accepted decision warning（accepted_from_candidate 欠落）は解消済み。
- accepted decision promotion policy の実装強制（schema/checker 振る舞い固定）は未実施（文書化は実施済み）。
- raw message の本文保持・参照方法はまだ最小例レベル。
- GIF/DIF / sigma / recency / branch_degree / semantic importance scoring は未導入。

## 4) 次フェーズ候補

- checklist-driven consistency helper（最小実装: `tool/check_r002_mapping_consistency.py`）
- accepted decision promotion policy を文書化（`docs/R002_ACCEPTED_DECISION_PROMOTION_POLICY.md`）
- candidate review table
- larger real conversation log mapping
- raw text attachment strategy（文書化済み: `docs/R002_RAW_TEXT_ATTACHMENT_STRATEGY.md`）
- external-reference contamination audit 実施（`docs/R002_EXTERNAL_REFERENCE_CONTAMINATION_AUDIT.md`）
- optional DOT visualization for R002 example

## 5) R002 の境界再確認

- この handoff は新しい理論主張ではない。
- schema / validator / JSON spec は変更しない。
- R002 は完全自動化ではなく、manual mapping を壊さない補助層として始まった。
