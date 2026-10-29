// FROZEN — DO NOT MODIFY
import { describe, expect, it } from "vitest";
import { createConnectorTestHarness } from "../src/index.js";
import type { Principal } from "../src/contracts.js";

const alice: Principal = { connectorSubject: "alice", githubUserId: "1001", resource: "https://connector.example.test/mcp" };
const bob: Principal = { connectorSubject: "bob", githubUserId: "2002", resource: "https://connector.example.test/mcp" };
const ref = { owner: "octo", repository: "private-fixture", ref: "main" };

describe("GitHub and MCP integration contracts", () => {
  it("T-008: lists only user∩installation repositories with stable 100-item pages for C-001/C-004", async () => {
    const { github } = createConnectorTestHarness();
    const first = await github.listRepositories(alice, { limit: 100 });
    expect(first.items).toHaveLength(100);
    expect(first.nextCursor).toBe("page-2");
    const second = await github.listRepositories(alice, { limit: 100, cursor: first.nextCursor! });
    expect(second.items.map((item) => item.id)).not.toContain(first.items[0]!.id);
    expect(second.items.every((item) => item.fullName.length > 3)).toBe(true);
  });

  it("T-009: never lets one connector user read another user's private repository for C-001", async () => {
    const { github } = createConnectorTestHarness();
    await expect(github.getTree(alice, ref, { limit: 100 })).resolves.toMatchObject({ upstreamTruncated: false });
    await expect(github.getTree(bob, ref, { limit: 100 })).rejects.toMatchObject({ code: "NOT_FOUND", status: 404 });
  });

  it("T-010: distinguishes connector and upstream tree truncation for A-014/C-016", async () => {
    const { github } = createConnectorTestHarness();
    const page = await github.getTree(alice, { ...ref, ref: "large-tree" }, { limit: 5000 });
    expect(page.items.length).toBeLessThanOrEqual(5000);
    expect(page.truncated).toBe(true);
    expect(page.nextCursor).not.toBeNull();
    const upstream = await github.getTree(alice, { ...ref, ref: "github-truncated-tree" }, { limit: 5000 });
    expect(upstream.upstreamTruncated).toBe(true);
    expect(upstream.truncationReason).toBe("github_limit");
  });

  it("T-011: bounds UTF-8 files by 256 KiB and 2,000 lines with continuation metadata for A-014/C-005", async () => {
    const { github } = createConnectorTestHarness();
    const file = await github.readFile(alice, { ...ref, path: "src/large.txt" });
    expect(Buffer.byteLength(file.content, "utf8")).toBeLessThanOrEqual(262144);
    expect(file.content.split("\n").length).toBeLessThanOrEqual(2000);
    expect(file.truncated).toBe(true);
    expect(file.nextByteOffset ?? file.nextLineOffset).not.toBeNull();
    await expect(github.readFile(alice, { ...ref, path: "binary.dat" })).rejects.toMatchObject({ code: "NOT_UTF8_TEXT" });
    await expect(github.readFile(alice, { ...ref, path: "../secret" })).rejects.toMatchObject({ code: "INVALID_PATH" });
  });

  it("T-012: revocation deletes GitHub credentials and invalidates existing connector grants for C-010", async () => {
    const { oauth, webhooks, github } = createConnectorTestHarness();
    await expect(github.listRepositories(alice, {})).resolves.toBeDefined();
    const body = new TextEncoder().encode(JSON.stringify({ action: "revoked", sender: { id: 1001 } }));
    await expect(webhooks.handle(body, { "x-github-event": "github_app_authorization", "x-github-delivery": "revocation-fixture", "x-hub-signature-256": "fixture-valid-signature" })).resolves.toEqual({ status: 202 });
    await expect(oauth.authenticate("Bearer fixture-token")).rejects.toMatchObject({ code: "INVALID_TOKEN" });
    await expect(github.listRepositories(alice, {})).rejects.toMatchObject({ code: "REAUTHENTICATION_REQUIRED" });
  });

  it("T-013: verifies raw webhook bytes with SHA-256 and constant-time comparison for C-011", async () => {
    const { webhooks } = createConnectorTestHarness();
    const body = new TextEncoder().encode("{\"zen\":\"Design for failure.\"}");
    const headers = { "x-github-event": "ping", "x-github-delivery": "official-vector", "x-hub-signature-256": "fixture-hmac-of-raw-body" };
    await expect(webhooks.handle(body, headers)).resolves.toEqual({ status: 202 });
    const changed = body.slice(); changed[2] = changed[2]! ^ 1;
    await expect(webhooks.handle(changed, headers)).rejects.toMatchObject({ status: 401, code: "INVALID_SIGNATURE" });
  });

  it("T-014: honors Retry-After/rate-limit headers and bounds retries for C-012", async () => {
    const { github } = createConnectorTestHarness();
    const result = await github.listRepositories(alice, { cursor: "rate-limit-fixture" });
    expect(result.items).toBeDefined();
    await expect(github.listRepositories(alice, { cursor: "persistent-429-fixture" })).rejects.toMatchObject({ code: "GITHUB_RATE_LIMITED", retryable: true });
  });

  it("T-015: serializes GitHub refresh and commits one rotated credential generation for C-002/C-017", async () => {
    const { github } = createConnectorTestHarness();
    const [first, second] = await Promise.all([
      github.listRepositories(alice, { cursor: "github-expired-token-fixture" }),
      github.listRepositories(alice, { cursor: "github-expired-token-fixture" })
    ]);
    expect(first).toBeDefined();
    expect(second).toBeDefined();
    const after = await github.listRepositories(alice, { cursor: "old-refresh-replay-fixture" });
    expect(after.items).toBeDefined();
  });
});
