# Implementation plan

Status: READY — planning complete; no implementation, deployment, release, or publication has been executed.
Profiles: `software`; `software.deploys=true`.
Claims: 23 total — 21 corroborated, 2 verified.
Tests: 30 total — 7 OAuth unit, 8 repository integration, 6 operational, 3 security, 1 performance, 5 deployment/live-surface.
Steps: 24. Gates: 2 (G-002, G-003).
Risks: 15 total — 1 Critical mitigated, 6 High mitigated, 7 Medium residual/verification, 1 Low accepted/mitigated; 0 unresolved Critical/High.
Assumption audit: 78 items — 63 confirmed, 0 falsified, 15 unverifiable with linked risks/tests.
Code-review findings by severity: NOT RUN — no zero-finding claim. Adversarial breaks: NOT RUN — no zero-break claim. Mutation score: NOT RUN — no score claimed.

## Protocol v3.6 persistence rule (Global Rule 6)

After every step turns green, after every amendment round, after every review record, and
after every gate record: commit the changed paths with a precise message, push to the
working branch, verify the remote head with `git ls-remote`, and record the verified hash
in `EXECUTION_LOG.md`. If local HEAD and the remote branch hash differ, stop and reconcile
from committed state; never force-push. If push fails transiently, retry up to three times
with 5, 15, and 45 second delays, then retry once with
`git -c http.version=HTTP/1.1 push`. If authentication remains unavailable, do not request
or reuse a pasted PAT: write a Git bundle under the durable output path, record the path,
and report the mismatch as blocked. A locally blocked verification is never marked
completed.

### S-000 Environment & Access Verification
- Tier: Haiku
- Profile: software; software.deploys
- Depends on: none
- Inputs: generation branch `gen-20261028T232935Z-kimi-github-app-connector`; `plan/ENVIRONMENT.md`; target `qualitycoding/kimi-code-github-app`; predeclared test GitHub App/user/repositories, staging origin/host, and alert target
- Actions: 1. `git switch -c impl-20261028T232935Z`. 2. Execute every planner-verified setup command and host preflight in `plan/ENVIRONMENT.md`. 3. Verify target push access, `https://api.github.com`, staging DNS/TLS, Docker daemon, PostgreSQL, test App permissions, and both Kimi 2.3.3 surfaces without printing secrets. 4. Resolve the linux/amd64 manifest digests for exactly `node:24.22.1-trixie-slim`, `caddy:2.11.7-alpine`, and `postgres:18.6-trixie` with `docker buildx imagetools inspect`; record the non-secret image@sha256 values in `ENVIRONMENT_VERIFICATION.md`, and block if any exact tag is unavailable. 5. Create `EXECUTION_LOG.md` and `DEVIATIONS.md`; append UTC time, step, attempt, outcome, commit, and note for this and every later attempt.
- Ephemeral environment (v3.6): record the environment class with a probe (`ENVIRONMENT_VERIFICATION.md` must state `environment_class` and the probe evidence), keep all durable state inside the repository working tree with `/tmp` used only for disposable caches, restage the pinned Node runtime under the ignored `.runtime/` directory when missing, and block with `BLOCKED.md` on any missing required tool or daemon instead of substituting versions or credentials
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: implementation branch; `EXECUTION_LOG.md`; `DEVIATIONS.md`; `.runtime/` ignored tool binaries; `ENVIRONMENT_VERIFICATION.md`
- Evidence produced: environment versions, lockfile/freeze hashes, non-secret access results; no T-### yet
- Done when: every setup, version, credential-permission, host, and reachability check passes and `sha256sum -c tests/FROZEN_MANIFEST.sha256` succeeds; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and `ENVIRONMENT_VERIFICATION.md`, `EXECUTION_LOG.md`, and `DEVIATIONS.md` each contain the environment class, remote head, and setup-check results
- Checkpoint: record implementation branch, environment evidence path, commit, and S-000 pass in `.checkpoints/state.json`
- On failure: before feature work, write `BLOCKED.md` listing each missing item; do not patch versions or request a PAT. After fixing access, rerun from a clean checkout with `git restore --source=HEAD --staged --worktree .`
- Gate: none
- Relevant decisions/claims: D-018, D-020, D-027, C-013, C-019, C-020
- Lessons applied: L-20261028T233100Z-git-auth-header; L-20261028T233130Z-private-knowledge-clone; L-20261029T000600Z-clean-install-storage
- Exclusive resources: repository working tree; staging host preflight

