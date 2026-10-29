// FROZEN — DO NOT MODIFY
import { describe, expect, it } from "vitest";
import { VerificationService } from "../src/index.js";

describe("Deployment and supported-surface contracts", () => {
  it("T-026: passes staging Compose/Caddy smoke and authenticated MCP discovery for A-007", async () => {
    await expect(new VerificationService().stagingSmoke()).resolves.toEqual({ passed: true });
  });

  it("T-027: restores the previous healthy release and database-compatible configuration on rollback for A-007", async () => {
    await expect(new VerificationService().rollback()).resolves.toEqual({ passed: true });
  });

  it("T-028: delivers a synthetic failed-health alert through the configured on-call channel", async () => {
    await expect(new VerificationService().monitoringAlert()).resolves.toEqual({ delivered: true });
  });

  it("T-029: completes browser OAuth and read-only MCP tools in Kimi Code CLI 2.3.3 for C-006/C-007", async () => {
    await expect(new VerificationService().kimiEndToEnd("cli")).resolves.toEqual({ oauth: true, tools: true });
  });

  it("T-030: completes browser OAuth and read-only MCP tools in kimi web 2.3.3 for A-001/C-007", async () => {
    await expect(new VerificationService().kimiEndToEnd("web")).resolves.toEqual({ oauth: true, tools: true });
  });
});
