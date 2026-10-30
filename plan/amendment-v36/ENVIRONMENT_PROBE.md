# Environment probe — amendment v3.6

Probe run: 2026-10-30T20:50:35Z (UTC)
Baseline branch: `gen-20261028T232935Z-kimi-github-app-connector`
Baseline commit verified: `f4305b019fb898d5f941a812196a14f7ffc69c00` (local HEAD == `git ls-remote` head at probe time)

## Environment classification

environment_class=ephemeral

Conservative-classification reason: this Kimi execution sandbox provides no persistence
guarantee across turn boundaries; the previous planning container disappeared with its
local state and this amendment run began from a fresh clone of the generation branch.
Per the conservative Kimi-environment default, the environment is classified `ephemeral`
in the absence of contradictory evidence.

## Durable path and /tmp warning

- Durable repository path: `/mnt/agents/output/kimi-code-github-app`
- All durable amendment state lives inside that repository. `/tmp` may be used only for
  disposable caches; no required evidence may be kept only in `/tmp`.

## Turn-start restaging rule

At the start of every step or resumed turn:

```sh
cd /mnt/agents/output/kimi-code-github-app
git status --short --branch
git rev-parse HEAD
git ls-remote origin refs/heads/gen-20261028T232935Z-kimi-github-app-connector
```

Local HEAD and the remote branch hash must match before work continues; otherwise stop
and reconcile from committed state (never force-push).

Runtime re-staging (Node 24 toolchain under the repo-local ignored `.runtime/`):

```sh
export RUNTIME_DIR="$PWD/.runtime"
mkdir -p "$RUNTIME_DIR/node24"
tar -xJf "$RUNTIME_DIR/node-v24.22.1-linux-x64.tar.xz" -C "$RUNTIME_DIR/node24" --strip-components=1
export PATH="$PWD/.runtime/node24/bin:$PATH"
test "$(node --version)" = "v24.22.1"
test "$(npm --version)" = "11.19.1"
```

## Runner facts (observed)

- OS/kernel: Linux 5.10.134-18.0.12.lifsea8.x86_64, x86_64
- vCPU: 2
- RAM: 4 GiB (`free -h` total 4.0Gi)
- `/mnt/agents` filesystem: `fuse.portal`
- Git: 2.39.5
- Python: 3.12.12

## Old mechanical suite results (these validate the v3.4-era suite, NOT v3.6 compliance)

- `python3 research/spikes/verify_planning.py` → exit 0:
  `all mechanical checks valid: 24 steps, 30 tests, 23 claims, 32 L/K entries`
- `sha256sum -c tests/FROZEN_MANIFEST.sha256` → exit 0 (all six frozen test files OK)

## Amendment-run credential note

The plan's prohibitions forbid using a pasted GitHub PAT. The human operator explicitly
directed this amendment run to authenticate with a provided fine-grained PAT, overriding
that prohibition for this run. The token is stored only in the repo-local
`.git/credentials` file (never committed; outside any artifact), pushes are verified with
`ls-remote` after every step, and the credential file is removed at the end of the run.
Recorded in `plan/amendment-v36/DEVIATIONS.md`.
