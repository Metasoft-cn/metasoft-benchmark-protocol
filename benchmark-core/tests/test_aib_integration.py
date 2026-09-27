"""Test AIB integration with benchmark-core.

Uses inline AIB-format data to avoid a hard dependency on the AIB repo path.
The data mirrors AIB's actual case format (scoring/ranking/perturbation).
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples"))

from aib_integration import (
    BASELINES,
    make_adapter,
    make_metric_registry,
)

from benchmark_core import Dataset, Runner, ReportEmitter


@pytest.fixture
def aib_dataset(tmp_path):
    scoring = [
        {"case_id": "sc_001", "type": "scoring", "question": "q1", "answer": "detailed answer with evidence",
         "ground_truth_score": 85, "difficulty": "easy", "evidence": ["evidence"]},
        {"case_id": "sc_002", "type": "scoring", "question": "q2", "answer": "vague",
         "ground_truth_score": 30, "difficulty": "hard", "evidence": []},
    ]
    ranking = [
        {"case_id": "rk_001", "type": "ranking", "question": "q1",
         "answer_better": "detailed answer", "answer_worse": "vague"},
    ]
    perturbation = [
        {"case_id": "pt_001", "type": "perturbation", "base_case_id": "sc_001", "perturbation": "paraphrase",
         "question": "q1", "answer": "rephrased detailed answer", "expected_score": 85},
    ]

    for name, data in [("scoring", scoring), ("ranking", ranking), ("perturbation", perturbation)]:
        f = tmp_path / f"{name}.jsonl"
        with open(f, "w", encoding="utf-8") as fh:
            for case in data:
                fh.write(json.dumps(case, ensure_ascii=False) + "\n")

    return Dataset.from_jsonl("0.1.0-draft", {
        "scoring": str(tmp_path / "scoring.jsonl"),
        "ranking": str(tmp_path / "ranking.jsonl"),
        "perturbation": str(tmp_path / "perturbation.jsonl"),
    }, seed=20260927)


def test_aib_metrics_registered():
    reg = make_metric_registry()
    assert len(reg) == 6
    assert "ranking_consistency" in reg
    assert "mae" in reg
    assert "stability_sigma" in reg
    assert "level_bias" in reg
    assert "evidence_grounding" in reg
    assert "paraphrase_score_drift" in reg


def test_aib_run_length_baseline(aib_dataset):
    adapter = make_adapter("length", BASELINES["length"])
    metrics = make_metric_registry()
    runner = Runner("ai-interview", "0.1.0-draft", "0.1.0-draft")
    result = runner.run(aib_dataset, adapter, metrics, n_repeats=3)

    vals = result.metric_values
    assert "mae" in vals
    assert "ranking_consistency" in vals
    assert isinstance(vals["ranking_consistency"], float)
    assert 0.0 <= vals["ranking_consistency"] <= 1.0
    assert vals["mae"] >= 0.0
    assert isinstance(vals["level_bias"], dict)


def test_aib_run_all_baselines(aib_dataset):
    metrics = make_metric_registry()
    runner = Runner("ai-interview", "0.1.0-draft", "0.1.0-draft")

    for name, fn in BASELINES.items():
        adapter = make_adapter(name, fn)
        result = runner.run(aib_dataset, adapter, metrics, n_repeats=3)
        vals = result.metric_values
        assert len(vals) == 6
        assert 0.0 <= vals["ranking_consistency"] <= 1.0
        assert vals["mae"] >= 0.0


def test_aib_report_emission(aib_dataset, tmp_path):
    adapter = make_adapter("keyword", BASELINES["keyword"])
    metrics = make_metric_registry()
    runner = Runner("ai-interview", "0.1.0-draft", "0.1.0-draft")
    result = runner.run(aib_dataset, adapter, metrics, n_repeats=3)

    emitter = ReportEmitter(str(tmp_path / "report"))
    path = emitter.emit_results(result, "keyword", "0.1.0")
    assert os.path.exists(path)

    obj = json.loads(open(path, encoding="utf-8").read())
    assert obj["benchmark"]["id"] == "ai-interview"
    assert "mae" in obj["metrics"]
    assert "ranking_consistency" in obj["metrics"]


def test_aib_provenance_complete(aib_dataset):
    adapter = make_adapter("constant", BASELINES["constant"])
    metrics = make_metric_registry()
    runner = Runner("ai-interview", "0.1.0-draft", "0.1.0-draft")
    result = runner.run(aib_dataset, adapter, metrics)

    prov = result.provenance
    assert prov.benchmark_id == "ai-interview"
    assert prov.adapter_id == "constant"
    assert len(prov.logical_prediction_sha256) == 64
    assert len(prov.logical_metrics_sha256) == 64
    assert prov.dataset_seed == 20260927
