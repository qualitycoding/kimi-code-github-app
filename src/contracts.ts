export type IsoInstant = string;
export type JsonObject = Record<string, unknown>;

export interface PageRequest {
  readonly cursor?: string;
  readonly limit?: number;
}

export interface Page<T> {
  readonly items: readonly T[];
  readonly nextCursor: string | null;
  readonly truncated: boolean;
}

export interface Repository {
  readonly id: number;
  readonly owner: string;
  readonly name: string;
  readonly fullName: string;
  readonly private: boolean;
  readonly defaultBranch: string;
}

export interface RepositoryRef {
  readonly owner: string;
  readonly repository: string;
  readonly ref: string;
}

export interface TreeEntry {
  readonly path: string;
  readonly kind: "blob" | "tree" | "commit";
  readonly sha: string;
  readonly size: number | null;
}

export interface TreeResult extends Page<TreeEntry> {
  readonly resolvedCommit: string;
  readonly upstreamTruncated: boolean;
  readonly truncationReason: "none" | "connector_limit" | "github_limit" | "both";
}

export interface FileReadRequest extends RepositoryRef {
  readonly path: string;
  readonly byteOffset?: number;
  readonly lineOffset?: number;
}

export interface FileReadResult {
  readonly path: string;
  readonly resolvedCommit: string;
  readonly size: number;
  readonly encoding: "utf-8";
  readonly content: string;
  readonly byteOffset: number;
  readonly lineOffset: number;
  readonly nextByteOffset: number | null;
  readonly nextLineOffset: number | null;
  readonly truncated: boolean;
  readonly truncationReason: "none" | "byte_limit" | "line_limit" | "both";
}

export interface Principal {
  readonly connectorSubject: string;
  readonly githubUserId: string;
  readonly resource: string;
}

export interface ClientMetadata {
  readonly clientId: string;
  readonly clientName: string;
  readonly redirectUris: readonly string[];
  readonly grantTypes: readonly string[];
  readonly responseTypes: readonly string[];
  readonly tokenEndpointAuthMethod: "none";
}

export interface AuthorizationRequest {
  readonly clientId: string;
  readonly redirectUri: string;
  readonly responseType: "code";
  readonly codeChallenge: string;
  readonly codeChallengeMethod: "S256";
  readonly state: string;
  readonly resource: string;
  readonly scope?: string;
}

export interface ConsentDecision {
  readonly approved: boolean;
  readonly consentId: string;
}

export interface TokenGrant {
  readonly accessToken: string;
  readonly tokenType: "Bearer";
  readonly expiresIn: 3600;
  readonly refreshToken: string;
  readonly scope: string;
  readonly resource: string;
}

export interface RuntimeHealth {
  readonly status: "ok" | "degraded" | "fail";
  readonly checks: Readonly<Record<string, "ok" | "fail">>;
}

export interface BenchmarkRequest {
  readonly concurrency: 50;
  readonly runs: 5;
  readonly mockedGithub: true;
}

export interface BenchmarkResult {
  readonly p95ConnectorLatencyMs: number;
  readonly errorFraction: number;
  readonly peakServiceMemoryMiB: number;
  readonly runP95ValuesMs: readonly number[];
  readonly variancePercent: number;
}
