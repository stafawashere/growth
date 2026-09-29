import { useId } from "react";
import { affordanceProps } from "../affordances";
import { motionClass } from "../styles/motion";

export interface SelfExplanationPromptProps {
   prompt: string | null;
   value: string;
   onChange: (text: string) => void;
}

export function SelfExplanationPrompt({ prompt, value, onChange }: SelfExplanationPromptProps) {
   const fieldId = useId();
   const hasPrompt = prompt !== null && prompt.trim().length > 0;

   if (!hasPrompt) {
      return null;
   }

   return (
      <section
         {...affordanceProps("selfExplanationPrompt")}
         className={`${motionClass("selfExplanationPrompt")} form-field`}
         data-testid="self-explanation-prompt"
      >
         <label className="field-label" htmlFor={fieldId}>
            {prompt}
         </label>

         <textarea id={fieldId} className="input" value={value} onChange={(event) => onChange(event.target.value)} />
      </section>
   );
}