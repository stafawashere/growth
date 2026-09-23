import { useId } from "react";
import { affordanceProps } from "../affordances";
import { motionClass } from "../styles/motion";
import type { Confidence } from "../api/types";

export const CONFIDENCE_QUESTION = "Before you see the answer: guess, unsure, or confident?";

export const CONFIDENCE_CHOICES: { value: Confidence; label: string }[] = [
   { value: "guess", label: "guess" },
   { value: "unsure", label: "unsure" },
   { value: "confident", label: "confident" }
];

export interface ConfidencePromptProps {
   value: Confidence | null;
   onChange: (confidence: Confidence) => void;
}

export function ConfidencePrompt({ value, onChange }: ConfidencePromptProps) {
   const groupName = useId();

   return (
      <fieldset
         {...affordanceProps("confidencePrompt")}
         className={motionClass("confidencePrompt")}
         data-testid="confidence-prompt"
      >
         <legend>{CONFIDENCE_QUESTION}</legend>

         {CONFIDENCE_CHOICES.map((choice) => {
            const isChosen = value === choice.value;

            return (
               <label key={choice.value}>
                  <input
                     type="radio"
                     name={groupName}
                     value={choice.value}
                     checked={isChosen}
                     aria-label={choice.label}
                     onChange={() => onChange(choice.value)}
                  />
                  {choice.label}
               </label>
            );
         })}
      </fieldset>
   );
}