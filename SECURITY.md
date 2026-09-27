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
