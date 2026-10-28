---
id: L-20261029T000500Z-third-party-typecheck
title: Strict application type-checking does not require checking third-party declaration internals
status: active
supersedes: []
recurrence_of: null
occurrences: 1
severity: Low
tags: [tech:typescript, phase:verification, kind:tooling]
recorded_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-29T00:05:00Z
---
## Trigger
A new dependency graph fails with declaration errors in optional database dialects or bundled packages when `skipLibCheck` is false.
## What went wrong
The first spike treated third-party declaration checking as part of application strictness. Drizzle's optional dialect declarations and a bundled Node type reference failed even though connector code did not import those dialects.
## Correction
Added the pinned Node types, retained `strict=true`, set `skipLibCheck=true`, and reran the import spike successfully. Do not suppress errors in application source.
## Prevention rule
For TypeScript application scaffolds, pin matching runtime types and verify application code with `strict=true`; isolate third-party declaration compatibility with `skipLibCheck=true` and record the choice.
## Detection check
`./node_modules/.bin/tsc -p tsconfig.json` exits 0 while `strict` remains true and `skipLibCheck` is explicitly true.
## Evidence
`research/spikes/dependency/tsconfig.json` and `research/spikes/dependency/output.txt`. No secrets.
