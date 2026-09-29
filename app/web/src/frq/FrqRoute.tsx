import { useState } from "react";

import { ApiError, openUnitCheck, readFrqUnits } from "../api/client";
import type { FrqQuestion, UnitCheckPayload } from "../api/types";
import { CaptureScreen } from "./CaptureScreen";
import { useLoad } from "../status/load";
import { Loading } from "../status/LoadState";
import { Icon } from "../ui/Icon";
import { List } from "../ui/List";
import { Page, PageHeader } from "../ui/Page";

/* The free-response part of a unit check, reached from home (08: home offers progress, review and
   the assessment modes, and none of them is the landing screen). The student picks a unit, the
   server picks its least-attempted questions, and each question runs through CaptureScreen. */

export interface FrqRouteProps {
   pollMilliseconds?: number;
}

/* A free-response unit check once it is open: its questions, and each one through CaptureScreen. */
export function FrqUnitCheck(props: { check: UnitCheckPayload; pollMilliseconds?: number; onLeave?: () => void; title?: string }) {
   const { check } = props;
   const [question, setQuestion] = useState<FrqQuestion | null>(null);

   if (question !== null) {
      return (
         <div className="stack stack-loose">
            <div className="cluster">
               <button type="button" className="back-link" onClick={() => setQuestion(null)}>
                  <Icon name="back" />
                  Back to the unit check
               </button>
            </div>

            <CaptureScreen sessionId={check.session_id} question={question} pollMilliseconds={props.pollMilliseconds} />
         </div>
      );
   }

   return (
      <section data-testid="unit-check">
         <Page
            header={
               <PageHeader
                  back={props.onLeave === undefined ? undefined : { label: "Assessments", onBack: props.onLeave }}
                  eyebrow={props.onLeave === undefined ? "Untimed" : undefined}
                  title={props.title ?? "Unit check, free response"}
                  intro="Untimed. Each answer is graded point by point once you confirm what the app read from your page."
               />
            }
         >
            <List as="ul">
               {check.questions.map((entry, index) => (
                  <li key={entry.id} className="list-row">
                     <span className="list-row-lead">Question {index + 1}</span>

                     <div className="list-row-body">
                        <span className="list-row-title">{entry.parts.length} parts</span>
                     </div>

                     <div className="list-row-trail">
                        <button type="button" className="button-secondary button-small" aria-label={`Question ${index + 1}, ${entry.parts.length} parts`} onClick={() => setQuestion(entry)}>
                           Open
                           <Icon name="chevron" />
                        </button>
                     </div>
                  </li>
               ))}
            </List>
         </Page>
      </section>
   );
}

export function FrqRoute({ pollMilliseconds }: FrqRouteProps) {
   const units = useLoad(readFrqUnits);
   const [check, setCheck] = useState<UnitCheckPayload | null>(null);
   const [problem, setProblem] = useState<string | null>(null);

   async function start(unitId: string) {
      setProblem(null);

      try {
         setCheck(await openUnitCheck(unitId));
      } catch (failure) {
         const hasDetail = failure instanceof ApiError && failure.detail !== "";

         setProblem(hasDetail ? failure.detail : "The unit check could not be opened.");
      }
   }

   if (check !== null) {
      return <FrqUnitCheck check={check} pollMilliseconds={pollMilliseconds} />;
   }

   if (units.kind === "waiting") {
      return <Loading testId="frq-waiting" />;
   }

   if (units.kind === "failed") {
      return (
         <Page header={<PageHeader title="Free response" />}>
            <p className="muted">The free-response questions could not be loaded.</p>
         </Page>
      );
   }

   return (
      <section data-testid="frq-units">
         <Page header={<PageHeader title="Free response" intro="Choose a unit. Its free-response questions are served as an untimed unit check." />}>
            {problem !== null ? <p role="alert">{problem}</p> : null}

            <List as="ul">
               {units.value.units.map((unit) => (
                  <li key={unit.unit_id} className="list-row">
                     <div className="list-row-body">
                        <button type="button" className="text-button list-row-title" onClick={() => start(unit.unit_id)}>
                           {unit.title}
                        </button>
                     </div>
                  </li>
               ))}
            </List>
         </Page>
      </section>
   );
}
