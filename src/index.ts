import { notImplemented } from "./not-implemented.js";
import type {
  AuthorizationRequest, BenchmarkRequest, BenchmarkResult, ClientMetadata,
  ConsentDecision, FileReadRequest, FileReadResult, IsoInstant, JsonObject,
  Page, PageRequest, Principal, Repository, RepositoryRef, RuntimeHealth,
  TokenGrant, TreeResult
} from "./contracts.js";

export class OAuthService {
  protectedResourceMetadata(): Promise<JsonObject> { return Promise.reject(notImplemented("OAuthService.protectedResourceMetadata")); }
  authorizationServerMetadata(): Promise<JsonObject> { return Promise.reject(notImplemented("OAuthService.authorizationServerMetadata")); }
  registerClient(input: JsonObject): Promise<ClientMetadata> { return Promise.reject(notImplemented("OAuthService.registerClient")); }
  resolveClient(clientId: string): Promise<ClientMetadata> { return Promise.reject(notImplemented("OAuthService.resolveClient")); }
  beginAuthorization(request: AuthorizationRequest): Promise<{ consentId: string }> { return Promise.reject(notImplemented("OAuthService.beginAuthorization")); }
  decideConsent(consentId: string, decision: ConsentDecision): Promise<{ githubAuthorizationUrl: string }> { return Promise.reject(notImplemented("OAuthService.decideConsent")); }
  completeGithubCallback(query: JsonObject): Promise<{ redirectUri: string }> { return Promise.reject(notImplemented("OAuthService.completeGithubCallback")); }
  exchangeCode(input: JsonObject): Promise<TokenGrant> { return Promise.reject(notImplemented("OAuthService.exchangeCode")); }
  refresh(input: JsonObject): Promise<TokenGrant> { return Promise.reject(notImplemented("OAuthService.refresh")); }
  authenticate(authorizationHeader: string): Promise<Principal> { return Promise.reject(notImplemented("OAuthService.authenticate")); }
}

export class GithubGateway {
  listRepositories(principal: Principal, page: PageRequest): Promise<Page<Repository>> { return Promise.reject(notImplemented("GithubGateway.listRepositories")); }
  getTree(principal: Principal, ref: RepositoryRef, page: PageRequest): Promise<TreeResult> { return Promise.reject(notImplemented("GithubGateway.getTree")); }
  readFile(principal: Principal, request: FileReadRequest): Promise<FileReadResult> { return Promise.reject(notImplemented("GithubGateway.readFile")); }
}

export class WebhookService {
  handle(rawBody: Uint8Array, headers: Readonly<Record<string, string>>): Promise<{ status: number }> { return Promise.reject(notImplemented("WebhookService.handle")); }
}

export class RetentionService {
  sweep(now: IsoInstant): Promise<{ transientDeleted: number; auditDeleted: number }> { return Promise.reject(notImplemented("RetentionService.sweep")); }
}

export class ConnectorRuntime {
  start(configuration: JsonObject): Promise<void> { return Promise.reject(notImplemented("ConnectorRuntime.start")); }
  readiness(): Promise<RuntimeHealth> { return Promise.reject(notImplemented("ConnectorRuntime.readiness")); }
  liveness(): Promise<RuntimeHealth> { return Promise.reject(notImplemented("ConnectorRuntime.liveness")); }
  shutdown(signal: "SIGTERM" | "SIGINT"): Promise<void> { return Promise.reject(notImplemented("ConnectorRuntime.shutdown")); }
  resumeAfterInterruption(): Promise<void> { return Promise.reject(notImplemented("ConnectorRuntime.resumeAfterInterruption")); }
}

export class VerificationService {
  resourceExhaustion(): Promise<{ rejected: boolean; processHealthy: boolean }> { return Promise.reject(notImplemented("VerificationService.resourceExhaustion")); }
  secretHandlingProbe(): Promise<{ passed: boolean }> { return Promise.reject(notImplemented("VerificationService.secretHandlingProbe")); }
  dependencyAudit(): Promise<{ critical: number; high: number }> { return Promise.reject(notImplemented("VerificationService.dependencyAudit")); }
  benchmark(request: BenchmarkRequest): Promise<BenchmarkResult> { return Promise.reject(notImplemented("VerificationService.benchmark")); }
  stagingSmoke(): Promise<{ passed: boolean }> { return Promise.reject(notImplemented("VerificationService.stagingSmoke")); }
  rollback(): Promise<{ passed: boolean }> { return Promise.reject(notImplemented("VerificationService.rollback")); }
  monitoringAlert(): Promise<{ delivered: boolean }> { return Promise.reject(notImplemented("VerificationService.monitoringAlert")); }
  kimiEndToEnd(surface: "cli" | "web"): Promise<{ oauth: boolean; tools: boolean }> { return Promise.reject(notImplemented("VerificationService.kimiEndToEnd")); }
}

export function createConnectorTestHarness(): {
  oauth: OAuthService;
  github: GithubGateway;
  webhooks: WebhookService;
  retention: RetentionService;
  runtime: ConnectorRuntime;
  verification: VerificationService;
  fixedNow: IsoInstant;
} {
  throw notImplemented("createConnectorTestHarness");
}

export * from "./contracts.js";
