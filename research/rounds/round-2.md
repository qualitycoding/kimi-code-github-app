# Research round 2 — depth and adversarial pass

Date: 2026-10-29 UTC (the run crossed midnight; the run ID remains `20261028T232935Z`).

## Depth findings

1. **Tree truncation is a second, independent limit.** GitHub's recursive Git Trees response can itself be truncated. Its documented ceiling is 100,000 entries and 7 MB. The connector's 5,000-entry presentation cap therefore cannot treat a complete page as proof that the GitHub response was complete; it must propagate both connector and upstream truncation. Added C-016.
2. **GitHub refresh is single-use.** Refreshing returns a new access token and refresh token and invalidates both old credentials. Concurrent refresh attempts can therefore turn a valid session into a reauthentication loop. Per-GitHub-user serialization and atomic compare-and-swap persistence are required. Added C-017.
3. **CIMD introduces a server-side URL fetch.** A client ID can be an HTTPS URL hosting a JSON metadata document. That improves client identity portability but adds SSRF, redirect, DNS-rebinding, size, timeout, and cache-poisoning hazards. DCR and CIMD need one common metadata validator and a bounded safe fetcher. Added C-018.
4. **The current TypeScript SDK is split into v2 packages.** The stable server package is `@modelcontextprotocol/server`, not the legacy monolithic `@modelcontextprotocol/sdk`. The v2 line implements 2026-07-28 and offers legacy compatibility. Express and Node transports are separate packages. Added C-019.
5. **Revocation must revoke both credential domains.** A `github_app_authorization` revocation event requires deletion of GitHub credentials and invalidation of connector access/refresh grants for that user. Installation changes invalidate catalog caches but are never authorization evidence by themselves.
6. **Repository presentation must be streaming and bounded.** Raw file responses need an abortable byte cap, fatal UTF-8 decoding, line caps, and explicit metadata. Directory/tree cursors are connector presentation cursors only; GitHub recursive trees are not paginated.

## Adversarial challenges

| Attack or failure | Required outcome | Planned evidence |
|---|---|---|
| Attacker swaps a connector token between users or organizations | Token audience, subject, and GitHub credential binding fail closed | Security integration tests |
| Stolen GitHub installation token is replayed as a user credential | Rejected: user-driven reads accept only the server-held GitHub App user-token flow | Unit and architecture tests |
| Confused deputy reuses GitHub's static client ID with a new MCP client | Connector consent identifies client and exact redirect before GitHub redirect | OAuth state-machine tests |
| Replay of authorization code, OAuth state, connector refresh token, or GitHub refresh token | Single-use transaction and rotation detection; no grant issued | Integration tests with fixed clock |
| CIMD URL resolves to loopback, link-local, private, or redirect-to-private address | Fetch rejected before and after every redirect; DNS answers revalidated | Security tests with fake resolver |
| Webhook JSON is parsed before HMAC verification or a normal string comparison is used | Request rejected; raw bytes and constant-time comparison required | Official-vector and mutation tests |
| Revoked user's already-issued connector token is used | Token lookup sees revoked grant; repository call never reaches GitHub | Revocation integration test |
| GitHub tree is truncated while connector page is not | Result exposes `upstream_truncated=true` and cannot claim completeness | Fixture test |
| Binary, invalid UTF-8, overlong line, or oversized file is returned | Bounded error/truncation metadata; no invalid text or memory blow-up | Fixture and resource tests |
| GitHub sends 403/429 with Retry-After, or times out | Bounded backoff, deadline propagation, no write retry, redacted error | Deterministic gateway tests |
| Refresh races invalidate credentials | One flight per user; atomic credential generation; retry only from committed generation | Concurrency test |
| OAuth transient rows or audit data accumulate | Expiry within 15 minutes and 30-day retention sweeps are tested | Operational tests |
| Dependency version drift changes MCP behavior | Exact pins, lockfile, frozen handshake compatibility tests | Build and CI tests |
| Cached repository catalog outlives permission change | Cache is advisory; live user-token API response remains the authorization boundary | Security integration test |

## Contradictions and corrections

- The earlier generic reference to an MCP TypeScript SDK was too ambiguous for implementation. Current stable v2 package names and versions are now pinned; no plan step may install the legacy monolith by accident.
- An initial strict dependency spike with `skipLibCheck=false` failed in third-party optional-dialect declarations. This was a test-harness configuration problem, not a connector result. The verified configuration uses `skipLibCheck=true`; application code remains `strict=true`. Recorded as a tooling lesson.
- No researched claim was falsified. C-016 through C-020 were added.

## Round 3 required probes

Download and checksum Node 24.22.1; install the exact dependency graph; compile imports under the pinned TypeScript configuration; run a production dependency audit; preserve the machine-readable outputs. Live GitHub OAuth and Kimi end-to-end tests require implementation-time credentials and remain explicit verification steps rather than fabricated planner results.
