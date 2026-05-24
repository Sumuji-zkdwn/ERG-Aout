# ADR-0001: Use Git as External ERG Log

## Status

Accepted as initial working rule.

## Context

Natural-language chat history makes convergence hard to observe.
Git provides file diffs, commits, branches, and decision records.

## Decision

Use GitHub repository artifacts as external ERG nodes:

- README as stable summary.
- FORMALIZATION as current mathematical model.
- CONVERGENCE as convergence tracker.
- logs as dialogue traces.
- decisions as accepted changes.

## Consequences

The model can be inspected through diffs rather than memory alone.
Unstable ideas must remain outside README until accepted.

