import { useId } from "react";
import type { ServedOption } from "../api/types";
import { MathText } from "../math/MathText";
import { MathValue } from "../math/MathValue";
import { Icon } from "../ui/Icon";

export interface McqControlProps {
   groupLabel: string;
   options: ServedOption[];
   selectedId?: string | null;
   onSelect: (optionId: string) => void;
   eliminatedIds?: ReadonlyArray<string>;
   onToggleEliminated?: (optionId: string) => void;
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

const OPTION_LETTERS = ["A", "B", "C", "D", "E"];

export function McqControl(props: McqControlProps) {
   const { groupLabel, options, selectedId, onSelect, eliminatedIds, onToggleEliminated } = props;
   const groupName = useId();
   const offersEliminator = onToggleEliminated !== undefined;

   return (
      <fieldset className="option-list">
         <legend className="field-label">{groupLabel}</legend>

         {options.map((option, index) => {
            const isSelected = selectedId === option.id;
            const hasLabel = option.label !== undefined;
            const mathSource = optionMathSource(option);
            const letter = OPTION_LETTERS[index] ?? option.id;

            const isEliminated = eliminatedIds?.includes(option.id) ?? false;
            const optionText = hasLabel ? <MathText text={option.label!} /> : <MathValue value={mathSource ?? option.id} className="option-math" />;

            const choice = (
               <label key={option.id} className="option" data-selected={isSelected ? "true" : undefined}>
                  <input
                     type="radio"
                     name={groupName}
                     value={option.id}
                     checked={isSelected}
                     onChange={() => onSelect(option.id)}
                  />

                  <span className="option-letter" data-letter={letter} aria-hidden="true" />

                  <span className={isEliminated ? "option-content crossed-out" : "option-content"}>{optionText}</span>
               </label>
            );

            if (!offersEliminator) {
               return choice;
            }

            return (
               <div key={option.id} className="option-row" data-testid="choice-option" data-eliminated={isEliminated}>
                  {choice}

                  <button
                     type="button"
                     className="icon-button icon-button-small motion-instant-eliminate-option"
                     aria-pressed={isEliminated}
                     aria-label={isEliminated ? `Restore option ${option.id}` : `Cross out option ${option.id}`}
                     title={isEliminated ? `Restore option ${option.id}` : `Cross out option ${option.id}`}
                     onClick={() => onToggleEliminated(option.id)}
                  >
                     <Icon name={isEliminated ? "refresh" : "close"} />
                  </button>
               </div>
            );
         })}
      </fieldset>
   );
}
