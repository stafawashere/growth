import type {
   AttemptResult,
   BudgetsPayload,
   Confidence,
   FeedbackPayload,
   ProgressPayload,
   ProvidersPayload,
   ServedItem,
   SessionPayload,
   SettingsPayload
} from "./types";

export class ApiError extends Error {
   status: number;
   detail: string;

   constructor(status: number, detail: string) {
      super(detail);

      this.name = "ApiError";
      this.status = status;
      this.detail = detail;
   }
}

export interface NextItemResponse {
   item: ServedItem | null;
}

export interface ConfidenceResult {
   id: string;
   confidence: Confidence | null;
}

export interface ErrorNoteResult {
   id: string;
   error_note: string | null;
}

export interface SelfExplanationResult {
   attempt_id: string;
   self_explanation: string;
}

export interface CloseResult {
   id: string;
   ended_at: string | null;
}

export interface MePayload {
   id: string;
   display_name: string | null;
   exam_date: string;
   purge_after: string | null;
}

export interface PurgeResult {
   purged: boolean;
   deleted: unknown;
}

export interface AttemptAnswer {
   option_id?: string;
   mathjson?: unknown;
   units?: string;
}

export interface OpenSessionFields {
   mode?: string;
   sub_mode?: string;
   today?: string;
}

export interface SubmitAttemptFields {
   item_id: string;
   answer?: AttemptAnswer;
   elapsed_ms?: number;
   today?: string;
   confidence?: Confidence;
}

export interface SubmitConfidenceFields {
   confidence: Confidence;
   today?: string;
}

export interface CloseSessionFields {
   today?: string;
}

export interface RequestPurgeFields {
   confirmation: string;
   reauth_token?: string;
}

export interface SubmitSelfExplanationFields {
   answer: string;
}

export interface UpdateSettingsFields {
   exam_date?: string;
   purge_after?: string;
}

export interface UpdateBudgetFields {
   role: string;
   cap_usd: number | null;
   cap_tokens: number | null;
   reauth_token: string;
}

export interface RequestExportFields {
   reauth_token: string;
}

export interface ExportJob {
   id: string;
   status: string;
   created_at: string;
}

export interface ReauthBegin {
   challenge_id: string;
   options: unknown;
}

export interface FinishReauthFields {
   challenge_id: string;
   credential: unknown;
}

export interface ReauthFinish {
   reauth_token: string;
}

async function detailFrom(response: Response) {
   try {
      const body = await response.json();
      const hasDetail = typeof body === "object" && body !== null && "detail" in body;

      if (hasDetail) {
         return String((body as { detail: unknown }).detail);
      }
   } catch {
      // response carried no JSON body to read a detail from
   }

   return response.statusText;
}

async function request(path: string, init?: RequestInit) {
   const hasBody = init !== undefined && init.body !== undefined;
   const headers = hasBody ? { "Content-Type": "application/json", ...init?.headers } : init?.headers;

   const response = await fetch(path, {
      ...init,
      credentials: "include",
      headers
   });

   if (!response.ok) {
      throw new ApiError(response.status, await detailFrom(response));
   }

   return response;
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
   const response = await request(path, init);

   return response.json() as Promise<T>;
}

function jsonInit(method: string, fields?: unknown) {
   const hasFields = fields !== undefined;

   return {
      method,
      body: hasFields ? JSON.stringify(fields) : undefined
   };
}

export function openSession(fields?: OpenSessionFields) {
   return requestJson<SessionPayload>("/sessions", jsonInit("POST", fields ?? {}));
}

export function readSession(sessionId: string) {
   return requestJson<SessionPayload>(`/sessions/${sessionId}`);
}

export function readNextItem(sessionId: string) {
   return requestJson<NextItemResponse>(`/sessions/${sessionId}/next`);
}

export function submitAttempt(sessionId: string, fields: SubmitAttemptFields) {
   return requestJson<AttemptResult>(`/sessions/${sessionId}/attempts`, jsonInit("POST", fields));
}

export function readFeedback(sessionId: string, attemptId: string) {
   return requestJson<FeedbackPayload>(`/sessions/${sessionId}/attempts/${attemptId}/feedback`);
}

