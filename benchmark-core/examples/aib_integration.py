"""AIB integration example: run the AI Interview Benchmark on benchmark-core.

This demonstrates how an existing benchmark (AIB) plugs into benchmark-core.
It wraps AIB's baselines as InProcessAdapters and registers AIB's 6 metrics
as benchmark-core Metrics, then runs through the unified Runner.

Usage:
    python examples/aib_integration.py --dataset-dir /path/to/ai-interview-benchmark/datasets
"""
from __future__ import annotations

import argparse
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from benchmark_core import (
    Dataset,
    InProcessAdapter,
    Metric,
    MetricRegistry,
    ReportEmitter,
    Runner,
)


# --- AIB baselines (copied from aib/baselines.py for self-containment) ---

def length_baseline(question, answer):
    return {"score": min(100.0, len(answer) * 2.0), "feedback": "length", "cited_evidence": []}


def keyword_baseline(question, answer):
    keywords = ["因为", "所以", "例如", "首先", "其次", "数据", "经验", "项目", "结果",
                "because", "for example", "first", "second", "data", "result"]
    hits = sum(1 for k in keywords if k in answer.lower())
    return {"score": min(100.0, hits * 18.0), "feedback": f"keyword:{hits}", "cited_evidence": []}


def constant_baseline(question, answer):
    return {"score": 50.0, "feedback": "constant", "cited_evidence": []}


BASELINES = {"length": length_baseline, "keyword": keyword_baseline, "constant": constant_baseline}


# --- Adapter wrapper: handles scoring/ranking/perturbation case types ---

def make_adapter(baseline_id, baseline_fn):
    def wrapped(case):
        if "answer" in case:
            return baseline_fn(case["question"], case["answer"])
        if "answer_better" in case:
            pb = baseline_fn(case["question"], case["answer_better"])
            pw = baseline_fn(case["question"], case["answer_worse"])
            return {"score_better": pb["score"], "score_worse": pw["score"]}
        return {"score": 50.0}
    return InProcessAdapter(id=baseline_id, version="0.1.0", fn=wrapped)


# --- AIB metrics adapted to benchmark-core's (predictions, cases) interface ---

def _compute_ranking_consistency(preds, cases):
    total = 0
    correct = 0
    for p, c in zip(preds, cases):
        if c.get("type") == "ranking":
            total += 1
            if p.get("score_better", 0) > p.get("score_worse", 0):
                correct += 1
    return correct / total if total > 0 else 1.0


def _compute_mae(preds, cases):
    errs = [abs(p["score"] - c["ground_truth_score"])
            for p, c in zip(preds, cases)
            if c.get("type") == "scoring" and "score" in p]
    return statistics.mean(errs) if errs else 0.0


def _compute_stability_sigma(preds, cases):
    by_case = {}
    for p, c in zip(preds, cases):
        cid = c.get("case_id", "")
        if "score" in p:
            by_case.setdefault(cid, []).append(p["score"])
    sigs = [statistics.stdev(seq) for seq in by_case.values() if len(seq) > 1]
    return statistics.mean(sigs) if sigs else 0.0


def _compute_level_bias(preds, cases):
    by_diff = {}
    for p, c in zip(preds, cases):
        if c.get("type") == "scoring" and "score" in p:
            d = c.get("difficulty", "unknown")
            by_diff.setdefault(d, []).append(p["score"] - c["ground_truth_score"])
    return {d: statistics.mean(v) for d, v in by_diff.items()}


def _compute_evidence_grounding(preds, cases):
    fracs = []
    for p, c in zip(preds, cases):
        if c.get("type") == "scoring":
            gt = set(c.get("evidence", []))
            ci = set(p.get("cited_evidence", []))
            fracs.append(len(gt & ci) / len(gt) if gt else 1.0)
    return statistics.mean(fracs) if fracs else 0.0


def _compute_paraphrase_drift(preds, cases):
    drifts = [abs(p["score"] - c["expected_score"])
              for p, c in zip(preds, cases)
              if c.get("type") == "perturbation" and "score" in p and "expected_score" in c]
    return statistics.mean(drifts) if drifts else 0.0


def make_metric_registry():
    reg = MetricRegistry()
    reg.register(Metric("ranking_consistency", "fraction of ranking cases correct",
                        _compute_ranking_consistency, "fraction", True))
    reg.register(Metric("mae", "mean absolute error", _compute_mae, "score", False))
    reg.register(Metric("stability_sigma", "mean per-case stdev", _compute_stability_sigma,
                        "score", False))
    reg.register(Metric("level_bias", "per-difficulty signed error", _compute_level_bias,
                        "score", None))
    reg.register(Metric("evidence_grounding", "mean evidence recall", _compute_evidence_grounding,
                        "fraction", True))
    reg.register(Metric("paraphrase_score_drift", "mean perturbation drift",
                        _compute_paraphrase_drift, "score", False))
    return reg


def run_aib(dataset_dir, output_dir, n_repeats=3):
    ds = Dataset.from_jsonl(
        version="0.1.0-draft",
        split_files={
            "scoring": os.path.join(dataset_dir, "scoring.jsonl"),
            "ranking": os.path.join(dataset_dir, "ranking.jsonl"),
            "perturbation": os.path.join(dataset_dir, "perturbation.jsonl"),
        },
        seed=20260927,
    )

    metrics = make_metric_registry()
    runner = Runner("ai-interview", "0.1.0-draft", "0.1.0-draft")
    emitter = ReportEmitter(output_dir)

    all_results = {}
    for name, fn in BASELINES.items():
        adapter = make_adapter(name, fn)
        result = runner.run(ds, adapter, metrics, n_repeats=n_repeats)
        emitter.emit_results(result, name, "0.1.0")
        all_results[name] = result.metric_values

    return all_results


def main():
    p = argparse.ArgumentParser(description="Run AIB on benchmark-core")
    p.add_argument("--dataset-dir", required=True, help="path to AIB datasets/")
    p.add_argument("--output-dir", default="aib_output", help="output directory")
    p.add_argument("--n-repeats", type=int, default=3)
    args = p.parse_args()

    results = run_aib(args.dataset_dir, args.output_dir, args.n_repeats)
    for name, vals in results.items():
        parts = [f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}"
                 for k, v in vals.items() if k != "level_bias"]
        print(f"{name}: {' '.join(parts)}")


if __name__ == "__main__":
    main()
