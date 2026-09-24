import { readFileSync } from "node:fs";
import { join } from "node:path";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { AFFORDANCE_ATTRIBUTE, P1_FEEDBACK_AFFORDANCES } from "../affordances";
import { MOTION_CLASS_PREFIX, REDUCED_MOTION_QUERY, TRANSFORM_MOTION_CLASSES } from "../styles/motion";
import type {
   AttemptResult,
   FadingStage,
   FeedbackPayload,
   ServedItem,
   ServedStep,
   SessionPayload,
   StepMark
} from "../api/types";
import * as client from "../api/client";
import { SessionScreen } from "./SessionScreen";

vi.mock("../api/client");

const mocked = vi.mocked(client);

const STEM = "Differentiate f(x) = x^2 sin(x)";

const SELF_EXPLANATION_PROMPT = "Which rule justifies step 3, and why does it apply here?";

/* docs/plan/11-phased-delivery.md gate 25 names the stage each affordance has to reach the
   student at, so the stages are the gate's own list and not a sample. */
const STAGES: FadingStage[] = ["example", "completion", "unsupported"];

const STAGE_OF_STEP_VERIFICATION_MARK: FadingStage[] = ["example", "completion"];

const STAGE_OF_ELABORATED_PANEL: FadingStage = "unsupported";

function servedItem(stage: FadingStage): ServedItem {
   return {
      id: `item-${stage}`,
      archetype_id: "BC-ARCH-0301",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: STEM,
      figure_spec: null,
      options: null,
      calculator_status: null,
      representation: null,
      difficulty_settings: null,
      skills: ["BC-SKL-0301"],
      status: "published",
      stage,
      format: "short_answer",
      is_probe: false,
      served_steps: servedStepsAt(stage),
      self_explanation_prompt: stage === "example" ? SELF_EXPLANATION_PROMPT : null
   };
}

const session: SessionPayload = {
   id: "session-reduced-motion",
   mode: "practice",
   sub_mode: null,
   started_at: "2027-01-05T09:00:00Z",
   ended_at: null,
   updates_mastery: true,
   snapshot_id: null,
   queue: {
      block1: [],
      block2: [],
      block3: [],
      block4: [],
      forecasts: {},
      coverage_gaps: [],
      interleaving_satisfied: true,
      interleaving_shortfalls: []
   },
   remaining: []
};

function attempt(stage: FadingStage): AttemptResult {
   return {
      id: `attempt-${stage}`,
      item_id: `item-${stage}`,
      correct: false,
      confidence: "unsure",
      served_stage: stage,
      format: "short_answer",
      p_split: null,
      p_compensatory: null
   };
}

/* app/feedback/render.py as_dict step_marks: every step given at example, the steps shown given and
   the blank carrying the verdict at completion, none at unsupported. */
function stepMarksAt(stage: FadingStage, correct: boolean | null): StepMark[] {
   const shown = (servedStepsAt(stage) ?? []).map((step) => ({ ...step, given: true, correct: null }));

   if (stage === "completion") {
      return [...shown, { index: shown.length + 1, text: "f'(x) = 2x sin(x) + x^2 cos(x)", given: false, correct }];
   }

   return shown;
}

function feedback(stage: FadingStage): FeedbackPayload {
   const isUnsupported = stage === STAGE_OF_ELABORATED_PANEL;

   return {
      kind: isUnsupported ? "elaborated" : "step_verification",
      stage,
      step_marks: stepMarksAt(stage, false),
      elaborated: isUnsupported
         ? {
              violated_step: "Product rule applied to both factors at once",
              observed_behavior: "Each factor was differentiated separately",
              scoring_consequence: "On an AP rubric this loses the product rule point",
              worked_solution: null,
              error_id: "BC-ERR-0304"
           }
         : null,
      self_explanation_prompt: SELF_EXPLANATION_PROMPT,
      confidence: "unsure",
      sentence: null,
      tutor_unavailable: false
   };
}

