import { useId } from "react";
import type { ServedOption } from "../api/types";
import { MathText } from "../math/MathText";
import { MathValue } from "../math/MathValue";

export interface McqControlProps {
   groupLabel: string;
   options: ServedOption[];
   selectedId?: string | null;
   onSelect: (optionId: string) => void;
}

/* An option carries a human label when one was authored, and otherwise a MathJSON value: a bare
   number or symbol, or an expression tree such as ["Add", ["Multiply", -5, ["Sin", "x"]]]
   (app/runtime/bank.py STUDENT_OPTION_FIELDS). A label may carry inline LaTeX between \( and \),
   so it goes through MathText. The math branch always goes through MathValue, even for a bare
   number, so every option is typeset consistently. */
function optionMathSource(option: ServedOption) {
   if (option.mathjson !== undefined) {
      return option.mathjson;
   }

   return option.value;
}

export function McqControl(props: McqControlProps) {
   const { groupLabel, options, selectedId, onSelect } = props;
   const groupName = useId();

   return (
      <fieldset className="choice-group">
         <legend>{groupLabel}</legend>
         {options.map((option) => {
            const isSelected = selectedId === option.id;
            const hasLabel = option.label !== undefined;
            const mathSource = optionMathSource(option);

            return (
               <label key={option.id}>
                  <input
                     type="radio"
                     name={groupName}
                     value={option.id}
                     checked={isSelected}
                     onChange={() => onSelect(option.id)}
                  />
                  {hasLabel ? <MathText text={option.label!} /> : <MathValue value={mathSource ?? option.id} className="option-math" />}
               </label>
            );
         })}
      </fieldset>
   );
}
