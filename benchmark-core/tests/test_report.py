"""Tests for ReportEmitter."""
import json
import os

from benchmark_core import (
    Dataset,
    InProcessAdapter,
    Metric,
    MetricRegistry,
    ReportEmitter,
    Runner,
)


def _make_result():
    ds = Dataset(version="0.1.0-draft", seed=42)
    ds.add_split("scoring", [
        {"q": "a", "gt": 80},
        {"q": "b", "gt": 60},
    ])
    ds.compute_hash()

    adapter = InProcessAdapter(
        id="eval",
        version="0.1.0",
        fn=lambda case: {"score": 70.0},
    )

    reg = MetricRegistry()
    reg.register(Metric(
        name="mae",
        definition="mean abs error",
        compute=lambda preds, cases: 10.0,
        unit="score",
        higher_is_better=False,
    ))

    runner = Runner("test-bench", "0.1.0-draft", "0.1.0-draft")
    return runner.run(ds, adapter, reg)


def test_emit_results(tmp_path):
    result = _make_result()
    emitter = ReportEmitter(str(tmp_path))
    path = emitter.emit_results(result, system_under_test_id="eval", system_under_test_version="0.1.0")

    assert os.path.exists(path)
    obj = json.loads(open(path, encoding="utf-8").read())
    assert obj["benchmark"]["id"] == "test-bench"
    assert obj["system_under_test"]["id"] == "eval"
    assert obj["dataset"]["cases"] == 2
    assert obj["metrics"]["mae"]["value"] == 10.0
    assert len(obj["reproducibility"]["logical_prediction_sha256"]) == 64
    assert len(obj["reproducibility"]["logical_metrics_sha256"]) == 64


def test_emit_provenance(tmp_path):
    result = _make_result()
    emitter = ReportEmitter(str(tmp_path))
    path = emitter.emit_provenance(result)

    assert os.path.exists(path)
    obj = json.loads(open(path, encoding="utf-8").read())
    assert obj["benchmark_id"] == "test-bench"
    assert obj["adapter_id"] == "eval"
    assert len(obj["logical_prediction_sha256"]) == 64


def test_emit_failure_corpus(tmp_path):
    emitter = ReportEmitter(str(tmp_path))
    failures = [
        {"case_id": 0, "category": "ranking_error", "detail": "wrong order"},
        {"case_id": 1, "category": "score_drift", "detail": "drift > 10"},
    ]
    path = emitter.emit_failure_corpus(failures)

    assert os.path.exists(path)
    obj = json.loads(open(path, encoding="utf-8").read())
    assert obj["count"] == 2
    assert obj["categories"]["ranking_error"] == 1
    assert obj["categories"]["score_drift"] == 1
    assert len(obj["items"]) == 2


def test_emit_failure_corpus_empty(tmp_path):
    emitter = ReportEmitter(str(tmp_path))
    path = emitter.emit_failure_corpus([])
    obj = json.loads(open(path, encoding="utf-8").read())
    assert obj["count"] == 0
    assert obj["items"] == []
