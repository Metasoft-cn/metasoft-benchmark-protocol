# Quant Strategy Black-box Benchmark — Design Skeleton

**Status:** DESIGN ONLY. No public leaderboard is run. No ASENT research rhythm is disturbed.
**Mode:** `HIDDEN_SUITE`
**Protocol:** MBP v0.1.0-draft

## Target

A general black-box evaluation protocol for personal / AI quant strategies. Not a "who has the highest return" leaderboard. The benchmark measures whether a strategy is robust, realistic, and research-clean, not whether it lucked into a regime.

## Public interface

A participant provides a **strategy adapter**:

- input: market state (bars, positions, config)
- output: orders or target positions

Source code is not required. The adapter is a black box.

## Hidden evaluator

Real evaluation uses:

- hidden market episodes,
- hidden temporal windows,
- hidden regimes,
- hidden cost perturbations,
- hidden execution assumptions.

Public: protocol, metric definitions, development set, sample scenarios.
Hidden: final evaluation periods, regime composition, stress selection, some execution perturbations.

Not all test windows are exposed, to prevent benchmark-specific overfitting.

## Core metrics

| Metric | Group |
|---|---|
| Return | performance |
| Sharpe-like risk-adjusted | performance |
| Max Drawdown | risk |
| Tail Loss | risk |
| Turnover | cost |
| Fee Sensitivity | cost |
| Slippage Sensitivity | cost |
| Regime Robustness | robustness |
| Parameter Stability | robustness |
| Exposure Concentration | risk |
| Recovery Time | risk |
| Trade Count | behavior |
| Capacity Proxy | realism |

## Research-integrity metrics (first-class)

| Metric | What it detects |
|---|---|
| PIT Compliance | point-in-time data used correctly |
| Temporal Leakage | future data leaking into decisions |
| Lookahead Detection | strategy peeks ahead |
| Unrealistic Fill Detection | fills at impossible prices/sizes |
| Execution Authenticity | fills respect spread, depth, impact |

A strategy that leaks the future is disqualified regardless of return.

## Black-box security boundary

Anti-gaming by engineering, not by口号:

- hidden evaluator (no raw holdout download),
- ephemeral evaluation jobs,
- submission hash + rate limits,
- randomized hidden episodes,
- no detailed per-case hidden output (aggregate failure categories only),
- canary episodes that an overfit strategy fails.

The goal is to prevent benchmark gaming, not to attack participants.

## Existing assets (from inventory)

- `D:\03_Others\Desktop\量化研究\ASENT_PUBLIC_STRATEGY_BENCHMARK` — harness, strict backtester, evidence, robustness, tests. Substantial, but a research harness, not a frozen black-box benchmark.
- `D:\03_Others\Desktop\quant-system-gitcode` — main system with CI.
- R2 is in governance / dependency-closure; do not disturb.

## Next step

This document is the design. No public quant leaderboard is run in this phase. When implemented, the benchmark adopts MBP `HIDDEN_SUITE` with the anti-gaming policy in [`../ANTI_GAMING.md`](../ANTI_GAMING.md).
