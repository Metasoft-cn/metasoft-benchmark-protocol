"""Runner: the core execution engine.

Loads cases, dispatches the adapter, collects predictions, computes metrics,
and packages everything into a RunResult. The runner is generic — it does not
know domain semantics. Metrics and adapters are registered by the benchmark.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any

from .adapter import Adapter
from .dataset import Dataset
from .metric import MetricRegistry
from .provenance import Provenance


@dataclass
class RunResult:
    """The result of a single benchmark run."""

    predictions: list[dict[str, Any]]
    cases: list[dict[str, Any]]
    metrics: dict[str, dict[str, Any]]
    provenance: Provenance
    duration_seconds: float
    n_repeats: int

    @property
    def metric_values(self) -> dict[str, Any]:
        """Convenience: metric_name -> value."""
        return {name: m["value"] for name, m in self.metrics.items()}


@dataclass
class Runner:
    """The benchmark execution engine.

    Attributes:
        benchmark_id: e.g. "ai-interview".
        benchmark_version: e.g. "0.1.0-draft".
        protocol_version: MBP protocol version.
        mode: "OPEN_SUITE" or "HIDDEN_SUITE".
    """

    benchmark_id: str
    benchmark_version: str
    protocol_version: str
    mode: str = "OPEN_SUITE"

    def run(
        self,
        dataset: Dataset,
        adapter: Adapter,
        metrics: MetricRegistry,
        n_repeats: int = 1,
    ) -> RunResult:
        """Run the adapter over all cases and compute metrics.

        Args:
            dataset: the benchmark dataset (one or more named splits).
            adapter: the system under test.
            metrics: the metric registry.
            n_repeats: number of times to run each case (for stability metrics).

        Returns:
            RunResult with predictions, metrics, provenance, and timing.
        """
        cases = dataset.all_cases
        predictions: list[dict[str, Any]] = []
        start = time.monotonic()

        for i, case in enumerate(cases):
            for r in range(n_repeats):
                pred = adapter.predict(case)
                pred_entry = dict(pred)
                pred_entry["_case_index"] = i
                pred_entry["_split"] = case.get("_split", "")
                if n_repeats > 1:
                    pred_entry["_repeat_index"] = r
                predictions.append(pred_entry)

        duration = time.monotonic() - start

        metric_results = metrics.compute_all(predictions, cases)

        prov = Provenance(
            benchmark_id=self.benchmark_id,
            benchmark_version=self.benchmark_version,
            protocol_version=self.protocol_version,
            dataset_version=dataset.version,
            dataset_hash=dataset.hash or dataset.compute_hash(),
            dataset_seed=dataset.seed,
            adapter_id=adapter.id,
            adapter_version=adapter.version,
        )
        prov.set_prediction_hash(predictions)
        prov.set_metrics_hash(metric_results)

        return RunResult(
            predictions=predictions,
            cases=cases,
            metrics=metric_results,
            provenance=prov,
            duration_seconds=duration,
            n_repeats=n_repeats,
        )
