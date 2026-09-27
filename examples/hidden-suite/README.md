# Hidden-suite example (skeleton)

This is a `HIDDEN_SUITE` skeleton. It illustrates the boundary between public and hidden material. **It contains no holdout data.**

## What is public

- `benchmark-manifest.json` — declares `mode: HIDDEN_SUITE`. Valid against [`../../schemas/benchmark.schema.json`](../../schemas/benchmark.schema.json).
- `adapter.json` — the public adapter contract. Valid against [`../../schemas/engine-adapter.schema.json`](../../schemas/engine-adapter.schema.json).
- `dev-set.jsonl` — a small public development subset for participant iteration.

## What is NOT here

- The hidden evaluation episodes, regimes, and stress selections.
- The final evaluation runner.
- Per-case hidden output.

## Boundary

- Submissions are black-box: a participant provides an adapter that reads market state and emits orders/target positions. Source code is not required.
- The operator runs the adapter against the hidden holdout in an ephemeral job.
- Only aggregate failure categories are returned, not per-case hidden results.
- Submission rate is limited; canary cases detect hardcoded or overfit behavior.

See [`../../docs/ANTI_GAMING.md`](../../docs/ANTI_GAMING.md) for the full anti-gaming policy.

## This is a design skeleton

The quant-strategy benchmark is design-only in this phase. No public leaderboard is run. The manifest uses placeholder zeros for counts/hash because the dataset is not yet built.
