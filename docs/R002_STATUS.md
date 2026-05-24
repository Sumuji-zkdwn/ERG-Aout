# R002 Status

## 1. Current status

R002 は、bounded real-log manual mapping を含む pilot handoff 後の時点で、安定したチェックポイントに到達している。

- R002 は automatic ingestion system ではない。
- R002 は automatic candidate generation system ではない。
- R002 は scoring layer や semantic metric layer ではない。

## 2. Completed R002 artifacts

- `docs/R002_PLAN.md`
- `docs/R002_MAPPING_CHECKLIST.md`
- `docs/R002_ACCEPTED_DECISION_PROMOTION_POLICY.md`
- `docs/R002_RAW_TEXT_ATTACHMENT_STRATEGY.md`
- `docs/R002_EXTERNAL_REFERENCE_CONTAMINATION_AUDIT.md`
- `docs/R002_LARGER_MANUAL_EXAMPLE.md`
- `docs/R002_REAL_LOG_PILOT_PLAN.md`
- `docs/R002_REAL_LOG_PILOT_01.md`
- `docs/R002_REAL_LOG_PILOT_HANDOFF.md`
- `examples/r002/larger_manual_conversation_example.json`
- `examples/r002/larger_manual_conversation_raw_text_sidecar.md`
- `examples/r002/larger_manual_conversation_candidate_review_table.md`
- `examples/r002/real_log_pilot_01.json`
- `examples/r002/real_log_pilot_01_raw_text_sidecar.md`
- `examples/r002/real_log_pilot_01_candidate_review_table.md`
- `tool/check_r002_mapping_consistency.py`
- `tool/check_r002_sidecar_consistency.py`
- `tool/export_r002_candidate_review_table.py`

## 3. What R002 can currently do

- raw anchor から candidate node、candidate node から accepted node への manual mapping を表現できる。
- raw_id と redacted sidecar の対応を保持できる。
- candidate introduction と candidate promotion を区別できる。
- accepted node で `extends_main` と `extends_branch` を分離して保持できる。
- unaccepted candidate を acceptance 強制なしで保持できる。
- human review 用の candidate review table を export できる。
- R001 validator と並行して supplemental R002 consistency checks を実行できる。
- artificial larger example と bounded real-log-derived pilot の両方に同一ワークフローを適用できる。

## 4. What R002 still cannot do

- full conversation の自動 ingest はできない。
- concept の自動抽出はできない。
- candidate node の自動生成はできない。
- main/branch の分離判断を human judgment なしで決めることはできない。
- convergence・semantic importance・recency・branch_degree・GIF/DIF/sigma semantics を score できない。
- 長大かつ unredacted な会話履歴に対する full scalability を証明していない。

## 5. Known caveats

- checker summary の一部は helper-level summary であり、完全な semantic interpretation ではない。
- accepted/unaccepted candidate status は `tool/export_r002_candidate_review_table.py` の出力で確認すべきであり、`tool/check_r002_mapping_consistency.py` の summary だけに依存すべきではない。
- redacted sidecar は privacy を保持する一方で、後段の再解釈に使える raw context 量を減らす。
- R002 artifacts は依然として manual / semi-manual workflow support である。

## 6. Boundary decision

- real-log pilot handoff 後の現時点で、R002 は当面の機能境界として functionally complete とみなす。
- R003 前に行う変更は small documentation cleanup に限定する。
- R003 は複数の大型機能を同時追加する形で開始しない。

## 7. Candidate R003 directions

以下は decision ではなく、deferred options である。

- semi-automatic candidate suggestion
- ingestion scaffolding
- richer review/audit tooling
- more real-log pilots
- optional DOT visualization for pilot graphs
- later scoring/semantic metrics only after more examples
