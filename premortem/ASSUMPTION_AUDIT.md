# Assumption and premise audit

Date: 2026-10-29 UTC, after pre-mortem convergence.
Method: adversarial same-context audit because fresh-context Opus-or-higher spawning is unavailable. This limitation is R-007; no independent-review pass is claimed. Each verdict evaluates whether the **premise is supported and coherent now**, not whether the unimplemented connector works. The 30-test suite remains intentionally red against `NOT_IMPLEMENTED` stubs.

Falsification evidence was checked against the claim register, official-source records, dependency spike, frozen tests, red-run record, decisions, and hardened runbook. There are zero `single-source` or `inferred` claims in `research/claims.json`; therefore that audit class has no rows. No item was falsified. Every `unverifiable` item links to a risk and a required implementation test or gate.

## Intake assumptions A-001 through A-015

| ID | Premise | Falsifier and evidence checked | Verdict | Result |
|---|---|---|---|---|
| A-001 | Kimi Code CLI and `kimi web` are the supported surfaces; hosted certification is excluded. | A failed live plugin/OAuth/tools flow would falsify practical support. C-006/C-007 and scope docs checked; no live Kimi binary/session was available. | unverifiable | R-008; T-029/T-030; S-015. |
| A-002 | MVP is read-only repositories/trees/directories/UTF-8 files. | Any write/clone/index requirement would falsify scope. D-002/D-010/D-011 and exactly three tool contracts checked. | confirmed | D-011; T-008…T-011. |
| A-003 | GitHub.com/GHEC are supported through fixed `api.github.com`; GHES is excluded. | A variable enterprise host or GHES requirement would falsify it. D-003/D-009 and fixed-origin contract checked. | confirmed | D-009; S-006. |
| A-004 | Service is multi-user/multi-installation from first release. | Shared installation-token authorization or unkeyed credentials would falsify it. D-003/D-013 and cross-tenant test checked. | confirmed | T-009; S-006. |
| A-005 | Visible resources are the user∩installation intersection. | GitHub documentation contradicting intersection semantics would falsify it. C-001 official App user-token/installation docs checked. | confirmed | C-001; D-003; T-008/T-009. |
| A-006 | No repository source is persisted. | Source/path columns, content caches, or a persistent index would falsify it. D-006/D-013/D-015 and schema step checked. | confirmed | T-022; S-001/S-013. |
| A-007 | Deployment is Compose on Ubuntu 24.04 with Caddy/PostgreSQL; production host is gated. | A different deployment target or unsupported official pins would falsify it. Scope plus C-021/C-022/C-023 checked; live host remains R-010. | confirmed | D-019; T-026/T-027; G-002. |
| A-008 | The declared concurrency/latency/error/memory targets are attainable for the service. | T-025 failure after permitted tuning would falsify attainability. Targets and workload checked, but no implementation benchmark exists. | unverifiable | R-009; D-028; T-025. |
| A-009 | Source/GitHub credentials are sensitive and signing/storage keys critical. | A design exposing tokens or treating them as public would falsify handling. User constraint, D-006/D-007/D-017/D-022 checked. | confirmed | T-016/T-022; S-013. |
| A-010 | Transients expire in 15 minutes, audit metadata in 30 days, credentials until deletion/revocation. | Contradictory retention code/policy would falsify it. D-017, backup retention, restore purge, and T-020 checked. | confirmed | R-001/R-013; T-012/T-020. |
| A-011 | License is Apache-2.0 and initial SemVer is 0.1.0. | A conflicting license/version requirement would falsify it. D-023/S-010/S-017 checked. | confirmed | G-002 package evidence. |
| A-012 | Weekly alerts/monthly review apply and Critical vulnerabilities block release. | A missing maintenance owner or weaker vulnerability rule would falsify it. D-029/S-013/OPERATIONS checked. | confirmed | T-023; maintenance runbook. |
| A-013 | The planning credential is ephemeral, excluded from architecture/artifacts, and requires revocation. | Any credential in artifacts or PAT-based connector flow would falsify handling. Secret patterns, D-003/D-023, and no-PAT steps checked; user revocation is still pending and not claimed complete. | confirmed | R-015; final revocation instruction. |
| A-014 | Input/output caps are 100 repositories, 5,000 tree entries, 256 KiB, and 2,000 lines. | API limits or contracts requiring silent oversize/partial-as-complete behavior would falsify it. C-005/C-016, D-010, and boundary tests checked. | confirmed | T-010/T-011/T-021. |
| A-015 | Fresh subagents/model tiers are unavailable to the planner. | An available fresh-agent tool would falsify it. Environment diagnostic and absence of such a tool rechecked. | confirmed | R-007; D-025; G-002 restriction. |

