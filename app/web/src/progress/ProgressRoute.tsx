import { useState } from "react";

import { readCalibration, readCheckpoints, readMasteryMap, readMockHistory, readProbe, readRepresentations } from "../api/client";
import type {
   CalibrationPayload,
   CheckpointsPayload,
   MasteryMapPayload,
   MockHistoryPayload,
   ProbePayload,
   RepresentationMatrixPayload
} from "../api/types";
import { CheckpointRoute } from "../evaluation/CheckpointRoute";
import { ProbeRoute } from "../evaluation/ProbeRoute";
import { CalibrationCurve } from "./CalibrationCurve";
import { CheckpointHistory, ProbeHistory } from "./CheckpointHistory";
import { useLoad } from "./load";
import { MasteryMap } from "./MasteryMap";
import { MockHistory } from "./MockHistory";
import { RepresentationMatrix } from "./RepresentationMatrix";

/* Progress takes no input from the shell: it is reached from home and reads its own record. Each
   section loads separately, so one failing leaves the others drawn. The checkpoint and the concept
   probe open from their sections here and come back here, and neither is ever on the bar. */
export interface ProgressRouteProps {}

type ProgressPage =
   | { kind: "overview" }
   | { kind: "checkpoint"; openCheckpointId: string | null }
   | { kind: "probe"; openAdministrationId: string | null };

function SectionFailed(props: { testId: string; what: string }) {
   return (
      <p data-testid={props.testId} className="muted">
         The {props.what} could not be loaded.
      </p>
   );
}

function Waiting(props: { testId: string }) {
   return <div aria-busy="true" data-testid={props.testId} />;
}

function ProgressOverview(props: {
   onOpenCheckpoint: (openCheckpointId: string | null) => void;
   onOpenProbe: (openAdministrationId: string | null) => void;
}) {
   const mastery = useLoad<MasteryMapPayload>(readMasteryMap);
   const calibration = useLoad<CalibrationPayload>(readCalibration);
   const matrix = useLoad<RepresentationMatrixPayload>(readRepresentations);
   const checkpoints = useLoad<CheckpointsPayload>(readCheckpoints);
   const probe = useLoad<ProbePayload>(readProbe);
   const mocks = useLoad<MockHistoryPayload>(readMockHistory);

   return (
      <section className="card">
         <h1 className="screen-title">Progress</h1>

         {mastery.kind === "waiting" ? <Waiting testId="mastery-waiting" /> : null}

         {mastery.kind === "failed" ? <SectionFailed testId="mastery-failed" what="mastery map" /> : null}

         {mastery.kind === "loaded" ? <MasteryMap map={mastery.value} /> : null}

         {calibration.kind === "waiting" ? <Waiting testId="progress-waiting" /> : null}

         {calibration.kind === "failed" ? <SectionFailed testId="progress-failed" what="calibration record" /> : null}

         {calibration.kind === "loaded" ? <CalibrationCurve calibration={calibration.value} /> : null}

         {matrix.kind === "waiting" ? <Waiting testId="matrix-waiting" /> : null}

         {matrix.kind === "failed" ? <SectionFailed testId="matrix-failed" what="representation matrix" /> : null}

         {matrix.kind === "loaded" ? <RepresentationMatrix matrix={matrix.value} /> : null}

         {checkpoints.kind === "waiting" ? <Waiting testId="checkpoints-waiting" /> : null}

         {checkpoints.kind === "failed" ? (
            <SectionFailed testId="checkpoints-failed" what="checkpoint history" />
         ) : null}

         {checkpoints.kind === "loaded" ? (
            <CheckpointHistory
               checkpoints={checkpoints.value}
               onOpenCheckpoint={() => props.onOpenCheckpoint(checkpoints.value.availability.open_checkpoint_id)}
            />
         ) : null}

         {mocks.kind === "waiting" ? <Waiting testId="mock-history-waiting" /> : null}

         {mocks.kind === "failed" ? <SectionFailed testId="mock-history-failed" what="mock history" /> : null}

         {mocks.kind === "loaded" ? <MockHistory history={mocks.value} /> : null}

         {probe.kind === "waiting" ? <Waiting testId="probe-history-waiting" /> : null}

         {probe.kind === "failed" ? <SectionFailed testId="probe-history-failed" what="concept probe record" /> : null}

         {probe.kind === "loaded" ? (
            <ProbeHistory
               probe={probe.value}
               onOpenProbe={() => props.onOpenProbe(probe.value.availability.open_administration_id)}
            />
         ) : null}
      </section>
   );
}

export function ProgressRoute(_props: ProgressRouteProps) {
   const [page, setPage] = useState<ProgressPage>({ kind: "overview" });

   const backToOverview = () => setPage({ kind: "overview" });

   if (page.kind === "checkpoint") {
      return <CheckpointRoute openCheckpointId={page.openCheckpointId} onLeave={backToOverview} />;
   }

   if (page.kind === "probe") {
      return <ProbeRoute openAdministrationId={page.openAdministrationId} onLeave={backToOverview} />;
   }

   return (
      <ProgressOverview
         onOpenCheckpoint={(openCheckpointId) => setPage({ kind: "checkpoint", openCheckpointId })}
         onOpenProbe={(openAdministrationId) => setPage({ kind: "probe", openAdministrationId })}
      />
   );
}
