import { LessonText } from "./LessonText";

/* TEMPLATE.md Delivery: every drawn mode carries the static form served when the mode cannot
   render, so a block that cannot be drawn shows that text in the figure's own frame and is never
   blank. A spec that reached the reader without its fallback still says so in words. */
export const MISSING_FALLBACK = "This part is drawn in the lesson, and the drawing could not be made here.";

export function LessonFallback(props: { text?: string }) {
   const text = props.text !== undefined && props.text.trim() !== "" ? props.text : MISSING_FALLBACK;

   return (
      <figure className="lesson-figure lesson-fallback" data-testid="lesson-figure-fallback">
         <p>
            <LessonText text={text} />
         </p>
      </figure>
   );
}
