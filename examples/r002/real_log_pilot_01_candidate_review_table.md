# R002 Candidate Review Table

| candidate_id | introduced_by_raw | raw_excerpt | status | accepted_target | accepted_type | review_note |
|---|---|---|---|---|---|---|
| cand.defer_automation_and_scoring | raw.msg.08 | automatic ingestion や scoring にはまだ進まない | accepted | acc.defer_automation_and_scoring | KernelDecision | candidate promoted to accepted |
| cand.pr53_candidate_review_exporter_checked | raw.msg.01 | PR #53 の candidate review exporter を確認する | accepted | acc.pr53_review_exporter_accepted | KernelDefinition | candidate promoted to accepted |
| cand.privacy_preserving_sidecar_policy | raw.msg.07 | 実ログ本文は短い抜粋または redacted text にする | accepted | acc.privacy_preserving_sidecar_policy | KernelDecision | candidate promoted to accepted |
| cand.progress_assessment_requested | raw.msg.02 | 現段階でどの程度進行したか確認する | unaccepted | (none) | (none) | candidate remains unaccepted |
| cand.r001_closed_r002_support_layer | raw.msg.03 | R001 は閉じ、R002 は手動写像支援レイヤに入った | accepted | acc.r002_progress_state_fixed | KernelDefinition | candidate promoted to accepted |
| cand.r002_stop_point_question | raw.msg.04 | どこまで進むのがよいかを確認する | unaccepted | (none) | (none) | candidate remains unaccepted |
| cand.real_log_mapping_stop_point | raw.msg.05 | larger real conversation log mapping までで止める | accepted | acc.r002_stop_at_real_log_mapping | KernelDecision | candidate promoted to accepted |
| cand.real_log_pilot_execution_start | raw.msg.09 | 次に行きましょう | accepted | acc.real_log_pilot_execution_started | KernelDecision | candidate promoted to accepted |
| cand.real_log_pilot_plan_step | raw.msg.06 | PR #54 で real-log pilot plan を追加する | accepted | acc.real_log_pilot_plan_fixed | KernelDefinition | candidate promoted to accepted |

## Warnings
- none
