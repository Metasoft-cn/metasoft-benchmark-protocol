# Metasoft Benchmark Asset Inventory

**Date:** 2026-09-27
**Scope:** read-only inventory of existing assets across Metasoft project areas, to plan benchmark adoption of MBP v0.1.0-draft. No product code was modified.

## Maturity scale

| Grade | Meaning |
|---|---|
| A | ready as a reference benchmark |
| B | substantial reusable assets (code + tests) but not a complete benchmark |
| C | design or partial assets exist; benchmark incomplete |
| D | concept only |

## Maturity matrix

| Domain | Dataset | Runner | Metrics | Baselines | CI | Hidden set | Maturity |
|---|---|---|---|---|---|---|---|
| Speech Follow | YES | YES | YES | YES | YES | YES (holdout/) | **A** |
| AI Interview | partial (structured questions) | NO (product-embedded) | partial (prompt-defined) | NO | NO (product tests only) | NO | **C** |
| AI Website / CMS | NO | NO | NO | NO | NO | NO | **C** (audit report only) |
| SEO / GEO | partial | YES (cli.py) | partial | NO | NO | NO | **C** |
| Quant / ASENT | partial | YES (harness) | partial | partial | YES (quant-system-gitcode) | NO | **B** |

---

## 1. Speech Follow — Maturity A

**Location:** `D:\03_Others\Desktop\chinese-speech-follow-benchmark`
**Public:** <https://github.com/Metasoft-cn/speech-follow-benchmark> (tag `v0.2.0-preview.1`)

| Asset | Present | Location |
|---|---|---|
| Dataset | YES | `datasets/` (golden/synthetic/adversarial/holdout), MANIFEST.json, 6,629 cases / 48,851 events, SHA256 `242a5937…95fcdf` |
| Evaluator / runner | YES | `csfb/` package, CLI `csfb validate\|run\|replay\|generate\|report` |
| Metrics | YES | `metrics/`, multi-dimensional (final accuracy, within-1, catastrophic-absolute, wrong-backward, false-jump-commit) |
| Baselines | YES | `baselines/` (global-exact, global-fuzzy, local-fuzzy) |
| Failure corpus | YES | `reports/failures.jsonl` (reproducible via `csfb run --full`) |
| Deterministic tests | YES | `tests/` (26 tests), deterministic generation with seed `20260923` |
| CI | YES | `.github/workflows/test.yml` — Ubuntu/Windows × Python 3.11/3.12, all green |
| Adapter boundary | YES | `docs/ENGINE_PROTOCOL.md`, `examples/echo_engine.py`, subprocess JSONL |
| Hidden / public split | YES | `datasets/holdout/` exists; current release is OPEN_SUITE |
| Provenance | YES | `docs/GOLDEN_REVIEW.md` (210 curated records, row-by-row review) |
| Licensing | YES | Apache-2.0 (code), CC0 (dataset) |

This is the first MBP reference implementation.

---

## 2. AI Interview — Maturity C

**Location:** `D:\03_Others\Desktop\washine\washine-personal-ai` (product-embedded, not a standalone benchmark)

| Asset | Present | Location |
|---|---|---|
| Dataset | partial | `knowledge/questions/structured_interview.json` (question bank, not an evaluation dataset) |
| Evaluator | partial (prompt) | `ai_engine/prompts/evaluator.v2.yaml`, `ai_engine/prompts/evaluator.yaml` — prompt-based scoring, not standalone code |
| Runner | NO | scoring runs inside the product interview flow |
| Metrics | partial (prompt-defined) | ranking consistency, MAE, stability, level bias, evidence grounding are referenced in the evaluator prompt; no standalone metric code found |
| Baselines | NO | |
| Failure corpus | NO | |
| Deterministic tests | partial | `app_flutter/test/interview_controller_test.dart` (controller tests, not metric invariance tests) |
| CI | NO (product build only) | |
| Adapter boundary | partial | `contracts/v1/interview_session.schema.json`, `contracts/v1/examples/interview_session.example.json` |
| Hidden / public split | NO | |
| Provenance | NO | |
| Licensing | unknown (product repo) | |

**Real code vs design:** the interview controller and schema are real code; the evaluator is a prompt, not a reproducible metric implementation. The metrics named in the prompt (ranking consistency, MAE, stability sigma, level bias, evidence grounding) are the intended AI Interview Benchmark metrics but are not yet implemented as standalone, testable code.

**Gap to benchmark:** needs a standalone evaluator package, a curated/perturbation dataset (100–300 cases), invariance tests (paraphrase, verbosity, ASR-noise), baselines, and CI. This is Phase D.

---

## 3. AI Website / CMS — Maturity C

