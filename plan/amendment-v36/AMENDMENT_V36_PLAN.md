# Protocol v3.6 amendment plan

Status: READY — amendment planning complete; no remediation has been executed.
Scope: amend the committed planning artifacts on the generation branch so the connector implementation plan satisfies planning protocol v3.6.
Baseline branch: `gen-20261028T232935Z-kimi-github-app-connector`
Baseline commit: `f4305b019fb898d5f941a812196a14f7ffc69c00`
Protocol reviewed: planning protocol v3.6, `qualitycoding/skills` commit `b361dab99ebc4de8a4dddd307085d12b998028d4`
Environment class for this amendment run: `ephemeral` by conservative Kimi-environment default. S-AMEND-000 records the probe and any contradictory evidence.

## Objective

Bring the existing connector plan from `READY` under protocol v3.4 to a truthful `READY` or `BLOCKED — HUMAN DECISION REQUIRED` status under protocol v3.6.

The amendment must close these findings:

1. C-01: missing artifact existence and content postconditions in most step `Done when` fields.
2. H-01: missing per-chunk commit, push, and `ls-remote` verification cadence.
3. H-02: missing environment-class and ephemeral-execution protections.
4. H-03: incomplete command and pinned-version verification evidence.
5. H-04: missing performance runner class.
6. M-01: stale checkpoint push state.
7. M-02: missing retrospective deviation-log diff verification.
8. M-03: substitutions not explicitly logged at the moment they are made.
9. M-04: mechanical verifier not enforcing protocol v3.6 requirements.
10. M-05: stale cold-read count and protocol version.

## Non-goals and prohibitions

- Do not implement connector features.
- Do not deploy, release, publish, or submit anything.
- Do not edit, skip, weaken, or delete frozen tests.
- Do not change the frozen-test manifest unless a separate formal frozen-test amendment is opened and red-verified.
- Do not use, store, print, commit, or request a GitHub PAT.
- Do not treat a locally blocked verification as completed.
- Do not mark the connector plan `READY` under v3.6 while any required verification remains unevidenced.

## Global execution rules

### Durable-mount and resumption rules

1. Treat this environment as ephemeral: any container may disappear at a turn boundary.
2. Keep all durable work inside `/mnt/agents/output/kimi-code-github-app`; never keep required state only in `/tmp`.
3. Keep staged tooling under the repository-local ignored `.runtime/` directory.
4. At the start of every step or resumed turn, run:

```sh
cd /mnt/agents/output/kimi-code-github-app
git status --short --branch
git rev-parse HEAD
git ls-remote origin refs/heads/gen-20261028T232935Z-kimi-github-app-connector
```

The local `HEAD` and remote branch hash must match before work continues. If they differ, stop and reconcile from committed state; never force-push.

5. Re-stage Node tooling when missing or wrong:

```sh
export RUNTIME_DIR="$PWD/.runtime"
mkdir -p "$RUNTIME_DIR/node24"
tar -xJf "$RUNTIME_DIR/node-v24.22.1-linux-x64.tar.xz" -C "$RUNTIME_DIR/node24" --strip-components=1
export PATH="$PWD/.runtime/node24/bin:$PATH"
test "$(node --version)" = "v24.22.1"
test "$(npm --version)" = "11.19.1"
```

If the runtime archive is absent, rerun the literal setup commands in `plan/ENVIRONMENT.md` and record that substitution in `DEVIATIONS.md`.

6. One step is one resumable chunk. Do not leave a step half-finished without recording the exact next action in `.checkpoints/state.json` and the amendment execution log.

### Push cadence

After every successful step, amendment round, review record, or gate record:

```sh
git status --short
git add <changed-paths>
git commit -m "<precise amendment message>"
git push origin gen-20261028T232935Z-kimi-github-app-connector
remote_head="$(git ls-remote origin refs/heads/gen-20261028T232935Z-kimi-github-app-connector | awk '{print $1}')"
test "$(git rev-parse HEAD)" = "$remote_head"
```

If push fails transiently, retry up to three times with 5, 15, and 45 second delays. On a flaky network, retry with HTTP/1.1:

```sh
git -c http.version=HTTP/1.1 push origin gen-20261028T232935Z-kimi-github-app-connector
```

