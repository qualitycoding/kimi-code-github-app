---
id: L-20261029T004636Z-final-push-preflight
title: Final push preflight must include remote and resumed-session authentication
status: active
supersedes: []
recurrence_of: null
occurrences: 1
severity: Medium
tags: [tech:github, phase:release, kind:permissions]
recorded_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-29T00:46:36Z
---
## Trigger
A planning run resumes in a new execution context after earlier pushes used an ephemeral credential helper, and the final phase assumes the remote and authentication still exist.
## What went wrong
The local checkout had no configured remote. After restoring the target URL, HTTPS had no reusable credential and the alternate SSH attempt had no authorized key, so the finalized commit could not be pushed.
## Correction
Restored the exact target remote, made the permitted alternate/retry attempts without exposing or recovering credentials, and used the protocol's local Git-bundle fallback after authentication remained unavailable.
## Prevention rule
Before the final planning commit, verify the target remote and run an authenticated `git ls-remote` with a non-secret ephemeral credential path; if either is unavailable, report the persistence limitation rather than claiming a push.
## Detection check
`git remote get-url origin` names the target and an authenticated `git ls-remote origin` exits 0 before a push is claimed; after fallback, `git bundle verify <bundle-path>` succeeds and the bundle lists the final generation-branch commit.
## Evidence
Final HTTPS/SSH push failures and the verified planning bundle. No credential was printed, stored, or embedded in the bundle metadata.
