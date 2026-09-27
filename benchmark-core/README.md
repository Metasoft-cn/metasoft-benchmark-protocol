# benchmark-core

Unified benchmark runtime for the Metasoft Benchmark Protocol (MBP).

**Status:** Phase 1 prototype. API may change before v0.1.0.

## What

A Python library that every MBP benchmark plugs into. Benchmarks contribute
**domain logic** (dataset, metrics, adapter contract); `benchmark-core`
contributes **plumbing** (load, run, validate, report, provenance).

## Install

```bash
cd benchmark-core
pip install -e ".[dev]"
```

## Usage

```python
from benchmark_core import (
    InProcessAdapter,
    Metric,
    MetricRegistry,
    Dataset,
    Runner,
    ReportEmitter,
)

# 1. Define your dataset
dataset = Dataset(version="0.1.0-draft")
dataset.add_split("scoring", [{"question": "q1", "answer": "a1", "ground_truth_score": 80}])
dataset.compute_hash()

# 2. Define your adapter (or use SubprocessAdapter for black-box)
adapter = InProcessAdapter(
    id="my-evaluator",
    version="0.1.0",
    fn=lambda case: {"score": 75.0},
)

# 3. Register your metrics
metrics = MetricRegistry()
metrics.register(Metric(
    name="mae",
    definition="Mean absolute error",
    compute=lambda preds, cases: sum(
        abs(p["score"] - c["ground_truth_score"])
        for p, c in zip(preds, cases)
    ) / len(cases),
    unit="score",
    higher_is_better=False,
))

# 4. Run
runner = Runner(
    benchmark_id="my-benchmark",
    benchmark_version="0.1.0-draft",
    protocol_version="0.1.0-draft",
)
result = runner.run(dataset, adapter, metrics)

# 5. Report
emitter = ReportEmitter("output/")
emitter.emit_results(result, system_under_test_id="my-evaluator")
emitter.emit_provenance(result)
```

## Modules

| Module | Responsibility |
|---|---|
| `adapter` | Adapter protocol, in-process callable, subprocess stdio transport |
| `metric` | Metric dataclass + MetricRegistry |
| `dataset` | Dataset loading (JSONL), splits, hash computation |
| `runner` | Execution engine: dispatch adapter, collect predictions, compute metrics |
| `report` | results.schema.json emitter + failure corpus writer |
| `provenance` | Dataset hash, run identity, logical SHA256 |
| `hidden_evaluator` | HIDDEN_SUITE boundary (stub, full impl in Phase 5) |

## Design

See [`docs/EVALUATION_ENGINE_DESIGN.md`](../docs/EVALUATION_ENGINE_DESIGN.md).
