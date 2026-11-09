# R005 Formal binding（ERG ノードと外部の形式証明の対応）

Status: R005 proposed. schema は変更しない sidecar 方式。validator の変更は、accepted 層への `KernelClaim` の追加だけ（§4a）。

## 1) 目的

ERG は、会話から出た主張が raw → candidate → accepted と手続き上の地位を得ていく過程を記録する。一方、主張の数学的な中身は外部の形式化リポジトリ（現在は Lean 4 の `Sumuji-zkdwn/primitive-lean`）で証明される。

これまで両者をつなぐ記録がなく、「どの会話のどの候補が、どの定理になったか」を機械的にたどれなかった。formal binding は、この対応を ERG 側に固定する。

## 2) 基本方針

- graph JSON は変えない。対応は `<graph の stem>.formal_binding.json` という sidecar に置く（raw text sidecar と同じ考え方。`docs/R002_RAW_TEXT_ATTACHMENT_STRATEGY.md`）。
- 束縛は**証拠の記録であって、受理ではない**。束縛しても node の layer は変わらない。accepted への昇格は従来どおり `accepted_from_candidate` とレビューで行う。
- 証明の正しさは形式化側の検証（primitive-lean では `--trust=0` と公理監査）に委ねる。ERG 側は、固定したコミットに、記録したとおりのファイルと宣言が存在することだけを確かめる。
- 宣言が元の直観を正しく表しているか（忠実性）は機械で確かめられない。そのため人の判断として `fidelity_note` に書き、主張しないことを `non_claims` に書く。

## 3) ファイル形式

```json
{
  "binding_version": 1,
  "formal_source": {
    "repository": "Sumuji-zkdwn/primitive-lean",
    "commit": "<40 桁のコミット ID>",
    "language": "Lean 4 ...",
    "files": { "<path>": "<sha256>" },
    "verification_record": "<形式化側の検証記録の path（任意）>",
    "verification_note": "<任意>"
  },
  "bindings": [
    {
      "id": "fb.xxx",
      "node": "<ERG node id>",
      "relation": "defines | proves | proves_restricted | refutes",
      "declarations": [ { "name": "Namespace.decl", "kind": "theorem", "file": "<path>" } ],
      "fidelity_note": "宣言が node の内容とどう対応するか",
      "non_claims": [ "この束縛が主張しないこと" ]
    }
  ],
  "unbound": [
    { "node": "<ERG node id>", "reason": "形式的な対応を置かない理由" }
  ]
}
```

- 宣言名は完全修飾名で書く。`kind` は `theorem` `lemma` `def` `abbrev` `structure` `inductive` `class` `instance` のいずれか。
- 宣言を含むファイルは、すべて `formal_source.files` に SHA-256 付きで載せる。
- 未知のキーはエラーにする（意味を黙って増やさないため）。

## 4) relation

| relation | 付けられる node type | 意味 | 必要なもの |
|---|---|---|---|
| `defines` | CandidateDefinition, CandSymbol, KernelDefinition, KConcept | 宣言が node の定義を与える | 定義系の宣言を1つ以上 |
| `proves` | CandidateClaim, CandidateExample, CandidateFailureCase, KernelClaim, KernelExample, KernelFailureCase | node の主張を、書かれたとおりに証明する | theorem/lemma を1つ以上 |
| `proves_restricted` | 同上 | 追加の仮定の下、または特殊な場合だけ証明する | theorem/lemma を1つ以上、`non_claims` を1つ以上 |
| `refutes` | CandidateClaim | node の主張の否定または反例を証明する | theorem/lemma を1つ以上 |

accepted ノードを `refutes` の対象にはしない。反証は昇格元の候補に付け、すでに昇格していれば WARNING になる。

L_raw と L_gitlog のノード、KernelDecision と KernelAxiom（手続き上の決定と前提）、CandidateQuestion には束縛を付けない。問いは、答えとなる主張のノードを別に立ててから束縛する。

すべての束縛に `fidelity_note` が必要。対応する宣言を探したが置かないと決めたノードは、理由を付けて `unbound` に入れる。同じノードを `bindings` と `unbound` の両方に入れることはできない。また、同じノードに `proves` 系と `refutes` を同時に付けることもできない。

## 4a) `KernelClaim`（R005 で追加）

R001 の accepted 層には、主張（`CandidateClaim`）の受け皿となる型がなかった。そのため、形式証明のある主張を昇格させられなかった。R005 では、`CandidateClaim` に対応する `KernelClaim` を L_accepted の型として追加した（`tool/validate_r001_kernel.py`、`docs/FORMALIZATION.md`）。

- accepted は、ここでも手続き上の地位であって、真理の保証ではない。主張の正しさの根拠は、束縛された形式証明とその `non_claims` にある。
- `KernelClaim` も、原則として `accepted_from_candidate` で候補から昇格させる。
- `proves_restricted` だけを持つ候補は、制限ごと引き継げる形で書き直すまで昇格させない運用を推奨する。

## 5) 検査（`tool/check_formal_binding.py`）

```bash
# 構造だけ
python tool/check_formal_binding.py <graph.json> <binding.json>
# 形式化側の clone も使う
python tool/check_formal_binding.py <graph.json> <binding.json> \
  --formal-repo Sumuji-zkdwn/primitive-lean=<clone の場所> \
  --formal-main-ref origin/main --require-formal-check
```

