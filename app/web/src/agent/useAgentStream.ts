import { useCallback, useEffect, useRef, useState } from "react";

import { SESSION_ENDED_EVENT, openAgentTurnStream } from "../api/client";
import type {
   AgentEndEvent,
   AgentErrorEvent,
   AgentErrorKind,
   AgentFigureRefusedEvent,
   AgentFigureStepEvent,
   AgentStartEvent,
   AgentTextEvent,
   AgentTurnBody
} from "../api/types";

/* One turn of the tutor over POST /agent/turns (docs/agent/architecture.md, "Streaming end to end").
   EventSource cannot POST, so the body is read as a stream and split into server-sent event frames
   here. A frame may arrive in pieces and a chunk may carry several frames, so the parser keeps what
   it has not yet seen the end of. No connection, a 5xx and no first text within 15 seconds are one
   state, "offline" (docs/agent/design.md, the degraded states); a 4xx carries its reason as JSON.
   A reply that draws adds the figure events of docs/agent/drawing-design.md, "Events and order";
   the opening of a figure or the figure itself counts as the reply having begun. */

export const FIRST_TEXT_TIMEOUT_MILLISECONDS = 15000;

export interface ServerSentEvent {
   event: string;
   data: string;
}

const FRAME_END = /\r?\n\r?\n/;

function frameFrom(block: string): ServerSentEvent | null {
   let event = "message";
   const dataLines: string[] = [];

   for (const line of block.split(/\r?\n/)) {
      const isComment = line.startsWith(":");
      const colon = line.indexOf(":");

      if (isComment || line === "") {
         continue;
      }

      const field = colon === -1 ? line : line.slice(0, colon);
      const rawValue = colon === -1 ? "" : line.slice(colon + 1);
      const value = rawValue.startsWith(" ") ? rawValue.slice(1) : rawValue;

      if (field === "event") {
         event = value;
      }

      if (field === "data") {
         dataLines.push(value);
      }
   }

   const hasData = dataLines.length > 0;

   return hasData ? { event, data: dataLines.join("\n") } : null;
}

export function createFrameParser(onFrame: (frame: ServerSentEvent) => void) {
   let pending = "";

   function push(chunk: string) {
      pending += chunk;

      let boundary = FRAME_END.exec(pending);

      while (boundary !== null) {
         const block = pending.slice(0, boundary.index);

         pending = pending.slice(boundary.index + boundary[0].length);

         const frame = frameFrom(block);

         if (frame !== null) {
            onFrame(frame);
         }

         boundary = FRAME_END.exec(pending);
      }
   }

   function finish() {
      const frame = frameFrom(pending);

      pending = "";

      if (frame !== null) {
         onFrame(frame);
      }
   }

   return { push, finish };
}

export type TurnFailure = { kind: "offline" } | { kind: AgentErrorKind; resetsAt: string | null; copy: string | null };

export interface TurnHandlers {
   onStart: (event: AgentStartEvent) => void;
   onText: (delta: string) => void;
   onEnd: (event: AgentEndEvent) => void;
   onFailure: (failure: TurnFailure) => void;
   onStopped: () => void;
   onFigurePending?: () => void;
   onFigure?: (spec: unknown) => void;
   onFigureStep?: (event: AgentFigureStepEvent) => void;
   onFigureRefused?: (event: AgentFigureRefusedEvent) => void;
}

const OFFLINE: TurnFailure = { kind: "offline" };

function parsed<T>(data: string): T | null {
   try {
      return JSON.parse(data) as T;
   } catch {
      return null;
   }
}

function failureFromError(event: AgentErrorEvent | null): TurnFailure {
   const hasKind = event !== null && typeof event.kind === "string";

   if (!hasKind) {
      return { kind: "refused", resetsAt: null, copy: null };
   }

   return { kind: event.kind, resetsAt: event.resets_at ?? null, copy: event.copy ?? null };
}

async function refusalFrom(response: Response): Promise<TurnFailure> {
   try {
      const body: unknown = await response.json();
      const isObject = typeof body === "object" && body !== null;
      const record = (isObject ? body : {}) as Record<string, unknown>;
      const hasKind = typeof record.kind === "string";

      if (hasKind) {
         return failureFromError(record as unknown as AgentErrorEvent);
      }

      const detail = typeof record.detail === "string" ? record.detail : null;

      return { kind: "refused", resetsAt: null, copy: detail };
   } catch {
      return { kind: "refused", resetsAt: null, copy: null };
   }
}

/* Resolves once the turn has ended one way or another; every outcome reaches exactly one of the
   handlers' onEnd, onFailure or onStopped. */
