"""Hidden-evaluator boundary for HIDDEN_SUITE benchmarks.

For HIDDEN_SUITE benchmarks, the engine's hidden_evaluator module:
- loads the hidden holdout from a path the participant cannot read,
- runs the adapter in an ephemeral job,
- returns only aggregate failure categories (never per-case hidden output),
- enforces submission rate limits and canary cases.

The public engine code defines the *boundary*; the hidden data and the final
evaluation runner are operator-controlled and not in the public repo.

This module is a stub for Phase 1. Full implementation is Phase 5 (Quant).
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HiddenEvaluatorConfig:
    """Configuration for the hidden evaluator boundary.

    Attributes:
        holdout_path: path to the hidden holdout (operator-controlled).
        rate_limit_per_hour: max submissions per hour.
        canary_count: number of canary cases to inject.
        ephemeral: whether to run the adapter in an ephemeral job.
    """

    holdout_path: str = ""
    rate_limit_per_hour: int = 10
    canary_count: int = 5
    ephemeral: bool = True


class HiddenEvaluator:
    """Hidden evaluator boundary.

    This is a stub. The full implementation is deferred to Phase 5 (Quant
    Hidden Suite). The boundary contract is defined here so benchmarks can
    declare their intent to use HIDDEN_SUITE mode.
    """

    def __init__(self, config: HiddenEvaluatorConfig) -> None:
        self.config = config

    def evaluate(self, adapter_id: str) -> dict:
        """Evaluate an adapter against the hidden holdout.

        Returns only aggregate failure categories, never per-case output.

        Raises:
            NotImplementedError: full implementation is Phase 5.
        """
        raise NotImplementedError(
            "HiddenEvaluator full implementation is Phase 5 (Quant). "
            "The boundary contract is defined here for declaration purposes."
        )