### S-001 Scaffold, Configuration, and Persistence
- Tier: Sonnet
- Profile: software; software.deploys
- Depends on: S-000
- Inputs: `package.json`, `package-lock.json`, `src/contracts.ts`, `src/index.ts`, `plan/DECISIONS.md` D-013/D-017/D-018/D-019
- Actions: 1. Replace only the relevant stubs with Express 5 composition, Zod configuration, Pino redaction, graceful lifecycle, and Drizzle/PostgreSQL wiring. 2. Create migrations for clients, OAuth transients, connector grants, encrypted GitHub credentials, webhook IDs, and audit metadata with UTC timestamps, generation constraints, unique delivery IDs, and the D-005 row-cap indexes. 3. Add `/health/live`, `/health/ready`, bounded JSON/raw-body parsers, trusted-proxy handling, and non-root container resource configuration using only the S-000 image digests. 4. Add `.env.example` with names only and database migration/rollback notes. 5. Make `createConnectorTestHarness()` return isolated initialized fixture services. Its runtime adapter passes `{}` unchanged for T-016's failure case, supplies non-secret test-only webhook/proxy/alert defaults only for T-016's exact otherwise-valid fixture, and never provides production defaults; other adapters execute their named real probes.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `src/config.ts`, `src/db/*`, `src/server.ts`, `drizzle/*`, `.env.example`, `Dockerfile`, initial `deploy/*`
- Evidence produced: T-016, T-017; migration up/down compatibility output
- Done when: T-016 and T-017 pass; missing configuration fails redacted; schema contains no repository source/path columns; migrations rerun idempotently; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result
- Checkpoint: record migration version, files, test results, and commit
- On failure: retry database startup once; `git restore --source=HEAD --staged --worktree src deploy drizzle .env.example Dockerfile`; if schema/data integrity is uncertain write `BLOCKED.md` rather than deleting volumes
- Gate: none
- Relevant decisions/claims: D-013, D-017, D-018, D-019, C-020
- Lessons applied: L-20261029T000500Z-third-party-typecheck
- Exclusive resources: repository working tree; test PostgreSQL database

### S-002 Cryptography and Token Stores
- Tier: Sonnet
- Profile: software
- Depends on: S-001
- Inputs: D-006/D-007/D-013/D-017; S-001 schema; fixed-clock test harness contract
- Actions: 1. Implement 32-byte random opaque connector credentials, SHA-256 lookup hashes, audience/client/subject binding, 3,600-second access and 30-day refresh expiry. 2. Implement AES-256-GCM GitHub credential encryption with unique nonces and key IDs. 3. Implement atomic generation compare-and-swap, old-generation replay rejection, per-grant and per-GitHub-user single-flight refresh locks, and transactional revocation. 4. Add deterministic fixed-clock/non-secret fixtures inside production test adapters, never live tokens.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `src/security/random.ts`, `src/security/crypto.ts`, `src/tokens/*`, updated test harness adapters
- Evidence produced: unit evidence supporting T-006, T-007, T-012, T-015, T-022; no new frozen tests
- Done when: concurrent refresh commits one generation, replay fails closed, plaintext credentials never appear in database/logs, and relevant frozen tests reach their later integration assertions; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and the token/crypto evidence records concurrent-refresh, replay, redaction, and fixed-clock results
- Checkpoint: record key ID, migration compatibility, concurrency result, and commit; never record key material
- On failure: revoke test grants and rerun once; `git restore --source=HEAD --staged --worktree src`; any replay/encryption ambiguity requires `BLOCKED.md`
- Gate: none
- Relevant decisions/claims: D-006, D-007, D-013, D-017, C-002, C-017
- Lessons applied: none
- Exclusive resources: repository working tree; test PostgreSQL database

### S-003 CIMD, DCR, and Safe Metadata Fetching
- Tier: Sonnet
- Profile: software
- Depends on: S-001
- Inputs: D-005 and public HTTP contract; `tests/oauth-unit.test.ts`; `tests/security.test.ts`
- Actions: 1. Implement authorization-client schemas and exact redirect/grant/public-client validation. 2. Implement DCR with the D-005 per-IP registration/OAuth-start limits, global client/transient caps, inactive-client deletion rule, and CIMD HTTPS-URL resolution using the same metadata validator. 3. Implement bounded safe fetch: 16 KiB metadata cap, 5-second timeout, at most three HTTPS redirects, JSON content validation, private/reserved/loopback IP denial, and DNS revalidation on every connection/redirect. 4. Add positive/negative fake-resolver fixtures and no-network production fallback for unrecognized client IDs.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `src/oauth/clients.ts`, `src/oauth/metadata-fetch.ts`, `src/oauth/registration.ts`, redacted test fixtures
- Evidence produced: T-002, T-003, T-024; SSRF resolver evidence
- Done when: T-002, T-003, and T-024 pass, including redirect-to-private and DNS-rebinding cases, with no arbitrary URL fetch; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and the SSRF evidence records redirect-to-private and DNS-rebinding cases
- Checkpoint: record client-metadata policy, fetch bounds, tests, and commit
- On failure: disable registration resolution and `git restore --source=HEAD --staged --worktree src/oauth tests/fixtures`; any SSRF bypass remains Critical and blocks progress
- Gate: none
- Relevant decisions/claims: D-005, D-026, C-007, C-008, C-018
- Lessons applied: none
- Exclusive resources: repository working tree; fake DNS resolver

