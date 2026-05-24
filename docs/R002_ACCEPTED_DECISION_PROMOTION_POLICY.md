# R002 Accepted Decision Promotion Policy

この文書は、R002 manual mapping における **accepted decision node（特に `KernelDecision`）の昇格規則**を明確化するための policy note である。

## 問題設定

`tool/check_r002_mapping_consistency.py` を `examples/r002/larger_manual_conversation_example.json` に実行すると、次の warning が出る。

- accepted node `acc.defer_full_automatic_ingestion` has no incoming accepted_from_candidate
- accepted node `acc.defer_gif_dif_sigma_scoring` has no incoming accepted_from_candidate

この warning は checker の単純バグを示すものではない。

R002 example には `KernelDecision` 型の accepted node があり、
その一部が `accepted_from_candidate` を持たないため、
「accepted は必ず candidate から昇格すべきか」「decision node に例外を認めるか」という
mapping rule の境界が露出している。

## 方針（現時点の整理）

### 原則

- `L_accepted` に置く node は、原則として candidate から `accepted_from_candidate` によって昇格させる。
- これにより、`raw -> candidate -> accepted` の追跡可能性（traceability）を維持する。

### decision node の扱い

- `KernelDecision` も、原則として candidate から昇格させる。
- `defer` / `reject` / `postpone` などの判断も、まず raw から candidate として表現し、
  その後 accepted decision として採択する形が望ましい。

### 例外（legacy example の扱い）

- 既存の古い example には、`accepted_from_candidate` を持たない `KernelDecision` が存在しうる。
- その場合は checker warning として検出される。
- ただし warning は「即時に正しい/誤りを自動断定する」意味ではなく、
  人間レビュー対象としての注意喚起である。

## この policy の適用範囲

- 本文書は **R002 manual mapping 運用方針の整理**であり、schema/validator/checker 実装の変更を要求しない。
- 現時点では warning の意味を固定し、将来の整理（例: decision node 昇格ルールの厳格化）に向けた土台とする。

## 適用例（larger manual example）

`examples/r002/larger_manual_conversation_example.json` は本 policy の適用例として更新され、defer 系 decision についても raw -> candidate -> accepted の昇格経路を持つように整理した。

- `cand.defer_full_automatic_ingestion_decision` -> `acc.defer_full_automatic_ingestion`
- `cand.defer_gif_dif_sigma_scoring_decision` -> `acc.defer_gif_dif_sigma_scoring`
