# Contributing

MBP is a working protocol, not an industry standard. Contributions are welcome as pull requests.

## Before proposing a change

1. Read [`SPEC.md`](SPEC.md) and the relevant [`docs/`](docs/) policy.
2. Read [`docs/BENCHMARK_PHILOSOPHY.md`](docs/BENCHMARK_PHILOSOPHY.md) — understand the principles.
3. Check whether the change is a clarification (no version bump) or a behavior change (version bump + changelog).
4. If the change affects a schema, update the schema and any example that validates against it.
5. If the change affects `benchmark-core/`, verify all 38 tests still pass.

## Change types

- **Clarification:** wording, examples, docs. No version bump.
- **Addition:** new optional field, new policy section, new doc. Minor bump.
- **Breaking:** removed field, changed semantics, changed freeze rules. Major bump (pre-1.0: minor bump + explicit changelog).

## benchmark-core API changes

`benchmark-core/` public API is frozen during Phase 2. If your PR changes the public API of `adapter`, `metric`, `dataset`, `runner`, `report`, or `provenance` modules, it will be rejected until the freeze is lifted. Add new functionality in the benchmark layer, not the core.

## Validation

A PR SHOULD include:

- the updated `CHANGELOG.md` entry,
- validation that all examples still conform to their schemas,
- `pytest` passing in `benchmark-core/`,
- a note if any reference implementation needs to update its `protocol_version`.

## Adding a new benchmark

1. Create a new repo following the AIB structure.
2. Fill `benchmark-manifest.json` (validate against `schemas/benchmark.schema.json`).
3. Adopt `benchmark-core` as a dependency.
4. Register adapter + metrics.
5. Follow the methodology: dataset split, perturbation generator, invariance test, hidden holdout.
6. See [`docs/REPOSITORY_MAP.md`](docs/REPOSITORY_MAP.md) for the portfolio.

## Style

- Engineering tone. No marketing claims ("new industry standard", "best", "leading").
- Specifications are normative; examples are illustrative.
- Chinese summaries are welcome where they aid comprehension, but the normative text is English.
- No emojis in code or docs unless explicitly requested.
