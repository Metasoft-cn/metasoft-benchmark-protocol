"""End-to-end integration test: a mini benchmark using benchmark-core.

This mirrors the AIB pattern (scoring + ranking splits, MAE + ranking
consistency metrics) but is self-contained. It demonstrates that benchmark-core
can host a real benchmark workflow.
"""
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


def _make_dataset():
    ds = Dataset(version="0.1.0-draft", seed=20260927)
    ds.add_split("scoring", [
        {"question": "q1", "answer": "detailed answer", "ground_truth_score": 85, "difficulty": "easy"},
        {"question": "q2", "answer": "vague answer", "ground_truth_score": 40, "difficulty": "hard"},
        {"question": "q3", "answer": "medium answer", "ground_truth_score": 60, "difficulty": "medium"},
    ])
    ds.add_split("ranking", [
        {"question": "q1", "answer_better": "detailed answer", "answer_worse": "vague answer"},
    ])
    ds.compute_hash()
    return ds


def _make_adapter():
    def fn(case):
        if "answer" in case:
            return {"score": min(100.0, len(case["answer"]) * 5.0)}
        if "answer_better" in case:
            return {
                "score_better": min(100.0, len(case["answer_better"]) * 5.0),
                "score_worse": min(100.0, len(case["answer_worse"]) * 5.0),
            }
        return {"score": 50.0}

    return InProcessAdapter(id="length-eval", version="0.1.0", fn=fn)


def _make_metrics():
    reg = MetricRegistry()

    reg.register(Metric(
        name="mae",
        definition="mean absolute error between adapter score and ground truth",
        compute=lambda preds, cases: _compute_mae(preds, cases),
        unit="score",
        higher_is_better=False,
    ))

    reg.register(Metric(
        name="ranking_consistency",
        definition="fraction of ranking cases where better answer scores higher",
        compute=lambda preds, cases: _compute_ranking(preds, cases),
        unit="fraction",
        higher_is_better=True,
    ))

    return reg


def _compute_mae(preds, cases):
    errs = []
    for p, c in zip(preds, cases):
        if "ground_truth_score" in c and "score" in p:
            errs.append(abs(p["score"] - c["ground_truth_score"]))
    return sum(errs) / len(errs) if errs else 0.0


def _compute_ranking(preds, cases):
    correct = 0
    total = 0
    for p, c in zip(preds, cases):
        if "answer_better" in c:
            total += 1
            if p.get("score_better", 0) > p.get("score_worse", 0):
                correct += 1
    return correct / total if total > 0 else 1.0


def test_integration_end_to_end(tmp_path):
    ds = _make_dataset()
    adapter = _make_adapter()
    metrics = _make_metrics()

    runner = Runner("mini-interview", "0.1.0-draft", "0.1.0-draft")
    result = runner.run(ds, adapter, metrics)

    assert len(result.cases) == 4
    assert len(result.predictions) == 4
    assert "mae" in result.metrics
    assert "ranking_consistency" in result.metrics
    assert result.metrics["ranking_consistency"]["value"] == 1.0

    emitter = ReportEmitter(str(tmp_path))
    results_path = emitter.emit_results(result, "length-eval", "0.1.0")
    prov_path = emitter.emit_provenance(result)

    assert os.path.exists(results_path)
    assert os.path.exists(prov_path)

    obj = json.loads(open(results_path, encoding="utf-8").read())
    assert obj["benchmark"]["id"] == "mini-interview"
    assert obj["dataset"]["cases"] == 4
    assert obj["metrics"]["mae"]["value"] >= 0
    assert obj["reproducibility"]["logical_prediction_sha256"]


def test_integration_n_repeats_stability(tmp_path):
    ds = _make_dataset()
    adapter = _make_adapter()
    metrics = _make_metrics()

    runner = Runner("mini-interview", "0.1.0-draft", "0.1.0-draft")
    result = runner.run(ds, adapter, metrics, n_repeats=5)

    assert len(result.predictions) == 20
    assert result.n_repeats == 5

    repeat_indices = [p.get("_repeat_index") for p in result.predictions]
    assert set(repeat_indices) == {0, 1, 2, 3, 4}
