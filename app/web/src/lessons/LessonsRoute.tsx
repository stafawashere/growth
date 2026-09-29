import { useId, useMemo, useState } from "react";

import { readLibrary } from "../api/client";
import type { LibraryConcept, LibraryLessonState, LibraryPayload, LibraryUnit } from "../api/types";
import { MASTERY_DISCLAIMER, stateCopy } from "../progress/LessonLibrary";
import { useLoad } from "../status/load";
import { LoadFailed, Loading } from "../status/LoadState";
import { Icon } from "../ui/Icon";
import { Page, PageHeader, Section } from "../ui/Page";

/* The Lessons tab (the operator's ruling of 2026-09-29, amending 15 UI, which kept the library
   inside progress). It lists every unit's lessons in curriculum order, filters them by unit or by
   a search, and opens the library reader. */
export interface LessonsRouteProps {
   onOpenLesson: (lessonId: string, conceptName: string) => void;
}

type Mark = "new" | "read" | "later" | "placed";

const MARK_BY_STATE: Record<LibraryLessonState, Mark> = {
   unseen: "new",
   deferred: "new",
   served: "new",
   skipped: "new",
   read: "read",
   bypassed_by_placement: "placed",
   coming_up: "later",
   not_available: "later"
};

function opens(concept: LibraryConcept) {
   return concept.servable && concept.lesson_id !== null;
}

function matchesSearch(concept: LibraryConcept, needle: string) {
   const hasNeedle = needle !== "";

   if (!hasNeedle) {
      return true;
   }

   const inName = concept.name.toLowerCase().includes(needle);
   const inId = concept.concept_id.toLowerCase().includes(needle);

   return inName || inId;
}

function LessonMark(props: { mark: Mark }) {
   const labels: Record<Mark, string> = { new: "Not read yet", read: "Read", later: "Coming later", placed: "Placed, not needed" };

   return (
      <span className="lesson-mark" data-mark={props.mark} title={labels[props.mark]}>
         {props.mark === "read" ? <Icon name="check" /> : null}
         {props.mark === "placed" ? <Icon name="minus" /> : null}
         {props.mark === "later" ? <Icon name="clock" /> : null}
         <span className="visually-hidden">{labels[props.mark]}</span>
      </span>
   );
}

function ConceptRow(props: { concept: LibraryConcept; onOpenLesson: LessonsRouteProps["onOpenLesson"] }) {
   const { concept } = props;
   const mark = MARK_BY_STATE[concept.state] ?? "new";
   const canOpen = opens(concept);
   const actionLabel = concept.state === "read" ? "Read again" : "Start";

   return (
      <li className="list-row lesson-row" data-testid="lesson-library-row" data-state={concept.state}>
         <LessonMark mark={mark} />

         <div className="list-row-body">
            <span className="lesson-library-name">{concept.name}</span>
            <span className="helper">{stateCopy(concept)}</span>
         </div>

         {canOpen ? (
            <div className="list-row-trail">
               <button
                  type="button"
                  className="button-secondary button-small"
                  aria-label={`${actionLabel}: ${concept.name}`}
                  onClick={() => props.onOpenLesson(concept.lesson_id!, concept.name)}
               >
                  {actionLabel}
                  <Icon name="chevron" />
               </button>
            </div>
         ) : null}
      </li>
   );
}

function UnitFilter(props: { units: ReadonlyArray<LibraryUnit>; active: string | null; onChange: (unitId: string | null) => void }) {
   return (
      <div className="unit-pills" role="group" aria-label="Browse by unit">
         <button type="button" className="unit-pill" aria-pressed={props.active === null} onClick={() => props.onChange(null)}>
            <strong>All units</strong>
         </button>

         {props.units.map((unit) => {
            const ready = unit.concepts.filter(opens).length;

            return (
               <button key={unit.id} type="button" className="unit-pill" aria-pressed={props.active === unit.id} onClick={() => props.onChange(unit.id)}>
                  <strong>{unit.name}</strong>
                  <span className="helper">{ready === 0 ? "Coming later" : `${ready} ready`}</span>
               </button>
            );
         })}
      </div>
   );
}

function Navigator(props: { library: LibraryPayload; onOpenLesson: LessonsRouteProps["onOpenLesson"] }) {
   const units = useMemo(() => [...props.library.units].sort((first, second) => first.order - second.order), [props.library]);
   const [query, setQuery] = useState("");
   const [unitId, setUnitId] = useState<string | null>(null);
   const searchId = useId();
   const needle = query.trim().toLowerCase();

   const shown = units
      .filter((unit) => unitId === null || unit.id === unitId)
      .map((unit) => ({ unit, concepts: unit.concepts.filter((concept) => matchesSearch(concept, needle)) }))
      .filter((entry) => entry.concepts.length > 0);

   const hasMatches = shown.length > 0;

   return (
      <section className="lesson-library stack stack-wide" data-testid="lesson-library" aria-label="Lessons">
         <p className="callout">
            <strong>Lessons build context before practice.</strong> {MASTERY_DISCLAIMER}
         </p>

         <div className="form-field">
            <label className="field-label" htmlFor={searchId}>
               Find a concept
            </label>
            <input id={searchId} className="input" type="search" placeholder="Search by name" value={query} onChange={(event) => setQuery(event.target.value)} />
         </div>

         <Section title="Browse by unit" plain>
            <UnitFilter units={units} active={unitId} onChange={setUnitId} />
         </Section>

         {hasMatches ? null : (
            <p className="muted" data-testid="lessons-no-match">
               No lesson matches that search.
            </p>
         )}

         {shown.map(({ unit, concepts }) => (
            <section key={unit.id} className="section lesson-library-unit" data-testid="lesson-library-unit">
               <h2 className="section-header">{unit.name}</h2>

               <ul className="list list-flush">
                  {concepts.map((concept) => (
                     <ConceptRow key={concept.concept_id} concept={concept} onOpenLesson={props.onOpenLesson} />
                  ))}
               </ul>
            </section>
         ))}
      </section>
   );
}

export function LessonsRoute({ onOpenLesson }: LessonsRouteProps) {
   const library = useLoad<LibraryPayload>(readLibrary);

   return (
      <Page
         header={
            <PageHeader
               eyebrow="Course navigator"
               title="Lessons"
               intro="Follow the course in order, or jump straight to a concept you want to revisit."
            />
         }
      >
         {library.kind === "waiting" ? <Loading testId="lessons-tab-waiting" /> : null}

         {library.kind === "failed" ? (
            <div data-testid="lessons-tab-failed">
               <LoadFailed testId="lessons-tab-load-failed" onRetry={library.retry} />
            </div>
         ) : null}

         {library.kind === "loaded" ? <Navigator library={library.value} onOpenLesson={onOpenLesson} /> : null}
      </Page>
   );
}