常に行うこと（構造の検査）:

- node が存在すること、layer・type と relation が整合すること
- 必須項目（`fidelity_note`、`proves_restricted` の `non_claims`、ファイルのハッシュ）がそろっていること
- 束縛同士が矛盾しないこと

`--formal-repo` を渡したとき（形式化側の検査）:

- 固定したコミットが clone に存在し、`--formal-main-ref` に含まれること
- 各ファイルの、そのコミットでのバイト列の SHA-256 が一致すること
- 各宣言が、コメントと文字列を除いた本文に、名前空間・キーワード・名前の組として存在すること。種類も一致すること（theorem と lemma は同一視）
- `verification_record` を書いた場合は、そのファイルがそのコミットに存在すること

行わないこと:

- Lean の型検査や証明の再検査（形式化側の CI の責任）
- 忠実性の判定（人の判断）
- node の昇格や graph の書き換え

出力の WARNINGS と NOTES は、レビューのための手がかりであり、graph の状態は変えない。

- `promotion candidate`：`proves` 付きでまだ昇格していない候補（昇格するかはレビューで決める）
- `promotion candidate (definition)`：`defines` 付きでまだ昇格していない定義
- `restricted evidence`：`proves_restricted` だけを持つ候補（昇格するなら `non_claims` も引き継ぐ）
- `refuted candidate`：`refutes` 付きの候補（書かれたままの形では昇格しない）
- WARNING `promoted candidate ... is refuted`：すでに昇格した候補が反証されている
- `nodes neither bound nor listed as unbound`：まだ判断していないノード。束縛された候補から `accepted_from_candidate` で昇格した accepted ノードは、候補の束縛を引き継ぐので、ここには含まれない（SUMMARY の `accepted nodes covered via their candidate` に数える）

## 6) R003 自動検査との関係

`tool/run_r003_automation_checks.py` は `examples/` 以下の `*.formal_binding.json` を自動で見つけ、同じ場所の同じ stem の graph と組にして検査する。binding ファイルは graph としての検証の対象から外す。

CI（`.github/workflows/r003-automation-checks.yml`）は primitive-lean を読み取り専用で `.formal/primitive-lean` に clone する。そのうえで `--require-formal-check` を付けて実行するので、形式化側の検査が行われなかった場合は失敗になる。

binding ファイルの変更は、リスク要約で soft-gated として扱う。忠実性は人の判断なので、`fidelity_note` と `non_claims` を PR で確認する。

## 7) 実例：F0（`examples/r005/`）

primitive-lean の `sources/f0_math_chat_2026-10-29/`（チャットの数学的内容をまとめた資料）を raw にとり、Lean の `F0Retractions.inc` と `F0Counting.inc` に束縛した。

| 候補 | relation | 主な宣言 | 要点 | 状態 |
|---|---|---|---|---|
| `cand.f0.system` | defines | `Idempotent`, `liftK`, `Compatible`, `Reconstructs`, `step` | 出力成分 d は任意の添字型 I に一般化されている | `acc.f0.system`（KernelDefinition） |
| `cand.f0.fiber_decomposition` | proves | `fiberDecomposition`, `fiber_card_sum` | 型の同値と濃度の等式 | `acc.f0.fiber_decomposition`（KernelClaim） |
| `cand.f0.image_in_fixed` | proves | `step_fixed` | A・B なしで T の値は Fix K に入る | `acc.f0.image_in_fixed`（KernelClaim） |
| `cand.f0.period_bound` | proves_restricted | `periodic_cycle_bound` | 周期内の点が相異なること（最小周期）を仮定する | 候補のまま |
| `cand.f0.idempotent_counts` | proves | `seven_point_idempotents` ほか | 会話では有限計算だった値が Lean の定理になっている | `acc.f0.idempotent_counts`（KernelExample） |
| `cand.f0.drop_b_separates` | proves | `exampleK`, `exampleBadS`, `incompatible_can_separate` | 会話の反例をそのまま表している | `acc.f0.drop_b_separates`（KernelFailureCase） |
| `cand.f0.drop_b_not_always` | unbound | なし | 名前の近い `failure_does_not_imply_noncollapse` は条件 A についての例なので、束縛しない | 候補のまま |
| `cand.f0.imbalance_monotonicity` | unbound | なし | 未証明予想。形式化側でも対象外と明記されている | 候補のまま |

`proves` を持つ4候補と、それらが依存する定義 `cand.f0.system`（`defines`）を、レビューの判断で accepted に昇格させた。昇格は手続き上の地位であり、各束縛の `non_claims` はそのまま有効である。`extends_main` には載せていない（この例のグラフには正準の主線がない）。

候補のまま残るのは、制限付きの周期上限（`proves_restricted`）と、unbound の2つである。

## 8) この文書がやらないこと

- schema・`extends_main` の規則の変更（validator は `KernelClaim` の追加のみ）
- 束縛を根拠とした自動昇格
- 形式化側への書き込み
- 忠実性の自動判定
- 会話の自動取り込みや概念の自動抽出（R003 の境界のまま）
