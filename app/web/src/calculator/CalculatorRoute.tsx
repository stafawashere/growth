import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { readCalculatorCard, readCalculatorCards, readCalculatorMeasured, startCalculatorDrill } from "../api/client";
import type {
   CalculatorAnswerPayload,
   CalculatorCapability,
   CalculatorCard,
   CalculatorCardsPayload,
   CalculatorDrill,
   CalculatorDrillRequestCapability,
   CalculatorMeasuredPayload
} from "../api/types";
import { MathText } from "../math/MathText";
import type { CalculatorSection, Place } from "../routing";
import { useLoad } from "../status/load";
import { LoadFailed, Loading, RETRY_LABEL } from "../status/LoadState";
import { Page, PageHeader } from "../ui/Page";
import { TabPanel, Tabs } from "../ui/Tabs";
import { CapabilityChooser, type AnsweredCounts } from "./CapabilityChooser";
import { DrillScreen } from "./DrillScreen";
import { MeasuredView } from "./MeasuredView";
import { ProcedureCard } from "./ProcedureCard";
import {
   BACK_TO_CARDS,
   CALCULATOR_EYEBROW,
   CALCULATOR_PRACTICE,
   CAPABILITY_ORDER,
   CARD_LIST_LABEL,
   DRILL_START_FAILED,
   SECTION_DRILL,
   SECTION_MEASURED,
   SECTION_PROCEDURES,
   isCapability
} from "./words";

/* The Calculator destination (docs/calculator/design.md): one page, three sections as tabs,
   Procedures, Drill and Measured, with the section, the open card and the drilled capability in
   the address. Nothing here is inserted into a session, credited, or scheduled. */

export interface CalculatorRouteProps {
   section: CalculatorSection;
   cardId?: string;
   capability?: string;
   offline?: boolean;
   go: (place: Place) => void;
}

const SECTION_ITEMS: ReadonlyArray<{ id: CalculatorSection; label: string }> = [
   { id: "cards", label: SECTION_PROCEDURES },
   { id: "drill", label: SECTION_DRILL },
   { id: "measured", label: SECTION_MEASURED }
];

/* app.css's phone breakpoint, where the clock moves into the page header. */
export const PHONE_MAX_WIDTH = 600;

function isPhoneWidth() {
   return typeof window !== "undefined" && window.innerWidth <= PHONE_MAX_WIDTH;
}

function usePhoneWidth() {
   const [isPhone, setIsPhone] = useState(isPhoneWidth);

   useEffect(() => {
      function follow() {
         setIsPhone(isPhoneWidth());
      }

      window.addEventListener("resize", follow);

      return () => window.removeEventListener("resize", follow);
   }, []);

   return isPhone;
}

function CardView(props: { cardId: string; onDrill: (capability: CalculatorCapability) => void; onBack: () => void }) {
   const { cardId } = props;
   const read = useCallback(() => readCalculatorCard(cardId), [cardId]);
   const card = useLoad<CalculatorCard>(read);

   return (
      <div className="stack">
         <div>
            <button type="button" className="text-button" onClick={props.onBack}>
               {BACK_TO_CARDS}
            </button>
         </div>

         {card.kind === "waiting" ? <Loading testId="calculator-card-waiting" /> : null}

         {card.kind === "failed" ? <LoadFailed testId="calculator-card-failed" onRetry={card.retry} /> : null}

         {card.kind === "loaded" ? <ProcedureCard card={card.value} onDrill={props.onDrill} /> : null}
      </div>
   );
}

function CardList(props: { cards: CalculatorCardsPayload; onOpen: (cardId: string) => void }) {
   return (
      <ul className="list" aria-label={CARD_LIST_LABEL} data-testid="calculator-cards">
         {props.cards.cards.map((card) => (
            <li key={card.id} className="list-row list-row-start">
               <div className="stack stack-tight">
                  <button type="button" className="text-button" onClick={() => props.onOpen(card.id)}>
                     {card.title}
                  </button>

                  <p className="helper">
                     <MathText text={card.task} />
                  </p>
               </div>
            </li>
         ))}
      </ul>
   );
}

function CardsSection(props: { cardId?: string; capability?: string; go: (place: Place) => void }) {
   const cards = useLoad<CalculatorCardsPayload>(readCalculatorCards);
   const { go } = props;

   function drill(capability: CalculatorCapability) {
      go({ view: "calculator", section: "drill", capability });
   }

   function openCard(cardId: string) {
      go({ view: "calculator", section: "cards", cardId });
   }

   function backToList() {
      go({ view: "calculator", section: "cards" });
   }

   if (props.cardId !== undefined) {
      return <CardView cardId={props.cardId} onDrill={drill} onBack={backToList} />;
   }

   if (cards.kind === "waiting") {
      return <Loading testId="calculator-cards-waiting" />;
   }

   if (cards.kind === "failed") {
      return <LoadFailed testId="calculator-cards-failed" onRetry={cards.retry} />;
   }

   const cardForCapability = cards.value.cards.find((card) => card.capability === props.capability);

   if (cardForCapability !== undefined) {
      return <CardView cardId={cardForCapability.id} onDrill={drill} onBack={backToList} />;
   }

   return <CardList cards={cards.value} onOpen={openCard} />;
}

type DrillState = { kind: "none" } | { kind: "starting" } | { kind: "failed" } | { kind: "ready"; drill: CalculatorDrill };

function countsFrom(measured: CalculatorMeasuredPayload | null, extra: AnsweredCounts): AnsweredCounts | null {
   if (measured === null) {
      return null;
   }

   const counts: AnsweredCounts = {};
   let total = 0;

   for (const capability of CAPABILITY_ORDER) {
      const recorded = measured.capabilities.find((measure) => measure.capability === capability)?.answered ?? 0;
      const answered = recorded + (extra[capability] ?? 0);

      counts[capability] = answered;
      total += answered;
   }

   counts.mixed = total;

   return counts;
}

