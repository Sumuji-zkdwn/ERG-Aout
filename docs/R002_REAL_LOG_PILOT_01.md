# R002 Real Log Pilot 01

## 1) Purpose

この文書は、R002-C における最初の bounded real-log 由来の手動写像 pilot（`real_log_pilot_01`）の意図と読み方を固定する。

- 対象は short / redacted excerpt ベースの小規模 manual mapping。
- 目的は、R001 kernel JSON 形式を維持したまま、実ワークフロー由来断片へ適用可能かを確認すること。

## 2) Why short / redacted excerpts

この pilot は full raw conversation log の保存を目的としない。privacy と運用境界を優先し、sidecar では次のみ扱う。

- 短い text excerpt
- redacted source note
- raw ノードとの対応表

よって、実ログ本文全量は含めない。

## 3) Main spine meaning

`real_log_pilot_01.json` の main spine は、次の進行固定を表す。

1. PR #53 candidate review exporter 確認
2. R001 closeout 後の R002 手動写像支援状態の固定
3. R002 の stop point を larger real conversation log mapping までに限定
4. PR #54 real-log pilot plan step の固定
5. pilot execution start の開始決定

## 4) Unaccepted / deferred candidates

本 pilot では、次の候補は質問起点として未受理のまま保持する。

- `cand.progress_assessment_requested`
- `cand.r002_stop_point_question`

また、境界条件として次を受理した。

- `acc.privacy_preserving_sidecar_policy`
- `acc.defer_automation_and_scoring`

これにより「短い抜粋・redacted 方針」と「automation/scoring defer」の R002 境界を graph 上で明示する。

## 5) Validation / consistency checks

次の順でチェックする。

```bash
python tool/validate_r001_kernel.py examples/r002/real_log_pilot_01.json
python tool/check_r002_mapping_consistency.py examples/r002/real_log_pilot_01.json
python tool/check_r002_sidecar_consistency.py examples/r002/real_log_pilot_01.json examples/r002/real_log_pilot_01_raw_text_sidecar.md
```

回帰確認として既存 larger manual example も併せて実行する。

## 6) Explicit boundary (non-automation)

この pilot は manual mapping 実証用であり、次は実施しない。

- automatic ingestion
- automatic concept extraction
- automatic candidate generation
- scoring（GIF/DIF, sigma, recency, branch_degree, semantic importance, convergence）

つまり、本成果物は **automatic ingestion でも automatic candidate generation でもない**。
