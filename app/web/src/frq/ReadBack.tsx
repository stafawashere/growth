import type { ReadBack, ReadBackLine, ReadBackPart } from "../api/types";
import { MathText } from "../math/MathText";

/* 08 "Mock exam, FRQ booklet and photo read-back": what the app read, rendered as mathematics,
   which the student confirms or corrects before any point is graded. Crossed-out lines are shown
   struck through, because the booklet does not score crossed-out work. */

export function lineText(line: ReadBackLine) {
   const isMath = line.kind === "math";

   return isMath ? `\\(${line.content}\\)` : line.content;
}

function PartView({ part }: { part: ReadBackPart }) {
   const hasLines = part.lines.length > 0;
   const hasAnswer = part.answer.trim() !== "";

   return (
      <li data-testid="read-back-part">
         <strong>({part.part_id})</strong>

         {hasLines ? null : <p className="muted">Nothing was read in this box.</p>}

         <ul className="read-back-lines">
            {part.lines.map((line, index) => (
               <li key={index} className={line.crossed_out ? "crossed-out" : undefined}>
                  {line.crossed_out ? <span className="visually-hidden">crossed out: </span> : null}
                  <MathText text={lineText(line)} />
               </li>
            ))}
         </ul>

         {hasAnswer ? (
            <p>
               Answer: <MathText text={`\\(${part.answer}\\)`} />
            </p>
         ) : null}
      </li>
   );
}

export function ReadBackView({ readBack }: { readBack: ReadBack }) {
   const hasUnreadable = readBack.unreadable.length > 0;

   return (
      <section aria-labelledby="read-back-heading">
         <h2 id="read-back-heading" className="section-heading">
            What I read
         </h2>

         <ol className="read-back">
            {readBack.parts.map((part) => (
               <PartView key={part.part_id} part={part} />
            ))}
         </ol>

         {hasUnreadable ? (
            <div data-testid="unreadable">
               <p>Places I was not sure of:</p>
               <ul>
                  {readBack.unreadable.map((note, index) => (
                     <li key={index}>{note}</li>
                  ))}
               </ul>
            </div>
         ) : null}
      </section>
   );
}

export interface ReadBackEditorProps {
   readBack: ReadBack;
   onChange: (readBack: ReadBack) => void;
}

const EMPTY_LINE: ReadBackLine = { kind: "math", content: "", crossed_out: false, outside_box: false };

export function editedPart(part: ReadBackPart, index: number, changed: Partial<ReadBackLine>): ReadBackPart {
   const lines = part.lines.map((line, position) => (position === index ? { ...line, ...changed } : line));

   return { ...part, lines };
}

/* Each line is edited as LaTeX, with the rendered line beside it so the student can see what
   will be graded. A line can be added, switched between mathematics and words, or marked as
   crossed out. */
export function ReadBackEditor({ readBack, onChange }: ReadBackEditorProps) {
   function replacePart(partIndex: number, part: ReadBackPart) {
      const parts = readBack.parts.map((current, position) => (position === partIndex ? part : current));

      onChange({ ...readBack, parts });
   }

   return (
      <section aria-labelledby="read-back-editor-heading">
         <h2 id="read-back-editor-heading" className="section-heading">
            Fix what I read
         </h2>

         {readBack.parts.map((part, partIndex) => (
            <fieldset key={part.part_id} data-testid="edit-part">
               <legend>Part ({part.part_id})</legend>

               {part.lines.map((line, lineIndex) => (
                  <div key={lineIndex} className="field read-back-edit-line">
                     <label>
                        Line {lineIndex + 1}
                        <input
                           type="text"
                           value={line.content}
                           onChange={(event) =>
                              replacePart(partIndex, editedPart(part, lineIndex, { content: event.target.value }))
                           }
                        />
                     </label>

                     <label>
                        <input
                           type="checkbox"
                           checked={line.kind === "text"}
                           onChange={(event) =>
                              replacePart(partIndex, editedPart(part, lineIndex, { kind: event.target.checked ? "text" : "math" }))
                           }
                        />
                        words, not mathematics
                     </label>

                     <label>
                        <input
                           type="checkbox"
                           checked={line.crossed_out}
                           onChange={(event) =>
                              replacePart(partIndex, editedPart(part, lineIndex, { crossed_out: event.target.checked }))
                           }
                        />
                        crossed out
                     </label>

                     <span className="muted" aria-hidden="true">
                        <MathText text={lineText(line)} />
                     </span>
                  </div>
               ))}

               <button
                  type="button"
                  className="text-button"
                  onClick={() => replacePart(partIndex, { ...part, lines: [...part.lines, { ...EMPTY_LINE }] })}
               >
                  Add a line to part ({part.part_id})
               </button>

               <label className="field">
                  Answer to part ({part.part_id})
                  <input
                     type="text"
                     value={part.answer}
                     onChange={(event) => replacePart(partIndex, { ...part, answer: event.target.value })}
                  />
               </label>
            </fieldset>
         ))}
      </section>
   );
}

export function emptyReadBack(partIds: ReadonlyArray<string>): ReadBack {
   return {
      parts: partIds.map((partId) => ({ part_id: partId, lines: [{ ...EMPTY_LINE }], answer: "" })),
      unreadable: []
   };
}
