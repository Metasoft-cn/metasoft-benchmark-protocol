# Benchmark Philosophy

> Why benchmark first. Why evaluation infrastructure precedes product capability.

## The problem

AI systems fail not because models cannot generate outputs. They fail because:

- **behavior is unstable** — the same input gives different outputs across runs
- **improvements cannot be measured** — "it feels better" is not engineering
- **regressions are invisible** — a change that helps one case may break three others, and nobody notices
- **human evaluation does not scale** — you cannot manually check 10,000 outputs per release

Therefore:

```
Model
  ↓
Agent
  ↓
Application

must have

Evaluation Layer
```

The evaluation layer is not a luxury. It is the foundation that makes everything above it trustworthy.

## Why benchmark, not just tests

Unit tests verify **implementation correctness** — does the code do what the code says?

Benchmarks verify **behavioral quality** — does the system do what the user needs?

| | Unit Test | Benchmark |
|---|---|---|
| Question | Does code match spec? | Does system meet quality bar? |
| Answer | Pass / Fail | Multi-dimensional score |
| Scope | Single function | Entire system |
| Dataset | Synthetic inputs | Real or realistic cases |
| Evolution | Changes with code | Frozen; code adapts to it |

Both are needed. But in AI systems, behavioral quality is the harder problem.

## Why freeze before compare

A benchmark that changes while you're comparing systems is useless. You cannot tell whether a score difference is due to the system or the benchmark.

```
Freeze dataset → Run system A → Run system B → Compare
```

If the benchmark changes between runs, the comparison is invalid. This is why MBP enforces:

- **DRAFT → PREVIEW → FROZEN → DEPRECATED** lifecycle
- SHA256 dataset hash
- Version pinning for metrics and runner

## Why multi-dimensional, not single score

A single score hides everything. "Accuracy = 95%" does not tell you:

- Which cases fail?
- Are the failures systematic or random?
- Is the system gaming the metric?
- Does it work equally across languages, difficulties, categories?

MBP requires multi-dimensional metrics with category breakdown and failure corpus. A single aggregate score is allowed only as a convenience, never as the only reported number.

## Why failure cases first

Most benchmarks report success rates. MBP reports failure cases first.

```
Not: "95% accuracy"
But: "5% failure, here are the 50 failure cases, categorized by mode"
```

Failure cases are more actionable than success rates. They tell you exactly where to improve.

## Why invariance testing

A system that scores 90 on "介绍你的优势" but 40 on "为什么公司应该选择你" (same capability, different phrasing) is not understanding — it is keyword matching.

Invariance testing exposes this:

```
Same capability → Different expression → Scores should be close
Large drift → Keyword matching, not understanding
```

This is MBP's signature contribution. It tests whether the system has semantic understanding or surface-level pattern matching.

## Why hidden holdout

If all test data is public, systems can overfit to the benchmark. The score goes up, but real-world performance does not.

```
Public score  →  can be optimized against
Hidden score  →  reflects real-world performance
```

MBP supports both OPEN_SUITE (fully public) and HIDDEN_SUITE (protocol public, eval data hidden). The hidden holdout is the anti-gaming foundation.

## Why reproducibility

A result that cannot be reproduced is not a result. It is an anecdote.

MBP requires:

- Dataset SHA256
- Generator seed
- Adapter version
- Runtime version (Python, OS)
- Logical prediction SHA256 (excluding latency/host)

Anyone with the same versions and the same dataset should get the same logical results.

## Why separation of concerns

A benchmark should measure, not prescribe. It should not tell you how to build your system — only whether your system meets the quality bar.

```
Benchmark: "Here is the test. Here is the metric. Here is your score."
System:    "Here is my approach. I optimize for the metric."
```

The benchmark does not know or care about the system's internals. The system does not get to change the benchmark.

## Why protocol, not just code

A single benchmark repo is a project. A protocol is a standard that multiple benchmarks follow.

MBP defines:

- How to declare a benchmark (schema)
- How to version a dataset (freeze policy)
- How to report results (results schema)
- How to prevent gaming (anti-gaming policy)
- How to ensure reproducibility (provenance)

Any benchmark that conforms to MBP gets: consistent structure, shared runtime, cross-benchmark comparability.

## Summary

```
Benchmark first    — because you cannot improve what you cannot measure
Freeze before compare  — because changing benchmarks invalidate comparisons
Multi-dimensional  — because single scores hide failures
Failure cases first — because failures are actionable
Invariance testing  — because keyword matching is not understanding
Hidden holdout     — because public scores can be gamed
Reproducibility    — because irreproducible results are anecdotes
Separation         — because benchmarks measure, they do not prescribe
Protocol           — because one benchmark is a project, many benchmarks need a standard
```
