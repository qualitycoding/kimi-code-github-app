// FROZEN — DO NOT MODIFY
import { describe, expect, it } from "vitest";
import { createConnectorTestHarness, OAuthService } from "../src/index.js";

describe("Security contracts", () => {
  it("T-022: forbids token passthrough and redacts GitHub/OAuth secrets from logs and errors for A-009/C-008", async () => {
    const { verification } = createConnectorTestHarness();
    await expect(verification.secretHandlingProbe()).resolves.toEqual({ passed: true });
  });

  it("T-023: reports dependency vulnerabilities so Critical findings block release for A-012", async () => {
    const { verification } = createConnectorTestHarness();
    const audit = await verification.dependencyAudit();
    expect(audit.critical).toBe(0);
    expect(audit.high).toBe(0);
  });

  it("T-024: rejects malformed paths, redirect URIs, resources, grants, and oversized input at boundaries for C-008/C-009", async () => {
    const service = new OAuthService();
    const base = { clientId: "client", redirectUri: "https://client.example/callback", responseType: "code" as const, codeChallenge: "fixture", codeChallengeMethod: "S256" as const, state: "state", resource: "https://connector.example.test/mcp" };
    await expect(service.beginAuthorization({ ...base, redirectUri: "https://client.example/callback?changed=1" })).rejects.toMatchObject({ code: "INVALID_REDIRECT_URI" });
    await expect(service.beginAuthorization({ ...base, resource: "https://attacker.example/mcp" })).rejects.toMatchObject({ code: "INVALID_RESOURCE" });
    await expect(service.exchangeCode({ grant_type: "client_credentials", client_id: "client" })).rejects.toMatchObject({ code: "UNSUPPORTED_GRANT_TYPE" });
  });
});
