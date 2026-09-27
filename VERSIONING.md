# Versioning

**MBP version:** 0.1.0-draft

## Protocol version

MBP itself follows semantic versioning:

- `0.x` — draft; breaking changes allowed with a minor bump and a changelog entry.
- `1.0` — first frozen protocol; breaking changes require a major bump.
- A benchmark's `protocol_version` field declares which MBP version it conforms to.

## Per-artifact versioning

A benchmark carries independent versions for each artifact that can change independently:

| Artifact | Field | When it changes |
|---|---|---|
| Benchmark spec | `benchmark.version` | the benchmark's own behavior changes |
| Dataset | `dataset.version` | cases added/removed/relabeled |
| Generator | `dataset.generator_version` (in dataset manifest) | generation algorithm changes |
| Runner | `runner.version` | runner behavior changes |
| Metrics | `metrics.version` | metric definitions change |
| Baselines | `baselines[].version` | a baseline algorithm changes |

Changing the dataset version MUST produce a new dataset hash. Changing the generator version MUST be recorded in the dataset manifest and the changelog, and the dataset regenerated to confirm the hash.

## Freeze interaction

Once a benchmark version is `FROZEN`:

- Dataset, expected, metrics, thresholds, and baselines MUST NOT change without a version bump.
- An objective bug fix requires: version bump + changelog + rerun all baselines + new manifest/hash.
- Silent modification is prohibited. See [`docs/FREEZE_POLICY.md`](docs/FREEZE_POLICY.md).

## Changelog

Every version bump MUST have a `CHANGELOG.md` entry describing what changed and why, and whether baselines were rerun.
