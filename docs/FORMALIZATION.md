# Formalization

## Version

v0.1 toy model.

## Basic objects

Let

```text
G = (V, E, type_V, type_E, attr)
```

where:

- `V` is a finite set of nodes.
- `E` is a finite set of directed typed edges.
- `type_V: V -> NodeType`.
- `type_E: E -> EdgeType`.
- `attr` assigns metadata to nodes and edges.

## Node types

Initial node types:

```text
Message
Proposal
Claim
Definition
Operation
Example
FailureCase
File
Commit
Decision
OpenQuestion
```

## Edge types

Initial edge types:

```text
mentions
proposes
refines
rejects
depends_on
contradicts
implements
logs
supersedes
accepted_as
needs_test
```

## Acceptance rule

A claim `c` may be marked `accepted_as` only if:

1. `c` has a written definition.
2. `c` has at least one minimum example.
3. `c` has at least one failure case or boundary case.
4. `c` has been reviewed by the critic role.
5. `c` is reflected in the convergence log.

## Open issues

- Whether ERG should remain a directed multigraph or become a DAG at the accepted layer.
- How to represent cycles without destroying the acyclic proof/history layer.
- Whether git commits should be first-class nodes or only source metadata.
- How to calibrate quantitative convergence parameters (`k`, `churn_cap`, status thresholds) from empirical rounds.



## Quantitative convergence (draft)

Draft source: `proposals/0001-quantitative-convergence-metrics.md` (pending critic review).

For topic `x` at round `t`:

```text
C_t(x) = 0.30*S_stability
       + 0.25*S_resolution
       + 0.20*S_rejection_traceability
       + 0.15*S_example_failure_coverage
       + 0.10*S_document_focus
```

where each sub-score is in `[0,1]`.

Default round window: `k = 3`.

Draft status labels:

- `exploring` if `C_t < 0.50`
- `stabilizing` if `0.50 <= C_t < 0.80`
- `converged_candidate` if `C_t >= 0.80` for 3 consecutive rounds and no unresolved critical open question older than 2 rounds.
