import { useState } from "react";

import type { ComingBackEntry, ErrorNoteEntry, ProvisionalPoint } from "../api/types";
import { Icon } from "../ui/Icon";
import { List } from "../ui/List";
import { Page, PageHeader } from "../ui/Page";
import { TabPanel, Tabs } from "../ui/Tabs";
import { ProvisionalPoints } from "./ProvisionalPoints";

/* The review screen, 08-design-brief.md "Review": what is coming back, the student's own error
   notes, and the provisional points. The list arrives in the order block 1 serves it, so the
   hypercorrection lane, the errors made at confident, comes first. */

export type ReviewTab = "coming" | "notes" | "provisional";

export interface ReviewScreenProps {
   comingBack: ReadonlyArray<ComingBackEntry>;
   errorNotes: ReadonlyArray<ErrorNoteEntry>;
   provisionalPoints: ReadonlyArray<ProvisionalPoint>;
   onSaveNote: (entry: ErrorNoteEntry, note: string) => Promise<void>;
   onAskForReread?: (gradingId: string) => void;
   onStartPractice?: () => void;
   initialTab?: ReviewTab;
}

const REVIEW_TABS: ReadonlyArray<{ id: ReviewTab; label: string }> = [
   { id: "coming", label: "Coming back" },
   { id: "notes", label: "My error notes" },
   { id: "provisional", label: "Provisional points" }
];

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

function ComingBack({ entries, onStartPractice }: { entries: ReadonlyArray<ComingBackEntry>; onStartPractice?: () => void }) {
   const hasEntries = entries.length > 0;
   const offersPractice = hasEntries && onStartPractice !== undefined;

   return (
      <section aria-labelledby="coming-back-heading" className="section">
         <div className="section-header section-header-plain">
            <h2 id="coming-back-heading" className="visually-hidden">
               Coming back to you
            </h2>

            <p className="helper">High-confidence errors come first.</p>

            {offersPractice ? (
               <button type="button" className="button-secondary button-small" onClick={onStartPractice}>
                  Practise these now
               </button>
            ) : null}
         </div>

         {hasEntries ? (
            <List as="ul">
               {entries.map((entry) => {
                  const rating = entry.confidence === null ? null : WAS_RATED[entry.confidence];
                  const isPriority = entry.lane === "hypercorrection";

                  return (
                     <li key={entry.item_id} className="list-row" data-testid="coming-back" data-lane={entry.lane}>
                        <span className="list-row-lead label-heading">{whenBack(entry.days_until)}</span>

                        <div className="list-row-body">
                           <span className="list-row-title">{entry.label}</span>
                           {rating === null ? null : <span className="list-row-meta">({rating})</span>}
                        </div>

                        {isPriority ? (
                           <span className="list-row-trail" title="Priority review: an error made while confident">
                              <Icon name="flag" />
                           </span>
                        ) : null}
                     </li>
                  );
               })}
            </List>
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
         <li data-testid="error-note" className="list-row list-row-start">
            <div className="list-row-body">
               <div className="form-field">
                  <label className="field-label" htmlFor={fieldId}>
                     In one line, what went wrong?
                  </label>
                  <input
                     id={fieldId}
                     className="input"
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

               {failure === null ? null : (
                  <p role="alert" className="field-error">
                     {failure}
                  </p>
               )}
            </div>

            <div className="list-row-trail">
               <button type="button" className="button-secondary button-small" disabled={isSaving} onClick={save}>
                  Save
               </button>

               <button type="button" className="text-button" disabled={isSaving} onClick={() => setDraft(null)}>
                  Cancel
               </button>
            </div>
         </li>
      );
   }

   return (
      <li data-testid="error-note" className="list-row list-row-start">
         <div className="list-row-body">
            <q className="note-quote">{entry.note}</q>
            <span className="caption">
               {entry.label}, {entry.written_on}
            </span>
         </div>

         <div className="list-row-trail">
            <button type="button" className="text-button" aria-label={`Edit the note "${entry.note}"`} onClick={() => setDraft(entry.note)}>
               <Icon name="edit" />
               edit
            </button>
         </div>
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
      <section aria-labelledby="error-notes-heading" className="section">
         <h2 id="error-notes-heading" className="visually-hidden">
            My error notes
         </h2>

         {hasNotes ? (
            <div className="form-field">
               <label className="field-label" htmlFor="error-note-search">
                  Search my notes
               </label>
               <input id="error-note-search" className="input" type="search" value={query} onChange={(event) => setQuery(event.target.value)} />
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
            <List as="ul">
               {shown.map((entry) => (
                  <NoteRow key={entry.attempt_id} entry={entry} onSave={onSave} />
               ))}
            </List>
         ) : null}
      </section>
   );
}

export function ReviewScreen(props: ReviewScreenProps) {
   const [tab, setTab] = useState<ReviewTab>(props.initialTab ?? "coming");

   return (
      <section className="review" data-testid="review-screen">
         <Page header={<PageHeader eyebrow="Revisit, refine, retain" title="Review" intro="The ideas worth meeting again." />}>
            <div className="stack stack-loose">
               <Tabs items={REVIEW_TABS} active={tab} onChange={setTab} label="Review sections" idPrefix="review" />

               <TabPanel idPrefix="review" active={tab}>
                  {tab === "coming" ? <ComingBack entries={props.comingBack} onStartPractice={props.onStartPractice} /> : null}

                  {tab === "notes" ? <ErrorNotes notes={props.errorNotes} onSave={props.onSaveNote} /> : null}

                  {tab === "provisional" ? <ProvisionalPoints points={props.provisionalPoints} onAskForReread={props.onAskForReread} /> : null}
               </TabPanel>
            </div>
         </Page>
      </section>
   );
}
