"""Provenance and reproducibility metadata.

Records per-run identity: benchmark id + version + protocol_version,
dataset version + hash + seed, adapter id + version, logical prediction SHA256,
logical metrics SHA256, engine version + Python version + OS.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import dataclass, field
from typing import Any

from ._version import __version__ as ENGINE_VERSION


@dataclass
class Provenance:
    """Reproducibility metadata for a single run."""

    benchmark_id: str
    benchmark_version: str
    protocol_version: str
    dataset_version: str
    dataset_hash: str
    dataset_seed: int | None
    adapter_id: str
    adapter_version: str
    logical_prediction_sha256: str = ""
    logical_metrics_sha256: str = ""
    engine_version: str = ENGINE_VERSION
    python_version: str = field(default_factory=lambda: sys.version)
    os_info: str = field(default_factory=lambda: platform.platform())

    def set_prediction_hash(self, predictions: list[dict[str, Any]]) -> str:
        """Compute SHA256 over the canonical JSON of all predictions.

        Only logical fields are hashed (excluding latency/host-specific data).
        """
        h = hashlib.sha256()
        for pred in predictions:
            line = json.dumps(pred, sort_keys=True, ensure_ascii=False)
            h.update(line.encode("utf-8"))
            h.update(b"\n")
        self.logical_prediction_sha256 = h.hexdigest()
        return self.logical_prediction_sha256

    def set_metrics_hash(self, metrics: dict[str, dict[str, Any]]) -> str:
        """Compute SHA256 over the canonical JSON of metrics.

        Only logical metric values are hashed (excluding host-specific data).
        """
        logical = {}
        for name, m in metrics.items():
            logical[name] = m.get("value")
        h = hashlib.sha256()
        h.update(json.dumps(logical, sort_keys=True, ensure_ascii=False).encode("utf-8"))
        self.logical_metrics_sha256 = h.hexdigest()
        return self.logical_metrics_sha256

    def to_dict(self) -> dict[str, Any]:
        return {
            "benchmark_id": self.benchmark_id,
            "benchmark_version": self.benchmark_version,
            "protocol_version": self.protocol_version,
            "dataset_version": self.dataset_version,
            "dataset_hash": self.dataset_hash,
            "dataset_seed": self.dataset_seed,
            "adapter_id": self.adapter_id,
            "adapter_version": self.adapter_version,
            "logical_prediction_sha256": self.logical_prediction_sha256,
            "logical_metrics_sha256": self.logical_metrics_sha256,
            "engine_version": self.engine_version,
            "python_version": self.python_version,
            "os_info": self.os_info,
        }
