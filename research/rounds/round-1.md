# Research round 1 — breadth

R0 loaded the knowledge store; R1 decomposed the engineering questions. R2 consulted current official Kimi, MCP, and GitHub documentation.

## Findings

- A manifest-only plugin is insufficient for this connector: Kimi can point to a remote MCP URL, but GitHub's client secret/private key and user credentials must remain in a backend.
- Per-user GitHub App user access tokens provide the required user∩app resource boundary. Installation tokens are installation-wide and must never be the sole authorization for a user request.
- Kimi supports browser OAuth for remote MCP servers and has changelog evidence of dynamic client registration. The server should implement DCR for Kimi compatibility and CIMD for current MCP compatibility.
- The connector is an OAuth proxy and therefore needs per-client consent, exact redirect matching, single-use state/code, PKCE S256, resource indicators, audience validation, and no token passthrough.
- Live Contents API access fits a no-source-retention MVP. Repository and installation catalogs must not become a stale authorization cache.
- Webhook validation, revocation handling, token rotation, bounded output, and GitHub-aware backoff are required.

## Gaps for round 2

Verify OAuth revocation/event details, CIMD/SSRF behavior, Git Tree truncation semantics, dependency/version compatibility, and security/operational failure modes. No contradictions found.
