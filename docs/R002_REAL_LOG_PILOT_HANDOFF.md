# R002 Real Log Pilot Handoff

## 1. Status

- `pilot_01` は、bounded かつ redacted な real-log manual mapping pilot として完了した。
- これは automatic ingestion ではない。
- これは automatic concept extraction ではない。
- これは scoring ではない。

## 2. Artifacts

本 pilot の関連成果物は次の通り。

- `examples/r002/real_log_pilot_01.json`
- `examples/r002/real_log_pilot_01_raw_text_sidecar.md`
- `examples/r002/real_log_pilot_01_candidate_review_table.md`
- `docs/R002_REAL_LOG_PILOT_01.md`
- `docs/R002_REAL_LOG_PILOT_PLAN.md`

## 3. What worked

- R001 kernel JSON format は、bounded な real-log 由来 excerpt を扱えた。
- sidecar と `raw_id` の alignment は機能した。
- `accepted_from_candidate` による candidate promotion は機能した。
- accepted main spine は表現できた。
- branch decision は表現できた。
- unaccepted candidates を、受理強制せずに保持できた。
- candidate review table により accepted / unaccepted 状態を可視化できた。
- privacy-preserving な short/redacted sidecar policy は workflow と両立した。

## 4. Observed weak points / limitations

- excerpt は小さく redacted であり、full conversation scalability を証明するものではない。
- raw anchor selection は依然として手動である。
- candidate naming は依然として手動である。
- main/branch separation は依然として人手判断に依存する。
- checker summary は exporter-level status を完全には要約しないため、`unaccepted candidates: (none)` と表示される場合がある。accepted/unaccepted status は candidate review table を参照する必要がある。
- automatic ingestion, automatic candidate generation, scoring は未実装である。
- GIF/DIF, sigma, recency, branch_degree, semantic importance, convergence semantics は未検証である。

## 5. Boundary decision

- R002 は、larger real conversation log mapping までの到達点として合理的な checkpoint に到達した。
- R002 は、small な documentation cleanup を除き、`pilot_01` の文書化後に停止すべきである。
- automatic ingestion, candidate generation, scoring, semantic metrics は R003 以降へ defer すべきである。

## 6. Recommended next phase

- R003 は、この handoff のレビュー後にのみ開始すべきである。
- R003 scope 候補は、semi-automatic candidate suggestion か ingestion scaffolding のいずれか一方に限定し、同時導入は避ける。
- R003 は R001/R002 artifacts に grounded に進め、新しい理論を先行追加せず、より多くの examples 運用を優先すべきである。

## 7. Validation snapshot

`real_log_pilot_01` についての期待チェック結果（現行の bounded pilot checkpoint）は次の通り。

- `validate_r001_kernel.py` on `real_log_pilot_01`: VALID
- `check_r002_mapping_consistency.py` on `real_log_pilot_01`: no warnings / no notes
- `check_r002_sidecar_consistency.py` on `real_log_pilot_01` + sidecar: no warnings
- `export_r002_candidate_review_table.py`: Warnings none, accepted 7, unaccepted 2

また、`larger_manual_conversation_example` に対する regression checks も pass している。
