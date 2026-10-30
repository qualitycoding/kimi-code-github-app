# Deviations — amendment v3.6

Every substitution to a version pin, package, command, timeout, config value, environment
class, runner class, or artifact requirement is appended here at the moment it is made.
Format: UTC timestamp; step ID; original planned value; substituted value; reason;
validation command and result; commit hash after the substitution is committed.

## D-AMEND-001 — authentication method for amendment pushes

- Timestamp: 2026-10-30T20:50:35Z
- Step: S-AMEND-000
- Original planned value: "Do not use, store, print, commit, or request a GitHub PAT";
  on unavailable authentication, write a Git bundle and leave the plan blocked.
- Substituted value: Git smart-HTTPS push authenticated with a human-provided fine-grained
  PAT via the repo-local ephemeral credential helper `.git/credentials` (never committed,
  removed at end of run).
- Reason: the human operator explicitly instructed this amendment run to push with the
  provided token. The prior container had lost all local state, so the repository was
  re-cloned; a bundle fallback would have stranded the amendment before any step ran.
- Validation: `git push --dry-run origin gen-20261028T232935Z-kimi-github-app-connector`
  exits 0 ("Everything up-to-date"); first real push in S-AMEND-000 verified with
  `git ls-remote` (local HEAD == remote head).
- Commit hash after substitution: recorded with the S-AMEND-000 commit in
  `plan/amendment-v36/EXECUTION_LOG.md`.
