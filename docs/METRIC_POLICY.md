# Metric Policy

## Metrics before rankings

A benchmark defines metrics before it compares systems. A leaderboard is a consequence of metrics, not the purpose of the benchmark.

## Multi-dimensional by default

A benchmark MUST NOT require a single aggregate score unless the domain has a defensible reason. The default is a set of named, individually meaningful metrics.

A composite score may be offered as a convenience but:

- MUST NOT be the only reported number,
- MUST be documented with its formula,
- MUST NOT be used as the sole basis for comparison in documentation.

Rationale (from CSFB): an engine with 98% accuracy and frequent catastrophic jumps can behave worse for a reader than one with 96% accuracy and rare wrong movement. One number hides this. CSFB reports final accuracy, within-1 accuracy, catastrophic-absolute rate, wrong-backward rate, and false-jump-commit rate, and does not create a single composite score.

## Failure-first

Aggregate accuracy without a failure corpus is insufficient. A benchmark SHOULD emit, for each failure:

- `category` — the failure class,
- `case_id` — the triggering case,
- `expected` and `actual`,
- `severity` — catastrophic / major / minor,
- `reproduction` — a command or trace.

See [`FAILURE_CORPUS.md`](FAILURE_CORPUS.md) and [`schemas/failure.schema.json`](../schemas/failure.schema.json).

## Category breakdown

Metrics SHOULD be reported with a category breakdown (e.g. by language, difficulty, case type) so that a good aggregate is not hiding a bad stratum. CSFB reports language strata (zh / en / mixed) and navigation strata (intentional skips, forgotten-then-skip, accidental future phrases, forgotten-word pauses).

## Adding a new metric

A new metric requires:

1. A definition and formula.
2. The reason it matters.
3. Unit tests.
4. A version bump of `metrics.version`.
5. A rerun of baselines against the new metric.

## Stability and invariance

Where the domain admits invariance properties (e.g. paraphrase invariance, verbosity invariance), a metric SHOULD be accompanied by invariance tests. A metric that changes under a meaning-preserving perturbation is itself a finding.
