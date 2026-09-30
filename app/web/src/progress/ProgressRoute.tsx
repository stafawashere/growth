import { Suspense, lazy, useState } from "react";

import { readCalibration, readCheckpoints, readLibrary, readMasteryMap, readMockHistory, readPace, readProbe, readRepresentations } from "../api/client";
import type {
   CalibrationPayload,
   CheckpointsPayload,
   LibraryPayload,
   MasteryMapPayload,
   MockHistoryPayload,
   PacePayload,
   ProbePayload,
   RepresentationMatrixPayload
} from "../api/types";
import { CalculatorLink } from "../calculator/CalculatorLink";
import { CALCULATOR_LINK_SHORT } from "../calculator/words";
import { CheckpointRoute } from "../evaluation/CheckpointRoute";
import { ProbeRoute } from "../evaluation/ProbeRoute";
import { CalibrationCurve } from "./CalibrationCurve";
import { CheckpointHistory, ProbeHistory } from "./CheckpointHistory";
import { useLoad } from "../status/load";
import { LessonLibrary } from "./LessonLibrary";
import { MasteryMap } from "./MasteryMap";
import { MockHistory } from "./MockHistory";
import { PaceStatement } from "./PaceStatement";
import { RepresentationMatrix } from "./RepresentationMatrix";
import { SkillDetailDialog } from "./SkillDetail";
import { useAgentScreen } from "../agent/AgentProvider";
import { Loading } from "../status/LoadState";
import type { ProgressTab } from "../routing";
import { Page, PageHeader } from "../ui/Page";
import { TabPanel, Tabs } from "../ui/Tabs";

/* Progress reads its own record, one tab at a time, each loading separately so one failing leaves
   the others drawn. The pace verdict sits above the tabs. The checkpoint and the concept probe open
   from their tabs and come back to them. The Lessons tab opens the library reader (15 UI). The
   shell passes the tab and the openers, so the address carries them; rendered without them,
   progress keeps its own tab and opens each page itself. */
export interface ProgressRouteProps {
   tab?: ProgressTab;
   onChangeTab?: (tab: ProgressTab) => void;
   onOpenLesson?: (lessonId: string, conceptName: string) => void;
   onOpenCheckpoint?: (openCheckpointId: string | null) => void;
   onOpenProbe?: (openAdministrationId: string | null) => void;
}

type ProgressPage =
   | { kind: "overview" }
   | { kind: "checkpoint"; openCheckpointId: string | null }
   | { kind: "probe"; openAdministrationId: string | null }
   | { kind: "lesson"; lessonId: string; conceptName: string };

const PROGRESS_TAB_ITEMS: ReadonlyArray<{ id: ProgressTab; label: string }> = [
   { id: "mastery", label: "Mastery" },
   { id: "calibration", label: "Calibration" },
   { id: "representations", label: "Representations" },
   { id: "checkpoints", label: "Checkpoints" },
   { id: "probes", label: "Concept probes" },
   { id: "lessons", label: "Lessons" }
];

function SectionFailed(props: { testId: string; what: string; onRetry?: () => void }) {
   return (
      <div className="state state-failed">
         <p data-testid={props.testId} role="alert">
            The {props.what} could not be loaded.
         </p>

         {props.onRetry !== undefined ? (
            <button type="button" className="button-secondary" onClick={props.onRetry}>
               Try again
            </button>
         ) : null}
      </div>
   );
}

function Waiting(props: { testId: string }) {
   return <Loading testId={props.testId} />;
}

/* The reader carries the math field, so it loads only when a lesson is opened. */
const LessonRoute = lazy(() => import("../lessons/LessonRoute").then((module) => ({ default: module.LessonRoute })));

function readLibraryAll() {
   return readLibrary();
}

