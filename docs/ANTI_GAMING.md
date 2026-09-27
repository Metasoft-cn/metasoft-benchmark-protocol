# Anti-Gaming Policy

Anti-gaming is engineering, not an attack on participants. The tone is neutral. The goal is to keep the benchmark measuring the thing it claims to measure.

## Required controls for HIDDEN_SUITE

A `HIDDEN_SUITE` benchmark MUST define:

- **Public dev set** — a reproducible subset for participant development.
- **Hidden holdout** — the evaluation set, not downloadable.
- **No case-id hardcoding** — submissions must not special-case known case ids; canary cases detect this.
- **Benchmark-specific tuning disclosure** — if a submission is tuned to the benchmark, that is disclosed, not hidden.
- **Submission rate limits** — to prevent probing of the hidden set.
- **Randomized hidden regimes** — the composition of the hidden set is not fixed forever; regimes are sampled.
- **Temporal holdouts** — evaluation periods the participant has not seen.
- **Canary cases** — synthetic cases that a hardcoded or overfit submission gets wrong.

## Boundary

- The hidden evaluation set is not downloadable.
- Evaluation runs are ephemeral and controlled by the operator.
- Submissions are identified by hash; raw holdout data is never returned.
- Per-case hidden output is not returned; only aggregate failure categories are reported.

This prevents a participant from recovering the hidden set by submitting and observing per-case results.

## For OPEN_SUITE

`OPEN_SUITE` benchmarks accept that participants can see all cases. Mitigations:

- Publish a large, diverse, deterministic dataset (memorization is expensive and visible).
- Require baselines to be simple reference algorithms, not tuned competitors.
- Refresh the dataset on a versioned cadence with a new seed and a new hash.
- Reserve a `HIDDEN_HOLDOUT` for future use if evaluator tuning becomes a risk.

## What anti-gaming is not

- Not a leaderboard arms race.
- Not public shaming of submissions.
- Not a reason to make the protocol secret. The protocol and metric definitions stay public; only the hidden evaluation data is protected.

## Canary case example

A canary case is a synthetic case constructed so that a correct general system passes it, but a system that hardcoded answers to public case ids fails it. Canary cases are injected into the hidden set and not disclosed individually; a submission that fails canaries is flagged as likely overfit.
