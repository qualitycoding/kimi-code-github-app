# Research round 4 — deployment-pin verification

Date: 2026-10-29 UTC.

The final environment review identified deployment versions that were selected in intake but not yet supported by the claim register. Official release metadata established Docker Engine 29.9.2, Docker Compose 5.6.1, Caddy 2.11.7, and PostgreSQL 18.6 as exact pins. Added C-021 through C-023 and corresponding knowledge items.

The Engine/Compose pins include October 2026 security fixes. PostgreSQL 18.6 is selected rather than an unverified newer major line; its official release notes and supported-version policy corroborate the pin. Caddy's official release and distribution channels corroborate its version.

No Docker daemon, Caddy service, PostgreSQL server, public hostname, or production credential was available, so these remain release-metadata corroborations, not deployment verifications. S-000 and T-026…T-028 are the execution checks. The planner does not claim that staging or production works.

The environment handoff was also corrected to check `kimi web --help`, and a stale spike note was updated. These documentation corrections are recorded in L-20261029T000700Z-artifact-consistency.
