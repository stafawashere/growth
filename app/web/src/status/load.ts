import { useCallback, useEffect, useMemo, useState } from "react";

export type Load<T> = { kind: "waiting" } | { kind: "failed" } | { kind: "loaded"; value: T };

export type Loader<T> = Load<T> & { retry: () => void };

/* Every screen and section that reads its own route on arrival loads through this, and draws the
   waiting and failed states with Loading and LoadFailed from LoadState.tsx. A refused request, a
   request that could not be made and a response that is not a JSON object all end in the same
   failed state, and a screen never draws from a payload it did not receive. retry goes back to
   waiting and reads again. The value keeps its identity until the load changes, so an effect that
   depends on it runs once per change. */
export function useLoad<T>(read: () => Promise<T>): Loader<T> {
   const [load, setLoad] = useState<Load<T>>({ kind: "waiting" });
   const [attempt, setAttempt] = useState(0);

   useEffect(() => {
      let isCurrent = true;

      async function settle() {
         try {
            const value = await read();
            const isPayload = typeof value === "object" && value !== null;

            if (!isPayload) {
               throw new Error("the response carried no payload");
            }

            if (isCurrent) {
               setLoad({ kind: "loaded", value });
            }
         } catch {
            if (isCurrent) {
               setLoad({ kind: "failed" });
            }
         }
      }

      setLoad({ kind: "waiting" });
      settle();

      return () => {
         isCurrent = false;
      };
   }, [read, attempt]);

   const retry = useCallback(() => setAttempt((previous) => previous + 1), []);

   return useMemo(() => ({ ...load, retry }), [load, retry]);
}