### S-004 Nested OAuth, Consent, and GitHub Callback
- Tier: Sonnet
- Profile: software
- Depends on: S-002, S-003
- Inputs: D-003/D-004/D-006/D-007/D-008; authorization types; test App configuration
- Actions: 1. Implement `/oauth/authorize` and a same-origin consent page showing client name/ID, `github.read`, resource, and exact redirect; bind the consent to the original request with a Secure, HttpOnly, SameSite=Lax browser-transaction cookie and require a same-origin CSRF token on POST. 2. On approval create random 256-bit single-use upstream state with 10-minute expiry and redirect to GitHub with `offline_access` and PKCE. 3. Exchange GitHub code server-side, require expiring user token + refresh token, identify the user, encrypt credentials, and issue a five-minute single-use connector code bound to downstream PKCE/client/resource/redirect. 4. Deny canceled, mismatched, cross-session, cross-origin, expired, or replayed flows without issuing grants; S-ADVERSARIAL must include consent-CSRF and session-fixation attempts.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `src/oauth/authorize.ts`, `src/oauth/consent.ts`, `src/oauth/github.ts`, consent HTML/CSS, updated stores
- Evidence produced: T-004, T-005; GitHub token-shape fixture with secrets removed
- Done when: T-004 and T-005 pass; no GitHub redirect occurs before consent; no GitHub token appears in a browser redirect or MCP response; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and the consent evidence records no pre-consent GitHub redirect and no GitHub token in browser or MCP output
- Checkpoint: record OAuth expiry constants, state-machine tests, and commit
- On failure: delete transient test rows and `git restore --source=HEAD --staged --worktree src/oauth src/tokens`; halt on any consent/state/token leak
- Gate: none
- Relevant decisions/claims: D-003, D-004, D-006, D-007, C-001, C-002, C-009
- Lessons applied: none
- Exclusive resources: repository working tree; test PostgreSQL database; test GitHub OAuth fixture

### S-005 OAuth Metadata, Token Endpoint, and MCP Authentication
- Tier: Sonnet
- Profile: software
- Depends on: S-004
- Inputs: D-004/D-006/D-012 and HTTP error contract
- Actions: 1. Publish protected-resource and authorization-server metadata at the exact routes. 2. Implement `/oauth/token` authorization-code and refresh grants with S256 verification, exact client/resource binding, single-use codes, and coalesced rotation. 3. Implement idempotent `/oauth/revoke` and bearer middleware with 401 `WWW-Authenticate` plus 403 scope behavior. 4. Add constant-time hash lookup handling and redacted OAuth errors.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `src/oauth/metadata.ts`, `src/oauth/token.ts`, `src/oauth/revoke.ts`, `src/http/authentication.ts`
- Evidence produced: T-001, T-006, T-007
- Done when: T-001, T-006, and T-007 pass; wrong-resource tokens never reach MCP handlers; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and the authentication evidence records wrong-resource and wrong-audience rejection
- Checkpoint: record metadata URLs, rotation test, and commit
- On failure: revoke test grants and `git restore --source=HEAD --staged --worktree src/oauth src/http`; any audience bypass blocks all later steps
- Gate: none
- Relevant decisions/claims: D-004, D-006, D-012, C-008, C-017
- Lessons applied: none
- Exclusive resources: repository working tree; test PostgreSQL database

### S-006 GitHub Repository Gateway and Refresh Resilience
- Tier: Sonnet
- Profile: software
- Depends on: S-005
- Inputs: D-003/D-007/D-009/D-015/D-016; Octokit 5.0.5; test GitHub fixtures
- Actions: 1. Implement `/user/installations` and installation-repository pagination using only the authenticated user's GitHub App user token. 2. Add stable opaque cursors, 100-item cap, per-user 60-second advisory metadata cache, and 404 non-enumeration behavior. 3. Implement GitHub access-token expiry plus single-flight refresh/atomic generation handling; on a 401 that persists after that refresh, delete the user's GitHub credentials and connector grants before requiring reauthentication. 4. Add 10-second deadlines, at most two idempotent retries, rate-limit header handling, redacted errors, and no PAT/installation-token alternative.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `src/github/client.ts`, `src/github/repositories.ts`, `src/github/refresh.ts`, `src/github/errors.ts`
- Evidence produced: T-008, T-009, T-014, T-015
- Done when: all four tests pass; cross-tenant fixtures produce 404 before repository data is returned; old refresh replay cannot corrupt the committed credential; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and the gateway evidence records cross-tenant 404 behavior and refresh-generation protection
- Checkpoint: record pagination/rate-limit/refresh evidence and commit
- On failure: clear advisory cache and `git restore --source=HEAD --staged --worktree src/github`; any cross-user exposure is Critical, revoke test credentials, and write `BLOCKED.md`
- Gate: none
- Relevant decisions/claims: D-003, D-007, D-009, D-015, D-016, C-001, C-002, C-004, C-012, C-017
- Lessons applied: none
- Exclusive resources: repository working tree; test PostgreSQL database; mocked GitHub server