If authentication remains unavailable, do not request or reuse a pasted PAT. Write a Git bundle under `/mnt/agents/output/`, record the path, and leave the plan blocked with the mismatch reported.

### Deviation rule

Every substitution to a version pin, package, command, timeout, config value, environment class, runner class, or artifact requirement must be appended to `DEVIATIONS.md` immediately. Each entry must contain:

- UTC timestamp;
- step ID;
- original planned value;
- substituted value;
- reason;
- validation command and result;
- commit hash after the substitution is committed.

## Completion definition

The amendment is complete only when all of the following are true:

1. Every amendment step is green.
2. Every step was committed, pushed, and verified with `ls-remote` at the time it turned green.
3. `research/spikes/verify_planning.py` enforces and passes the v3.6 checks.
4. `tests/FROZEN_MANIFEST.sha256` still matches all six frozen test files.
5. No GitHub token, PAT, private key, or connector credential appears in any artifact.
6. `.checkpoints/state.json` no longer claims the external generation-branch push is pending.
7. `plan/PLAN.md` has a truthful v3.6 status header: `READY` only if all required evidence exists, otherwise `BLOCKED — HUMAN DECISION REQUIRED`.
8. The remote branch head equals local `HEAD`.

## Steps

### S-AMEND-000 Environment probe and amendment baseline

- Tier: Haiku
- Profile: software; software.deploys
- Depends on: none
- Inputs: clean generation branch at `f4305b0`; current protocol v3.6 findings; durable repository path `/mnt/agents/output/kimi-code-github-app`
- Actions: 1. Run the global resumption checks and verify local `HEAD` equals `f4305b019fb898d5f941a812196a14f7ffc69c00`. 2. Create `plan/amendment-v36/` and the files `EXECUTION_LOG.md`, `DEVIATIONS.md`, and `ENVIRONMENT_PROBE.md`. 3. Record `environment_class=ephemeral`, the conservative-classification reason, the repository durable path, the non-durable `/tmp` warning, and the turn-start restaging rule. 4. Record the current runner facts: Linux x86_64, 2 vCPU, 4 GiB RAM, `/mnt/agents` on `fuse.portal`, Git 2.39.5, Python 3.12.12. 5. Run `python3 research/spikes/verify_planning.py` and `sha256sum -c tests/FROZEN_MANIFEST.sha256`; record that these validate the old mechanical suite, not v3.6 compliance. 6. Commit, push, and verify remote HEAD before continuing.
- Outputs: `plan/amendment-v36/EXECUTION_LOG.md`; `plan/amendment-v36/DEVIATIONS.md`; `plan/amendment-v36/ENVIRONMENT_PROBE.md`
- Evidence produced: branch/remote match, environment class, runner facts, old verifier result, freeze-manifest result
- Done when: all three files exist and are non-empty; `ENVIRONMENT_PROBE.md` contains `environment_class=ephemeral`, the durable path, the runner facts, and the restaging rule; the old verifier and freeze manifest pass; local `HEAD` equals the verified remote HEAD.
- Checkpoint: record step completion, commit, remote head, environment class, and next step `S-AMEND-001` in `.checkpoints/state.json` and the amendment execution log.
- On failure: write `plan/amendment-v36/BLOCKED.md`, stop, and do not substitute versions or credentials.
- Gate: none
- Relevant decisions/claims: protocol v3.6 finding H-02; the future amendment decision assigned by `plan/DECISIONS.md`
- Lessons applied: `L-20261029T002439Z-artifact-id-boundaries`; `L-20261029T004636Z-final-push-preflight`
- Exclusive resources: repository working tree; generation branch

### S-AMEND-001 Record the v3.6 amendment decision and profile applicability

