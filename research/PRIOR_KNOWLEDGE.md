# Prior knowledge (R0)

Store: `qualitycoding/knowledge` at `462f6cb6da6507db1e9255a5213df4cc26b086e3`.

## Prevention checklist

No active lessons matched `domain:github-integration`, `tech:github`, `tech:github-actions`, `tech:mcp`, `tech:oauth`, `tech:nodejs`, `tech:typescript`, or `applies:all`.

## Knowledge loaded and applied

- `K-20261004T102023Z-github-access-from-sandbox`: use per-command authentication and never persist credentials. Applied to L-20261028T233100Z and all Git operations. Environment-specific historical observations are not connector design evidence.
- `K-20261009T193504Z-proxy-injected-git-config`: shell variables do not persist between calls; never print tokens. Applied to planning commands and S-000 secret checks.
- `K-20261009T160122Z-token-scopes`: repository Contents and Workflows are distinct permissions. Applied to S-000 and the CI/release credential contract; the delivered connector uses a GitHub App, not a PAT.
- `K-20261007T160017Z-c-018`: `actions/checkout` v7.0.1 and commit pin. To be revalidated before pinning CI.
- `K-20261007T160136Z-c-097`: action major breaking changes. Applied to the CI security decision; no `pull_request_target` with fork heads.
- `K-20261009T193011Z-typescript-erasable-syntax-only-rejects-parameter-properties`: avoid constructor parameter properties when `erasableSyntaxOnly` is enabled. Applied to TypeScript interface/stub style.
- `K-20261009T160119Z-vite-vitest-node`: Node/Vitest compatibility needs an engine check. Applied to environment pinning; versions must be refreshed before use.

Other entries matching only a broad technology tag were read as non-applicable because their subjects were unrelated packages or audio/Web Audio projects. No prior entry supplies evidence for GitHub App, MCP, OAuth, or Kimi behavior; those remain research questions.
