# Amendment v3.6 execution log

One entry per step attempt: UTC time, step ID, attempt, pass/fail/blocked, commit hash, note.
The amendment plan itself is preserved at `plan/amendment-v36/AMENDMENT_V36_PLAN.md`.

## 2026-10-30T20:50:35Z — S-AMEND-000 — attempt 1 — pass

- Baseline verified: local HEAD `f4305b019fb898d5f941a812196a14f7ffc69c00` ==
  `git ls-remote origin refs/heads/gen-20261028T232935Z-kimi-github-app-connector`.
- Note: prior sandbox lost; repository re-cloned into the durable path
  `/mnt/agents/output/kimi-code-github-app`. environment_class=ephemeral recorded in
  `plan/amendment-v36/ENVIRONMENT_PROBE.md`; runner facts observed (Linux x86_64, 2 vCPU,
  4 GiB, fuse.portal, Git 2.39.5, Python 3.12.12) and recorded.
- Old mechanical suite (validates v3.4-era checks only, not v3.6 compliance):
  `python3 research/spikes/verify_planning.py` → exit 0
  ("all mechanical checks valid: 24 steps, 30 tests, 23 claims, 32 L/K entries");
  `sha256sum -c tests/FROZEN_MANIFEST.sha256` → exit 0 (6/6 OK).
- Deviation D-AMEND-001 recorded (human-directed PAT authentication for this run).
- Next step: S-AMEND-001.

## 2026-10-30T20:56:00Z — S-AMEND-001 — attempt 1 — pass

- Added D-034 to `plan/DECISIONS.md`: protocol v3.6 requires a plan-only amendment;
  connector architecture unchanged; amendment environment conservatively classified
  `ephemeral`.
- `plan/PROFILE.md` now records `environment_class: ephemeral`, the probe evidence path
  `plan/amendment-v36/ENVIRONMENT_PROBE.md`, and the applicable `[ephemeral]` protections.
- `.checkpoints/state.json`: stale pending item `external-generation-branch-push-requires-authentication`
  removed; verified remote head `8068f965135ffefc0094ce25ce50dce0395a8efd` recorded;
  active step set to `S-AMEND-002`; artifact hashes refreshed for changed files.
- Next step: S-AMEND-002.

## 2026-10-30T21:26:00Z — S-AMEND-002 — attempt 1 — pass (with blocked-unverified items)

- Created `research/spikes/v36-command-verification/README.md` and `output.txt`: full
  command/pin evidence matrix for every literal command and pinned version in
  `plan/PLAN.md` and `plan/ENVIRONMENT.md`.
- VERIFIED: Node archive SHA-256 exact match against nodejs.org SHASUMS256; Docker Engine
  29.9.2 (docs.docker.com); Docker Compose 5.6.1 (GitHub release 2026-10-21); Caddy 2.11.7;
  PostgreSQL 18.6; Kimi Code CLI 2.3.3 (npm `@moonshot-ai/kimi-code`); container tags
  `caddy:2.11.7-alpine` and `postgres:18.6-trixie` (official-images manifest, amd64,
  GitCommits recorded).
- BLOCKED-UNVERIFIED: `node:24.22.1-trixie-slim` exact-tag existence (Docker Hub registry
  unreachable from this sandbox; tag superseded by 24.22.2 in the current supported
  manifest; upstream Node v24.22.1 release itself verified). Immutable image digests and
  `kimi web --help` require the S-000 implementation host.
- Runner class defined and recorded: `linux-x86_64-2vCPU-4GiB-fuse.portal`; benchmark
  evidence is runner-class-specific.
- `plan/ENVIRONMENT.md` updated with the evidence matrix and runner class.
- Consequence recorded in the spike and `plan/ENVIRONMENT.md`: the final connector plan
  status must remain `BLOCKED — HUMAN DECISION REQUIRED` under v3.6 until S-000 resolves
  the node tag on the implementation host.
- Next step: S-AMEND-003.
