# R001 edge semantics (stage R001-next)

Status: normative interpretation note for the current R001 graph shape.

This document defines the intended meaning of each edge type that appears in `examples/r001/sample_r001_development_graph.json`.

Scope boundary:
- This is a semantic specification for reading/writing R001 graphs.
- This does **not** add automatic inference or automatic construction rules.
- Validation and policy checks remain those implemented in the current R001 validator.

## Layer legend

- `L_raw`: source-side conversational and artifact observations.
- `L_candidate`: provisional objects before acceptance.
- `L_accepted`: accepted kernel objects in the current round.
- `L_gitlog`: git-history observations.

## Edge type semantics

## 1) `reply`

- Allowed layer endpoints: `L_raw -> L_raw`.
- Meaning: a raw item is a reply/response to another raw item in conversation flow.
- Prohibited uses:
  - Must not connect candidate, accepted, or gitlog nodes.
  - Must not be interpreted as acceptance, entailment, or kernel extension.

## 2) `mentions`

- Allowed layer endpoints: `L_raw -> L_accepted`.
- Meaning: a raw utterance or artifact refers to an accepted kernel object.
- Prohibited uses:
  - Must not be treated as creation of accepted content.
  - Must not be used as a substitute for `accepted_from_candidate`.
  - Must not target non-accepted layers.

## 3) `introduces`

- Allowed layer endpoints: `L_raw -> L_candidate`.
- Meaning: raw material introduces a candidate object into consideration.
- Prohibited uses:
  - Must not directly produce accepted status.
  - Must not target accepted or gitlog nodes.

## 4) `accepted_from_candidate`

- Allowed layer endpoints: `L_candidate -> L_accepted`.
- Meaning: a candidate object is mapped into accepted state (adoption/projection from candidate space into kernel space).
- Prohibited uses:
  - Must not be read as a raw mention or conversational link.
  - Must not originate from `L_raw` or `L_gitlog`.
  - Must not target `L_candidate`.

## 5) `extends_main`

- Allowed layer endpoints: `L_accepted -> L_accepted`.
- Meaning: canonical accepted-history extension along the main accepted chain.
- History-structure definition (not display-only):
  - `extends_main` edges define the canonical accepted lineage.
  - The canonical lineage is constrained to one linear acyclic path (single start, single end, no fan-in/fan-out).
  - Nodes on this path are the canonical accepted spine at this stage.
- Prohibited uses:
  - Must not connect non-accepted layers.
  - Must not be used for side alternatives that are intentionally off the canonical spine.

## 6) `extends_branch`

- Allowed layer endpoints: `L_accepted -> L_accepted`.
- Meaning: accepted-history extension into a non-canonical branch retained beside the canonical lineage.
- History-structure definition (not display-only):
  - `extends_branch` records accepted alternatives that do not rewrite or continue the canonical `extends_main` spine.
  - Branch targets are non-canonical with respect to the current main lineage.
  - This is therefore a structural distinction in accepted history, not merely a visualization label.
- Prohibited uses:
  - Must not connect non-accepted layers.
  - Must not target nodes that are part of the canonical `extends_main` path.

## 7) `observes_kernel_change`

- Allowed layer endpoints: `L_gitlog -> L_accepted`.
- Meaning: a gitlog observation node observes an accepted object as changed/realized in repository history.
- Prohibited uses:
  - Must not be interpreted as acceptance itself.
  - Must not originate from raw/candidate/accepted layers.
  - Must not target non-accepted layers.

## `extends_main` vs `extends_branch` (concise contrast)

- `extends_main`: membership in the canonical accepted lineage.
- `extends_branch`: accepted but non-canonical lineage retained as a branch.
- The difference is a property of accepted-history structure and canonicality, not only rendering style.

## Current R001 boundary (explicit non-claims)

At this stage, R001 does **not** yet claim:
- convergence semantics,
- GIF-DIF semantics,
- sigma semantics.

Those are outside the currently asserted kernel meaning and are deferred to future stages.
