# SEO Track — Design Skeleton

**Status:** DESIGN ONLY. A sub-track of the AI Website Benchmark.

The SEO track measures whether the renovated website preserves and improves technical SEO. It is checkable from the generated site alone (no search-engine telemetry required).

## Checks

| Check | What |
|---|---|
| robots | `robots.txt` present, parseable, not blocking important paths |
| sitemap | `sitemap.xml` present, valid, lists important URLs |
| canonical | each page has a correct canonical tag |
| title | each page has a non-empty, unique `<title>` |
| description | each page has a meta description |
| heading hierarchy | exactly one `<h1>`, headings nest correctly |
| structured data | JSON-LD or microdata for business/product where applicable |
| internal links | important pages linked from navigation or body |
| redirects | old URLs redirect (301) to new URLs where mapped |
| indexability | important pages not `noindex` |
| mobile | viewport meta, no horizontal overflow |
| performance | Core Web Vitals thresholds (LCP, CLS, INP) |

## Failure categories

- `missing_title`, `missing_description`, `broken_canonical`, `heading_hierarchy_violation`, `missing_structured_data`, `broken_internal_link`, `missing_redirect`, `noindex_important_page`, `mobile_regression`, `performance_regression`.

## No subjective ranking

The SEO track does not produce "this site is more SEO-friendly than that one" as a subjective score. It produces a pass/fail per check and a failure corpus. Aggregates are counts, not grades.
