import { useState } from "react";

import { openCheck, openDrill, openMock, openUnitCheck, readCheck, readTimedSession, type CaptureMode } from "../api/client";
import type { AssessmentResult, AssessmentSession, PartKey, TimedKind, UnfinishedAssessment, UnitCheckPayload } from "../api/types";
import { CheckpointRoute } from "../evaluation/CheckpointRoute";
import { FrqUnitCheck } from "../frq/FrqRoute";
import type { AssessmentFormat } from "../routing";
import { refusalText } from "./format";
import { ResultScreen } from "./ResultScreen";
import { SetupScreen } from "./SetupScreen";
import { TimedSessionScreen } from "./TimedSessionScreen";
import { UnitCheckScreen } from "./UnitCheckScreen";

/* The Assessments tab (the operator's ruling of 2026-09-29, amending 08's information
   architecture). It opens a unit check, a free-response unit check, a part drill, a full mock or a
   checkpoint and follows each to its end. The shell passes the chosen format so the address
   carries it; rendered without one, the hub keeps its own. */

export interface AssessmentRouteProps {
   pollMilliseconds?: number;
   format?: AssessmentFormat;
   onChangeFormat?: (format: AssessmentFormat) => void;
}

type AssessmentPage =
   | { kind: "setup" }
   | { kind: "timed"; timedKind: TimedKind; session: AssessmentSession }
   | { kind: "unitCheck"; session: AssessmentSession; title: string }
   | { kind: "freeResponse"; check: UnitCheckPayload }
   | { kind: "checkpoint"; openCheckpointId: string | null }
   | { kind: "result"; result: AssessmentResult };

export function AssessmentRoute({ pollMilliseconds, format, onChangeFormat }: AssessmentRouteProps) {
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

   function startFreeResponse(unitId: string) {
      open(async () => ({ kind: "freeResponse", check: await openUnitCheck(unitId) }), "The unit check could not be opened.");
   }

   const backToSetup = () => setPage({ kind: "setup" });

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

   if (page.kind === "freeResponse") {
      return <FrqUnitCheck check={page.check} pollMilliseconds={pollMilliseconds} onLeave={backToSetup} />;
   }

   if (page.kind === "checkpoint") {
      return <CheckpointRoute openCheckpointId={page.openCheckpointId} onLeave={backToSetup} />;
   }

   if (page.kind === "result") {
      return <ResultScreen result={page.result} onDone={backToSetup} />;
   }

   return (
      <SetupScreen
         problem={problem}
         format={format}
         onChangeFormat={onChangeFormat}
         onStartMock={startMock}
         onStartDrill={startDrill}
         onStartUnitCheck={startUnitCheck}
         onStartFreeResponse={startFreeResponse}
         onOpenCheckpoint={(openCheckpointId) => setPage({ kind: "checkpoint", openCheckpointId })}
         onResume={resume}
      />
   );
}

export const AssessmentsRoute = AssessmentRoute;
