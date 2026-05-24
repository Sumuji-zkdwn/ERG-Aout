# R001 manual mapping rules（manual examples から読める範囲）

Status: companion note (explanatory only).

この文書は、次の 2 つの手動 example から**読み取れる範囲だけ**で、R001 の手動写像ルールを明文化する。

- `examples/r001/manual_conversation_to_erg_example.json`
- `examples/r001/manual_conversation_cpr_origin_example.json`

## 前提と境界

- JSON example は変更しない。
- schema は変更しない。
- validator は変更しない。
- 自動 conversation ingestion は実装しない。
- 自動 concept extraction は実装しない。
- convergence scoring は実装しない。
- GIF/DIF / sigma / recency / branch_degree は実装しない。
- 新しい理論主張は追加しない。

以下は「既存 manual examples を人手で写像する時の読解ルール」であり、アルゴリズム仕様ではない。

## 1. raw node にする条件

手動写像で `L_raw` / `RawMessage` に置くのは、会話断片の**出発点として保持したい発話素材**である。

- 両 example とも `raw.user.*` が先に置かれ、そこから `introduces` / `mentions` が出る。
- したがって raw は「まだ candidate/accepted に整形・採択していない入力側アンカー」として使う。

## 2. candidate node にする条件

`L_candidate` / `CandidateDefinition` に置くのは、raw 断片から取り出した**概念候補**である。

- 両 example とも、candidate は `introduces` の target になっている。
- したがって candidate は「raw の内容を概念単位へ整形した中間表現」として置く。

## 3. accepted node に昇格させる条件

candidate を `L_accepted` に昇格させるのは、当該 candidate を受理して核に載せるときである。

- 両 example とも、昇格は `accepted_from_candidate` edge で明示される。
- よって manual mapping 上の必要条件は「candidate から accepted への `accepted_from_candidate` を張ること」。

## 4. extends_main に置く条件

`extends_main` は、accepted ノードどうしのうち**canonical spine（主線）**として扱う遷移に置く。

- `manual_conversation_to_erg_example` では
  `acc.state_transition_graph_seed -> acc.formalize_dynamic_system_as_state_transition_graph` が主線。
- `manual_conversation_cpr_origin_example` でも
  `acc.state_transition_seed -> acc.linear_operator_form_attempt` が主線。

つまり、accepted の中で「この進行を正準の連なりとして残す」と判断した接続を `extends_main` に置く。

## 5. extends_branch に置く条件

`extends_branch` は、accepted ノードどうしのうち**保持はするが主線ではない分岐**に置く。

- 両 example とも、`operator_physics_analogy` 側は accepted だが main ではなく branch で接続される。
- したがって「受理済みだが canonical spine には入れない進行」を branch として保持する。

## 6. unaccepted candidate として残す条件

candidate を unaccepted のまま残すのは、候補として記録はするが現時点で受理核へ入れないときである。

- 両 example に `cand.unaccepted_*` があり、`accepted_from_candidate` を持たない。
- よって manual mapping では「introduces はあるが accepted へ昇格 edge を張らない candidate」を unaccepted candidate として残す。

## 7. mentions edge を張る条件

`mentions` は raw 断片が accepted 概念に**参照・言及**していることを示すときに張る。

- `manual_conversation_to_erg_example` では `raw.user.2 -> acc.formalize_dynamic_system_as_state_transition_graph`。
- `manual_conversation_cpr_origin_example` では
  `raw.user.6 -> acc.linear_operator_form_attempt`、`raw.user.2 -> acc.state_transition_seed`。

したがって `mentions` は導入 (`introduces`) や昇格 (`accepted_from_candidate`) と別に、raw から accepted への参照関係を保存する用途で使う。

## 8. 2 つの example の対応表（要約）

- raw -> candidate: `introduces`
- candidate -> accepted: `accepted_from_candidate`（あるものだけ昇格）
- accepted -> accepted (canonical): `extends_main`
- accepted -> accepted (non-canonical kept branch): `extends_branch`
- raw -> accepted (reference): `mentions`

以上が、2 つの manual example から直接読める最小の手動写像ルールである。
