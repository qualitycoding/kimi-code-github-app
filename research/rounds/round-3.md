# Research round 3 — empirical verification and saturation

Date: 2026-10-29 UTC.

## Probes

### Node runtime

Downloaded the official Linux x64 Node 24.22.1 archive and compared its SHA-256 with the official `SHASUMS256.txt` value. Both were `6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6`. The binary reported `v24.22.1`; bundled npm reported `11.19.1`.

### Exact package graph

The probe in `research/spikes/dependency/` pins the current MCP v2 server/adapters, Express, Octokit, Drizzle/PostgreSQL, validation, logging, security middleware, TypeScript, Vitest, Supertest, Autocannon, and Stryker. Results:

- Clean `npm ci` from the committed lockfile: passed.
- Import/compile probe under TypeScript 7.0.2, `strict=true`: passed.
- Production `npm audit --omit=dev`: 0 info/low/moderate/high/critical findings at probe time.
- Two output-mount installs timed out at 115 seconds; the identical clean probe on local scratch storage passed in six seconds. This is an environment observation, not a connector performance result.

C-013, C-019, and C-020 are empirically supported; C-020 is `verified`. The runtime/dependency claims do not establish live Kimi or GitHub interoperability.

## Deliberately unprobed external behavior

No live OAuth grant, private repository read, GitHub webhook, public deployment, or Kimi login was attempted. Those require the not-yet-implemented service and implementation-time credentials. They are frozen implementation tests and G-002 evidence, not planner claims.

## Saturation

This round produced no new load-bearing claim, confidence downgrade, or unresolved contradiction. It corrected only harness execution details, recorded as lessons. Research therefore saturates after three rounds (R1 architecture, R2 depth/adversarial, R3 empirical). All 20 claims end at `corroborated` or `verified`.

## Residual verification gap

Fresh-context model agents and selectable model tiers are unavailable. Mechanical checks can verify IDs, schemas, hashes, and references, but cannot substitute for independent semantic review. A-015 carries this as a Medium planning risk; implementation still requires fresh-context reviews when the required agent capability is available, otherwise G-002 must remain unsatisfied.
