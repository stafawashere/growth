import type {
   AttemptResult,
   Confidence,
   FeedbackPayload,
   ServedItem,
   SessionPayload
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

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
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
