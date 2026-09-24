import { useState } from "react";

import type { Confidence, ReadBack, ReadBackLine } from "../api/types";
import { MathField } from "../input/MathField";
import { ConfidencePrompt } from "../session/ConfidencePrompt";

/* 11 P3 scope item 9: typed MathLive entry as the secondary free-response mode. Each part is a list
   of lines; a mathematics line is a MathLive field whose LaTeX becomes the line, a words line is a
   plain field. If the math keyboard does not load, the line falls back to a LaTeX text field so an
   answer can still be written. */

export interface TypedEntryProps {
   initial: ReadBack;
   confidence: Confidence | null;
   onConfidence: (confidence: Confidence) => void;
   onSubmit: (typed: ReadBack) => void;
}

function LineInput(props: { label: string; line: ReadBackLine; onChange: (line: ReadBackLine) => void }) {
   const { label, line, onChange } = props;
   const [keyboardFailed, setKeyboardFailed] = useState(false);
   const usesMathField = line.kind === "math" && !keyboardFailed;

   if (usesMathField) {
      return (
         <MathField
            label={label}
            initialLatex={line.content}
            onChange={() => undefined}
            onLatexChange={(latex) => onChange({ ...line, content: latex })}
            onLoadFailure={() => setKeyboardFailed(true)}
         />
      );
   }

   return (
      <label className="field">
         {label}
         <input type="text" value={line.content} onChange={(event) => onChange({ ...line, content: event.target.value })} />
      </label>
   );
}

export function TypedEntry({ initial, confidence, onConfidence, onSubmit }: TypedEntryProps) {
   const [typed, setTyped] = useState<ReadBack>(initial);

   function setLine(partIndex: number, lineIndex: number, line: ReadBackLine) {
      const parts = typed.parts.map((part, position) => {
         if (position !== partIndex) {
            return part;
         }

         return { ...part, lines: part.lines.map((current, index) => (index === lineIndex ? line : current)) };
      });

      setTyped({ ...typed, parts });
   }

   function addLine(partIndex: number, kind: ReadBackLine["kind"]) {
      const parts = typed.parts.map((part, position) =>
         position === partIndex
            ? { ...part, lines: [...part.lines, { kind, content: "", crossed_out: false, outside_box: false }] }
            : part
      );

      setTyped({ ...typed, parts });
   }

   return (
      <section aria-labelledby="typed-heading">
         <h2 id="typed-heading" className="section-heading">
            Type your answer
         </h2>

         {typed.parts.map((part, partIndex) => (
            <fieldset key={part.part_id} data-testid="typed-part">
               <legend>Part ({part.part_id})</legend>

               {part.lines.map((line, lineIndex) => (
                  <LineInput
                     key={lineIndex}
                     label={`Part (${part.part_id}), line ${lineIndex + 1}${line.kind === "text" ? ", words" : ""}`}
                     line={line}
                     onChange={(changed) => setLine(partIndex, lineIndex, changed)}
                  />
               ))}

               <div className="choice-row">
                  <button type="button" className="text-button" onClick={() => addLine(partIndex, "math")}>
                     Add a mathematics line
                  </button>
                  <button type="button" className="text-button" onClick={() => addLine(partIndex, "text")}>
                     Add a line of words
                  </button>
               </div>
            </fieldset>
         ))}

         <ConfidencePrompt value={confidence} onChange={onConfidence} />

         <button type="button" className="button-primary" disabled={confidence === null} onClick={() => onSubmit(typed)}>
            Grade my answer
         </button>
      </section>
   );
}
