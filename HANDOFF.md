# Kimi–GitHub connector implementation handoff

## Purpose and profiles

Build a read-only GitHub App connector for Kimi Code CLI and `kimi web`: users install the App on personal/organization accounts, select all or some repositories, complete browser OAuth without managing a PAT, and use three live repository-read MCP tools. A thin Kimi plugin points to a hosted OAuth/MCP backend. Production/public release is separately gated.

Active profiles: `software`; `software.deploys=true`. Math, computational, publication, figures, and manuscript sections are N/A.

## Reading order

1. `plan/PROFILE.md` and `plan/ASSUMPTIONS.md`
2. This document, then `plan/ENVIRONMENT.md`
3. `plan/DECISIONS.md` and `src/contracts.ts` / `src/index.ts`
4. `plan/TRACEABILITY.md` and the frozen tests
5. `plan/PLAN.md`
6. `plan/GATES.md` and `plan/OPERATIONS.md`
7. `research/claims.json`, round logs, spikes, and `research/PRIOR_KNOWLEDGE.md`
8. `premortem/RISK_REGISTER.md` and `premortem/ASSUMPTION_AUDIT.md`

## Setup and frozen suite

Create the implementation branch only through S-000. Run the literal setup in `plan/ENVIRONMENT.md`; it installs the checksum-verified Node runtime and exact lockfile. Required implementation-time inputs are named there and in S-000: test GitHub App/user/repositories, staging origin/host, alert target, production inputs at G-002, and both Kimi 2.3.3 surfaces. Secrets come from the execution environment, never chat, Git, plugin manifests, logs, or knowledge items.

```sh
npm ci --ignore-scripts --no-audit --no-fund
npm run typecheck
sha256sum -c tests/FROZEN_MANIFEST.sha256
npm test
npm audit --omit=dev
npm run test:mutation
```

At handoff the suite is intentionally red: 30 tests, six files, all reaching `NOT_IMPLEMENTED` stubs. See `tests/RED_VERIFICATION.txt`. Implementation replaces stubs and adds production code but never edits, skips, marks expected-failure, or weakens frozen tests. A necessary test change follows `TEST_CHALLENGE.md` and the amendment path in `plan/TRACEABILITY.md`.

## Step list at a glance

- S-000: implementation branch, environment, access, execution log
- S-001…S-010: configuration/persistence, crypto, CIMD/DCR, OAuth, token authentication, GitHub reads, MCP, lifecycle, plugin/docs
- S-011…S-015: operational verification, performance, CI/supply chain, staging rollback/alerts, live GitHub/Kimi compatibility
- S-REVIEW, S-ADVERSARIAL, S-MUTATE: independent review, attack review, mutation score ≥85%
- S-017: unreleased candidate and evidence bundle
- S-018: G-002, then approved production/public 0.1.0 release only
- S-019: post-release verification and handover
- S-RETRO then S-KNOW: retrospective and G-003 knowledge disposition

A step starts only after every dependency passes. Independent steps may run concurrently only when fresh agents exist and their exclusive resources do not overlap. While halted at a gate, independent non-external steps may continue; production, public release, and knowledge push may not.

## Human gates

- **G-002 / S-018:** approve or reject production deployment/public release after reviewing the complete evidence bundle. Responses: `proceed`, `proceed-with-rescope: <text>`, `stop`.
- **G-003 / S-KNOW:** approve the knowledge push target or decline it. Responses: `push-to-proposed`, `push-to: <target>`, `do-not-push`.

Write the gate record before waiting. Do not infer approval from silence.

## Halt, deviation, and review protocol

The default is D-033: choose the most reversible non-scope-expanding option and log it in `DEVIATIONS.md`, except for frozen tests, security, data integrity, public interfaces, research integrity, or evidence class; those require `BLOCKED.md`. Operational forks follow D-026…D-032 and `plan/OPERATIONS.md`.

S-REVIEW, S-ADVERSARIAL, and S-RETRO require fresh-context agents that authored none of the reviewed work. The planner had no subagent/model-tier tool, so its mechanical reviews are not represented as independent semantic reviews. If fresh contexts remain unavailable during implementation, record the limitation and keep G-002 unsatisfied.

`EXECUTION_LOG.md` starts in S-000 and receives one line per step attempt: UTC time, step ID, attempt, pass/fail/blocked, commit hash, and short note. Corrections create lessons before work continues. New subject facts create knowledge items before work continues.

## Ephemeral execution

The execution environment is classified `environment_class=ephemeral` (probe: `plan/amendment-v36/ENVIRONMENT_PROBE.md` for the amendment run; the implementation run re-probes in S-000). Any container may disappear at a turn boundary. Therefore:

