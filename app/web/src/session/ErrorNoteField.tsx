import { useId } from "react";
import { affordanceProps } from "../affordances";
import { motionClass } from "../styles/motion";

export const ERROR_NOTE_LABEL = "In one line, what went wrong?";

export interface ErrorNoteFieldProps {
   value: string;
   onChange: (note: string) => void;
}

export function ErrorNoteField({ value, onChange }: ErrorNoteFieldProps) {
   const fieldId = useId();

   return (
      <section
         {...affordanceProps("errorNoteField")}
         className={motionClass("errorNoteField")}
         data-testid="error-note-field"
      >
         <label htmlFor={fieldId}>{ERROR_NOTE_LABEL}</label>

         <input id={fieldId} type="text" value={value} onChange={(event) => onChange(event.target.value)} />
      </section>
   );
}