/* app/runtime/bank.py served_steps: every step at example, all but the last at completion. */
function servedStepsAt(stage: FadingStage): ServedStep[] | null {
   const workedSteps: ServedStep[] = [
      { index: 1, text: "Name the factors: u = x^2, v = sin(x)" },
      { index: 2, text: "u' = 2x, v' = cos(x)" },
      { index: 3, text: "f'(x) = 2x sin(x) + x^2 cos(x)" }
   ];

   if (stage === "example") {
      return workedSteps;
   }

   if (stage === "completion") {
      return workedSteps.slice(0, -1);
   }

   return null;
}

function stubReducedMotion() {
   const matchMedia = (query: string) => {
      const asksForReduce = query.replace(/\s+/g, " ").trim() === REDUCED_MOTION_QUERY;

      return {
         matches: asksForReduce,
         media: query,
         onchange: null,
         addListener: () => undefined,
         removeListener: () => undefined,
         addEventListener: () => undefined,
         removeEventListener: () => undefined,
         dispatchEvent: () => false
      } as unknown as MediaQueryList;
   };

   vi.stubGlobal("matchMedia", matchMedia);
   window.matchMedia = matchMedia;
}

function affordanceValues() {
   return Array.from(document.querySelectorAll(`[${AFFORDANCE_ATTRIBUTE}]`)).map(
      (node) => node.getAttribute(AFFORDANCE_ATTRIBUTE) as string
   );
}

function mockStage(stage: FadingStage) {
   mocked.openSession.mockResolvedValue(session);
   mocked.readNextItem.mockResolvedValue({ item: servedItem(stage) });
   mocked.submitAttempt.mockResolvedValue(attempt(stage));
   mocked.readFeedback.mockResolvedValue(feedback(stage));
   mocked.submitErrorNote.mockResolvedValue({ id: `attempt-${stage}`, error_note: null });
   mocked.closeSession.mockResolvedValue({ id: session.id, ended_at: "2027-01-05T09:30:00Z" });
}

async function affordancesReachedAt(stage: FadingStage) {
   mockStage(stage);

   render(<SessionScreen resumeSessionId={null} />);

   const reached = new Set<string>();

   await screen.findByText(STEM);

   for (const value of affordanceValues()) {
      reached.add(value);
   }

   fireEvent.click(screen.getAllByRole("button", { name: /Check my answer|I have explained this/ })[0]);
   await screen.findByRole("button", { name: "Next item" });

   for (const value of affordanceValues()) {
      reached.add(value);
   }

   cleanup();

   return reached;
}

function motionStyleSheet() {
   const source = readFileSync(join(process.cwd(), "src", "styles", "motion.css"), "utf8");
   const element = document.createElement("style");

   element.textContent = source;
   document.head.appendChild(element);

   const sheets = Array.from(document.styleSheets) as CSSStyleSheet[];
   const loaded = sheets.find((sheet) => sheet === element.sheet);

   if (loaded === undefined) {
      throw new Error("motion.css did not reach document.styleSheets");
   }

   return loaded;
}

interface MotionRules {
   base: Map<string, CSSStyleRule>;
   reduce: Map<string, CSSStyleRule>;
}

function readMotionRules(sheet: CSSStyleSheet): MotionRules {
   const base = new Map<string, CSSStyleRule>();
   const reduce = new Map<string, CSSStyleRule>();

   for (const rule of Array.from(sheet.cssRules)) {
      const isMediaRule = rule instanceof CSSMediaRule;

      if (isMediaRule) {
         const media = rule.media.mediaText.replace(/\s+/g, " ").trim();
         const governsReducedMotion = media === REDUCED_MOTION_QUERY;

         if (!governsReducedMotion) {
            continue;
         }

         for (const inner of Array.from(rule.cssRules)) {
            const isStyleRule = inner instanceof CSSStyleRule;

            if (isStyleRule) {
               reduce.set(inner.selectorText, inner);
            }
         }

         continue;
      }

      const isStyleRule = rule instanceof CSSStyleRule;

      if (isStyleRule) {
         base.set(rule.selectorText, rule);
      }
   }

   return { base, reduce };
}

