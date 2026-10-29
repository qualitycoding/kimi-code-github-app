---
id: L-20261029T002439Z-artifact-id-boundaries
title: Artifact-ID scans must not match identifiers embedded in technical terms
status: active
supersedes: []
recurrence_of: null
occurrences: 1
severity: Low
tags: [tech:python, phase:verification, kind:tooling]
recorded_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-29T00:24:39Z
---
## Trigger
A mechanical cold-read scans prose and code for artifact IDs such as `A-###` and `S-###`, including text that also contains cryptographic names or other hyphenated technical terms.
## What went wrong
The first reference regex interpreted the `A-256` in `AES-256` as an assumption ID and the `S-256` in `HMAC-SHA256` as a step ID, producing undefined-reference failures rather than checking actual plan defects.
## Correction
Added an ASCII uppercase-letter/digit negative lookbehind to artifact-reference expressions while leaving the actual assumption, decision, and step definitions unchanged.
## Prevention rule
Bound generated artifact-ID search patterns so a reference cannot begin inside a longer uppercase alphanumeric technical token, and test the checker against cryptographic names before treating its output as a plan defect.
## Detection check
`python3 research/spikes/verify_planning.py` reports neither `A-256` nor `S-256` while still detecting genuinely undefined `A-###` and `S-###` references.
## Evidence
`research/spikes/verify_planning.py`; initial cold-read output contained false `A-256` and `S-256` findings. No secrets.
