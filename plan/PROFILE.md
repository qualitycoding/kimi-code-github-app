# Planning profiles

- Active profiles: `software`
- Mode flags: `software.deploys=true`
- environment_class: ephemeral
- Environment probe evidence: `plan/amendment-v36/ENVIRONMENT_PROBE.md` (probe run 2026-10-30T20:50:35Z; runner class `linux-x86_64-2vCPU-4GiB-fuse.portal`). The `[ephemeral]` execution protections apply: all durable state under the repository durable path, turn-start branch/remote/runtime restaging, one-step chunking, and resume from committed remote-verified state only.
- Justification: the deliverable is a maintained GitHub App, remote MCP service, and installable Kimi Code plugin with staging and gated production deployment.
- N/A sections: all `math`, `computational`, and `publication` artifacts and checks, including `research/NOVELTY.md`, `math/**`, `figures/**`, and `manuscript/**`.
- Model execution note: this session exposes no subagent-spawning tool or selectable model tiers. The sole available model performs all tiers; fresh-context requirements are recorded as an open verification limitation rather than silently treated as satisfied.
