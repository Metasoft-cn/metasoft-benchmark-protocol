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
  Phase 1  benchmark-core prototype          ✅ COMPLETE (c6472a0)
  Phase 2  AIB v0.2 preview freeze           ✅ COMPLETE (9f4df06, tag v0.2.0-preview.1)
  Phase 4  AI Website Benchmark
  Phase 5  Quant Hidden Suite

Private track:
  Phase 3    Adaptive Speaking Engine         ← after Phase 2
  Phase 3.5  MBP Evaluation Cloud             ← after Phase 3
```

Phase 3 sits between Phase 2 and Phase 4 because the Adaptive Speaking Engine has the highest commercial value and reuses benchmark-core + AIB's evaluator metrics internally.

Phase 3.5 (MBP Evaluation Cloud) is a private evaluation platform — not a public leaderboard SaaS, but an internal tool to run hidden holdouts, manage verified scores, and support commercial evaluation services. It depends on Phase 3 (Adaptive Speaking Engine needs internal evaluation) and feeds Phase 4/5 (Website/Quant need the evaluation infrastructure).

---

## Phase 1 — benchmark-core prototype ✅ COMPLETE

Commit `c6472a0`. 38 tests passing. AIB integration + CSFB retrofit verified.

- `benchmark-core/` subpackage: adapter (InProcess + Subprocess), metric (Metric + MetricRegistry), dataset (splits + hash), runner, report (results.schema.json emitter), provenance (SHA256), hidden_evaluator (stub).
- Adapter registry: `SpeechAdapter`, `EvaluatorAdapter`, `StrategyAdapter`, `SiteAnalyzerAdapter`.
- AIB integrated as first consumer (3 baselines, 6 metrics, real dataset 24 cases × 3 repeats).
- CSFB retrofit shows event-driven engine protocol adaptation.
- CI: Ubuntu/Windows × Python 3.11/3.12.

**Constraint: benchmark-core API is now frozen for Phase 2.** The interface just formed; early modification would force all downstream benchmarks to refactor. Phase 2 must not change benchmark-core's public API.

## Phase 2 — AIB v0.2 preview freeze ✅ COMPLETE

Commit `9f4df06`, tag `v0.2.0-preview.1`. 108 total cases (24 curated + 60 generated + 24 invariance). 34 tests passing.

**Four core assets delivered:**

1. **Dataset split**: train(8) / dev(16) / public_test(30) / hidden_test(30, not released).
2. **Perturbation generator**: 60 cases — paraphrase, verbosity, asr_noise. Deterministic (fixed seed, no LLM). Labels: `curated` / `template-derived` / `synthetic`.
3. **Invariance evaluator**: 6 groups, 24 cases. Same capability, different question phrasings → scores should be close. MBP signature feature.
4. **Hidden holdout**: `HOLDOUT_MANIFEST.json` with SHA256. Hidden test cases not released. MBP Public Score vs MBP Verified Score.

Preview report: `reports/AIB_PREVIEW_REPORT.md`. benchmark-core API unchanged.

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
Phase 3    Adaptive Speaking Engine
           ↓
Phase 3.5  MBP Evaluation Cloud (private)
           — internal platform for hidden holdouts, verified scores,
             commercial evaluation services
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
