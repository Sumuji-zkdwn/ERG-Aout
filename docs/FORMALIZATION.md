# Formalization

## Version

Round 001 ERG kernel (`R001-kernel`).

## Scope and intent

This document contains only the accepted Round 001 kernel.
Quantitative convergence scoring is postponed and not part of this kernel.

## Four-layer model

We define ERG as a 4-layer typed directed graph bundle:

```text
ERG = (L_raw, L_candidate, L_accepted, L_gitlog)
```

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
- `reply` (`M_i -> M_j`)
- `mentions` (`M_i -> KConcept_j`)
- `introduces` (`M_i -> CandSymbol_k`)

#### Cycle policy

- **Cycles allowed**.

### Layer 2: candidate mathematical layer (`L_candidate`)

Purpose: represent candidate formal objects not yet accepted as kernel.

#### Node types

- `CandidateDefinition`
- `CandidateClaim`
- `CandidateExample`
- `CandidateFailureCase`
- `CandidateQuestion`
- `CandSymbol`

#### Edge types

- `defines_candidate`
- `supports_candidate`
- `refutes_candidate`
- `depends_on_candidate`
- `revises_candidate`

#### Cycle policy

- **Cycles allowed**.

### Layer 3: accepted kernel layer (`L_accepted`)

Purpose: store accepted ERG kernel objects for the round.

#### Node types

- `KernelDefinition`
- `KernelAxiom`
- `KernelExample`
- `KernelFailureCase`
- `KernelDecision`
- `KConcept`

#### Edge types

- `accepted_from_candidate`
- `extends_main`
- `extends_branch`
- `justified_by_example`
- `bounded_by_failure_case`
- `supersedes_kernel`

#### Cycle policy

- `extends_main` must be acyclic.
- `extends_main` is a single linear canonical chain (path invariant).
- `extends_branch` is non-canonical and may branch from canonical nodes.

### Layer 4: git-log observation layer (`L_gitlog`)

Purpose: append-oriented observations derived from git history.

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

- `parent_commit` is acyclic.


## Cross-layer edge policy

Edge types are listed under the layer where they are primarily observed or controlled.
However, some edges may target nodes in another layer when endpoint node types explicitly indicate a cross-layer link.

Examples:

- `reply`: `L_raw -> L_raw`
- `mentions`: `L_raw -> L_accepted`
- `introduces`: `L_raw -> L_candidate`
- `accepted_from_candidate`: `L_candidate -> L_accepted`
- `observes_kernel_change`: `L_gitlog -> L_accepted`

## Semantics of `extends_main` vs `extends_branch`

- `extends_main(a, b)`: `b` is the next canonical accepted node after `a`.
- `extends_branch(a, b)`: `b` is a non-canonical exploratory accepted branch from `a`.

## Minimal example: why chronological memory is weaker than ERG

Given messages:

1. `m1`: proposes definition `D0`.
2. `m2`: provides failure case `F0` against `D0`.
3. `m3`: proposes revised definition `D1`.

Chronological storage alone keeps order `(m1, m2, m3)` but does not encode explicit
`refutes`, `revises`, and canonical/non-canonical acceptance topology.

## Failure cases

### Failure case A: canonical cycle corruption

If:

```text
extends_main(K0, K1), extends_main(K1, K2), extends_main(K2, K0)
```

canonical order is invalid. This is forbidden.

### Failure case B: branch/main confusion

If exploratory updates are linked by `extends_main` instead of `extends_branch`,
non-canonical updates are incorrectly treated as canonical.
