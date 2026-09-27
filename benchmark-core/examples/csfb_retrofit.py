"""CSFB retrofit example: run a speech-follow benchmark on benchmark-core.

CSFB is event-driven: each case has a script + a sequence of speech events,
and the engine maintains state across events (load_script → process_event ×N).
This adapter wraps that sequential protocol into benchmark-core's per-case
predict() interface.

Usage:
    python examples/csfb_retrofit.py
"""
from __future__ import annotations

import json
import math
import os
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


# --- Inline CSFB-style sample data ---

SAMPLE_CASES = [
    {
        "case_id": "csfb_001",
        "type": "speech_follow",
        "category": "normal",
        "script_segments": ["大家好", "今天我们讨论AI", "谢谢大家"],
        "events": [
            {"event_index": 0, "type": "final", "text": "大家好"},
            {"event_index": 1, "type": "final", "text": "今天我们讨论AI"},
            {"event_index": 2, "type": "final", "text": "谢谢大家"},
        ],
        "expectations": [
            {"event_index": 0, "expected_segment": 0},
            {"event_index": 1, "expected_segment": 1},
            {"event_index": 2, "expected_segment": 2},
        ],
    },
    {
        "case_id": "csfb_002",
        "type": "speech_follow",
        "category": "skip",
        "script_segments": ["第一段", "第二段", "第三段", "第四段"],
        "events": [
            {"event_index": 0, "type": "final", "text": "第一段"},
            {"event_index": 1, "type": "final", "text": "第三段"},
        ],
        "expectations": [
            {"event_index": 0, "expected_segment": 0},
            {"event_index": 1, "expected_segment": 2},
        ],
    },
]


# --- CSFB adapter: wraps an engine in the predict() interface ---

def make_csfb_adapter(engine_id, engine_fn):
    """Wrap a CSFB engine as a benchmark-core InProcessAdapter.

    engine_fn(script_segments, initial_index) -> engine object with:
        engine.process_event(event) -> {segment_index, confidence, ...}
    """

    def predict(case):
        segments = case["script_segments"]
        engine = engine_fn(segments, 0)
        predictions = []
        for event in case["events"]:
            pred = engine.process_event(event)
            predictions.append(pred)
        return {"predictions": predictions, "case_id": case["case_id"]}

    return InProcessAdapter(id=engine_id, version="0.2.0", fn=predict)


# --- Simple reference engine: exact text match ---

def exact_match_engine(segments, initial_index=0):
    class Engine:
        def __init__(self):
            self.segments = segments
            self.anchor = initial_index

        def process_event(self, event):
            text = event.get("text", "")
            for i, seg in enumerate(self.segments):
                if seg in text or text in seg:
                    self.anchor = i
                    break
            return {"segment_index": self.anchor, "confidence": 1.0}

    return Engine()


# --- CSFB metrics adapted to benchmark-core ---

def _flatten(preds, cases):
    """Flatten per-case predictions into per-event rows."""
    rows = []
    for pred, case in zip(preds, cases):
        expectations = {e["event_index"]: e for e in case.get("expectations", [])}
        for i, p in enumerate(pred["predictions"]):
            ex = expectations.get(i)
            rows.append({
                "case_id": case["case_id"],
                "category": case["category"],
                "predicted": p["segment_index"],
                "expected": ex["expected_segment"] if ex else None,
                "correct": (ex is None or p["segment_index"] == ex["expected_segment"]),
            })
    return rows


def _compute_event_accuracy(preds, cases):
    rows = _flatten(preds, cases)
    judged = [r for r in rows if r["expected"] is not None]
    return sum(r["correct"] for r in judged) / len(judged) if judged else 1.0


def _compute_mean_error(preds, cases):
    rows = _flatten(preds, cases)
    errors = [abs(r["predicted"] - r["expected"]) for r in rows if r["expected"] is not None]
    return sum(errors) / len(errors) if errors else 0.0


def _compute_category_breakdown(preds, cases):
    rows = _flatten(preds, cases)
    by_cat = {}
    for r in rows:
        if r["expected"] is not None:
            by_cat.setdefault(r["category"], []).append(r["correct"])
    return {cat: sum(v) / len(v) for cat, v in by_cat.items()}


def make_csfb_metrics():
    reg = MetricRegistry()
    reg.register(Metric(
        "event_accuracy",
        "fraction of events where predicted segment matches expected",
        _compute_event_accuracy,
        "fraction",
        True,
    ))
    reg.register(Metric(
        "mean_segment_error",
        "mean absolute segment index error",
        _compute_mean_error,
        "segments",
        False,
    ))
    reg.register(Metric(
        "accuracy_by_category",
        "per-category event accuracy",
        _compute_category_breakdown,
        "fraction",
        None,
    ))
    return reg


def run_csfb(output_dir="csfb_output"):
    ds = Dataset(version="0.2.0-preview.1", seed=20260923)
    ds.add_split("main", SAMPLE_CASES)
    ds.compute_hash()

    adapter = make_csfb_adapter("global-exact", exact_match_engine)
    metrics = make_csfb_metrics()

    runner = Runner("speech-follow", "0.2.0-preview.1", "0.1.0-draft")
    result = runner.run(ds, adapter, metrics)

    emitter = ReportEmitter(output_dir)
    emitter.emit_results(result, "global-exact", "0.2.0")
    emitter.emit_provenance(result)

    return result.metric_values


def main():
    vals = run_csfb()
    parts = [f"{k}={v:.4f}" if isinstance(v, float) else f"{k}={v}"
             for k, v in vals.items() if k != "accuracy_by_category"]
    print("global-exact: " + " ".join(parts))
    print(f"accuracy_by_category: {vals.get('accuracy_by_category')}")


if __name__ == "__main__":
    main()
