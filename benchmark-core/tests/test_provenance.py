"""Tests for Provenance."""
from benchmark_core import Provenance


def test_provenance_prediction_hash():
    prov = Provenance(
        benchmark_id="x",
        benchmark_version="0.1.0",
        protocol_version="0.1.0",
        dataset_version="0.1.0",
        dataset_hash="a" * 64,
        dataset_seed=42,
        adapter_id="a",
        adapter_version="0.1.0",
    )
    preds = [{"score": 80}, {"score": 90}]
    h = prov.set_prediction_hash(preds)
    assert len(h) == 64
    assert prov.logical_prediction_sha256 == h


def test_provenance_prediction_hash_deterministic():
    prov1 = Provenance("x", "0.1.0", "0.1.0", "0.1.0", "a" * 64, 42, "a", "0.1.0")
    prov2 = Provenance("x", "0.1.0", "0.1.0", "0.1.0", "a" * 64, 42, "a", "0.1.0")
    preds = [{"score": 80}, {"score": 90}]
    assert prov1.set_prediction_hash(preds) == prov2.set_prediction_hash(preds)


def test_provenance_metrics_hash():
    prov = Provenance("x", "0.1.0", "0.1.0", "0.1.0", "a" * 64, 42, "a", "0.1.0")
    metrics = {
        "mae": {"value": 10.5, "unit": "score"},
        "acc": {"value": 0.8, "unit": "fraction"},
    }
    h = prov.set_metrics_hash(metrics)
    assert len(h) == 64


def test_provenance_to_dict():
    prov = Provenance(
        benchmark_id="b",
        benchmark_version="0.1.0",
        protocol_version="0.1.0",
        dataset_version="0.1.0",
        dataset_hash="a" * 64,
        dataset_seed=42,
        adapter_id="a",
        adapter_version="0.1.0",
    )
    d = prov.to_dict()
    assert d["benchmark_id"] == "b"
    assert d["adapter_id"] == "a"
    assert d["dataset_seed"] == 42