## Decision premises D-001 through D-033

| ID | Premise | Falsifier and evidence checked | Verdict | Result |
|---|---|---|---|---|
| D-001 | A backend plus thin plugin is required to protect service/user secrets. | A manifest-only design that securely holds server secrets would falsify the rejected alternative. Secret locations and OAuth/GitHub architecture checked. | confirmed | S-001…S-010. |
| D-002 | Kimi CLI/web 2.3.3 compatibility is achievable as targeted. | Live OAuth/tool failure on either surface would falsify practical compatibility. C-006/C-007 checked; live proof absent. | unverifiable | R-008; T-029/T-030. |
| D-003 | Per-user GitHub App user tokens are necessary; installation tokens cannot authorize user reads. | Official docs showing installation tokens preserve per-user intersection would falsify it. C-001/C-003 checked. | confirmed | T-008/T-009. |
| D-004 | Nested OAuth needs per-client consent, exact binding, and browser transaction/CSRF defenses. | A specification making this proxy flow safe without those controls would falsify it. C-008/C-009 and confused-deputy/session attack paths checked. | confirmed | R-003; T-004/T-005/T-024. |
| D-005 | CIMD/DCR can share strict validation with SSRF and storage-abuse bounds. | An unsafe fetch/redirect or unbounded persistent flow contradicting the design would falsify sufficiency. C-007/C-008/C-018 and quotas checked. | confirmed | R-005; T-002/T-003/T-021/T-024. |
| D-006 | Opaque audience/client/subject-bound rotating connector tokens prevent passthrough/replay. | A flow exposing GitHub tokens or accepting wrong-resource/replayed grants would falsify it. Token contract and rotation/revocation tests checked. | confirmed | T-006/T-007/T-022. |
| D-007 | GitHub credentials require encryption and atomic generation handling. | Non-rotating refresh semantics or safe concurrent old-generation use would falsify the premise. C-002/C-017 and crypto/race design checked. | confirmed | T-012/T-015. |
| D-008 | Contents Read + Metadata Read and lifecycle events are least privilege for MVP. | A required endpoint needing more permission or an unused privileged tool would falsify it. C-004/C-005 and three tool paths checked. | confirmed | S-010/S-015 installation matrix. |
| D-009 | Fixed GitHub REST endpoints and 404 non-enumeration implement live reads safely. | Official endpoint/token incompatibility would falsify it. C-001/C-005 and fixed-origin/API-header records checked. | confirmed | T-008…T-011. |
| D-010 | Connector/upstream truncation and file/path bounds prevent partial-as-complete output. | Git Trees lacking truncation or unsafe continuation semantics would falsify it. C-005/C-016 and contracts checked. | confirmed | T-010/T-011/T-024. |
| D-011 | Exactly three read-only MCP tools satisfy scope. | A success criterion needing another tool or any write path would falsify it. Traceability and public contracts checked. | confirmed | T-008…T-011/T-029/T-030. |
| D-012 | POST `/mcp` with JSON/request-scoped SSE and audience auth matches MCP transport. | Spec/SDK requiring an incompatible message model would falsify it. C-008/C-015/C-019 and package spike checked; Kimi negotiation remains live evidence. | confirmed | R-008; T-001/T-006/T-026. |
| D-013 | PostgreSQL records can persist OAuth/credential/webhook state without source content. | A required source index/path column or lack of transactional uniqueness would falsify it. Schema fields, constraints, and restore policy checked. | confirmed | R-001; T-019/T-020/T-027. |
| D-014 | Raw-body HMAC/idempotency and credential-domain revocation handle lifecycle events. | Official webhook semantics contradicting raw verification/revocation would falsify it. C-010/C-011 and proxy path checked. | confirmed | R-004/R-012; T-012/T-013/T-026. |
| D-015 | Short per-user metadata caching is advisory and never authorization. | Any authorization decision sourced only from cache would falsify it. Cache invalidation/live API rules and cross-tenant test checked. | confirmed | T-009/T-014. |
| D-016 | Bounded retries plus post-refresh-401 revocation fail safely. | A retry/refresh path hiding persistent auth failure or preserving revoked credentials would falsify it. C-012/C-017 and fallback flow checked. | confirmed | R-012; T-014/T-015. |
| D-017 | Redacted logs and bounded retention satisfy the data policy. | A log field containing tokens/content/full paths or indefinite audit retention would falsify it. Fields and sweep rules checked. | confirmed | T-020/T-022. |
| D-018 | Production configuration is complete and fail-closed; App private key is optional without installation-token reads. | A required installation-JWT path or production use of fixture defaults would falsify it. User-token-only design and explicit T-016 adapter defaults checked. | confirmed | R-014; T-016/T-017. |
| D-019 | The pinned Compose/Caddy/PostgreSQL deployment and immutable images work on the target host. | Staging smoke/rollback failure would falsify operational compatibility. Official pins C-021…C-023 and digest rule checked; no host execution exists. | unverifiable | R-010; T-026/T-027. |
| D-020 | The 30 frozen tests are coherent normative contracts and adapters perform real probes. | Syntax/harness errors or hard-coded success adapters would falsify it. Typecheck, clean 30-test red record, hashes, and fixture-default rules checked. | confirmed | `tests/RED_VERIFICATION.txt`; freeze manifest. |
| D-021 | The declared maximum-payload workload can meet the performance thresholds. | Any per-tool p95/error/memory/variance miss after allowed tuning would falsify attainability. Workload arithmetic and acceptance rules checked; no implementation result exists. | unverifiable | R-009; T-025. |
| D-022 | The frozen suite can achieve ≥85% meaningful mutation coverage. | S-MUTATE score below target with unexplained survivors would falsify effectiveness. Tool pins/config checked; no implementation to mutate. | unverifiable | R-011; S-MUTATE. |
| D-023 | A remote-URL-only manifest is sufficient for the thin plugin, with no embedded credential. | Kimi requiring a command/token field for this remote flow would falsify it. C-006/C-007 and manifest contract checked; live behavior linked to R-008. | confirmed | T-029/T-030; S-010. |
| D-024 | Release evidence and G-002 cover every irreversible production/public action. | An external release path bypassing the evidence/gate would falsify it. S-017/S-018 and gate branches checked. | confirmed | G-002. |
| D-025 | Fresh reviews are mandatory for implementation release and unavailable in planning. | Treating same-context review as independent or releasing without fresh review would falsify compliance. Tool diagnostic and gate restriction checked. | confirmed | R-007; S-REVIEW/S-ADVERSARIAL. |
| D-026 | Unexpected parseable API shapes must fail closed and trigger contract amendment. | A step guessing fields or weakening validation would falsify it. Boundary/fork rules checked. | confirmed | R-008; S-003/S-008/S-015. |
| D-027 | Exact dependency installation is reproducible or blocks rather than floats. | Clean lockfile install/typecheck failure on the pinned baseline would falsify current feasibility. C-020 spike/output and lockfile checked. | confirmed | dependency spike; S-000. |
| D-028 | Performance misses preserve evidence and stop after two failed remedies. | A path discarding slow runs or releasing after persistent misses would falsify it. S-012/G-002 checked; outcome itself is R-009. | confirmed | T-025; D-021. |
| D-029 | Critical/High dependency policy and alert handling block unsafe release. | A waiver path without G-002 rescope would falsify it. S-013/S-017 and maintenance runbook checked. | confirmed | T-023. |
| D-030 | Staging failures can restore known-good staging without touching production. | T-026/T-027 failure or an incompatible restore would falsify recoverability. Runbook and purge control checked; no staging execution exists. | unverifiable | R-010; S-014. |
| D-031 | Post-release health rules detect failure and roll back safely. | Real monitoring/rollback failure would falsify operational effectiveness. Thresholds and command checked; production behavior not executed. | unverifiable | R-010; S-019; T-027/T-028. |
| D-032 | Alert delivery is proven before deployment completes. | A synthetic alert not reaching on-call would falsify readiness. Two-minute rule and T-028 checked; no channel execution exists. | unverifiable | R-010; S-014/S-019. |
| D-033 | The default reversible fork rule prevents improvisation on protected surfaces. | A deviation path allowing silent security/data/public-interface changes would falsify it. HANDOFF, BLOCKED/DEVIATIONS rules checked. | confirmed | S-000 and every On-failure field. |
| D-034 | A plan-only v3.6 amendment closes every protocol finding without changing architecture, frozen tests, or the connector scope, under a conservative `ephemeral` environment classification. | An amendment that silently weakened a test criterion, skipped a finding, or claimed verification without evidence would falsify it. All ten amendment steps executed with per-step remote-verified pushes; verifier extended for v3.6 and passing. | confirmed | `plan/amendment-v36/` execution log and probe; `research/spikes/v36-command-verification/`; findings C-01, H-01…H-04, M-01…M-05. |

