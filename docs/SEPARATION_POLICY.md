# Separation Policy — Public Benchmark vs Private Product R&D

**Status:** ENFORCED
**Reason:** Metasoft builds both public benchmarks (for the field) and private product components (for competitive advantage). The two must not collide: commercial-moat components must not become public test standards prematurely, and public benchmarks must not silently depend on private product code.

## Two tracks

### PUBLIC ROADMAP (open, reproducible, MBP-conformant)

```
CSFB v0.2 (PREVIEW)            — done
        ↓
AI Interview Benchmark v0.2    — next
        ↓
AI Website Benchmark            — design done
        ↓
Quant Strategy Benchmark        — design done (HIDDEN_SUITE)
```

These live in public repos under `Metasoft-cn/`, adopt MBP, and accept third-party participation.

### PRIVATE PRODUCT R&D (not public until deliberately released)

```
Adaptive Speaking Engine
        ↓
internal NextGen Benchmark
        ↓
MTRS
        ↓
selectively re-publish when ready
```

These live in private repos. They may use MBP internally for evaluation, but they are not public benchmarks and do not accept third-party submissions until a deliberate release decision.

## Commercial-moat components (DO NOT publish as public benchmark standards)

These components are the product's competitive advantage. They may be evaluated internally, but they must not become public test standards that would disclose the evaluation surface to competitors:

- **Personal Speech Rate Model** — individual speaking-rate adaptation
- **Time Budget Engine** — per-segment timing allocation
- **Topic Contract** — scope/coverage agreement between user and engine
- **Dynamic Prompt** — runtime prompt construction
- **Improvisation** — off-script handling
- **Rejoin** — return-to-script after deviation

Rule: a moat component is evaluated by an **internal** benchmark that is not published. If a public benchmark is later desired for a capability that overlaps a moat component, the public benchmark must measure the *interface* (input→output behavior), not the *internal model*, and must be approved as a deliberate release.

## What this prevents

- A public benchmark that encodes the Adaptive Speaking Engine's internal scoring, leaking the moat.
- A public benchmark that depends on private product code (violates MBP separation-of-concerns, SPEC §11).
- An agent autonomously pushing a NextGen / MTRS / Quant-hidden repo to public GitHub.

## Push governance

See [`SECURITY.md`](../SECURITY.md) → `PUBLIC_PUSH_REQUIRES_HUMAN_CONFIRMATION`. In summary:

- CSFB / AIB / MBP: public by design; pushes follow normal review.
- **NextGen benchmark, MTRS, Quant hidden suite, any repo naming a moat component: a human must confirm before the first public push.** An agent MUST NOT autonomously make these public.

## Enforcement checklist (before publishing a new benchmark repo)

1. Does it name or measure a moat component? If yes → private, stop.
2. Does it depend on private product code? If yes → stop (SPEC §11 violation).
3. Is it MBP-conformant (manifest + schema + CI)? If no → fix before publish.
4. Has a human approved the public push? If no → request confirmation.
