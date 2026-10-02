import type { LessonDecision, LessonDelivery } from "../api/types";
import { LessonText } from "./LessonText";
import { isRecord } from "./specGraph";

/* Mode contrast (TEMPLATE.md Delivery; plan 15 Decision lessons): two to four stems on one
   screen, each with the feature that selects its method marked. The mark is a glyph and a word as
   well as a rule beside it, so it reads in greyscale (08 Accessibility). A spec may name each
   stem's own feature (marks [{stem, feature}]); without one, the stem's method is what the
   feature selects, and the decision's selecting feature heads the panel. On the sheet each stem
   is one row, numbered in the margin. */

export const FEATURE_GLYPH = ">";

export const FEATURE_WORD = "Selects:";

export interface ContrastPanelProps {
   decision: LessonDecision;
   delivery?: LessonDelivery;
}

function featureFor(delivery: LessonDelivery | undefined, stemId: string, index: number) {
   const marks = delivery?.spec?.marks;

   if (!Array.isArray(marks)) {
      return null;
   }

   const byId = marks.find((mark) => isRecord(mark) && mark.stem === stemId);
   const entry = byId ?? marks[index];

   if (typeof entry === "string") {
      return entry;
   }

   return isRecord(entry) && typeof entry.feature === "string" ? entry.feature : null;
}

export function ContrastPanel({ decision, delivery }: ContrastPanelProps) {
   const stems = decision.stems.slice(0, 4);

   return (
      <div className="contrast-panel sheet" data-testid="contrast-panel">
         <div className="sheet-row sheet-row-ruled">
            <span className="sheet-margin sheet-tag" aria-hidden="true">
               Recognise
            </span>

            <p className="sheet-body lesson-question">Tell the stems apart by {decision.selecting_feature}</p>
         </div>

         {stems.map((stem, index) => (
            <article key={stem.id} className="sheet-row contrast-stem" data-testid="contrast-stem">
               <span className="sheet-margin sheet-tag" aria-hidden="true">
                  Stem {index + 1}
               </span>

               <div className="sheet-body sheet-body-stack">
                  <p>
                     <LessonText text={stem.text} />
                  </p>

                  <p className="contrast-feature" data-testid="contrast-feature">
                     <span aria-hidden="true">{FEATURE_GLYPH}</span> {FEATURE_WORD} <LessonText text={featureFor(delivery, stem.id, index) ?? stem.method} />
                  </p>

                  <p className="muted">
                     <LessonText text={stem.method} />
                  </p>
               </div>
            </article>
         ))}
      </div>
   );
}
