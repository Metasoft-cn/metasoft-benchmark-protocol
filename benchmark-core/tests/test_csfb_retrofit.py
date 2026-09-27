"""Test CSFB retrofit with benchmark-core."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples"))

from csfb_retrofit import (
    SAMPLE_CASES,
    make_csfb_adapter,
    make_csfb_metrics,
    exact_match_engine,
)

from benchmark_core import Dataset, Runner, ReportEmitter


def test_csfb_metrics_registered():
    reg = make_csfb_metrics()
    assert len(reg) == 3
    assert "event_accuracy" in reg
    assert "mean_segment_error" in reg
    assert "accuracy_by_category" in reg


def test_csfb_run():
    ds = Dataset(version="0.2.0-preview.1", seed=20260923)
    ds.add_split("main", SAMPLE_CASES)
    ds.compute_hash()

    adapter = make_csfb_adapter("global-exact", exact_match_engine)
    metrics = make_csfb_metrics()
    runner = Runner("speech-follow", "0.2.0-preview.1", "0.1.0-draft")
    result = runner.run(ds, adapter, metrics)

    vals = result.metric_values
    assert vals["event_accuracy"] == 1.0
    assert vals["mean_segment_error"] == 0.0
    assert isinstance(vals["accuracy_by_category"], dict)
    assert vals["accuracy_by_category"]["normal"] == 1.0
    assert vals["accuracy_by_category"]["skip"] == 1.0


def test_csfb_report(tmp_path):
    ds = Dataset(version="0.2.0-preview.1", seed=20260923)
    ds.add_split("main", SAMPLE_CASES)
    ds.compute_hash()

    adapter = make_csfb_adapter("global-exact", exact_match_engine)
    metrics = make_csfb_metrics()
    runner = Runner("speech-follow", "0.2.0-preview.1", "0.1.0-draft")
    result = runner.run(ds, adapter, metrics)

    emitter = ReportEmitter(str(tmp_path))
    path = emitter.emit_results(result, "global-exact", "0.2.0")
    obj = json.loads(open(path, encoding="utf-8").read())
    assert obj["benchmark"]["id"] == "speech-follow"
    assert obj["metrics"]["event_accuracy"]["value"] == 1.0


def test_csfb_provenance():
    ds = Dataset(version="0.2.0-preview.1", seed=20260923)
    ds.add_split("main", SAMPLE_CASES)
    ds.compute_hash()

    adapter = make_csfb_adapter("global-exact", exact_match_engine)
    metrics = make_csfb_metrics()
    runner = Runner("speech-follow", "0.2.0-preview.1", "0.1.0-draft")
    result = runner.run(ds, adapter, metrics)

    prov = result.provenance
    assert prov.benchmark_id == "speech-follow"
    assert prov.adapter_id == "global-exact"
    assert len(prov.logical_prediction_sha256) == 64
