---
id: K-20261029T000017Z-c-017-connector-research
statement: GitHub App user-token refresh rotates both credentials and invalidates the old access and refresh tokens, so persistence and refresh must be atomic per user.
status: current
supersedes: []
tags: [subject:kimi-github-connector, tech:github, phase:research]
applies_to_version: "2026-10-29 researched interfaces"
source: { url: "https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/refreshing-user-access-tokens", doi: "", title: "Official documentation", locator: "relevant section", accessed: "2026-10-29", tier: 1 }
confidence: corroborated
derived_from: [C-017]
discovered_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-29T00:00:17Z
---
Corroborating source: https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app. This item is scoped to the researched versions and must be rechecked at implementation start.
