# Environment and verified setup

## Verified planner baseline

| Component | Exact pin | Verification |
|---|---:|---|
| Linux ABI for the runtime archive | linux-x64 | Official archive executed |
| Node.js | 24.22.1 | Binary reports `v24.22.1` |
| npm | 11.19.1 | Bundled binary reports `11.19.1` |
| Node archive SHA-256 | `6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6` | Matches official `SHASUMS256.txt` |
| TypeScript | 7.0.2 | Clean import and planning-suite type-check passed |
| Vitest | 5.0.5 | 30-test red verification passed as a red suite |
| Stryker core / Vitest runner | 10.1.1 / 10.1.1 | Registry engines verified; mutation run is an implementation step |
| Git | 2.39.5 or newer compatible 2.x | Planner version 2.39.5 |
| Python for schema checks | 3.12.12 | Planner execution |

All npm production and development dependencies are exact-pinned in `package.json`; transitive versions and integrity hashes are locked in `package-lock.json`. `strict=true` applies to application source. `skipLibCheck=true` isolates optional third-party declaration internals and is not permission to suppress application errors.

## Literal setup commands

Run from the implementation-branch repository root on Linux x64. These commands were executed in scratch storage during planning; use local storage for the large clean install if a network filesystem is slow.

```sh
export RUNTIME_DIR="${RUNTIME_DIR:-$PWD/.runtime}"
mkdir -p "$RUNTIME_DIR"
curl -fSLo "$RUNTIME_DIR/node-v24.22.1-linux-x64.tar.xz" \
  https://nodejs.org/dist/v24.22.1/node-v24.22.1-linux-x64.tar.xz
echo "6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6  $RUNTIME_DIR/node-v24.22.1-linux-x64.tar.xz" | sha256sum -c -
mkdir -p "$RUNTIME_DIR/node24"
tar -xJf "$RUNTIME_DIR/node-v24.22.1-linux-x64.tar.xz" -C "$RUNTIME_DIR/node24" --strip-components=1
export PATH="$RUNTIME_DIR/node24/bin:$PATH"
test "$(node --version)" = "v24.22.1"
test "$(npm --version)" = "11.19.1"
npm ci --ignore-scripts --no-audit --no-fund
npm run typecheck
sha256sum -c tests/FROZEN_MANIFEST.sha256
```

`.runtime/` is local tooling only and must be ignored. Before implementation, `npm test` is expected to report 30 `NOT_IMPLEMENTED` failures; after implementation it must pass. Never edit frozen tests to make that transition.

## Implementation-time host and external compatibility pins

These are preflight requirements for S-000 and staging, not claims that the planner executed a deployment. The planner has no Docker daemon, Ubuntu host, public hostname, Kimi binary, or live GitHub App credentials.

| Component | Required pin |
|---|---:|
| Ubuntu | 24.04 LTS, x86_64 |
| Docker Engine | 29.9.2 |
| Docker Compose | 5.6.1 |
| Caddy | 2.11.7 |
| PostgreSQL | 18.6 |
| Kimi Code CLI and `kimi web` | 2.3.3 compatibility target |
| MCP authorization/transport | 2026-07-28 with legacy negotiated compatibility required by Kimi |
| GitHub REST API version header | `X-GitHub-Api-Version: 2026-03-10` |
| GitHub API origin | `https://api.github.com` only |
| Connector base image | official `node:24.22.1-trixie-slim`, linux/amd64 digest resolved and recorded in S-000 |
| Caddy image | official `caddy:2.11.7-alpine`, linux/amd64 digest resolved and recorded in S-000 |
| PostgreSQL image | official `postgres:18.6-trixie`, linux/amd64 digest resolved and recorded in S-000 |

All three container tags must be resolved to immutable `image@sha256:...` references with `docker buildx imagetools inspect`; an unavailable exact tag blocks S-000 rather than permitting substitution. Every Dockerfile, Compose file, scan, and release candidate uses the recorded digests.

S-000 must run and record:

```sh
docker version --format '{{.Server.Version}}'
docker compose version
caddy version
psql --version
kimi --version
kimi web --help
git --version
node --version
npm --version
```

Expected values are the pins above. If a patch differs, do not silently update the plan: record the candidate in `DEVIATIONS.md`, re-run the full frozen suite and dependency review, and obtain G-002 approval for any deployment-affecting change. A missing tool, daemon, hostname, credential, or supported Kimi surface blocks implementation delivery before feature work.

## Security and reproducibility commands

```sh
npm audit --omit=dev
npm run test:mutation
sha256sum -c tests/FROZEN_MANIFEST.sha256
```

Release requires zero Critical/High production-audit findings on the exact candidate, mutation score at least 85% in the selected modules, and a valid freeze manifest. Weekly automated alerts and monthly manual dependency review use this same lockfile as the comparison baseline.