export function submitConfidence(sessionId: string, attemptId: string, fields: SubmitConfidenceFields) {
   return requestJson<ConfidenceResult>(
      `/sessions/${sessionId}/attempts/${attemptId}/confidence`,
      jsonInit("POST", fields)
   );
}

export function submitErrorNote(sessionId: string, attemptId: string, note: string) {
   return requestJson<ErrorNoteResult>(
      `/sessions/${sessionId}/attempts/${attemptId}/error-note`,
      jsonInit("POST", { note })
   );
}

export function closeSession(sessionId: string, fields?: CloseSessionFields) {
   return requestJson<CloseResult>(`/sessions/${sessionId}/close`, jsonInit("POST", fields ?? {}));
}

export function readMe() {
   return requestJson<MePayload>("/me");
}

export function requestPurge(fields: RequestPurgeFields) {
   return requestJson<PurgeResult>("/purge", jsonInit("POST", fields));
}

export function submitSelfExplanation(sessionId: string, attemptId: string, fields: SubmitSelfExplanationFields) {
   return requestJson<SelfExplanationResult>(
      `/sessions/${sessionId}/attempts/${attemptId}/self-explanation`,
      jsonInit("POST", fields)
   );
}

export function readProgress() {
   return requestJson<ProgressPayload>("/progress");
}

export function readSettings() {
   return requestJson<SettingsPayload>("/settings");
}

export function updateSettings(fields: UpdateSettingsFields) {
   return requestJson<SettingsPayload>("/settings", jsonInit("PUT", fields));
}

export function readProviders() {
   return requestJson<ProvidersPayload>("/settings/providers");
}

export function readBudgets() {
   return requestJson<BudgetsPayload>("/settings/budgets");
}

export function updateBudget(fields: UpdateBudgetFields) {
   return requestJson<BudgetsPayload>("/settings/budgets", jsonInit("PUT", fields));
}

export function requestExport(fields: RequestExportFields) {
   return requestJson<ExportJob>("/export", jsonInit("POST", fields));
}

export async function readExport(exportId: string) {
   const response = await request(`/export/${exportId}`);

   return response.blob();
}

export function beginReauth() {
   return requestJson<ReauthBegin>("/auth/reauth/begin", jsonInit("POST", {}));
}

export function finishReauth(fields: FinishReauthFields) {
   return requestJson<ReauthFinish>("/auth/reauth/finish", jsonInit("POST", fields));
}

interface CredentialDescriptorJson {
   id: string;
   type: string;
   transports?: string[];
}

interface RequestOptionsJson {
   challenge: string;
   timeout?: number;
   rpId?: string;
   allowCredentials?: CredentialDescriptorJson[];
   userVerification?: UserVerificationRequirement;
}

function bytesFromBase64Url(encoded: string) {
   const base64 = encoded.replace(/-/g, "+").replace(/_/g, "/");
   const padding = "=".repeat((4 - (base64.length % 4)) % 4);
   const binary = atob(base64 + padding);

   return Uint8Array.from(binary, (character) => character.charCodeAt(0));
}

