"""Tests for adapters."""
from benchmark_core import InProcessAdapter, SubprocessAdapter


def test_in_process_adapter():
    adapter = InProcessAdapter(
        id="test",
        version="0.1.0",
        fn=lambda case: {"score": len(case["answer"])},
    )
    assert adapter.id == "test"
    result = adapter.predict({"answer": "hello"})
    assert result == {"score": 5}


def test_in_process_adapter_passthrough():
    adapter = InProcessAdapter(
        id="echo",
        version="0.1.0",
        fn=lambda case: {"echo": case},
    )
    result = adapter.predict({"q": "hi", "a": "bye"})
    assert result["echo"]["q"] == "hi"
    assert result["echo"]["a"] == "bye"


def test_subprocess_adapter(tmp_path):
    script = tmp_path / "adapter.py"
    script.write_text(
        "import json, sys\n"
        "for line in sys.stdin:\n"
        "    case = json.loads(line)\n"
        "    pred = {'score': len(case.get('answer', ''))}\n"
        "    sys.stdout.write(json.dumps(pred) + '\\n')\n"
        "    sys.stdout.flush()\n",
        encoding="utf-8",
    )
    adapter = SubprocessAdapter(
        id="sub",
        version="0.1.0",
        command=["python", str(script)],
    )
    result = adapter.predict({"answer": "hello"})
    assert result == {"score": 5}
    result2 = adapter.predict({"answer": "hi"})
    assert result2 == {"score": 2}
    adapter.close()
