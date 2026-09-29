import type { LessonDecision, LessonDelivery } from "../api/types";
import { MathText } from "../math/MathText";
import { isRecord } from "./specGraph";

/* Mode contrast (TEMPLATE.md Delivery; plan 15 Decision lessons): two to four stems side by side
   on one screen, each with the feature that selects its method marked. The mark is a glyph and a
   word as well as a rule beside it, so it reads in greyscale (08 Accessibility). A spec may name
   each stem's own feature (marks [{stem, feature}]); without one, the stem's method is what the
   feature selects, and the decision's selecting feature heads the panel. */

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
      <div className="contrast-panel" data-testid="contrast-panel">
         <p className="eyebrow">Tell the stems apart by {decision.selecting_feature}</p>

         <div className="contrast-grid">
            {stems.map((stem, index) => (
               <article key={stem.id} className="contrast-stem" data-testid="contrast-stem">
                  <p>
                     <MathText text={stem.text} />
                  </p>

                  <p className="contrast-feature" data-testid="contrast-feature">
                     <span aria-hidden="true">{FEATURE_GLYPH}</span> {FEATURE_WORD} <MathText text={featureFor(delivery, stem.id, index) ?? stem.method} />
                  </p>

                  <p className="muted">
                     <MathText text={stem.method} />
                  </p>
               </article>
            ))}
         </div>
      </div>
   );
}
