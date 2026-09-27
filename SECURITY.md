# Security Policy

## Reporting a vulnerability

Report security issues privately. Do not open a public issue for a vulnerability in MBP or an adopting benchmark. Include a description, a minimal reproduction, and an affected version.

## Scope

This policy covers the MBP repository itself. Adopting benchmarks have their own `SECURITY.md`.

## Hidden-suite boundary

`HIDDEN_SUITE` benchmarks protect their holdout by engineering, not by trust:

- The hidden evaluation set is not downloadable.
- Evaluation runs are ephemeral and controlled by the operator.
- Submissions are identified by hash; raw holdout data is never returned to submitters.
- Per-case hidden output is not returned; only aggregate failure categories are reported.

This is described in [`docs/ANTI_GAMING.md`](docs/ANTI_GAMING.md). The goal is to prevent benchmark gaming, not to attack participants.

## Secrets and private paths

A benchmark repository MUST NOT contain:

- secrets, credentials, API keys, or tokens,
- private product source code,
- private filesystem paths that identify non-public projects.

History rewrites to remove accidentally committed private data MUST preserve a backup ref and an old→new commit mapping, and MUST NOT be delivered by force push to a public remote that has already been published without coordination. See CSFB `reports/PRE_RELEASE_AUDIT.md` for an example of a sanitized history with a retained backup ref and explicit commit map.

## PUBLIC_PUSH_REQUIRES_HUMAN_CONFIRMATION

Some repositories are public by design (CSFB, AIB, MBP). Others MUST NOT be made public without explicit human confirmation:

- **NextGen benchmark** — internal product benchmark, not for public release.
- **MTRS** — internal product, not for public release.
- **Quant hidden suite** — the hidden holdout and final evaluation runner; publishing would destroy the anti-gaming boundary.
- **Any repository naming a moat component** (Personal Speech Rate Model, Time Budget Engine, Topic Contract, Dynamic Prompt, Improvisation, Rejoin) — see [`docs/SEPARATION_POLICY.md`](docs/SEPARATION_POLICY.md).

An agent MUST NOT autonomously `git push` these to a public remote or create a public GitHub repo for them. The first public push requires a human's explicit confirmation. Subsequent pushes to an already-public repo follow normal review.

Rationale: an autonomous public push of a moat component or a hidden holdout is irreversible enough to damage competitive position or destroy the benchmark's anti-gaming property.
