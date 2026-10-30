# kimi-code-github-app

Read-only GitHub App connector for Kimi Code CLI and `kimi web` (planning repository).

Status: `BLOCKED — HUMAN DECISION REQUIRED` under planning protocol v3.6 — see
`plan/PLAN.md` (status header), `HANDOFF.md` (reading order), and `plan/amendment-v36/`
(amendment evidence). No implementation, deployment, release, or publication has been
executed.

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
