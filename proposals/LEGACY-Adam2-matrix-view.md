# Legacy Adam2 matrix view

Status: rejected-for-now / candidate only (not accepted kernel).

## Objects

- `M = {M_1, ..., M_T}`
- `C = {C_1, ..., C_n}`
- `H ∈ {0,1}^{T×n}`
- `P_main ∈ {0,1}^{T×T}`
- `P_branch ∈ {0,1}^{T×T}`

where:

- `H_{ij}=1` iff message `M_i` mentions concept `C_j`.
- `P_main` encodes `extends_main` candidates.
- `P_branch` encodes `extends_branch` candidates.

## Candidate relation matrix

```text
W = αH^T H + βH^T P_main H + γH^T P_branch H
```

This matrix view is retained for legacy reference only.
It is not part of Round 001 accepted kernel.
