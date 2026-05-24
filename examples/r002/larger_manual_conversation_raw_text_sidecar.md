# R002 Larger Manual Conversation Raw Text Sidecar (Artificial Example)

`examples/r002/larger_manual_conversation_example.json` の `L_raw` ノード対応を、schema 変更なしで固定するための人工的 sidecar 例。

| raw_id | turn_index | speaker | text_excerpt | source_note | mapping_note |
|---|---:|---|---|---|---|
| raw.msg.01 | 1 | user | R001 closeout を固定したい | artificial-r002-example | introduces cand.r001_closeout_ready |
| raw.msg.02 | 2 | user | R002 の開始計画を固定したい | artificial-r002-example | introduces cand.r002_kickoff_scope |
| raw.msg.03 | 3 | user | manual mapping checklist が必要 | artificial-r002-example | introduces cand.manual_mapping_checklist |
| raw.msg.04 | 4 | user | larger conversation log に適用したい | artificial-r002-example | introduces cand.larger_log_application |
| raw.msg.05 | 5 | user | candidate / accepted の判断補助が必要 | artificial-r002-example | introduces cand.candidate_decision_support |
| raw.msg.06 | 6 | user | consistency check が必要 | artificial-r002-example | introduces cand.consistency_checks; mentions acc.mapping_checklist_fixed |
| raw.msg.07 | 7 | user | R002 handoff を準備したい | artificial-r002-example | introduces cand.handoff_ready |
| raw.msg.08 | 8 | user | full automatic ingestion を今すぐ入れる案 | artificial-r002-example | introduces cand.full_auto_ingestion_now |
| raw.msg.09 | 9 | user | GIF/DIF semantics を今すぐ入れる案 | artificial-r002-example | introduces cand.gif_dif_semantics_now; mentions acc.defer_gif_dif_sigma_scoring |
| raw.msg.10 | 10 | user | sigma scoring を今すぐ入れる案 | artificial-r002-example | introduces cand.sigma_scoring_now |
| raw.msg.11 | 11 | assistant | larger log application への言及 | artificial-r002-example | mentions acc.larger_log_application_started |
| raw.msg.12 | 12 | assistant | full automatic ingestion defer への言及 | artificial-r002-example | mentions acc.defer_full_automatic_ingestion |
| raw.msg.13 | 13 | assistant | full automatic ingestion は R002 では defer する | artificial-r002-example | introduces cand.defer_full_automatic_ingestion_decision; accepted as acc.defer_full_automatic_ingestion |
| raw.msg.14 | 14 | assistant | GIF/DIF / sigma / convergence scoring は R002 では defer する | artificial-r002-example | introduces cand.defer_gif_dif_sigma_scoring_decision; accepted as acc.defer_gif_dif_sigma_scoring |
