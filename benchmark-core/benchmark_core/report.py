"""Report emitter: results.schema.json + failure corpus writer.

Emits a results object conforming to MBP's results.schema.json. The failure
corpus is a separate JSON file containing per-failure reproduction traces.
"""
from __future__ import annotations

import json
import os
from typing import Any

from .runner import RunResult


class ReportEmitter:
    """Emit results and failure corpus files."""

    def __init__(self, output_dir: str) -> None:
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def emit_results(
        self,
        result: RunResult,
        system_under_test_id: str,
        system_under_test_version: str | None = None,
    ) -> str:
        """Emit a results.schema.json-valid object.

        Returns the path to the written file.
        """
        metrics_obj: dict[str, dict[str, Any]] = {}
        for name, m in result.metrics.items():
            entry: dict[str, Any] = {"value": m["value"]}
            if "unit" in m:
                entry["unit"] = m["unit"]
            metrics_obj[name] = entry

        results_obj = {
            "benchmark": {
                "id": result.provenance.benchmark_id,
                "version": result.provenance.benchmark_version,
                "protocol_version": result.provenance.protocol_version,
                "mode": "OPEN_SUITE",
            },
            "system_under_test": {
                "id": system_under_test_id,
                **(
                    {"version": system_under_test_version}
                    if system_under_test_version
                    else {}
                ),
            },
            "dataset": {
                "version": result.provenance.dataset_version,
                "hash": result.provenance.dataset_hash,
                "cases": len(result.cases),
                "events": len(result.predictions),
            },
            "metrics": metrics_obj,
            "runtime": {
                "duration_seconds": result.duration_seconds,
                "n_repeats": result.n_repeats,
            },
            "reproducibility": {
                "deterministic": result.n_repeats == 1,
                "logical_prediction_sha256": result.provenance.logical_prediction_sha256,
                "logical_metrics_sha256": result.provenance.logical_metrics_sha256,
            },
        }

        path = os.path.join(self.output_dir, "results.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(results_obj, f, indent=2, ensure_ascii=False)
        return path

    def emit_provenance(self, result: RunResult) -> str:
        """Emit a provenance JSON file alongside results."""
        path = os.path.join(self.output_dir, "provenance.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(result.provenance.to_dict(), f, indent=2, ensure_ascii=False)
        return path

    def emit_failure_corpus(
        self,
        failures: list[dict[str, Any]],
        categories: dict[str, int] | None = None,
    ) -> str:
        """Emit a failure corpus JSON file.

        Args:
            failures: list of failure item dicts.
            categories: optional dict category_name -> count.
        """
        if categories is None:
            categories = {}
            for f in failures:
                cat = f.get("category", "uncategorized")
                categories[cat] = categories.get(cat, 0) + 1

        corpus = {
            "count": len(failures),
            "categories": categories,
            "items": failures,
        }
        path = os.path.join(self.output_dir, "failures.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(corpus, f, indent=2, ensure_ascii=False)
        return path
