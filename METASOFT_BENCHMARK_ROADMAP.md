# Metasoft Benchmark Roadmap

This roadmap records what is done and what is next. New test ideas go here, not into frozen benchmarks. The work runs on two tracks: a **public** track (open benchmarks under MBP) and a **private** track (product R&D that is not published until a deliberate release).

## Done (v0.1 foundation)

- CSFB published as first reference implementation (PREVIEW, v0.2.0-preview.1, CI green, clean clone PASS).
- MBP v0.1.0-draft extracted from CSFB: spec, 5 schemas, open/hidden suites, freeze/metric/anti-gaming/failure policies.
- Benchmark Asset Inventory produced (5 domains, maturity matrix).
- AI Interview Benchmark MVP built (24 cases, 6 metrics, 3 baselines, CI green) — MBP validated in a second domain.
- AI Website / SEO / GEO / Quant design skeletons written.
- Separation policy enforced: public vs private tracks, moat-component list, `PUBLIC_PUSH_REQUIRES_HUMAN_CONFIRMATION`.
- Evaluation engine design skeleton written.

## Phase ordering (refined)

Two tracks run concurrently, but within each track the phase order is fixed:

```
Public track:
  Phase 1  benchmark-core prototype          ← NOW
  Phase 2  AIB v0.2 preview freeze
  Phase 4  AI Website Benchmark
  Phase 5  Quant Hidden Suite

Private track:
  Phase 3  Adaptive Speaking Engine           ← after Phase 2
```

Phase 3 sits between Phase 2 and Phase 4 because the Adaptive Speaking Engine has the highest commercial value and reuses benchmark-core + AIB's evaluator metrics internally.

---

## Phase 1 — benchmark-core prototype (NOW)

Build the shared runtime inside the MBP repo (`benchmark-core/`). Every future benchmark depends on it instead of reimplementing runner/adapter/metric/provenance logic.

- Implement `benchmark-core/` subpackage: `schema/` re-export, `runner/`, `adapter/` loader + subprocess transport, `metric_engine/` registry, `report/` emitter, `provenance/`.
- Define adapter registry: `SpeechAdapter`, `EvaluatorAdapter`, `StrategyAdapter`, `SiteAnalyzerAdapter`.
- Integrate AIB first (smallest domain) as the first consumer.
- Retrofit CSFB to adopt `benchmark-core`.
- See [`docs/EVALUATION_ENGINE_DESIGN.md`](docs/EVALUATION_ENGINE_DESIGN.md).

## Phase 2 — AIB v0.2 preview freeze

- Expand AIB to 100–300 curated cases.
- Add programmatic perturbation generation (paraphrase, verbosity, ASR-noise) with `curated` / `template-derived` / `synthetic` labels.
- Add invariance tests as first-class benchmark cases.
- Reserve a `HIDDEN_HOLDOUT`.
- Freeze AIB at `PREVIEW` with a dataset hash and tag.
- AIB now runs on `benchmark-core`.

## Phase 3 — Adaptive Speaking Engine (PRIVATE, not public)

- Build the �词器 Adaptive Speaking Engine: Personal Speech Rate Model, Time Budget Engine, Topic Contract, Dynamic Prompt, Improvisation, Rejoin.
- Reuses `benchmark-core` + AIB evaluator metrics internally for self-evaluation.
- All moat components stay private. No public repo. No public benchmark of internal models.
- See `docs/SEPARATION_POLICY.md` and the private design doc.

## Phase 4 — AI Website Benchmark prototype

- Define the old-site corpus + business-fact ground truth.
- Prototype the hallucination detector (`unsupported_business_claim`).
- Implement the SEO track checks (see [`docs/case-studies/seo-track.md`](docs/case-studies/seo-track.md)).
- Implement the GEO track with a fixed extractor and question set (see [`docs/case-studies/geo-track.md`](docs/case-studies/geo-track.md)).
- Single repo (`ai-website-benchmark`) with `core/seo/geo`, adopting `benchmark-core`.
- Tied to CMS SaaS deployment workflow.

## Phase 5 — Quant Black-box Benchmark design freeze

- Freeze the hidden-evaluator protocol, adapter contract, and metric definitions.
- Build the public dev set and sample scenarios.
- Do NOT run a public leaderboard.
- Coordinate with R2 governance; do not disturb the scheduler/soak/release pipeline.
- Adopts `benchmark-core` `hidden_evaluator/` boundary.

## v1.0 — First frozen releases

- CSFB `FROZEN` at v1.0 (frozen spec, schemas, metrics, dataset).
- MBP `FROZEN` at v1.0.
- AIB `FROZEN` after preview validation.

---

## Private track summary (not public until deliberately released)

```
Phase 3  Adaptive Speaking Engine
        ↓
internal NextGen Benchmark   (uses MBP internally; not published)
        ↓
MTRS                         (internal product)
        ↓
selectively re-publish when ready
```

Moat components (Personal Speech Rate Model, Time Budget Engine, Topic Contract, Dynamic Prompt, Improvisation, Rejoin) are evaluated internally only. See [`docs/SEPARATION_POLICY.md`](docs/SEPARATION_POLICY.md). A public benchmark for an overlapping capability, if ever desired, must measure the interface (input→output), not the internal model, and requires a deliberate release decision + human push confirmation.

## Principles (carried forward)

- Reproducible where possible, hidden where necessary.
- Metrics before rankings; failure cases before aggregate scores.
- Freeze before comparison; no benchmark tuning for a specific engine.
- Public benchmarks and private product R&D stay separated; moat components are not public test standards.
- An agent does not autonomously publish moat components, NextGen, MTRS, or hidden suites.
