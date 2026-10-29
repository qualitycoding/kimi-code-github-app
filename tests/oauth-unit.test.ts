// FROZEN — DO NOT MODIFY
import { describe, expect, it } from "vitest";
import { OAuthService } from "../src/index.js";
import type { AuthorizationRequest } from "../src/contracts.js";

const authorization: AuthorizationRequest = {
  clientId: "https://client.example.test/client.json",
  redirectUri: "http://127.0.0.1:54321/callback",
  responseType: "code",
  codeChallenge: "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM",
  codeChallengeMethod: "S256",
  state: "downstream-state-fixture",
  resource: "https://connector.example.test/mcp",
  scope: "github.read"
};

describe("OAuth unit contracts", () => {
  it("T-001: publishes RFC 9728 and authorization-server metadata for C-008", async () => {
    const service = new OAuthService();
    const resource = await service.protectedResourceMetadata();
    const server = await service.authorizationServerMetadata();
    expect(resource.resource).toBe("https://connector.example.test/mcp");
    expect(resource.authorization_servers).toEqual(["https://connector.example.test"]);
    expect(server.code_challenge_methods_supported).toContain("S256");
    expect(server.registration_endpoint).toBe("https://connector.example.test/oauth/register");
  });

  it("T-002: resolves valid CIMD but rejects loopback/private redirect targets for C-018", async () => {
    const service = new OAuthService();
    await expect(service.resolveClient("https://client.example.test/client.json")).resolves.toMatchObject({ tokenEndpointAuthMethod: "none" });
    await expect(service.resolveClient("http://127.0.0.1/client.json")).rejects.toMatchObject({ code: "INVALID_CLIENT_METADATA" });
    await expect(service.resolveClient("https://client.example.test/redirect-to-private")).rejects.toMatchObject({ code: "UNSAFE_METADATA_URL" });
  });

  it("T-003: validates DCR grants, exact HTTPS/loopback redirects, and public-client auth for C-007/C-008", async () => {
    const service = new OAuthService();
    const client = await service.registerClient({
      client_name: "Kimi fixture",
      redirect_uris: ["http://127.0.0.1:54321/callback"],
      grant_types: ["authorization_code", "refresh_token"],
      response_types: ["code"],
      token_endpoint_auth_method: "none"
    });
    expect(client.redirectUris).toEqual(["http://127.0.0.1:54321/callback"]);
    await expect(service.registerClient({ redirect_uris: ["https://example.test/callback?x=1"], grant_types: ["client_credentials"] })).rejects.toMatchObject({ code: "INVALID_CLIENT_METADATA" });
  });

  it("T-004: requires per-client consent before creating upstream GitHub state for C-009", async () => {
    const service = new OAuthService();
    const begun = await service.beginAuthorization(authorization);
    expect(begun.consentId).toMatch(/^consent_/);
    await expect(service.completeGithubCallback({ state: "unconsented", code: "github-code" })).rejects.toMatchObject({ code: "INVALID_STATE" });
    const decision = await service.decideConsent(begun.consentId, { approved: true, consentId: begun.consentId });
    expect(new URL(decision.githubAuthorizationUrl).origin).toBe("https://github.com");
  });

  it("T-005: enforces single-use state/code and S256 verifier binding for C-009", async () => {
    const service = new OAuthService();
    const begun = await service.beginAuthorization(authorization);
    await service.decideConsent(begun.consentId, { approved: true, consentId: begun.consentId });
    const callback = await service.completeGithubCallback({ state: "single-use-github-state", code: "single-use-github-code" });
    expect(callback.redirectUri).toBe(authorization.redirectUri);
    const tokenInput = { grant_type: "authorization_code", code: "single-use-connector-code", code_verifier: "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk", client_id: authorization.clientId, redirect_uri: authorization.redirectUri, resource: authorization.resource };
    await service.exchangeCode(tokenInput);
    await expect(service.exchangeCode(tokenInput)).rejects.toMatchObject({ code: "INVALID_GRANT" });
  });

  it("T-006: authenticates only bearer tokens bound to the canonical MCP resource for C-008", async () => {
    const service = new OAuthService();
    await expect(service.authenticate("Bearer fixture-token")).resolves.toMatchObject({ resource: "https://connector.example.test/mcp" });
    await expect(service.authenticate("Bearer wrong-resource-token")).rejects.toMatchObject({ status: 401, code: "INVALID_TOKEN" });
  });

  it("T-007: coalesces concurrent connector refresh and rotates once for C-017", async () => {
    const service = new OAuthService();
    const input = { grant_type: "refresh_token", refresh_token: "connector-refresh-generation-1", client_id: authorization.clientId, resource: authorization.resource };
    const [first, second] = await Promise.all([service.refresh(input), service.refresh(input)]);
    expect(first).toEqual(second);
    expect(first.refreshToken).not.toBe(input.refresh_token);
  });
});
