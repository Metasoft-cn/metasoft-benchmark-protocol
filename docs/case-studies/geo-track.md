# GEO Track — Design Skeleton

**Status:** DESIGN ONLY. A sub-track of the AI Website Benchmark.

GEO (Generative Engine Optimization) measures whether the renovated website is correctly and faithfully extractable by LLMs / generative engines. It does NOT use "the AI likes this site" as a metric. Every metric is grounded in a verifiable claim.

## Metrics

| Metric | Definition |
|---|---|
| Fact Extraction Accuracy | facts extracted from the generated site by a fixed extractor match the source business facts |
| Entity Consistency | the same entity (name, product, location) is represented consistently across pages |
| Answerability | questions a user would ask are answerable from the site content |
| Source Traceability | each extracted fact traces to a page/element on the site |
| Citation Readiness | content is structured so a generative engine can cite a source URL |
| Hallucinated Answer Rate | a fixed QA extractor produces answers not supported by the source |
| Important Fact Coverage | fraction of source business facts present and extractable on the generated site |

## Failure categories

- `unsupported_extracted_fact`, `entity_inconsistency`, `unanswerable_important_question`, `uncitable_fact`, `hallucinated_answer`, `missing_important_fact`.

## Method

A fixed extractor (deterministic where possible, or a pinned model with a seed for reproducibility) reads the generated site and answers a fixed question set. Answers are checked against the source business-fact ground truth. This keeps the track reproducible and avoids "the AI likes it" subjectivity.

## Existing assets

`D:\03_Others\Desktop\AI评估GEO项目` has a `geoengine/` and `cli.py` that can seed the extractor, but it is a tool, not a benchmark. The benchmark wraps it with a frozen question set, ground truth, and failure corpus.
