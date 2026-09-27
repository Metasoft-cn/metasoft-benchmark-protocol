# Metasoft Benchmark Portfolio

**Date:** 2026-09-27

The Metasoft benchmark portfolio on two tracks: **public** (open, MBP-conformant) and **private** (product R&D, not published until deliberate release). See [`docs/SEPARATION_POLICY.md`](docs/SEPARATION_POLICY.md).

## Public track

### 1. Speech Follow Benchmark (CSFB)

- **Repository:** <https://github.com/Metasoft-cn/speech-follow-benchmark>
- **Status:** Public Reference — `PREVIEW`, tag `v0.2.0-preview.1`
- **Mode:** `OPEN_SUITE`
- **Maturity:** A
- **Head:** `ff923c5ba705d91b9a4ca53c1f4f39e1cb9b56aa`
- **Dataset:** 6,629 cases / 48,851 events, SHA256 `242a5937…95fcdf`
- **CI:** green (Ubuntu/Windows × Python 3.11/3.12)
- **Role:** first MBP reference implementation.

### 2. AI Interview Benchmark (AIB)

- **Repository:** <https://github.com/Metasoft-cn/ai-interview-benchmark>
- **Status:** Second Reference / Development — `DRAFT`, v0.1.0-draft
- **Mode:** `OPEN_SUITE` (reserved `HIDDEN_HOLDOUT`)
- **Maturity:** C → B (MVP built, CI green, 24 cases)
- **Role:** validates MBP in a second domain (evaluation-system consistency).

### 3. AI Website Benchmark

- **Status:** Design
- **Mode:** `OPEN_SUITE` with possible `HIDDEN_SUITE` for hallucination holdout
- **Maturity:** C
- **Design:** [`docs/case-studies/ai-website.md`](docs/case-studies/ai-website.md)
- **Role:** measures website renovation quality (preservation, coverage, hallucination, SEO, GEO).

### 4. SEO / GEO Track

- **Status:** Website sub-track design
- **Maturity:** C
- **Design:** [`docs/case-studies/seo-track.md`](docs/case-studies/seo-track.md), [`docs/case-studies/geo-track.md`](docs/case-studies/geo-track.md)
- **Role:** technical SEO checks and generative-engine extraction fidelity.

### 5. Quant Strategy Benchmark

- **Status:** Hidden-suite design
- **Mode:** `HIDDEN_SUITE`
- **Maturity:** B (substantial assets exist; design done; no public leaderboard)
- **Design:** [`docs/case-studies/quant.md`](docs/case-studies/quant.md)
- **Role:** black-box evaluation of quant strategies with research-integrity gates.

## Private track (product R&D, not public)

### 6. Adaptive Speaking Engine

- **Status:** Private R&D
- **Components (moat, do not publish):** Personal Speech Rate Model, Time Budget Engine, Topic Contract, Dynamic Prompt, Improvisation, Rejoin.
- **Evaluation:** internal NextGen benchmark (uses MBP internally; not published).

### 7. MTRS

- **Status:** Private product
- **Release:** selectively re-publish when ready, after human confirmation.

## Shared runtime

### Metasoft Evaluation Engine

- **Status:** Design — [`docs/EVALUATION_ENGINE_DESIGN.md`](docs/EVALUATION_ENGINE_DESIGN.md)
- **Role:** unified `benchmark-core/` runtime so MBP is a real protocol, not a repo collection. Adapter registry: `SpeechAdapter`, `EvaluatorAdapter`, `StrategyAdapter`, `SiteAnalyzerAdapter`. First integration target: AIB (v0.2).

## Naming

- Protocol: **Metasoft Benchmark Protocol (MBP)**.
- Benchmarks keep concrete names: Speech Follow Benchmark, AI Interview Benchmark, AI Website Benchmark, Quant Strategy Benchmark. No forced acronyms.

## Public messaging

Metasoft develops open, reproducible benchmarks and evaluation protocols for practical software systems. 元软正在构建面向实际软件系统的开放、可复现 Benchmark 与评测协议。
