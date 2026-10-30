# Pre-mortem round 3 — protocol v3.6 amendment

Date: 2026-10-30 UTC.
Context: fresh-context spawning remains unavailable; this is a structured adversarial
re-simulation by the amending context, not an independent model review (R-007).
Scope: the amendment changed persistence (Global Rule 6), ephemeral execution,
command/pin verification, artifact postconditions, deviation logging, and the mechanical
verifier. The connector architecture and frozen tests are unchanged.

## Incident report

It is six months after the amended plan entered implementation. The implementation host
lost power mid-step; the executor resumed from `.checkpoints/state.json` plus
`EXECUTION_LOG.md`, restored the last remote-verified commit, and reran only the
interrupted step from its declared Inputs. No unverified local state was continued and no
force-push occurred, so no evidence fork exists. Every green step was committed, pushed,
and `ls-remote`-verified, and the verified hashes in `EXECUTION_LOG.md` match the remote
history; the deviation-diff at S-RETRO compared `DEVIATIONS.md` against the baseline diff
and commit log and found zero unlogged substitutions.

## Lens examination (amendment-specific)

- **Persistence (H-01/M-01):** a step cannot silently pass locally: `Done when` now
  requires the pushed, remote-verified commit hash in `EXECUTION_LOG.md`. A stale or
  unverifiable checkpoint fails the mechanical verifier, not just the executor's judgment.
- **Ephemeral execution (H-02):** treating the sandbox as stable would strand state in a
  dead container. The conservative `ephemeral` classification, durable-mount rule, and
  restaging commands keep every required artifact inside the repository; misclassification
  is now a register risk (R-017) with an explicit probe requirement.
- **Command/pin verification (H-03/H-04):** the matrix records evidence class per pin.
  One item — `node:24.22.1-trixie-slim` exact-tag existence — is honestly
  `blocked-unverified` from the amendment sandbox, and the plan status is
  `BLOCKED — HUMAN DECISION REQUIRED` rather than claiming a verification that did not
  happen. At S-000 the implementation host either resolves the exact tag digest (unblocking
  via a recorded evidence update) or blocks and the human decides on a formal re-pin.
  Benchmark evidence is runner-class-specific (`linux-x86_64-2vCPU-4GiB-fuse.portal`), so
  numbers from a differently shaped host cannot silently satisfy D-021.
- **Artifact postconditions (C-01):** universal existence/non-empty/`git diff --check`
  clauses plus 17 specific evidence postconditions make "step green" mechanically
  falsifiable. Residual risk: presence is mechanical, semantic correctness of evidence is
  still an implementation-time obligation (R-018).
- **Deviation logging (M-02/M-03):** substitutions must be logged at the moment they are
  made, and S-RETRO's deviation-diff fails on any unlogged substitution, closing the
  batch-later loophole.
- **Verifier integrity (M-04):** the verifier enforces v3.6 mechanically, scans
  plan-specified commands for failure-swallowing idioms, and computes counts dynamically;
  weakening a check to force a pass would itself be caught by review of the diff.

## New risks

| ID | Failure mode | Severity | Disposition |
|---|---|---|---|
| R-016 | The pinned `node:24.22.1-trixie-slim` tag no longer exists on the registry when S-000 resolves digests | High | **Mitigated:** plan status is BLOCKED — HUMAN DECISION REQUIRED until S-000 proves the exact tag with `docker buildx imagetools inspect`; per D-019 an unavailable tag blocks and a re-pin requires the formal deviation path with full re-verification, never a silent float. |
| R-017 | The execution environment is misclassified (stable treated as ephemeral or vice versa), losing state or over-blocking | Medium | **Mitigated:** S-000 re-probes the environment class and records evidence in `ENVIRONMENT_VERIFICATION.md`; durable-mount and restaging rules apply under `ephemeral`; the probe evidence path is referenced from `plan/PROFILE.md`. |
| R-018 | Artifact postconditions are satisfied mechanically but the recorded evidence is semantically wrong or vacuous | Medium | **Open residual:** the mechanical verifier checks existence, non-emptiness, and naming; semantic correctness of evidence remains an implementation-time review obligation at S-REVIEW and gate G-002. |

## Convergence

Zero unresolved Critical/High risks. Round 3 adds R-016 (High, mitigated by the BLOCKED
status and the S-000 gate), R-017 (Medium), and R-018 (Medium). All amendment findings
C-01, H-01…H-04, M-01…M-05 are closed by plan edits with evidence under
`plan/amendment-v36/`; the single blocked-unverified pin is a human-decision item, not a
hidden gap.
