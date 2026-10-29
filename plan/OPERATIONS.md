# Operations runbook

## Service ownership and dashboards

The G-002 record names the on-call owner and alert destination. Dashboards show request rate, p50/p95/p99 connector-added latency, connector error fraction, active requests, process RSS, event-loop delay, PostgreSQL pool/health, GitHub 401/403/429/5xx counts, refresh single-flight conflicts, webhook signature failures, and retention-sweep results. Logs contain no credentials, repository contents, or full repository paths.

## Routine start, migration, and health verification

From the approved release directory:

```sh
docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.release.yml config --quiet
docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.release.yml pull
docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.release.yml up -d postgres
./deploy/migrate.sh
docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.release.yml up -d connector caddy
curl -fsS "$CONNECTOR_ORIGIN/health/live"
curl -fsS "$CONNECTOR_ORIGIN/health/ready"
```

Startup is complete only when both health checks pass and a synthetic authenticated MCP discovery succeeds. Database migrations must be backward-compatible with the previous release; expand before contract, and defer destructive changes beyond the rollback window.

## Alerts and immediate response

| Condition | Threshold | Response |
|---|---|---|
| Readiness | Two consecutive failed 30-second probes | Roll back if during rollout; otherwise remove from service and investigate database/key health |
| Connector errors | >1% for 5 minutes, excluding GitHub-attributed upstream errors | Roll back during rollout; inspect redacted error-code distribution |
| Latency | p95 connector-added ≥300 ms for 10 minutes | Profile and reduce load; roll back a regression |
| Memory | Service RSS ≥448 MiB for 10 minutes | Investigate before the 512 MiB limit; restart only after preserving evidence |
| Revocation/webhook failures | Any sustained authenticated processing failure, or repeated invalid signatures | Pause affected credential processing; verify raw-body proxy behavior and secret configuration |
| Refresh replay | Any old-generation replay | Revoke the affected grant, force reauthentication, and investigate possible credential theft |
| Retention | Sweep fails twice or rows exceed retention | Block new OAuth starts, repair sweep, and verify deletion before resuming |
| Dependency alert | Critical production vulnerability | Block release and patch immediately; High follows D-029 |
| Synthetic alert | Not received within 2 minutes | Deployment/rollout is incomplete; repair monitoring before proceeding |

Invalid-signature attempts are security signals but do not by themselves prove compromise. Do not add alert thresholds that leak repository/user metadata into notifications.

## Rollback command

Set `PREVIOUS_RELEASE_ID` to the last release whose readiness, migration compatibility, and authenticated MCP smoke all passed, then run:

```sh
export PREVIOUS_RELEASE_ID="<recorded-known-good-release-id>"
./deploy/rollback.sh "$PREVIOUS_RELEASE_ID"
curl -fsS "$CONNECTOR_ORIGIN/health/live"
curl -fsS "$CONNECTOR_ORIGIN/health/ready"
./deploy/smoke.sh "$CONNECTOR_ORIGIN"
```

The script pins the previous image digest and release configuration, starts it without deleting the current database, and never downgrades through an incompatible migration. If the previous release cannot use the current schema, stop the connector, restore the pre-migration backup using `./deploy/restore.sh <verified-backup-id>`, apply the mandatory all-credential/all-grant invalidation below, rerun rollback, and reauthenticate the synthetic test user before authenticated smoke. Never delete a volume as a rollback shortcut or skip invalidation to preserve sessions.

## Backup, revocation, and recovery

Back up PostgreSQL before every migration and daily; encrypt backups, retain each for at most 30 days, and test restore monthly. The external token-encryption key is required for restore and is never stored in the database dump. Every restore is fail-closed: keep connector/Caddy OAuth and MCP traffic stopped, complete `./deploy/restore.sh <verified-backup-id>`, delete **all** restored GitHub credential generations and connector grants in one transaction, and prove a pre-restore connector token is rejected and GitHub access requires reauthentication before restarting traffic. Never treat a restored credential or grant as valid merely because its expiry is in the future. Revoke/rotate the GitHub client secret, webhook secret, connector token key, or encryption key through the documented dual-key/dual-secret rollout; immediate key compromise response revokes active connector grants. User deauthorization requires no operator action after T-012 passes; a persistent post-refresh GitHub 401 invokes the same deletion path under D-016.

After interruption, PostgreSQL uniqueness constraints deduplicate webhook deliveries and token generations. Run `./deploy/migrate.sh`, start the service, verify readiness, and confirm consumed authorization codes/states are not replayed. Never replay a queue manually without checking delivery IDs.

## Post-release verification

For 60 minutes after S-018: run live/ready/smoke at 1, 5, 15, 30, and 60 minutes; execute one real revocation against a test user; run one Kimi read-only repository call; verify the synthetic alert; compare latency/error/memory against baseline; and check retention logs. Any D-031/D-032 condition triggers rollback. Record outcomes in `RELEASE_VERIFICATION.md`.

## Maintenance

Weekly: review automated dependency and container-base alerts, rotate failing credentials as needed, and verify backup/alert health. Monthly: manually compare every direct dependency and deployment pin with maintained releases, restore one backup, review access/audit retention, and run the frozen suite on the candidate lockfile. Critical vulnerabilities block release. Dependency updates use exact pins, a new lockfile, full tests/reviews, and G-002 evidence; never edit production dependencies in place.
