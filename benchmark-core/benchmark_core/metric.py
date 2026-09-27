"""Metric definitions and registry.

A metric is a registered callable with metadata. The engine computes all
registered metrics and emits a results.schema.json-valid object. No composite
score is imposed by the engine; if a benchmark wants one, it registers it as
just another metric.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class Metric:
    """A single metric definition.

    Attributes:
        name: machine-readable metric name (snake_case).
        definition: human-readable definition + formula.
        compute: (predictions, cases) -> value. predictions is a list of
            dicts (one per case, or per case repeat). cases is a list of
            case dicts. The return value is a number, string, bool, or dict
            (for vector metrics like level_bias).
        unit: unit of the metric value (e.g. "score", "fraction", "seconds").
        higher_is_better: True/False for scalar metrics, None for vector metrics.
    """

    name: str
    definition: str
    compute: Callable[[list[dict], list[dict]], Any]
    unit: str = "value"
    higher_is_better: bool | None = None


class MetricRegistry:
    """Registry of metrics for a benchmark.

    Metrics are registered by name. The runner computes all registered metrics
    and includes them in the results object.
    """

    def __init__(self) -> None:
        self._metrics: dict[str, Metric] = {}

    def register(self, metric: Metric) -> None:
        if metric.name in self._metrics:
            raise ValueError(f"metric '{metric.name}' already registered")
        self._metrics[metric.name] = metric

    def get(self, name: str) -> Metric:
        return self._metrics[name]

    def names(self) -> list[str]:
        return list(self._metrics.keys())

    def compute_all(
        self, predictions: list[dict], cases: list[dict]
    ) -> dict[str, dict[str, Any]]:
        """Compute all registered metrics.

        Returns a dict metric_name -> {value, unit, higher_is_better, definition}.
        """
        results: dict[str, dict[str, Any]] = {}
        for name, m in self._metrics.items():
            value = m.compute(predictions, cases)
            results[name] = {
                "value": value,
                "unit": m.unit,
                "higher_is_better": m.higher_is_better,
                "definition": m.definition,
            }
        return results

    def __len__(self) -> int:
        return len(self._metrics)

    def __contains__(self, name: str) -> bool:
        return name in self._metrics
