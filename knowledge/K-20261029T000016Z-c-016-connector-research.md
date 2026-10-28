---
id: K-20261029T000016Z-c-016-connector-research
statement: Recursive GitHub trees expose an upstream truncated flag and are limited to 100,000 entries or 7 MB; connector truncation must be tracked independently.
status: current
supersedes: []
tags: [subject:kimi-github-connector, tech:github, phase:research]
applies_to_version: "2026-10-29 researched interfaces"
source: { url: "https://docs.github.com/en/rest/git/trees#get-a-tree", doi: "", title: "Official documentation", locator: "relevant section", accessed: "2026-10-29", tier: 1 }
confidence: corroborated
derived_from: [C-016]
discovered_by: planner
run: 20261028T232935Z
recorded_at: 2026-10-29T00:00:16Z
---
Corroborating source: https://github.com/github/rest-api-description. This item is scoped to the researched versions and must be rechecked at implementation start.
