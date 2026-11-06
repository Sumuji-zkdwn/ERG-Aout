# 根拠表：primitive-lean 未統合 PR の棚卸し

`main` = `67fdf6b` に対する測定。判定案は候補であり、採否は人が決める。

列の意味：新定理・新定義 = `main` にない宣言のうち、この PR 固有のファイルに属するもの（カーネル受理済み）。main 参照 = 推移的依存に `main` の宣言を含む定理の数。main 定理を証明に使用 = 証明項の連鎖に `main` の定理を含む定理の数。初期層 = 初期層に到達する定理の数。遅れ = PR のヘッドに含まれない `main` のコミット数。

| PR | 判定案 | 新定理 | 新定義 | main 参照 | main 定理を証明に使用 | 初期層 | 遅れ | 規則 |
|---|---|---:|---:|---:|---:|---:|---:|---|
| #29 | 本線候補 | 13 | 12 | 10 | 8 | 0 | 56 | compiles; references main; no duplicate or version conflict |
| #31 | 本線候補 | 71 | 29 | 49 | 0 | 49 | 56 | compiles; references main; no duplicate or version conflict |
| #33 | 本線候補 | 28 | 7 | 27 | 4 | 25 | 56 | compiles; references main; no duplicate or version conflict |
| #36 | 本線候補 | 33 | 13 | 7 | 0 | 0 | 56 | compiles; references main; no duplicate or version conflict |
| #37 | 本線候補 | 14 | 4 | 14 | 6 | 13 | 56 | compiles; references main; no duplicate or version conflict |
| #38 | 本線候補 | 37 | 15 | 26 | 8 | 0 | 56 | compiles; references main; no duplicate or version conflict |
| #39 | 本線候補 | 27 | 10 | 3 | 0 | 0 | 56 | compiles; references main; no duplicate or version conflict |
| #40 | 本線候補 | 6 | 8 | 3 | 0 | 3 | 56 | compiles; references main; no duplicate or version conflict |
| #41 | 本線候補 | 16 | 4 | 3 | 0 | 3 | 56 | compiles; references main; no duplicate or version conflict |
| #43 | 本線候補 | 15 | 3 | 2 | 0 | 0 | 56 | compiles; references main; no duplicate or version conflict |
| #48 | 本線候補 | 73 | 26 | 63 | 0 | 31 | 56 | compiles; references main; no duplicate or version conflict |
| #75 | 本線候補 | 98 | 52 | 73 | 20 | 0 | 1 | compiles; references main; no duplicate or version conflict |
| #77 | 本線候補 | 18 | 1 | 5 | 2 | 0 | 0 | compiles; references main; no duplicate or version conflict |
| #81 | 本線候補 | 24 | 9 | 20 | 5 | 0 | 0 | compiles; references main; no duplicate or version conflict |
| #83 | 本線候補 | 8 | 2 | 8 | 3 | 8 | 0 | compiles; references main; no duplicate or version conflict |
| #87 | 本線候補 | 50 | 53 | 14 | 9 | 0 | 0 | compiles; references main; no duplicate or version conflict |
| #91 | 本線候補 | 65 | 66 | 7 | 5 | 7 | 0 | compiles; references main; no duplicate or version conflict |
| #42 | 分岐 | 31 | 19 | 0 | 0 | 0 | 56 | compiles; none of its new theorems references a declaration that is in main |
| #44 | 分岐 | 14 | 5 | 0 | 0 | 0 | 56 | compiles; none of its new theorems references a declaration that is in main |
| #46 | 分岐 | 26 | 16 | 0 | 0 | 0 | 56 | compiles; none of its new theorems references a declaration that is in main |
| #47 | 分岐 | 10 | 1 | 0 | 0 | 0 | 56 | compiles; none of its new theorems references a declaration that is in main |
| #50 | 分岐 | 21 | 12 | 0 | 0 | 0 | 56 | compiles; none of its new theorems references a declaration that is in main |
| #51 | 分岐 | 23 | 14 | 0 | 0 | 0 | 56 | compiles; none of its new theorems references a declaration that is in main |
| #52 | 分岐 | 19 | 4 | 0 | 0 | 0 | 56 | compiles; none of its new theorems references a declaration that is in main |
| #53 | 分岐 | 14 | 11 | 0 | 0 | 0 | 56 | compiles; none of its new theorems references a declaration that is in main |
| #54 | 分岐 | 10 | 2 | 0 | 0 | 0 | 56 | compiles; none of its new theorems references a declaration that is in main |
| #80 | 分岐 | 26 | 23 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #82 | 分岐 | 14 | 1 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #85 | 分岐 | 30 | 55 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #86 | 分岐 | 23 | 23 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #88 | 分岐 | 41 | 24 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #89 | 分岐 | 18 | 7 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #92 | 分岐 | 29 | 8 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #93 | 分岐 | 23 | 8 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #94 | 分岐 | 56 | 15 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #95 | 分岐 | 5 | 5 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #96 | 分岐 | 4 | 16 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #97 | 分岐 | 10 | 14 | 0 | 0 | 0 | 0 | compiles; none of its new theorems references a declaration that is in main |
| #32 | 吸収 | 17 | 2 | 16 | 3 | 15 | 56 | all own Lean units reappear byte-identically in PR(s) [33] |
| #65 | 吸収 | 18 | 14 | 9 | 0 | 0 | 124 | all own Lean units reappear byte-identically in PR(s) [72, 75] |
| #66 | 吸収 | 26 | 15 | 25 | 11 | 0 | 124 | all own Lean units reappear byte-identically in PR(s) [72, 75] |
| #67 | 吸収 | 20 | 9 | 10 | 3 | 0 | 124 | all own Lean units reappear byte-identically in PR(s) [72, 75] |
| #69 | 吸収 | 20 | 8 | 19 | 6 | 0 | 124 | all own Lean units reappear byte-identically in PR(s) [72, 75] |
| #72 | 吸収 | 98 | 52 | 73 | 20 | 0 | 124 | all own Lean units reappear byte-identically in PR(s) [75] |
| #70 | 版の選択 | 14 | 11 | 6 | 1 | 0 | 124 | same file path with different bytes in PR(s) [71] |
| #71 | 版の選択 | 29 | 15 | 15 | 3 | 0 | 124 | same file path with different bytes in PR(s) [70] |
| #30 | 保留 | — | — | — | — | — | 56 | kernel extraction not possible: the head's own proof check failed |
| #34 | 保留 | — | — | — | — | — | 56 | kernel extraction not possible: the head's own proof check failed |
| #35 | 保留 | — | — | — | — | — | 56 | kernel extraction not possible: the head's own proof check failed |
| #45 | 保留 | — | — | — | — | — | 56 | kernel extraction not possible: the head's own proof check failed |
| #49 | 保留 | — | — | — | — | — | 56 | kernel extraction not possible: the head's own proof check failed |
| #58 | 保留 | — | — | — | — | — | 56 | kernel extraction not possible: the head's own proof check failed |
| #59 | 保留 | — | — | — | — | — | 56 | kernel extraction not possible: the head's own proof check failed |
| #78 | 保留 | 35 | 21 | 4 | 1 | 0 | 0 | the PR title marks the result as open |
| #76 | 道具類 | — | — | — | — | — | 0 | no Lean source of its own (tools, docs, demos or Python checks only) |
| #79 | 道具類 | — | — | — | — | — | 0 | no Lean source of its own (tools, docs, demos or Python checks only) |
| #84 | 道具類 | — | — | — | — | — | 0 | no Lean source of its own (tools, docs, demos or Python checks only) |
| #90 | 道具類 | — | — | — | — | — | 0 | no Lean source of its own (tools, docs, demos or Python checks only) |

## 補足

- #31: 宣言が帰属しないファイル: `probes/ChebyshevDegreeTower.inc`, `probes/ChebyshevNext.inc`
- #32: 同名の宣言を持つ PR: #33
- #33: 同名の宣言を持つ PR: #32
- #65: 同名の宣言を持つ PR: #72, #75
- #66: 同名の宣言を持つ PR: #72, #75
- #67: 同名の宣言を持つ PR: #72, #75
- #69: 同名の宣言を持つ PR: #72, #75
- #70: 同名の宣言を持つ PR: #71
- #71: 同名の宣言を持つ PR: #70
- #72: 同名の宣言を持つ PR: #65, #66, #67, #69, #75
- #75: 同名の宣言を持つ PR: #65, #66, #67, #69, #72
- #78: 宣言が帰属しないファイル: `probes/IutPilotCrossRepo.lean`
- #83: 宣言が帰属しないファイル: `lean/MovingCurveAudit.lean`
- #85: 宣言が帰属しないファイル: `lean/SelfRewritingObserverBridgeTail.inc`
- #86: 宣言が帰属しないファイル: `lean/DarkBrightObservationBridgeTail.inc`
- #88: 宣言が帰属しないファイル: `lean/TwoMotionEmissionBridgeTail.inc`
