# Freeze Policy

A benchmark version is always in one of four states.

## States

```
DRAFT → PREVIEW → FROZEN → DEPRECATED
```

### DRAFT
- May change freely.
- Not published for comparison.
- No reproducibility guarantee.

### PREVIEW
- Published for feedback.
- May change with a version bump and a changelog entry.
- Reproducibility is expected but not contractually guaranteed.

### FROZEN
- Dataset, expected results, metrics, thresholds, and baselines MUST NOT change.
- An objective bug requires: version bump + changelog + rerun all baselines + new manifest/hash.
- Silent modification is prohibited.
- Comparison across systems is only valid against the same frozen hash.

### DEPRECATED
- Superseded by a newer version.
- Do not use for new comparison.
- Kept for reproducibility of historical results.

## What "freeze" protects

Once `FROZEN`, the following are immutable for that version:

- dataset bytes and hash,
- expected results,
- metric definitions,
- metric thresholds,
- baseline algorithms and their versions.

## What freeze does not protect

- Documentation wording (clarifications allowed without a bump).
- CI runner image updates (allowed; if they break the benchmark, that is a bug to fix with a version bump).
- Runtime performance numbers (latency is not part of the freeze identity; logical output is).

## Bug fix procedure for a frozen benchmark

```
1. Open an issue with a minimal reproduction.
2. Version bump (dataset or benchmark version).
3. Fix.
4. Rerun all baselines.
5. Emit new manifest and dataset hash.
6. Changelog entry describing what changed and why.
7. Re-validate CI and clean-clone gates.
```

## CSFB reference

CSFB v0.2.0-preview is in `PREVIEW`. The dataset SHA256 `242a5937…95fcdf` is the freeze identity. The preview tag `v0.2.0-preview.1` marks the first public reference point. v1.0 will be the first `FROZEN` release.