### S-007 Tree, Directory, and UTF-8 File Reads
- Tier: Sonnet
- Profile: software
- Depends on: S-006
- Inputs: D-009/D-010/D-016; `TreeResult` and `FileReadResult`; bounded fixtures
- Actions: 1. Resolve refs to immutable commit SHAs and implement Git Trees reads with recursive/nonrecursive modes, path validation, 5,000-entry presentation cursors, and independent upstream truncation. 2. Implement Contents/raw file reads with streaming abort at the connector cap, 256 KiB/2,000-line continuations, fatal UTF-8 decoding, and binary/symlink/submodule errors. 3. Never persist source or log full paths/content. 4. Verify memory behavior with oversized, invalid, compressed, and slow fixtures.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `src/github/trees.ts`, `src/github/files.ts`, `src/github/paths.ts`, bounded fixture generators
- Evidence produced: T-010, T-011; resource-bound output
- Done when: both tests pass; no response presents partial data as complete; memory remains bounded under T-021 harness; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and the read evidence distinguishes connector truncation from GitHub truncation and records memory-bound results
- Checkpoint: record cap/truncation/UTF-8 evidence and commit
- On failure: abort fixture streams and `git restore --source=HEAD --staged --worktree src/github`; do not raise caps or weaken UTF-8/path checks
- Gate: none
- Relevant decisions/claims: D-009, D-010, D-016, C-005, C-016
- Lessons applied: none
- Exclusive resources: repository working tree; mocked GitHub server

### S-008 Streamable-HTTP MCP Server and Tools
- Tier: Sonnet
- Profile: software
- Depends on: S-005, S-006, S-007
- Inputs: D-011/D-012; MCP server 2.4.0, Express adapter 2.0.2, Node adapter 2.1.2; three public gateway interfaces
- Actions: 1. Create per-request isolated MCP server/transport composition at `POST /mcp`, negotiating current and Kimi-compatible legacy revisions. 2. Register exactly the three read-only tools with Zod schemas, structured output, concise text, and safe `isError` mapping. 3. Enforce bearer middleware, canonical audience, request/body/concurrency bounds, origin policy, and request-scoped JSON/SSE behavior. 4. Confirm no GitHub or connector token is included in tool output.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `src/mcp/server.ts`, `src/mcp/tools.ts`, `src/mcp/errors.ts`, route wiring
- Evidence produced: end-to-end evidence completing T-008…T-011 through MCP, plus T-006/T-022
- Done when: authenticated MCP discovery and all three tools pass; unauthenticated/wrong-resource calls fail before tool execution; only three tools are listed; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and the MCP evidence records exactly three exposed tools and unauthenticated rejection
- Checkpoint: record negotiated protocol revisions, tool list, tests, and commit
- On failure: `git restore --source=HEAD --staged --worktree src/mcp src/server.ts`; if SDK behavior differs capture a redacted fixture and apply D-026 rather than bypassing authentication
- Gate: none
- Relevant decisions/claims: D-011, D-012, D-026, C-008, C-015, C-019
- Lessons applied: none
- Exclusive resources: repository working tree; MCP test client

### S-009 Webhooks, Revocation, and Retention
- Tier: Sonnet
- Profile: software
- Depends on: S-006, S-008
- Inputs: D-013/D-014/D-017; raw webhook route; retention policy
- Actions: 1. Route raw bytes to HMAC-SHA256 verification before parsing and use constant-time digest comparison. 2. Deduplicate `X-GitHub-Delivery`; handle user revocation, installation/repository changes, and suspension idempotently. 3. Revoke connector grants and delete GitHub credentials on user deauthorization; invalidate only advisory cache on installation changes. 4. Implement scheduled transient/audit deletion and tests for restart-safe sweeps.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `src/webhooks/*`, `src/jobs/retention.ts`, route wiring, migration updates if backward-compatible
- Evidence produced: T-012, T-013, T-020; idempotent delivery/sweep output
- Done when: all three tests pass; a revoked user's existing connector token cannot reach GitHub; duplicate delivery/sweep has no extra effect; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and the lifecycle evidence records duplicate webhook delivery, revocation, and sweep behavior
- Checkpoint: record webhook/retention test evidence and commit
- On failure: stop webhook processing and `git restore --source=HEAD --staged --worktree src/webhooks src/jobs src/server.ts`; any unverified processed payload is Critical
- Gate: none
- Relevant decisions/claims: D-013, D-014, D-017, C-010, C-011
- Lessons applied: none
- Exclusive resources: repository working tree; test PostgreSQL database

### S-010 Kimi Plugin and Administrator/User Documentation
- Tier: Sonnet
- Profile: software
- Depends on: S-008
- Inputs: D-002/D-008/D-023; Kimi plugin/MCP docs; staged connector origin placeholder
- Actions: 1. Create `kimi.plugin.json` with only the remote GitHub MCP URL and a manifest schema test outside the frozen suite. 2. Write App registration least-privilege settings, installation all/selected repository instructions, connector deployment configuration, and revocation instructions. 3. Write Kimi CLI/`kimi web` plugin installation and `/mcp-config login github` flow, tool examples, bounds, errors, and no-PAT security explanation. 4. Add Apache-2.0 license, security policy, and data-retention/privacy notice.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `kimi.plugin.json`, `README.md`, `docs/github-app.md`, `docs/kimi.md`, `docs/security.md`, `LICENSE`, `SECURITY.md`
- Evidence produced: manifest validation; documentation inputs for T-029/T-030
- Done when: a clean reader can install/login without any PAT field or secret in the plugin; documented permissions/routes match D-008 and source; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and `kimi.plugin.json` and the administrator/user documentation exist, validate, and contain no PAT or secret field
- Checkpoint: record manifest hash, docs paths, and commit
- On failure: `git restore --source=HEAD --staged --worktree kimi.plugin.json README.md docs LICENSE SECURITY.md`; any credential instruction other than browser OAuth must be removed before continuing
- Gate: none
- Relevant decisions/claims: D-002, D-008, D-023, C-006, C-007
- Lessons applied: none
- Exclusive resources: repository working tree

