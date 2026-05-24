# Formalization

## Version

Round 001 ERG kernel (`R001-kernel`).

## Scope and intent

This document defines the minimum ERG core before any quantitative convergence scoring.
Convergence scoring is **postponed** and moved out of this kernel.

Round 001 is not a generic typed-graph exercise: it is a model of ERG-specific
conversation memory, semantic revisit, and local state management.

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

## Legacy Eve/ERG motifs and Round 001 classification

Observed motifs from older Eve/ERG-style logs and tooling include:
`memory_erg_app.py`, `memory_store`, JSONL nodes, `features`, `sigma`, `M_i`, `C_j`,
`extends_main`, `extends_branch`, `branch_degree`, `recency`.

Round 001 classifies these motifs into four buckets.

### A) accepted kernel candidate

These are admitted into Round 001 semantics:

- `extends_main` / `extends_branch` as accepted-layer evolution primitives.
- `M_i` as message-indexed raw memory symbol (raw trace identity).
- `C_j` as candidate-indexed formal symbol (candidate-layer identity).
- `recency` as local state hint for retrieval priority (not a convergence score).
- `branch_degree` as local branching-state hint for exploratory pressure.

### B) implementation artifact

These are recognized as implementation choices, not kernel axioms:

- `memory_erg_app.py` (or sibling scripts).
- `memory_store` directory layout.
- JSONL physical format for node/edge persistence.

### C) postponed meta-theory

These are meaningful but deferred:

- Global semantics of `features` vector spaces.
- Global semantics of `sigma` (normalization, proof obligations, probabilistic meaning).
- Any quantitative convergence-scoring function that composes above signals.
- `T_h` / `reconditioning` global semantics.

### D) unclear legacy term

Terms retained only as legacy placeholders until clarified:

- Exact historical meaning differences among Eve / ERG / HVM labels in old logs.
- Whether `M_i`/`C_j` should be strict canonical identifiers or merely notation.
- Whether `sigma` denotes certainty, salience, or routing state in legacy traces.


## Legacy GIF/DIF transform view

GIF/DIF is treated as a legacy transform viewpoint over ERG states, not as ERG core itself.
Round 001 does **not** absorb GIF/DIF into the accepted kernel ontology.

### Provisional interpretation

- ERG state at time `t`: `G_t`.
- `DIF_t`: a graph difference or edit sequence from `G_t` to `G_{t+1}`.
- `GIF`: a mechanism that generates/expands structured operation sequences.
- Operation composition:

```text
G_{t+1} = op_k \circ ... \circ op_1(G_t)
```

Mathematical scope in Round 001 stays within finite graph transforms,
rewriting systems, and state transitions.

### Classification in Round 001

- operation sequence: **accepted kernel candidate**.
- graph/state transform: **accepted kernel candidate**.
- "4 principles + 1 empty slot": **legacy proposal** (not current spec).
- `T_h` / `reconditioning`: **postponed meta-theory**.
- strict definition of GIF/DIF: **unclear legacy term**.

### Boundary to accepted layer

- GIF/DIF terms may appear in `L_raw` and `L_candidate` as legacy/candidate viewpoints.
- GIF/DIF terms are **not promoted** to `L_accepted` as kernel primitives in Round 001.
- Promotion requires later explicit definitions and failure-case validation.

## ERG-specific kernel behavior (not generic typed graph)

Round 001 adds ERG-specific operational interpretation.

### 1) Conversation memory

- Raw layer stores message-indexed memory atoms `M_i`.
- Candidate layer stores revisitable formal candidates `C_j`.
- Accepted layer stores canonicalized kernel steps connected by `extends_main`.

### 2) Semantic revisit

A revisit operation is modeled as:

1. Select prior `M_i` under local state (`recency`, `branch_degree`).
2. Map to one or more `C_j` via candidate relations.
3. Either:
   - commit to canonical path via `extends_main`, or
   - keep exploratory continuation via `extends_branch`.

This makes revisit semantics explicit, not mere time-ordered recall.

### 3) Local state management

Round 001 allows local per-node/per-branch state:

- `recency`: retrieval-priority state.
- `branch_degree`: divergence-pressure state.

Constraints:

- These states may guide revisit/routing decisions.
- They do **not** define truth, acceptance, or convergence by themselves.
- They are auxiliary control state, not kernel validity axioms.

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

ERG captures this with typed nodes/edges and local revisit state (`recency`, `branch_degree`),
making acceptance state and revision topology explicit.

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

### Failure case C: local-state absolutization

If high `recency` is treated as automatic acceptance,
recent but weak candidates can overwrite better-established kernel nodes.
Local state must remain routing aid, not truth criterion.

## Postponed items

Quantitative convergence scoring is **not part of Round 001 kernel**.
It remains postponed to a separate proposal document.
