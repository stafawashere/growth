import { forwardRef } from "react";

import type { CalculatorDrillRequestCapability } from "../api/types";
import { Icon } from "../ui/Icon";
import { CAPABILITY_NAMES, CAPABILITY_ORDER, CHOOSER_LABEL, answeredText } from "./words";

/* The top of the Drill section (docs/calculator/design.md, The drills): the six drilled
   capabilities and Mixed, each with how many drills of it were answered, "12 answered" or "none
   yet". Counts are left off while the measured record has not arrived rather than shown as zero. */

export type AnsweredCounts = Partial<Record<CalculatorDrillRequestCapability, number>>;

const CHOICES: ReadonlyArray<CalculatorDrillRequestCapability> = [...CAPABILITY_ORDER, "mixed"];

export interface CapabilityChooserProps {
   chosen: CalculatorDrillRequestCapability | null;
   counts: AnsweredCounts | null;
   onChoose: (capability: CalculatorDrillRequestCapability) => void;
}

export const CapabilityChooser = forwardRef<HTMLDivElement, CapabilityChooserProps>(function CapabilityChooser(props, ref) {
   return (
      <div className="capability-chooser" role="group" aria-label={CHOOSER_LABEL} data-testid="capability-chooser" ref={ref} tabIndex={-1}>
         {CHOICES.map((capability) => {
            const isChosen = props.chosen === capability;
            const count = props.counts?.[capability];
            const hasCount = count !== undefined;

            return (
               <button
                  key={capability}
                  type="button"
                  className="button-secondary capability-choice"
                  aria-pressed={isChosen}
                  data-capability={capability}
                  onClick={() => props.onChoose(capability)}
               >
                  {isChosen ? <Icon name="check" /> : null}
                  <span>{CAPABILITY_NAMES[capability]}</span>
                  {hasCount ? <span className="helper">{answeredText(count)}</span> : null}
               </button>
            );
         })}
      </div>
   );
});
