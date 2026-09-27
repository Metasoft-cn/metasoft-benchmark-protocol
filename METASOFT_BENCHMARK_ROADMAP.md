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

## Public track

```
CSFB v0.2 (PREVIEW)            — done
        ↓
AI Interview Benchmark v0.2    — next
        ↓
AI Website Benchmark            — design done
        ↓
Quant Strategy Benchmark        — design done (HIDDEN_SUITE)
```

### v0.2 — AIB preview freeze + evaluation engine prototype
- Expand AIB to 100–300 curated cases.
- Add programmatic perturbation generation (paraphrase, verbosity, ASR-noise) with `curated` / `template-derived` / `synthetic` labels.
- Add invariance tests as first-class benchmark cases.
- Reserve a `HIDDEN_HOLDOUT`.
- Freeze AIB at `PREVIEW` with a dataset hash and tag.
- Prototype `benchmark-core/` (see [`docs/EVALUATION_ENGINE_DESIGN.md`](docs/EVALUATION_ENGINE_DESIGN.md)); integrate AIB first (smallest domain), then retrofit CSFB.

### v0.3 — AI Website Benchmark prototype
- Define the old-site corpus + business-fact ground truth.
- Prototype the hallucination detector (`unsupported_business_claim`).
- Implement the SEO track checks (see [`docs/case-studies/seo-track.md`](docs/case-studies/seo-track.md)).
- Implement the GEO track with a fixed extractor and question set (see [`docs/case-studies/geo-track.md`](docs/case-studies/geo-track.md)).
- Single repo (`ai-website-benchmark`) with `core/seo/geo`, adopting `benchmark-core`.

### v0.4 — Quant Black-box Benchmark design freeze
- Freeze the hidden-evaluator protocol, adapter contract, and metric definitions.
- Build the public dev set and sample scenarios.
- Do NOT run a public leaderboard.
- Coordinate with R2 governance; do not disturb the scheduler/soak/release pipeline.

### v1.0 — First frozen releases
- CSFB `FROZEN` at v1.0 (frozen spec, schemas, metrics, dataset).
- MBP `FROZEN` at v1.0.
- AIB `FROZEN` after preview validation.

## Private track (not public until deliberately released)

```
Adaptive Speaking Engine
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
