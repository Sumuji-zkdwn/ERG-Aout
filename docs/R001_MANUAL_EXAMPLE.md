# R001 manual conversation example の読み方

Status: companion note (explanatory only).

この文書は `examples/r001/manual_conversation_to_erg_example.json` の**現在の手作業サンプル**を読み解くための companion document です。

- JSON example 自体は変更しない
- schema は変更しない
- validator は変更しない
- 自動 ingestion / 自動 extraction / convergence scoring は実装しない
- GIF/DIF / sigma / recency / branch_degree は実装しない
- 新しい理論主張は追加しない

要するに、「いまある manual example をどう読むか」だけを説明します。

## 1) このサンプルが想定する自然言語断片

この JSON は、次のような 3 つの発話断片を手で要約してノード化したものとして読む。

1. 「共通の更新規則を置いて状態遷移として扱う」
2. 「avatar / token / cell の共有ルール案もあり得る」
3. 「線形作用素で表現できるかもしれない」

`raw.user.*` は、上記のような自然言語断片の**出発点**を保存するためのノードであり、厳密な逐語録そのものではない。

## 2) raw node と自然言語断片の対応

- `raw.user.1`
  - 対応断片: 「共通の更新規則を置いて状態遷移として扱う」
  - `introduces` で `cand.common_update_rule` を導入する。

- `raw.user.2`
  - 対応断片: 「avatar / token / cell の共有ルール案もあり得る」
  - `introduces` で `cand.unaccepted_avatar_token_cell_shared_rule` を導入する。
  - あわせて `mentions` により、既受理側の `acc.formalize_dynamic_system_as_state_transition_graph` に言及している。

- `raw.user.3`
  - 対応断片: 「線形作用素で表現できるかもしれない」
  - `introduces` で `cand.linear_operator_representation` を導入する。

## 3) raw -> candidate -> accepted の写像理由（短縮版）

このサンプルでは、`raw` は会話由来の素材、`candidate` は整形された候補、`accepted` は当面採用された核、という 3 段階で読む。

- `raw.user.1 -> cand.common_update_rule -> acc.state_transition_graph_seed`
  - 理由: 更新規則の話は、最小の受理核（state-transition seed）として固定しやすい。

- `raw.user.3 -> cand.linear_operator_representation -> acc.formalize_dynamic_system_as_state_transition_graph`
  - 理由: 線形作用素の観点は、状態遷移グラフとしての形式化を前進させる候補として採用可能。

`raw.user.2 -> cand.unaccepted_avatar_token_cell_shared_rule` は candidate 止まりで、accepted への `accepted_from_candidate` を持たない。

## 4) `cand.unaccepted_avatar_token_cell_shared_rule` が未採用の理由

このノードは「案としては記録するが、現時点の最小核には入れない」ための未採用候補として置かれている。

- 理由（このサンプルの読み）:
  - 現在の受理核を増やさなくても、主線（state transition graph の形式化）は進められる。
  - `manual_conversation_to_erg_example.json` は、候補の一部が未採用のまま残るケースを示す教育用サンプルである。

## 5) `acc.operator_physics_analogy` が main ではなく branch の理由

`acc.operator_physics_analogy` は `extends_main` ではなく `extends_branch` で接続される。

- 理由（このサンプルの読み）:
  - 物理アナロジーは、受理済みではあるが canonical spine（主線）の必須ステップとしては扱っていない。
  - 主線は `acc.state_transition_graph_seed -> acc.formalize_dynamic_system_as_state_transition_graph` に絞り、
    `operator_physics_analogy` は補助的・並行的な解釈として保持する。

この区別によって、R001 の `main`（正準進行）と `branch`（保持される非正準進行）の違いを最小例で確認できる。

## 6) エッジの見取り図

- `introduces`:
  - raw 断片がどの candidate を導入したか。
- `accepted_from_candidate`:
  - どの candidate が accepted に昇格したか。
- `extends_main`:
  - accepted の canonical path。
- `extends_branch`:
  - accepted の非 canonical な分岐。
- `mentions`:
  - raw 断片が accepted 概念に言及する参照関係。

## 7) この文書の境界

この文書は説明のみであり、R001 の意味論や仕様を拡張しない。

- 新規アルゴリズムは導入しない。
- 新規スコアリングは導入しない。
- 自動化機構は導入しない。

したがって、ここでの結論は「manual example の読み方」の範囲に限定される。
