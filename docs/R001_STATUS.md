# R001 Status

この文書は、R001 の到達点と境界を固定し、R002 以降で追加する対象を明確化するためのステータス整理である。

## R001 で現在できること

R001 の範囲では、次が実装・文書化済みである。

- graph JSON validation
- extends_main / extends_branch validation
- DOT export
- full / accepted / spine projection
- short labels
- edge semantics document
- semantics coverage checker
- development sample graph through PR #28

## R001 でまだできないこと

R001 の範囲では、次は未実装・未確立である。

- automatic conversation ingestion
- automatic concept extraction
- convergence scoring
- GIF/DIF semantics
- sigma semantics
- recency
- branch_degree
- semantic importance scoring

## R002 候補

R002 候補として、manual conversation-to-ERG example を追加する。

意図は、自然言語の会話断片から、手作業で R001 形式の ERG へ写像する手順と最小例を提示し、
将来の automatic conversation ingestion / automatic concept extraction の前段を与えることにある。

## Scope note

本メモはステータス整理のみを目的とし、新しい理論主張を導入しない。