function PaceSection() {
   const pace = useLoad<PacePayload>(readPace);

   if (pace.kind === "waiting") {
      return <Waiting testId="pace-waiting" />;
   }

   if (pace.kind === "failed") {
      return <SectionFailed testId="pace-failed" what="pace verdict" onRetry={pace.retry} />;
   }

   /* The pace card itself does not change; the calculator's measured times live on their own
      section, reached by one link (docs/calculator/design.md, The measured view). */
   return (
      <>
         <PaceStatement pace={pace.value} />

         <p>
            <CalculatorLink label={CALCULATOR_LINK_SHORT} place={{ view: "calculator", section: "measured" }} />
         </p>
      </>
   );
}

function MasteryTab(props: { onOpenLesson: (lessonId: string, conceptName: string) => void }) {
   const mastery = useLoad<MasteryMapPayload>(readMasteryMap);
   const [opened, setOpened] = useState<{ skillId: string; name: string } | null>(null);

   useAgentScreen(opened === null ? null : { kind: "progress", tab: "mastery", skill_id: opened.skillId }, { skillName: opened?.name });

   if (mastery.kind === "waiting") {
      return <Waiting testId="mastery-waiting" />;
   }

   if (mastery.kind === "failed") {
      return <SectionFailed testId="mastery-failed" what="mastery map" onRetry={mastery.retry} />;
   }

   function openLesson(lessonId: string, conceptName: string) {
      setOpened(null);
      props.onOpenLesson(lessonId, conceptName);
   }

   return (
      <>
         <MasteryMap map={mastery.value} onOpenSkill={(skillId, name) => setOpened({ skillId, name })} />

         <SkillDetailDialog skillId={opened?.skillId ?? null} title={opened?.name ?? ""} onClose={() => setOpened(null)} onOpenLesson={openLesson} />
      </>
   );
}

function CalibrationTab() {
   const calibration = useLoad<CalibrationPayload>(readCalibration);

   if (calibration.kind === "waiting") {
      return <Waiting testId="progress-waiting" />;
   }

   if (calibration.kind === "failed") {
      return <SectionFailed testId="progress-failed" what="calibration record" onRetry={calibration.retry} />;
   }

   return <CalibrationCurve calibration={calibration.value} />;
}

function RepresentationsTab() {
   const matrix = useLoad<RepresentationMatrixPayload>(readRepresentations);

   if (matrix.kind === "waiting") {
      return <Waiting testId="matrix-waiting" />;
   }

   if (matrix.kind === "failed") {
      return <SectionFailed testId="matrix-failed" what="representation matrix" onRetry={matrix.retry} />;
   }

   return <RepresentationMatrix matrix={matrix.value} />;
}

function CheckpointsTab(props: { onOpenCheckpoint: (openCheckpointId: string | null) => void }) {
   const checkpoints = useLoad<CheckpointsPayload>(readCheckpoints);
   const mocks = useLoad<MockHistoryPayload>(readMockHistory);

   return (
      <>
         {checkpoints.kind === "waiting" ? <Waiting testId="checkpoints-waiting" /> : null}

         {checkpoints.kind === "failed" ? <SectionFailed testId="checkpoints-failed" what="checkpoint history" onRetry={checkpoints.retry} /> : null}

         {checkpoints.kind === "loaded" ? (
            <CheckpointHistory
               checkpoints={checkpoints.value}
               onOpenCheckpoint={() => props.onOpenCheckpoint(checkpoints.value.availability.open_checkpoint_id)}
            />
         ) : null}

         {mocks.kind === "waiting" ? <Waiting testId="mock-history-waiting" /> : null}

         {mocks.kind === "failed" ? <SectionFailed testId="mock-history-failed" what="mock history" onRetry={mocks.retry} /> : null}

         {mocks.kind === "loaded" ? <MockHistory history={mocks.value} /> : null}
      </>
   );
}

function ProbesTab(props: { onOpenProbe: (openAdministrationId: string | null) => void }) {
   const probe = useLoad<ProbePayload>(readProbe);

   if (probe.kind === "waiting") {
      return <Waiting testId="probe-history-waiting" />;
   }

   if (probe.kind === "failed") {
      return <SectionFailed testId="probe-history-failed" what="concept probe record" onRetry={probe.retry} />;
   }

   return <ProbeHistory probe={probe.value} onOpenProbe={() => props.onOpenProbe(probe.value.availability.open_administration_id)} />;
}

