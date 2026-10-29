---
id: L-20261029T000700Z-artifact-consistency
title: Generated planning artifacts need a consistency pass before freeze and handoff
status: active
supersedes: []
recurrence_of: null
occurrences: 3
severity: Low
tags: [tech:typescript, phase:verification, kind:process]
recorded_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-29T00:07:00Z
---
## Trigger
Multiple generated stubs, fixtures, setup commands, and evidence notes are edited in separate passes before being frozen.
## What went wrong
The first stub contained an invalid method signature, a fixture described as 32 bytes was 31 bytes, and a spike note became stale after the final dependency update. The Kimi web preflight also initially checked only the base CLI version.
## Correction
Removed the invalid signature, corrected the fixture length before freezing, reran typecheck/red verification, updated the evidence note, and added an explicit `kimi web --help` preflight.
## Prevention rule
Before freezing or committing generated planning artifacts, run typecheck, fixture-length checks, freeze hashes, and a documentation/reference consistency pass after the last edit.
## Detection check
`tsc` exits 0, all red failures are NOT_IMPLEMENTED, `sha256sum -c tests/FROZEN_MANIFEST.sha256` passes, and the final preflight names both Kimi surfaces.
## Evidence
`tests/RED_VERIFICATION.txt`, `plan/ENVIRONMENT.md`, and `research/spikes/dependency/output.txt`. No secrets.
