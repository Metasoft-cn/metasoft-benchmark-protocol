"""Tests for Dataset loading and hash computation."""
import json

from benchmark_core import Dataset, DatasetSplit
from benchmark_core.dataset import load_jsonl, file_sha256


def test_dataset_splits():
    ds = Dataset(version="0.1.0-draft")
    ds.add_split("scoring", [{"q": "a"}, {"q": "b"}])
    ds.add_split("ranking", [{"q": "c"}])
    assert ds.case_count == 3
    assert len(ds.splits) == 2
    assert len(ds.splits["scoring"]) == 2


def test_dataset_all_cases_tagged():
    ds = Dataset(version="0.1.0-draft")
    ds.add_split("scoring", [{"q": "a"}])
    ds.add_split("ranking", [{"q": "b"}])
    all_cases = ds.all_cases
    assert all_cases[0]["_split"] == "scoring"
    assert all_cases[1]["_split"] == "ranking"
    assert all_cases[0]["q"] == "a"


def test_dataset_hash_deterministic():
    ds1 = Dataset(version="0.1.0-draft")
    ds1.add_split("scoring", [{"q": "a"}, {"q": "b"}])
    ds1.compute_hash()

    ds2 = Dataset(version="0.1.0-draft")
    ds2.add_split("scoring", [{"q": "a"}, {"q": "b"}])
    ds2.compute_hash()

    assert ds1.hash == ds2.hash
    assert len(ds1.hash) == 64


def test_dataset_hash_order_independent():
    ds1 = Dataset(version="0.1.0-draft")
    ds1.add_split("scoring", [{"q": "a"}, {"q": "b"}])
    ds1.add_split("ranking", [{"q": "c"}])
    ds1.compute_hash()

    ds2 = Dataset(version="0.1.0-draft")
    ds2.add_split("ranking", [{"q": "c"}])
    ds2.add_split("scoring", [{"q": "a"}, {"q": "b"}])
    ds2.compute_hash()

    assert ds1.hash == ds2.hash


def test_dataset_hash_content_dependent():
    ds1 = Dataset(version="0.1.0-draft")
    ds1.add_split("scoring", [{"q": "a"}])
    ds1.compute_hash()

    ds2 = Dataset(version="0.1.0-draft")
    ds2.add_split("scoring", [{"q": "b"}])
    ds2.compute_hash()

    assert ds1.hash != ds2.hash


def test_dataset_from_jsonl(tmp_path):
    f = tmp_path / "cases.jsonl"
    f.write_text('{"q": "a"}\n{"q": "b"}\n', encoding="utf-8")
    ds = Dataset.from_jsonl("0.1.0-draft", {"main": str(f)})
    assert ds.case_count == 2
    assert ds.hash is not None
    assert len(ds.hash) == 64


def test_load_jsonl(tmp_path):
    f = tmp_path / "test.jsonl"
    f.write_text('{"a": 1}\n{"b": 2}\n\n', encoding="utf-8")
    cases = load_jsonl(str(f))
    assert len(cases) == 2
    assert cases[0] == {"a": 1}


def test_file_sha256(tmp_path):
    f = tmp_path / "test.bin"
    f.write_bytes(b"hello world")
    h = file_sha256(str(f))
    assert len(h) == 64