- Tier: Haiku
- Profile: software; software.deploys
- Depends on: S-AMEND-000
- Inputs: `plan/PROFILE.md`; `plan/DECISIONS.md`; `.checkpoints/state.json`; `plan/amendment-v36/ENVIRONMENT_PROBE.md`
- Actions: 1. Add the next sequential decision to `plan/DECISIONS.md`, recording that protocol v3.6 requires a plan-only amendment, that the connector architecture remains unchanged, and that the amendment environment is conservatively classified `ephemeral`. 2. Update `plan/PROFILE.md` with `environment_class: ephemeral`, the probe evidence path, and the fact that `[ephemeral]` execution protections apply. 3. Update `.checkpoints/state.json`: add the environment class, remove the stale pending external-push item, record the verified remote head, and set the active step to `S-AMEND-002`. 4. Append the same state to the amendment execution log. 5. Commit, push, and verify remote HEAD.
- Outputs: updated `plan/DECISIONS.md`; updated `plan/PROFILE.md`; updated `.checkpoints/state.json`
- Evidence produced: the new decision text; profile environment fields; corrected checkpoint state
- Done when: the new decision exists and names protocol v3.6 and the unchanged connector scope; `plan/PROFILE.md` contains `environment_class: ephemeral` and an applicable `[ephemeral]` statement; `.checkpoints/state.json` no longer lists the generation-branch push as pending; all modified files pass `git diff --check`; the commit is pushed and remote-verified.
- Checkpoint: record the new decision ID, profile path, checkpoint path, commit, remote head, and next step.
- On failure: revert only the failed edit with `git restore --source=HEAD --staged --worktree <path>`; record the correction as a lesson if the edit was already committed; stop rather than leaving partial profile state.
- Gate: none
- Relevant decisions/claims: the amendment decision created in this step; findings H-02 and M-01
- Lessons applied: `L-20261029T000700Z-artifact-consistency`
- Exclusive resources: repository working tree; generation branch

### S-AMEND-002 Complete command/pin verification and define the runner class

- Tier: Sonnet
- Profile: software; software.deploys
- Depends on: S-AMEND-001
- Inputs: `plan/ENVIRONMENT.md`; `plan/PLAN.md`; `plan/amendment-v36/ENVIRONMENT_PROBE.md`
- Actions: 1. Create `research/spikes/v36-command-verification/README.md` and `output.txt`. 2. Build a command/pin evidence matrix covering every literal command in `plan/PLAN.md` and `plan/ENVIRONMENT.md`, including Docker Engine 29.9.2, Docker Compose 5.6.1, Caddy 2.11.7, PostgreSQL 18.6, Kimi Code CLI and `kimi web` 2.3.3, `docker buildx imagetools inspect`, `kimi web --help`, and the exact container tags `node:24.22.1-trixie-slim`, `caddy:2.11.7-alpine`, and `postgres:18.6-trixie`. 3. For each item record one of: planner spike output, pinned-version official documentation locator, registry metadata check, or `blocked-unverified`. 4. Verify exact container-tag existence before freeze through registry metadata or `docker buildx imagetools inspect`; record immutable digests when available. 5. Define the benchmark runner class as `linux-x86_64-2vCPU-4GiB-fuse.portal` for the observed planner environment, and state that release benchmark evidence is valid only when run on the same recorded class or a later explicitly approved runner class. 6. Update `plan/ENVIRONMENT.md` with the evidence matrix and runner class. 7. If Kimi or container-tag verification cannot be completed, keep the final connector status `BLOCKED — HUMAN DECISION REQUIRED`; do not represent it as verified. 8. Commit, push, and verify remote HEAD.
- Outputs: `research/spikes/v36-command-verification/README.md`; `research/spikes/v36-command-verification/output.txt`; updated `plan/ENVIRONMENT.md`
- Evidence produced: command/pin matrix; exact-tag existence results; runner-class definition; explicit blocked-unverified list if any
- Done when: every literal command and pinned version in `plan/PLAN.md` and `plan/ENVIRONMENT.md` has an evidence row; every container tag is either proven to exist with a recorded locator/digest or explicitly marked `blocked-unverified`; `plan/ENVIRONMENT.md` contains the exact runner class and the rule that benchmark targets are runner-class-specific; the spike files contain the same evidence; the commit is pushed and remote-verified.
- Checkpoint: record evidence paths, unverified items, commit, remote head, and next step.
- On failure: mark the affected pin `blocked-unverified`; do not substitute a newer version without a deviation entry and full validation; stop if the missing evidence prevents a truthful `READY` status.
- Gate: none
- Relevant decisions/claims: D-019; D-021; finding H-03; finding H-04
- Lessons applied: `L-20261029T000500Z-third-party-typecheck`; `L-20261029T000600Z-clean-install-storage`
- Exclusive resources: repository working tree; external documentation/network metadata

