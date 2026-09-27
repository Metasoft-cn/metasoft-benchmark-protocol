"""Adapter contracts.

An adapter is the system under test. The engine calls it with case data and
collects predictions. Two transports are supported in this prototype:

- InProcessAdapter: a Python callable (for baselines and testing).
- SubprocessAdapter: subprocess stdio + JSONL (for real black-box adapters).
"""
from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import dataclass, field
from typing import Any, Callable, Protocol


class Adapter(Protocol):
    """The adapter interface every system under test must satisfy."""

    id: str
    version: str

    def predict(self, case: dict[str, Any]) -> dict[str, Any]:
        """Take a case dict, return a prediction dict."""
        ...


@dataclass
class InProcessAdapter:
    """An in-process callable adapter.

    Used for reference baselines and testing. The callable receives a case
    dict and returns a prediction dict.
    """

    id: str
    version: str
    fn: Callable[[dict[str, Any]], dict[str, Any]]

    def predict(self, case: dict[str, Any]) -> dict[str, Any]:
        return self.fn(case)


@dataclass
class SubprocessAdapter:
    """A subprocess stdio + JSONL adapter.

    Launches ``command`` as a subprocess. For each case, writes a JSON line to
    stdin and reads a JSON line from stdout. The subprocess is kept alive for
    all cases (persistent process mode).

    The subprocess must:
    - read JSON lines from stdin (one per case)
    - write JSON lines to stdout (one prediction per case)
    - flush stdout after each prediction
    """

    id: str
    version: str
    command: list[str]
    _proc: subprocess.Popen | None = field(default=None, init=False, repr=False)

    def _start(self) -> None:
        if self._proc is not None and self._proc.poll() is None:
            return
        self._proc = subprocess.Popen(
            self.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )

    def predict(self, case: dict[str, Any]) -> dict[str, Any]:
        self._start()
        assert self._proc is not None
        assert self._proc.stdin is not None and self._proc.stdout is not None
        line = json.dumps(case, ensure_ascii=False) + "\n"
        self._proc.stdin.write(line)
        self._proc.stdin.flush()
        resp = self._proc.stdout.readline()
        if not resp:
            raise RuntimeError(
                f"adapter {self.id} produced no output. "
                f"stderr: {self._proc.stderr.read() if self._proc.stderr else 'n/a'}"
            )
        return json.loads(resp)

    def close(self) -> None:
        if self._proc is not None:
            if self._proc.stdin:
                self._proc.stdin.close()
            self._proc.terminate()
            self._proc.wait(timeout=5)
            self._proc = None

    def __del__(self) -> None:
        try:
            self.close()
        except Exception:
            pass
