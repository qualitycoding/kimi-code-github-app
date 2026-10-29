# Pre-mortem round 2 — hardened-plan convergence

Date: 2026-10-29 UTC.
Context: fresh-context spawning remains unavailable; this is a structured adversarial re-simulation, not an independent model review (R-007).

## Incident report

It is six months after a release produced under the hardened plan. A rollback restore invalidates every restored GitHub credential and connector grant before traffic resumes, so revoked sessions do not return. Users must reauthenticate, which is disruptive but reversible and explicitly preferable to exposure. Signed webhooks have already been tested through Caddy, and a missed revocation event cannot restore GitHub access after GitHub invalidates the user token; a persistent post-refresh 401 also deletes both credential domains. No Critical security exposure is found.

The release candidate either meets the declared 50-request maximum-payload workload or stops under D-028 before G-002. It cannot hide slow tree/file samples in an aggregate average. Immutable image digests, consent transaction binding, storage quotas, and explicit fixture defaults remove the round-1 implementation forks. No High feature-blocking ambiguity or invalid frozen-test premise is found.

## Lens examination

- **Technical correctness:** restored sessions fail closed; no source is persisted; GitHub and connector truncation remain separate. No new Critical/High risk.
- **Dependency/supply-chain drift:** exact npm and container pins, audits, SHA-pinned CI actions, and candidate rebuild checks form one traceable chain. Future vulnerabilities still follow D-029.
- **Invalid research assumptions:** zero `single-source`/`inferred` claims. Live Kimi, staging, and benchmark outcomes remain honestly unverified and are risks R-008/R-009/R-010, not claimed facts.
- **Implementer misinterpretation:** exact quotas, cookie/CSRF behavior, test defaults, workload counts, and restore ordering are literal. D-033 still requires a halt for security/data/public-interface ambiguity.
- **Integrity:** all five runs, every wave, and every per-tool result are retained. Review/mutation placeholders remain NOT RUN; no green implementation evidence is fabricated.
- **Past lessons:** R0 had no matching active lessons. Reused knowledge remains limited to its documented scope. New planning corrections are recorded as L-20261029T002500Z and L-20261029T002530Z.
- **Scale/performance:** 15 measured waves per run include maximum tree/file fixtures; memory/error/per-tool p95 limits and D-028 failure handling apply. Attainability is R-009, not a hidden assumption.
- **Security:** backup purge, consent binding, DCR/transient caps, 401 revocation fallback, and raw-body proxy evidence address round 1. Residual delayed-revocation and independent-review limitations are R-012/R-007.
- **Operational/on-call:** restore forces reauthentication; rollback, alert, backup retention, and post-release checks are rehearsed. Unexecuted deployment evidence remains R-010.

## Convergence

Round 2 introduces no Critical or High risk and finds no unresolved Critical/High risk from round 1. Pre-mortem converges after two rounds, below the five-round maximum. Medium/Low residual and verification risks are retained in `RISK_REGISTER.md`; G-002 cannot pass until their implementation-time evidence requirements are satisfied.
