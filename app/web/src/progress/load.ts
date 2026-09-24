import { useEffect, useState } from "react";

export type Load<T> = { kind: "waiting" } | { kind: "failed" } | { kind: "loaded"; value: T };

/* Every screen section that reads its own route loads through this, so a refused request, a
   request that could not be made and a response that is not a JSON object all end in the same
   failed state, and a section never draws from a payload it did not receive. */
export function useLoad<T>(read: () => Promise<T>): Load<T> {
   const [load, setLoad] = useState<Load<T>>({ kind: "waiting" });

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
   }, [read]);

   return load;
}