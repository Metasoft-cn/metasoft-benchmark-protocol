# Reference Implementations

MBP is validated by reference implementations that adopt it. Each reference proves the protocol works in a real domain and surfaces gaps in the draft.

## 1. Chinese Speech Follow Benchmark (CSFB)

- **Repository:** <https://github.com/Metasoft-cn/speech-follow-benchmark>
- **Mode:** `OPEN_SUITE`
- **Status:** `PREVIEW`, tag `v0.2.0-preview.1`
- **Head:** `ff923c5ba705d91b9a4ca53c1f4f39e1cb9b56aa`
- **Dataset:** version `0.2.0-preview`, 6,629 cases / 48,851 events, SHA256 `242a593739e55a02f305ffce0350425b04d5aad0ef1781d0a4190ab67195fcdf`, seed `20260923`, generator `0.2.1`.
- **Protocol version:** `0.1.0-draft` (declared retrospectively; CSFB predates MBP and was the source MBP was extracted from).
- **CI:** Ubuntu/Windows × Python 3.11/3.12, all green.
- **Clean clone:** PASS.
- **Baselines:** Global Exact 90.68%, Global Fuzzy 88.96%, Local Fuzzy 90.33% final accuracy, plus within-1, catastrophic-absolute, wrong-backward, and false-jump-commit rates. No composite score.
- **Role:** the first reference implementation. MBP's schemas, freeze policy, failure-first reporting, and reproducibility requirements were abstracted from CSFB's `MANIFEST.json`, `PRE_RELEASE_AUDIT.md`, and CI/clean-clone gates.

## 2. AI Interview Benchmark

- **Repository:** in development (`ai-interview-benchmark`).
- **Mode:** `OPEN_SUITE` with a reserved `HIDDEN_HOLDOUT`.
- **Status:** `DRAFT`.
- **Role:** the second reference implementation, validating MBP in a different domain (evaluation-system consistency rather than alignment tracking). Reuses existing evaluator metrics: ranking consistency, MAE, stability sigma, level bias, evidence grounding.

## Adding a reference implementation

A benchmark becomes a reference implementation when:

1. It has a valid `benchmark.schema.json` manifest declaring its `protocol_version`.
2. It has a valid `dataset-manifest.schema.json` with a deterministic, hashed dataset.
3. It emits `results.schema.json`-valid results with a failure corpus.
4. It has hosted CI that is actually green on the declared matrix.
5. It passes a clean-clone gate.
6. It carries a preview or frozen tag.

List it here with its repository, mode, status, head, dataset identity, and CI status.
