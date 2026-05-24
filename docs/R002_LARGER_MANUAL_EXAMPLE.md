# R002 Larger Manual Conversation Example

この文書は、`examples/r002/larger_manual_conversation_example.json` の読み方を説明する companion note である。

## 目的

この example は、R002-C（larger conversation log application）の最初の実例として、
R001 で確立した手動写像の形を少し大きな会話ログへ適用するために追加した。

## R001 形式をそのまま使う理由

R002 の初期段階では schema 拡張や理論拡張を行わず、R001 の kernel JSON 形式（`nodes` / `edges` / layer / type / edge type）をそのまま使う。
これにより、既存の validator / inspector を継続利用でき、手動写像の再現性を確保できる。

## raw / candidate / accepted の読み方

- `L_raw` の `RawMessage` は、会話ログ上の発話断片を表す。
- `L_candidate` の `CandidateDefinition` は、raw から抽出した候補概念を表す。
- `L_accepted` の `KernelDefinition` / `KernelDecision` は、候補から採択された定義・判断を表す。

## main spine の読み方

accepted の主系列は次の順で進む。

- `acc.r001_closeout_fixed`
- `acc.r002_plan_fixed`
- `acc.mapping_checklist_fixed`
- `acc.larger_log_application_started`
- `acc.r002_handoff_prepared`

この spine は `extends_main` で接続され、R001 closeout から R002 handoff 準備までの自然な進行を示す。

## branch の読み方

本 example では、`extends_branch` を使って「今回は採用しないが判断は記録する」側線を置く。

- `acc.defer_full_automatic_ingestion`: full automatic ingestion は R002 非目標として defer。
- `acc.defer_gif_dif_sigma_scoring`: GIF/DIF / sigma / convergence scoring は後続課題として defer。

## unaccepted candidates の読み方

以下の candidate は意図的に unaccepted のまま残している（`accepted_from_candidate` を張らない）。

- `cand.full_auto_ingestion_now`
- `cand.gif_dif_semantics_now`
- `cand.sigma_scoring_now`

これらは「将来候補」または「時期尚早な提案」を raw/candidate 層に保持する例である。

## R002-C の最初の実例であること

この example は、R002-C の最初の larger log application 実例として位置づける。
小規模な R001 manual examples よりノード数・関係数を増やし、
手動写像手順（候補抽出、採択、保留、分岐記録）の運用感を確認する。

## 自動化ではなく手動写像例であること

この example は automatic ingestion / automatic concept extraction の実装例ではない。
あくまで人手中心の写像を、R001 形式で少し大きなログに適用した manual mapping example である。


## raw text sidecar 参照

raw node id と発話断片の対応は、人工的 sidecar 実例 `examples/r002/larger_manual_conversation_raw_text_sidecar.md` を参照。


## sidecar consistency checker 実行例

`raw` 対応の補助確認として、次を実行できる。

```bash
python tool/check_r002_sidecar_consistency.py \
  examples/r002/larger_manual_conversation_example.json \
  examples/r002/larger_manual_conversation_raw_text_sidecar.md
```

## accepted decision warning について

現在の `examples/r002/larger_manual_conversation_example.json` では、defer 系 `KernelDecision`（`acc.defer_full_automatic_ingestion` / `acc.defer_gif_dif_sigma_scoring`）が `accepted_from_candidate` を持たない。

そのため、`tool/check_r002_mapping_consistency.py` 実行時に warning として現れる。

今後の整理候補として、defer decision も raw -> candidate -> accepted の昇格経路で表現する方向がある（詳細は `docs/R002_ACCEPTED_DECISION_PROMOTION_POLICY.md` を参照）。

