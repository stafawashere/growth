import { readLibrary } from "../api/client";
import type { LibraryPayload } from "../api/types";
import { PageHeader } from "../page/PageHeader";
import { LessonLibrary } from "../progress/LessonLibrary";
import { useLoad } from "../status/load";
import { Loading } from "../status/LoadState";

/* The Lessons tab, on the top bar beside Home and Settings (the operator's ruling of 2026-09-29,
   amending 15 UI, which kept the library inside progress). It lists every unit's lessons in
   curriculum order and opens the library reader. */
export interface LessonsRouteProps {
   onOpenLesson: (lessonId: string, conceptName: string) => void;
}

export function LessonsRoute({ onOpenLesson }: LessonsRouteProps) {
   const library = useLoad<LibraryPayload>(readLibrary);

   return (
      <section className="card">
         <PageHeader title="Lessons" />

         {library.kind === "waiting" ? <Loading testId="lessons-tab-waiting" /> : null}

         {library.kind === "failed" ? (
            <p data-testid="lessons-tab-failed" className="muted">
               The lessons could not be loaded.
            </p>
         ) : null}

         {library.kind === "loaded" ? <LessonLibrary library={library.value} onOpenLesson={onOpenLesson} titled={false} /> : null}
      </section>
   );
}