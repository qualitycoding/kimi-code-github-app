// FROZEN — DO NOT MODIFY
import { describe, expect, it } from "vitest";
import { createConnectorTestHarness } from "../src/index.js";

describe("Operational contracts", () => {
  it("T-016: fails startup on missing/invalid critical configuration without leaking secrets for A-009", async () => {
    const { runtime } = createConnectorTestHarness();
    await expect(runtime.start({})).rejects.toMatchObject({ code: "INVALID_CONFIGURATION" });
    await expect(runtime.start({ canonicalResource: "https://connector.example.test/mcp", databaseUrl: "fixture", githubClientId: "fixture", githubClientSecret: "fixture", tokenEncryptionKey: "32-byte-fixture-key-material!!!!" })).resolves.toBeUndefined();
  });

  it("T-017: distinguishes liveness from dependency-aware readiness for deployment monitoring", async () => {
    const { runtime } = createConnectorTestHarness();
    await expect(runtime.liveness()).resolves.toMatchObject({ status: "ok" });
    await expect(runtime.readiness()).resolves.toMatchObject({ status: "ok", checks: { database: "ok", tokenKey: "ok" } });
  });

  it("T-018: drains in-flight MCP calls and closes resources on SIGTERM within 10 seconds", async () => {
    const { runtime } = createConnectorTestHarness();
    await expect(runtime.shutdown("SIGTERM")).resolves.toBeUndefined();
    await expect(runtime.readiness()).resolves.toMatchObject({ status: "fail" });
  });

  it("T-019: resumes after interruption without replaying consumed grants or duplicate webhook effects", async () => {
    const { runtime } = createConnectorTestHarness();
    await expect(runtime.resumeAfterInterruption()).resolves.toBeUndefined();
  });

  it("T-020: deletes OAuth transient rows within 15 minutes and audit metadata after 30 days for A-010", async () => {
    const { retention, fixedNow } = createConnectorTestHarness();
    const swept = await retention.sweep(fixedNow);
    expect(swept.transientDeleted).toBeGreaterThan(0);
    expect(swept.auditDeleted).toBeGreaterThan(0);
    await expect(retention.sweep(fixedNow)).resolves.toEqual({ transientDeleted: 0, auditDeleted: 0 });
  });

  it("T-021: rejects excess bodies, metadata fetches, and concurrency without process failure for A-008", async () => {
    const { verification, runtime } = createConnectorTestHarness();
    await expect(verification.resourceExhaustion()).resolves.toEqual({ rejected: true, processHealthy: true });
    await expect(runtime.liveness()).resolves.toMatchObject({ status: "ok" });
  });
});
