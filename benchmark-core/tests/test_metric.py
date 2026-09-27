"""Tests for Metric and MetricRegistry."""
from benchmark_core import Metric, MetricRegistry


def test_metric_basic():
    m = Metric(
        name="accuracy",
        definition="fraction correct",
        compute=lambda preds, cases: 1.0,
        unit="fraction",
        higher_is_better=True,
    )
    assert m.name == "accuracy"
    assert m.higher_is_better is True


def test_registry_register_and_get():
    reg = MetricRegistry()
    m = Metric(name="mae", definition="mean abs error", compute=lambda p, c: 0.0)
    reg.register(m)
    assert "mae" in reg
    assert reg.get("mae") is m
    assert reg.names() == ["mae"]
    assert len(reg) == 1


def test_registry_duplicate_raises():
    reg = MetricRegistry()
    m = Metric(name="x", definition="", compute=lambda p, c: 0)
    reg.register(m)
    try:
        reg.register(m)
        assert False, "should have raised"
    except ValueError:
        pass


def test_registry_compute_all():
    reg = MetricRegistry()
    reg.register(Metric(
        name="acc",
        definition="accuracy",
        compute=lambda preds, cases: sum(1 for p in preds if p["ok"]) / len(cases),
        unit="fraction",
        higher_is_better=True,
    ))
    reg.register(Metric(
        name="count",
        definition="total cases",
        compute=lambda preds, cases: len(cases),
        unit="count",
        higher_is_better=True,
    ))
    preds = [{"ok": True}, {"ok": False}, {"ok": True}]
    cases = [{}, {}, {}]
    results = reg.compute_all(preds, cases)
    assert results["acc"]["value"] == 2 / 3
    assert results["count"]["value"] == 3
    assert results["acc"]["unit"] == "fraction"
    assert results["acc"]["higher_is_better"] is True