**Locations:**
- `D:\03_Others\Desktop\江枫官网V2_第一轮审计报告.md` — audit report (design/audit, not code)
- `D:\03_Others\Desktop\提词器\ai_teleprompter\benchmark\` — exists inside the teleprompter product (not inspected in detail; may contain product-specific benchmarks)

| Asset | Present | Location |
|---|---|---|
| Dataset | NO | no old-site corpus or business-fact ground truth found |
| Evaluator | NO | |
| Runner | NO | |
| Metrics | NO | |
| Baselines | NO | |
| Failure corpus | NO | |
| Deterministic tests | NO | |
| CI | NO | |
| Adapter boundary | NO | |
| Hidden / public split | NO | |
| Provenance | NO | |
| Licensing | NO | |

**Real code vs design:** only an audit report exists. The website-renovation benchmark is design-only. This is Phase E.

---

## 4. SEO / GEO — Maturity C

**Location:** `D:\03_Others\Desktop\AI评估GEO项目`

| Asset | Present | Location |
|---|---|---|
| Dataset | partial | `data/` exists (not inspected for benchmark-shaped ground truth) |
| Evaluator / runner | YES | `cli.py`, `geoengine/`, `run_server.py` — real code |
| Metrics | partial | `reports/`, `test_results.xml` — metrics exist but not benchmark-shaped (no frozen metric definitions found) |
| Baselines | NO | |
| Failure corpus | NO | |
| Deterministic tests | partial | `tests/`, `test_results.xml` |
| CI | NO | no `.github/workflows` |
| Adapter boundary | NO | |
| Hidden / public split | NO | |
| Provenance | NO | |
| Licensing | NO (no LICENSE found) | |

**Real code vs design:** `geoengine/` and `cli.py` are real code. This is a GEO evaluation tool, not a benchmark. It can seed the GEO track of the AI Website Benchmark but is not itself a benchmark. This is Phase E.

---

## 5. Quant / ASENT — Maturity B

**Locations:**
- `D:\03_Others\Desktop\量化研究\ASENT_PUBLIC_STRATEGY_BENCHMARK` — strategy benchmark harness
- `D:\03_Others\Desktop\quant-system-gitcode` — main quant system (asent_core, tests, CI)
- `D:\03_Others\Desktop\ASENT_EVENT_ALPHA_RESEARCH_MODULE` — event-alpha research module
- `D:\03_Others\Desktop\量化研究\asent_core\interfaces\evaluator.py` — evaluator interface

| Asset | Present | Location |
|---|---|---|
| Dataset | partial | `ASENT_PUBLIC_STRATEGY_BENCHMARK/data/`, `raw_sources/`, `normalized_strategies/` — strategy data exists; not a frozen benchmark dataset |
| Evaluator / runner | YES | `ASENT_PUBLIC_STRATEGY_BENCHMARK/run_first_benchmark.py`, `harness/`, `strict_backtest/` |
| Metrics | partial | `evidence/`, `robustness/`, `reports/` — risk/robustness metrics exist; not frozen metric definitions |
| Baselines | partial | `generate_corrected_baseline.py`, `normalized_strategies/` — corrected baselines exist |
| Failure corpus | NO | |
| Deterministic tests | partial | `ASENT_PUBLIC_STRATEGY_BENCHMARK/tests/`, `quant-system-gitcode/tests/`, `pytest.ini`, `conftest.py` |
| CI | YES | `quant-system-gitcode/.github/` |
| Adapter boundary | partial | `asent_core/interfaces/evaluator.py` (interface exists) |
| Hidden / public split | NO | |
| Provenance | partial | `CANONICAL_STATE.json`, `WORKTREE_PROVENANCE_MATRIX.json` |
| Licensing | YES | `quant-system-gitcode/LICENSE` |

**Real code vs design:** substantial real code (harness, backtester, tests, CI). However, R2 is in a governance/dependency-closure phase; the existing harness is a research harness, not a frozen black-box benchmark with hidden holdout. This is Phase F (design only; do not run a public leaderboard).

**Note:** per the foundation spec, do not disturb R2 scheduler / soak / release governance. This inventory is read-only.

---

## Summary

- **A:** Speech Follow (CSFB) — public reference implementation, frozen at v0.2.0-preview.1.
- **B:** Quant / ASENT — substantial reusable harness, tests, and CI; not a frozen benchmark; R2 governance in progress.
- **C:** AI Interview, AI Website, SEO/GEO — assets or design exist but no standalone, frozen, CI-gated benchmark.
- **D:** none in this inventory.

## Recommended next step

AI Interview is the highest-leverage next benchmark: the evaluator metrics are already named (ranking consistency, MAE, stability sigma, level bias, evidence grounding) and the product has a session schema and test scaffold. Building a standalone AI Interview Benchmark MVP (Phase D) reuses these names and validates MBP in a second domain.
