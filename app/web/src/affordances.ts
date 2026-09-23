/* The five P1 feedback affordances, as docs/plan/11-phased-delivery.md gate 25 lists them.
   Every component that renders one sets data-affordance to its value here, and gate 25 ranges
   over this object rather than over a hand-copied list. An affordance added by a later phase is
   added here and the gate picks it up. */

export const P1_FEEDBACK_AFFORDANCES = {
   stepVerificationMark: "step-verification-mark",
   elaboratedFeedbackPanel: "elaborated-feedback-panel",
   confidencePrompt: "confidence-prompt",
   selfExplanationPrompt: "self-explanation-prompt",
   errorNoteField: "error-note-field"
} as const;

export type AffordanceName = keyof typeof P1_FEEDBACK_AFFORDANCES;

export const AFFORDANCE_ATTRIBUTE = "data-affordance";

export function affordanceProps(name: AffordanceName) {
   return { [AFFORDANCE_ATTRIBUTE]: P1_FEEDBACK_AFFORDANCES[name] };
}
