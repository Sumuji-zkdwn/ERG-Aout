# R002 Candidate Review Table

| candidate_id | introduced_by_raw | raw_excerpt | status | accepted_target | accepted_type | review_note |
|---|---|---|---|---|---|---|
| cand.candidate_decision_support | raw.msg.05 | candidate / accepted の判断補助が必要 | unaccepted | (none) | (none) | candidate remains unaccepted |
| cand.consistency_checks | raw.msg.06 | consistency check が必要 | unaccepted | (none) | (none) | candidate remains unaccepted |
| cand.defer_full_automatic_ingestion_decision | raw.msg.13 | full automatic ingestion は R002 では defer する | accepted | acc.defer_full_automatic_ingestion | KernelDecision | candidate promoted to accepted |
| cand.defer_gif_dif_sigma_scoring_decision | raw.msg.14 | GIF/DIF / sigma / convergence scoring は R002 では defer する | accepted | acc.defer_gif_dif_sigma_scoring | KernelDecision | candidate promoted to accepted |
| cand.full_auto_ingestion_now | raw.msg.08 | full automatic ingestion を今すぐ入れる案 | unaccepted | (none) | (none) | candidate remains unaccepted |
| cand.gif_dif_semantics_now | raw.msg.09 | GIF/DIF semantics を今すぐ入れる案 | unaccepted | (none) | (none) | candidate remains unaccepted |
| cand.handoff_ready | raw.msg.07 | R002 handoff を準備したい | accepted | acc.r002_handoff_prepared | KernelDecision | candidate promoted to accepted |
| cand.larger_log_application | raw.msg.04 | larger conversation log に適用したい | accepted | acc.larger_log_application_started | KernelDefinition | candidate promoted to accepted |
| cand.manual_mapping_checklist | raw.msg.03 | manual mapping checklist が必要 | accepted | acc.mapping_checklist_fixed | KernelDefinition | candidate promoted to accepted |
| cand.r001_closeout_ready | raw.msg.01 | R001 closeout を固定したい | accepted | acc.r001_closeout_fixed | KernelDefinition | candidate promoted to accepted |
| cand.r002_kickoff_scope | raw.msg.02 | R002 の開始計画を固定したい | accepted | acc.r002_plan_fixed | KernelDefinition | candidate promoted to accepted |
| cand.sigma_scoring_now | raw.msg.10 | sigma scoring を今すぐ入れる案 | unaccepted | (none) | (none) | candidate remains unaccepted |

## Warnings
- none