### S-011 Operational and Interruption Verification
- Tier: Sonnet
- Profile: software; software.deploys
- Depends on: S-009
- Inputs: T-016…T-024; Compose test stack; fixed-clock and failure fixtures
- Actions: 1. Run the full unit/integration/security suite through real HTTP and PostgreSQL with mocked GitHub. 2. Exercise SIGTERM drain, process interruption/restart, duplicate webhooks, expired grants, and migration resume. 3. Exercise oversized bodies, slow metadata, connection exhaustion, database unavailability, and GitHub timeouts while checking liveness. 4. Save redacted operational evidence and fix only production code.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `research/results/operational.json`, `research/results/security-integration.json`, `research/results/aggregate-test-log.json`, production fixes and lessons for implementer mistakes
- Evidence produced: T-016…T-024 as applicable
- Done when: T-001…T-024 pass together; no skipped/expected-failure tests; restart does not replay grants or webhook effects; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and `research/results/aggregate-test-log.json` records all frozen tests with zero skips or expected failures
- Checkpoint: record aggregate test counts, failure recovery, and commit
- On failure: preserve result JSON, retry only the failing scenario once, and `git restore --source=HEAD --staged --worktree src`; persistent security/data-integrity failure writes `BLOCKED.md`
- Gate: none
- Relevant decisions/claims: D-013, D-016, D-017, D-018, D-020, D-033
- Lessons applied: L-20261029T000600Z-clean-install-storage
- Exclusive resources: test Compose stack; PostgreSQL database; repository working tree

### S-012 Performance Benchmark and Resource Tuning
- Tier: Sonnet
- Profile: software
- Depends on: S-011
- Inputs: T-025; D-021; Autocannon 8.0.0; deterministic mocked-GitHub MCP workload
- Actions: 1. Build the D-021 pinned authenticated MCP benchmark measuring connector-added time separately from mock upstream time. 2. Run one excluded warm-up wave and 15 measured waves in each of five runs; every 50-request wave contains one 7 MiB/100,000-entry GitHub tree, 24 maximum file reads, and 25 full repository pages. Record every aggregate/per-tool p95, error, and memory value without dropping maximum-payload samples. 3. If targets fail, profile and tune production code without weakening authorization, bounds, workload shape, or fixtures. 4. Save raw and summarized results including per-tool p95 and variance.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `bench/mcp.ts`, `research/results/performance-run-{1,2,3,4,5}.json`, `research/results/performance-summary.json`
- Evidence produced: T-025 and five-run variance report
- Done when: aggregate and every per-tool p95 <300 ms, errors <1%, peak service memory <512 MiB, five complete workload-shaped p95 values exist, variance ≤20%, and T-025 passes; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and `research/results/performance-summary.json` contains five runs, aggregate and per-tool p95 values, error rate, peak memory, and variance on the recorded runner class
- Checkpoint: record all measurements, tuning commits, and final result
- On failure: apply D-028; after two unsuccessful fix attempts stop before release with `BLOCKED.md` and measurements; never discard slow runs
- Gate: none
- Relevant decisions/claims: D-021, D-028, A-008
- Lessons applied: none
- Exclusive resources: benchmark host; mocked GitHub; PostgreSQL database

### S-013 CI, Secret Scanning, and Supply-Chain Controls
- Tier: Sonnet
- Profile: software
- Depends on: S-011
- Inputs: D-020/D-022/D-029; exact lockfile; full source and deployment configuration
- Actions: 1. Add CI for Node checksum/setup, `npm ci`, typecheck, freeze verification, all tests, production audit, secret scan, and build. 2. Add weekly scheduled dependency alerts and monthly manual-review documentation. 3. Run secret scans over source, history, images, and release artifacts; verify logs/database fixtures contain no tokens or source, and verify every Docker/Compose base image matches its S-000 immutable digest. 4. Pin CI actions by full commit SHA and record release-blocking vulnerability policy.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `.github/workflows/ci.yml`, `.github/workflows/dependency-review.yml`, `research/results/supply-chain.json`, `docs/maintenance.md`
- Evidence produced: T-022, T-023; CI and scan results
- Done when: CI is green, zero Critical/High production findings remain, no secret is detected, weekly schedule exists, and frozen hashes still match; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result
- Checkpoint: record CI run URL, scan summaries, and commit; no credentials
- On failure: quarantine any detected credential by revocation, remove it from deliverables, and write the required lesson; `git restore --source=HEAD --staged --worktree .github src deploy`; Critical/High findings block later delivery
- Gate: none
- Relevant decisions/claims: D-020, D-022, D-029, C-020
- Lessons applied: L-20261029T000500Z-third-party-typecheck
- Exclusive resources: repository working tree; CI runner

