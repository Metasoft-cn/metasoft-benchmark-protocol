# Open-suite example (extracted from CSFB)

This is a minimal `OPEN_SUITE` example. The values are real CSFB v0.2.0-preview values, abridged.

- `benchmark-manifest.json` — valid against [`../../schemas/benchmark.schema.json`](../../schemas/benchmark.schema.json).
- `dataset-manifest.json` — valid against [`../../schemas/dataset-manifest.schema.json`](../../schemas/dataset-manifest.schema.json); this is CSFB's actual dataset manifest.
- `results.json` — valid against [`../../schemas/results.schema.json`](../../schemas/results.schema.json); an abridged result for the `global-exact` baseline.

## Validate

```bash
python -c "import jsonschema, json; \
  s=json.load(open('../../schemas/benchmark.schema.json')); \
  jsonschema.validate(json.load(open('benchmark-manifest.json')), s); print('benchmark OK')"
```

The full CSFB repository is at <https://github.com/Metasoft-cn/speech-follow-benchmark>.
