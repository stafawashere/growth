import { useCallback, useEffect, useRef, useState } from "react";

import {
   openDiagnostic,
   readDiagnostic,
   readNextItem,
   submitAttempt,
   type AttemptAnswer,
   type DiagnosticNextItemResponse
} from "../api/client";
import type { DiagnosticResult, DiagnosticServedItem } from "../api/types";
import {
   DiagnosticIntro,
   DiagnosticItem,
   DiagnosticResultView,
   type DiagnosticItemState,
   type OnboardingReason
} from "./OnboardingScreen";

/* resumeSessionId names the unfinished diagnostic GET /progress reported, and null opens a new
   one once the student starts from the intro. reason picks the intro's copy: a long gap runs a
   re-diagnostic that updates what the app knows rather than starting over. */
export interface OnboardingRouteProps {
   reason: OnboardingReason;
   resumeSessionId: string | null;
   onFinished: () => void;
}

type OnboardingStage =
   | { kind: "intro" }
   | { kind: "waiting" }
   | { kind: "failed" }
   | { kind: "item"; sessionId: string; item: DiagnosticServedItem }
   | { kind: "result"; result: DiagnosticResult };

export function OnboardingRoute({ reason, resumeSessionId, onFinished }: OnboardingRouteProps) {
   const isResuming = resumeSessionId !== null;

   const [stage, setStage] = useState<OnboardingStage>(isResuming ? { kind: "waiting" } : { kind: "intro" });
   const [answerMathJson, setAnswerMathJson] = useState<unknown>(null);
   const [submitted, setSubmitted] = useState(false);
   const [answerUnavailable, setAnswerUnavailable] = useState(false);

   const resumed = useRef(false);
   const inFlight = useRef(false);
   const shownAt = useRef(0);

   const advance = useCallback(async (sessionId: string) => {
      const next = (await readNextItem(sessionId)) as DiagnosticNextItemResponse;
      const hasFinished = next.diagnostic_finished || next.item === null;

      if (hasFinished) {
         const result = await readDiagnostic(sessionId);

         setStage({ kind: "result", result });

         return;
      }

      setAnswerMathJson(null);
      setSubmitted(false);
      setAnswerUnavailable(false);
      shownAt.current = Date.now();

      setStage({ kind: "item", sessionId, item: next.item as DiagnosticServedItem });
   }, []);

   useEffect(() => {
      const shouldResume = resumeSessionId !== null && !resumed.current;

      if (!shouldResume) {
         return;
      }

      resumed.current = true;

      advance(resumeSessionId).catch(() => setStage({ kind: "failed" }));
   }, [advance, resumeSessionId]);

   function start() {
      setStage({ kind: "waiting" });

      openDiagnostic()
         .then((session) => advance(session.id))
         .catch(() => setStage({ kind: "failed" }));
   }

   const noteAnswerUnavailable = useCallback(() => {
      setAnswerUnavailable(true);
   }, []);

   async function send(answer: AttemptAnswer) {
      const isOnItem = stage.kind === "item";
      const canSend = isOnItem && !inFlight.current;

      if (!canSend) {
         return;
      }

      inFlight.current = true;
      setSubmitted(true);

      try {
         await submitAttempt(stage.sessionId, {
            item_id: stage.item.id,
            answer,
            elapsed_ms: Date.now() - shownAt.current
         });

         await advance(stage.sessionId);
      } catch {
         // no plan copy exists for a refused diagnostic answer, so the item stays on screen to retry
         setSubmitted(false);
      } finally {
         inFlight.current = false;
      }
   }

   if (stage.kind === "intro") {
      return <DiagnosticIntro reason={reason} onStart={start} />;
   }

   if (stage.kind === "waiting") {
      return <section aria-busy="true" data-testid="onboarding-waiting" />;
   }

   if (stage.kind === "failed") {
      return (
         <section className="card">
            <p data-testid="onboarding-failed" className="muted">
               The diagnostic could not be loaded.
            </p>
         </section>
      );
   }

   if (stage.kind === "result") {
      return <DiagnosticResultView units={stage.result.units} onFinished={onFinished} />;
   }

   const hasAnswer = answerMathJson !== null;
   let itemState: DiagnosticItemState = hasAnswer ? "answered" : "unanswered";

   if (submitted) {
      itemState = "submitted";
   }

   return (
      <DiagnosticItem
         item={stage.item}
         state={itemState}
         answerUnavailable={answerUnavailable}
         onAnswerChange={setAnswerMathJson}
         onAnswerUnavailable={noteAnswerUnavailable}
         onCheck={() => send({ mathjson: answerMathJson })}
         onNotLearned={() => send({ not_learned: true })}
      />
   );
}
