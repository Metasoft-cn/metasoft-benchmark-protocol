# Metasoft Evaluation Engine — Design Skeleton

**Status:** Phase 1 implementation in progress. See roadmap.
**Goal:** a unified benchmark runtime so MBP is a real protocol, not a collection of independent repos.

## Why

Today each benchmark (CSFB, AIB, Quant, Website) has its own runner, adapter loader, metric dispatcher, and report format. They conform to MBP's *schemas* but share no *code*. This is acceptable for v0.1 (the protocol is the contract), but as the portfolio grows, duplicated runner/adapter/provenance logic will diverge.

The evaluation engine is the shared runtime that every benchmark plugs into. Benchmarks contribute **domain logic** (dataset, metrics, adapter contract); the engine contributes **plumbing** (load, run, validate, report, provenance, hidden-evaluator boundary).

## benchmark-core/ structure

```
benchmark-core/
├── schema/            # MBP JSON schemas (re-exported from MBP)
├── runner/            # load cases, dispatch adapter, collect predictions
├── adapter/           # adapter loader + subprocess/stdio transport
├── metric_engine/     # register metrics, compute, aggregate, category breakdown
├── report/            # results.schema.json emitter + failure corpus writer
├── provenance/        # dataset hash, generator seed, run identity
├── hidden_evaluator/  # HIDDEN_SUITE boundary: ephemeral job, no holdout download
└── evidence/          # evidence package: per-failure reproduction trace
```

The engine is a library, not a service. A benchmark depends on `benchmark-core` and provides its domain pieces.

## Adapter registry

Every benchmark registers an adapter type. The engine runs any registered adapter through a uniform transport (subprocess stdio / JSONL by default).

| Benchmark | Adapter type | Input | Output |
|---|---|---|---|
| CSFB | `SpeechAdapter` | script segments + recognized-text events | segment position predictions |
| AI Interview | `EvaluatorAdapter` | question + answer | score + feedback + cited_evidence |
| Quant | `StrategyAdapter` | market state (bars, positions, config) | orders / target positions |
| Website | `SiteAnalyzerAdapter` | generated site + source business files | per-check pass/fail + extracted facts |

The engine does not know the domain semantics; it only knows the transport and the metric interface. Domain metrics are registered by the benchmark, not hardcoded in the engine.

## Metric interface

A metric is a registered callable:

```
Metric(
    name: str,
    definition: str,          # human-readable definition + formula
    compute: Callable,        # (predictions, cases) -> value
    unit: str,
    higher_is_better: bool | None,   # None for vector metrics like level_bias
)
```

The engine computes all registered metrics, emits a `results.schema.json`-valid object, and writes the failure corpus. No composite score is imposed by the engine; if a benchmark wants one, it registers it as just another metric.

## Provenance and reproducibility

The engine records, per run:

- benchmark id + version + protocol_version,
- dataset version + hash + seed,
- adapter id + version,
- logical prediction SHA256 + logical metrics SHA256 (excluding latency/host),
- engine version + Python version + OS.

This is the reproducibility contract from [`REPRODUCIBILITY.md`](../REPRODUCIBILITY.md), enforced in code rather than only in docs.

## Hidden-evaluator boundary

For `HIDDEN_SUITE` benchmarks, the engine's `hidden_evaluator/` module:

- loads the hidden holdout from a path the participant cannot read,
- runs the adapter in an ephemeral job,
- returns only aggregate failure categories (never per-case hidden output),
- enforces submission rate limits and canary cases.

The public engine code defines the *boundary*; the hidden data and the final evaluation runner are operator-controlled and not in the public repo.

## Relationship to MBP

- MBP defines the *schemas and policies* (the contract).
- The evaluation engine implements the *runtime* that enforces the contract.
- A benchmark adopts MBP by conforming to the schemas; it adopts the engine by depending on `benchmark-core` and registering its adapter + metrics.

Benchmarks may still run without the engine (CSFB and AIB v0.1 do). The engine is an opt-in shared runtime for v0.2+, to reduce divergence as the portfolio grows.

## Status in the roadmap

Phase 1 (current). The first integration target is AIB (smallest domain), then CSFB retrofits, then Website/Quant adopt on build.