- **Durable mount.** All durable state lives inside the repository working tree at the recorded durable path; nothing required may be kept only in `/tmp` (`/tmp` is for disposable caches only).
- **Turn-start restaging.** At the start of every step or resumed turn, run the branch/remote checks (`git status --short --branch`, `git rev-parse HEAD`, `git ls-remote origin <branch>`); local HEAD and the remote hash must match before work continues. Restage the pinned Node runtime under the repo-local ignored `.runtime/` directory per `plan/ENVIRONMENT.md` when missing, and re-run `plan/ENVIRONMENT.md` setup when the runtime archive is absent (recording the substitution in `DEVIATIONS.md`).
- **One-step chunking.** One step is one resumable chunk; never leave a step half-finished without recording the exact next action in `.checkpoints/state.json` and `EXECUTION_LOG.md`.
- **Resume rule.** Resume only from `.checkpoints/state.json` plus `EXECUTION_LOG.md`, never from unrecorded local state.
- **On container loss.** Restore the last remote-verified commit (re-clone or reset to the recorded remote head), rerun the current step from its declared inputs, and never continue from unverified local state; never force-push.

## Integrity and persistence rules

Protocol v3.6 persistence rule (Global Rule 6), restated:

> **Persistence** `[All]`: After every step turns green, after every amendment round, after
> every review record, and after every gate record: commit the changed paths with a precise
> message, push to the working branch, verify the remote head with `git ls-remote`, and
> record the verified hash in `EXECUTION_LOG.md`. If local HEAD and the remote branch hash
> differ, stop and reconcile from committed state; never force-push. If push fails
> transiently, retry up to three times with 5, 15, and 45 second delays, then retry once
> with `git -c http.version=HTTP/1.1 push`. If authentication remains unavailable, do not
> request or reuse a pasted PAT: write a Git bundle under the durable output path, record
> the path, and report the mismatch as blocked. A locally blocked verification is never
> marked completed. Every connector step in `plan/PLAN.md` carries this as an explicit
> `Persistence (v3.6 Rule 6)` action and a remote-HEAD verification clause in its
> `Done when`.

Rule 9, restated verbatim:

> **Integrity** `[All]`: No step may fabricate, cherry-pick without disclosure, or manually alter data, test results, benchmarks, or figures. In addition:
> * `[computational, publication]` Every reported number is generated from committed results, not transcribed by hand.
> * `[publication]` Generative-AI images are never used as data figures. AI assistance is disclosed according to the venue's policy, as recorded in `plan/ASSUMPTIONS.md`.

Rule 11, restated verbatim:

> **Lessons** `[All]`: Whenever the executing agent corrects its own execution, it records a lesson before continuing. The *executing agent* is the planning agent while it runs this protocol, and the implementing agent while it runs the plan. A *correction* is any of:
> * redoing or reverting something the agent did;
> * a command, assumption, or edit that failed and was fixed by taking a different approach;
> * a check (test, cold read, proof review, pre-mortem, CI) that caught the agent's own mistake;
> * a correction from the human.
>
> Retrying the same action after a transient failure is not a correction, and neither is a failure the protocol plans for (such as tests failing red against stubs).
> * Each lesson is one file, `lessons/L-<YYYYMMDDTHHMMSSZ>-<slug>.md`, on the working branch, using the template in Appendix A. It is committed before work continues.
> * A lesson carries the *identifying information* that lets a future agent recognise the situation before repeating the mistake: the trigger (the circumstances and observable signals), the mistake, the correction, a prevention rule written as one imperative, checkable instruction, and a detection check.
> * Every lesson is classified with tags from the store taxonomy (Appendix C), so lessons can be read as a group: for example, all `tech:java` lessons, or all `domain:audio` lessons.
> * If the mistake repeats a lesson loaded in R0, the new lesson names it in `recurrence_of` and strengthens its prevention rule; a recurrence means the earlier rule did not work.
> * If the same mistake recurs within the run, increase `occurrences` on the run's existing lesson and add the new evidence, instead of writing a second file.

Rule 12, restated verbatim:

> **Knowledge Base** `[All]`: All supporting research and derived knowledge is recorded as knowledge items, so later work can reuse it instead of researching it again. Whenever either agent discovers a new fact about the task's Subject (its technologies, formats, APIs, platforms, tools, mathematical objects, or venues), it adds an item before continuing.
> * Each item is one file, `knowledge/K-<YYYYMMDDTHHMMSSZ>-<slug>.md`, on the working branch, using the template in Appendix B. It records the fact, its source and locator, the version it applies to, its confidence, and the claim it derives from (`C-###`), if any.
> * Every item is classified with tags from the store taxonomy (Appendix C), including at least one `subject:` tag, so it can be found again.
> * A fact that turns out wrong or outdated is never edited away: a new item `supersedes` it, so the history remains.

Rule 13, restated verbatim:

> **Knowledge Store** `[All]`: Lessons and knowledge items persist across tasks in the knowledge store recorded at intake (`A-###`; layout in Appendix C). The store is read at the start of research (R0) and written only at the end of implementation, after gate `G-003` (3.7.2). During a run, new lessons and items accumulate on the working branch. Lessons and items must never contain credentials, tokens, secrets, or personal data; redact them (for example, `github_pat_***`).

During implementation, new entries go in root `lessons/` and `knowledge/` on the implementation branch. Only S-KNOW copies them to the approved store after G-003. Planning entries already on the generation branch travel with them.

## Operations

The monitoring, alert, backup, migration, rollback, recovery, maintenance, and post-release runbook is `plan/OPERATIONS.md`. Its rollback command is mandatory release evidence; do not improvise volume deletion or schema downgrade.
