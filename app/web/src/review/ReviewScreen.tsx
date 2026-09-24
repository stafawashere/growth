import { useState } from "react";

import type { ComingBackEntry, ErrorNoteEntry, ProvisionalPoint } from "../api/types";
import { ProvisionalPoints } from "./ProvisionalPoints";

/* The review screen, 08-design-brief.md "Review": what is coming back, the student's own error
   notes, and the provisional points. The list arrives in the order block 1 serves it, so the
   hypercorrection lane, the errors made at confident, comes first. */

export interface ReviewScreenProps {
   comingBack: ReadonlyArray<ComingBackEntry>;
   errorNotes: ReadonlyArray<ErrorNoteEntry>;
   provisionalPoints: ReadonlyArray<ProvisionalPoint>;
   onSaveNote: (entry: ErrorNoteEntry, note: string) => Promise<void>;
   onAskForReread?: (gradingId: string) => void;
}

const WAS_RATED: Record<string, string> = {
   confident: "was confident",
   unsure: "was unsure",
   guess: "was a guess"
};

export function whenBack(daysUntil: number) {
   if (daysUntil === 0) {
      return "today";
   }

   return daysUntil === 1 ? "tomorrow" : `in ${daysUntil} days`;
}

function ComingBack({ entries }: { entries: ReadonlyArray<ComingBackEntry> }) {
   const hasEntries = entries.length > 0;

   return (
      <section aria-labelledby="coming-back-heading">
         <h2 id="coming-back-heading" className="section-heading">
            Coming back to you
         </h2>

         {hasEntries ? (
            <ul className="review-list">
               {entries.map((entry) => {
                  const rating = entry.confidence === null ? null : WAS_RATED[entry.confidence];

                  return (
                     <li key={entry.item_id} data-testid="coming-back" data-lane={entry.lane}>
                        <span className="label-heading">{whenBack(entry.days_until)}</span>
                        <span>{entry.label}</span>
                        {rating === null ? null : <span className="muted">({rating})</span>}
                     </li>
                  );
               })}
            </ul>
         ) : (
            <p className="muted" data-testid="coming-back-empty">
               Nothing you corrected is waiting to come back.
            </p>
         )}
      </section>
   );
}

function matches(entry: ErrorNoteEntry, query: string) {
   const needle = query.trim().toLowerCase();
   const isEmptyQuery = needle === "";

   if (isEmptyQuery) {
      return true;
   }

   const inNote = entry.note.toLowerCase().includes(needle);
   const inLabel = entry.label.toLowerCase().includes(needle);

   return inNote || inLabel;
}

function NoteRow(props: { entry: ErrorNoteEntry; onSave: (entry: ErrorNoteEntry, note: string) => Promise<void> }) {
   const { entry, onSave } = props;
   const [draft, setDraft] = useState<string | null>(null);
   const [failure, setFailure] = useState<string | null>(null);
   const [isSaving, setIsSaving] = useState(false);

   const isEditing = draft !== null;
   const fieldId = `error-note-edit-${entry.attempt_id}`;

   function save() {
      const note = (draft ?? "").trim();
      const isBlank = note === "";

      if (isBlank) {
         setFailure("A note cannot be empty.");

         return;
      }

      setIsSaving(true);
      setFailure(null);

      onSave(entry, note).then(
         () => {
            setIsSaving(false);
            setDraft(null);
         },
         (problem: unknown) => {
            const detail = problem instanceof Error && problem.message !== "" ? problem.message : "The note was not saved.";

            setIsSaving(false);
            setFailure(detail);
         }
      );
   }

   if (isEditing) {
      return (
         <li data-testid="error-note">
            <div className="field">
               <label htmlFor={fieldId}>In one line, what went wrong?</label>
               <input
                  id={fieldId}
                  type="text"
                  value={draft}
                  onChange={(event) => setDraft(event.target.value)}
                  onKeyDown={(event) => {
                     if (event.key === "Enter") {
                        save();
                     }

                     if (event.key === "Escape") {
                        setDraft(null);
                     }
                  }}
               />
            </div>

            <button type="button" className="text-button" disabled={isSaving} onClick={save}>
               Save
            </button>

            <button type="button" className="text-button" disabled={isSaving} onClick={() => setDraft(null)}>
               Cancel
            </button>

            {failure === null ? null : (
               <p role="alert" className="muted">
                  {failure}
               </p>
            )}
         </li>
      );
   }

   return (
      <li data-testid="error-note">
         <q>{entry.note}</q>
         <span className="caption">
            {entry.label}, {entry.written_on}
         </span>
         <button
            type="button"
            className="text-button"
            aria-label={`Edit the note "${entry.note}"`}
            onClick={() => setDraft(entry.note)}
         >
            edit
         </button>
      </li>
   );
}

function ErrorNotes(props: {
   notes: ReadonlyArray<ErrorNoteEntry>;
   onSave: (entry: ErrorNoteEntry, note: string) => Promise<void>;
}) {
   const { notes, onSave } = props;
   const [query, setQuery] = useState("");

   const hasNotes = notes.length > 0;
   const shown = notes.filter((entry) => matches(entry, query));
   const hasMatches = shown.length > 0;
   const searchFoundNothing = hasNotes && !hasMatches;

   return (
      <section aria-labelledby="error-notes-heading">
         <h2 id="error-notes-heading" className="section-heading">
            My error notes
         </h2>

         {hasNotes ? (
            <div className="field">
               <label htmlFor="error-note-search">Search my notes</label>
               <input
                  id="error-note-search"
                  type="search"
                  value={query}
                  onChange={(event) => setQuery(event.target.value)}
               />
            </div>
         ) : (
            <p className="muted" data-testid="error-notes-empty">
               No error notes yet. You write one in a set, after an item you got wrong.
            </p>
         )}

         {searchFoundNothing ? (
            <p className="muted" data-testid="error-notes-no-match">
               No note matches that search.
            </p>
         ) : null}

         {hasMatches ? (
            <ul className="review-list">
               {shown.map((entry) => (
                  <NoteRow key={entry.attempt_id} entry={entry} onSave={onSave} />
               ))}
            </ul>
         ) : null}
      </section>
   );
}

export function ReviewScreen(props: ReviewScreenProps) {
   return (
      <section className="card review">
         <h1 className="screen-title">Review</h1>

         <ComingBack entries={props.comingBack} />

         <ErrorNotes notes={props.errorNotes} onSave={props.onSaveNote} />

         <ProvisionalPoints points={props.provisionalPoints} onAskForReread={props.onAskForReread} />
      </section>
   );
}