function DrillSection(props: {
   capability?: string;
   offline: boolean;
   clockSlot: HTMLElement | null;
   go: (place: Place) => void;
}) {
   const { go } = props;
   const measured = useLoad<CalculatorMeasuredPayload>(readCalculatorMeasured);
   const [extra, setExtra] = useState<AnsweredCounts>({});
   const [serial, setSerial] = useState(0);
   const [drill, setDrill] = useState<DrillState>({ kind: "none" });
   const [budgetShownFor, setBudgetShownFor] = useState<string | null>(null);
   const [arrivedByChoice, setArrivedByChoice] = useState(false);
   const [focusChooser, setFocusChooser] = useState(false);
   const wanted = useRef<string | null>(null);
   const chooser = useRef<HTMLDivElement | null>(null);

   const requested: CalculatorDrillRequestCapability | null = isCapability(props.capability) ? props.capability : null;
   const measuredValue = measured.kind === "loaded" ? measured.value : null;
   const counts = useMemo(() => countsFrom(measuredValue, extra), [measuredValue, extra]);

   /* A drill is served once per request: the ref keeps a remounted effect from drawing a second
      task, and an answer for a request that has since changed is dropped. */
   useEffect(() => {
      if (requested === null) {
         wanted.current = null;
         setDrill({ kind: "none" });

         return;
      }

      const key = `${requested}:${serial}`;

      if (wanted.current === key) {
         return;
      }

      wanted.current = key;
      setDrill({ kind: "starting" });

      startCalculatorDrill({ capability: requested }).then(
         (served) => {
            if (wanted.current === key) {
               setDrill({ kind: "ready", drill: served });
            }
         },
         () => {
            if (wanted.current === key) {
               setDrill({ kind: "failed" });
            }
         }
      );
   }, [requested, serial]);

   useEffect(() => {
      if (focusChooser) {
         chooser.current?.focus();
         setFocusChooser(false);
      }
   }, [focusChooser]);

   function choose(capability: CalculatorDrillRequestCapability) {
      setArrivedByChoice(true);

      if (capability === requested) {
         setSerial((previous) => previous + 1);

         return;
      }

      go({ view: "calculator", section: "drill", capability });
   }

   function next() {
      setArrivedByChoice(true);
      setSerial((previous) => previous + 1);
   }

   function changeCapability() {
      go({ view: "calculator", section: "drill" });
      setFocusChooser(true);
   }

   function answered(answer: CalculatorAnswerPayload, capability: CalculatorCapability) {
      setExtra((previous) => ({ ...previous, [capability]: (previous[capability] ?? 0) + 1 }));
      setBudgetShownFor((previous) => previous ?? answer.drill_id);
   }

   return (
      <div className="stack stack-loose">
         <CapabilityChooser chosen={requested} counts={counts} onChoose={choose} ref={chooser} />

         {drill.kind === "starting" ? <Loading testId="calculator-drill-waiting" /> : null}

         {drill.kind === "failed" ? (
            <div className="state state-failed" data-testid="calculator-drill-failed">
               <p role="alert">{DRILL_START_FAILED}</p>

               <button type="button" className="button-secondary" onClick={() => setSerial((previous) => previous + 1)}>
                  {RETRY_LABEL}
               </button>
            </div>
         ) : null}

         {drill.kind === "ready" ? (
            <DrillScreen
               key={drill.drill.drill_id}
               drill={drill.drill}
               offline={props.offline}
               showsBudget={budgetShownFor === null || budgetShownFor === drill.drill.drill_id}
               focusTaskOnArrival={arrivedByChoice}
               onAnswered={(answer) => answered(answer, drill.drill.capability)}
               onNext={next}
               onChangeCapability={changeCapability}
               clockSlot={props.clockSlot}
            />
         ) : null}
      </div>
   );
}

function MeasuredSection() {
   const measured = useLoad<CalculatorMeasuredPayload>(readCalculatorMeasured);

   if (measured.kind === "waiting") {
      return <Loading testId="calculator-measured-waiting" />;
   }

   if (measured.kind === "failed") {
      return <LoadFailed testId="calculator-measured-failed" onRetry={measured.retry} />;
   }

   return <MeasuredView measured={measured.value} />;
}

export function CalculatorRoute(props: CalculatorRouteProps) {
   const { section, go } = props;
   const isPhone = usePhoneWidth();
   const [clockSlot, setClockSlot] = useState<HTMLElement | null>(null);
   const holdsClockInHeader = isPhone && section === "drill";

   const header = (
      <PageHeader
         eyebrow={CALCULATOR_EYEBROW}
         title={CALCULATOR_PRACTICE}
         aside={holdsClockInHeader ? <div className="drill-clock-slot" ref={setClockSlot} /> : undefined}
      />
   );

   return (
      <Page header={header} testId="calculator-route">
         <div className="stack stack-loose">
            <Tabs
               items={SECTION_ITEMS}
               active={section}
               onChange={(next) => go({ view: "calculator", section: next })}
               label="Calculator sections"
               idPrefix="calculator"
            />

            <TabPanel idPrefix="calculator" active={section}>
               {section === "cards" ? <CardsSection cardId={props.cardId} capability={props.capability} go={go} /> : null}

               {section === "drill" ? (
                  <DrillSection capability={props.capability} offline={props.offline === true} clockSlot={holdsClockInHeader ? clockSlot : null} go={go} />
               ) : null}

               {section === "measured" ? <MeasuredSection /> : null}
            </TabPanel>
         </div>
      </Page>
   );
}
