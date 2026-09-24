import type {
   AssessmentAnswer,
   AssessmentResult,
   AssessmentSession,
   AssessmentShape,
   AttemptResult,
   BudgetsPayload,
   CalibrationPayload,
   CheckResult,
   CheckUnitsPayload,
   CheckpointsPayload,
   CheckpointView,
   Confidence,
   DiagnosticResult,
   DiagnosticServedItem,
   ExperimentsPayload,
   ExperimentState,
   DisputeResult,
   FeedbackPayload,
   FrqAttempt,
   FrqUnitsPayload,
   GradingsPayload,
   HighlightRange,
   MasteryMapPayload,
   MetricsPayload,
   MockHistoryPayload,
   PartKey,
   PhotoVerdict,
   ProbeAdministration,
   ProbePayload,
   ProbeServedItem,
   ProgressPayload,
   ProvidersPayload,
   ReadBack,
   RepresentationMatrixPayload,
   ReviewPayload,
   SavedQuestion,
   ServedItem,
   SessionPayload,
   SettingsPayload,
   TimedKind,
   UnfinishedPayload,
   UnitCheckPayload
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

/* app/api/routes/sessions.py next_diagnostic_item. Once diagnostic_finished is true the item is
   null and the server has already closed the session. */
export interface DiagnosticNextItemResponse {
   item: DiagnosticServedItem | null;
   diagnostic_finished: boolean;
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

/* not_learned is the diagnostic's "I have not learned this yet" (app/session/diagnostic_session.py
   record_answer), sent in place of an answer. */
export interface AttemptAnswer {
   option_id?: string;
   mathjson?: unknown;
   units?: string;
   not_learned?: boolean;
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

/* The evaluation routes of app/api/routes/evaluation.py read today from the body on a write and
   from the query on a read, and fall back to the server's own date without it. */
export interface DayFields {
   today?: string;
}

export interface SetExperimentFields {
   state: ExperimentState;
   today?: string;
}

export interface ScoreCheckpointPartFields {
   record_id: string;
   points_earned: number;
   today?: string;
}

export interface ProbeAnswer {
   option_id?: string;
   mathjson?: unknown;
}

export interface AnswerProbeItemFields {
   item_id: string;
   answer: ProbeAnswer;
   elapsed_ms?: number;
   today?: string;
}

export interface ProbeNextItemResponse {
   item: ProbeServedItem | null;
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

function withToday(path: string, today?: string) {
   const hasDay = today !== undefined;

   return hasDay ? `${path}?today=${encodeURIComponent(today)}` : path;
}

export function openSession(fields?: OpenSessionFields) {
   return requestJson<SessionPayload>("/sessions", jsonInit("POST", fields ?? {}));
}

export function readSession(sessionId: string) {
   return requestJson<SessionPayload>(`/sessions/${sessionId}`);
}

export function readNextItem(sessionId: string) {
   return requestJson<NextItemResponse | DiagnosticNextItemResponse>(`/sessions/${sessionId}/next`);
}

export function openDiagnostic() {
   return openSession({ mode: "diagnostic" });
}

export function readDiagnostic(sessionId: string) {
   return requestJson<DiagnosticResult>(`/sessions/${sessionId}/diagnostic`);
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

export function readCalibration() {
   return requestJson<CalibrationPayload>("/progress/calibration");
}

export function readMasteryMap() {
   return requestJson<MasteryMapPayload>("/progress/mastery");
}

export function readMetrics(today?: string) {
   return requestJson<MetricsPayload>(withToday("/progress/metrics", today));
}

export function readRepresentations() {
   return requestJson<RepresentationMatrixPayload>("/progress/representations");
}

export function readReview() {
   return requestJson<ReviewPayload>("/review");
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

export function readExperiments() {
   return requestJson<ExperimentsPayload>("/settings/experiments");
}

export function setExperimentState(name: string, fields: SetExperimentFields) {
   return requestJson<ExperimentsPayload>(`/settings/experiments/${name}`, jsonInit("POST", fields));
}

export function readCheckpoints(today?: string) {
   return requestJson<CheckpointsPayload>(withToday("/checkpoints", today));
}

export function startCheckpoint(fields?: DayFields) {
   return requestJson<CheckpointView>("/checkpoints", jsonInit("POST", fields ?? {}));
}

export function readCheckpoint(checkpointId: string) {
   return requestJson<CheckpointView>(`/checkpoints/${checkpointId}`);
}

export function scoreCheckpointPart(checkpointId: string, fields: ScoreCheckpointPartFields) {
   return requestJson<CheckpointView>(`/checkpoints/${checkpointId}/scores`, jsonInit("POST", fields));
}

export function finishCheckpoint(checkpointId: string, fields?: DayFields) {
   return requestJson<CheckpointView>(`/checkpoints/${checkpointId}/finish`, jsonInit("POST", fields ?? {}));
}

export function readProbe(today?: string) {
   return requestJson<ProbePayload>(withToday("/probe", today));
}

export function startProbe(fields?: DayFields) {
   return requestJson<ProbeAdministration>("/probe", jsonInit("POST", fields ?? {}));
}

export function readNextProbeItem(administrationId: string) {
   return requestJson<ProbeNextItemResponse>(`/probe/${administrationId}/next`);
}

export function answerProbeItem(administrationId: string, fields: AnswerProbeItemFields) {
   return requestJson<ProbeAdministration>(`/probe/${administrationId}/answers`, jsonInit("POST", fields));
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

export type CaptureMode = "photo" | "typed";

export interface PhotoFields {
   media_type: string;
   data_base64: string;
}

export interface ConfirmReadBackFields {
   read_back?: ReadBack;
   confidence?: Confidence;
}

export interface TypedAnswerFields {
   read_back: ReadBack;
   confidence?: Confidence;
}

export function readFrqUnits() {
   return requestJson<FrqUnitsPayload>("/frq/units");
}

export function openUnitCheck(unitId: string) {
   return requestJson<UnitCheckPayload>("/frq/unit-checks", jsonInit("POST", { unit_id: unitId }));
}

export function readUnitCheck(sessionId: string) {
   return requestJson<UnitCheckPayload>(`/frq/unit-checks/${encodeURIComponent(sessionId)}`);
}

export function startFrqAttempt(sessionId: string, itemId: string, captureMode: CaptureMode) {
   const path = `/sessions/${encodeURIComponent(sessionId)}/frq/${encodeURIComponent(itemId)}/attempts`;

   return requestJson<FrqAttempt>(path, jsonInit("POST", { capture_mode: captureMode }));
}

export function bookletAddress(attemptId: string) {
   return `/attempts/${encodeURIComponent(attemptId)}/booklet.png`;
}

export function photoAddress(attemptId: string, imageId: string) {
   return `/attempts/${encodeURIComponent(attemptId)}/images/${encodeURIComponent(imageId)}`;
}

export function uploadPhoto(attemptId: string, fields: PhotoFields) {
   return requestJson<PhotoVerdict>(`/attempts/${encodeURIComponent(attemptId)}/images`, jsonInit("POST", fields));
}

export function requestReadBack(attemptId: string) {
   return requestJson<FrqAttempt>(`/attempts/${encodeURIComponent(attemptId)}/transcription`, jsonInit("POST"));
}

export function readReadBack(attemptId: string) {
   return requestJson<FrqAttempt>(`/attempts/${encodeURIComponent(attemptId)}/transcription`);
}

export function confirmReadBack(attemptId: string, fields: ConfirmReadBackFields) {
   const path = `/attempts/${encodeURIComponent(attemptId)}/transcription/confirm`;

   return requestJson<FrqAttempt>(path, jsonInit("POST", fields));
}

export function submitTypedAnswer(attemptId: string, fields: TypedAnswerFields) {
   return requestJson<FrqAttempt>(`/attempts/${encodeURIComponent(attemptId)}/typed`, jsonInit("POST", fields));
}

export function readGradings(attemptId: string) {
   return requestJson<GradingsPayload>(`/attempts/${encodeURIComponent(attemptId)}/gradings`);
}

export function askForReread(gradingId: string, reason?: string) {
   const path = `/gradings/${encodeURIComponent(gradingId)}/dispute`;

   return requestJson<DisputeResult>(path, jsonInit("POST", { reason: reason ?? "" }));
}


export interface OpenMockFields {
   capture_mode: CaptureMode;
}

export interface OpenDrillFields {
   part: PartKey;
   capture_mode: CaptureMode;
}

/* visit_ms is the length of the visit that just ended, sent whenever the student leaves a
   question. The server never answers with correctness here. */
export interface SaveQuestionFields {
   answer?: AssessmentAnswer | null;
   visit_ms?: number;
   marked?: boolean;
   eliminated?: string[];
   notes?: string;
   highlights?: HighlightRange[];
   confidence?: Confidence | null;
}

function timedPath(kind: TimedKind, sessionId: string) {
   return `/${kind}/${encodeURIComponent(sessionId)}`;
}

function partPath(kind: TimedKind, sessionId: string, position: number) {
   return `${timedPath(kind, sessionId)}/sections/${position}`;
}

export function readUnfinished() {
   return requestJson<UnfinishedPayload>("/assessments/unfinished");
}

export function readAssessmentShape() {
   return requestJson<AssessmentShape>("/assessments/shape");
}

export function openMock(fields: OpenMockFields) {
   return requestJson<AssessmentSession>("/mocks", jsonInit("POST", fields));
}

export function openDrill(fields: OpenDrillFields) {
   return requestJson<AssessmentSession>("/drills", jsonInit("POST", fields));
}

export function readTimedSession(kind: TimedKind, sessionId: string) {
   return requestJson<AssessmentSession>(timedPath(kind, sessionId));
}

export function startPart(kind: TimedKind, sessionId: string, position: number) {
   return requestJson<AssessmentSession>(`${partPath(kind, sessionId, position)}/start`, jsonInit("POST"));
}

export function submitPart(kind: TimedKind, sessionId: string, position: number) {
   return requestJson<AssessmentSession>(`${partPath(kind, sessionId, position)}/submit`, jsonInit("POST"));
}

export function saveQuestion(kind: TimedKind, sessionId: string, position: number, number: number, fields: SaveQuestionFields) {
   const path = `${partPath(kind, sessionId, position)}/questions/${number}`;

   return requestJson<SavedQuestion>(path, jsonInit("PUT", fields));
}

export function readTimedResult(kind: TimedKind, sessionId: string) {
   return requestJson<AssessmentResult>(`${timedPath(kind, sessionId)}/result`);
}

export function finishMock(sessionId: string) {
   return requestJson<AssessmentResult>(`${timedPath("mocks", sessionId)}/finish`, jsonInit("POST"));
}

export function readMockHistory() {
   return requestJson<MockHistoryPayload>("/mocks");
}

export function readCheckUnits() {
   return requestJson<CheckUnitsPayload>("/unit-checks/units");
}

export function openCheck(unitId: string) {
   return requestJson<AssessmentSession>("/unit-checks", jsonInit("POST", { unit_id: unitId }));
}

export function readCheck(sessionId: string) {
   return requestJson<AssessmentSession>(`/unit-checks/${encodeURIComponent(sessionId)}`);
}

export function saveCheckQuestion(sessionId: string, number: number, fields: SaveQuestionFields) {
   const path = `/unit-checks/${encodeURIComponent(sessionId)}/questions/${number}`;

   return requestJson<SavedQuestion>(path, jsonInit("PUT", fields));
}

export function submitCheck(sessionId: string, fields?: DayFields) {
   return requestJson<CheckResult>(`/unit-checks/${encodeURIComponent(sessionId)}/submit`, jsonInit("POST", fields ?? {}));
}