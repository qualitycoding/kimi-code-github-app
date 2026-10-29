# Pre-mortem round 1 — catastrophic connector failure

Date: 2026-10-29 UTC.
Context: structured same-context simulation because fresh-context Opus-or-higher spawning is unavailable. This is not represented as independent review; that limitation is R-007.

## Incident report

It is 2027-04-29, six months after the 0.1.0 release. A schema rollback requires restoration of an encrypted pre-migration backup. The restored database contains GitHub credentials and connector grants deleted after user revocations. Because the original runbook did not invalidate restored credential generations, previously revoked connector tokens work again. This is a Critical security failure, R-001.

The incident review finds contributing control failures. An attacker can submit a victim's consent in a different browser transaction because cookie/CSRF binding was implicit (R-003). Open DCR and OAuth starts can exhaust persistent storage despite request-body limits (R-005). Mutable container tags make an emergency rebuild differ from the reviewed image (R-006). Caddy is never exercised with signed webhooks, so proxy-specific raw-body behavior can disable revocation while direct tests remain green (R-004). The performance report passes an unspecified average workload while maximum trees/files exhaust memory (R-002). Finally, T-016's valid fixture omits fields that D-018 calls required; without explicit test-only defaults, an implementer must guess whether the frozen test or production configuration wins (R-014).

## Lens examination

- **Technical correctness:** live user∩installation reads and two independent truncation flags remain sound. Restore atomicity and fixture configuration were under-specified.
- **Dependency/supply-chain drift:** npm versions and integrity hashes are locked, but container base-image digests were not. Added R-006 and immutable digest resolution/use.
- **Invalid research assumptions:** no `single-source` or `inferred` claims exist. Corroborated documentation does not prove live compatibility; that remains implementation evidence, not a hidden pass.
- **Implementer misinterpretation:** consent session binding, storage caps, benchmark shape, and test-fixture defaults required judgment. The amended decisions/steps now pre-decide them.
- **Integrity:** an average-only benchmark could produce a misleading green result. D-021 now preserves every maximum-payload sample and per-tool result; no result may be discarded to pass.
- **Past lessons:** R0 loaded no active matching lessons. All seven reused knowledge entries in `research/PRIOR_KNOWLEDGE.md` remain applied; credential handling continues to forbid tokens in artifacts.
- **Scale/performance:** request-size caps alone did not bound DCR/transient rows or worst-case tree/object memory. Added D-005 quotas and D-021 maximum-payload waves.
- **Security:** backup restoration, consent CSRF/session fixation, registration abuse, and proxy webhook verification needed explicit controls. Added R-001/R-003/R-004/R-005 mitigations.
- **Operational/on-call:** restoration could undo revocation and a rollback could use an unreviewed base image. Restore now fails closed, forces reauthentication, and is rehearsed with alert/rollback evidence.

## Root causes and hardening

R-001 through R-006 and R-014 are entered in `RISK_REGISTER.md`. Mitigations amend D-004/D-005/D-016/D-019/D-020/D-021, S-000/S-001/S-003/S-004/S-006/S-012/S-013/S-014/S-017, and `plan/OPERATIONS.md`. All map to existing frozen tests or review evidence; no frozen test changed. `tests/FROZEN_MANIFEST.sha256` remains valid, and the post-change cold read reported only the then-missing pre-mortem/audit files.

Round 1 result: 1 Critical and 6 High risks found, all with committed plan mitigations. A second round is required.
