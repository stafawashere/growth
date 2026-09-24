import { useState } from "react";

import { openCheck, openDrill, openMock, readCheck, readTimedSession, type CaptureMode } from "../api/client";
import type { AssessmentResult, AssessmentSession, PartKey, TimedKind, UnfinishedAssessment } from "../api/types";
import { refusalText } from "./format";
import { ResultScreen } from "./ResultScreen";
import { SetupScreen } from "./SetupScreen";
import { TimedSessionScreen } from "./TimedSessionScreen";
import { UnitCheckScreen } from "./UnitCheckScreen";

/* The assessment area, reached from home's "Mock exam" button and never from the bar (08,
   Information architecture). It opens a full mock, a part drill or a unit check and follows it
   to its result. */

export interface AssessmentRouteProps {
   pollMilliseconds?: number;
}

type AssessmentPage =
   | { kind: "setup" }
   | { kind: "timed"; timedKind: TimedKind; session: AssessmentSession }
   | { kind: "unitCheck"; session: AssessmentSession; title: string }
   | { kind: "result"; result: AssessmentResult };

export function AssessmentRoute({ pollMilliseconds }: AssessmentRouteProps) {
   const [page, setPage] = useState<AssessmentPage>({ kind: "setup" });
   const [problem, setProblem] = useState<string | null>(null);

   async function open(work: () => Promise<AssessmentPage>, fallback: string) {
      setProblem(null);

      try {
         setPage(await work());
      } catch (failure) {
         setProblem(refusalText(failure, fallback));
      }
   }

   function startMock(captureMode: CaptureMode) {
      open(async () => ({ kind: "timed", timedKind: "mocks", session: await openMock({ capture_mode: captureMode }) }), "The mock could not be opened.");
   }

   function startDrill(part: PartKey, captureMode: CaptureMode) {
      open(
         async () => ({ kind: "timed", timedKind: "drills", session: await openDrill({ part, capture_mode: captureMode }) }),
         "The part drill could not be opened."
      );
   }

   function startUnitCheck(unitId: string, title: string) {
      open(async () => ({ kind: "unitCheck", session: await openCheck(unitId), title }), "The unit check could not be opened.");
   }

   /* A resumed session opens on the screen its mode belongs to. A mock whose parts are all closed
      lands on its capture and finish step, because that is where TimedSessionScreen puts it. */
   function resume(entry: UnfinishedAssessment, subject: string) {
      const isUnitCheck = entry.mode === "unit_check";

      if (isUnitCheck) {
         open(async () => ({ kind: "unitCheck", session: await readCheck(entry.id), title: subject }), "The unit check could not be resumed.");

         return;
      }

      const timedKind: TimedKind = entry.mode === "mock" ? "mocks" : "drills";

      open(async () => ({ kind: "timed", timedKind, session: await readTimedSession(timedKind, entry.id) }), "That session could not be resumed.");
   }

   if (page.kind === "timed") {
      return (
         <TimedSessionScreen
            kind={page.timedKind}
            sessionId={page.session.id}
            initial={page.session}
            pollMilliseconds={pollMilliseconds}
            onShowResult={(result) => setPage({ kind: "result", result })}
         />
      );
   }

   if (page.kind === "unitCheck") {
      return <UnitCheckScreen sessionId={page.session.id} initial={page.session} unitTitle={page.title} />;
   }

   if (page.kind === "result") {
      return <ResultScreen result={page.result} onDone={() => setPage({ kind: "setup" })} />;
   }

   return <SetupScreen problem={problem} onStartMock={startMock} onStartDrill={startDrill} onStartUnitCheck={startUnitCheck} onResume={resume} />;
}
