# AI Website Benchmark — Design Skeleton

**Status:** DESIGN ONLY. No implementation in this phase.
**Mode:** `OPEN_SUITE` (static-structure tracks) with possible `HIDDEN_SUITE` for hallucination holdout.
**Protocol:** MBP v0.1.0-draft

## Object

Input: an old website + business files (company facts, product specs, history).
Output: an AI-generated / renovated website.
The benchmark measures how well the renovation preserves truth, structure, and reachability without inventing facts.

## Proposed tracks

| Track | What it measures |
|---|---|
| Content Preservation | source text/meaning survives in the output |
| Information Coverage | important business facts appear in the output |
| Structural Reconstruction | pages/sections map to source structure |
| Navigation Completeness | all important pages reachable |
| Business Fact Hallucination | output claims not supported by source |
| Responsive Layout | layout works across viewports |
| Accessibility | a11y checks (contrast, alt, landmarks) |
| Performance | Core Web Vitals, load time |
| URL Migration | old URLs map to new URLs or redirects |
| SEO | see [`seo-track.md`](seo-track.md) |
| GEO | see [`geo-track.md`](geo-track.md) |

## Hallucinated Business Facts (first-class metric)

This MUST be a first-class metric, not a sub-track. If the source does not state "全国服务", "30年历史", "5000客户", "国际认证", but the generated site claims them, each is an `unsupported_business_claim` failure of severity `catastrophic`.

Detection: extract claims from the generated site; check each against the source business files; flag unsupported ones. This is a failure-corpus-first metric per MBP.

## Repository shape (when implemented)

First stage: a single repo, not three.

```
ai-website-benchmark/
├─ core/      # content, structure, navigation, hallucination, a11y, performance
├─ seo/       # SEO track
└─ geo/       # GEO track
```

Split into separate repos only when scale demands it.

## Existing assets (from inventory)

- `D:\03_Others\Desktop\江枫官网V2_第一轮审计报告.md` — an audit report (design, not code).
- `D:\03_Others\Desktop\AI评估GEO项目` — a GEO evaluation tool (`geoengine/`, `cli.py`); can seed the GEO track but is not a benchmark.

## Next step

Define the dataset shape (old-site corpus + business-fact ground truth), then prototype the hallucination detector. SEO and GEO tracks are specified in [`seo-track.md`](seo-track.md) and [`geo-track.md`](geo-track.md).
