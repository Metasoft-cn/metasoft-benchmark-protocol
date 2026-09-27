# Reproducibility

Reproducible where possible, hidden where necessary. This document defines the reproducibility requirements for the `OPEN_SUITE` mode and the reproducible subset of `HIDDEN_SUITE`.

## Deterministic generation

Dataset generation MUST be deterministic:

```
same generator_version + same seed ⇒ identical bytes ⇒ identical SHA256
```

The dataset manifest records `seed` and `generator_version`. `generate` with the same inputs MUST reproduce the same files and the same top-level digest.

CSFB evidence: `csfb generate` was run twice; manifest bytes and dataset digest were unchanged across both runs (see CSFB `reports/PRE_RELEASE_AUDIT.md`).

## Dataset hash

The dataset manifest carries:

- a per-file `sha256` for every dataset file,
- a top-level `sha256` digest over the manifest content.

These are the freeze identity. A frozen benchmark's dataset hash MUST NOT change. Comparison across systems is only valid against the same hash.

## Reproducible commands

A benchmark MUST document the exact commands to:

1. Install (including Python version and dependencies).
2. Validate the dataset (`validate`).
3. Run a quick subset (`run --quick`).
4. Run the full benchmark (`run --full`).
5. Replay a single case (`replay --case <id>`).

These commands are the reproducibility contract. They are what CI and clean-clone gates execute.

## CI

A benchmark MUST have hosted CI that runs, at minimum, install + validate + quick run, on the declared platform/Python matrix. CI must be actually run, not only configured.

CSFB evidence: Ubuntu/Windows × Python 3.11/3.12, all four jobs green on the frozen commit.

## Clean-clone gate

Before a preview/frozen tag, a benchmark MUST pass a clean-clone gate:

1. In a fresh directory, `git clone` the public repository.
2. Create a fresh virtualenv.
3. Install using the README instructions.
4. `validate` and `run --quick` pass.
5. Dataset hash matches the manifest.

CSFB evidence: clean clone of `Metasoft-cn/speech-follow-benchmark` at `ff923c5` passed validate (6,629 cases / 48,851 events) and quick run on Python 3.14.

## Determinism replay

For a frozen benchmark, `run --full` MUST produce identical logical output across runs, excluding latency, host, and runtime identity. CSFB evidence: logical prediction SHA256 and logical metrics SHA256 were identical across two full runs and a final full replay.

## Provenance

A benchmark SHOULD record provenance for curated data: who reviewed it, when, and what review status it carries. CSFB evidence: 210 curated records received row-by-row label review by one contributor; no external adjudication is claimed.

## Hidden-suite reproducibility

For `HIDDEN_SUITE`, the public development subset and the protocol are reproducible. The hidden holdout is not published; reproducibility of the hidden evaluation is the operator's responsibility and is verified by the operator's internal CI, not by public clone.
