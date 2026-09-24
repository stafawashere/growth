import { useEffect, useRef, useState } from "react";

import {
   ApiError,
   finishCheckpoint,
   readCheckpoint,
   scoreCheckpointPart,
   startCheckpoint
} from "../api/client";
import type { CheckpointView } from "../api/types";
import { CheckpointIntro, CheckpointScreen } from "./CheckpointScreen";

/* openCheckpointId names the checkpoint GET /checkpoints reported open, and null starts a new one
   once the student chooses to from the intro. */
export interface CheckpointRouteProps {
   openCheckpointId: string | null;
   onLeave: () => void;
}

type CheckpointStage =
   | { kind: "intro"; refusal: string | null }
   | { kind: "waiting" }
   | { kind: "failed" }
   | { kind: "open"; checkpoint: CheckpointView };

function refusalOf(failure: unknown) {
   const isServerRefusal = failure instanceof ApiError;

   return isServerRefusal ? failure.detail : "The checkpoint could not be started.";
}

export function CheckpointRoute({ openCheckpointId, onLeave }: CheckpointRouteProps) {
   const isResuming = openCheckpointId !== null;

   const [stage, setStage] = useState<CheckpointStage>(
      isResuming ? { kind: "waiting" } : { kind: "intro", refusal: null }
   );

   const inFlight = useRef(false);

   useEffect(() => {
      if (openCheckpointId === null) {
         return undefined;
      }

      let isCurrent = true;

      readCheckpoint(openCheckpointId).then(
         (checkpoint) => {
            if (isCurrent) {
               setStage({ kind: "open", checkpoint });
            }
         },
         () => {
            if (isCurrent) {
               setStage({ kind: "failed" });
            }
         }
      );

      return () => {
         isCurrent = false;
      };
   }, [openCheckpointId]);

   async function start() {
      setStage({ kind: "waiting" });

      try {
         const checkpoint = await startCheckpoint();

         setStage({ kind: "open", checkpoint });
      } catch (failure) {
         setStage({ kind: "intro", refusal: refusalOf(failure) });
      }
   }

   async function exclusively(action: (checkpointId: string) => Promise<CheckpointView>) {
      const isOpen = stage.kind === "open";
      const canAct = isOpen && !inFlight.current;

      if (!canAct) {
         return false;
      }

      inFlight.current = true;

      try {
         const checkpoint = await action(stage.checkpoint.id);

         setStage({ kind: "open", checkpoint });

         return true;
      } catch {
         return false;
      } finally {
         inFlight.current = false;
      }
   }

   function score(recordId: string, pointsEarned: number) {
      return exclusively((checkpointId) =>
         scoreCheckpointPart(checkpointId, { record_id: recordId, points_earned: pointsEarned })
      );
   }

   function finish() {
      return exclusively((checkpointId) => finishCheckpoint(checkpointId));
   }

   if (stage.kind === "intro") {
      return <CheckpointIntro refusal={stage.refusal} onStart={start} onLeave={onLeave} />;
   }

   if (stage.kind === "waiting") {
      return <section aria-busy="true" data-testid="checkpoint-waiting" />;
   }

   if (stage.kind === "failed") {
      return (
         <section className="card">
            <p data-testid="checkpoint-failed" className="muted">
               The checkpoint could not be loaded.
            </p>

            <button type="button" className="text-button" onClick={onLeave}>
               Back to progress
            </button>
         </section>
      );
   }

   return <CheckpointScreen checkpoint={stage.checkpoint} onScore={score} onFinish={finish} onLeave={onLeave} />;
}