### S-014 Staging Compose, Rollback, and Alert Rehearsal
- Tier: Sonnet
- Profile: software.deploys
- Depends on: S-012, S-013
- Inputs: `plan/OPERATIONS.md`; staging origin/host; `Dockerfile`; `deploy/*`; T-026…T-028
- Actions: 1. Build and scan the non-root image from the recorded digest; validate Compose/Caddy configuration and start staging with internal PostgreSQL and TLS. 2. Run migrations, health checks, authenticated MCP discovery, OAuth smoke, resource-limit checks, and valid/invalid raw-body signed webhooks through the public Caddy route. 3. Rehearse rollback to the previous known-good image/configuration and verify schema compatibility; rehearse backup restore with the connector stopped, delete all restored GitHub credentials and connector grants, and prove pre-restore tokens fail before reopening traffic. 4. Trigger failed-readiness and synthetic alert tests; save runbook evidence.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `deploy/docker-compose.yml`, `deploy/docker-compose.release.yml`, `deploy/Caddyfile`, `deploy/migrate.sh`, `deploy/rollback.sh`, `deploy/restore.sh`, `deploy/smoke.sh`, `research/results/staging.json`
- Evidence produced: T-026, T-027, T-028
- Done when: all three tests pass; Caddy preserves valid webhook HMACs and rejects altered bodies; rollback restores authenticated MCP health without resurrecting credentials/grants; alert reaches the predeclared on-call target within two minutes; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result
- Checkpoint: record staging image digest, migration version, rollback target, alert receipt, and commit
- On failure: apply D-030/D-032, keep production untouched, restore previous staging image, and retry at most three times before `BLOCKED.md`
- Gate: none
- Relevant decisions/claims: D-019, D-030, D-031, D-032
- Lessons applied: none
- Exclusive resources: staging host; staging database; alert channel

### S-015 Live GitHub App and Kimi Compatibility
- Tier: Sonnet
- Profile: software
- Depends on: S-014
- Inputs: test GitHub App with Contents Read, test user with both accessible and inaccessible private repositories, staging plugin URL, Kimi CLI and `kimi web` 2.3.3
- Actions: 1. Install the test App on personal and organization accounts using all-repositories and selected-repositories modes. 2. Install the plugin and complete `/mcp-config login github` in CLI, then equivalent browser OAuth in `kimi web`. 3. On each surface call all three read-only tools; verify selected/all visibility, cross-user denial, truncation metadata, revocation/relogin, and absence of token display. 4. Save redacted screenshots/logs with repository secrets removed.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `research/results/kimi-cli.json`, `research/results/kimi-web.json`, `research/results/github-installations.json`
- Evidence produced: T-029, T-030; live installation matrix
- Done when: both tests pass and the personal/organization × all/selected matrix matches user∩app visibility without a PAT; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and the live compatibility evidence (`research/results/kimi-cli.json`, `research/results/kimi-web.json`, `research/results/github-installations.json`) records the personal/organization and all/selected repository matrix
- Checkpoint: record Kimi versions, OAuth protocol revision, installation matrix, and commit
- On failure: capture redacted discovery/handshake evidence and apply D-026; do not substitute static tokens or claim compatibility. Revoke test grants before retry
- Gate: none
- Relevant decisions/claims: D-002, D-003, D-004, D-023, C-001, C-004, C-006, C-007
- Lessons applied: none
- Exclusive resources: browser session; test GitHub user/App installations; Kimi CLI/web profiles

### S-REVIEW Traditional Code Review
- Tier: Opus
- Profile: software; software.deploys
- Depends on: S-015
- Inputs: full implementation diff, frozen tests, dependency release/deprecation metadata, prior lessons, all research results
- Actions: 1. Start a fresh-context reviewer that authored no code. 2. Review bad patterns, hidden mutation, duplication, clarity, abstraction leaks, untested paths, injection, unsafe resource handling, secrets, validation, and dependency currency. 3. Classify findings Critical/High/Medium/Low; fix Critical/High before delivery and link every finding to a fix commit or accepted risk. 4. Record any new test need through the unfreeze/red/re-freeze amendment process and every implementer correction as a lesson.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `reviews/CODE_REVIEW.md`, linked fix commits and lessons
- Evidence produced: review findings by severity; frozen tests after any amendments
- Done when: no unresolved Critical/High finding, every code path has test coverage or a named rationale, and fresh-review identity is recorded; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result
- Checkpoint: record reviewer independence, findings, fixes, and commit
- On failure: return affected code to the responsible step; `git restore --source=HEAD --staged --worktree src` only before applying reviewed fixes; unresolved Critical/High blocks release
- Gate: none
- Relevant decisions/claims: D-020, D-025, D-033
- Lessons applied: all entries in `lessons/`
- Exclusive resources: repository working tree; fresh reviewer context

