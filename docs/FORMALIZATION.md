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
- `reply` (`M_i -> M_j`)
- `mentions` (`M_i -> KConcept_j`)
- `introduces` (`M_i -> CandSymbol_k`)

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
- `CandSymbol`

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
- `KConcept`

#### Edge types

- `accepted_from_candidate`
- `extends_main`
- `extends_branch`
- `justified_by_example`
- `bounded_by_failure_case`
- `supersedes_kernel`

#### Cycle policy

- **Cycles not allowed** in `extends_main`.
- `extends_main` must be a single linear chain (a total order over accepted revision points in the round), not a tree and not a DAG with merges.
- `extends_branch` may branch from chain nodes, but branch edges are non-canonical.

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

## Legacy Eve/ERG motifs and Round 001 classification

Observed motifs from older Eve/ERG-style logs and tooling include:
`memory_erg_app.py`, `memory_store`, JSONL nodes, `features`, `sigma`, `M_i`, `C_j`,
`extends_main`, `extends_branch`, `branch_degree`, `recency`.

Round 001 classifies these motifs into four buckets.

### A) accepted kernel candidate

- `extends_main` / `extends_branch` as accepted-layer evolution primitives.
- `M_i` as message-indexed raw memory symbol.
- `recency` as local retrieval hint.
- `branch_degree` as local branching hint.

### B) implementation artifact

- `memory_erg_app.py` (or sibling scripts).
- `memory_store` directory layout.
- JSONL physical format for node/edge persistence.

### C) postponed meta-theory

- Global semantics of `features`.
- Global semantics of `sigma`.
- Any quantitative convergence-scoring function.
- `T_h` / `reconditioning` global semantics.

### D) unclear legacy term

- Exact historical meaning differences among Eve / ERG / HVM labels.
- Legacy overloaded `C_j` usage without concept-vs-candidate split.

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

## Legacy Adam2 matrix view (critic status)

This view is retained only as a rejected-for-now candidate block.
It is **not accepted kernel** in Round 001.

### Objects

- `M = {M_1, ..., M_T}` (messages)
- `K = {KConcept_1, ..., KConcept_n}` (accepted concepts)
- `H ∈ {0,1}^{T×n}` (mentions-only incidence)
- `P_main ∈ {0,1}^{T×T}` (candidate mapping of canonical progression)
- `P_branch ∈ {0,1}^{T×T}` (candidate mapping of exploratory progression)

`H_{ij} = 1` iff `M_i` mentions `KConcept_j`.

### Candidate relation matrix

```text
W = αH^T H + βH^T P_main H + γH^T P_branch H
```

Status:

- **legacy proposal / accepted-kernel-candidate only**.
- **not accepted kernel**.

## Critic review of PR #7 (what should NOT be accepted)

### 1) `C_j` ambiguity: reject overload

`C_j` was used ambiguously as both concept and candidate symbol. This is unstable.
Round 001 splits roles:

- `KConcept_j`: accepted concept node.
- `CandSymbol_k`: candidate formal symbol.

Any text using unsplit `C_j` as both is rejected.

### 2) `extends_main` ambiguity: resolve to path

PR #7 mixed “single canonical spine” with DAG-like wording. For Round 001 this is rejected.
Accepted rule:

- `extends_main` is a **single linear chain** (path / total order).
- Not a tree.
- Not a DAG with merges.

This is the minimum stable invariant for R001 auditability.

### 3) `H^T P H` semantics: one working and one misleading minimal case

Working case:

- Messages: `M_1, M_2`
- Concepts: `A, B`
- `H = [[1,0],[0,1]]`
- `P_main(1,2)=1` only

Then `H^T P_main H` gives one directed cross-term from `A` to `B`, matching a transition from a message mentioning `A` to one mentioning `B`.

Misleading case:

- `M_1` mentions `A` and `B` (`[1,1]`), `M_2` mentions `A` (`[1,0]`)
- `P_main(1,2)=1`

`H^T P_main H` now contributes both `A->A` and `B->A`, but this does not distinguish whether `B` was semantically revised, merely co-mentioned, or negated. Co-mention conflation makes interpretation unstable.

Therefore `H^T P H` is useful only as coarse co-transition summary, not accepted semantics.

### 4) Should `reply` be in matrix form (`P_reply`)?

Not in Round 001 kernel.

Reason: `reply` is conversational adjacency, while current matrix view is already underdetermined for semantic transitions. Adding `P_reply` multiplies ambiguity (reply graph vs revision graph vs mention graph) without stable interpretation.

So `reply` remains an explicit edge type in `L_raw`, not part of current matrix block.

### 5) Should `W` remain?

Keep it only as a **postponed candidate note**, not as operational kernel logic.

Rationale: deleting it loses review context, but promoting it causes premature formal lock-in on unstable semantics (`H`, orientation, weighting meaning).

### 6) Underdetermined definitions in PR #7 (at least three)

Rejected as underdetermined unless clarified:

1. Orientation convention of `P_main` / `P_branch` indices.
2. Exact semantics of `H_{ij}=1` under quoting, negation, and hypothetical mention.
3. Meaning of `branch_degree` (out-degree? weighted? time-windowed?).
4. Meaning of `recency` (absolute time decay? turn count? bucketed rank?).
5. Role of `sigma` (confidence, salience, or routing score).

### 7) Smaller R001 kernel (deletion proposal)

For merge, minimum necessary kernel should keep only:

- 4-layer structure.
- Layer node/edge types.
- Cycle policies.
- `extends_main` path invariant.
- `extends_branch` as non-canonical branch relation.
- Minimal “chronological memory is weaker” example.
- At least one failure case.

Everything else stays candidate/postponed (Legacy GIF/DIF, Legacy Adam2 matrix block, `W`, `features/sigma` meta-theory).

## Minimal example: why pure chronological memory is weaker than ERG

Consider three time-ordered messages:

1. `m1`: propose definition `D0`.
2. `m2`: present failure case `F0` contradicting `D0`.
3. `m3`: propose revised definition `D1` that avoids `F0`.

A plain chronological memory can store `(m1, m2, m3)` but cannot explicitly enforce:

- that `F0` **refutes** `D0`,
- that `D1` **revises** `D0`,
- and that only `D1` is on canonical `extends_main`.

## Failure case examples

### Failure case A: canonical-cycle corruption

If accepted nodes satisfy:

```text
extends_main(K0, K1), extends_main(K1, K2), extends_main(K2, K0)
```

then no linear canonical order exists.
Therefore cycles in `extends_main` are forbidden.

### Failure case B: branch/main confusion

If an exploratory update is linked with `extends_main` instead of `extends_branch`,
unverified paths are mistaken as canonical.

## Postponed items

Quantitative convergence scoring is **not part of Round 001 kernel**.
