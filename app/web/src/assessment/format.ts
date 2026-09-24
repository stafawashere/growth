import { ApiError } from "../api/client";
import type { AssessmentPart } from "../api/types";

export const FIVE_MINUTE_ANNOUNCEMENT = "Five minutes remain in this part.";

/* The part header in the wording of 08's two mock wireframes: "Section I Part B {count} questions". */
export function partHeading(part: Pick<AssessmentPart, "section" | "part" | "question_count">) {
   return `Section ${part.section} Part ${part.part}, ${part.question_count} questions`;
}

/* Minutes and seconds, as the exam timer reads. No part runs long enough to need hours. */
export function clockText(milliseconds: number) {
   const totalSeconds = Math.max(0, Math.ceil(milliseconds / 1000));
   const minutes = Math.floor(totalSeconds / 60);
   const seconds = String(totalSeconds % 60).padStart(2, "0");

   return `${minutes}:${seconds}`;
}

/* The server's closed_part_note and break_note carry a {label} slot for the part's own label. */
export function withLabel(template: string, label: string) {
   return template.split("{label}").join(label);
}

export function refusalText(failure: unknown, fallback: string) {
   const hasDetail = failure instanceof ApiError && failure.detail !== "";

   return hasDetail ? failure.detail : fallback;
}
