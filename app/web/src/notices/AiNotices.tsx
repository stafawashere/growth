import { useCallback, useEffect, useRef, useState } from "react";

import { readNotices } from "../api/client";
import type { AiNotice, AiNoticeOutcome, NoticesPayload } from "../api/types";

/* app/providers/notices.py records a notice each time the app talks to an AI model. While the
   student is signed in this polls GET /notices and shows each new one as a small notice that
   screen readers announce politely. The first read after signing in only sets the cursor, so a
   reload does not replay the calls already made. Nothing here animates. */

export const NOTICE_POLL_MILLISECONDS = 5000;

export const NOTICE_VISIBLE_MILLISECONDS = 8000;

export const MAXIMUM_SHOWN_NOTICES = 3;

export const AI_NOTICES_KEY = "growth-ai-notices";

const OFF = "off";

const ON = "on";

const OUTCOME_TEXT: Record<AiNoticeOutcome, string> = {
   answered: "answered",
   failed: "the call failed",
   refused: "the call was not sent",
   stopped: "the call was stopped by a limit",
   interrupted: "the answer was cut off",
   queued: "the call was saved for later"
};

/* The choice lives in this browser's storage, which can be missing, full or refused outright, so
   every read and write is guarded and a choice that cannot be read is on. */
export function readAiNoticesEnabled(): boolean {
   try {
      return window.localStorage.getItem(AI_NOTICES_KEY) !== OFF;
   } catch {
      return true;
   }
}

export function saveAiNoticesEnabled(enabled: boolean) {
   try {
      window.localStorage.setItem(AI_NOTICES_KEY, enabled ? ON : OFF);
   } catch {
      // storage refused; the choice still holds until the page is reloaded
   }
}

function isNoticesPayload(payload: unknown): payload is NoticesPayload {
   const isObject = typeof payload === "object" && payload !== null;

   if (!isObject) {
      return false;
   }

   const candidate = payload as Partial<NoticesPayload>;
   const hasNotices = Array.isArray(candidate.notices);
   const hasLatest = typeof candidate.latest === "number";

   return hasNotices && hasLatest;
}

export function noticeTitle(notice: AiNotice) {
   const outcome = OUTCOME_TEXT[notice.outcome] ?? notice.outcome;

   return `AI ${notice.role}: ${outcome}`;
}

function noticeSource(notice: AiNotice) {
   const model = notice.model || notice.provider;

   return notice.replayed ? `${model}, replayed from a recording` : model;
}

interface AiNoticeToastProps {
   notice: AiNotice;
   visibleMilliseconds: number;
   onDismiss: (id: number) => void;
}

function AiNoticeToast(props: AiNoticeToastProps) {
   const { notice, visibleMilliseconds, onDismiss } = props;
   const title = noticeTitle(notice);
   const isAnswer = notice.outcome === "answered";

   useEffect(() => {
      const timer = setTimeout(() => onDismiss(notice.id), visibleMilliseconds);

      return () => {
         clearTimeout(timer);
      };
   }, [notice.id, visibleMilliseconds, onDismiss]);

   return (
      <div className="notice notice-framed ai-notice" data-testid="ai-notice">
         <p>{title}</p>

         <p className="caption">{noticeSource(notice)}</p>

         <p>Asked: {notice.asked}</p>

         <p>
            {isAnswer ? "Answer: " : "Result: "}
            {notice.answered}
         </p>

         <button type="button" className="text-button" aria-label={`Dismiss: ${title}`} onClick={() => onDismiss(notice.id)}>
            Dismiss
         </button>
      </div>
   );
}

export interface AiNoticesProps {
   active: boolean;
   pollMilliseconds?: number;
   visibleMilliseconds?: number;
}

export function AiNotices(props: AiNoticesProps) {
   const { active } = props;
   const pollEvery = props.pollMilliseconds ?? NOTICE_POLL_MILLISECONDS;
   const visibleFor = props.visibleMilliseconds ?? NOTICE_VISIBLE_MILLISECONDS;

   const [shown, setShown] = useState<AiNotice[]>([]);
   const cursor = useRef<number | null>(null);
   const polling = useRef(false);

   const dismiss = useCallback((id: number) => {
      setShown((current) => current.filter((notice) => notice.id !== id));
   }, []);

   useEffect(() => {
      if (!active) {
         cursor.current = null;
         setShown([]);

         return;
      }

      let isCurrent = true;

      async function poll() {
         if (polling.current) {
            return;
         }

         polling.current = true;

         try {
            const payload: unknown = await readNotices(cursor.current ?? 0);
            const isReadable = isCurrent && isNoticesPayload(payload);

            if (!isReadable) {
               return;
            }

            const isPriming = cursor.current === null;
            const seen = cursor.current ?? 0;
            const fresh = payload.notices.filter((notice) => notice.id > seen);
            cursor.current = Math.max(seen, payload.latest);

            const hasNew = !isPriming && fresh.length > 0;

            if (hasNew) {
               setShown((current) => [...current, ...fresh].slice(-MAXIMUM_SHOWN_NOTICES));
            }
         } catch {
            // a failed read says nothing; the next poll asks again from the same cursor
         } finally {
            polling.current = false;
         }
      }

      void poll();

      const poller = setInterval(() => void poll(), pollEvery);

      return () => {
         isCurrent = false;
         clearInterval(poller);
      };
   }, [active, pollEvery]);

   if (!active) {
      return null;
   }

   return (
      <div className="ai-notices" role="status" aria-live="polite" data-testid="ai-notices">
         {shown.map((notice) => (
            <AiNoticeToast key={notice.id} notice={notice} visibleMilliseconds={visibleFor} onDismiss={dismiss} />
         ))}
      </div>
   );
}

export interface AiNoticesSettingProps {
   enabled: boolean;
   onChange: (enabled: boolean) => void;
}

/* Kept in this browser, as the theme is, because the settings route stores only dates and a server
   preference would need a new column. The server records the notices either way. */
export function AiNoticesSetting(props: AiNoticesSettingProps) {
   function change(enabled: boolean) {
      saveAiNoticesEnabled(enabled);
      props.onChange(enabled);
   }

   return (
      <section className="card settings" data-testid="ai-notices-settings">
         <h2 className="section-heading">AI activity</h2>

         <fieldset className="choice-group">
            <legend>Notices</legend>

            <label className="check-row">
               <input type="checkbox" checked={props.enabled} onChange={(event) => change(event.target.checked)} />
               Show a short notice each time the app asks an AI model something
            </label>
         </fieldset>
      </section>
   );
}
