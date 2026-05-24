# R002 Raw Text Attachment Strategy

この文書は、R002 の次フェーズ候補として、raw node と元発話本文の対応方法を **schema を変更せずに固定** するための strategy note である。

## 1) 目的

- graph JSON 内の raw node id だけでは、元発話本文との対応が薄い。
- larger real conversation log mapping に進む前に、raw node と元発話断片の対応方法を固定する。
- ただし R001/R002 の kernel JSON schema は変更しない。

## 2) 基本方針

- graph JSON には raw node id を置く。
- 発話本文・話者・時系列番号・出典メモは、別の sidecar document に置く。
- graph JSON と raw text sidecar は raw node id で対応させる。
- これにより schema / validator を変更せずに、元発話参照を保持できる。

## 3) Sidecar document の推奨形式

推奨配置先:

- `docs/` または `examples/r002/` 配下

推奨表現形式:

- Markdown table

推奨 columns:

- `raw_id`
- `turn_index`
- `speaker`
- `text_excerpt`
- `source_note`
- `mapping_note`

最小イメージ:

| raw_id | turn_index | speaker | text_excerpt | source_note | mapping_note |
|---|---:|---|---|---|---|
| L_raw_001 | 12 | user | 「〜したい」(要約) | meeting-log-2026-05-01 | introduces C_cand_x |

## 4) raw_id 対応ルール

- `raw_id` は graph JSON の `L_raw` node id と完全一致させる。
- `raw_id` は stable identifier として扱う。
- 本文を編集しても `raw_id` をむやみに変えない。
- 1 つの raw node は、原則として 1 つの会話断片または短い連続発話に対応させる。

## 5) text_excerpt の扱い

- 長文全体を必ず graph JSON に入れない。
- sidecar には必要最小限の引用・要約・位置情報を置く。
- 長いログの場合は、全文保存ファイルと `raw_id` table を分けてもよい。
- 個人情報や秘密情報がある場合は、sidecar に入れる前に注意する。

## 6) mapping_note の扱い

`mapping_note` には、次を短く書けるようにする。

- その raw がどの candidate を introduces するのか
- どの accepted に mentions しているのか
- なぜ raw として切ったのか

## 7) この strategy がやらないこと

この文書は次を対象外とする。

- schema は変更しない
- validator は変更しない
- raw node に text field を追加しない
- automatic conversation ingestion は実装しない
- automatic concept extraction は実装しない
- full raw log storage policy はまだ確定しない
- GIF/DIF / sigma / convergence scoring は扱わない

## 8) 運用上の位置づけ

- 本 strategy は、larger real conversation log mapping へ進む前段の固定ルールである。
- 実装を先行せず、manual mapping の追跡可能性を維持するための文書化に限定する。
