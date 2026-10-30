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
