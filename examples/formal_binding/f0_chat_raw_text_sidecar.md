# F0 チャット由来資料の raw text sidecar

`examples/formal_binding/f0_chat.json` の `L_raw` ノード対応表。

出典は公開リポジトリ `Sumuji-zkdwn/primitive-lean` の `sources/f0_math_chat_2026-10-29/`（コミット `09f141ea6845ccb658b82b69ff788aab5522fbc5`）。この資料自体がチャットの数学的内容を整理した要約であり、元の対話の逐語記録ではない。したがって raw ノードは発話（RawMessage）ではなく資料の節（RawArtifact）として切り、`turn_index` には資料内の順序を置く。抜粋は数式を要約したもので、原文の引用ではない。

| raw_id | turn_index | speaker | text_excerpt | source_note | mapping_note |
|---|---:|---|---|---|---|
| raw.f0.defs | 1 | chat-summary | K は冪等、S: 𝓑→𝓑^d、C: 𝓑^d→𝓑、T = K∘C∘K^(d)∘S。追加条件 A: C∘S=id、B: S∘K=K^(d)∘S | 01_definitions_and_theorems.md §1 | introduces cand.f0.system |
| raw.f0.blocks | 2 | chat-summary | 𝓑 は固定点ごとのファイバー B_a の非交和で、a∈B_a。有限なら N = Σ m_a | 01_definitions_and_theorems.md §2 | introduces cand.f0.fiber_decomposition |
| raw.f0.period | 3 | chat-summary | T(𝓑) ⊆ F。有限なら任意の周期の長さ ≤ r（A・B 不要） | 01_definitions_and_theorems.md §3 | introduces cand.f0.image_in_fixed, cand.f0.period_bound |
| raw.f0.counts | 4 | chat-summary | 7点で冪等写像 6,322 個、8点で 41,393 個（有限計算） | README.md 主な確認結果 | introduces cand.f0.idempotent_counts |
| raw.f0.drop_b | 5 | chat-summary | 𝓑={0,1,2}, K=(0,0,2), d=1, S=(0,2,0) で B が崩れ区別が現れる。ただし B 不成立が常に区別を復活させるわけではない | 03_conjecture_and_cautions.md §5 | introduces cand.f0.drop_b_separates, cand.f0.drop_b_not_always |
| raw.f0.conjecture | 6 | chat-summary | 総量 N・成分数 r 固定で (a,b)→(a+1,b−1) とすると Φ_d が厳密に増加するという未証明予想 | 03_conjecture_and_cautions.md §1 | introduces cand.f0.imbalance_monotonicity |
