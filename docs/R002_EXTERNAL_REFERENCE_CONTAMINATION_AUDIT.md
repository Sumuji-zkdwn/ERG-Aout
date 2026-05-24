# R002 External Reference Contamination Audit

この文書は、ERG-Aout repository の **repository hygiene / project-boundary check** として、
README / docs / examples / tool に外部プロジェクト由来の文言・語彙・設計ノイズが混入していないかを確認するための監査メモである。

- 目的は hygiene check であり、法的判断ではない。
- 新しい理論主張・仕様変更を導入する文書ではない。

## 1) Audit purpose

本監査では、次を確認する。

- ERG-Aout の README / docs / examples / tool に、ERG-Aout と無関係な外部プロジェクト由来ノイズが混ざっていないか。
- とくに次の語彙の混入有無を重点確認する。
  - lean / Lean / lean puzzle / puzzle / theorem / proof assistant / mathlib / lake
  - tactic / sorry / axioms / theorem proving

## 2) Audit scope

### 対象

- `README.md`
- `docs/`
- `examples/`
- `tool/`

### 対象外

- `.git` 内部
- GitHub PR 本文
- Codex task UI
- 外部リポジトリそのもの

## 3) Search terms and commands

### 検索語（最低限）

- lean
- Lean
- lean puzzle
- puzzle
- theorem
- proof assistant
- mathlib
- lake
- tactic
- sorry
- axioms
- theorem proving

### 実行コマンド

```bash
git grep -n -i "lean" README.md docs examples tool
git grep -n -i "lean puzzle" README.md docs examples tool
git grep -n -i "puzzle" README.md docs examples tool
git grep -n -i "theorem" README.md docs examples tool
git grep -n -i "proof assistant" README.md docs examples tool
git grep -n -i "mathlib" README.md docs examples tool
git grep -n -i "lake" README.md docs examples tool
git grep -n -i "tactic" README.md docs examples tool
git grep -n -i "sorry" README.md docs examples tool
git grep -n -i "axioms" README.md docs examples tool
git grep -n -i "theorem proving" README.md docs examples tool
```

注意:

- 検索語が本 audit 文書自身に含まれることがある。
- **audit 文書自身のヒットは contamination 判定から除外**する。

## 4) Audit result (current snapshot)

### 4.1 Summary

- `theorem` 検索で 1 件ヒット（`tool/memory_erg_app_github_math.py` 内の `theorem_candidate`）。
- `lean` 検索は複数ヒットしたが、`clean` 等への部分一致であり、`lean` 固有語彙の混入ではない。
- そのほか（lean puzzle / puzzle / proof assistant / mathlib / lake / tactic / sorry / axioms / theorem proving）は対象範囲内でヒットなし。

### 4.2 Finding detail template

#### Finding-1

- file: `tool/memory_erg_app_github_math.py`
- matched term: `theorem`
- matched expression: `theorem_candidate`
- why this may be a concern:
  - 外部系語彙（theorem）が識別子に含まれており、project boundary の観点で曖昧さを生み得る。
- current handling policy:
  - 現時点では仕様変更・実装変更は行わず、**boundary-awareness note** として記録する。
  - 今後、この識別子が ERG-Aout の正式語彙体系と不整合と判断された場合に、別タスクで名称見直しを検討する。

## 5) Determination format

- ヒットなしの場合: `no contamination found in tracked project files`
- ヒットありの場合: 本文書の finding detail template に従って、
  - 該当ファイル
  - 該当語
  - なぜ問題になりうるか
  - 対応方針
  を記録する。

## 6) Boundary reminder for future Codex work

今後の Codex 作業では、ERG-Aout 内の既存 docs と明示指示を根拠に進め、
外部プロジェクト語彙を無目的に導入しない。
