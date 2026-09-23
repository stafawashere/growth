import { useId } from "react";
import { affordanceProps } from "../affordances";
import { motionClass } from "../styles/motion";

export const ERROR_NOTE_LABEL = "In one line, what went wrong?";

/* BUILD-LEDGER.md, "Decisions taken on the operator's instruction, 2026-09-20": the error note is
   capped at 500 characters. app/session/service.py ERROR_NOTE_MAX_CHARACTERS enforces the same
   number server-side. */
export const ERROR_NOTE_MAX_CHARACTERS = 500;

export interface ErrorNoteFieldProps {
   value: string;
   onChange: (note: string) => void;
}

export function ErrorNoteField({ value, onChange }: ErrorNoteFieldProps) {
   const fieldId = useId();

   return (
      <section
         {...affordanceProps("errorNoteField")}
         className={`${motionClass("errorNoteField")} field`}
         data-testid="error-note-field"
      >
         <label htmlFor={fieldId}>{ERROR_NOTE_LABEL}</label>

         <input
            id={fieldId}
            type="text"
            value={value}
            maxLength={ERROR_NOTE_MAX_CHARACTERS}
            onChange={(event) => onChange(event.target.value)}
         />
      </section>
   );
}