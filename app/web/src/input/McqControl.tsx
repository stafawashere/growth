import { useId } from "react";
import type { ServedOption } from "../api/types";

export interface McqControlProps {
   groupLabel: string;
   options: ServedOption[];
   selectedId?: string | null;
   onSelect: (optionId: string) => void;
}

export function McqControl(props: McqControlProps) {
   const { groupLabel, options, selectedId, onSelect } = props;
   const groupName = useId();

   return (
      <fieldset className="choice-group">
         <legend>{groupLabel}</legend>
         {options.map((option) => {
            const optionText = option.label ?? option.value ?? option.id;
            const isSelected = selectedId === option.id;

            return (
               <label key={option.id}>
                  <input
                     type="radio"
                     name={groupName}
                     value={option.id}
                     checked={isSelected}
                     onChange={() => onSelect(option.id)}
                  />
                  {optionText}
               </label>
            );
         })}
      </fieldset>
   );
}
