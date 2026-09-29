import type { DetailedHTMLProps, HTMLAttributes, MutableRefObject } from "react";
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

/* MathLive writes an empty field as the symbol Nothing, and a stand-in may write nothing at all. */
export function isEmptyMathJson(value: unknown) {
   const isAbsent = value === null || value === undefined || value === "";
   const isNothingSymbol = value === "Nothing";
   const isEmptyList = Array.isArray(value) && value.length === 0;
   const isNothingList = Array.isArray(value) && value.length === 1 && value[0] === "Nothing";

   return isAbsent || isNothingSymbol || isEmptyList || isNothingList;
}

export const UNREAD_FIELD = Symbol("unread field");

/* The field's value as it stands now, read from the element rather than from the last input event,
   so a check pressed straight after typing sends what is in the field. An element MathLive has not
   upgraded has nothing to read. */
export function readFieldNow(node: HTMLElement): unknown {
   const field = node as unknown as Partial<MathFieldElementLike>;
   const isUpgraded = typeof field.getValue === "function";

   if (!isUpgraded) {
      return UNREAD_FIELD;
   }

   try {
      return readMathJsonValue(field as MathFieldElementLike);
   } catch {
      return null;
   }
}

export type MathFieldReader = () => unknown;

export interface MathFieldProps {
   label: string;
   initialLatex?: string;
   onChange: (mathjson: unknown) => void;
   onLoadFailure: (reason: unknown) => void;
   onLatexChange?: (latex: string) => void;
   readerRef?: MutableRefObject<MathFieldReader | null>;
   onReady?: () => void;
}

export function MathField(props: MathFieldProps) {
   const { label, initialLatex, onChange, onLoadFailure, onLatexChange, readerRef, onReady } = props;
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
   const readyHandler = useRef(onReady);
   const [loadFailed, setLoadFailed] = useState(false);

   useEffect(() => {
      failureHandler.current = onLoadFailure;
      readyHandler.current = onReady;
   }, [onLoadFailure, onReady]);

   useEffect(() => {
      let isMounted = true;

      import("mathlive")
         .then(() => customElements.whenDefined("math-field"))
         .then(() => {
            if (isMounted) {
               readyHandler.current?.();
            }
         })
         .catch((reason) => {
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

      if (readerRef !== undefined) {
         readerRef.current = () => readFieldNow(node);
      }

      return () => {
         node.removeEventListener("input", handleInput);

         if (readerRef !== undefined) {
            readerRef.current = null;
         }
      };
   }, [onChange, onLatexChange, loadFailed, readerRef]);

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
