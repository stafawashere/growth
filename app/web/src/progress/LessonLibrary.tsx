import type { LibraryConcept, LibraryLessonState, LibraryPayload } from "../api/types";
import { formatPlanDate } from "../home/dates";

/* 15 UI, Library: progress lists the units of data/curriculum.json in order, then each concept
   with its name and its state. A row whose concept has a signed-off lesson opens the library
   reader. There is no percent bar and no count of lessons read, because 08 bans percent-complete
   bars and reading is not mastery; the copy says so. A read date is written the way 08 writes a
   date. */

export const MASTERY_DISCLAIMER = "Reading a lesson does not count toward mastery.";

export const STATE_COPY: Record<LibraryLessonState, string> = {
   unseen: "Not read",
   deferred: "Not read",
   served: "Not read",
   skipped: "Not read",
   read: "Read on {date}",
   bypassed_by_placement: "Placed, not needed",
   coming_up: "Coming up",
   not_available: "Not yet available"
};

export function stateCopy(concept: LibraryConcept) {
   const copy = STATE_COPY[concept.state] ?? STATE_COPY.unseen;
   const hasDate = concept.state === "read" && concept.read_at !== null;

   if (concept.state === "read" && !hasDate) {
      return "Read";
   }

   return hasDate ? copy.replace("{date}", formatPlanDate(concept.read_at!.slice(0, 10))) : copy;
}

export interface LessonLibraryProps {
   library: LibraryPayload;
   onOpenLesson: (lessonId: string, conceptName: string) => void;
   /* false on the Lessons tab, whose page header already names the list. */
   titled?: boolean;
}

function Row({ concept, onOpenLesson }: { concept: LibraryConcept; onOpenLesson: LessonLibraryProps["onOpenLesson"] }) {
   const opens = concept.servable && concept.lesson_id !== null;
   const content = (
      <>
         <span className="lesson-library-name">{concept.name}</span>
         <span className="muted">{stateCopy(concept)}</span>
      </>
   );

   if (!opens) {
      return (
         <li className="lesson-library-row" data-testid="lesson-library-row" data-state={concept.state}>
            {content}
         </li>
      );
   }

   return (
      <li data-state={concept.state}>
         <button
            type="button"
            className="text-button lesson-library-row"
            data-testid="lesson-library-row"
            onClick={() => onOpenLesson(concept.lesson_id!, concept.name)}
         >
            {content}
         </button>
      </li>
   );
}

export function LessonLibrary({ library, onOpenLesson, titled = true }: LessonLibraryProps) {
   const units = [...library.units].sort((first, second) => first.order - second.order);

   return (
      <section
         className="lesson-library"
         data-testid="lesson-library"
         aria-labelledby={titled ? "lesson-library-heading" : undefined}
         aria-label={titled ? undefined : "Lessons"}
      >
         {titled ? (
            <h2 className="section-heading" id="lesson-library-heading">
               Lessons
            </h2>
         ) : null}

         <p className="muted">{MASTERY_DISCLAIMER}</p>

         {units.map((unit) => (
            <section key={unit.id} className="lesson-library-unit" data-testid="lesson-library-unit">
               <h3 className="label-heading">{unit.name}</h3>

               <ul className="lesson-library-list">
                  {unit.concepts.map((concept) => (
                     <Row key={concept.concept_id} concept={concept} onOpenLesson={onOpenLesson} />
                  ))}
               </ul>
            </section>
         ))}
      </section>
   );
}
