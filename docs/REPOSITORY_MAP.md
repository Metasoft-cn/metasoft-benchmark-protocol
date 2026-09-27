# Repository Map

> 30-second guide for first-time visitors.

## What is this?

Metasoft Benchmark Protocol (MBP) — a reusable engineering protocol for building reproducible, anti-gaming benchmarks across domains. Not a leaderboard. Not a SaaS. A protocol + shared runtime + methodology.

## Structure at a glance

```
metasoft-benchmark-protocol/
│
├── Protocol & Governance
│   ├── SPEC.md                    — normative specification
│   ├── VERSIONING.md              — version rules
│   ├── REPRODUCIBILITY.md         — reproducibility contract
│   ├── SECURITY.md                — security + push governance
│   ├── CONTRIBUTING.md            — contribution guide
│   └── CHANGELOG.md               — change history
│
├── Schemas (JSON)
│   └── schemas/                   — benchmark, dataset, results, failure, adapter
│
├── benchmark-core/                — unified runtime (Phase 1 ✅)
│   ├── benchmark_core/            — adapter, metric, dataset, runner, report, provenance
│   ├── examples/                  — AIB integration + CSFB retrofit
│   └── tests/                     — 38 tests
│
├── Methodology Docs
│   └── docs/
│       ├── OPEN_VS_HIDDEN.md      — two evaluation modes
│       ├── FREEZE_POLICY.md       — DRAFT → PREVIEW → FROZEN → DEPRECATED
│       ├── METRIC_POLICY.md       — multi-dimensional, failure-first
│       ├── ANTI_GAMING.md         — anti-overfitting measures
│       ├── FAILURE_CORPUS.md      — failure case exposure
│       ├── REFERENCE_IMPLEMENTATIONS.md
│       ├── SEPARATION_POLICY.md   — public vs private separation
│       └── EVALUATION_ENGINE_DESIGN.md
│
├── Examples
│   └── examples/
│       ├── open-suite/            — minimal OPEN_SUITE
│       └── hidden-suite/          — minimal HIDDEN_SUITE skeleton
│
├── Articles (technical)
│   └── articles/
│       ├── 01-why-ai-teleprompter-needs-standards.md
│       ├── 02-why-ai-interview-scoring-needs-benchmark.md
│       └── 03-why-ai-agent-era-needs-evaluation-infrastructure.md
│
└── Roadmap & Portfolio
    ├── METASOFT_BENCHMARK_ROADMAP.md
    ├── METASOFT_BENCHMARK_PORTFOLIO.md
    └── METASOFT_BENCHMARK_ASSET_INVENTORY.md
```

## External benchmarks (separate repos)

| Benchmark | Repo | Version | Cases | Mode |
|-----------|------|---------|-------|------|
| CSFB (Speech Follow) | [Metasoft-cn/speech-follow-benchmark](https://github.com/Metasoft-cn/speech-follow-benchmark) | v0.2.0-preview.1 | 6,629 | OPEN_SUITE |
| AIB (AI Interview) | [Metasoft-cn/ai-interview-benchmark](https://github.com/Metasoft-cn/ai-interview-benchmark) | v0.2.0-preview.1 | 108 | OPEN_SUITE + HIDDEN_HOLDOUT |

## Phase status

| Phase | What | Status |
|-------|------|--------|
| 1 | benchmark-core runtime | ✅ COMPLETE |
| 2 | AIB v0.2 methodology | ✅ COMPLETE |
| 3 | Adaptive Speaking Engine (private) | 🔒 Design phase |
| 3.5 | MBP Evaluation Cloud (private) | 🔒 Planned |
| 4 | AI Website Benchmark | Planned |
| 5 | Quant Hidden Suite | Planned |

## Quick start

```bash
cd benchmark-core
pip install -e ".[dev]"
pytest  # 38 tests
```
