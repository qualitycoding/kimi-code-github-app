# v3.6 command/pin verification spike

Run: 2026-10-30T21:20:00Z (UTC), amendment step S-AMEND-002.
Purpose: close finding H-03 (incomplete command and pinned-version verification evidence)
and finding H-04 (missing performance runner class).

Environment limitation: this sandbox has no Docker daemon and cannot reach
`registry-1.docker.io` / `auth.docker.io` / `hub.docker.com` (connection reset/timeout from
this network). Where registry metadata was unreachable, the official-image library manifest
(`docker-library/official-images`, master HEAD 2026-10-30T20:21:07Z — fetched via the
GitHub API with `Accept: application/vnd.github.raw+json`) was used as the pinned-version
official locator, and items that still could not be proven are marked `blocked-unverified`.

## Evidence classes used

- **planner-spike** — output produced during the original planning run (2026-10-28/29).
- **official-docs-locator** — pinned-version official documentation or official release metadata.
- **registry-metadata** — package/registry metadata lookup (npm, GitHub releases, nodejs.org dist).
- **official-images-manifest** — `docker-library/official-images` library file entry (tag list, architectures, GitCommit).
- **blocked-unverified** — cannot be proven from this environment; must be verified at implementation time (S-000) before any freeze claim.

## Command/pin evidence matrix