function transitionOf(rule: CSSStyleRule) {
   return rule.style.getPropertyValue("transition").toLowerCase();
}

beforeEach(() => {
   vi.clearAllMocks();
   stubReducedMotion();
});

afterEach(() => {
   cleanup();
   vi.unstubAllGlobals();

   for (const element of Array.from(document.head.querySelectorAll("style"))) {
      element.remove();
   }
});

describe("reduced motion keeps every P1 feedback affordance", () => {
   it("reports reduce for the query the stylesheet is written against", () => {
      expect(window.matchMedia(REDUCED_MOTION_QUERY).matches).toBe(true);
   });

   it("renders each affordance at the stage gate 25 names, ranging over the registry", async () => {
      const reachedAt = new Map<FadingStage, Set<string>>();

      for (const stage of STAGES) {
         reachedAt.set(stage, await affordancesReachedAt(stage));
      }

      for (const stage of STAGE_OF_STEP_VERIFICATION_MARK) {
         expect(Array.from(reachedAt.get(stage) as Set<string>)).toContain(
            P1_FEEDBACK_AFFORDANCES.stepVerificationMark
         );
      }

      expect(Array.from(reachedAt.get(STAGE_OF_ELABORATED_PANEL) as Set<string>)).toContain(
         P1_FEEDBACK_AFFORDANCES.elaboratedFeedbackPanel
      );

      const everywhere = new Set<string>();

      for (const reached of reachedAt.values()) {
         for (const value of reached) {
            everywhere.add(value);
         }
      }

      const missing = Object.values(P1_FEEDBACK_AFFORDANCES).filter(
         (affordance) => !everywhere.has(affordance)
      );

      expect(missing).toEqual([]);
   });
});

describe("reduced motion replaces transform with an opacity cross-fade", () => {
   it("declares a reduce rule for every class the stylesheet transitions transform on", () => {
      const { base, reduce } = readMotionRules(motionStyleSheet());

      const transformSelectors = Array.from(base.entries())
         .filter(([, rule]) => transitionOf(rule).includes("transform"))
         .map(([selector]) => selector)
         .sort();

      const registrySelectors = TRANSFORM_MOTION_CLASSES.map((name) => `.${name}`).sort();

      expect(transformSelectors).toEqual(registrySelectors);

      const unanswered = transformSelectors.filter((selector) => !reduce.has(selector));

      expect(unanswered).toEqual([]);
   });

   it("cross-fades on opacity instead of deleting the transition", () => {
      const { base, reduce } = readMotionRules(motionStyleSheet());

      const transformSelectors = Array.from(base.entries())
         .filter(([, rule]) => transitionOf(rule).includes("transform"))
         .map(([selector]) => selector);

      expect(transformSelectors.length).toBe(TRANSFORM_MOTION_CLASSES.length);

      for (const selector of transformSelectors) {
         const rule = reduce.get(selector) as CSSStyleRule;
         const transition = transitionOf(rule);
         const animation = rule.style.getPropertyValue("animation").toLowerCase();

         const crossFades = transition.includes("opacity");
         const stillMovesTransform = transition.includes("transform");
         const transitionDeleted = transition === "" || transition === "none";
         const animationDeleted = animation === "none";

         expect({ selector, crossFades }).toEqual({ selector, crossFades: true });
         expect({ selector, stillMovesTransform }).toEqual({ selector, stillMovesTransform: false });
         expect({ selector, transitionDeleted }).toEqual({ selector, transitionDeleted: false });
         expect({ selector, animationDeleted }).toEqual({ selector, animationDeleted: false });
      }
   });

   it("names every reduce selector with the motion class prefix", () => {
      const { reduce } = readMotionRules(motionStyleSheet());

      const foreign = Array.from(reduce.keys()).filter(
         (selector) => !selector.startsWith(`.${MOTION_CLASS_PREFIX}`)
      );

      expect(foreign).toEqual([]);
   });
});
