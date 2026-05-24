# Formalization

## Version

Round 001 ERG kernel (`R001-kernel`).

## Scope and intent

This document defines the minimum ERG core before any quantitative convergence scoring.
Convergence scoring is **postponed** and moved out of this kernel.

## Four-layer model

We define ERG as a 4-layer typed directed graph bundle:

```text
ERG = (L_raw, L_candidate, L_accepted, L_gitlog)
```

with cross-layer links allowed by explicit edge types.

### Layer 1: raw conversation/artifact layer (`L_raw`)

Purpose: retain unfiltered traces from dialogue and generated artifacts.

#### Node types

- `RawMessage`
- `RawArtifact`
- `RawObservation`

#### Edge types

- `responds_to`
- `references_artifact`
- `records_observation`
- `branches_from_raw`

#### Cycle policy

- **Cycles allowed** (conversation loops and repeated references are expected).

### Layer 2: candidate mathematical layer (`L_candidate`)

Purpose: represent candidate formal objects not yet accepted as kernel.

#### Node types

- `CandidateDefinition`
- `CandidateClaim`
- `CandidateExample`
- `CandidateFailureCase`
- `CandidateQuestion`

#### Edge types

- `defines_candidate`
- `supports_candidate`
- `refutes_candidate`
- `depends_on_candidate`
- `revises_candidate`

#### Cycle policy

- **Cycles allowed** (mutual dependence and iterative refinement are permitted).

### Layer 3: accepted kernel layer (`L_accepted`)

Purpose: store accepted ERG kernel objects for the current round.

#### Node types

- `KernelDefinition`
- `KernelAxiom`
- `KernelExample`
- `KernelFailureCase`
- `KernelDecision`

#### Edge types

- `accepted_from_candidate`
- `extends_main`
- `extends_branch`
- `justified_by_example`
- `bounded_by_failure_case`
- `supersedes_kernel`

#### Cycle policy

- **Cycles not allowed** in `extends_main` subgraph (must be acyclic).
- Cycles for non-extension relations are discouraged; if present, they must not induce cycles in `extends_main`.

### Layer 4: git-log observation layer (`L_gitlog`)

Purpose: external, append-oriented observations derived from git history.

#### Node types

- `GitCommit`
- `GitFileDelta`
- `GitTagOrRound`
- `GitDecisionNote`

#### Edge types

- `parent_commit`
- `touches_file`
- `observes_kernel_change`
- `annotates_round`

#### Cycle policy

- **Cycles not allowed** for `parent_commit` (commit DAG).
- Other edge types should preserve acyclicity with respect to commit ancestry.

## Semantics of `extends_main` vs `extends_branch`

`extends_main` and `extends_branch` are both extension relations in `L_accepted`, but with different merge intent.

- `extends_main(a, b)` means node `b` is a direct canonical extension of `a` on the main accepted trajectory.
  - Invariant: these edges form the single canonical acyclic spine for the round sequence.
- `extends_branch(a, b)` means node `b` extends `a` as a non-canonical exploratory accepted branch.
  - Invariant: branch nodes may later be merged by creating a new node with `extends_main` from the last canonical node and provenance links back to branch nodes.

Intuition: `extends_main` = canonical history; `extends_branch` = accepted-but-side trajectory.

## Minimal example: why pure chronological memory is weaker than ERG

Consider three time-ordered messages:

1. `m1`: propose definition `D0`.
2. `m2`: present failure case `F0` contradicting `D0`.
3. `m3`: propose revised definition `D1` that avoids `F0`.

A plain chronological memory can store `(m1, m2, m3)` but cannot explicitly enforce:

- that `F0` **refutes** `D0`,
- that `D1` **revises** `D0`,
- and that only `D1` is on canonical `extends_main`.

ERG captures this with typed nodes/edges across layers, making acceptance state and revision topology explicit.

## Failure case examples

### Failure case A: canonical-cycle corruption

If accepted nodes satisfy:

```text
extends_main(K0, K1), extends_main(K1, K2), extends_main(K2, K0)
```

then no topological order exists for canonical kernel evolution.
This invalidates auditability and round-by-round reasoning.
Therefore cycles in `extends_main` are forbidden.

### Failure case B: branch/main confusion

If an exploratory update is linked with `extends_main` instead of `extends_branch`,
review tools may incorrectly treat an unverified path as canonical.
This can cause premature lock-in of unstable definitions.

## Postponed items

Quantitative convergence scoring is **not part of Round 001 kernel**.
It is postponed to a separate proposal document.
