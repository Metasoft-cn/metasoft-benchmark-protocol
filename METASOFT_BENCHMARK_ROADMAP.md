# Metasoft Benchmark Roadmap

This roadmap records what is done and what is next. New test ideas go here, not into frozen benchmarks.

## Done (v0.1 foundation)

- CSFB published as first reference implementation (PREVIEW, v0.2.0-preview.1, CI green, clean clone PASS).
- MBP v0.1.0-draft extracted from CSFB: spec, 5 schemas, open/hidden suites, freeze/metric/anti-gaming/failure policies.
- Benchmark Asset Inventory produced (5 domains, maturity matrix).
- AI Interview Benchmark MVP built (24 cases, 6 metrics, 3 baselines, CI green) — MBP validated in a second domain.
- AI Website / SEO / GEO / Quant design skeletons written.

## Next

### v0.2 — AIB preview freeze
- Expand AIB to 100–300 curated cases.
- Add programmatic perturbation generation (paraphrase, verbosity, ASR-noise) with `curated` / `template-derived` / `synthetic` labels.
- Add invariance tests as first-class benchmark cases.
- Reserve a `HIDDEN_HOLDOUT`.
- Freeze AIB at `PREVIEW` with a dataset hash and tag.

### v0.3 — AI Website Benchmark prototype
- Define the old-site corpus + business-fact ground truth.
- Prototype the hallucination detector (`unsupported_business_claim`).
- Implement the SEO track checks (see [`docs/case-studies/seo-track.md`](docs/case-studies/seo-track.md)).
- Implement the GEO track with a fixed extractor and question set (see [`docs/case-studies/geo-track.md`](docs/case-studies/geo-track.md)).
- Single repo (`ai-website-benchmark`) with `core/seo/geo`.

### v0.4 — Quant Black-box Benchmark design freeze
- Freeze the hidden-evaluator protocol, adapter contract, and metric definitions.
- Build the public dev set and sample scenarios.
- Do NOT run a public leaderboard.
- Coordinate with R2 governance; do not disturb the scheduler/soak/release pipeline.

### v1.0 — First frozen releases
- CSFB `FROZEN` at v1.0 (frozen spec, schemas, metrics, dataset).
- MBP `FROZEN` at v1.0.
- AIB `FROZEN` after preview validation.

## Principles (carried forward)

- Reproducible where possible, hidden where necessary.
- Metrics before rankings; failure cases before aggregate scores.
- Freeze before comparison; no benchmark tuning for a specific engine.
- One mature benchmark + one reusable protocol + one second-domain validation + clear designs for the rest.
