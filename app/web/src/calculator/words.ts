import type { CalculatorCapability, CalculatorDrillRequestCapability, CalculatorSetupVerdict, CalculatorValueVerdict } from "../api/types";

/* Every string the student reads in the calculator destination, listed once so the screens and
   their tests read the same words (docs/calculator/design.md, Words). None of them grades the
   student, promises anything about the exam, or sets a goal. */

export const CALCULATOR_EYEBROW = "Calculator";

export const CALCULATOR_PRACTICE = "Calculator practice";

export const CALCULATOR_LINK_SHORT = "Calculator";

export const SECTION_PROCEDURES = "Procedures";

export const SECTION_DRILL = "Drill";

export const SECTION_MEASURED = "Measured";

export const RESULT_LABEL = "Result, to three decimal places";

export const SETUP_LABEL = "Setup, as you would write it on the page";

export const CHECK_LABEL = "Check";

export const NEXT_LABEL = "Next";

export const CHANGE_CAPABILITY_LABEL = "Change capability";

export const DRILL_THIS_LABEL = "Drill this";

export const VALUE_ACCURATE = "Accurate to three places";

export const VALUE_NOT_ACCURATE = "Not accurate to three places";

export const VALUE_FEW_PLACES = "Give three decimal places";

export const VALUE_WRONG = "Not the value Desmos gives for this setup";

export const VALUE_NOT_A_NUMBER = "Not a number";

export const SETUP_EQUIVALENT = "Setup shown and equivalent";

export const SETUP_NOT_EQUIVALENT = "Setup shown but not equivalent";

export const SETUP_MISSING = "No setup shown";

export const SETUP_UNREADABLE = "The expression could not be read";

export const NOT_MEASURED_YET = "not measured yet";

export const ANSWERED = "answered";

export const NONE_YET = "none yet";

export const HIDE_CLOCK = "Hide the clock";

export const SHOW_CLOCK = "Show the clock";

export const SKIP_TO_RESULT = "Skip to the result field";

export const OFFLINE_SENTENCE =
   "Desmos loads from the internet, so it needs a connection. A handheld calculator works for the drill; enter the result and the setup as before.";

export const RADIAN_NOTE = "Your calculator should be in radian mode.";

export const TASK_HEADING = "Task";

export const STEPS_HEADING = "Steps in Desmos";

export const DEMONSTRATION_HEADING = "One worked instance";

export const EXAM_HABIT_HEADING = "The habit on the exam";

export const BLUEBOOK_HEADING = "In Bluebook";

export const EXPECTED_SETUP_LEAD = "A setup that is equivalent:";

export const CHOOSER_LABEL = "Capability to drill";

export const CLOCK_LABEL = "Time on this task";

export const RECENT_HEADING = "The last twenty drills";

export const NO_DRILLS_YET = "No drill has been answered yet.";

export const DRILL_START_FAILED = "The drill could not be started.";

export const ANSWER_FAILED = "That did not go through. What you typed is still here, so you can check again.";

export const MEASURED_COLUMNS = ["Capability", "Answered", "Accurate to three places", "Setup shown", "Setup equivalent", "Median time"] as const;

export const CAPABILITY_ORDER: ReadonlyArray<CalculatorCapability> = ["plot", "zero", "derivative", "integral", "intersection", "value"];

export const CAPABILITY_NAMES: Record<CalculatorDrillRequestCapability, string> = {
   plot: "Plot and read an extreme value",
   zero: "Zeros and f(x) = k",
   derivative: "Derivative at a point",
   integral: "Definite integral",
   intersection: "Intersection as a bound",
   value: "Value at a point",
   mixed: "Mixed"
};

export function isCapability(value: string | undefined): value is CalculatorDrillRequestCapability {
   return value !== undefined && Object.prototype.hasOwnProperty.call(CAPABILITY_NAMES, value);
}

export function answeredText(count: number) {
   return count === 0 ? NONE_YET : `${count} ${ANSWERED}`;
}

export function secondsText(milliseconds: number) {
   const seconds = Math.round(milliseconds / 1000);

   return seconds === 1 ? "1 second" : `${seconds} seconds`;
}

export function ratioText(numerator: number, denominator: number) {
   return `${numerator} of ${denominator}`;
}

function figure(seconds: number) {
   return Number.isInteger(seconds) ? String(seconds) : seconds.toFixed(1);
}

/* The exam's own per-question figure, in the words the timed drill uses; it is stated, never
   offered as a target. */
export function budgetLine(sectionIPartB: number) {
   return `The exam allows ${figure(sectionIPartB)} seconds a question on Section I Part B.`;
}

export function budgetLines(sectionIPartB: number, sectionIIPartA: number) {
   return `The exam allows ${figure(sectionIPartB)} seconds a question on Section I Part B and ${figure(sectionIIPartA)} seconds a question on Section II Part A.`;
}

export function acceptedFormsText(rounded: string, truncated: string) {
   return `Rounded ${rounded}, truncated ${truncated}`;
}

export function valueVerdictText(verdict: CalculatorValueVerdict) {
   if (verdict.correct) {
      return VALUE_ACCURATE;
   }

   if (verdict.reason === "not_three_places") {
      return VALUE_FEW_PLACES;
   }

   if (verdict.reason === "outside_tolerance") {
      return VALUE_WRONG;
   }

   return VALUE_NOT_A_NUMBER;
}

export type SetupState = "equivalent" | "not_equivalent" | "missing" | "unreadable";

export function setupState(verdict: CalculatorSetupVerdict): SetupState {
   const wasRead = verdict.correct !== null;

   if (!verdict.shown) {
      return "missing";
   }

   if (!wasRead) {
      return "unreadable";
   }

   return verdict.correct === true ? "equivalent" : "not_equivalent";
}

export const SETUP_TEXT: Record<SetupState, string> = {
   equivalent: SETUP_EQUIVALENT,
   not_equivalent: SETUP_NOT_EQUIVALENT,
   missing: SETUP_MISSING,
   unreadable: SETUP_UNREADABLE
};

export const DEMO_FUNCTION_LEAD = "The function";

export const DEMO_SHOWS_LEAD = "Desmos shows";

export const DEMO_SETUP_LEAD = "Written on the page";

export const DEMO_ANSWER_LEAD = "Reported to three places";

export const BACK_TO_CARDS = "Back to the procedures";

export const CARD_LIST_LABEL = "Procedure cards";