export async function runAgentTurn(body: AgentTurnBody, handlers: TurnHandlers, signal: AbortSignal, isStopped: () => boolean) {
   let settled = false;
   let hasText = false;
   let hasFigure = false;

   function settle(action: () => void) {
      if (settled) {
         return;
      }

      settled = true;
      action();
   }

   function interrupted() {
      settle(() => (isStopped() ? handlers.onStopped() : handlers.onFailure(OFFLINE)));
   }

   let response: Response;

   try {
      response = await openAgentTurnStream(body, signal);
   } catch {
      interrupted();

      return;
   }

   const isServerFailure = response.status >= 500;
   const isRefusal = response.status >= 400 && !isServerFailure;
   const hasBody = response.body !== null && response.body !== undefined;

   if (isServerFailure || (response.ok && !hasBody)) {
      settle(() => handlers.onFailure(OFFLINE));

      return;
   }

   if (isRefusal) {
      const sessionEnded = response.status === 401;

      if (sessionEnded) {
         window.dispatchEvent(new CustomEvent(SESSION_ENDED_EVENT));
      }

      const failure = await refusalFrom(response);

      settle(() => handlers.onFailure(failure));

      return;
   }

   function dispatch(frame: ServerSentEvent) {
      if (settled) {
         return;
      }

      if (frame.event === "start") {
         const start = parsed<AgentStartEvent>(frame.data);

         if (start !== null) {
            handlers.onStart(start);
         }

         return;
      }

      if (frame.event === "text") {
         const text = parsed<AgentTextEvent>(frame.data);
         const hasDelta = text !== null && typeof text.delta === "string";

         if (hasDelta) {
            hasText = true;
            handlers.onText(text.delta);
         }

         return;
      }

      if (frame.event === "figure_pending") {
         handlers.onFigurePending?.();

         return;
      }

      if (frame.event === "figure") {
         const spec = parsed<unknown>(frame.data);

         if (spec !== null) {
            hasFigure = true;
            handlers.onFigure?.(spec);
         }

         return;
      }

      if (frame.event === "figure_step") {
         const step = parsed<AgentFigureStepEvent>(frame.data);
         const namesAStep = step !== null && typeof step.figure === "string" && typeof step.step === "string";

         if (namesAStep) {
            handlers.onFigureStep?.(step);
         }

         return;
      }

      if (frame.event === "figure_refused") {
         const refusal = parsed<AgentFigureRefusedEvent>(frame.data);
         const hasCopy = refusal !== null && typeof refusal.copy === "string";

         handlers.onFigureRefused?.(hasCopy ? refusal : { reason: "malformed", copy: "" });

         return;
      }

      if (frame.event === "end") {
         const end = parsed<AgentEndEvent>(frame.data);

         settle(() => handlers.onEnd(end ?? { turn_id: "", outcome: "incomplete", turns_on_item: 0, turns_in_conversation: 0 }));

         return;
      }

      if (frame.event === "error") {
         const failure = failureFromError(parsed<AgentErrorEvent>(frame.data));

         settle(() => handlers.onFailure(failure));
      }
   }

   const reader = (response.body as ReadableStream<Uint8Array>).getReader();
   const decoder = new TextDecoder();
   const parser = createFrameParser(dispatch);

   try {
      for (;;) {
         const { done, value } = await reader.read();

         if (done) {
            break;
         }

         parser.push(decoder.decode(value, { stream: true }));
      }

      parser.push(decoder.decode());
      parser.finish();
   } catch {
      interrupted();

      return;
   }

   const endedWithoutEnd = !settled;

   if (endedWithoutEnd && isStopped()) {
      settle(handlers.onStopped);

      return;
   }

   const hasReply = hasText || hasFigure;

   if (endedWithoutEnd && hasReply) {
      settle(() => handlers.onEnd({ turn_id: "", outcome: "incomplete", turns_on_item: 0, turns_in_conversation: 0 }));

      return;
   }

   settle(() => handlers.onFailure(OFFLINE));
}

/* The hook the panel's provider drives: one turn at a time, Stop aborts it, and a turn with no text
   after FIRST_TEXT_TIMEOUT_MILLISECONDS is abandoned as offline. Once a turn has settled (its end
   or error frame, a failure or a stop) it lets go of the turn's controller and its timer, so the
   body is read on to the server's own close and nothing aborts a request that already finished. */
export function useAgentStream(timeoutMilliseconds = FIRST_TEXT_TIMEOUT_MILLISECONDS) {
   const [isStreaming, setIsStreaming] = useState(false);
   const controller = useRef<AbortController | null>(null);
   const stopRequested = useRef(false);
   const timer = useRef<ReturnType<typeof setTimeout> | null>(null);

   const clearTimer = useCallback(() => {
      if (timer.current !== null) {
         clearTimeout(timer.current);
         timer.current = null;
      }
   }, []);

   useEffect(() => {
      return () => {
         clearTimer();
         controller.current?.abort();
      };
   }, [clearTimer]);

   const start = useCallback(
      async (body: AgentTurnBody, handlers: TurnHandlers) => {
         const isBusy = controller.current !== null;

         if (isBusy) {
            return;
         }

         const turnController = new AbortController();
         let timedOut = false;

         controller.current = turnController;
         stopRequested.current = false;
         setIsStreaming(true);

         timer.current = setTimeout(() => {
            timedOut = true;
            turnController.abort();
         }, timeoutMilliseconds);

         function release() {
            const isCurrentTurn = controller.current === turnController;

            if (!isCurrentTurn) {
               return;
            }

            clearTimer();
            controller.current = null;
            setIsStreaming(false);
         }

         const guarded: TurnHandlers = {
            ...handlers,
            onText: (delta) => {
               clearTimer();
               handlers.onText(delta);
            },
            onFigurePending: () => {
               clearTimer();
               handlers.onFigurePending?.();
            },
            onFigure: (spec) => {
               clearTimer();
               handlers.onFigure?.(spec);
            },
            onEnd: (event) => {
               release();
               handlers.onEnd(event);
            },
            onFailure: (failure) => {
               release();
               handlers.onFailure(failure);
            },
            onStopped: () => {
               release();
               handlers.onStopped();
            }
         };

         try {
            await runAgentTurn(body, guarded, turnController.signal, () => stopRequested.current && !timedOut);
         } finally {
            release();
         }
      },
      [clearTimer, timeoutMilliseconds]
   );

   const stop = useCallback(() => {
      const turn = controller.current;

      if (turn === null) {
         return;
      }

      stopRequested.current = true;
      turn.abort();
   }, []);

   return { isStreaming, start, stop };
}
