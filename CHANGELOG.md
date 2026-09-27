# Changelog

All notable changes to the Metasoft Benchmark Protocol are recorded here.

## Unreleased

### Added
- `benchmark-core/` Phase 1 prototype: unified benchmark runtime (adapter, metric, dataset, runner, report, provenance, hidden_evaluator).
- 38 tests passing: core modules + AIB integration + CSFB retrofit + end-to-end.
- AIB integration example (`benchmark-core/examples/aib_integration.py`): wraps AIB's 3 baselines and 6 metrics, verified against real AIB dataset (24 cases × 3 repeats).
- CSFB retrofit example (`benchmark-core/examples/csfb_retrofit.py`): wraps CSFB's event-driven engine protocol.
- CI workflow for `benchmark-core` (Ubuntu/Windows × Python 3.11/3.12).

### Changed
- Roadmap refined to Phase 1–5 + Phase 3.5 ordering: benchmark-core → AIB v0.2 → Adaptive Speaking Engine (private) → MBP Evaluation Cloud (private) → AI Website → Quant.
- Phase 1 marked COMPLETE (commit c6472a0).
- Phase 2 marked COMPLETE (commit 9f4df06, tag v0.2.0-preview.1).
- Phase 2 expanded with methodology: dataset split (train/dev/public_test/hidden_test), perturbation generator, invariance test, hidden holdout.
- `docs/EVALUATION_ENGINE_DESIGN.md` status updated from DESIGN ONLY to Phase 1 implementation in progress.
- **benchmark-core API frozen for Phase 2** — no breaking changes to public API.

## 0.1.0-draft — 2026-09-27

### Added
- Initial specification (`SPEC.md`) extracted from the CSFB v0.2.0-preview.1 reference implementation.
- JSON Schemas: `benchmark`, `dataset-manifest`, `results`, `failure`, `engine-adapter`.
- Two evaluation modes: `OPEN_SUITE` and `HIDDEN_SUITE`.
- Policies: freeze (`DRAFT`/`PREVIEW`/`FROZEN`/`DEPRECATED`), metric (multi-dimensional, failure-first), anti-gaming, reproducibility, separation of concerns.
- Examples: a minimal `open-suite` extracted from CSFB and a `hidden-suite` skeleton.
- Reference implementation registry: CSFB as the first reference.

### Sources
- Frozen CSFB dataset SHA256 `242a5937…95fcdf`, 6,629 cases / 48,851 events, seed `20260923`, generator `0.2.1`.
- CSFB hosted CI matrix: Ubuntu/Windows × Python 3.11/3.12.
- CSFB clean-clone gate: PASS.
