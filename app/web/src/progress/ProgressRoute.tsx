import { useEffect, useState } from "react";

import { readCalibration } from "../api/client";
import type { CalibrationPayload } from "../api/types";
import { CalibrationCurve } from "./CalibrationCurve";

type ProgressLoad =
   | { kind: "waiting" }
   | { kind: "failed" }
   | { kind: "loaded"; calibration: CalibrationPayload };

/* Progress takes no input from the shell: it is reached from home and reads its own record. */
export interface ProgressRouteProps {}

export function ProgressRoute(_props: ProgressRouteProps) {
   const [load, setLoad] = useState<ProgressLoad>({ kind: "waiting" });

   useEffect(() => {
      let isCurrent = true;

      readCalibration().then(
         (calibration) => {
            if (isCurrent) {
               setLoad({ kind: "loaded", calibration });
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
   }, []);

   return (
      <section className="card">
         <h1 className="screen-title">Progress</h1>

         {load.kind === "waiting" ? <div aria-busy="true" data-testid="progress-waiting" /> : null}

         {load.kind === "failed" ? (
            <p data-testid="progress-failed" className="muted">
               The calibration record could not be loaded.
            </p>
         ) : null}

         {load.kind === "loaded" ? <CalibrationCurve calibration={load.calibration} /> : null}
      </section>
   );
}
