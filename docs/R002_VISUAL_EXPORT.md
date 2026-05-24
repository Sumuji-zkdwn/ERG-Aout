# R002 Visual Export (matplotlib/networkx)

## 1) Purpose

`tool/export_r002_visual.py` は、R001/R002 graph JSON を Graphviz 非依存で静的 PNG に描画する manual review 補助ツールです。  
semantic capability を追加するものではなく、既存の manual mapping 結果を見やすく確認するための補助です。

## 2) Recommended first commands

まずは次の順で確認することを推奨します。

- accepted view（accepted 構造の確認）
- full view（raw/candidate/accepted の対応確認）
- spine view（extends_main 主線の確認）

```bash
python tool/export_r002_visual.py examples/r002/real_log_pilot_01.json \
  --sidecar examples/r002/real_log_pilot_01_raw_text_sidecar.md \
  -o real_log_pilot_01_accepted.png --view accepted --label-mode excerpt

python tool/export_r002_visual.py examples/r002/real_log_pilot_01.json \
  --sidecar examples/r002/real_log_pilot_01_raw_text_sidecar.md \
  -o real_log_pilot_01_full.png --view full --label-mode excerpt

python tool/export_r002_visual.py examples/r002/real_log_pilot_01.json \
  -o real_log_pilot_01_spine.png --view spine --label-mode id
```

## 3) Label modes

- `id`: 安定した技術確認向け（node id 中心）
- `short`: compact 表示（id の人間可読短縮）
- `excerpt`: sidecar の `text_excerpt` を優先して review 可読性を上げる
- `id_excerpt`: id と excerpt を併記して traceability を維持

`--max-label-chars` で表示長を制限し、長文ラベルは改行して PNG の可読性を保ちます。

## 4) Caveats

- 出力は static PNG であり、hover や interactive 展開はありません。
- redacted sidecar excerpt は可読性を改善しますが、元会話の完全 context を復元できるわけではありません。
- これは automatic ingestion、automatic candidate generation、semantic scoring ではありません。

## 5) Example commands (real_log_pilot_01)

```bash
python tool/export_r002_visual.py examples/r002/real_log_pilot_01.json \
  --sidecar examples/r002/real_log_pilot_01_raw_text_sidecar.md \
  -o real_log_pilot_01_full.png --view full --label-mode excerpt

python tool/export_r002_visual.py examples/r002/real_log_pilot_01.json \
  --sidecar examples/r002/real_log_pilot_01_raw_text_sidecar.md \
  -o real_log_pilot_01_accepted.png --view accepted --label-mode short

python tool/export_r002_visual.py examples/r002/real_log_pilot_01.json \
  -o real_log_pilot_01_spine.png --view spine --label-mode id
```