### S-AMEND-003 Add the v3.6 persistence protocol

- Tier: Sonnet
- Profile: software; software.deploys
- Depends on: S-AMEND-002
- Inputs: `HANDOFF.md`; `plan/PLAN.md`; protocol v3.6 Global Rule 6
- Actions: 1. Add a `Protocol v3.6 persistence rule` section to `HANDOFF.md` restating Global Rule 6, including commit and push after every green step, amendment round, review record, or gate record, followed by `ls-remote` verification and mismatch reporting. 2. Add the same rule to the opening execution rules of `plan/PLAN.md`. 3. Add one persistence action to every connector step in `plan/PLAN.md`: after the step turns green, commit, push, verify remote HEAD with `ls-remote`, and record the verified hash. 4. Add the same post-green persistence requirement to the `Done when` of every connector step. 5. Update `reviews/COLD_READ.md` only in a later review step; do not mark this step as a cold read. 6. Commit, push, and verify remote HEAD.
- Outputs: updated `HANDOFF.md`; updated `plan/PLAN.md`
- Evidence produced: Rule 6 text; step-by-step persistence additions; remote-verified commits
- Done when: `HANDOFF.md` contains the updated Rule 6 push cadence; `plan/PLAN.md` contains the global rule; every connector step has a post-green commit/push/`ls-remote` action; every connector step `Done when` includes remote-HEAD verification; the commit is pushed and remote-verified.
- Checkpoint: record changed file hashes, commit, remote head, and next step.
- On failure: stop; do not continue to artifact postconditions while persistence is unspecified.
- Gate: none
- Relevant decisions/claims: finding H-01; protocol v3.6 Global Rule 6
- Lessons applied: `L-20261029T004636Z-final-push-preflight`
- Exclusive resources: repository working tree; generation branch

### S-AMEND-004 Add artifact existence and content postconditions

- Tier: Sonnet
- Profile: software; software.deploys
- Depends on: S-AMEND-003
- Inputs: `plan/PLAN.md`; `HANDOFF.md`; finding C-01
- Actions: 1. Append this universal clause to every connector step `Done when`: `and every path listed in Outputs exists, is non-empty where it is a file, passes git diff --check, and the evidence named in Evidence produced is recorded in EXECUTION_LOG.md with its validation result`. 2. Add the following specific postconditions in addition to the universal clause:
  - `S-000`: `ENVIRONMENT_VERIFICATION.md`, `EXECUTION_LOG.md`, and `DEVIATIONS.md` each contain the environment class, remote head, and setup-check results.
  - `S-002`: token/crypto evidence records concurrent-refresh, replay, redaction, and fixed-clock results.
  - `S-003`: SSRF evidence records redirect-to-private and DNS-rebinding cases.
  - `S-004`: consent evidence records no pre-consent GitHub redirect and no GitHub token in browser or MCP output.
  - `S-005`: authentication evidence records wrong-resource and wrong-audience rejection.
  - `S-006`: gateway evidence records cross-tenant 404 behavior and refresh-generation protection.
  - `S-007`: read evidence distinguishes connector truncation from GitHub truncation and records memory-bound results.
  - `S-008`: MCP evidence records exactly three exposed tools and unauthenticated rejection.
  - `S-009`: lifecycle evidence records duplicate webhook delivery, revocation, and sweep behavior.
  - `S-010`: `kimi.plugin.json` and administrator/user documentation exist, validate, and contain no PAT or secret field.
  - `S-011`: the aggregate test log records all frozen tests with zero skips or expected failures.
  - `S-012`: the benchmark report contains five runs, aggregate and per-tool p95 values, error rate, peak memory, and variance.
  - `S-015`: the live compatibility report records the personal/organization and all/selected repository matrix.
  - `S-ADVERSARIAL`: `reviews/ADVERSARIAL_REVIEW.md` records every confirmed break and disposition.
  - `S-MUTATE`: `reviews/MUTATION.md` records the score and every survivor class or justification.
  - `S-019`: the post-release report records the 60-minute checks, alert result, and revocation result.
  - `S-RETRO`: the retrospective artifact records every finding, its L/K links, and the deviation-diff result. 3. Update the `Outputs` or `Evidence produced` fields when a required artifact path is currently ambiguous; do not weaken the test criteria. 4. Commit after each contiguous group of step edits, push, and verify remote HEAD.
