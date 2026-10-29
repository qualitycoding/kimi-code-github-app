// FROZEN — DO NOT MODIFY
import { describe, expect, it } from "vitest";
import { VerificationService } from "../src/index.js";

describe("Performance contract", () => {
  it("T-025: meets 50-concurrency p95/error/memory targets over five mocked-GitHub runs for A-008", async () => {
    const service = new VerificationService();
    const result = await service.benchmark({ concurrency: 50, runs: 5, mockedGithub: true });
    expect(result.runP95ValuesMs).toHaveLength(5);
    expect(result.p95ConnectorLatencyMs).toBeLessThan(300);
    expect(result.errorFraction).toBeLessThan(0.01);
    expect(result.peakServiceMemoryMiB).toBeLessThan(512);
    expect(result.variancePercent).toBeLessThanOrEqual(20);
  }, 120_000);
});
