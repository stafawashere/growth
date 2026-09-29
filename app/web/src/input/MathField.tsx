import type { DetailedHTMLProps, HTMLAttributes } from "react";
import { useEffect, useId, useRef, useState } from "react";

declare global {
   namespace JSX {
      interface IntrinsicElements {
         "math-field": DetailedHTMLProps<HTMLAttributes<HTMLElement>, HTMLElement>;
      }
   }
}

export const MATHLIVE_LOAD_FAILURE_MESSAGE =
   "The math keyboard did not load, so this field cannot take an answer.";

export interface MathFieldElementLike {
   getValue(format: string): string;
}

/* MathLive speaks the field's content as spoken text (its "spoken-text" output), and that reading
   is carried as the field's description, so a screen reader landing on the field hears what is in
   it as mathematics rather than as the LaTeX keystrokes. An element MathLive has not upgraded has
   no reading to give. */
export function readSpokenText(field: MathFieldElementLike): string {
   try {
      return field.getValue("spoken-text");
   } catch {
      return "";
   }
}

export function readMathJsonValue(field: MathFieldElementLike): unknown {
   const raw = field.getValue("math-json");

   return JSON.parse(raw);
}

export interface MathFieldProps {
   label: string;
   initialLatex?: string;
   onChange: (mathjson: unknown) => void;
   onLoadFailure: (reason: unknown) => void;
   onLatexChange?: (latex: string) => void;
}

export function MathField(props: MathFieldProps) {
   const { label, initialLatex, onChange, onLoadFailure, onLatexChange } = props;
   const handlesLoadFailure = typeof onLoadFailure === "function";

   if (!handlesLoadFailure) {
      throw new Error(
         "MathField needs an onLoadFailure handler: a field whose keyboard never loads takes no answer"
      );
   }

   const fieldId = useId();
   const speechId = useId();
   const [spoken, setSpoken] = useState("");
   const elementRef = useRef<HTMLElement | null>(null);
   const failureHandler = useRef(onLoadFailure);
   const [loadFailed, setLoadFailed] = useState(false);

   useEffect(() => {
      failureHandler.current = onLoadFailure;
   }, [onLoadFailure]);

   useEffect(() => {
      let isMounted = true;

      import("mathlive").catch((reason) => {
         if (!isMounted) {
            return;
         }

         setLoadFailed(true);
         failureHandler.current(reason);
      });

      return () => {
         isMounted = false;
      };
   }, []);

   useEffect(() => {
      const node = elementRef.current;

      if (node === null) {
         return undefined;
      }

      const handleInput = () => {
         const field = node as unknown as MathFieldElementLike;
         const wantsLatex = onLatexChange !== undefined;

         if (wantsLatex) {
            onLatexChange(field.getValue("latex"));
         }

         setSpoken(readSpokenText(field));
         onChange(readMathJsonValue(field));
      };

      node.addEventListener("input", handleInput);

      return () => {
         node.removeEventListener("input", handleInput);
      };
   }, [onChange, onLatexChange, loadFailed]);

   if (loadFailed) {
      return (
         <div className="form-field">
            <span id={fieldId}>{label}</span>
            <p role="alert">{MATHLIVE_LOAD_FAILURE_MESSAGE}</p>
         </div>
      );
   }

   return (
      <div className="form-field">
         <label className="field-label" htmlFor={fieldId}>
            {label}
         </label>
         <math-field id={fieldId} aria-label={label} aria-describedby={speechId} ref={elementRef}>
            {initialLatex ?? ""}
         </math-field>
         <span id={speechId} className="visually-hidden" data-testid="math-field-speech">
            {spoken}
         </span>
      </div>
   );
}