### S-ADVERSARIAL Adversarial Review
- Tier: Opus
- Profile: software; software.deploys
- Depends on: S-REVIEW
- Inputs: all assumptions A-001…A-015, source, frozen tests, threat model, staging stack, review fixes
- Actions: 1. Start a fresh-context adversary and attempt cross-tenant reads, OAuth replay/confused deputy, SSRF/DNS rebinding, webhook forgery, token leakage, refresh races, malicious paths/UTF-8, resource exhaustion, dependency outages, and rollback failure. 2. Challenge every assumption embodied in code and every single-source/inferred premise. 3. Turn each confirmed break into a frozen-test amendment or accepted severity-ranked risk; fix Critical/High before release. 4. Rerun the complete suite and staging abuse probes.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `reviews/ADVERSARIAL_REVIEW.md`, redacted exploit evidence, fixes/lessons/risks
- Evidence produced: confirmed-break count and resolutions; amended frozen tests if required
- Done when: zero unresolved Critical/High breaks; all Medium/Low breaks have explicit risk disposition; frozen manifest and full suite pass; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and `reviews/ADVERSARIAL_REVIEW.md` records every confirmed break and disposition
- Checkpoint: record attacks, confirmed breaks, fixes, residual risks, and commit
- On failure: isolate vulnerable routes and return to the earliest responsible step; any credential/source exposure triggers revocation and `BLOCKED.md`
- Gate: none
- Relevant decisions/claims: D-003…D-007, D-010, D-014, D-018, D-025, D-033
- Lessons applied: all entries in `lessons/`
- Exclusive resources: staging stack; test credentials; fresh adversary context

### S-MUTATE Mutation Testing
- Tier: Sonnet
- Profile: software
- Depends on: S-ADVERSARIAL
- Inputs: `stryker.config.json`, implemented `src/**/*.ts`, frozen suite, Stryker 10.1.1
- Actions: 1. `npm run test:mutation`. 2. Preserve HTML/JSON and classify every surviving mutant by behavior. 3. Add tests for meaningful survivors only through the formal amendment process, or document equivalent-mutant/class rationale. 4. Rerun until the score is at least 85% and no unexplained survivor remains.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `reviews/MUTATION.md`, `reports/mutation/*`, amendment records if any
- Evidence produced: mutation score and survivor disposition
- Done when: score ≥85%, every survivor has a test or written justification, and full frozen suite passes; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and `reviews/MUTATION.md` records the score and every survivor class or justification
- Checkpoint: record score, mutant classes, amendments, and commit
- On failure: never raise thresholds or exclude modules to pass; restore temporary mutation artifacts and return meaningful survivors to the responsible implementation step
- Gate: none
- Relevant decisions/claims: D-020, D-022
- Lessons applied: none
- Exclusive resources: mutation runner; repository working tree; test database

### S-017 Package the Release Candidate
- Tier: Sonnet
- Profile: software; software.deploys
- Depends on: S-MUTATE
- Inputs: all source/docs/tests/reviews/results; `plan/GATES.md`; Apache-2.0 and SemVer decisions
- Actions: 1. Set service/plugin version 0.1.0 and generate changelog/release notes with commit SHA, Node/lockfile hashes, all S-000 base-image digests, built image digest, and compatibility matrix. 2. Build plugin source archive and connector image without credentials; verify license/notices, manifest, and immutable base-image references. 3. Rerun clean install, typecheck, freeze, all tests, scans, and staging smoke from the exact candidate commit. 4. Assemble the G-002 evidence bundle without publishing a tag or deploying production.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `release/kimi-code-github-app-0.1.0.zip`, `release/SHA256SUMS`, `CHANGELOG.md`, `RELEASE_CANDIDATE.md`, `GATE-G-002.md` draft
- Evidence produced: candidate hashes and final verification counts; no external release
- Done when: candidate hashes reproduce, every required artifact is present, and all required tests/scans/reviews pass on the same commit; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result
- Checkpoint: record candidate commit/digests, evidence bundle, and commit
- On failure: delete only `release/` outputs and rebuild after correction; any new code change returns to S-REVIEW
- Gate: none
- Relevant decisions/claims: D-011, D-019, D-023, D-024
- Lessons applied: none
- Exclusive resources: repository working tree; release builder; staging smoke target

### S-018 Production Deployment and Public 0.1.0 Release
- Tier: Sonnet
- Profile: software.deploys
- Depends on: S-017
- Inputs: `GATE-G-002.md`, production origin/DNS/host/App settings/alert owner, candidate image and hashes, `plan/OPERATIONS.md`
- Actions: 1. Halt at G-002 and record exactly one allowed response. 2. On `proceed`, deploy the reviewed image digest with production secrets injected by the host, run backward-compatible migrations and health/authenticated smoke. 3. Publish the GitHub release/tag and plugin 0.1.0 archive only after deployment smoke passes. 4. On rescope/stop, follow `plan/GATES.md` and perform no external action.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `GATE-G-002.md`, production release record, git tag/GitHub release only after approval, deployment provenance
- Evidence produced: production deployment and public-release result, or documented no-action branch
- Done when: approved production is healthy and the exact candidate is publicly released, or the gate's non-proceed branch is fully recorded; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result
- Checkpoint: record gate response, release ID/digest/tag if any, and deployment commit
- On failure: execute `./deploy/rollback.sh "$PREVIOUS_RELEASE_ID"` per D-030/D-031, do not publish or withdraw to an unverified state, and halt with incident evidence
- Gate: G-002
- Relevant decisions/claims: D-019, D-024, D-030, D-031, D-032
- Lessons applied: none
- Exclusive resources: production host/database; GitHub release; DNS; alert channel

