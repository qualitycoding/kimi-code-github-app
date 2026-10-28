# Assumptions and intake resolutions

| ID | Resolution | Consequence |
|---|---|---|
| A-001 | Supported surfaces are Kimi Code CLI and `kimi web`; hosted kimi.com certification is out of scope. | Deliver a custom Kimi Code plugin, not a claim of hosted Kimi marketplace availability. |
| A-002 | MVP is read-only: repositories, refs/trees, directories, and UTF-8 text files. | No writes, issues, PRs, Actions, clones, or persistent index. |
| A-003 | GitHub.com and GitHub Enterprise Cloud are supported; GHES self-hosted is out of scope. | GitHub API base URL is fixed to `https://api.github.com`. |
| A-004 | The service is multi-user and multi-installation from the first release. | Every credential and authorization decision is keyed by connector user; no shared installation-token authorization. |
| A-005 | A user sees only resources accessible to both that GitHub user and the app installation. | Use GitHub App user access tokens for user-driven API calls. |
| A-006 | No repository source is persisted in the MVP. | Only live API responses pass through the service; bounded caches cannot contain file content. |
| A-007 | Deployment artifact is Docker Compose on Ubuntu 24.04 with Caddy and PostgreSQL; public hostname is selected at G-002. | Local/staging configuration is literal; production DNS and host credentials are gate evidence. |
| A-008 | Target: 50 concurrent MCP requests, p95 connector-added latency below 300 ms excluding GitHub, under 1% connector errors, and below 512 MiB service memory with mocked GitHub. | Performance tests use a deterministic mock and report variance over five runs. |
| A-009 | Private source and GitHub credentials are sensitive; OAuth signing/storage keys are critical. | Encryption, redaction, least privilege, fail-closed authorization, and secret scanning are release blockers. |
| A-010 | Security/audit metadata is retained for 30 days; GitHub credentials persist until revocation/deletion; OAuth transient state expires within 15 minutes. | Scheduled deletion and deletion-on-revocation tests are required. |
| A-011 | Repository license is Apache-2.0; initial plugin/service version is 0.1.0 using SemVer. | Release packaging includes license, notices, changelog, and commit-SHA provenance. |
| A-012 | Maintenance includes weekly automated dependency alerts and monthly manual review; Critical vulnerabilities block release. | CI and operations include ownership and patching procedures. |
| A-013 | The user-supplied planning credential is ephemeral and must be revoked after planning. | It is never part of the delivered architecture or artifacts. |
| A-014 | Maximum tool inputs: 100 repositories per page, 5,000 tree entries, 256 KiB text file, 2,000 output lines. | Larger resources return explicit truncation/pagination metadata, never partial content presented as complete. |
| A-015 | Fresh-context subagent spawning is unavailable to the planner. | Mechanical cold-read and adversarial checks are committed; lack of independent model review is a residual Medium risk, not a silent pass. |
