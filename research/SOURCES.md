# Sources and verification notes

Accessed 2026-10-28 UTC. Tier 1 means official specification, documentation, release metadata, or source.

1. [Kimi Code: Plugins](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/plugins) — Tier 1. Plugin installation, `kimi.plugin.json`, and `mcpServers` declarations. Live documentation has no immutable version; target Kimi 2.3.3 and re-run compatibility at implementation start.
2. [Kimi Code: MCP](https://www.kimi.com/code/docs/en/kimi-code-cli/customization/mcp.html) — Tier 1. HTTP transport, `/mcp-config login`, static credential alternatives, and plugin MCP behavior.
3. [Kimi Code changelog](https://www.kimi.com/code/docs/en/kimi-code-cli/changelog.html) — Tier 1. Version 2.3.3 dated 2026-10-26; 0.33.0 fixed stale OAuth client registration, providing evidence of DCR-based client registration.
4. [MCP Authorization, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization) — Tier 1. Protected-resource metadata, authorization metadata, PKCE/OAuth 2.1, resource indicators, audience validation, and CIMD/DCR compatibility.
5. [MCP Security Best Practices, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/security_best_practices) — Tier 1. Mandatory per-client consent for OAuth proxies, exact redirect matching, state handling, token-passthrough prohibition, and SSRF guidance.
6. [MCP Transports, 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic/transports) — Tier 1. Streamable HTTP POST endpoint and JSON/SSE response model.
7. [GitHub: Generate a user access token](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app) — Tier 1. User/app permission intersection, installation listing APIs, 8-hour tokens, refresh flow, PKCE, and revocation event.
8. [GitHub: Refresh user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/refreshing-user-access-tokens) — Tier 1. Rotation invalidates old access and refresh tokens; six-month refresh expiry.
9. [GitHub: Generate an installation access token](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app) — Tier 1. One-hour expiry, repository/permission downscoping, and 2026 stateless token-format notice.
10. [GitHub: Review installed Apps](https://docs.github.com/en/apps/using-github-apps/reviewing-and-modifying-installed-github-apps) — Tier 1. Selected-repository installation, suspension, uninstallation, and user deauthorization semantics.
11. [GitHub REST: App installations](https://docs.github.com/en/rest/apps/installations) — Tier 1. `/user/installations` and `/user/installations/{id}/repositories` contracts.
12. [GitHub REST: Repository contents](https://docs.github.com/en/rest/repos/contents#get-repository-content) — Tier 1. Contents-read permission, directory/file response forms, ref support, and size/directory limits.
13. [GitHub: Validate webhook deliveries](https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries) — Tier 1. Raw-body HMAC-SHA256 and constant-time comparison with official test vector.
14. [GitHub REST rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api) — Tier 1. User-token limits, concurrency/point secondary limits, and response-header backoff rules.
15. [GitHub App best practices](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/best-practices-for-creating-a-github-app) — Tier 1. Least privilege, secret storage, minimal webhooks, monitoring, and deletion.
16. [Node.js 24.22.1 release](https://nodejs.org/en/blog/release/v24.22.1) — Tier 1. LTS release dated 2026-10-21 and security fixes.
17. [GitHub REST: Git trees](https://docs.github.com/en/rest/git/trees#get-a-tree) — Tier 1. `truncated` response semantics and recursive-tree ceiling of 100,000 entries / 7 MB.
18. [GitHub REST OpenAPI description](https://github.com/github/rest-api-description) — Tier 1. Official response schema corroborating the tree `truncated` field.
19. [OAuth Client ID Metadata Document draft](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-client-id-metadata-document-00) — Tier 1. HTTPS-URL client ID and JSON metadata-document contract.
20. [MCP TypeScript SDK repository and releases](https://github.com/modelcontextprotocol/typescript-sdk) — Tier 1. Stable v2 package split, 2026-07-28 support, framework adapters, and Node requirement.
21. [npm registry](https://registry.npmjs.org/) — Tier 1 release metadata. Exact package versions and engine ranges queried 2026-10-29.
22. Local dependency spike `research/spikes/dependency/` — verified empirical evidence. Node checksum, lockfile, TypeScript import compile, and production audit output.
23. [Docker Engine 29 release notes](https://docs.docker.com/engine/release-notes/29/) and [Docker Compose releases](https://github.com/docker/compose/releases) — Tier 1. Engine 29.9.2 and Compose 5.6.1 security-release metadata.
24. [Caddy releases](https://github.com/caddyserver/caddy/releases) and [Caddy download](https://caddyserver.com/download) — Tier 1. Caddy 2.11.7 release/distribution metadata.
25. [PostgreSQL 18.6 release notes](https://www.postgresql.org/docs/release/18.6/) and [versioning policy](https://www.postgresql.org/support/versioning/) — Tier 1. PostgreSQL 18.6 security fixes and supported-release policy.