### S-019 Post-Release Verification and Handover
- Tier: Sonnet
- Profile: software.deploys
- Depends on: S-018
- Inputs: `plan/OPERATIONS.md`; production origin; release ID; monitoring and on-call configuration
- Actions: 1. At 1, 5, 15, 30, and 60 minutes run health/smoke and compare errors, latency, memory, database, webhooks, and refresh behavior. 2. Run one test-user revocation/relogin and one real Kimi read-only call. 3. Verify synthetic alert delivery and retention sweep; record rollback readiness. 4. Finalize operational handover and maintenance schedule.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `RELEASE_VERIFICATION.md`, `OPERATIONS_HANDOVER.md`
- Evidence produced: post-release measurements and alert/revocation evidence
- Done when: every check passes for 60 minutes or a non-proceed G-002 branch is accurately marked N/A; no D-031/D-032 condition remains; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and `RELEASE_VERIFICATION.md` records the 60-minute checks, alert result, and revocation result
- Checkpoint: record verification timestamps, owner, and final release state
- On failure: roll back immediately using the runbook, halt public rollout, and record an incident plus lessons; do not suppress alerts
- Gate: none
- Relevant decisions/claims: D-017, D-029, D-031, D-032
- Lessons applied: none
- Exclusive resources: production host/database; monitoring/alert channel; test GitHub user

### S-RETRO Retrospective
- Tier: Opus
- Profile: software; software.deploys
- Depends on: S-000, S-001, S-002, S-003, S-004, S-005, S-006, S-007, S-008, S-009, S-010, S-011, S-012, S-013, S-014, S-015, S-REVIEW, S-ADVERSARIAL, S-MUTATE, S-017, S-018, S-019
- Inputs: `EXECUTION_LOG.md`, commits, `DEVIATIONS.md`, `BLOCKED.md` if present, `TEST_CHALLENGE.md` if present, `GATE-*.md`, CI/review history, `research/PRIOR_KNOWLEDGE.md`, all lessons/knowledge
- Actions: 1. Have Haiku collect a single digest, then start a fresh Opus retrospective that reruns nothing and changes no deliverable. 2. Identify errors, corrections, overlooked checks, unapplied/recurring lessons, and new subject facts. 3. Link every finding to an existing or new L/K item and run Appendix C schema/secret checks. 4. Record release and non-proceed gate outcomes without rewriting history.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `RETROSPECTIVE.md`, new lessons/knowledge as required
- Evidence produced: retrospective findings and L/K links
- Done when: every finding links to an L/K file and all entry schemas and secret scans pass; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result; and `RETROSPECTIVE.md` records every finding, its L/K links, and the deviation-diff result
- Checkpoint: record retrospective completion and new L/K IDs
- On failure: supplement missing records only; do not rerun implementation or alter release artifacts to improve the narrative
- Gate: none
- Relevant decisions/claims: D-025, D-033
- Lessons applied: all entries in `lessons/`
- Exclusive resources: fresh retrospective context

### S-KNOW Lessons & Knowledge Push
- Tier: Haiku
- Profile: software
- Depends on: S-RETRO
- Inputs: all planning/implementation `lessons/` and `knowledge/`; proposed target `qualitycoding/knowledge`; `plan/GATES.md` G-003
- Actions: 1. Halt at G-003 and write `GATE-G-003.md` with IDs, titles, tags, target, and schema/secret evidence. 2. On approval copy entries into Appendix C layout, regenerate indexes, and push; retry rejected pushes up to three times with pull/index regeneration. 3. On `do-not-push`, retain branch entries and finish. 4. On persistent failure/no response create `knowledge-20261028T232935Z.bundle` and report it.
- Resumption (v3.6): before starting this step in any turn, run the turn-start checks — `git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <working-branch>` — confirm local HEAD equals the remote hash, restage the pinned runtime under `.runtime/` when missing, and resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`; on container loss restore the last remote-verified commit and rerun this step from its declared Inputs, never continuing from unverified local state.
- Persistence (v3.6 Rule 6): after this step turns green, commit the changed paths with a precise message, push to the working branch, verify the remote head with `git ls-remote` (local HEAD must equal the remote hash), and record the verified hash in `EXECUTION_LOG.md`; on mismatch stop and reconcile from committed state, never force-push.
- Outputs: `GATE-G-003.md`, knowledge-store commits/indexes or local bundle fallback
- Evidence produced: push/index result, explicit do-not-push result, or bundle path
- Done when: push and indexes succeed, do-not-push is recorded, or bundle fallback is written and reported; and the green commit was pushed and remote-verified with `git ls-remote` (local HEAD == remote HEAD), with the verified hash recorded in `EXECUTION_LOG.md`; and every path listed in Outputs exists, is non-empty where it is a file, passes `git diff --check`, and the evidence named in Evidence produced is recorded in `EXECUTION_LOG.md` with its validation result
- Checkpoint: record final L/K disposition and close the run
- On failure: never include secrets or force-push; follow the three-retry/bundle rule and preserve all local entries
- Gate: G-003
- Relevant decisions/claims: D-025, D-033
- Lessons applied: L-20261028T233100Z-git-auth-header; L-20261028T233130Z-private-knowledge-clone
- Exclusive resources: knowledge store; Git push credentials
