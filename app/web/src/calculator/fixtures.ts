import type {
   CalculatorAnswerPayload,
   CalculatorCard,
   CalculatorCardsPayload,
   CalculatorCapabilityMeasure,
   CalculatorDrill,
   CalculatorMeasuredPayload
} from "../api/types";

/* Payloads in the shape of the contract in docs/calculator/build-plan.md, trimmed to what the
   calculator screen tests read. Test data only. */

export const CARDS: CalculatorCardsPayload = {
   cards: [
      { id: "CDC-integral", capability: "integral", title: "Definite integral", task: "Evaluate a definite integral in Desmos.", drills: ["CDT-integral-01"] },
      { id: "CDC-derivative", capability: "derivative", title: "Derivative at a point", task: "Find a derivative at one input.", drills: ["CDT-derivative-01"] }
   ]
};

export const INTEGRAL_CARD: CalculatorCard = {
   id: "CDC-integral",
   version: 1,
   capability: "integral",
   title: "Definite integral",
   task: "Evaluate a definite integral in Desmos.",
   steps: [
      { text: "Start the integral with the template.", keys: "int" },
      { text: "Type the integrand after the bounds.", keys: "dx" }
   ],
   demonstration: {
      function_tex: "f(x)=\\sin(x^2)",
      lines: [
         { typed: "f(x)=sin(x^2)", shows: "the curve" },
         { typed: "int_0^2 f(x) dx", shows: "0.8048" }
      ],
      setup_latex: "\\int_0^2 \\sin(x^2)\\,dx",
      answer: "0.805"
   },
   exam_habit: [{ text: "The integral is written beside the value." }],
   bluebook_note: "Bluebook opens Desmos in radians.",
   drills: ["CDT-integral-01"]
};

export function drill(drillId: string): CalculatorDrill {
   return {
      drill_id: drillId,
      template_id: "CDT-integral-01",
      capability: "integral",
      card_id: "CDC-integral",
      prompt: "Find \\(\\int_0^2 \\sin(x^2)\\,dx\\).",
      function_tex: "\\sin(x^2)",
      unit: null,
      radian_sensitive: true,
      desmos_url: "https://www.desmos.com/testing/collegeboard/graphing",
      served_at: "2026-09-29T10:00:00Z"
   };
}

export function answer(overrides: Partial<CalculatorAnswerPayload> = {}): CalculatorAnswerPayload {
   return {
      drill_id: "DRL-1",
      value: { correct: true, reason: null, rounded: "3.901", truncated: "3.900" },
      setup: { shown: true, correct: true, reason: null, key_latex: "\\int_0^2 \\sin(x^2)\\,dx" },
      elapsed_ms: 42000,
      budget_seconds: { "I-B": 120, "II-A": 900 },
      ...overrides
   };
}

export function measure(capability: CalculatorCapabilityMeasure["capability"], answered: number, medianMs: number | null): CalculatorCapabilityMeasure {
   return {
      capability,
      served: answered,
      answered,
      value_correct: { numerator: answered, denominator: answered, value: answered === 0 ? null : 1 },
      setup_shown: { numerator: answered, denominator: answered, value: answered === 0 ? null : 1 },
      setup_correct: { numerator: answered, denominator: answered, value: answered === 0 ? null : 1 },
      median_ms: medianMs
   };
}

export function measured(capabilities: CalculatorCapabilityMeasure[] = []): CalculatorMeasuredPayload {
   return {
      capabilities,
      budget_seconds: { "I-B": 120, "II-A": 900 },
      recent: []
   };
}
