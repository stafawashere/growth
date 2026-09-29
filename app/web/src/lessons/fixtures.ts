import type { LessonDelivery, LessonPlan, LessonRecord, LessonSection, LessonSpec } from "../api/types";

/* Test data only: a lesson built from content/lessons/LSN-CON-02013.json (the record shape, its
   sections, checks and refresher), with delivery entries on the blocks that need one, plus
   synthetic sections carrying one delivery of each mode and one spec of each kind family, so every
   branch of the reader is exercised. */

export const GRAPH_SPEC: LessonSpec = {
   kind: "graph",
   window: { x: [-1, 5], y: [-4, 8] },
   curves: [{ expr: "-x**2 + 4*x + 2", domain: [-1, 5] }, { expr: "5 - 2*(x - 3)", domain: [1.5, 4.5] }],
   points: [{ at: [3, 5], label: { text: "(3, 5)", placement: "inside", at: "just above the point" } }],
   labels: [
      { text: "y = f(x)", placement: "inside", at: "near the vertex of the curve" },
      { text: "tangent at x = 3", placement: "inside", at: "along the tangent, right of the point" }
   ]
};

export const TABLE_SPEC: LessonSpec = {
   kind: "table",
   columns: ["t (minutes)", "D(t) (meters)"],
   rows: [[1, 20], [3, 31], [6, 43], [8, 52], [11, 70]],
   marked_rows: [2, 4],
   labels: [{ text: "(52 - 31)/(8 - 3) = 21/5 meters per minute", placement: "inside", at: "last line of the table frame" }]
};

export const MOTION_SPEC: LessonSpec = {
   kind: "graph_sweep",
   axes: { x: [0, 3.5], y: [-1, 12] },
   curves: [{ expr: "2*x**2 - 3*x + 1", domain: [0, 3.5] }],
   points: [{ at: [2, 3], label: { text: "(2, 3)", placement: "inside", at: "just above the point" } }],
   parameter: { name: "h", frames: [1, 0.5, 0.25, 0.1, 0.01] },
   secant: { through: ["(2, f(2))", "(2 + h, f(2 + h))"], slope: "2*h + 5" },
   labels: [{ text: "h = {h}", placement: "inside", at: "top left corner" }]
};

export const INTERACTIVE_SPEC: LessonSpec = {
   kind: "graph",
   curve: "f'(x) = 3(x - 1)^2(x + 2)",
   window: { x: [-3, 2], y: [-10, 12] },
   controls: [{ type: "slider", name: "x", domain: [-3, 2], step: 0.1, readout: "sign of f'(x)" }],
   question: "Does the sign of f' change as x passes -2? As x passes 1?",
   labels: [{ text: "graph of f'", placement: "inside" }]
};

export const MODEL_SPEC: LessonSpec = {
   kind: "numeric_experiment",
   function: "3*t**2 - 4*t + 6",
   at: 2,
   h_values: [1, 0.1, 0.01, 0.001],
   computed: "(s(2 + h) - s(2))/h",
   columns: ["h", "average rate over [2, 2 + h]"],
   labels: [{ text: "averages approach 8", placement: "inside", at: "row below the last value" }]
};

export const CONTRAST_SPEC: LessonSpec = {
   kind: "panels",
   marks: [
      { stem: "LSN-CON-02013#stem-1", feature: "a product of two expressions" },
      { stem: "LSN-CON-02013#stem-2", feature: "four supplied values at a point" }
   ]
};

function delivery(mode: LessonDelivery["mode"], spec?: LessonSpec, extra: Partial<LessonDelivery> = {}): LessonDelivery {
   const drawn = spec === undefined ? {} : { spec, fallback: `Fallback for ${spec.kind}.`, keyboard: "Tab reaches the control." };

   return { mode, reason: "rule 1", ...drawn, ...extra };
}

export const PREDICTION_ID = "LSN-CON-02013#s0";

export const FADED_EXAMPLE_ID = "LSN-CON-02013#s8";

export const ERROR_ID = "LSN-CON-02013#err-BC-ERR-02020";

