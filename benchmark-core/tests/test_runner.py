"""Tests for the Runner."""
from benchmark_core import (
    Dataset,
    InProcessAdapter,
    Metric,
    MetricRegistry,
    Runner,
)


def _make_mini_benchmark():
    ds = Dataset(version="0.1.0-draft", seed=42)
    ds.add_split("scoring", [
        {"question": "q1", "answer": "good answer", "ground_truth_score": 90},
        {"question": "q2", "answer": "bad answer", "ground_truth_score": 30},
    ])
    ds.compute_hash()

    adapter = InProcessAdapter(
        id="test-evaluator",
        version="0.1.0",
        fn=lambda case: {"score": 80.0},
    )

    reg = MetricRegistry()
    reg.register(Metric(
        name="mae",
        definition="mean absolute error",
        compute=lambda preds, cases: sum(
            abs(p["score"] - c["ground_truth_score"])
            for p, c in zip(preds, cases)
        ) / len(cases),
        unit="score",
        higher_is_better=False,
    ))
    return ds, adapter, reg


def test_runner_basic():
    ds, adapter, reg = _make_mini_benchmark()
    runner = Runner("mini", "0.1.0-draft", "0.1.0-draft")
    result = runner.run(ds, adapter, reg)

    assert len(result.predictions) == 2
    assert len(result.cases) == 2
    assert "mae" in result.metrics
    mae = result.metrics["mae"]["value"]
    assert mae == (abs(80 - 90) + abs(80 - 30)) / 2


def test_runner_provenance():
    ds, adapter, reg = _make_mini_benchmark()
    runner = Runner("mini", "0.1.0-draft", "0.1.0-draft")
    result = runner.run(ds, adapter, reg)

    prov = result.provenance
    assert prov.benchmark_id == "mini"
    assert prov.benchmark_version == "0.1.0-draft"
    assert prov.adapter_id == "test-evaluator"
    assert len(prov.logical_prediction_sha256) == 64
    assert len(prov.logical_metrics_sha256) == 64
    assert prov.dataset_seed == 42


def test_runner_n_repeats():
    ds, adapter, reg = _make_mini_benchmark()
    runner = Runner("mini", "0.1.0-draft", "0.1.0-draft")
    result = runner.run(ds, adapter, reg, n_repeats=3)

    assert len(result.predictions) == 6
    assert result.n_repeats == 3
    assert all("_repeat_index" in p for p in result.predictions)


def test_runner_split_tagging():
    ds = Dataset(version="0.1.0-draft")
    ds.add_split("scoring", [{"q": "a", "gt": 80}])
    ds.add_split("ranking", [{"q": "b", "gt": 50}])
    ds.compute_hash()

    adapter = InProcessAdapter(
        id="test",
        version="0.1.0",
        fn=lambda case: {"score": 70.0},
    )
    reg = MetricRegistry()
    reg.register(Metric(
        name="mean",
        definition="mean score",
        compute=lambda preds, cases: sum(p["score"] for p in preds) / len(preds),
    ))

    runner = Runner("mini", "0.1.0-draft", "0.1.0-draft")
    result = runner.run(ds, adapter, reg)

    assert result.predictions[0]["_split"] == "scoring"
    assert result.predictions[1]["_split"] == "ranking"
