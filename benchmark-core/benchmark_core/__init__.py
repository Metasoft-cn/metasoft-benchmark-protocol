"""Metasoft Benchmark Core — unified runtime for MBP benchmarks.

Public API:
    Adapter, InProcessAdapter, SubprocessAdapter  — adapter contracts
    Metric, MetricRegistry                         — metric definitions
    Dataset, DatasetSplit                          — dataset loading
    Runner, RunResult                              — execution engine
    ReportEmitter                                  — results.schema.json emitter
    Provenance                                     — reproducibility metadata
"""
from .adapter import Adapter, InProcessAdapter, SubprocessAdapter
from .metric import Metric, MetricRegistry
from .dataset import Dataset, DatasetSplit
from .runner import Runner, RunResult
from .report import ReportEmitter
from .provenance import Provenance

from ._version import __version__
__all__ = [
    "Adapter",
    "InProcessAdapter",
    "SubprocessAdapter",
    "Metric",
    "MetricRegistry",
    "Dataset",
    "DatasetSplit",
    "Runner",
    "RunResult",
    "ReportEmitter",
    "Provenance",
]
