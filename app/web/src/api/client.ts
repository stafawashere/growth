import type {
   AgentConversationDeleted,
   AgentConversationPayload,
   AgentConversationsPayload,
   AgentMemoriesPayload,
   AgentMemoryCleared,
   AgentMemoryDeleted,
   AgentMemoryEntry,
   AgentProfilePayload,
   AgentSettingsPayload,
   AgentTurnBody,
   MasteryNodeState,
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
   LessonBand,
   LessonCheckAnswerBody,
   LessonCheckVerdict,
   LessonEventBody,
   LessonPlanPayload,
   LessonPromptAnswerBody,
   LessonPromptVerdict,
   LessonReason,
   LessonRecordPayload,
   LessonStatePayload,
   LibraryPayload,
   GradingsPayload,
   HighlightRange,
   MasteryMapPayload,
   PacePayload,
   MetricsPayload,
   MockHistoryPayload,
   NoticesPayload,
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
   ServedEntry,
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
   item: ServedEntry | null;
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
   username?: string | null;
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

/* FastAPI's validation errors carry a list of objects in detail; each one's msg is the sentence. */
function readableDetail(detail: unknown) {
   const isList = Array.isArray(detail);

   if (!isList) {
      return String(detail);
   }

   return (detail as unknown[])
      .map((entry) => {
         const hasMessage = typeof entry === "object" && entry !== null && "msg" in entry;

         return hasMessage ? String((entry as { msg: unknown }).msg) : String(entry);
      })
      .join("; ");
}

/* A 401 from any route but the auth routes and /me means the session ended while the student was
   working. The shell listens for this and asks /me whether that is so, rather than trusting one
   refusal: a refused re-authentication also answers 401 and must not sign anyone out. */
export const SESSION_ENDED_EVENT = "growth:session-ended";

function reportsSessionEnded(path: string, status: number) {
   const isUnauthorised = status === 401;
   const isAccountCheck = path.startsWith("/auth/") || path === "/me";

   return isUnauthorised && !isAccountCheck;
}

async function detailFrom(response: Response) {
   try {
      const body = await response.json();
      const hasDetail = typeof body === "object" && body !== null && "detail" in body;

      if (hasDetail) {
         return readableDetail((body as { detail: unknown }).detail);
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
      const sessionEnded = reportsSessionEnded(path, response.status);

      if (sessionEnded) {
         window.dispatchEvent(new CustomEvent(SESSION_ENDED_EVENT));
      }

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

/* app/api/routes/sessions.py skip_diagnostic_unit: "I have not learned this yet" for the item on
   screen and every later item of its unit, answered as it is served. Replies as readNextItem does. */
export function skipDiagnosticUnit(sessionId: string, fields: { item_id: string; elapsed_ms?: number; today?: string }) {
   return requestJson<DiagnosticNextItemResponse>(`/sessions/${sessionId}/diagnostic/skip-unit`, jsonInit("POST", fields));
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

export function renameDisplayName(displayName: string) {
   return requestJson<MePayload>("/me", jsonInit("PUT", { display_name: displayName }));
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

export interface SkillPrerequisite {
   id: string;
   name: string;
   kind: "hard" | "supporting";
   state: MasteryNodeState | null;
}

export interface SkillDetail {
   skill_id: string;
   name: string;
   unit_id: string | null;
   state: MasteryNodeState;
   assumed: boolean;
   last_success_on: string | null;
   days_since_success: number | null;
   description: string | null;
   mastered_if: string | null;
   partially_mastered_if: string | null;
   prerequisites: SkillPrerequisite[];
   concept_id: string | null;
   lesson_id: string | null;
}

export function readSkill(skillId: string) {
   return requestJson<SkillDetail>(`/progress/skills/${encodeURIComponent(skillId)}`);
}

export function readPace() {
   return requestJson<PacePayload>("/progress/pace");
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

export interface StudyPlanPayload {
   study_plan: string | null;
}

export function readStudyPlan() {
   return requestJson<StudyPlanPayload>("/settings/study-plan");
}

export function updateStudyPlan(studyPlan: string) {
   return requestJson<StudyPlanPayload>("/settings/study-plan", jsonInit("PUT", { study_plan: studyPlan }));
}

export function readProviders() {
   return requestJson<ProvidersPayload>("/settings/providers");
}

/* app/api/routes/notices.py: the signed-in student's AI call notices newer than the given id. */
export function readNotices(after: number) {
   return requestJson<NoticesPayload>(`/notices?after=${encodeURIComponent(String(after))}`);
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

export interface ReauthFields {
   password: string;
}

export interface ReauthResult {
   reauth_token: string;
}

/* A re-authentication token is single use, so each consequential action asks for the password
   again and spends the token it gets back. */
export function reauthenticate(fields: ReauthFields) {
   return requestJson<ReauthResult>("/auth/reauth", jsonInit("POST", fields));
}

export interface SignUpFields {
   username: string;
   password: string;
}

export interface RegisteredUser {
   id: string;
   display_name: string | null;
   exam_date: string;
   purge_after: string | null;
}

export interface SignUpResult {
   user: RegisteredUser;
   seeded_skill_states: number;
   recovery_code: string;
}

export function signUp(fields: SignUpFields) {
   return requestJson<SignUpResult>("/auth/signup", jsonInit("POST", fields));
}

export interface SignInFields {
   username: string;
   password: string;
}

export interface SignInResult {
   user_id: string;
}

export function signIn(fields: SignInFields) {
   return requestJson<SignInResult>("/auth/login", jsonInit("POST", fields));
}

export interface SignOutResult {
   logged_out: boolean;
}

export function signOut() {
   return requestJson<SignOutResult>("/auth/logout", jsonInit("POST", {}));
}

export interface ChangePasswordFields {
   current_password: string;
   new_password: string;
   reauth_token: string;
}

export interface ChangePasswordResult {
   password_changed: boolean;
}

export function changePassword(fields: ChangePasswordFields) {
   return requestJson<ChangePasswordResult>("/auth/password/change", jsonInit("POST", fields));
}

/* username is read only while the account has none, which is the state an account carried over
   from passkeys starts in. */
export interface RecoveryResetFields {
   recovery_code: string;
   new_password: string;
   username?: string;
}

export interface RecoveryResetResult {
   user_id: string;
   recovery_code: string;
}

export function resetWithRecoveryCode(fields: RecoveryResetFields) {
   return requestJson<RecoveryResetResult>("/auth/recovery/reset", jsonInit("POST", fields));
}

export interface RotateRecoveryResult {
   recovery_code: string;
}

export function rotateRecoveryCode(reauthToken: string) {
   return requestJson<RotateRecoveryResult>("/auth/recovery/rotate", jsonInit("POST", { reauth_token: reauthToken }));
}

/* needs_password is served only to a caller on this machine, so its absence means no more than
   that the server did not say. */
export interface AuthStatus {
   user_exists: boolean;
   needs_password?: boolean;
}

export function readAuthStatus() {
   return requestJson<AuthStatus>("/auth/status");
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

export interface PhotoDeleted {
   deleted: string;
}

export interface PhotosDeleted {
   deleted: number;
}

export function deleteEveryPhoto() {
   return requestJson<PhotosDeleted>("/frq/photos", jsonInit("DELETE"));
}

export function deletePhoto(attemptId: string, imageId: string) {
   return requestJson<PhotoDeleted>(photoAddress(attemptId, imageId), jsonInit("DELETE"));
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
/* Lessons, app/api/routes/lessons.py. A check id carries the lesson id and a # (LSN-CON-02013#chk-1),
   so every id is encoded into its path segment. */
function lessonPath(lessonId: string) {
   return `/lessons/${encodeURIComponent(lessonId)}`;
}

export function readLibrary(unit?: string) {
   const query = unit === undefined ? "" : `?unit=${encodeURIComponent(unit)}`;

   return requestJson<LibraryPayload>(`/lessons${query}`);
}

export function readLesson(lessonId: string, version?: number) {
   const query = version === undefined ? "" : `?version=${version}`;

   return requestJson<LessonRecordPayload>(`${lessonPath(lessonId)}${query}`);
}

export function readLessonPlan(lessonId: string, band: LessonBand, reason?: LessonReason) {
   const query = reason === undefined ? `?band=${band}` : `?band=${band}&reason=${encodeURIComponent(reason)}`;

   return requestJson<LessonPlanPayload>(`${lessonPath(lessonId)}/plan${query}`);
}

export function postLessonEvent(lessonId: string, body: LessonEventBody) {
   return requestJson<LessonStatePayload>(`${lessonPath(lessonId)}/events`, jsonInit("POST", body));
}

export function postSessionLessonEvent(sessionId: string, lessonId: string, body: LessonEventBody) {
   const path = `/sessions/${encodeURIComponent(sessionId)}/lessons/${encodeURIComponent(lessonId)}/events`;

   return requestJson<LessonStatePayload>(path, jsonInit("POST", body));
}

export function answerLessonCheck(lessonId: string, checkId: string, body: LessonCheckAnswerBody) {
   const path = `${lessonPath(lessonId)}/checks/${encodeURIComponent(checkId)}/answers`;

   return requestJson<LessonCheckVerdict>(path, jsonInit("POST", body));
}

export function answerLessonPrompt(lessonId: string, sectionId: string, body: LessonPromptAnswerBody) {
   const path = `${lessonPath(lessonId)}/prompts/${encodeURIComponent(sectionId)}/answers`;

   return requestJson<LessonPromptVerdict>(path, jsonInit("POST", body));
}

/* The live tutor's Tutor tab, app/api/routes/agent.py. Clearing everything sends the typed phrase
   the student entered, and the server refuses anything but "forget everything". */
function agentMemoryPath(memoryId: string) {
   return `/agent/memories/${encodeURIComponent(memoryId)}`;
}

function agentConversationPath(conversationId: string) {
   return `/agent/conversations/${encodeURIComponent(conversationId)}`;
}

export function readAgentMemories() {
   return requestJson<AgentMemoriesPayload>("/agent/memories");
}

export function editAgentMemory(memoryId: string, text: string) {
   return requestJson<AgentMemoryEntry>(agentMemoryPath(memoryId), jsonInit("PUT", { text }));
}

export function deleteAgentMemory(memoryId: string) {
   return requestJson<AgentMemoryDeleted>(agentMemoryPath(memoryId), jsonInit("DELETE"));
}

export function clearAgentMemory(confirmation: string) {
   return requestJson<AgentMemoryCleared>("/agent/memories", jsonInit("DELETE", { confirmation }));
}

export function readAgentConversations() {
   return requestJson<AgentConversationsPayload>("/agent/conversations");
}

export function readAgentConversation(conversationId: string) {
   return requestJson<AgentConversationPayload>(agentConversationPath(conversationId));
}

export function deleteAgentConversation(conversationId: string) {
   return requestJson<AgentConversationDeleted>(agentConversationPath(conversationId), jsonInit("DELETE"));
}

export function readAgentSettings() {
   return requestJson<AgentSettingsPayload>("/agent/settings");
}

export function updateAgentSettings(fields: AgentSettingsPayload) {
   return requestJson<AgentSettingsPayload>("/agent/settings", jsonInit("PUT", fields));
}

export function readAgentProfile() {
   return requestJson<AgentProfilePayload>("/agent/profile");
}

/* POST /agent/turns answers text/event-stream, so the body is handed back unread for
   agent/useAgentStream.ts to parse frame by frame. A refusal is not thrown here: the caller reads a
   4xx JSON body as the turn's error and treats a 5xx like no connection. */
export function openAgentTurnStream(body: AgentTurnBody, signal: AbortSignal) {
   return fetch("/agent/turns", {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json", Accept: "text/event-stream" },
      body: JSON.stringify(body),
      signal
   });
}

export async function closeAgentConversation(conversationId: string) {
   await request(`${agentConversationPath(conversationId)}/close`, jsonInit("POST", {}));
}
