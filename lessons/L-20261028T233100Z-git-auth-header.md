---
id: L-20261028T233100Z-git-auth-header
title: Bearer extraHeader did not authenticate Git smart HTTP
status: active
supersedes: []
recurrence_of: null
occurrences: 1
severity: Medium
tags: [tech:github, phase:verification, kind:tooling]
recorded_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-28T23:31:00Z
---
## Trigger
GitHub API bearer authentication succeeds but `git push` still requests a username when using only `http.extraHeader`.
## What went wrong
The first non-mutating push check assumed API and Git smart-HTTP authentication were interchangeable and failed before contacting the remote with usable Git credentials.
## Correction
Used Git's ephemeral credential-helper interface with the GitHub token as the password and repeated the dry-run successfully.
## Prevention rule
Verify Git smart-HTTP access with a non-mutating push through an ephemeral credential helper before relying on repository write access.
## Detection check
`git push --dry-run` exits 0 without writing a ref or printing a credential prompt.
## Evidence
Planning environment check on 2026-10-28; no credential values retained.
