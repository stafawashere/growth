import { useRef, type KeyboardEvent, type ReactNode } from "react";

export interface TabItem<T extends string> {
   id: T;
   label: string;
}

const STEP_BY_KEY: Record<string, number | "first" | "last"> = {
   ArrowRight: 1,
   ArrowDown: 1,
   ArrowLeft: -1,
   ArrowUp: -1,
   Home: "first",
   End: "last"
};

function neighbourIndex(current: number, count: number, step: number | "first" | "last") {
   if (step === "first") {
      return 0;
   }

   if (step === "last") {
      return count - 1;
   }

   return (current + step + count) % count;
}

/* A tablist that moves with the arrow keys, Home and End, and selects as it moves, the pattern
   the mockup's installKeyboard gave every tab row. */
export function Tabs<T extends string>(props: {
   items: ReadonlyArray<TabItem<T>>;
   active: T;
   onChange: (id: T) => void;
   label: string;
   idPrefix: string;
}) {
   const buttons = useRef<Array<HTMLButtonElement | null>>([]);

   function moveWith(event: KeyboardEvent<HTMLButtonElement>, index: number) {
      const step = STEP_BY_KEY[event.key];
      const isNavigationKey = step !== undefined;

      if (!isNavigationKey) {
         return;
      }

      event.preventDefault();

      const next = neighbourIndex(index, props.items.length, step);

      buttons.current[next]?.focus();
      props.onChange(props.items[next].id);
   }

   return (
      <div className="tabs" role="tablist" aria-label={props.label}>
         {props.items.map((item, index) => {
            const isSelected = item.id === props.active;

            return (
               <button
                  key={item.id}
                  ref={(element) => {
                     buttons.current[index] = element;
                  }}
                  type="button"
                  className="tab"
                  role="tab"
                  id={`${props.idPrefix}-tab-${item.id}`}
                  aria-selected={isSelected}
                  aria-controls={`${props.idPrefix}-panel`}
                  tabIndex={isSelected ? 0 : -1}
                  onClick={() => props.onChange(item.id)}
                  onKeyDown={(event) => moveWith(event, index)}
               >
                  {item.label}
               </button>
            );
         })}
      </div>
   );
}

export function TabPanel(props: { idPrefix: string; active: string; children: ReactNode }) {
   return (
      <div
         className="tab-panel"
         role="tabpanel"
         id={`${props.idPrefix}-panel`}
         aria-labelledby={`${props.idPrefix}-tab-${props.active}`}
      >
         {props.children}
      </div>
   );
}