- Outputs: updated `plan/PLAN.md`; possibly updated `HANDOFF.md` wording referencing artifact postconditions
- Evidence produced: updated step fields; verifier-ready artifact-postcondition markers
- Done when: all 24 connector steps contain the universal artifact clause; all listed specific postconditions are present in the corresponding `Done when` fields; no test criterion was weakened; every commit in this step is pushed and remote-verified.
- Checkpoint: record modified step IDs, commit list, remote head, and next step.
- On failure: restore the affected step block from `HEAD` and reapply only that block; record a lesson if the same edit fails twice.
- Gate: none
- Relevant decisions/claims: finding C-01; Rule 14
- Lessons applied: `L-20261029T002530Z-premortem-evidence-specificity`
- Exclusive resources: repository working tree

### S-AMEND-005 Encode ephemeral execution and resumability

- Tier: Sonnet
- Profile: software; software.deploys
- Depends on: S-AMEND-004
- Inputs: `plan/PROFILE.md`; `plan/ENVIRONMENT.md`; `HANDOFF.md`; `plan/PLAN.md`
- Actions: 1. Add an `Ephemeral execution` section to `HANDOFF.md` containing the durable-mount rule, the turn-start restaging commands, runtime re-staging commands, one-step chunking, and the requirement to resume from `.checkpoints/state.json` plus `EXECUTION_LOG.md`. 2. Extend connector `S-000` with the same environment probe, durable mount, restaging, and blocked-tool checks. 3. Add a pre-action to every connector step requiring the turn-start branch/remote/runtime checks. 4. Add an `On container loss` rule: restore the last remote-verified commit, rerun the current step from its declared inputs, and never continue from unverified local state. 5. Keep `/tmp` usable only for disposable caches; required evidence must be written under the repository durable path. 6. Commit, push, and verify remote HEAD.
- Outputs: updated `HANDOFF.md`; updated `plan/PLAN.md`; possibly updated `plan/ENVIRONMENT.md`
- Evidence produced: ephemeral rules; S-000 probe/restaging additions; per-step turn-start checks
- Done when: `HANDOFF.md` contains all ephemeral rules; connector `S-000` records the environment class and restaging procedure; every connector step contains a turn-start resumption check; the container-loss rule exists; no required state is stored only in `/tmp`; the commit is pushed and remote-verified.
- Checkpoint: record changed paths, commit, remote head, and next step.
- On failure: stop; do not classify the environment as stable without probe evidence.
- Gate: none
- Relevant decisions/claims: the amendment decision created in S-AMEND-001; finding H-02
- Lessons applied: `L-20261029T000600Z-clean-install-storage`; `L-20261029T004636Z-final-push-preflight`
- Exclusive resources: repository working tree

### S-AMEND-006 Strengthen deviation logging and retrospective verification

- Tier: Sonnet
- Profile: software; software.deploys
- Depends on: S-AMEND-005
- Inputs: `HANDOFF.md`; `plan/PLAN.md`; `plan/ENVIRONMENT.md`
- Actions: 1. Update the deviation rule in `HANDOFF.md` to require every substitution to be logged at the moment it is made. 2. Update `S-000` and any step capable of changing pins, packages, commands, timeouts, config values, environment class, or runner class with an explicit `Append DEVIATIONS.md before continuing` action. 3. Update `S-RETRO` with a deviation-diff procedure: compare `DEVIATIONS.md` against `git diff --stat <baseline>..HEAD`, `git log --oneline --name-only <baseline>..HEAD`, package changes, pin changes, timeout changes, and config changes; fail if any actual substitution is unlogged. 4. Require `S-RETRO` to produce `reviews/RETRO_DEVIATION_DIFF.md`. 5. Commit, push, and verify remote HEAD.
- Outputs: updated `HANDOFF.md`; updated `plan/PLAN.md`; `reviews/RETRO_DEVIATION_DIFF.md` required as future S-RETRO output
- Evidence produced: immediate-logging rule; S-RETRO diff procedure; future retrospective artifact requirement
- Done when: the immediate-deviation rule exists; every substitution-capable step has an explicit deviation action; `S-RETRO` requires `reviews/RETRO_DEVIATION_DIFF.md`; the S-RETRO `Done when` includes a successful deviation-diff result; the commit is pushed and remote-verified.
- Checkpoint: record changed paths, commit, remote head, and next step.
- On failure: stop; do not allow retrospective verification to remain informal.
- Gate: none
- Relevant decisions/claims: D-033; findings M-02 and M-03
- Lessons applied: `L-20261029T002530Z-premortem-evidence-specificity`
- Exclusive resources: repository working tree