function LessonsTab(props: { onOpenLesson: (lessonId: string, conceptName: string) => void }) {
   const library = useLoad<LibraryPayload>(readLibraryAll);

   if (library.kind === "waiting") {
      return <Waiting testId="lesson-library-waiting" />;
   }

   if (library.kind === "failed") {
      return <SectionFailed testId="lesson-library-failed" what="lesson library" onRetry={library.retry} />;
   }

   return <LessonLibrary library={library.value} onOpenLesson={props.onOpenLesson} />;
}

function ProgressOverview(props: {
   tab: ProgressTab;
   onChangeTab: (tab: ProgressTab) => void;
   onOpenCheckpoint: (openCheckpointId: string | null) => void;
   onOpenProbe: (openAdministrationId: string | null) => void;
   onOpenLesson: (lessonId: string, conceptName: string) => void;
}) {
   const { tab } = props;

   return (
      <Page header={<PageHeader eyebrow="Your record" title="Progress" intro="Pace, mastery, and the evidence behind them." />}>
         <PaceSection />

         <div className="stack stack-loose">
            <Tabs items={PROGRESS_TAB_ITEMS} active={tab} onChange={props.onChangeTab} label="Progress sections" idPrefix="progress" />

            <TabPanel idPrefix="progress" active={tab}>
               {tab === "mastery" ? <MasteryTab onOpenLesson={props.onOpenLesson} /> : null}
               {tab === "calibration" ? <CalibrationTab /> : null}
               {tab === "representations" ? <RepresentationsTab /> : null}
               {tab === "checkpoints" ? <CheckpointsTab onOpenCheckpoint={props.onOpenCheckpoint} /> : null}
               {tab === "probes" ? <ProbesTab onOpenProbe={props.onOpenProbe} /> : null}
               {tab === "lessons" ? <LessonsTab onOpenLesson={props.onOpenLesson} /> : null}
            </TabPanel>
         </div>
      </Page>
   );
}

export function ProgressRoute(props: ProgressRouteProps) {
   const [page, setPage] = useState<ProgressPage>({ kind: "overview" });
   const [ownTab, setOwnTab] = useState<ProgressTab>(props.tab ?? "mastery");

   const isControlled = props.tab !== undefined && props.onChangeTab !== undefined;
   const tab = isControlled ? (props.tab as ProgressTab) : ownTab;
   const changeTab = isControlled ? (props.onChangeTab as (tab: ProgressTab) => void) : setOwnTab;
   const tabName = PROGRESS_TAB_ITEMS.find((item) => item.id === tab)?.label ?? tab;

   useAgentScreen({ kind: "progress", tab }, { tabName });
   const backToOverview = () => setPage({ kind: "overview" });

   if (page.kind === "checkpoint") {
      return <CheckpointRoute openCheckpointId={page.openCheckpointId} onLeave={backToOverview} />;
   }

   if (page.kind === "lesson") {
      return (
         <Suspense fallback={<Loading testId="lesson-waiting" />}>
            <LessonRoute lessonId={page.lessonId} conceptName={page.conceptName} onLeave={backToOverview} />
         </Suspense>
      );
   }

   if (page.kind === "probe") {
      return <ProbeRoute openAdministrationId={page.openAdministrationId} onLeave={backToOverview} />;
   }

   return (
      <ProgressOverview
         tab={tab}
         onChangeTab={changeTab}
         onOpenCheckpoint={props.onOpenCheckpoint ?? ((openCheckpointId) => setPage({ kind: "checkpoint", openCheckpointId }))}
         onOpenProbe={props.onOpenProbe ?? ((openAdministrationId) => setPage({ kind: "probe", openAdministrationId }))}
         onOpenLesson={props.onOpenLesson ?? ((lessonId, conceptName) => setPage({ kind: "lesson", lessonId, conceptName }))}
      />
   );
}
