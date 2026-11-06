# primitive-lean 未統合 PR の棚卸し（2026-11-07）

primitive-lean の未統合 PR 58 件を、ERG の 1 ラウンドとして記録したもの。判定案はすべて **候補** であり、採否はまだ決まっていない。

## 入力

- `main` = `67fdf6b`。PR ヘッドは 2026-11-07 時点のもの
- primitive-lean `tools/deps/` による測定
  - 構造：PR ごとの Lean ファイルとブロブ SHA、積み重なりの親子、包含、同一内容、同名異版
  - カーネル：各 PR ヘッドで、そのヘッド自身の `--proof-only` 検査を実行し、Lean が受理した型・証明項から依存を抽出
  - CI：GitHub Actions の履歴を PR ヘッドの SHA で突き合わせ
- 測定の詳細と数値は primitive-lean の `docs/dependency/pr-inventory/` を正とする

## このディレクトリの中身

| ファイル | 内容 |
|---|---|
| `graph.json` | R001 形式のグラフ。`tool/validate_r001_kernel.py` で VALID |
| `evidence.md` | PR ごとの数値と、判定案を出した規則 |
| `evidence.json` | 上の元データ |
| `candidate_review_table.md` | `tool/export_r002_candidate_review_table.py` の出力 |

## グラフの構成

| 層 | ノード | 意味 |
|---|---|---|
| `L_raw` | `raw.primitive_lean.prNN`（58）、カーネル依存レポート（1） | 観測された成果物 |
| `L_candidate` | `cand.primitive_lean.prNN.content`（58）、版の選択を問う `CandidateQuestion`（1） | 判断待ちの内容 |
| `L_accepted` | `main` に統合済みの 4 段（ベースライン → #68 → #3 → #74） | `extends_main` の本線 |
| `L_gitlog` | `main` のコミット `67fdf6b` | `observes_kernel_change` で本線の末尾を観測 |

未統合の PR は 1 つも `L_accepted` に置いていない。カーネルが証明を受理したことは、ERG での受理とは別の事実として扱う。PR 同士の関係（包含・同一内容・同名異版）は R001 の辺の型にないため、`evidence.md` に記録した。

## 判定案の規則（上から順に適用）

| 判定案 | 規則 |
|---|---|
| 道具類 | PR 自身の Lean ソースがない |
| 保留 | ヘッド自身の証明検査が通らない、またはタイトルが未解決を明示している |
| 吸収 | 固有の Lean ファイルがすべて、カーネル検査を通った別の PR にバイト単位で同一に含まれる |
| 版の選択 | 同じファイルパスで中身の違う版が別の PR にある |
| 分岐 | 通るが、新しい定理のどれも `main` の宣言を参照しない |
| 本線候補 | 通り、`main` を参照し、重複も版の衝突もない |

「本線候補」は `main` の何かを参照しているというだけで、多くは定義の再利用にとどまる。`main` の定理を証明に使っている定理の数は `evidence.md` の列で確認できる。

## 集計

| 判定案 | PR 数 | 新定理（カーネル） |
|---|---:|---:|
| 本線候補 | 17 | 596 |
| 分岐 | 21 | 447 |
| 版の選択 | 2 | 43 |
| 吸収 | 6 | （吸収先で計上） |
| 保留 | 8 | 測定不能 |
| 道具類 | 4 | — |

重複を除いたカーネル受理済みの新定理は 1121（41 PR）。PR 固有ファイルの字句上の定理数の合計は 1764 で、差の大部分は同一内容の重複と、測定不能な保留分である。

## 次の手順

1. 人が `evidence.md` を見て、PR ごとに採否を決める。
2. 決まった判断ごとに、`L_candidate` の判断ノードと `accepted_from_candidate` を追加する。`main` に統合したものだけを `extends_main` で本線に延長し、分岐として残すものは `extends_branch` を使う。
3. 判断を入れた時点で `docs/CONVERGENCE.md` に実数の行を加える。
