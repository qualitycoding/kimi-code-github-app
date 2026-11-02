# kimi-code-github-app

A planned read-only GitHub App connector for Kimi Code CLI and `kimi web`. It is meant to be a remote
MCP server that lets those clients read repository content (repositories, trees and files) through a
GitHub App, with an OAuth flow and a consent step in front.

> **Status: planning only. Nothing is implemented, deployed or released.** The plan is marked
> `BLOCKED: HUMAN DECISION REQUIRED`. One item is unverified from the planning environment: the container
> image tag `node:24.22.1-trixie-slim` has to be checked with `docker buildx imagetools inspect` at the
> first step (S-000), or re-pinned by a human.

## What is in the repository

| Path | Contents |
|---|---|
| `HANDOFF.md` | Start here: reading order for whoever implements it |
| `plan/` | The plan (24 steps, 2 human gates: G-002 production release, G-003 lessons push), decisions, assumptions, environment, traceability |
| `src/` | Typed interfaces (`contracts.ts`) and class stubs (`index.ts`) whose every method throws "not implemented" |
| `tests/` | 30 specified tests (OAuth unit, repository integration, operational, security, performance, deployment). They are written to fail until the code exists. `tests/FROZEN_MANIFEST.sha256` records their hashes |
| `research/`, `knowledge/` | Claims register (23 claims), sources, spikes and research notes |
| `premortem/`, `reviews/` | Risk register (18 risks), assumption audit, cold read. The code review, adversarial review and mutation score have **not** been run |

## Planned stack

Node 24.22.1, TypeScript, the MCP TypeScript SDK (server, node and express packages), Express 5, Octokit,
Drizzle ORM on PostgreSQL, Pino, Zod, and Vitest and Stryker for tests.

```bash
npm install
npm test               # runs the frozen tests; expected to fail until implemented
npm run verify:freeze  # checks the test files against FROZEN_MANIFEST.sha256
```

## Implementation notes

### Loopback redirect matching for Kimi OAuth clients (pre-S-003)

Kimi Code CLI/desktop acts as the OAuth client for the connector and, for remote MCP
server login (`/mcp-config login <server-name>`), listens on a **local loopback redirect**
at `http://127.0.0.1:<port>/callback` with an **ephemeral, per-login port**. D-005
currently requires exact-string redirect-URI matching, which would reject every login.

When implementation reaches S-003 (CIMD/DCR validator), apply the RFC 8252 §7.3 loopback
rule: for `127.0.0.1`/`::1` loopback client redirect URIs, match host and path but allow
any port; keep exact-string matching for all non-loopback redirect URIs (HTTPS only). Add
a decision entry recording this rule before or during S-003, and cover it with the
redirect-validation tests (S-003 evidence: redirect-to-private and DNS-rebinding cases
already required by the plan).

## Licence

Apache License 2.0. See [LICENSE](LICENSE).
