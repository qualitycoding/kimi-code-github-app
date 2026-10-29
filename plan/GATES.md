# Human gates

While halted, independent non-external steps may continue. No production deployment, public release, or knowledge push may proceed without its specified response.

## G-002 — Production deployment and public release

- **Trigger step:** S-018, after S-017 has assembled the release candidate.
- **Evidence bundle:** implementation branch and commit; valid freeze manifest; T-001…T-030 results; five performance runs; dependency/secret scans; `reviews/CODE_REVIEW.md`, `reviews/ADVERSARIAL_REVIEW.md`, and `reviews/MUTATION.md`; staging smoke/rollback/alert evidence; live Kimi CLI/web OAuth and repository-read evidence; Apache-2.0/SemVer package; migration and rollback rehearsal; proposed production origin and release notes; current risk register.
- **Questions the human must answer:** (1) Is the evidence acceptable for production and public 0.1.0 release? (2) Are the proposed production origin, DNS, host, GitHub App production settings, alert destination, and on-call owner approved? (3) Is any scope reduction required?
- **Allowed responses:** `proceed`, `proceed-with-rescope: <text>`, or `stop`.
- **Branches:** `proceed` → deploy the exact reviewed commit, run S-019, and publish 0.1.0 only if post-release checks pass. `proceed-with-rescope` → record the rescope in `DEVIATIONS.md`, trace affected tests/interfaces, execute any required amendment, and return to S-017; no external action on the old candidate. `stop` → write `GATE-G-002.md`, leave production and public release untouched, and continue only independent non-external closing work.

## G-003 — Lessons and knowledge push

- **Trigger step:** S-KNOW after S-RETRO.
- **Evidence bundle:** `GATE-G-003.md` listing every planning and implementation lesson/knowledge ID, title, and tags; schema and secret-scan results; proposed target `qualitycoding/knowledge`; final execution log and retrospective.
- **Questions the human must answer:** May the listed non-secret lessons and knowledge be pushed, and to which repository?
- **Allowed responses:** `push-to-proposed`, `push-to: <target>`, or `do-not-push`.
- **Branches:** `push-to-proposed` → copy entries in Appendix C layout, regenerate indexes, and push to `qualitycoding/knowledge`. `push-to` → perform the same actions on the named target. `do-not-push` → retain entries on the implementation branch and finish without external knowledge publication. Up to three rejected-push retries use pull/index regeneration; persistent failure or no response produces `knowledge-20261028T232935Z.bundle` and reports its path.

No other gates are required: this is not a research-result publication, and staging uses only predeclared test resources. G-002 covers every production or public irreversible action; G-003 is mandatory for the knowledge push.
