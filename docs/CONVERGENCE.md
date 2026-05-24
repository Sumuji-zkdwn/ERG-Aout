# Convergence Log

## Definition of convergence

A topic is considered more converged when:

1. accepted definitions change less frequently;
2. open questions decrease or become more precise;
3. rejected alternatives are explicitly recorded;
4. examples and failure cases stop changing the core definition;
5. README diffs become smaller while FORMALIZATION becomes sharper.

## Suggested measurable indicators

```text
accepted_claim_count
open_question_count
rejected_claim_count
definition_churn_lines
readme_churn_lines
formalization_churn_lines
rounds_since_last_kernel_change
```

## Quantitative scoring procedure (draft)

Draft source: `proposals/0001-quantitative-convergence-metrics.md`.

Per topic and round `t`, compute:

```text
C_t = 0.30*S_stability
    + 0.25*S_resolution
    + 0.20*S_rejection_traceability
    + 0.15*S_example_failure_coverage
    + 0.10*S_document_focus
```

Operational default window: `k = 3` rounds.

Status mapping (draft):

- `exploring`: `C_t < 0.50`
- `stabilizing`: `0.50 <= C_t < 0.80`
- `converged_candidate`: `C_t >= 0.80` for 3 consecutive rounds and no unresolved critical open question older than 2 rounds.

## Round table

| Round | Date | Topic | Accepted | Rejected | Open | README changed | Formalization changed | C_t | Status |
|---|---|---|---:|---:|---:|---|---|---:|---|
| R000 | YYYY-MM-DD | initialize toy model | 5 | 0 | 4 | yes | yes | 0.00 | exploring |
