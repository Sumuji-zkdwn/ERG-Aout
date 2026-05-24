# R002 Mapping Checklist（manual mapping 補助）

Status: practical checklist (R002 kickoff aid).

この文書は、`docs/R001_MANUAL_MAPPING_RULES.md` に基づいて、manual mapping 作業時の候補抽出・判断・整合性確認をチェックリスト化した補助ノートである。  
対象は **R001 manual mapping rules の運用補助のみ**であり、schema / validator / JSON examples / 新規理論主張は変更しない。

## 前提

- 判断の根拠は `docs/R001_MANUAL_MAPPING_RULES.md` と既存 manual examples の読解範囲に限定する。
- これはアルゴリズム仕様ではなく、人手作業時の見落とし防止 checklist である。

## 1) raw node 候補を選ぶ checklist

- [ ] 会話断片を「まだ candidate / accepted に整形していない入力側アンカー」として保持する必要があるか。
- [ ] 後続で `introduces` または `mentions` の起点として使う見込みがあるか。
- [ ] 候補化・採択判断の前段として、出発点を残す価値があるか。
- [ ] raw に置いた理由を短く説明できるか（例: どの概念候補の出発点になるか）。

## 2) candidate node 候補を選ぶ checklist

- [ ] raw 断片から概念単位へ整形した「概念候補」として表現できているか。
- [ ] どの raw から来た候補かを `introduces` で結べるか。
- [ ] accepted へ昇格する可能性がある候補か、あるいは保留候補として残す意味があるか。
- [ ] candidate 名称が、元 raw と照合して過不足なく読めるか。

## 3) accepted に昇格させるか判断する checklist

- [ ] candidate を「受理して核に載せる」判断が明示できるか。
- [ ] 昇格時に `accepted_from_candidate` を張る対象 candidate が一意に定まっているか。
- [ ] raw からの `mentions`（参照）と、candidate から accepted への昇格を混同していないか。
- [ ] 昇格後に、主線/分岐どちらへ接続するかの見通しがあるか。

## 4) extends_main に置くか extends_branch に置くか判断する checklist

- [ ] 接続元・接続先がいずれも accepted node か。
- [ ] この遷移を canonical spine（主線）として残すべきか。
- [ ] 主線ではないが、受理済みの分岐として保持したい遷移か。
- [ ] 主線に置く理由（正準進行）と、分岐に置く理由（非主線だが保持）を区別して説明できるか。

判定の目安:

- `extends_main`: accepted 間の正準進行として残す。
- `extends_branch`: accepted 間の非主線分岐として残す。

## 5) unaccepted candidate として残す判断 checklist

- [ ] candidate としては記録価値があるが、現時点で accepted 核へ入れない判断か。
- [ ] raw から candidate への `introduces` はあるか。
- [ ] 当該 candidate に `accepted_from_candidate` を張っていないか。
- [ ] 「unaccepted」として残す理由（保留・比較候補など）を簡潔に説明できるか。

## 6) mentions edge を張る判断 checklist

- [ ] raw 断片が accepted 概念への参照・言及をしているか。
- [ ] `introduces`（raw -> candidate）と用途が異なることを確認したか。
- [ ] `accepted_from_candidate`（candidate -> accepted）と用途が異なることを確認したか。
- [ ] 「概念を作った」のではなく「既存 accepted に言及した」関係として妥当か。

## 7) consistency check checklist

以下は manual mapping 後に毎回確認する。

補助として、`tool/check_r002_mapping_consistency.py` により本節の一部を機械的に点検できる（ただし validator の代替ではない）。checker 出力では、不整合 warning と確認用 note が分離表示される。

- [ ] `accepted_from_candidate` を持たない accepted がないか。
- [ ] `unaccepted` と名付けた candidate が accepted に昇格していないか。
- [ ] branch target が main spine に混ざっていないか。
- [ ] raw -> candidate の `introduces` が不足していないか。
- [ ] raw -> accepted の `mentions` と candidate 昇格を混同していないか。

## 8) 最小運用手順（推奨）

1. raw 候補を先に置く（入力アンカー確保）。
2. raw から candidate を `introduces` で結ぶ。
3. candidate ごとに accepted 昇格可否を判断し、昇格時のみ `accepted_from_candidate` を張る。
4. accepted 間の接続を `extends_main` / `extends_branch` で仕分ける。
5. raw から accepted への参照がある箇所だけ `mentions` を張る。
6. 最後に consistency checklist を通す。

