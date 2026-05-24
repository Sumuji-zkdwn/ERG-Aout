# REVIEW-R001 critical notes

Status: review note (not accepted kernel text).

## 1) `C_j` ambiguity critique

Legacy `C_j` was overloaded between concept nodes and candidate formal symbols.
For review clarity, this must be split conceptually; otherwise traces are ambiguous.

## 2) `H^T P H` examples

### Minimal working example

- Messages: `M_1, M_2`
- Concepts: `A, B`
- `H = [[1,0],[0,1]]`
- `P_main(1,2)=1`

`H^T P_main H` yields a directed transition-like contribution from `A` to `B`.

### Minimal misleading example

- `M_1` mentions `A` and `B`
- `M_2` mentions `A`
- `P_main(1,2)=1`

`H^T P_main H` mixes co-mention with semantic transition and may over-interpret
`B -> A` as meaningful revision when it may be incidental.

## 3) `W` postponement rationale

`W = αH^T H + βH^T P_main H + γH^T P_branch H` is useful as candidate summary,
but currently underdetermined (orientation, weighting, semantics). Keep postponed.

## 4) `P_reply` rejection

`reply` is conversational adjacency in raw traces. Adding `P_reply` into the matrix view
before stable semantics increases ambiguity and is not needed for R001 kernel.

## 5) Underdetermined terms (examples)

- Orientation convention for `P_main` / `P_branch`.
- Interpretation of `H_{ij}=1` under quote/negation/hypothetical mention.
- Operational meaning of `sigma`.
- Exact operational definition of `branch_degree`.
- Exact operational definition of `recency`.

## 6) Smaller R001 kernel proposal

Keep only:

- 4-layer structure
- node/edge types
- cycle policies
- `extends_main` path invariant
- `extends_branch` non-canonical relation
- one minimal example
- failure cases

Everything else remains proposal/legacy/postponed.
