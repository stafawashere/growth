import { useState } from "react";

import { addPasskey, ApiError } from "../api/client";

type AddState =
   | { kind: "idle"; refusal: string | null; added: boolean }
   | { kind: "working" };

/* docs/plan/09-security-and-privacy.md, "Recovery": a second authenticator is the primary recovery
   answer, so a signed-in student can register one here. */
export function AddPasskeyControl() {
   const [state, setState] = useState<AddState>({ kind: "idle", refusal: null, added: false });

   async function add() {
      setState({ kind: "working" });

      try {
         await addPasskey();

         setState({ kind: "idle", refusal: null, added: true });
      } catch (failure) {
         const isServerRefusal = failure instanceof ApiError;

         setState({ kind: "idle", refusal: isServerRefusal ? failure.detail : null, added: false });
      }
   }

   const isWorking = state.kind === "working";
   const refusal = state.kind === "idle" ? state.refusal : null;
   const wasAdded = state.kind === "idle" && state.added;

   return (
      <div className="field">
         <button type="button" className="text-button" disabled={isWorking} onClick={add}>
            Add a passkey
         </button>

         <p role="status">{wasAdded ? "Passkey added." : ""}</p>

         {refusal === null ? null : <p role="alert">{refusal}</p>}
      </div>
   );
}