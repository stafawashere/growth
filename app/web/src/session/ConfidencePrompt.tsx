import { useEffect, useId, useRef, useState, type KeyboardEvent } from "react";
import { affordanceProps } from "../affordances";
import { motionClass } from "../styles/motion";
import type { Confidence } from "../api/types";
import { Icon, type IconName } from "../ui/Icon";

export const CONFIDENCE_QUESTION = "Before you see the answer: guess, unsure, or confident?";

export const CONFIDENCE_EYEBROW = "How sure am I?";

export const CONFIDENCE_CLOSE_LABEL = "Close";

export const CONFIDENCE_CHOICES: { value: Confidence; label: string }[] = [
   { value: "guess", label: "guess" },
   { value: "unsure", label: "unsure" },
   { value: "confident", label: "confident" }
];

/* What each word means in the student's voice, and the face drawn at the end of its row. */
const CHOICE_MEANINGS: Record<Confidence, { meaning: string; face: IconName }> = {
   guess: { meaning: "I could not say why.", face: "faceGuess" },
   unsure: { meaning: "I have a reason, and I would not bet on it.", face: "faceUnsure" },
   confident: { meaning: "I can say why, and I would stand by it.", face: "faceConfident" }
};

const CHOICE_KEYS = ["1", "2", "3"];

const ARROW_FORWARD = ["ArrowDown", "ArrowRight"];

const ARROW_BACK = ["ArrowUp", "ArrowLeft"];

export interface ConfidencePromptProps {
   value: Confidence | null;
   onChange: (confidence: Confidence) => void;
   onClose?: () => void;
}

function radiosOf(dialog: HTMLElement) {
   return Array.from(dialog.querySelectorAll<HTMLInputElement>("input[type='radio']"));
}

/* The rating is asked in a modal at the moment the student moves on, before the answer is shown
   or the step advances. Choosing one of the three words completes the action that opened it. The
   way out is Escape or the close button, which sends nothing and hands focus back to the control
   that opened the dialog. Within it, Tab cycles between the choices and the close button, the
   arrows move between the three words without choosing, and Space, a click or the word's digit
   chooses. Under 600 px it rises from the bottom of the screen as a sheet. */
export function ConfidencePrompt({ value, onChange, onClose }: ConfidencePromptProps) {
   const groupName = useId();
   const titleId = useId();
   const dialogRef = useRef<HTMLElement | null>(null);
   const [isEntering, setIsEntering] = useState(true);
   const offersClose = onClose !== undefined;

   useEffect(() => {
      const opener = document.activeElement as HTMLElement | null;
      const dialog = dialogRef.current;

      if (dialog !== null) {
         const radios = radiosOf(dialog);
         const chosen = radios.find((radio) => radio.checked) ?? radios[0];

         chosen?.focus();
      }

      const frame = requestAnimationFrame(() => setIsEntering(false));

      return () => {
         cancelAnimationFrame(frame);
         opener?.focus?.();
      };
   }, []);

   function tabStops(dialog: HTMLElement) {
      const radios = radiosOf(dialog);
      const radioStop = radios.find((radio) => radio.checked) ?? radios[0];
      const buttons = Array.from(dialog.querySelectorAll<HTMLElement>("button:not(:disabled)"));

      return [radioStop, ...buttons].filter((stop): stop is HTMLElement => stop !== undefined);
   }

   function onKeyDown(event: KeyboardEvent<HTMLElement>) {
      const dialog = dialogRef.current;
      const hasModifier = event.altKey || event.ctrlKey || event.metaKey;

      if (dialog === null || hasModifier) {
         return;
      }

      const isEscape = event.key === "Escape";

      if (isEscape && offersClose) {
         event.preventDefault();
         event.stopPropagation();
         onClose();

         return;
      }

      const choiceIndex = CHOICE_KEYS.indexOf(event.key);
      const picksByKey = choiceIndex >= 0;

      if (picksByKey) {
         event.preventDefault();
         event.stopPropagation();
         onChange(CONFIDENCE_CHOICES[choiceIndex].value);

         return;
      }

      const isTab = event.key === "Tab";

      if (isTab) {
         const stops = tabStops(dialog);
         const active = document.activeElement as HTMLElement;
         const current = stops.indexOf(active);
         const isRadio = active instanceof HTMLInputElement && active.type === "radio";
         const position = current === -1 && isRadio ? 0 : current;
         const step = event.shiftKey ? -1 : 1;
         const next = stops[(position + step + stops.length) % stops.length];

         event.preventDefault();
         next?.focus();

         return;
      }

      const movesForward = ARROW_FORWARD.includes(event.key);
      const movesBack = ARROW_BACK.includes(event.key);
      const target = event.target as HTMLElement;
      const isOnRadio = target instanceof HTMLInputElement && target.type === "radio";
      const movesBetweenWords = (movesForward || movesBack) && isOnRadio;

      if (movesBetweenWords) {
         const radios = radiosOf(dialog);
         const step = movesForward ? 1 : -1;
         const next = radios[(radios.indexOf(target as HTMLInputElement) + step + radios.length) % radios.length];

         event.preventDefault();
         next?.focus();
      }
   }

   return (
      <div className="confidence-scrim">
         <section
            {...affordanceProps("confidencePrompt")}
            ref={dialogRef}
            role="dialog"
            aria-modal="true"
            aria-labelledby={titleId}
            className={`${motionClass("confidencePrompt")} confidence`}
            data-testid="confidence-prompt"
            data-entering={isEntering ? "true" : undefined}
            onKeyDown={onKeyDown}
         >
            <header className="confidence-head">
               <div className="confidence-title">
                  <p className="eyebrow">{CONFIDENCE_EYEBROW}</p>

                  <h2 id={titleId} className="field-label confidence-question">
                     {CONFIDENCE_QUESTION}
                  </h2>
               </div>

               {offersClose ? (
                  <button type="button" className="icon-button icon-button-small" aria-label={CONFIDENCE_CLOSE_LABEL} onClick={onClose}>
                     <Icon name="close" />
                  </button>
               ) : null}
            </header>

            <div className="choice-group" role="radiogroup" aria-labelledby={titleId}>
               {CONFIDENCE_CHOICES.map((choice, index) => {
                  const isChosen = value === choice.value;
                  const detail = CHOICE_MEANINGS[choice.value];

                  return (
                     <label key={choice.value} className="choice-chip" data-confidence={choice.value} data-chosen={isChosen ? "true" : undefined}>
                        <input
                           type="radio"
                           name={groupName}
                           value={choice.value}
                           checked={isChosen}
                           aria-label={choice.label}
                           onChange={() => onChange(choice.value)}
                        />

                        <kbd className="choice-key" aria-hidden="true">
                           {CHOICE_KEYS[index]}
                        </kbd>

                        <span className="choice-text">
                           <span className="choice-word">{choice.label}</span>
                           <span className="choice-meaning">{detail.meaning}</span>
                        </span>

                        <span className="choice-face" aria-hidden="true">
                           <Icon name={detail.face} size="lg" />
                        </span>
                     </label>
                  );
               })}
            </div>
         </section>
      </div>
   );
}