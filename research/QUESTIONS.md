# Research question tree

## Engineering

1. Which GitHub App authorization and permission model prevents cross-user and cross-installation repository exposure? Informs D-001, D-002, T-SEC.
2. Which MCP authorization discovery, client-registration, token, and transport behavior does Kimi Code support? Informs D-003, compatibility spikes, and frozen OAuth tests.
3. Which plugin manifest and installation flow exposes the remote MCP server in Kimi Code? Informs D-004 and plugin contract tests.
4. Which GitHub APIs provide selected repositories, trees, directories, and file contents with bounded output? Informs D-005 and repository tool tests.
5. Which token storage, webhook, revocation, logging, rate-limit, deployment, backup, and rollback controls satisfy the threat model? Informs D-006 through D-012 and security/operational tests.
6. Which exact runtime and dependency versions can be installed and tested in this environment? Informs `plan/ENVIRONMENT.md`.
