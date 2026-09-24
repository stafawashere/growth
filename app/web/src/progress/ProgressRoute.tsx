import { useEffect, useState } from "react";

import { readCalibration, readMasteryMap } from "../api/client";
import type { CalibrationPayload, MasteryMapPayload } from "../api/types";
import { CalibrationCurve } from "./CalibrationCurve";
import { MasteryMap } from "./MasteryMap";

type Load<T> = { kind: "waiting" } | { kind: "failed" } | { kind: "loaded"; value: T };

/* Progress takes no input from the shell: it is reached from home and reads its own record. The
   map and the curve load separately, so one failing leaves the other drawn. */
export interface ProgressRouteProps {}

function useLoad<T>(read: () => Promise<T>): Load<T> {
   const [load, setLoad] = useState<Load<T>>({ kind: "waiting" });

   useEffect(() => {
      let isCurrent = true;

      read().then(
         (value) => {
            if (isCurrent) {
               setLoad({ kind: "loaded", value });
            }
         },
         () => {
            if (isCurrent) {
               setLoad({ kind: "failed" });
            }
         }
      );

      return () => {
         isCurrent = false;
      };
   }, [read]);

   return load;
}

export function ProgressRoute(_props: ProgressRouteProps) {
   const mastery = useLoad<MasteryMapPayload>(readMasteryMap);
   const calibration = useLoad<CalibrationPayload>(readCalibration);

   return (
      <section className="card">
         <h1 className="screen-title">Progress</h1>

         {mastery.kind === "waiting" ? <div aria-busy="true" data-testid="mastery-waiting" /> : null}

         {mastery.kind === "failed" ? (
            <p data-testid="mastery-failed" className="muted">
               The mastery map could not be loaded.
            </p>
         ) : null}

         {mastery.kind === "loaded" ? <MasteryMap map={mastery.value} /> : null}

         {calibration.kind === "waiting" ? <div aria-busy="true" data-testid="progress-waiting" /> : null}

         {calibration.kind === "failed" ? (
            <p data-testid="progress-failed" className="muted">
               The calibration record could not be loaded.
            </p>
         ) : null}

         {calibration.kind === "loaded" ? <CalibrationCurve calibration={calibration.value} /> : null}
      </section>
   );
}
