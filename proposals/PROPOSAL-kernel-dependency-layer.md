# PROPOSAL: Lean カーネル依存グラフを ERG / HMDG に載せる方法

Status: proposal（未受理）。スキーマ、validator、`docs/` の受理済み記述はいずれも変更しない。

## 背景

primitive-lean（公開）に、Lean が受理した宣言の型・証明項・定義本体から、実際に現れる定数を抽出するツールを追加した。

- ツール：`tools/deps/`
- 結果：`docs/dependency/`
- 対象：コミット `67fdf6b` の main と、自動生成された有限模型 cycle 1–2

出力では、次の 4 種類を混ぜずに分けている。

| 種類 | 意味 | 抽出元 |
|---|---|---|
| proof | 定理の証明項に現れる定数 | `ConstantInfo.value?`（定理） |
| statement | 命題の型に現れる定数 | `ConstantInfo.type` |
| definition | 定義本体に現れる定数 | `ConstantInfo.value?`（定義） |
| module | import によるモジュール依存 | `.olean` ヘッダ |

4 種類目の「概念的な接続」は、このツールは生成しない。

## 提案する対応

### 1. 層の扱い

Lean が受理した宣言を、ERG の `L_accepted` には置かない。

`L_accepted` は「ERG の批判的レビューを経て受理された」ことを意味する。カーネルが証明を受理したことは、ERG での受理とは別の事実である。R001 の層の列挙は変更せず、次のどちらかを選ぶことを提案する。

- **案 A**：カーネル依存グラフを ERG の外部成果物として扱う。ERG 側の `L_raw` ノード（成果物の観測）が、それを `mentions` ではなく別の型の辺で参照する。
- **案 B**：将来の段階で、形式的な層（仮称 `L_formal`）を追加する。この層には `proof` / `statement` / `definition` / `module` の辺だけを許可し、`extends_main` や `accepted_from_candidate` は禁止する。

どちらも R001 の範囲外なので、採用には別途レビューが要る。

### 2. HMDG との接続

HMDG v0 は、外部の定理依存 DAG（LeanDojo の mathlib グラフ）を入力にして、主経路と境界を抽出している。primitive-lean の `proof` 辺は同じ「前提 → 定理」の DAG として使える。ただし、次を守る。

- `Declaration` ノードは、カーネル依存グラフの宣言 1 個に対応させる。
- `main_path_edge` などの HMDG の導出辺は、`proof` 辺から計算したものであることを属性で明示する。
- **ConceptBridge と ProofBridge は、`proof` 辺が存在しても `candidate` のまま**とする。辺の存在は根拠の 1 つにはなるが、橋の受理はこれまでどおりレビュー記録を経て行う。
- 逆に、`proof` 辺が存在しないことを理由に、橋を否定もしない。

### 3. 主張しないこと

- 辺は、その定数が項に現れることだけを表す。数学的に必要であることは意味しない。
- 初期層への経路がないことは、初期層から導出できないことの証明ではない。
- ソースファイル間の集約辺（`source_edges.json`）は件数の要約であり、ERG の `extends_*` の系譜とは別物である。

## 次の手順の候補

1. 案 A と案 B のどちらにするかを、critic の役割でレビューする。
2. 採用されたら、`deps.json` を R001 形式（または拡張形式）に変換する補助スクリプトを `tool/` に追加する。validator を通すことを前提にする。
3. HMDG の `run_real_graph.py` に、primitive-lean の `proof` 辺を入力として渡す読み込み口を追加する。

## データの扱い

この提案は、公開リポジトリ（primitive-lean）の成果物を参照するだけで、ERG-Aout の非公開の内容を外へ出さない。逆方向でも、ERG のスキーマや記録を primitive-lean にコピーしない。