### S-AMEND-007 Extend the mechanical verifier for v3.6

- Tier: Sonnet
- Profile: software
- Depends on: S-AMEND-006
- Inputs: `research/spikes/verify_planning.py`; amended `plan/` and `HANDOFF.md`
- Actions: 1. Extend the verifier to require an environment class of `stable` or `ephemeral` in both `plan/PROFILE.md` and `.checkpoints/state.json`. 2. Require the v3.6 Rule 6 cadence text in `HANDOFF.md` and `plan/PLAN.md`, a post-green push/`ls-remote` action in every connector step, and remote-HEAD verification in every connector `Done when`. 3. Require the universal artifact-postcondition clause in every connector `Done when` and the specific postcondition markers added in S-AMEND-004. 4. Require the command/pin matrix, runner class, and either evidence or `blocked-unverified` for every implementation-time pin. 5. Require the ephemeral restaging and container-loss rules when `environment_class=ephemeral`. 6. Require `S-RETRO` to name `reviews/RETRO_DEVIATION_DIFF.md` and the deviation-diff procedure. 7. Update the L/K count dynamically instead of hard-coding 31 or 32. 8. Add a scan for failure-swallowing idioms in all plan-specified commands. 9. Run the verifier; it must pass before the next step. 10. Commit, push, and verify remote HEAD.
- Outputs: updated `research/spikes/verify_planning.py`; verifier output recorded under `plan/amendment-v36/`
- Evidence produced: v3.6 verifier implementation and passing output
- Done when: the verifier contains checks for all findings C-01, H-01, H-02, H-03, H-04, M-01, M-02, M-03, M-04, and M-05; it passes on the amended tree; the output records 24 connector steps, 30 tests, 23 claims, and the actual current L/K count; the commit is pushed and remote-verified.
- Checkpoint: record verifier output path, commit, remote head, and next step.
- On failure: fix the verifier or the artifact it correctly rejects; never weaken a check to force a pass.
- Gate: none
- Relevant decisions/claims: finding M-04; Rule 14; protocol v3.6 Global Rule 6
- Lessons applied: `L-20261029T002439Z-artifact-id-boundaries`; `L-20261029T000700Z-artifact-consistency`
- Exclusive resources: repository working tree

### S-AMEND-008 Re-run review, pre-mortem, audit, and traceability

- Tier: Sonnet
- Profile: software; software.deploys
- Depends on: S-AMEND-007
- Inputs: amended planning artifacts; `premortem/`; `plan/TRACEABILITY.md`; `reviews/COLD_READ.md`
- Actions: 1. Update `reviews/COLD_READ.md` for protocol v3.6, including the actual current L/K count and the fact that this environment exposes no fresh-context subagent tool; do not claim an independent semantic cold read. 2. Run `premortem/round-3.md` against the changed persistence, ephemeral, verification, and amendment rules. 3. Add risk-register entries for any new material risks, such as environment misclassification, unavailable pin evidence, or overly generic artifact postconditions; mitigate every Critical/High finding before continuing. 4. Extend `premortem/ASSUMPTION_AUDIT.md` to any new load-bearing amendment assumptions and update verdict counts truthfully. 5. Update `plan/TRACEABILITY.md` with the amendment decision ID and the amendment evidence requirements. 6. Update `plan/PLAN.md` header counts and status: use `READY` only when every v3.6 check passes; otherwise use `BLOCKED — HUMAN DECISION REQUIRED`. 7. Commit after each review/audit artifact, push, and verify remote HEAD.
- Outputs: updated `reviews/COLD_READ.md`; `premortem/round-3.md`; updated `premortem/RISK_REGISTER.md`; updated `premortem/ASSUMPTION_AUDIT.md`; updated `plan/TRACEABILITY.md`; updated `plan/PLAN.md` header
- Evidence produced: cold-read record; pre-mortem round; audit rows; traceability rows; truthful v3.6 status header
- Done when: every changed artifact exists and contains its required sections; pre-mortem round 3 has zero unresolved Critical/High risks; audit counts match actual rows; traceability includes the amendment decision ID; `plan/PLAN.md` has a v3.6 status header supported by the verifier; every commit is pushed and remote-verified.
- Checkpoint: record review/audit artifacts, risk convergence, commit list, remote head, and next step.
- On failure: record the exact unresolved finding and stop; do not downgrade severity to continue.
- Gate: none
- Relevant decisions/claims: the amendment decision created in S-AMEND-001; findings C-01 and H-01 through M-05
- Lessons applied: `L-20261029T002530Z-premortem-evidence-specificity`
- Exclusive resources: repository working tree

