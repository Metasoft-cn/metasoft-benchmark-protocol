# Release Checklist

> Pre-release verification for MBP and its benchmarks.

## MBP protocol release

- [ ] `SPEC.md` version updated
- [ ] `CHANGELOG.md` entry written
- [ ] All schemas validate against their examples
- [ ] `benchmark-core/` tests pass (`pytest`)
- [ ] CI green on Ubuntu + Windows × Python 3.11 + 3.12
- [ ] `README.md` status section accurate
- [ ] `METASOFT_BENCHMARK_ROADMAP.md` phase status accurate
- [ ] No broken links in docs (verify all markdown link references resolve)
- [ ] No secrets or private content in the commit
- [ ] Tag created: `vX.Y.Z`
- [ ] Tag pushed to remote

## Benchmark release (CSFB / AIB / future)

- [ ] `benchmark-manifest.json` version updated
- [ ] Dataset `MANIFEST.json` hash computed and verified
- [ ] All cases validate against their schema
- [ ] `pytest` passes
- [ ] CI green
- [ ] Reproduction script exists and runs (`generate_v02_preview.py` or equivalent)
- [ ] Hidden holdout NOT in git (verify `.gitignore`)
- [ ] `HOLDOUT_MANIFEST.json` SHA256 matches actual hidden file
- [ ] Preview report generated (if PREVIEW release)
- [ ] Tag created: `vX.Y.Z`
- [ ] Tag pushed to remote

## Freeze lifecycle gates

### DRAFT → PREVIEW
- [ ] Dataset has ≥ 50 cases (or justification for smaller)
- [ ] At least 3 metrics defined
- [ ] At least 1 baseline runs
- [ ] Reproduction script exists
- [ ] Dataset hash frozen

### PREVIEW → FROZEN
- [ ] Dataset has been reviewed by ≥ 2 people
- [ ] No changes to dataset for ≥ 2 weeks
- [ ] All known failure modes have cases
- [ ] Hidden holdout exists (for HIDDEN_SUITE)
- [ ] Invariance tests pass on reference implementation
- [ ] Public review period completed

### FROZEN → DEPRECATED
- [ ] Successor benchmark identified
- [ ] Migration guide written
- [ ] Users notified
