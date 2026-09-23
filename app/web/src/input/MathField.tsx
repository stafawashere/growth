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

export function readMathJsonValue(field: MathFieldElementLike): unknown {
   const raw = field.getValue("math-json");

   return JSON.parse(raw);
}

export interface MathFieldProps {
   label: string;
   initialLatex?: string;
   onChange: (mathjson: unknown) => void;
   onLoadFailure: (reason: unknown) => void;
}

export function MathField(props: MathFieldProps) {
   const { label, initialLatex, onChange, onLoadFailure } = props;
   const handlesLoadFailure = typeof onLoadFailure === "function";

   if (!handlesLoadFailure) {
      throw new Error(
         "MathField needs an onLoadFailure handler: a field whose keyboard never loads takes no answer"
      );
   }

   const fieldId = useId();
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
         onChange(readMathJsonValue(node as unknown as MathFieldElementLike));
      };

      node.addEventListener("input", handleInput);

      return () => {
         node.removeEventListener("input", handleInput);
      };
   }, [onChange, loadFailed]);

   if (loadFailed) {
      return (
         <div>
            <span id={fieldId}>{label}</span>
            <p role="alert">{MATHLIVE_LOAD_FAILURE_MESSAGE}</p>
         </div>
      );
   }

   return (
      <div>
         <label htmlFor={fieldId}>{label}</label>
         <math-field id={fieldId} aria-label={label} ref={elementRef}>
            {initialLatex ?? ""}
         </math-field>
      </div>
   );
}