### S-AMEND-009 Final consistency validation and amendment handoff

- Tier: Haiku
- Profile: software; software.deploys
- Depends on: S-AMEND-008
- Inputs: all amended artifacts; generation branch; remote repository
- Actions: 1. Run the global resumption checks. 2. Run `git diff --check`; `python3 research/spikes/verify_planning.py`; `sha256sum -c tests/FROZEN_MANIFEST.sha256`; a full-tree scan using the same secret patterns as the verifier; and `git status --short`. 3. Verify that `git diff --name-only f4305b019fb898d5f941a812196a14f7ffc69c00..HEAD -- tests/` is empty unless a formal frozen-test amendment was separately completed. 4. Verify `.checkpoints/state.json` shows the amendment complete and the remote synchronized. 5. Confirm `plan/PLAN.md` has a truthful v3.6 status. 6. Create the final amendment handoff entry in `plan/amendment-v36/EXECUTION_LOG.md`. 7. Commit, push, verify `ls-remote`, and stop without executing any connector implementation step.
- Outputs: final commit; verified remote branch; final amendment log entry
- Evidence produced: final validation output; remote-verified commit; final connector plan status
- Done when: every validation command exits zero or has an explicitly documented blocked result; the frozen manifest matches; no secret is detected; the working tree is clean; local `HEAD` equals remote `HEAD`; `plan/PLAN.md` truthfully reports v3.6 `READY` or `BLOCKED — HUMAN DECISION REQUIRED`; no connector implementation, deployment, release, publication, or knowledge push occurred.
- Checkpoint: record final commit, remote head, validation results, and workflow termination.
- On failure: fix and rerun the failed validation; if the failure is external authentication or unavailable verification, record the bundle path or blocked item and stop.
- Gate: none
- Relevant decisions/claims: the amendment decision created in S-AMEND-001; all v3.6 findings
- Lessons applied: all applicable lessons on the generation branch
- Exclusive resources: repository working tree; generation branch

## Validation commands

Run these commands after S-AMEND-007 and again in S-AMEND-009:

```sh
cd /mnt/agents/output/kimi-code-github-app
git diff --check
python3 research/spikes/verify_planning.py
sha256sum -c tests/FROZEN_MANIFEST.sha256
git status --short --branch
git diff --name-only f4305b019fb898d5f941a812196a14f7ffc69c00..HEAD -- tests/
git rev-parse HEAD
git ls-remote origin refs/heads/gen-20261028T232935Z-kimi-github-app-connector
```

Expected results:

- `git diff --check` exits 0.
- The v3.6-extended verifier exits 0.
- The freeze manifest exits 0.
- The test-file diff is empty unless a formal frozen-test amendment was separately completed.
- Local `HEAD` equals the remote branch hash.
- `git status --short --branch` shows a clean tree on the generation branch.

## Failure and halt protocol

1. A failed check is never marked passed.
2. A substitution is never made without an immediate `DEVIATIONS.md` entry.
3. A missing tool or unavailable verification is recorded as blocked; it is not converted into assumed success.
4. A Critical or High finding blocks the next step until mitigated.
5. Every correction after a failed approach creates a lesson before work continues.
6. Every new durable subject fact creates a knowledge item before work continues.
7. If remote authentication remains unavailable, do not request or reuse a PAT; write a Git bundle and report the path.
8. If all checks pass and the remote is verified, stop immediately after the final amendment handoff. Do not execute connector implementation steps.
