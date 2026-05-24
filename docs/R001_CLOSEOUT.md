# R001 Closeout

この文書は、R001 の終了時点で確定した到達点・境界・R002へ渡す入力を短く固定する closeout document である。

## 1) R001 で確定したこと

R001 では、次を実装・文書化済みとする。

- typed graph JSON を扱う。
- schema / validator による検査を行う。
- `extends_main` / `extends_branch` の制約を導入する。
- DOT export を提供する。
- `full` / `accepted` / `spine` projection を提供する。
- short labels を提供する。
- edge semantics document を整備する。
- semantics coverage checker を提供する。
- development sample graph を提供する。
- manual conversation examples を提供する。
- manual example reading guide を提供する。
- manual mapping rules を提供する。

## 2) R001 で意図的にやらないこと

R001 のスコープ外として、次は意図的に実施しない。

- automatic conversation ingestion
- automatic concept extraction
- convergence scoring
- GIF/DIF semantics
- sigma semantics
- recency
- branch_degree
- semantic importance scoring

## 3) R001 の主要ファイル

- `docs/R001_STATUS.md`
- `docs/R001_SEMANTICS.md`
- `docs/R001_INTERPRETATION.md`
- `docs/R001_MANUAL_EXAMPLE.md`
- `docs/R001_MANUAL_MAPPING_RULES.md`
- `examples/r001/sample_r001_development_graph.json`
- `examples/r001/manual_conversation_to_erg_example.json`
- `examples/r001/manual_conversation_cpr_origin_example.json`
- `tool/validate_r001_kernel.py`
- `tool/inspect_r001_graph.py`
- `tool/export_r001_dot.py`
- `tool/check_r001_semantics_coverage.py`

## 4) R002 へ渡す入力

R002 の開始入力として、次を引き継ぐ。

- manual examples
- manual mapping rules
- validator / inspector / DOT exporter
- `docs/R001_STATUS.md` で固定した境界

## 5) R002 で検討すること（短縮版）

- semi-automatic mapping support
- mapping consistency checks
- larger conversation log application
- candidate/accepted decision assistance

## 6) Closeout note

本書は R001 の終了整理のみを目的とし、新しい理論主張は追加しない。
