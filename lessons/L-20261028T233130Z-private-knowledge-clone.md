---
id: L-20261028T233130Z-private-knowledge-clone
title: Private knowledge store requires authenticated clone
status: active
supersedes: []
recurrence_of: null
occurrences: 1
severity: Low
tags: [tech:github, phase:research, kind:permissions]
recorded_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-28T23:31:30Z
---
## Trigger
A knowledge-store API read succeeds with authentication but an unauthenticated Git clone requests credentials.
## What went wrong
The initial clone treated the knowledge store as public without checking repository visibility.
## Correction
Retry the clone using the same ephemeral Git credential helper already verified for the target repository.
## Prevention rule
Check repository visibility before choosing authenticated or anonymous clone commands; default to ephemeral authentication for private stores.
## Detection check
`git clone` exits 0 and `git rev-parse HEAD` prints the store commit.
## Evidence
GitHub API confirmed read access to `qualitycoding/knowledge`; anonymous clone failed. No credential values retained.
