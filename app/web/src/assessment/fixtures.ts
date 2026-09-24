import type { AssessmentPart, AssessmentQuestion, AssessmentSession, AssessmentTool } from "../api/types";

/* Payload shapes captured from the running assessment routes, trimmed to what the screen tests
   read. Test data only. */

const NO_CALCULATOR_TOOLS: AssessmentTool[] = [
   "timer",
   "highlight_and_notes",
   "mark_for_review",
   "option_eliminator",
   "question_menu",
   "zoom"
];

export function multipleChoiceQuestion(number: number): AssessmentQuestion {
   return {
      number,
      kind: "mcq",
      format: "mcq",
      answer: null,
      marked: false,
      eliminated: [],
      notes: null,
      highlights: [],
      confidence: null,
      time_ms: 0,
      attempt_id: null,
      item: {
         id: `ITM-${number}`,
         archetype_id: "BC-QA-05010",
         variant_id: null,
         snapshot_id: null,
         parameter_draw: null,
         stem: `The function f is twice differentiable, question ${number}.`,
         figure_spec: null,
         options: [
            { id: "A", label: "First choice" },
            { id: "B", label: "Second choice" },
            { id: "C", label: "Third choice" },
            { id: "D", label: "Fourth choice" }
         ],
         calculator_status: "no_calculator",
         representation: null,
         difficulty_settings: null,
         skills: ["BC-SKL-05007"],
         status: "verified",
         requires_choice: true,
         radian_note: false
      }
   };
}

export function freeResponseQuestion(number: number): AssessmentQuestion {
   return {
      number,
      kind: "frq",
      format: "free_response",
      answer: null,
      marked: false,
      eliminated: [],
      notes: null,
      highlights: [],
      confidence: null,
      time_ms: 0,
      attempt_id: `ATT-${number}`,
      item: {
         id: `FRQ-${number}`,
         archetype_id: "BC-QA-09013",
         calculator_status: "calculator",
         stem: "The curves r = 4 sin(theta) and r = 1 + theta are drawn in the xy-plane.",
         parts: [
            { id: "a", prompt: "Find the area of R.", setup_required: true, points: 3 },
            { id: "b", prompt: "Find the area of S.", setup_required: true, points: 3 }
         ],
         radian_note: true
      }
   };
}

export function noCalculatorPart(overrides: Partial<AssessmentPart> = {}): AssessmentPart {
   return {
      key: "I-A",
      section: "I",
      part: "A",
      label: "Section I, Part A",
      question_type: "Multiple choice",
      multiple_choice: true,
      question_count: 3,
      minutes: 62,
      calculator: false,
      calculator_label: "NO CALCULATOR ALLOWED",
      calculator_note: "There is no calculator on this part. It is not hidden. It is not there.",
      first_number: 1,
      budget_seconds_per_question: 128.27586206896552,
      tools: NO_CALCULATOR_TOOLS,
      five_minute_alert_seconds: 300,
      position: 1,
      status: "open",
      timed: true,
      started_at: "2026-09-24T21:50:04+00:00",
      deadline_at: "2026-09-24T22:52:04+00:00",
      closed_at: null,
      closed_by: null,
      time_remaining_ms: 3720000,
      answered: 0,
      questions: [multipleChoiceQuestion(1), multipleChoiceQuestion(2), multipleChoiceQuestion(3)],
      ...overrides
   };
}

export function calculatorPart(overrides: Partial<AssessmentPart> = {}): AssessmentPart {
   return noCalculatorPart({
      key: "I-B",
      part: "B",
      label: "Section I, Part B",
      question_count: 2,
      minutes: 38,
      calculator: true,
      calculator_label: "CALCULATOR REQUIRED",
      calculator_note: null,
      first_number: 30,
      tools: [...NO_CALCULATOR_TOOLS, "graphing_panel"],
      position: 2,
      time_remaining_ms: 2280000,
      questions: [multipleChoiceQuestion(30), multipleChoiceQuestion(31)],
      ...overrides
   });
}

export function freeResponsePart(overrides: Partial<AssessmentPart> = {}): AssessmentPart {
   return noCalculatorPart({
      key: "II-A",
      section: "II",
      part: "A",
      label: "Section II, Part A",
      question_type: "Free response",
      multiple_choice: false,
      question_count: 2,
      minutes: 30,
      calculator: true,
      calculator_label: "CALCULATOR REQUIRED",
      calculator_note: null,
      tools: ["timer", "highlight_and_notes", "mark_for_review", "question_menu", "zoom", "graphing_panel"],
      position: 3,
      time_remaining_ms: 1800000,
      questions: [freeResponseQuestion(1), freeResponseQuestion(2)],
      ...overrides
   });
}

export function sessionWith(parts: AssessmentPart[]): AssessmentSession {
   return {
      id: "SES-MOCK",
      mode: "mock",
      sub_mode: "full_mock",
      updates_mastery: false,
      started_at: "2026-09-24T21:50:04+00:00",
      ended_at: null,
      capture_mode: "typed",
      parts,
      closed_part_note: "{label} is closed. You cannot return to its questions.",
      break_note:
         "{label} is closed. Take your break here. The next part starts when you choose to start it, and its timer starts then.",
      reference_sheet: { shown: false, note: "No reference sheet is shown." },
      radian_note: "Your calculator should be in radian mode."
   };
}
