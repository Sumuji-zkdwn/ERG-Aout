# R002 Real Log Pilot Plan

この文書は、R002 の次ステップとして **1つの real conversation log excerpt** に対して、
既存の R001/R002 manual mapping workflow が運用可能かを確認する pilot plan を固定するための計画ノートである。

この計画文書の初期追加時点では、実際の real log data は追加しない方針だった。pilot_01 開始後も、full raw conversation log は保存せず、短い抜粋・redacted sidecar に限定する。

## Pilot status update

- `examples/r002/real_log_pilot_01.json` と sidecar / companion doc の追加により、pilot_01 は開始済み。
- 本計画文書の non-goals は維持し、automatic ingestion や scoring には進めない。

## 1) Purpose

- 次の R002 ステップとして、R001/R002 で整備した manual mapping workflow を、
  1つの実ログ抜粋へ適用できるかを検証する。
- これは **manual / semi-manual mapping pilot** であり、自動化導入の主張ではない。
- 目的は、larger manual example で確認した手順が、実ログ由来の入力でも破綻しないかを確認し、
  handoff 可能な知見を残すことにある。

## 2) Pilot input policy

- 入力は **1つの bounded real conversation excerpt** に限定する。
- excerpt は small-to-medium サイズを優先し、次を含むものを選ぶ。
  - clear な main line
  - 少なくとも 1つの branch / defer / unaccepted candidate
- 本文は privacy を優先し、full raw chat text を含めない。
  - 必要最小限の短い抜粋、または redacted text を sidecar に記録する。
- `raw_id` は sidecar と JSON 間で安定に保ち、再編集時にも再採番を避ける。

## 3) Planned artifacts

pilot 実施時に作成予定の成果物（この PR では未追加）は次の通り。

- `examples/r002/real_log_pilot_01.json`
- `examples/r002/real_log_pilot_01_raw_text_sidecar.md`
- `examples/r002/real_log_pilot_01_candidate_review_table.md`
- `docs/R002_REAL_LOG_PILOT_HANDOFF.md`

## 4) Mapping workflow

pilot では既存 R002 の手動写像原則をそのまま使う。

1. raw anchors を選ぶ。
2. candidate nodes を作る。
3. accepted node への昇格は、可能な限り `accepted_from_candidate` を用いる。
4. `extends_main` と `extends_branch` を分離して扱う。
5. 有用な unaccepted candidates は削除せず残す。
6. `mentions` は raw -> accepted 参照に限定し、candidate promotion には使わない。

## 5) Required checks

pilot JSON 作成後は、既存ツールを次の順で実行する。

1. `python tool/validate_r001_kernel.py examples/r002/real_log_pilot_01.json`
2. `python tool/check_r002_mapping_consistency.py examples/r002/real_log_pilot_01.json`
3. `python tool/check_r002_sidecar_consistency.py examples/r002/real_log_pilot_01.json examples/r002/real_log_pilot_01_raw_text_sidecar.md`
4. `python tool/export_r002_candidate_review_table.py examples/r002/real_log_pilot_01.json --sidecar examples/r002/real_log_pilot_01_raw_text_sidecar.md`

- warning と note は handoff に記録する。
- validator と checker の挙動変更は行わない。

## 6) Success criteria

pilot 完了条件は次とする。

- graph が validate される。
- `raw_id` と sidecar rows が整合する。
- candidate review table が人手レビュー可能な可読性を持つ。
- main spine と branch の分離を説明できる。
- unresolved candidates を受理強制せず保持できる。
- handoff note に「うまくいった点 / 壊れた点」を残せる。

## 7) Explicit non-goals

この pilot では次を実施しない。

- automatic ingestion
- automatic concept extraction
- automatic candidate generation
- scoring（GIF/DIF, sigma, recency, branch_degree, semantic importance, convergence を含む）
- new theory claims
- schema changes

## 8) Scope and boundary reminder

- この文書は R002-C の次計画を固定するための documentation である。
- 実データ投入・仕様変更・自動化導入は別 PR で扱う。
