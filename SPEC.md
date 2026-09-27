# Metasoft Benchmark Protocol — Specification

**Version:** 0.1.0-draft
**State:** DRAFT

This is the normative specification. Examples live under [`examples/`](examples/) and schemas under [`schemas/`](schemas/). Where this document and a schema disagree, the schema is authoritative for machine validation and this document is authoritative for intent.

## 1. Scope

MBP defines the engineering rules shared by Metasoft benchmarks. It does not define any single benchmark's domain, dataset, or metrics. Each benchmark is a separate repository that adopts MBP by producing valid manifests and following the policies below.

## 2. Benchmark identity

A benchmark is identified by:

- `id` — stable short identifier (e.g. `csfb`, `ai-interview`).
- `name` — human name.
- `version` — the benchmark's own semantic version.
- `protocol_version` — the MBP version it conforms to (e.g. `0.1.0-draft`).
- `mode` — `OPEN_SUITE` or `HIDDEN_SUITE`.
- `domain` — the problem domain (e.g. `speech-follow`, `interview-evaluation`, `website-renovation`, `quant-strategy`).

## 3. Evaluation modes

### 3.1 OPEN_SUITE

- Dataset is public.
- Expected results are public or reproducible from a deterministic generator.
- Baselines are public.
- Runner is public.
- Metrics are public.

Suitable when the task can be fully reproduced by any third party and benchmark gaming is not a primary risk.

### 3.2 HIDDEN_SUITE

- Protocol is public.
- Metric definitions are public.
- A development subset is public.
- Evaluation data is hidden.
- Evaluation runner is controlled by the benchmark operator.
- Submissions are black-box (an adapter interface; source code is not required).

Suitable for anti-overfitting, anti-gaming, and adversarial evaluation. See [`docs/ANTI_GAMING.md`](docs/ANTI_GAMING.md).

## 4. Benchmark manifest

Every benchmark MUST have a manifest valid against [`schemas/benchmark.schema.json`](schemas/benchmark.schema.json):

```yaml
benchmark:
  id: csfb
  name: Chinese Speech Follow Benchmark
  version: 0.2.0-preview
  protocol_version: 0.1.0-draft
  mode: OPEN_SUITE
  domain: speech-follow

dataset:
  version: 0.2.0-preview
  cases: 6629
  events: 48851
  hash: 242a593739e55a02f305ffce0350425b04d5aad0ef1781d0a4190ab67195fcdf
  seed: 20260923

runner:
  version: 0.2.1

metrics:
  version: 0.2.0

baselines:
  - id: global-exact
    version: 0.2.0
  - id: global-fuzzy
    version: 0.2.0
  - id: local-fuzzy
    version: 0.2.0
```

## 5. Dataset manifest

Every dataset MUST have a manifest valid against [`schemas/dataset-manifest.schema.json`](schemas/dataset-manifest.schema.json). The manifest records:

- `dataset_version`
- `seed` — the deterministic seed, so `generate` reproduces identical bytes.
- `generator_version`
- `case_count`, `event_count`
- per-file `path`, `sha256`, `case_count`, `event_count`, `bytes`
- a top-level `sha256` digest over the manifest content

Dataset generation MUST be deterministic: same version + same seed ⇒ identical bytes ⇒ identical hashes.

## 6. Result schema

Results SHOULD be emitted in a shape valid against [`schemas/results.schema.json`](schemas/results.schema.json):

```json
{
  "benchmark": {},
  "system_under_test": {},
  "dataset": {},
  "metrics": {},
  "category_breakdown": {},
  "failures": {},
  "runtime": {},
  "reproducibility": {}
}
```

## 7. No mandatory single score

A benchmark MUST NOT require a single aggregate score unless the domain has a defensible reason. The default is multi-dimensional metrics. A composite score may be offered as a convenience but MUST NOT be the only reported number.

Rationale: an engine with 98% accuracy and frequent catastrophic jumps can behave worse for a user than one with 96% accuracy and rare wrong movement. One number hides this.

## 8. Failure-first reporting

A benchmark SHOULD emit a failure corpus valid against [`schemas/failure.schema.json`](schemas/failure.schema.json). For each failure:

- `category` — the failure class (e.g. `wrong_backward`, `false_jump_commit`).
- `case_id` — the case that triggered it.
- `expected` — the expected outcome.
- `actual` — the observed outcome.
- `severity` — `catastrophic` / `major` / `minor`.
- `reproduction` — a command or trace that reproduces the failure.

Aggregate accuracy without a failure corpus is insufficient for comparison.

## 9. Freeze policy

Every benchmark version is in one of:

- `DRAFT` — may change freely.
- `PREVIEW` — published for feedback, may change with a version bump.
- `FROZEN` — dataset, expected, metrics, thresholds, and baselines MUST NOT change. An objective bug requires a version bump, a changelog entry, and a re-run of all baselines.
- `DEPRECATED` — superseded; do not use for new comparison.

See [`docs/FREEZE_POLICY.md`](docs/FREEZE_POLICY.md).

## 10. Anti-gaming

`HIDDEN_SUITE` benchmarks MUST follow [`docs/ANTI_GAMING.md`](docs/ANTI_GAMING.md): public dev set, hidden holdout, no case-id hardcoding, benchmark-specific tuning disclosure, submission rate limits, randomized hidden regimes, temporal holdouts, canary cases.

Anti-gaming is engineering, not an attack on participants. The tone is neutral.

## 11. Separation of concerns

A benchmark MUST distinguish:

- Benchmark code
- Dataset
- Baselines
- System under test
- Private product code

A benchmark MUST NOT silently depend on private product code. Baselines are intentionally simple reference algorithms for sanity and comparison, not weak fake competitors.

## 12. Reproducibility

See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) and [`docs/FREEZE_POLICY.md`](docs/FREEZE_POLICY.md). In summary: versioned schema, versioned dataset, versioned metrics, dataset hash, deterministic generation, baselines, failure corpus, category breakdown, reproducible commands, CI, licensing, provenance, changelog, freeze policy.

## 13. Benchmark bugs

If a benchmark bug is found:

```
issue → minimal reproduction → version bump → fix → rerun baselines → new manifest/hash
```

Silent modification is prohibited.
