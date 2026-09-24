import { useEffect, useState } from "react";

import { ApiError, openUnitCheck, readFrqUnits } from "../api/client";
import type { FrqQuestion, FrqUnit, UnitCheckPayload } from "../api/types";
import { CaptureScreen } from "./CaptureScreen";

/* The free-response part of a unit check, reached from home (08: home offers progress, review and
   the assessment modes, and none of them is the landing screen). The student picks a unit, the
   server picks its least-attempted questions, and each question runs through CaptureScreen. */

type UnitsLoad = { kind: "waiting" } | { kind: "failed" } | { kind: "loaded"; units: FrqUnit[] };

export interface FrqRouteProps {
   pollMilliseconds?: number;
}

export function FrqRoute({ pollMilliseconds }: FrqRouteProps) {
   const [units, setUnits] = useState<UnitsLoad>({ kind: "waiting" });
   const [check, setCheck] = useState<UnitCheckPayload | null>(null);
   const [question, setQuestion] = useState<FrqQuestion | null>(null);
   const [problem, setProblem] = useState<string | null>(null);

   useEffect(() => {
      let isCurrent = true;

      readFrqUnits().then(
         (payload) => {
            if (isCurrent) {
               setUnits({ kind: "loaded", units: payload.units });
            }
         },
         () => {
            if (isCurrent) {
               setUnits({ kind: "failed" });
            }
         }
      );

      return () => {
         isCurrent = false;
      };
   }, []);

   async function start(unitId: string) {
      setProblem(null);

      try {
         setCheck(await openUnitCheck(unitId));
      } catch (failure) {
         const hasDetail = failure instanceof ApiError && failure.detail !== "";

         setProblem(hasDetail ? failure.detail : "The unit check could not be opened.");
      }
   }

   if (question !== null && check !== null) {
      return (
         <>
            <button type="button" className="text-button" onClick={() => setQuestion(null)}>
               Back to the unit check
            </button>

            <CaptureScreen sessionId={check.session_id} question={question} pollMilliseconds={pollMilliseconds} />
         </>
      );
   }

   if (check !== null) {
      return (
         <section className="card" data-testid="unit-check">
            <h1 className="screen-title">Unit check, free response</h1>

            <p className="muted">
               Untimed. Each answer is graded point by point once you confirm what the app read from your page.
            </p>

            <ul className="review-list">
               {check.questions.map((entry, index) => (
                  <li key={entry.id}>
                     <button type="button" className="text-button" onClick={() => setQuestion(entry)}>
                        Question {index + 1}, {entry.parts.length} parts
                     </button>
                  </li>
               ))}
            </ul>
         </section>
      );
   }

   if (units.kind === "waiting") {
      return <section aria-busy="true" data-testid="frq-waiting" />;
   }

   if (units.kind === "failed") {
      return (
         <section className="card">
            <h1 className="screen-title">Free response</h1>
            <p className="muted">The free-response questions could not be loaded.</p>
         </section>
      );
   }

   return (
      <section className="card" data-testid="frq-units">
         <h1 className="screen-title">Free response</h1>

         <p className="muted">Choose a unit. Its free-response questions are served as an untimed unit check.</p>

         {problem !== null ? <p role="alert">{problem}</p> : null}

         <ul className="review-list">
            {units.units.map((unit) => (
               <li key={unit.unit_id}>
                  <button type="button" className="text-button" onClick={() => start(unit.unit_id)}>
                     {unit.title}
                  </button>
               </li>
            ))}
         </ul>
      </section>
   );
}
