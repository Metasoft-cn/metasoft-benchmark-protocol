# Metasoft Benchmark Protocol (MBP)

**A reusable engineering protocol for building reproducible, anti-gaming benchmarks across domains.**

MBP defines the shared rules that every Metasoft benchmark follows: how datasets are versioned and frozen, how results are reported, how failure cases are exposed before aggregate scores, how hidden evaluation sets is protected, and how benchmark gaming is discouraged. It is not a large SDK; v0.1 is a draft specification plus JSON schemas and two reference modes.

## Status

- **Version:** 0.1.0-draft (protocol spec); benchmark-core 0.1.0.dev1 (runtime)
- **State:** Phase 1-2 complete. benchmark-core prototype + AIB v0.2-preview.1 methodology frozen.
- **Not:** an industry standard. A working protocol used by Metasoft benchmarks.

## Mission

> Turn "how to measure" itself into a reliable software-engineering asset.

The goal is not many leaderboards. It is one mature public benchmark, one reusable protocol, a second-domain validation, and clear designs for the rest.

## Core principles

```
Reproducible where possible.
Hidden where necessary.
Metrics before rankings.
Failure cases before aggregate scores.
Freeze before comparison.
No benchmark tuning for a specific engine.
```

In Chinese:

```
能公开复现的，尽量公开复现。
必须防刷榜的，使用隐藏评测。
先定义指标，再比较系统。
优先暴露失败模式，而不是只给一个总分。
比较前必须冻结评测。
禁止为了某个被测系统修改 Benchmark。
```

## Two evaluation modes

| Mode | Dataset | Expected | Baselines | Runner | Use when |
|---|---|---|---|---|---|
| `OPEN_SUITE` | public | public or reproducible | public | public | the task can be fully reproduced by anyone |
| `HIDDEN_SUITE` | protocol public, eval data hidden | hidden | submission black-box | controlled | anti-overfitting, anti-gaming, adversarial |

See [`docs/OPEN_VS_HIDDEN.md`](docs/OPEN_VS_HIDDEN.md).

## What MBP provides

- [`SPEC.md`](SPEC.md) — the normative specification.
- [`schemas/`](schemas/) — JSON Schemas for benchmark manifest, dataset manifest, results, failures, and engine adapters.
- [`examples/open-suite/`](examples/open-suite/) — a minimal open-suite example extracted from CSFB.
- [`examples/hidden-suite/`](examples/hidden-suite/) — a minimal hidden-suite skeleton (protocol + dev set, no holdout data).
- [`docs/`](docs/) — freeze policy, metric policy, anti-gaming, failure corpus, reproducibility, reference implementations.

## Reference implementations

1. **Speech Follow Benchmark (CSFB)** — `OPEN_SUITE`, public, frozen at v0.2.0-preview.1. The first reference implementation MBP was extracted from. <https://github.com/Metasoft-cn/speech-follow-benchmark>
2. **AI Interview Benchmark (AIB)** — `OPEN_SUITE` with `HIDDEN_HOLDOUT`, frozen at v0.2.0-preview.1. 108 cases, 4 core methodology assets (dataset split, perturbation generator, invariance test, hidden holdout). <https://github.com/Metasoft-cn/ai-interview-benchmark>

See [`docs/REFERENCE_IMPLEMENTATIONS.md`](docs/REFERENCE_IMPLEMENTATIONS.md).

## benchmark-core

The unified benchmark runtime. Every Metasoft benchmark plugs into it instead of reimplementing runner/adapter/metric/provenance logic.

```
benchmark-core/
├─ adapter/          # InProcess + Subprocess stdio
├─ metric/           # Metric + MetricRegistry
├─ dataset/          # JSONL loading, splits, SHA256
├─ runner/           # execution engine
├─ report/           # results.schema.json emitter
├─ provenance/       # reproducibility metadata
└─ hidden_evaluator/ # HIDDEN_SUITE boundary (stub)
```

See [`benchmark-core/README.md`](benchmark-core/README.md) and [`docs/EVALUATION_ENGINE_DESIGN.md`](docs/EVALUATION_ENGINE_DESIGN.md).

## Repository layout

```
metasoft-benchmark-protocol/
├─ README.md
├─ SPEC.md
├─ VERSIONING.md
├─ REPRODUCIBILITY.md
├─ SECURITY.md
├─ CONTRIBUTING.md
├─ CHANGELOG.md
├─ LICENSE
├─ schemas/
│  ├─ benchmark.schema.json
│  ├─ dataset-manifest.schema.json
│  ├─ results.schema.json
│  ├─ failure.schema.json
│  └─ engine-adapter.schema.json
├─ benchmark-core/          # unified runtime (Phase 1)
│  ├─ benchmark_core/
│  ├─ examples/             # AIB integration + CSFB retrofit
│  └─ tests/
├─ examples/
│  ├─ open-suite/
│  └─ hidden-suite/
└─ docs/
   ├─ OPEN_VS_HIDDEN.md
   ├─ FREEZE_POLICY.md
   ├─ METRIC_POLICY.md
   ├─ ANTI_GAMING.md
   ├─ FAILURE_CORPUS.md
   ├─ REFERENCE_IMPLEMENTATIONS.md
   ├─ SEPARATION_POLICY.md
   └─ EVALUATION_ENGINE_DESIGN.md
```

## Usage

A benchmark adopting MBP:

1. Fills a `benchmark.schema.json`-valid manifest declaring id, version, mode, domain.
2. Fills a `dataset-manifest.schema.json`-valid dataset manifest with version, case/event counts, SHA256, seed.
3. Emits `results.schema.json`-valid results with category breakdown and a failure corpus.
4. Follows [`docs/FREEZE_POLICY.md`](docs/FREEZE_POLICY.md) (DRAFT → PREVIEW → FROZEN → DEPRECATED).
5. Follows [`docs/ANTI_GAMING.md`](docs/ANTI_GAMING.md) if `HIDDEN_SUITE`.

## License

[Apache-2.0](LICENSE). Schemas and specification text are Apache-2.0; benchmarks adopting MBP keep their own licenses.

## Public messaging

Metasoft develops open, reproducible benchmarks and evaluation protocols for practical software systems. 元软正在构建面向实际软件系统的开放、可复现 Benchmark 与评测协议。