const RECORD_SECTIONS: LessonSection[] = [
   {
      id: PREDICTION_ID,
      type: "prediction",
      bands: ["low", "mid"],
      stem: { text: "Before the rule: what does the derivative of \\(h(x)=(x^2+1)(x^3-2x)\\) look like?", command_verb: "predict" },
      format: "mcq",
      options: [
         { id: "A", label: "The product of the two derivatives", is_key: false },
         { id: "B", label: "Two terms, each with one derivative", is_key: true },
         { id: "C", label: "The derivative of the first factor only", is_key: false }
      ],
      resolution: { text: "A product gives two terms, each with one derivative." }
   },
   {
      id: "LSN-CON-02013#s1",
      type: "orientation",
      bands: ["low", "mid"],
      delivery: delivery("text"),
      text: "A response shows the derivative of a product as two terms added: the first factor times the derivative of the second, and the second factor times the derivative of the first."
   },
   {
      id: "LSN-CON-02013#s2",
      type: "key_ideas",
      bands: ["low", "mid"],
      depth: "core",
      delivery: delivery("text"),
      text: "For a product \\(fg\\) the derivative is \\(f'g+fg'\\) (BC-EK-FUN-3B1, ced:67). It is not \\(f'g'\\).",
      notation: "product rule",
      quote: { text: "Derivatives of products of differentiable functions can be found using the product rule.", source: "ced:67" }
   },
   {
      id: "LSN-CON-02013#s3",
      type: "strategy",
      bands: ["low", "mid"],
      cue: "The stem asks for the derivative of the product or quotient, from a product or quotient of two differentiable expressions.",
      method: "First written step: identify the two factors and their derivatives.",
      rival: "The rival is multiplying the derivatives of the two factors.",
      separating_feature: "A product gives two terms, each with one derivative.",
      contrast: {
         this: { text: "Let \\(h(x)=x e^x\\). Find \\(h'(x)\\).", archetype_id: "BC-QA-02008" },
         not_this: { text: "Let \\(h(x)=e^{x^2}\\). Find \\(h'(x)\\).", why_not: "One function sits inside another, so the chain rule applies." },
         feature: "two factors multiplied, not one function inside another"
      }
   },
   {
      id: "LSN-CON-02013#s5",
      type: "worked_example",
      bands: ["low", "mid"],
      delivery: delivery("step_reveal"),
      problem: { text: "Let \\(h(x)=(x^2+1)(x^3-2x)\\). Find \\(h'(x)\\).", command_verb: "find" },
      steps: [
         { cue: "The stem is a product of \\(f=x^2+1\\) and \\(g=x^3-2x\\).", why: "Each factor needs its own derivative: \\(f'=2x\\) and \\(g'=3x^2-2\\)." },
         {
            cue: "Two factors are multiplied, so the rule is \\(f'g+fg'\\).",
            why: "Both terms are needed. Each keeps one factor and differentiates the other.",
            expression: ["Add", ["Multiply", ["Multiply", 2, "x"], ["Add", ["Power", "x", 3], ["Multiply", -2, "x"]]], ["Multiply", ["Add", ["Power", "x", 2], 1], ["Add", ["Multiply", 3, ["Power", "x", 2]], -2]]],
            point_type_id: "BC-PT-99022"
         },
         {
            cue: "The stem asks for \\(h'(x)\\), so multiply out and collect terms.",
            why: "Expanding first agrees: \\(x^5-x^3-2x\\) differentiates to \\(5x^4-3x^2-2\\).",
            expression: ["Add", ["Multiply", 5, ["Power", "x", 4]], ["Multiply", -3, ["Power", "x", 2]], -2]
         }
      ]
   },
   {
      id: "LSN-CON-02013#s7",
      type: "what_a_reader_scores",
      bands: ["low", "mid"],
      example_id: "LSN-CON-02013#s5",
      lines: [{ point_type_id: "BC-PT-99022", text: "Product rule. Earned by: a differentiation that correctly applies the product rule to the given expression." }]
   },
   {
      id: ERROR_ID,
      type: "common_error",
      bands: ["low", "mid"],
      delivery: delivery("step_reveal"),
      error_id: "BC-ERR-02020",
      observed_behavior: "The response multiplies the derivatives of the two factors together.",
      scoring_consequence: "The rule point and the result point are both lost.",
      wrong_step: { text: "The derivatives of the two factors are multiplied: \\(f'g'\\)." },
      right_step: { text: "The rule adds two terms: \\(f'g+fg'\\)." },
      relation: "distinct",
      fix_prompt: true,
      possible_reason: { misconception_id: "BC-MIS-02011", text: "the derivative of a product is taken as the product of the derivatives" }
   },
   {
      id: FADED_EXAMPLE_ID,
      type: "worked_example",
      bands: ["low"],
      delivery: delivery("step_reveal"),
      problem: { text: "Let \\(k(x)=x^2(3x+1)\\). Find \\(k'(x)\\).", command_verb: "find" },
      fade_from: 2,
      steps: [
         { cue: "The factors are \\(f=x^2\\) and \\(g=3x+1\\).", why: "Each factor needs its own derivative.", expression: ["Multiply", 2, "x"] },
         {
            cue: "Two factors are multiplied, so the rule is \\(f'g+fg'\\).",
            why: "Each term keeps one factor and differentiates the other.",
            expression: ["Add", ["Multiply", 2, "x", ["Add", ["Multiply", 3, "x"], 1]], ["Multiply", 3, ["Power", "x", 2]]]
         },
         { cue: "Multiply out and collect terms.", why: "Expanding first agrees.", expression: ["Add", ["Multiply", 9, ["Power", "x", 2]], ["Multiply", 2, "x"]] }
      ],
      answer: { form: "symbolic", mathjson: ["Add", ["Multiply", 9, ["Power", "x", 2]], ["Multiply", 2, "x"]] }
   },
   {
      id: "LSN-CON-02013#prq-BC-PRQ-00001",
      type: "prerequisite_bridge",
      prerequisite_id: "BC-PRQ-00001",
      text: "A derivative of a sum is the sum of the derivatives."
   }
];