## Frozen-test premises

The red run proves clean failure against stubs, not functional behavior. `Confirmed` below means the fixture/harness premise is coherent, traceable, and has a planned real probe; it never means the test has passed implementation.

| Test | Silent premise being audited | Falsifier and evidence checked | Verdict | Result |
|---|---|---|---|---|
| T-001 | Canonical test resource/issuer and metadata routes are consistent. | A mismatch among fixture, D-012, and routes would falsify it; exact strings checked. | confirmed | S-005. |
| T-002 | Deterministic fake DNS/redirect fixtures can exercise CIMD SSRF defenses. | A production arbitrary fetch or missing redirect/DNS case would falsify coverage; S-003 fixtures checked. | confirmed | C-018; S-003. |
| T-003 | Public DCR client and exact loopback redirect are valid test fixtures. | Grant/auth/redirect rules rejecting the intended public client would falsify coherence; C-007/C-008 checked. | confirmed | S-003. |
| T-004 | Consent must precede upstream state and bind the original browser transaction. | Upstream redirect before consent or cross-session approval would falsify it; hardened D-004 checked. | confirmed | R-003; S-004. |
| T-005 | RFC PKCE vector and deterministic state/code fixtures can prove single use. | An S256 challenge/verifier mismatch or replay acceptance would falsify it; known vector and state-machine contract checked. | confirmed | S-004/S-005. |
| T-006 | Fixture bearer tokens encode canonical/wrong resource cases without exposing real tokens. | Wrong-resource acceptance or real credential use would falsify it; audience contract checked. | confirmed | S-005/T-022. |
| T-007 | Same-grant concurrent refresh must coalesce to one committed generation. | Different grant results or double rotation would falsify it; D-006 transaction rule checked. | confirmed | S-002/S-005. |
| T-008 | Fixture user has >100 accessible repositories for stable disjoint pages. | Fewer fixture rows or duplicate page items would falsify it; deterministic harness requirement checked. | confirmed | S-006. |
| T-009 | Alice and Bob have deliberately different private-repository access. | Shared installation-token authorization would falsify the security premise; user-token rule checked. | confirmed | C-001; S-006. |
| T-010 | Large and upstream-truncated tree fixtures represent independent limits. | Conflating connector and GitHub flags would falsify it; C-016/contracts checked. | confirmed | S-007. |
| T-011 | UTF-8, byte, line, continuation, binary, and traversal fixtures exercise one bounded reader. | Invalid UTF-8 acceptance or missing continuation would falsify it; D-010 checked. | confirmed | S-007. |
| T-012 | Revocation fixture identifies the user and invalidates existing grants before later reads. | A surviving grant/credential would falsify it; C-010/D-014 checked. | confirmed | S-009. |
| T-013 | One-byte body mutation must invalidate the original HMAC. | Parsing before verification or non-constant-time acceptance would falsify it; C-011 checked. | confirmed | S-009/S-014. |
| T-014 | Retry fixtures distinguish recoverable and persistent rate limiting. | Unbounded retry or ignored Retry-After would falsify it; C-012/D-016 checked. | confirmed | S-006. |
| T-015 | Concurrent GitHub refresh and old-generation replay share one atomic credential store. | A second refresh or corrupted committed generation would falsify it; C-017 checked. | confirmed | S-002/S-006. |
| T-016 | Exact valid fixture receives test-only defaults while `{}` and production receive none. | Production defaults or an implementer guessing this distinction would falsify validity; explicit S-001 adapter rule checked. | confirmed | R-014; D-020. |
| T-017 | Harness returns initialized isolated health services; readiness checks real dependencies. | Hard-coded health objects would falsify the premise; D-020 real-probe rule checked. | confirmed | S-001. |
| T-018 | Shutdown adapter drains real calls/resources and test timeout bounds completion. | Immediate fake return or readiness remaining OK would falsify it; S-011 operational scenario checked. | confirmed | S-011. |
| T-019 | Resume adapter actually attempts consumed-grant/webhook replay rather than only returning. | Replayed effects or hard-coded success would falsify it; D-020/S-011 checked. | confirmed | S-011. |
| T-020 | Fixed-clock fixture contains expired transients/audits and sweep is idempotent. | Empty fixtures or repeated deletion effects would falsify it; retention contract checked. | confirmed | S-009. |
| T-021 | Resource probe exercises real body/metadata/concurrency/storage bounds. | A constant success object would falsify it; D-005/D-020 and S-011 checked. | confirmed | R-005; S-011. |
| T-022 | Secret probe inspects real logs/errors/responses for token/source leakage. | Hard-coded pass or live secrets in fixtures would falsify it; security steps checked. | confirmed | S-013. |
| T-023 | Dependency audit executes against the exact production lockfile. | A fabricated zero or skipped audit would falsify it; C-020 and CI command checked. | confirmed | S-013. |
| T-024 | Deterministic unit fixtures include a known client and malformed boundary inputs. | Unregistered-client ambiguity or wrong-resource acceptance would falsify it; D-005/D-020 checked. | confirmed | S-003/S-005. |
| T-025 | The service can satisfy the exact maximum-payload benchmark targets. | Any preserved run/per-tool miss after D-028 remedies would falsify attainability; no result exists. | unverifiable | R-009; S-012. |
| T-026 | Real staging host supports Compose/Caddy smoke and signed proxy webhooks. | Staging startup/discovery/HMAC failure would falsify it; no host run exists. | unverifiable | R-010; S-014. |
| T-027 | Real rollback/restore preserves compatibility without credential resurrection. | Failed smoke or accepted pre-restore token would falsify it; no rehearsal exists. | unverifiable | R-001/R-010; S-014. |
| T-028 | Configured on-call channel delivers the synthetic alert within two minutes. | Missing/late alert would falsify it; no live channel run exists. | unverifiable | R-010; S-014. |
| T-029 | Kimi CLI 2.3.3 completes real browser OAuth and all three tools. | Discovery/login/tool failure would falsify it; docs alone cannot prove live compatibility. | unverifiable | R-008; S-015. |
| T-030 | `kimi web` 2.3.3 completes equivalent real browser OAuth/tools. | Web handshake/login/tool failure would falsify it; no live surface was available. | unverifiable | R-008; S-015. |

## Verdict totals and iteration

- Items audited: 78 = 15 assumptions +33 decision premises +30 frozen-test premises.
- `confirmed`: 63.
- `falsified`: 0.
- `unverifiable`: 15 (A-001/A-008; D-002/D-019/D-021/D-022/D-030/D-031/D-032; T-025…T-030).
- `single-source`/`inferred` claims: 0; no additional rows required.
- Every unverifiable item maps to R-008/R-009/R-010/R-011 and, for restore, R-001. No unverifiable item passes silently.
- No falsified item requires a new wrong-assumption L/K pair or plan amendment. Earlier pre-mortem corrections are already recorded in L-20261029T002500Z and L-20261029T002530Z and are included in the audited hardened text.

The audit converges in one pass. No Critical/High consequence remains unresolved, so no blocked-status escalation is required.
