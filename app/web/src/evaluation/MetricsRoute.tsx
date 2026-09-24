import { readMetrics } from "../api/client";
import type { MetricsPayload } from "../api/types";
import { useLoad } from "../progress/load";
import { MetricsView } from "./MetricsView";

export interface MetricsRouteProps {
   onLeave: () => void;
}

export function MetricsRoute({ onLeave }: MetricsRouteProps) {
   const metrics = useLoad<MetricsPayload>(readMetrics);

   return (
      <>
         {metrics.kind === "waiting" ? <section aria-busy="true" data-testid="metrics-waiting" /> : null}

         {metrics.kind === "failed" ? (
            <section className="card">
               <p data-testid="metrics-failed" className="muted">
                  The learning metrics could not be loaded.
               </p>
            </section>
         ) : null}

         {metrics.kind === "loaded" ? <MetricsView metrics={metrics.value} /> : null}

         <button type="button" className="text-button" onClick={onLeave}>
            Back to settings
         </button>
      </>
   );
}