/* One synthetic representations block per drawn mode and per spec family. */
export const MODE_SECTIONS: LessonSection[] = [
   { id: "LSN-CON-02013#r-figure", type: "representations", text: "The graph and its tangent.", delivery: delivery("figure", GRAPH_SPEC) },
   { id: "LSN-CON-02013#r-table", type: "representations", text: "The table of distances.", delivery: delivery("table", TABLE_SPEC) },
   {
      id: "LSN-CON-02013#r-motion",
      type: "representations",
      text: "The secant closes on the tangent.",
      delivery: delivery("motion", MOTION_SPEC, { reduced_motion: "no auto-advance: each arrow key press cross-fades to the next frame" })
   },
   { id: "LSN-CON-02013#r-interactive", type: "representations", text: "The sign of the derivative.", delivery: delivery("interactive", INTERACTIVE_SPEC) },
   { id: "LSN-CON-02013#r-model", type: "representations", text: "Difference quotients at shrinking h.", delivery: delivery("model", MODEL_SPEC) },
   {
      id: "LSN-CON-02013#r-unknown",
      type: "representations",
      text: "A kind this reader does not draw.",
      delivery: delivery("figure", { kind: "hologram" })
   }
];

export const LESSON: LessonRecord = {
   id: "LSN-CON-02013",
   version: 1,
   kind: "concept",
   target_id: "BC-CON-02013",
   status: "signed_off",
   read_minutes: { full: 4, brief: 2.5 },
   word_count: { full: 563, brief: 344 },
   sections: [...RECORD_SECTIONS, ...MODE_SECTIONS],
   checks: [
      {
         id: "LSN-CON-02013#chk-1",
         check_kind: "completion",
         bands: ["low", "mid"],
         format: "short_answer",
         stem: { text: "The product rule gives \\(h'(x)=(2x)(x^3-2x)+(x^2+1)(3x^2-2)\\). Multiply out and collect terms to write \\(h'(x)\\).", command_verb: "write" },
         completes: "LSN-CON-02013#s5"
      },
      {
         id: "LSN-CON-02013#chk-3",
         check_kind: "mcq",
         bands: ["low"],
         format: "mcq",
         stem: { text: "Suppose \\(f(2)=3\\), \\(f'(2)=5\\), \\(g(2)=4\\), \\(g'(2)=-1\\) and \\(h(x)=f(x)g(x)\\). Find \\(h'(2)\\).", command_verb: "find" },
         options: [
            { id: "A", value: 9, error_path: "BC-ERR-02024" },
            { id: "B", value: -5, error_path: "BC-ERR-02020" },
            { id: "C", value: 17, error_path: null },
            { id: "D", value: 32, error_path: "BC-ERR-02024" }
         ]
      }
   ],
   refresher: ["LSN-CON-02013#s2", "LSN-CON-02013#err-BC-ERR-02020", "LSN-CON-02013#s5"],
   decision: {
      unit: "BC-UNIT-02",
      skills: ["BC-SKL-02036"],
      selecting_feature: "whether the stem gives expressions or values",
      delivery: { mode: "contrast", reason: "plan 15 decision lessons", spec: CONTRAST_SPEC, fallback: "The stems one under another.", keyboard: "Tab moves between the stems." },
      stems: [
         { id: "LSN-CON-02013#stem-1", archetype_id: "BC-QA-02008", method: "Apply the product rule to the two factors", text: "Let \\(h(x)=x e^x\\). Find \\(h'(x)\\)." },
         { id: "LSN-CON-02013#stem-2", archetype_id: "BC-QA-02009", method: "Record the four values, then apply the rule", text: "Given \\(f(1)=2\\), \\(f'(1)=3\\), \\(g(1)=-1\\), \\(g'(1)=4\\), find \\(h'(1)\\)." }
      ]
   }
};

export function sectionNamed(id: string): LessonSection {
   const found = LESSON.sections.find((section) => section.id === id);

   if (found === undefined) {
      throw new Error(`fixture has no section ${id}`);
   }

   return found;
}

export function planFor(sectionIds: string[], checkIds: string[] = [], reason: LessonPlan["reason"] = "first_contact"): LessonPlan {
   const byId = new Map(LESSON.sections.map((section) => [section.id, section.type] as const));

   return {
      lesson_id: LESSON.id,
      version: 1,
      band: "low",
      reason,
      sections: [
         ...sectionIds.map((id) => ({ id, type: byId.get(id)!, form: "full" as const })),
         ...checkIds.map((id) => ({ id, type: "check" as const, form: "full" as const }))
      ],
      checks: checkIds,
      minutes: 4,
      words: 563,
      anchors: []
   };
}
