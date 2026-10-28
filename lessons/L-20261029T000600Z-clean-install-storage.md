---
id: L-20261029T000600Z-clean-install-storage
title: Large clean npm installs can exceed short timeouts on persistent output storage
status: active
supersedes: []
recurrence_of: null
occurrences: 2
severity: Low
tags: [tech:npm, phase:verification, kind:environment]
recorded_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-29T00:06:00Z
---
## Trigger
A 400-plus-package clean install runs on the persistent output mount under a two-minute execution limit.
## What went wrong
Two `npm ci` attempts exceeded 115 seconds on the output mount, leaving partial dependency directories that required cleanup.
## Correction
Ran the identical committed-lockfile probe on local scratch storage; it completed in six seconds, then type-checking and the production audit passed. Removed the partial output-mount install.
## Prevention rule
Run large dependency verification on local scratch storage with a measured timeout, copy only lockfiles and evidence to persistent output, and clean partial installs before committing.
## Detection check
The clean probe exits 0, `git status` shows no `node_modules` content, and the output records the command duration or timeout.
## Evidence
`research/spikes/dependency/output.txt` records both the timeouts and the successful clean probe. No secrets.