function base64UrlFromBuffer(buffer: ArrayBuffer) {
   const binary = String.fromCharCode(...new Uint8Array(buffer));

   return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function hexFromBuffer(buffer: ArrayBuffer) {
   return Array.from(new Uint8Array(buffer), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

function publicKeyRequestFrom(options: RequestOptionsJson): PublicKeyCredentialRequestOptions {
   const allowed = options.allowCredentials ?? [];

   return {
      challenge: bytesFromBase64Url(options.challenge),
      timeout: options.timeout,
      rpId: options.rpId,
      userVerification: options.userVerification,
      allowCredentials: allowed.map((descriptor) => ({
         id: bytesFromBase64Url(descriptor.id),
         type: "public-key",
         transports: descriptor.transports as AuthenticatorTransport[] | undefined
      }))
   };
}

/* The assertion in the JSON form app/auth/webauthn.py LibraryVerifier hands to
   verify_authentication_response, plus credential_id in hex, which app/auth/service.py
   credential_for reads to find the stored passkey. */
function assertionJson(credential: PublicKeyCredential) {
   const response = credential.response as AuthenticatorAssertionResponse;
   const userHandle = response.userHandle;

   return {
      credential_id: hexFromBuffer(credential.rawId),
      id: credential.id,
      rawId: base64UrlFromBuffer(credential.rawId),
      type: credential.type,
      response: {
         clientDataJSON: base64UrlFromBuffer(response.clientDataJSON),
         authenticatorData: base64UrlFromBuffer(response.authenticatorData),
         signature: base64UrlFromBuffer(response.signature),
         userHandle: userHandle === null ? null : base64UrlFromBuffer(userHandle)
      },
      clientExtensionResults: credential.getClientExtensionResults()
   };
}

export class ReauthDeclined extends Error {
   constructor() {
      super("the authenticator returned no assertion");

      this.name = "ReauthDeclined";
   }
}

/* The re-authentication ceremony of app/api/routes/auth.py, end to end: the returned token is
   single use, so each consequential action runs this again. */
export async function reauthenticate() {
   const begun = await beginReauth();
   const publicKey = publicKeyRequestFrom(begun.options as RequestOptionsJson);
   const credential = await navigator.credentials.get({ publicKey });
   const hasAssertion = credential !== null;

   if (!hasAssertion) {
      throw new ReauthDeclined();
   }

   const finished = await finishReauth({
      challenge_id: begun.challenge_id,
      credential: assertionJson(credential as PublicKeyCredential)
   });

   return finished.reauth_token;
}

export interface CeremonyBegin {
   challenge_id: string;
   options: unknown;
}

export interface FinishRegistrationFields {
   challenge_id: string;
   credential: unknown;
   display_name?: string;
}

export interface RegisteredUser {
   id: string;
   display_name: string | null;
   exam_date: string;
   purge_after: string | null;
}

export interface RegistrationFinish {
   user: RegisteredUser;
   seeded_skill_states: number;
   recovery_code: string;
}

export interface FinishLoginFields {
   challenge_id: string;
   credential: unknown;
}

export interface LoginFinish {
   user_id: string;
}

export function beginRegistration() {
   return requestJson<CeremonyBegin>("/auth/passkey/register/begin", jsonInit("POST", {}));
}

export function finishRegistration(fields: FinishRegistrationFields) {
   return requestJson<RegistrationFinish>("/auth/passkey/register/finish", jsonInit("POST", fields));
}

export function beginLogin() {
   return requestJson<CeremonyBegin>("/auth/passkey/login/begin", jsonInit("POST", {}));
}

export function finishLogin(fields: FinishLoginFields) {
   return requestJson<LoginFinish>("/auth/passkey/login/finish", jsonInit("POST", fields));
}

interface CreationOptionsJson {
   rp: PublicKeyCredentialRpEntity;
   user: { id: string; name: string; displayName: string };
   challenge: string;
   pubKeyCredParams: PublicKeyCredentialParameters[];
   timeout?: number;
   excludeCredentials?: CredentialDescriptorJson[];
   authenticatorSelection?: AuthenticatorSelectionCriteria;
   attestation?: AttestationConveyancePreference;
}

function publicKeyCreationFrom(options: CreationOptionsJson): PublicKeyCredentialCreationOptions {
   const excluded = options.excludeCredentials ?? [];

   return {
      rp: options.rp,
      user: {
         id: bytesFromBase64Url(options.user.id),
         name: options.user.name,
         displayName: options.user.displayName
      },
      challenge: bytesFromBase64Url(options.challenge),
      pubKeyCredParams: options.pubKeyCredParams,
      timeout: options.timeout,
      authenticatorSelection: options.authenticatorSelection,
      attestation: options.attestation,
      excludeCredentials: excluded.map((descriptor) => ({
         id: bytesFromBase64Url(descriptor.id),
         type: "public-key",
         transports: descriptor.transports as AuthenticatorTransport[] | undefined
      }))
   };
}

/* The attestation in the JSON form parse_registration_credential_json reads, which
   app/auth/webauthn.py LibraryVerifier hands the credential to unchanged. */
function attestationJson(credential: PublicKeyCredential) {
   const response = credential.response as AuthenticatorAttestationResponse;
   const canListTransports = typeof response.getTransports === "function";

   return {
      id: credential.id,
      rawId: base64UrlFromBuffer(credential.rawId),
      type: credential.type,
      authenticatorAttachment: credential.authenticatorAttachment ?? null,
      response: {
         clientDataJSON: base64UrlFromBuffer(response.clientDataJSON),
         attestationObject: base64UrlFromBuffer(response.attestationObject),
         transports: canListTransports ? response.getTransports() : []
      },
      clientExtensionResults: credential.getClientExtensionResults()
   };
}

export class PasskeyDeclined extends Error {
   constructor() {
      super("the authenticator returned no credential");

      this.name = "PasskeyDeclined";
   }
}

export async function registerPasskey() {
   const begun = await beginRegistration();
   const publicKey = publicKeyCreationFrom(begun.options as CreationOptionsJson);
   const credential = await navigator.credentials.create({ publicKey });
   const hasCredential = credential !== null;

   if (!hasCredential) {
      throw new PasskeyDeclined();
   }

   return finishRegistration({
      challenge_id: begun.challenge_id,
      credential: attestationJson(credential as PublicKeyCredential)
   });
}

export interface FinishRecoveryRegistrationFields {
   challenge_id: string;
   credential: unknown;
   recovery_code: string;
}

export interface RecoveryRegistrationFinish {
   user_id: string;
   credential_id: string;
   recovery_code: string;
}

export function beginRecoveryRegistration() {
   return requestJson<CeremonyBegin>("/auth/recovery/register/begin", jsonInit("POST", {}));
}

export function finishRecoveryRegistration(fields: FinishRecoveryRegistrationFields) {
   return requestJson<RecoveryRegistrationFinish>("/auth/recovery/register/finish", jsonInit("POST", fields));
}

export async function registerPasskeyWithRecoveryCode(recoveryCode: string) {
   const begun = await beginRecoveryRegistration();
   const publicKey = publicKeyCreationFrom(begun.options as CreationOptionsJson);
   const credential = await navigator.credentials.create({ publicKey });
   const hasCredential = credential !== null;

   if (!hasCredential) {
      throw new PasskeyDeclined();
   }

   return finishRecoveryRegistration({
      challenge_id: begun.challenge_id,
      credential: attestationJson(credential as PublicKeyCredential),
      recovery_code: recoveryCode
   });
}

export interface AuthStatus {
   user_exists: boolean;
}

export function readAuthStatus() {
   return requestJson<AuthStatus>("/auth/status");
}

export interface FinishAddPasskeyFields {
   challenge_id: string;
   credential: unknown;
   reauth_token: string;
}

export interface AddPasskeyFinish {
   credential_id: string;
}

export function beginAddPasskey() {
   return requestJson<CeremonyBegin>("/auth/passkey/add/begin", jsonInit("POST", {}));
}

export function finishAddPasskey(fields: FinishAddPasskeyFields) {
   return requestJson<AddPasskeyFinish>("/auth/passkey/add/finish", jsonInit("POST", fields));
}

export async function addPasskey() {
   /* Ruled 2026-09-23: adding a passkey now needs a fresh re-authentication, the same proof
      the other consequential actions require, because a credential it mints outlives the
      session that requested it. */
   const begun = await beginAddPasskey();
   const publicKey = publicKeyCreationFrom(begun.options as CreationOptionsJson);
   const credential = await navigator.credentials.create({ publicKey });
   const hasCredential = credential !== null;

   if (!hasCredential) {
      throw new PasskeyDeclined();
   }

   const reauthToken = await reauthenticate();

   return finishAddPasskey({
      challenge_id: begun.challenge_id,
      credential: attestationJson(credential as PublicKeyCredential),
      reauth_token: reauthToken
   });
}

export async function signInWithPasskey() {
   const begun = await beginLogin();
   const publicKey = publicKeyRequestFrom(begun.options as RequestOptionsJson);
   const credential = await navigator.credentials.get({ publicKey });
   const hasAssertion = credential !== null;

   if (!hasAssertion) {
      throw new PasskeyDeclined();
   }

   return finishLogin({
      challenge_id: begun.challenge_id,
      credential: assertionJson(credential as PublicKeyCredential)
   });
}
