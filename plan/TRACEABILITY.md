# Requirements and traceability

## Success criteria

| Criterion | Observable success | Tests | Delivery steps |
|---|---|---|---|
| SC-001 | A user installs a public GitHub App on a personal account or organization, selects all/some repositories, and connects Kimi without creating a PAT | T-003, T-004, T-029, T-030 | S-003, S-004, S-010, S-015 |
| SC-002 | Every read is limited to resources shared by that user and the App installation | T-008, T-009 | S-006, S-008 |
| SC-003 | Kimi can list accessible repositories with bounded stable pages | T-008 | S-006, S-008 |
| SC-004 | Kimi can inspect refs/trees/directories without hiding connector or GitHub truncation | T-010 | S-007, S-008 |
| SC-005 | Kimi can read bounded UTF-8 text with explicit continuations and safe errors | T-011, T-024 | S-007, S-008 |
| SC-006 | MCP OAuth supports CIMD/DCR, PKCE, per-client consent, audience binding, rotation, and no token passthrough | T-001…T-007, T-022, T-024 | S-002…S-005, S-008 |
| SC-007 | GitHub refresh races, webhooks, revocation, and rate limits fail safely | T-012…T-015 | S-006, S-009 |
| SC-008 | No source is persisted; credentials are encrypted/redacted and retention is enforced | T-020, T-022 | S-001, S-002, S-009, S-013 |
| SC-009 | Connector meets the 50-concurrency latency/error/memory targets | T-025 | S-012 |
| SC-010 | Startup, readiness, shutdown, interruption, retention, and exhaustion behavior is operational | T-016…T-021 | S-001, S-009, S-011 |
| SC-011 | Compose/Caddy staging, rollback, healthchecks, and alerts are proven | T-026…T-028 | S-014, S-019 |
| SC-012 | Versioned Apache-2.0 plugin/service is released only after live Kimi verification and human approval | T-029, T-030 | S-010, S-015, S-017, S-018 |

## Test-to-evidence matrix

| Test | Category | Requirements / claims / decisions | Producing step |
|---|---|---|---|
| T-001 | Unit | SC-006; C-008; D-004, D-012 | S-005 |
| T-002 | Unit/security | SC-006; C-018; D-005 | S-003 |
| T-003 | Unit | SC-001/006; C-007/C-008; D-005 | S-003 |
| T-004 | Unit/security | SC-001/006; C-009; D-004 | S-004 |
| T-005 | Integration | SC-006; C-009; D-004/D-006 | S-004 |
| T-006 | Unit/security | SC-006; C-008; D-006/D-012 | S-005 |
| T-007 | Concurrency | SC-006; C-017; D-006 | S-005 |
| T-008 | Integration | SC-002/003; C-001/C-004; D-003/D-009 | S-006 |
| T-009 | Security integration | SC-002; C-001; D-003 | S-006 |
| T-010 | Integration/boundary | SC-004; A-014; C-016; D-010 | S-007 |
| T-011 | Integration/boundary | SC-005; A-014; C-005; D-010 | S-007 |
| T-012 | Revocation integration | SC-007; C-010; D-007/D-014 | S-009 |
| T-013 | Security integration | SC-007; C-011; D-014 | S-009 |
| T-014 | Failure recovery | SC-007; C-012; D-016 | S-006 |
| T-015 | Concurrency | SC-007; C-002/C-017; D-007 | S-006 |
| T-016 | Operational/security | SC-010; A-009; D-018 | S-001 |
| T-017 | Operational | SC-010/011; D-019 | S-001 |
| T-018 | Operational | SC-010; D-019 | S-011 |
| T-019 | Operational recovery | SC-010; D-013/D-014 | S-011 |
| T-020 | Operational/retention | SC-008/010; A-010; D-017 | S-009 |
| T-021 | Operational/security | SC-009/010; A-008; D-005/D-012 | S-011 |
| T-022 | Security | SC-006/008; A-009; C-008; D-006/D-017 | S-013 |
| T-023 | Security/supply chain | A-012; D-029 | S-013 |
| T-024 | Security/input | SC-005/006; C-008/C-009; D-005/D-010 | S-003 |
| T-025 | Performance | SC-009; A-008; D-021 | S-012 |
| T-026 | Deployment | SC-011; A-007; D-019 | S-014 |
| T-027 | Deployment/rollback | SC-011; A-007; D-030/D-031 | S-014 |
| T-028 | Deployment/alerting | SC-011; D-032 | S-014 |
| T-029 | Live compatibility | SC-001/012; C-006/C-007; D-002/D-023 | S-015 |
| T-030 | Live compatibility | SC-001/012; A-001; C-007; D-002/D-023 | S-015 |

## Test freeze and amendment

`tests/FROZEN_MANIFEST.sha256` covers every test file. `tests/RED_VERIFICATION.txt` records the clean 30-test red run. Implementation may change stubs and add production code, but may not modify, skip, mark expected-failure, or weaken frozen tests. A test challenge starts at the earliest affected research/claim row above, then re-runs red verification, freeze, cold read, and pre-mortem on changed steps. Math, computational, publication, figure, and manuscript artifacts are N/A and are not required by any row.
