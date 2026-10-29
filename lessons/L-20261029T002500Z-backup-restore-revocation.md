---
id: L-20261029T002500Z-backup-restore-revocation
title: Restoring credential backups must not undo revocation
status: active
supersedes: []
recurrence_of: null
occurrences: 1
severity: Critical
tags: [tech:postgresql, phase:planning, kind:security]
recorded_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-29T00:25:00Z
---
## Trigger
A service stores rotating OAuth/GitHub credentials in PostgreSQL and supports encrypted backup restoration after users may have revoked access.
## What went wrong
The initial rollback runbook allowed an older backup to be restored without a mandatory credential invalidation step, so deleted credentials and connector grants could be resurrected.
## Correction
Made restoration fail closed: keep the connector stopped, delete every restored GitHub credential and connector grant, force reauthentication, bound backup retention, and rehearse that behavior in the rollback evidence.
## Prevention rule
Before opening OAuth or MCP traffic after any database restore, invalidate all restored credential generations and connector grants and prove that pre-restore tokens cannot authenticate.
## Detection check
The T-027 rollback/restore evidence shows a pre-backup connector token rejected and a GitHub reauthentication requirement after restoration, before readiness is declared.
## Evidence
`plan/OPERATIONS.md`, S-014, and R-001. No secrets.
