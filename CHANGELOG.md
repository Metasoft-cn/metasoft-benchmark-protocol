# Changelog

All notable changes to the Metasoft Benchmark Protocol are recorded here.

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
