---
id: L-20261029T002530Z-premortem-evidence-specificity
title: Security and performance controls need scenario-specific acceptance evidence
status: active
supersedes: []
recurrence_of: null
occurrences: 5
severity: High
tags: [tech:nodejs, phase:verification, kind:wrong-assumption]
recorded_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-29T00:25:30Z
---
## Trigger
A plan names a control such as consent, bounded storage, image pinning, webhook verification, or benchmarking but leaves its hostile scenario or workload shape implicit.
## What went wrong
The first plan did not explicitly bind consent to a browser transaction/CSRF token, cap DCR/OAuth storage, lock container base-image digests, exercise signed webhooks through Caddy, or define a maximum-payload performance mix. The test-harness configuration defaults were also implicit.
## Correction
Added those controls and their exact acceptance evidence to existing decisions and steps mapped to T-004, T-021, T-023, T-025, T-026, and T-027; no frozen test was changed.
## Prevention rule
For every named security, deployment, or performance control, predeclare the hostile input or maximum workload, the exact boundary enforced, and the existing frozen test or review artifact that proves it.
## Detection check
The cold-read trace and second pre-mortem show each control linked to a test/evidence row, and benchmark raw output includes the declared per-tool workload rather than an unspecified average.
## Evidence
R-002 through R-006 and R-014; `plan/DECISIONS.md`; `plan/PLAN.md`. No secrets.
