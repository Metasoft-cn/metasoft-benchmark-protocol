"""Dataset loading.

A Dataset is a collection of named splits. Each split is a list of case dicts
loaded from a JSONL file. The dataset manifest provides metadata (version,
hash, seed, case_count).
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any


@dataclass
class DatasetSplit:
    """A named split of a dataset (e.g. scoring, ranking, perturbation)."""

    name: str
    cases: list[dict[str, Any]]

    def __len__(self) -> int:
        return len(self.cases)

    def __iter__(self):
        return iter(self.cases)


@dataclass
class Dataset:
    """A benchmark dataset with one or more named splits.

    Attributes:
        version: dataset version string.
        splits: dict split_name -> DatasetSplit.
        seed: optional generator seed.
        hash: SHA256 of all split files (computed if not provided).
    """

    version: str
    splits: dict[str, DatasetSplit] = field(default_factory=dict)
    seed: int | None = None
    hash: str | None = None

    def add_split(self, name: str, cases: list[dict[str, Any]]) -> None:
        self.splits[name] = DatasetSplit(name, cases)

    @property
    def case_count(self) -> int:
        return sum(len(s) for s in self.splits.values())

    @property
    def all_cases(self) -> list[dict[str, Any]]:
        """All cases from all splits, with ``_split`` tag added."""
        result = []
        for split in self.splits.values():
            for case in split.cases:
                tagged = dict(case)
                tagged["_split"] = split.name
                result.append(tagged)
        return result

    def compute_hash(self) -> str:
        """Compute SHA256 over the canonical JSON of all splits."""
        h = hashlib.sha256()
        for name in sorted(self.splits.keys()):
            h.update(name.encode("utf-8"))
            h.update(b"\n")
            for case in self.splits[name].cases:
                line = json.dumps(case, sort_keys=True, ensure_ascii=False)
                h.update(line.encode("utf-8"))
                h.update(b"\n")
        self.hash = h.hexdigest()
        return self.hash

    @classmethod
    def from_jsonl(
        cls,
        version: str,
        split_files: dict[str, str],
        seed: int | None = None,
    ) -> "Dataset":
        """Load a dataset from named JSONL files.

        Args:
            version: dataset version string.
            split_files: dict split_name -> file_path.
            seed: optional generator seed.
        """
        ds = cls(version=version, seed=seed)
        for name, path in split_files.items():
            cases = load_jsonl(path)
            ds.add_split(name, cases)
        ds.compute_hash()
        return ds


def load_jsonl(path: str) -> list[dict[str, Any]]:
    """Load a JSONL file into a list of dicts."""
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_manifest(path: str) -> dict[str, Any]:
    """Load a benchmark manifest JSON file."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def file_sha256(path: str) -> str:
    """Compute SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()