| Item | Planned pin / command | Evidence class | Result |
|---|---|---|---|
| Node.js runtime archive | `node-v24.22.1-linux-x64.tar.xz`, SHA-256 `6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6` | registry-metadata | VERIFIED — `https://nodejs.org/dist/v24.22.1/` returns 200 and `SHASUMS256.txt` line for `node-v24.22.1-linux-x64.tar.xz` exactly matches the planned checksum. |
| npm | 11.19.1 (bundled with Node 24.22.1) | planner-spike | Planner-verified (`test "$(npm --version)" = "11.19.1"` during planning); re-verification happens on runtime restaging. |
| TypeScript | 7.0.2 | planner-spike | `research/spikes/dependency/` clean-import and type-check passed at planning. |
| Vitest | 5.0.5 | planner-spike | 30-test red verification passed as a red suite at planning (`tests/RED_VERIFICATION.txt`). |
| Stryker core / Vitest runner | 10.1.1 / 10.1.1 | planner-spike | Registry engines verified at planning; mutation run itself is an implementation step (S-MUTATE). |
| Git | 2.39.5 | planner-spike + amendment probe | `git version 2.39.5` observed 2026-10-30T20:50:35Z. |
| Python | 3.12.12 | planner-spike + amendment probe | `python3 --version` = 3.12.12 observed 2026-10-30T20:50:35Z. |
| Ubuntu host | 24.04 LTS x86_64 | blocked-unverified | Implementation-time host preflight (S-000); no Ubuntu host exists in the planning/amendment sandbox. |
| Docker Engine | 29.9.2 | official-docs-locator | VERIFIED — `https://docs.docker.com/engine/release-notes/29/` lists 29.9.2 (2026-10-20). Local `docker version` check deferred to S-000 (no daemon here). |
| Docker Compose | 5.6.1 | registry-metadata | VERIFIED — `docker/compose` GitHub release `v5.6.1`, published 2026-10-21T07:54:18Z. |
| Caddy | 2.11.7 | official-docs-locator | VERIFIED — Caddy 2.11.7 is the current supported release (released 2026-10-03). |
| PostgreSQL | 18.6 | official-docs-locator | VERIFIED — PostgreSQL 18.6 release date 2026-08-13. |
| Kimi Code CLI and `kimi web` | 2.3.3 | registry-metadata | VERIFIED — npm package `@moonshot-ai/kimi-code` version `2.3.3` exists in the npm registry (latest is 2.4.1; the plan's compatibility target remains the pinned 2.3.3). |
| MCP authorization/transport | 2026-07-28 + legacy negotiated compatibility | planner-spike | Recorded from Kimi 2.3.3 surface research during planning; re-checked at S-015. |
| GitHub REST API version header | `X-GitHub-Api-Version: 2026-03-10` | planner-spike | Recorded from GitHub API version research during planning. |
| GitHub API origin | `https://api.github.com` only | registry-metadata | VERIFIED reachable from amendment sandbox (used for release metadata lookups). |
| `node:24.22.1-trixie-slim` | exact tag, linux/amd64 digest recorded at S-000 | blocked-unverified | Docker Hub registry unreachable from this sandbox. The current official-images manifest lists 24.22.2 as the supported 24.x patch (`24-trixie-slim, 24.22-trixie-slim, 24.22.2-trixie-slim, krypton-trixie-slim`), so the exact tag 24.22.1-trixie-slim is superseded and NOT in the supported manifest. Upstream Node v24.22.1 release itself is verified to exist (nodejs.org dist, checksum match). Tag existence + amd64 digest must be resolved with `docker buildx imagetools inspect` at S-000; if the exact tag is unavailable, S-000 blocks per D-019. |
| `caddy:2.11.7-alpine` | exact tag, linux/amd64 digest recorded at S-000 | official-images-manifest | VERIFIED — `Tags: 2.11.7-alpine, ...`, `Architectures: amd64, ...`, `GitCommit: 9234f5785658cae8129bfae366e196d0670468ac`, directory `2.11/alpine`. Digest resolution still recorded at S-000 per D-019. |
| `postgres:18.6-trixie` | exact tag, linux/amd64 digest recorded at S-000 | official-images-manifest | VERIFIED — `Tags: 18.6, 18, latest, 18.6-trixie, ...`, `Architectures: amd64, ...`, `GitCommit: e00e1bd34ec5c8a8e7ad89b273b3d42efaf6d5bc`, directory `18/trixie`. Digest resolution still recorded at S-000 per D-019. |
| `docker buildx imagetools inspect` | literal command | official-docs-locator | Command ships with Docker Engine 29.x / Buildx; executed at S-000 against the live daemon. Not runnable here (no daemon). |
| `kimi web --help` | literal command | blocked-unverified locally | No Kimi binary in the planning/amendment sandbox; executed at S-000 on the implementation host. npm registry metadata for the 2.3.3 package is verified above. |
| `npm ci --ignore-scripts --no-audit --no-fund` | literal command | planner-spike | Executed during planning (`research/spikes/dependency/`). |
| `npm run typecheck` | literal command | planner-spike | Passed during planning. |
| `sha256sum -c tests/FROZEN_MANIFEST.sha256` | literal command | planner-spike + amendment probe | Exit 0 at 2026-10-30T20:50:35Z (all six frozen files OK). |
| `npm audit --omit=dev` / `npm run test:mutation` | literal commands | planner-spike | Audit/mutation commands validated at planning; re-run at implementation gates. |

## Immutable digests

Registry digests (`image@sha256:...`) could not be recorded because the Docker Hub registry
is unreachable from this sandbox and no Docker daemon exists here. S-000 must resolve and
record the linux/amd64 digests for all three exact tags with
`docker buildx imagetools inspect` before any freeze; per D-019 an unavailable exact tag
blocks S-000 rather than permitting substitution. Note: `node:24.22.1-trixie-slim` is the
one tag whose existence is not yet proven anywhere (superseded in the supported manifest);
if it cannot be resolved at S-000, S-000 blocks and the human decides between re-pinning
(24.22.2 or later) through the formal deviation path or halting.

## Performance runner class

Benchmark runner class: `linux-x86_64-2vCPU-4GiB-fuse.portal`.

Basis: observed planner/amendment environment (Linux x86_64, 2 vCPU, 4 GiB RAM,
`/mnt/agents` on `fuse.portal`; see `plan/amendment-v36/ENVIRONMENT_PROBE.md`).

Rule: release benchmark evidence (S-012, T-025) is valid only when run on the same recorded
runner class, or on a later runner class explicitly approved in a decision entry; benchmark
targets are runner-class-specific and a different class requires a new recorded probe and
an explicit decision before its evidence can satisfy D-021.
