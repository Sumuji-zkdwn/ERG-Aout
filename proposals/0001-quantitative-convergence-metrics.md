# Proposal 0001: Quantitative Convergence Framework (Draft)

## Scope and sequencing

This proposal is a **draft for critic review**.
In this round we update only:

- `docs/FORMALIZATION.md` (formal definitions draft)
- `docs/CONVERGENCE.md` (operational logging draft)

`README.md` is intentionally unchanged.

## Goal

Resolve the open issue: **"How to define convergence quantitatively."**

## Draft model

Define a per-topic convergence score at round `t`:

```text
C_t(topic) = w1*S_stability
           + w2*S_resolution
           + w3*S_rejection_traceability
           + w4*S_example_failure_coverage
           + w5*S_document_focus
```

with:

```text
w1=0.30, w2=0.25, w3=0.20, w4=0.15, w5=0.10
sum(wi)=1, each sub-score in [0,1]
```

## Sub-score definitions (draft)

- `S_stability`:
  `1 - min(1, definition_churn_lines(topic, k) / churn_cap)`
- `S_resolution`:
  `resolved_open_questions(topic, k) / max(1, opened_open_questions(topic, k))`
- `S_rejection_traceability`:
  `rejections_with_explicit_rationale(topic, k) / max(1, total_rejections(topic, k))`
- `S_example_failure_coverage`:
  `accepted_claims_with_example_and_failure(topic) / max(1, accepted_claims(topic))`
- `S_document_focus`:
  `1 - min(1, readme_churn_lines(k) / max(1, formalization_churn_lines(k)))`

`k` is a rolling round window (default `k=3`).

## Status labels from score (draft)

- `exploring`: `C_t < 0.50`
- `stabilizing`: `0.50 <= C_t < 0.80`
- `converged_candidate`: `C_t >= 0.80` for `3` consecutive rounds

Additionally, `converged_candidate` requires no unresolved `critical` open question older than 2 rounds.

## Proposed docs changes in this issue

1. `docs/FORMALIZATION.md`
   - add a "Quantitative convergence (draft)" section with variables, score equation, and status labels.
   - keep it marked as draft and linked to this proposal.

2. `docs/CONVERGENCE.md`
   - add a score computation procedure.
   - extend the round table schema to include `Topic`, `C_t`, and `Status`.
   - add one example row with placeholder values.

## Risks and review points

- Weight selection may bias behavior.
- `S_document_focus` can be gamed by suppressing useful README updates.
- Need critic agreement on `k`, `churn_cap`, and open-question severity tagging.

## Decision request

If accepted after review:

- promote formula + variable definitions to accepted kernel text.
- use the extended convergence table format in subsequent rounds.
