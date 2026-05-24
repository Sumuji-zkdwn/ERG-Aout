# R002 Plan (kickoff fixed after R001 closeout)

この文書は、R001 closeout を受けて R002 の開始計画を固定するための計画ノートである。  
R002 は R001 の手動写像ルールを前提にし、より大きな会話ログへの適用可能性を高める。  
ただし R002 の開始段階では完全自動化を目標にせず、**半自動写像補助・整合性検査・候補提示**を最小範囲として進める。

## 1) R002 の目的

- `docs/R001_MANUAL_MAPPING_RULES.md` で固定された manual mapping rules を運用前提にする。
- 小規模例で成立した R001 の写像手順を、より大きな conversation log に適用できる形へ段階的に拡張する。
- 初期スコープは「人手中心 + 補助機能」であり、次を優先する。
  - mapping candidate の提示
  - mapping consistency の検査
  - larger log 適用時の作業手順の明確化

## 2) R002 の入力（固定）

R002 の開始時点で参照する入力は次に固定する。

- `docs/R001_CLOSEOUT.md`
- `docs/R001_STATUS.md`
- `docs/R001_MANUAL_MAPPING_RULES.md`
- `docs/R001_MANUAL_EXAMPLE.md`
- `examples/r001/manual_conversation_to_erg_example.json`
- `examples/r001/manual_conversation_cpr_origin_example.json`
- `tool/validate_r001_kernel.py`
- `tool/inspect_r001_graph.py`
- `tool/export_r001_dot.py`

## 3) R002 の最小成果物

R002 完了時に最低限そろえる成果物を次とする。

1. larger manual conversation example
2. mapping candidate checklist（`docs/R002_MAPPING_CHECKLIST.md`）
3. consistency check checklist（`docs/R002_MAPPING_CHECKLIST.md`）
4. R002 handoff note（`docs/R002_HANDOFF.md`）
5. raw text attachment strategy note（`docs/R002_RAW_TEXT_ATTACHMENT_STRATEGY.md`）

## 4) Workstream 分割（R002-A / R002-B / R002-C）

### R002-A: manual mapping support

- 手動写像作業の補助に必要なチェック項目・候補提示の型を整理する。
- 人手の判断点（曖昧箇所、分岐箇所、保留判断）を明示する。

### R002-B: mapping consistency checks

- 手動写像結果の整合性確認手順を定義する。
- R001 kernel validator/inspector を前提に、写像過程で見落としやすい不整合を checklist 化する。

### R002-C: larger conversation log application

- 小規模例より大きい会話ログに対し、R002-A/B で定義した手順を適用する。
- 適用結果を handoff 可能な形でまとめ、次ラウンドへ渡す。
- larger manual example（`examples/r002/larger_manual_conversation_example.json`）と companion note（`docs/R002_LARGER_MANUAL_EXAMPLE.md`）を R002-C の最初の適用実例として参照する。
- 次の R002-C planning artifact として `docs/R002_REAL_LOG_PILOT_PLAN.md` を参照し、1件の bounded real log excerpt pilot を documentation-first で進める。

## 5) R002 でまだやらないこと（明示的に除外）

以下は R002 の非目標として明示し、実装・主張を行わない。

- full automatic conversation ingestion
- full automatic concept extraction
- convergence scoring
- GIF/DIF semantics
- sigma semantics
- recency
- branch_degree
- semantic importance scoring

## 6) 境界条件

- R002 は計画固定を目的とし、新しい理論主張を追加しない。
- R001 で確定した schema / validator / examples（JSON）を変更しない前提で進める。
- 実装先行ではなく、手動運用を壊さない段階的拡張を優先する。
