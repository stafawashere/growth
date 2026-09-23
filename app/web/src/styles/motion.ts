import { P1_FEEDBACK_AFFORDANCES, type AffordanceName } from "../affordances";

/* docs/plan/08-design-brief.md's Motion rules section gives exactly one number, "under roughly
   300 ms", and records that Material 3's numeric duration and easing tokens could not be loaded.
   So the stylesheet has one duration and one easing, both named here, and a second duration or a
   cubic-bezier curve would be invented rather than sourced. */

export const MOTION_DURATION = "300ms";

export const MOTION_EASING = "ease-out";

export const REDUCED_MOTION_QUERY = "(prefers-reduced-motion: reduce)";

export const ANIMATABLE_PROPERTIES = ["transform", "opacity"] as const;

export const MOTION_CLASS_PREFIX = "motion-";

export function motionClass(name: AffordanceName) {
   return MOTION_CLASS_PREFIX + P1_FEEDBACK_AFFORDANCES[name];
}

export const TRANSFORM_MOTION_CLASSES = Object.values(P1_FEEDBACK_AFFORDANCES).map(
   (affordance) => MOTION_CLASS_PREFIX + affordance
);

/* 08 names six paths reached by a repeated keystroke and says all of them are instant. */

export const INSTANT_CLASSES = [
   "motion-instant-symbol-insertion",
   "motion-instant-blank-move",
   "motion-instant-question-move",
   "motion-instant-mark-for-review",
   "motion-instant-eliminate-option",
   "motion-instant-submit-answer"
];

export const MOTION_CLASSES = [...TRANSFORM_MOTION_CLASSES, ...INSTANT_CLASSES];
