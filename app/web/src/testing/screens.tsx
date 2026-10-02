import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { ReactElement } from "react";
import { expect, vi } from "vitest";

import { AccountScreen } from "../account/AccountScreen";
import { App } from "../App";
import * as client from "../api/client";
import type {
   AiNotice,
   AssessmentShape,
   AttemptResult,
   CalibrationPayload,
   FeedbackPayload,
   FigureSpec,
   FrqAttempt,
   FrqQuestion,
   GradingsPayload,
   LibraryPayload,
   MasteryMapPayload,
   PacePayload,
   ServedItem,
   SessionPayload,
   StepMark,
   TutorFigureSpec,
   TutorMarksSpec
} from "../api/types";
import { calculatorPart, multipleChoiceQuestion, noCalculatorPart } from "../assessment/fixtures";
import { PartRunner } from "../assessment/PartRunner";
import { CaptureScreen } from "../frq/CaptureScreen";
import { ReadBackEditor, ReadBackView } from "../frq/ReadBack";
import { GradingView } from "../frq/GradingView";
import { HomeScreen, type HomeScreenStatus } from "../home/HomeScreen";
import { DiagnosticIntro, DiagnosticItem, DiagnosticResultView } from "../onboarding/OnboardingScreen";
import { CalibrationCurve } from "../progress/CalibrationCurve";
import { MasteryMap } from "../progress/MasteryMap";
import { RepresentationMatrix } from "../progress/RepresentationMatrix";
import { ReviewScreen } from "../review/ReviewScreen";
import { LESSON, planFor } from "../lessons/fixtures";
import { LessonReader } from "../lessons/LessonReader";
import { LessonLibrary } from "../progress/LessonLibrary";
import { AiNoticeToast } from "../notices/AiNotices";
import { ElaboratedPanel } from "../session/ElaboratedPanel";
import { SessionScreen } from "../session/SessionScreen";
import { ReauthPromptView } from "../account/ReauthPrompt";
import { SettingsPage } from "../settings/SettingsPage";
import { AccountPage } from "../account/AccountPage";
import { AssessmentRoute } from "../assessment/AssessmentRoute";
import { FrqUnitCheck } from "../frq/FrqRoute";
import { LessonsRoute } from "../lessons/LessonsRoute";
import { PaceStatement } from "../progress/PaceStatement";
import type { SettingsTab } from "../routing";
import { TutorHarness, UNCHECKED_ITEM, frame } from "./agent";
import { ArtBoard, type BoardMode } from "../agent/ArtBoard";
import { EVERY_ROLE_FIGURE, EVERY_ROLE_MARKS, ITEM_MARKS, LABELLED_TABLE, SECANT_TO_TANGENT, TABLE_MARKS, TABLE_OF_VALUES, TRIANGLE_DIAGRAM } from "../agent/figureFixtures";
import { PageMarks } from "../agent/PageMarks";
import { Item } from "../session/Item";
import { TutorFigure } from "../agent/TutorFigure";
import { Loading } from "../status/LoadState";
import type { CountdownPace } from "../ui/Countdown";

/* Test support: the screens and states the P8 evals render, each inside the app page App renders
   every destination in. A caller must vi.mock("../api/client") before using the screens that read
   from it. Test data only. */

export interface Screen {
   name: string;
   mount: () => Promise<HTMLElement>;
}

const mocked = vi.mocked(client);

export function inPage(content: ReactElement) {
   return render(<main className="app-page">{content}</main>).container;
}

async function settle() {
   await act(async () => {
      await Promise.resolve();
   });
}

export const FUNCTION_GRAPH: FigureSpec = {
   kind: "function_graph",
   domain: [-4, 4],
   range: [-4, 4],
   curves: [{ segments: [[[-4, -2], [0, 0], [4, 2]]], style: "solid" }],
   fills: [{ points: [[0, 0], [2, 1], [2, 0]] }],
   marks: [
      { type: "point", at: [2, 1] },
      { type: "open_point", at: [-2, -1] },
      { type: "segment", from: [1, -4], to: [1, 4], style: "dashed" },
      { type: "segment", from: [-4, 3], to: [4, 3], style: "solid" }
   ],
   labels: [{ text: "\\(y = f(x)\\)", anchor: [2.5, 2.5], placement: "inside" }],
   gridlines: true,
   axis_titles: ["x", "y"],
   alt: "The graph of y = f(x) through the origin."
};

export const TABLE_FIGURE: FigureSpec = {
   kind: "table",
   columns: ["\\(x\\)", "\\(f(x)\\)"],
   rows: [["1", "\\(e^{2}\\)"]],
   labels: [],
   alt: "Values of f."
};

export function servedItem(overrides: Partial<ServedItem> = {}): ServedItem {
   return {
      id: "ITM-1",
      archetype_id: "BC-ARCH-0301",
      variant_id: null,
      snapshot_id: null,
      parameter_draw: null,
      stem: "Differentiate \\(f(x) = x^2 \\sin x\\).",
      figure_spec: FUNCTION_GRAPH,
      options: null,
      calculator_status: "calculator",
      representation: null,
      difficulty_settings: null,
      skills: ["BC-SKL-0301"],
      status: "verified",
      stage: "completion",
      format: "short_answer",
      is_probe: false,
      served_steps: [
         { index: 1, text: "Name the factors \\(u = x^2\\), \\(v = \\sin x\\)" },
         { index: 2, text: "\\(u' = 2x\\), \\(v' = \\cos x\\)" }
      ],
      self_explanation_prompt: "Which rule justifies the last step?",
      ...overrides
   };
}

export const SESSION: SessionPayload = {
   id: "SES-1",
   mode: "learning",
   sub_mode: null,
   started_at: "2027-01-05T09:30:00",
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

export const EVERY_STEP_MARK: StepMark[] = [
   { index: 1, text: "Name the factors \\(u = x^2\\)", given: true, correct: null },
   { index: 2, text: "\\(u' = 2x\\)", given: false, correct: true },
   { index: 3, text: "\\(f'(x) = 2x\\)", given: false, correct: false },
   { index: 4, text: "Combine the terms", given: false, correct: null }
];

function feedbackFor(stage: ServedItem["stage"]): FeedbackPayload {
   const isUnsupported = stage === "unsupported";

   return {
      kind: isUnsupported ? "elaborated" : "step_verification",
      stage,
      step_marks: isUnsupported ? [] : EVERY_STEP_MARK,
      elaborated: isUnsupported
         ? {
              violated_step: "Product rule applied to both factors at once",
              observed_behavior: "Each factor was differentiated separately",
              scoring_consequence: "On an AP rubric this loses the product rule point",
              worked_solution: null,
              error_id: "BC-ERR-0304"
           }
         : null,
      self_explanation_prompt: "Which rule justifies step 3?",
      confidence: "unsure",
      sentence: isUnsupported ? "The derivative of a product is not the product of the derivatives." : null,
      tutor_unavailable: false
   };
}

function attemptFor(stage: ServedItem["stage"]): AttemptResult {
   return {
      id: "ATT-1",
      item_id: "ITM-1",
      correct: false,
      confidence: "unsure",
      served_stage: stage,
      format: "short_answer",
      p_split: null,
      p_compensatory: null
   };
}

export async function sessionFeedback(stage: ServedItem["stage"]) {
   mocked.openSession.mockResolvedValue(SESSION);
   mocked.readNextItem.mockResolvedValue({ item: servedItem({ stage }) });
   mocked.submitAttempt.mockResolvedValue(attemptFor(stage));
   mocked.readFeedback.mockResolvedValue(feedbackFor(stage));

   const container = inPage(<SessionScreen resumeSessionId={null} />);

   fireEvent.click(await screen.findByRole("button", { name: "Check my answer" }));
   fireEvent.click(await screen.findByRole("radio", { name: "unsure" }));
   await screen.findByTestId("feedback");

   return container;
}

export const MASTERY: MasteryMapPayload = {
   today: "2027-01-05",
   states: ["not_attempted", "in_progress", "mastered", "fading", "gap"],
   units: [
      {
         unit_id: "BC-UNIT-03",
         number: 3,
         name: "Differentiation: Composite, Implicit, and Inverse Functions",
         nodes: (["mastered", "fading", "in_progress", "not_attempted", "gap"] as const).map((state, index) => ({
            skill_id: `BC-SKL-0300${index}`,
            name: `Skill ${index}`,
            state,
            depth: index,
            assumed: false,
            last_success_on: null,
            days_since_success: null
         }))
      }
   ]
};

export const CALIBRATION: CalibrationPayload = {
   available: true,
   rated_attempts: 40,
   minimum_rated_attempts: 30,
   attempts_needed: 0,
   window_days: 30,
   window_start: "2026-12-07",
   window_end: "2027-01-05",
   bins: [
      { confidence: "guess", attempts: 0, correct: 0, accuracy: null, interval_low: null, interval_high: null },
      { confidence: "unsure", attempts: 15, correct: 9, accuracy: 0.6, interval_low: 0.36, interval_high: 0.8 },
      { confidence: "confident", attempts: 25, correct: 21, accuracy: 0.84, interval_low: 0.65, interval_high: 0.94 }
   ]
};

export function gradings(): GradingsPayload {
   const point = {
      grading_id: "G-1",
      part_id: "a",
      point_id: "P-1",
      point_type_id: "answer",
      point_label: "Answer",
      criterion: "States the critical point",
      decided_by: "grader",
      earned: 1,
      provisional: false,
      rationale: "The answer is stated",
      evidence_quote: "x = 3",
      eligibility_note: null,
      rereads: 0
   };

   return {
      attempt_id: "ATT-1",
      item_id: "ITM-1",
      grading_state: "graded",
      points: [
         point,
         { ...point, grading_id: "G-2", point_id: "P-2", earned: 0 },
         { ...point, grading_id: "G-3", point_id: "P-3", earned: null, provisional: true }
      ],
      earned: 1,
      decided: 2,
      total: 3,
      provisional: 1,
      worked_solution: [{ part_id: "a", answer_latex: "x = 3", steps: [{ text: "Set", latex: "g'(x) = 0" }] }],
      probe_scheduled: null,
      tutor_explanation: null,
      tutor_unavailable: false
   };
}

export const READ_BACK = {
   parts: [
      {
         part_id: "a",
         lines: [
            { kind: "math" as const, content: "g'(x) = (x - 3)e^{x}", crossed_out: false, outside_box: false },
            { kind: "text" as const, content: "so the minimum is at 3", crossed_out: true, outside_box: false }
         ],
         answer: "x = 3"
      }
   ],
   unreadable: []
};

const FRQ_QUESTION: FrqQuestion = {
   id: "FRQ-AGT-05007-01",
   archetype_id: "BC-QA-05007",
   calculator_status: "no_calculator",
   stem: "The function \\(g\\) is defined by an integral.",
   parts: [{ id: "a", prompt: "Find the critical point.", setup_required: false, points: 2 }]
};

function frqAttempt(fields: Partial<FrqAttempt> = {}): FrqAttempt {
   return {
      attempt_id: "ATT-1",
      item_id: FRQ_QUESTION.id,
      capture_mode: "photo",
      grading_state: "capturing",
      transcription_confirmed: false,
      read_back: null,
      confirmed: null,
      images: [],
      ...fields
   };
}

async function photographedReadBack() {
   mocked.startFrqAttempt.mockResolvedValue(frqAttempt());
   mocked.uploadPhoto.mockResolvedValue({ image_id: "IMG-1", accepted: true, reasons: [], measurements: {} });
   mocked.requestReadBack.mockResolvedValue(frqAttempt({ read_back: READ_BACK, grading_state: "awaiting_confirmation" }));

   const container = inPage(
      <CaptureScreen sessionId="SES-1" question={FRQ_QUESTION} pollMilliseconds={5} readFile={async () => "anBlZw=="} />
   );

   fireEvent.click(screen.getByRole("button", { name: "Write on paper and photograph it" }));
   fireEvent.change(await screen.findByLabelText("Photo of the page"), {
      target: { files: [new File(["jpeg"], "page.jpg", { type: "image/jpeg" })] }
   });
   fireEvent.click(await screen.findByRole("button", { name: "Read my page" }));
   await screen.findByTestId("read-back-confirm");

   return container;
}

function homeScreen(status: HomeScreenStatus, pace: CountdownPace | null = null) {
   return inPage(
      <HomeScreen
         status={status}
         examDate="Monday 10 May 2027"
         daysToExam={125}
         queueMinutes={23}
         queueLines={[
            { id: "due", label: "skills due for review", count: 12 },
            { id: "frontier", label: "skills at your current frontier", count: 4 },
            { id: "corrected", label: "corrected items coming back", count: 7 }
         ]}
         focus={[
            { block: "review", items: 5, skills: ["Compute a right Riemann sum from a table of values"], more_skills: 0, units: [6] },
            {
               block: "learn",
               items: 8,
               skills: ["Find the radius of convergence of a power series", "Apply the ratio test"],
               more_skills: 3,
               units: [10]
            }
         ]}
         onStartSession={vi.fn()}
         onAddPracticeSet={vi.fn()}
         onResumeSession={vi.fn()}
         onStartRediagnostic={vi.fn()}
         pace={pace}
      />
   );
}

export async function partRunner(part: ReturnType<typeof noCalculatorPart>) {
   const container = inPage(
      <PartRunner part={part} radianNote="Radian mode." sectionCount={42} onSave={vi.fn()} onSubmit={vi.fn()} onTimeUp={vi.fn()} />
   );

   await settle();
   fireEvent.click(screen.getByRole("button", { name: "Question menu" }));

   return container;
}

export function workedQuestion() {
   return {
      ...multipleChoiceQuestion(1),
      answer: { option_id: "A" },
      marked: true,
      eliminated: ["B"],
      highlights: [{ start: 0, end: 12 }]
   };
}

function serverRefusal(detail: string) {
   return Object.assign(Object.create(client.ApiError.prototype), { status: 401, detail });
}

async function accountScreen(status: client.AuthStatus, firstControl: string) {
   mocked.readAuthStatus.mockResolvedValue(status);

   const container = inPage(<AccountScreen onSignedIn={vi.fn()} />);

   await screen.findByRole("button", { name: firstControl });

   return container;
}

/* The lesson reader's screens (docs/plan/15-lessons.md UI), one per state that draws something of
   its own: every mode block, the revealed steps, the wrong-beside-right pair, a check answered
   wrong, the contrast screen, a refresher and the progress Lessons section. */
function lessonReader(sectionIds: string[], checkIds: string[] = [], overrides: Partial<Parameters<typeof LessonReader>[0]> = {}) {
   return inPage(
      <LessonReader
         lesson={LESSON}
         plan={planFor(sectionIds, checkIds)}
         band="low"
         context="session"
         conceptName="the product rule"
         onComplete={vi.fn()}
         onSkip={vi.fn()}
         onSectionViewed={vi.fn()}
         onCheckAnswer={vi.fn().mockResolvedValue({ correct: false, error_id: "BC-ERR-02020", anchor: "#err-BC-ERR-02020", explanation_anchor: null })}
         {...overrides}
      />
   );
}

function revealEveryStep() {
   while (screen.queryByTestId("lesson-next-step") !== null) {
      fireEvent.click(screen.getByTestId("lesson-next-step"));
   }
}

const LESSON_SCREENS: Screen[] = [
   {
      name: "lesson, worked example with every step shown",
      mount: async () => {
         const container = lessonReader(["LSN-CON-02013#s5"]);

         revealEveryStep();

         return container;
      }
   },
   {
      name: "lesson, error block with the wrong step beside the right step",
      mount: async () => {
         const container = lessonReader(["LSN-CON-02013#err-BC-ERR-02020"]);

         revealEveryStep();

         return container;
      }
   },
   { name: "lesson, key idea with its quote", mount: async () => lessonReader(["LSN-CON-02013#s2"]) },
   {
      name: "lesson, prediction committed",
      mount: async () => {
         const container = lessonReader(["LSN-CON-02013#s0"], [], { onPromptAnswer: vi.fn().mockResolvedValue({ correct: false, resolution: "A product gives two terms." }) });

         fireEvent.click(container.querySelector("input[type='radio']")!);
         fireEvent.click(screen.getByTestId("lesson-prediction-commit"));
         await screen.findByTestId("lesson-next");
         await waitFor(() => expect(screen.queryByTestId("lesson-prediction-commit")).toBeNull());

         return container;
      }
   },
   {
      name: "lesson, key idea after a committed prediction",
      mount: async () => {
         const container = lessonReader(["LSN-CON-02013#s0", "LSN-CON-02013#s2"], [], { onPromptAnswer: vi.fn().mockResolvedValue({ correct: false, resolution: "A product gives two terms." }) });

         fireEvent.click(container.querySelector("input[type='radio']")!);
         fireEvent.click(screen.getByTestId("lesson-prediction-commit"));
         await waitFor(() => expect(screen.queryByTestId("lesson-prediction-commit")).toBeNull());
         fireEvent.click(screen.getByTestId("lesson-next"));
         await screen.findByTestId("lesson-prediction-resolution");

         return container;
      }
   },
   {
      name: "lesson, check wrong with the error's part opened below it",
      mount: async () => {
         const container = lessonReader([], ["LSN-CON-02013#chk-3"]);

         fireEvent.click(container.querySelector("input[type='radio']")!);
         fireEvent.click(screen.getByTestId("lesson-check-submit"));
         fireEvent.click(await screen.findByTestId("lesson-link"));
         await screen.findByTestId("lesson-inline-section");

         return container;
      }
   },
   { name: "lesson, strategy", mount: async () => lessonReader(["LSN-CON-02013#s3"]) },
   { name: "lesson, figure", mount: async () => lessonReader(["LSN-CON-02013#r-figure"]) },
   { name: "lesson, table with marked rows", mount: async () => lessonReader(["LSN-CON-02013#r-table"]) },
   { name: "lesson, figure that cannot be drawn shows its fallback", mount: async () => lessonReader(["LSN-CON-02013#r-unknown"]) },
   {
      name: "lesson, motion stepped one frame",
      mount: async () => {
         const container = lessonReader(["LSN-CON-02013#r-motion"]);

         fireEvent.keyDown(screen.getByTestId("frame-stepper"), { key: "ArrowRight" });

         return container;
      }
   },
   { name: "lesson, interactive control", mount: async () => lessonReader(["LSN-CON-02013#r-interactive"]) },
   {
      name: "lesson, model with its current row",
      mount: async () => {
         const container = lessonReader(["LSN-CON-02013#r-model"]);

         fireEvent.click(screen.getByTestId("model-run"));

         return container;
      }
   },
   {
      name: "lesson, decision stems side by side",
      mount: async () => {
         const container = lessonReader(["LSN-CON-02013#s3"], [], { lesson: { ...LESSON, kind: "decision" } });

         fireEvent.click(screen.getByTestId("lesson-next"));
         await screen.findByTestId("contrast-panel");

         return container;
      }
   },
   {
      name: "lesson, check answered wrong with its error link",
      mount: async () => {
         const container = lessonReader([], ["LSN-CON-02013#chk-3"]);

         fireEvent.click(container.querySelector("input[type='radio']")!);
         fireEvent.click(screen.getByTestId("lesson-check-submit"));
         await screen.findByTestId("lesson-link");

         return container;
      }
   },
   {
      name: "lesson, refresher panel",
      mount: async () => inPage(
         <LessonReader
            lesson={LESSON}
            plan={planFor(["LSN-CON-02013#s2", "LSN-CON-02013#err-BC-ERR-02020", "LSN-CON-02013#s5"], [], "T1")}
            band="low"
            context="session"
            conceptName="the product rule"
            onComplete={vi.fn()}
            onSkip={vi.fn()}
            onSectionViewed={vi.fn()}
            onCheckAnswer={vi.fn()}
         />
      )
   },
   {
      name: "lesson, library end screen",
      mount: async () => {
         const container = lessonReader(["LSN-CON-02013#s1"], [], { context: "library" });

         fireEvent.click(screen.getByTestId("lesson-next"));

         return container;
      }
   },
   {
      name: "progress Lessons section",
      mount: async () =>
         inPage(
            <section className="card">
               <LessonLibrary
                  library={{
                     units: [
                        {
                           id: "BC-UNIT-02",
                           name: "Differentiation: Definition and Fundamental Properties",
                           order: 2,
                           concepts: [
                              { concept_id: "BC-CON-02013", name: "The product rule", lesson_id: "LSN-CON-02013", version: 1, servable: true, state: "read", read_at: "2026-10-03T09:00:00Z" },
                              { concept_id: "BC-CON-02014", name: "The quotient rule", lesson_id: null, version: null, servable: false, state: "not_available", read_at: null }
                           ]
                        }
                     ]
                  }}
                  onOpenLesson={vi.fn()}
               />
            </section>
         )
   }
];

const AI_NOTICE: AiNotice = {
   id: 4,
   role: "tutor",
   provider: "subscription",
   model: "claude-sonnet-5",
   outcome: "answered",
   replayed: false,
   asked: "a one-line hint",
   answered: "the hint arrived",
   created_at: "2027-01-05T09:30:00"
};

const ME: client.MePayload = { id: "USR-1", username: "sam", display_name: "student", exam_date: "2027-05-10", purge_after: "2027-06-09" };

const PACE = {
   as_of: "2027-01-05",
   verdict: "ahead",
   statement: "Ahead of pace.",
   exam_date: "2027-05-10",
   days_to_exam: 125,
   review_reserve_days: 28,
   new_mastery_deadline: "2027-04-12",
   skills: { total: 541, held: 120, fading: 6, assumed: 0, remaining: 421, remaining_weighted: 400 },
   rate: { window_start: "2026-12-06", window_days: 30, earned_weighted: 40, weekly: 9.3, required_weekly: 8.1, pace_ratio: 1.1, projected_finish: "2027-03-30" },
   study_time: {
      window_start: "2026-12-06",
      window_days: 30,
      active_days: 20,
      timed_attempts: 80,
      attempts: 90,
      minutes: 600,
      minutes_per_active_day: 30,
      active_days_per_week: 5,
      minutes_per_week: 150
   },
   evidence: {
      graded_attempts: 90,
      recent_accuracy: { value: 0.8, correct: 16, graded: 20, days: 14 },
      retention_30_day: { value: null, correct: 0, attempts: 0 }
   },
   caveat: "A pace on mastering the exam's skills, not a predicted AP score."
} as unknown as PacePayload;

const LESSONS_LIBRARY: LibraryPayload = {
   units: [
      {
         id: "BC-UNIT-02",
         name: "Differentiation: Definition and Fundamental Properties",
         order: 2,
         concepts: [
            { concept_id: "BC-CON-02013", name: "The product rule", lesson_id: "LSN-CON-02013", version: 1, servable: true, state: "read", read_at: "2027-01-02T09:00:00" },
            { concept_id: "BC-CON-02014", name: "The quotient rule", lesson_id: "LSN-CON-02014", version: 1, servable: true, state: "coming_up", read_at: null },
            { concept_id: "BC-CON-02015", name: "Derivatives of the other trigonometric functions", lesson_id: null, version: null, servable: false, state: "not_available", read_at: null }
         ]
      }
   ]
};

async function settingsPage(tab: SettingsTab) {
   mocked.readProviders.mockResolvedValue({
      roles: [{ role: "tutor", provider: "anthropic", model: "claude-sonnet-5", wired: true }],
      chains: { tutor: ["subscription"], grading: ["subscription"] },
      cooling: []
   });
   mocked.readBudgets.mockResolvedValue({
      day: "2027-01-05",
      roles: [
         {
            role: "tutor",
            cap_usd: 6,
            cap_tokens: 70000,
            cost_usd: 1.25,
            tokens_in: 800,
            tokens_out: 90,
            tokens_cached_read: 31,
            tokens_cached_write: 17,
            hard_stopped: false
         }
      ],
      month_to_date_usd: 3.5
   });
   mocked.readSettings.mockResolvedValue({ exam_date: "2027-05-10", purge_after: "2027-06-09", desired_retention: 0.9 });
   mocked.readStudyPlan.mockResolvedValue({ study_plan: "After breakfast, at my desk." });
   mocked.readExperiments.mockResolvedValue({
      experiments: [
         {
            name: "worked_example_fading",
            description: "Fade worked steps.",
            unit: "skill",
            arms: ["control", "treatment"],
            state: "on",
            randomised_from: null,
            assigned_units: { control: 3, treatment: 4 }
         }
      ]
   });

   mocked.readAgentMemories.mockResolvedValue({
      memory_paused: false,
      groups: [
         {
            kind: "preference",
            label: "How you like to be helped",
            entries: [{ id: "MEM-1", kind: "preference", text: "Short questions first", skill_ids: [], created_at: "2027-01-04T09:00:00", source_conversation_id: "ACV-1", editable: true }]
         }
      ]
   });
   mocked.readAgentConversations.mockResolvedValue({
      conversations: [{ id: "ACV-1", opened_at: "2027-01-04T09:00:00", last_turn_at: "2027-01-04T09:05:00", closed_at: null, opened_on_screen: "today", turn_count: 2 }]
   });
   mocked.readAgentConversation.mockResolvedValue({
      id: "ACV-1",
      opened_at: "2027-01-04T09:00:00",
      last_turn_at: "2027-01-04T09:05:00",
      closed_at: null,
      opened_on_screen: "today",
      turn_count: 2,
      turns: [
         { id: "ATN-1", role: "student", text: "Where do I start?", created_at: "2027-01-04T09:00:00", outcome: null },
         { id: "ATN-2", role: "agent", text: "What does the question ask for?", created_at: "2027-01-04T09:00:05", outcome: "complete" }
      ]
   });
   mocked.readAgentProfile.mockResolvedValue({ profile: null, version: null, experiment: "off" });

   const container = inPage(
      <SettingsPage
         tab={tab}
         onChangeTab={vi.fn()}
         purgeConfirmationPhrase="delete my data"
         saveFile={vi.fn()}
         aiNoticesOn
         onAiNoticesChange={vi.fn()}
         onOpenEvidence={vi.fn()}
         onRunDiagnostic={vi.fn()}
      />
   );

   await settle();

   if (tab === "budgets") {
      fireEvent.click(await screen.findByRole("button", { name: "open" }));
   }

   if (tab === "tutor") {
      fireEvent.click(await screen.findByRole("button", { name: "Open" }));
      await screen.findByText("What does the question ask for?");
   }

   if (tab === "operator") {
      await waitFor(() => expect(screen.getAllByTestId("experiment-switch").length).toBeGreaterThan(0));
   }

   return container;
}

async function assessmentsHub(format: "unit" | "drill" | "mock") {
   mocked.readAssessmentShape.mockResolvedValue({
      form: "2027",
      parts: [
         {
            key: "I-A",
            section: "I",
            part: "A",
            label: "Section I, Part A",
            question_type: "Multiple choice",
            multiple_choice: true,
            question_count: 30,
            minutes: 60,
            calculator: false,
            calculator_label: "No calculator",
            calculator_note: null,
            first_number: 1,
            budget_seconds_per_question: 120,
            tools: []
         }
      ],
      multiple_choice_total: 45,
      free_response_total: 6,
      points_per_free_response_question: 9,
      section_weights: {},
      testing_minutes: 195,
      reference_sheet: { shown: false, note: "No reference sheet is shown." },
      radian_note: "Radian mode.",
      timed_available: true
   } as unknown as AssessmentShape);
   mocked.readCheckUnits.mockResolvedValue({
      units: [{ unit_id: "BC-UNIT-01", items: 8, covered_skills: 8, unit_skills: 40, available: true, title: "Limits and Continuity" }]
   });
   mocked.readUnfinished.mockResolvedValue({
      unfinished: [{ id: "MOCK-1", mode: "mock", sub_mode: null, started_at: "2027-01-04T09:00:00", parts_closed: 1, parts_total: 4 }]
   });
   mocked.readFrqUnits.mockResolvedValue({ units: [] });
   mocked.readCheckpoints.mockRejectedValue(new Error("offline"));

   const container = inPage(<AssessmentRoute format={format} onChangeFormat={vi.fn()} />);

   await screen.findByTestId("resume-list");
   await settle();

   if (format === "drill") {
      fireEvent.click(screen.getByRole("radio", { name: /Section I, Part A/ }));
   }

   return container;
}

function sseResponse(frames: string[], keepsOpen = false) {
   const encoder = new TextEncoder();
   const body = new ReadableStream<Uint8Array>({
      start(controller) {
         for (const text of frames) {
            controller.enqueue(encoder.encode(text));
         }

         if (!keepsOpen) {
            controller.close();
         }
      }
   });

   return { ok: true, status: 200, body, json: async () => ({}) } as unknown as Response;
}

async function tutorPanel(answer: () => Promise<Response>, question: string) {
   mocked.openAgentTurnStream.mockImplementation(answer);

   const { container } = render(<TutorHarness screen={UNCHECKED_ITEM} />);

   fireEvent.click(screen.getByRole("button", { name: "Ask, Ctrl+/" }));
   fireEvent.change(screen.getByLabelText("Message to the tutor"), { target: { value: question } });
   fireEvent.click(screen.getByRole("button", { name: "Send" }));
   await settle();
   await settle();

   return container;
}

/* The live tutor: the panel on an unchecked item with a reply, the wait before the first text, no
   connection, and the Ask button on a timed part. */
const TUTOR_SCREENS: Screen[] = [
   {
      name: "tutor panel, a reply on an unchecked item",
      mount: async () => {
         const container = await tutorPanel(
            async () =>
               sseResponse([
                  frame("start", { conversation_id: "ACV-1", turn_id: "ATN-1", screen_line: "", can_see: [] }),
                  frame("text", { delta: "What does \\(0/0\\) tell you about the form of this limit?" }),
                  frame("end", { turn_id: "ATN-1", outcome: "complete", turns_on_item: 1, turns_in_conversation: 1 })
               ]),
            "I plugged in 3 and got 0/0."
         );

         await waitFor(() => expect(screen.getByTestId("agent-status").textContent).toContain("tell you about the form"));

         return container;
      }
   },
   {
      name: "tutor panel, writing a reply",
      mount: async () => {
         const container = await tutorPanel(async () => sseResponse([], true), "Where do I start?");

         await screen.findByText("Writing a reply");

         return container;
      }
   },
   {
      name: "tutor panel, no connection",
      mount: async () => {
         const container = await tutorPanel(() => Promise.reject(new TypeError("Failed to fetch")), "Are you there?");

         await screen.findByText(/No connection to the tutor/);

         return container;
      }
   },
   {
      name: "tutor, the Ask button on a timed part",
      mount: async () => render(<TutorHarness screen={{ kind: "assessments", format: "mock", timed: true }} />).container
   }
];

export function tutorFigure(spec: TutorFigureSpec, revealed: number, finished: boolean) {
   return inPage(
      <aside className="agent-panel">
         <div className="agent-reply">
            <TutorFigure spec={spec} revealed={revealed} finished={finished} reducedMotion={false} />
         </div>
      </aside>
   );
}

/* The tutor's figure in a reply: a finished graph in every role with arrowheads, a region above the
   axis and one below it, and the last step fading the constructed marks; a finished table with a
   highlighted row faded, an error cell and a highlighted column; and a figure still being built,
   with only Show all under it. */
/* A practice item with the tutor's marks over it, finished: every role and kind on the stem and the
   graph, and a table row and cell. */
function markedItem(item: ServedItem, marks: TutorMarksSpec) {
   return inPage(
      <>
         <Item
            item={item}
            onAnswerChange={vi.fn()}
            answerUnavailable={false}
            onAnswerUnavailable={vi.fn()}
            selectedOptionId={null}
            onOptionChange={vi.fn()}
            confidence={null}
            onConfidenceChange={vi.fn()}
            selfExplanation=""
            onSelfExplanationChange={vi.fn()}
            onCommit={vi.fn()}
            awaitingConfidence={false}
         />
         <PageMarks spec={marks} revealed={marks.steps.length} />
      </>
   );
}

/* The tutor's art board holding two finished figures, on the first of them: floating, minimized to
   its bar, and docked under the top bar as it is under 900 px. */
export function artBoard(mode: BoardMode, isNarrow: boolean, current = 0) {
   const figures = [SECANT_TO_TANGENT, TRIANGLE_DIAGRAM].map((spec, index) => ({ turnId: `reply-${index}`, spec, revealed: spec.steps.length, finished: true }));

   return inPage(
      <ArtBoard
         figures={figures}
         current={current}
         mode={mode}
         isNarrow={isNarrow}
         isPanelOpen={false}
         panel={{ current: null }}
         focusFigure={false}
         onFigureFocused={vi.fn()}
         onChoose={vi.fn()}
         onMinimize={vi.fn()}
         onRestore={vi.fn()}
         onClose={vi.fn()}
         onShowAll={vi.fn()}
      />
   );
}

const TUTOR_FIGURE_SCREENS: Screen[] = [
   { name: "tutor art board, floating, the first of two figures", mount: async () => artBoard("open", false) },
   { name: "tutor art board, minimized to its bar", mount: async () => artBoard("minimized", false) },
   { name: "tutor art board, docked under the top bar under 900 px", mount: async () => artBoard("open", true) },
   { name: "tutor marks on an item, every role and kind, finished", mount: async () => markedItem(servedItem(), EVERY_ROLE_MARKS) },
   { name: "tutor marks on an item's table, finished", mount: async () => markedItem(servedItem({ figure_spec: TABLE_FIGURE }), TABLE_MARKS) },
   { name: "tutor figure, every role, finished", mount: async () => tutorFigure(EVERY_ROLE_FIGURE, EVERY_ROLE_FIGURE.steps.length, true) },
   { name: "tutor figure, a table with its highlights, finished", mount: async () => tutorFigure(TABLE_OF_VALUES, TABLE_OF_VALUES.steps.length, true) },
   { name: "tutor figure, being built", mount: async () => tutorFigure(SECANT_TO_TANGENT, 2, false) },
   { name: "tutor figure, a table with labelled cells, finished", mount: async () => tutorFigure(LABELLED_TABLE, LABELLED_TABLE.steps.length, true) },
   {
      name: "tutor panel, a reply that drew a figure",
      mount: async () => {
         const steps = SECANT_TO_TANGENT.steps.map((step) => frame("figure_step", { figure: SECANT_TO_TANGENT.id, step: step.id }));
         const container = await tutorPanel(
            async () =>
               sseResponse([
                  frame("start", { conversation_id: "ACV-1", turn_id: "ATN-1", screen_line: "", can_see: [] }),
                  frame("figure_pending", {}),
                  frame("figure", SECANT_TO_TANGENT),
                  ...steps,
                  frame("text", { delta: "The tangent touches the curve at \\(P\\)." }),
                  frame("end", { turn_id: "ATN-1", outcome: "complete", turns_on_item: 1, turns_in_conversation: 1 })
               ]),
            "Can you draw the tangent?"
         );

         await waitFor(() => expect(screen.getByTestId("agent-status").textContent).toContain("Figure: Secant to tangent."));

         return container;
      }
   },
   {
      name: "tutor panel, a figure while it builds",
      mount: async () => {
         const container = await tutorPanel(
            async () =>
               sseResponse(
                  [
                     frame("start", { conversation_id: "ACV-1", turn_id: "ATN-1", screen_line: "", can_see: [] }),
                     frame("text", { delta: "Look at the curve first. " }),
                     frame("figure", SECANT_TO_TANGENT),
                     frame("figure_step", { figure: SECANT_TO_TANGENT.id, step: SECANT_TO_TANGENT.steps[0].id })
                  ],
                  true
               ),
            "Can you draw the tangent?"
         );

         await screen.findByTestId("tutor-figure");

         return container;
      }
   },
   {
      name: "tutor panel, a reply that marked the page",
      mount: async () => {
         const steps = ITEM_MARKS.steps.map((step) => frame("figure_step", { figure: ITEM_MARKS.id, step: step.id }));
         const container = await tutorPanel(
            async () =>
               sseResponse([
                  frame("start", { conversation_id: "ACV-1", turn_id: "ATN-1", screen_line: "", can_see: [] }),
                  frame("marks", ITEM_MARKS),
                  ...steps,
                  frame("text", { delta: "The phrase and the point are marked on the page." }),
                  frame("end", { turn_id: "ATN-1", outcome: "complete", turns_on_item: 1, turns_in_conversation: 1 })
               ]),
            "Where should I look?"
         );

         await waitFor(() => expect(screen.getByTestId("agent-status").textContent).toContain("Marks on the page:"));

         return container;
      }
   }
];

export const SCREENS: Screen[] = [
   ...LESSON_SCREENS,
   {
      name: "app shell with the token notice",
      mount: async () => {
         mocked.readMe.mockRejectedValue(new Error("offline"));
         mocked.readProgress.mockRejectedValue(new Error("offline"));

         const { container } = render(<App />);

         await settle();

         return container;
      }
   },
   ...(["ready", "inProgress", "empty", "longGap"] as HomeScreenStatus[]).map((status) => ({
      name: `home, ${status}`,
      mount: async () => homeScreen(status)
   })),
   { name: "account, sign-up", mount: () => accountScreen({ user_exists: false }, "Create account") },
   {
      name: "account, sign-in refused",
      mount: async () => {
         mocked.signIn.mockRejectedValue(serverRefusal("username or password is incorrect"));

         const container = await accountScreen({ user_exists: true }, "Sign in");

         fireEvent.click(screen.getByRole("button", { name: "Sign in" }));
         await screen.findByRole("alert");

         return container;
      }
   },
   {
      name: "account, reset for an account with no password",
      mount: () => accountScreen({ user_exists: true, needs_password: true }, "Reset password")
   },
   {
      name: "account, recovery code shown once",
      mount: async () => {
         mocked.signUp.mockResolvedValue({
            user: { id: "USR-1", display_name: "student", exam_date: "2027-05-10", purge_after: "2027-06-09" },
            seeded_skill_states: 0,
            recovery_code: "RC-shown-once"
         });

         const container = await accountScreen({ user_exists: false }, "Create account");

         fireEvent.click(screen.getByRole("button", { name: "Create account" }));

         const acknowledgeButton = await screen.findByRole("button", { name: "I have saved it" });

         /* The screen focuses this button, and the contrast eval reads a focused element's offset
            outline as a border on the button's own fill, which it never touches. The button is
            drawn unfocused here, as every other catalogued primary button is. */
         await waitFor(() => expect(document.activeElement).toBe(acknowledgeButton));
         act(() => acknowledgeButton.blur());

         return container;
      }
   },
   {
      name: "session item at completion, with a figure, the answer field focused",
      mount: async () => {
         mocked.openSession.mockResolvedValue(SESSION);
         mocked.readNextItem.mockResolvedValue({ item: servedItem() });

         const container = inPage(<SessionScreen resumeSessionId={null} />);

         await screen.findByTestId("item");

         /* MathLive makes its host focusable; its stand-in here does not, so the fixture does. */
         const field = container.querySelector("math-field") as HTMLElement;

         field.tabIndex = 0;
         field.focus();

         return container;
      }
   },
   {
      name: "session item with two items still to come, the set's progress drawn",
      mount: async () => {
         const inProgress: SessionPayload = {
            ...SESSION,
            queue: { ...SESSION.queue, forecasts: { "BC-ARCH-0301": 3 } },
            remaining: [servedItem(), servedItem({ id: "ITM-2" })] as SessionPayload["remaining"]
         };

         mocked.openSession.mockResolvedValue(inProgress);
         mocked.readSession.mockResolvedValue(inProgress);
         mocked.readNextItem.mockResolvedValue({ item: servedItem() });

         const container = inPage(<SessionScreen resumeSessionId={null} />);

         await screen.findByTestId("set-progress");

         return container;
      }
   },
   {
      name: "session item on a calculator question, with Desmos open",
      mount: async () => {
         mocked.openSession.mockResolvedValue(SESSION);
         mocked.readNextItem.mockResolvedValue({ item: servedItem({ figure_spec: null }) });

         const container = inPage(<SessionScreen resumeSessionId={null} />);

         fireEvent.click(await screen.findByRole("button", { name: "Open Desmos" }));

         return container;
      }
   },
   ...(["guess", "unsure", "confident"] as const).map((word) => ({
      name: `session item at completion, the confidence dialog open with ${word} chosen`,
      mount: async () => {
         mocked.openSession.mockResolvedValue(SESSION);
         mocked.readNextItem.mockResolvedValue({ item: servedItem({ figure_spec: null, format: "mcq", requires_choice: true, options: [{ id: "A", label: "2x" }, { id: "B", label: "x" }] }) });
         mocked.submitAttempt.mockReturnValue(new Promise(() => undefined));

         const container = inPage(<SessionScreen resumeSessionId={null} />);

         await screen.findByTestId("item");
         fireEvent.click(screen.getByRole("radio", { name: "2x" }));
         fireEvent.click(screen.getByRole("button", { name: "Check my answer" }));

         const chosen = await screen.findByRole("radio", { name: word });

         fireEvent.click(chosen);
         chosen.focus();

         return container;
      }
   })),
   {
      name: "onboarding, diagnostic introduction",
      mount: async () => inPage(<DiagnosticIntro reason="first_login" onStart={vi.fn()} />)
   },
   {
      name: "onboarding, diagnostic question answered",
      mount: async () =>
         inPage(
            <DiagnosticItem
               item={{ ...servedItem({ figure_spec: null, served_steps: null, stage: "unsupported" }), diagnostic_position: 6, diagnostic_cap: 30 }}
               state="answered"
               answerUnavailable={false}
               onAnswerChange={vi.fn()}
               onAnswerUnavailable={vi.fn()}
               onCheck={vi.fn()}
               onNotLearned={vi.fn()}
               onSkipUnit={vi.fn()}
            />
         )
   },
   {
      name: "onboarding, diagnostic question, confirming a unit skip",
      mount: async () => {
         const container = inPage(
            <DiagnosticItem
               item={{ ...servedItem({ figure_spec: null, served_steps: null, stage: "unsupported" }), diagnostic_position: 6, diagnostic_cap: 30 }}
               state="unanswered"
               answerUnavailable={false}
               onAnswerChange={vi.fn()}
               onAnswerUnavailable={vi.fn()}
               onCheck={vi.fn()}
               onNotLearned={vi.fn()}
               onSkipUnit={vi.fn()}
            />
         );

         fireEvent.click(screen.getByRole("button", { name: "Skip this unit" }));

         return container;
      }
   },
   {
      name: "onboarding, diagnostic result",
      mount: async () =>
         inPage(
            <DiagnosticResultView
               units={[
                  { unit: "BC-UNIT-01", title: "Limits and Continuity", state: "fluent" },
                  { unit: "BC-UNIT-02", title: "Differentiation: Definition and Fundamental Properties", state: "partial" }
               ]}
               onFinished={vi.fn()}
            />
         )
   },
   {
      name: "session item at example, multiple choice with a table",
      mount: async () => {
         mocked.openSession.mockResolvedValue(SESSION);
         mocked.readNextItem.mockResolvedValue({
            item: servedItem({
               stage: "unsupported",
               format: "mcq",
               figure_spec: TABLE_FIGURE,
               served_steps: null,
               options: [
                  { id: "A", mathjson: ["Multiply", 2, "x"] },
                  { id: "B", label: "\\(\\sqrt{x}\\)" }
               ]
            })
         });

         const container = inPage(<SessionScreen resumeSessionId={null} />);

         await screen.findByTestId("item");

         const firstOption = screen.getAllByRole("radio")[0];

         fireEvent.click(firstOption);
         act(() => firstOption.focus());

         return container;
      }
   },
   { name: "session feedback, step marks", mount: () => sessionFeedback("completion") },
   { name: "session feedback, elaborated", mount: () => sessionFeedback("unsupported") },
   {
      name: "review with provisional points",
      mount: async () =>
         inPage(
            <ReviewScreen
               comingBack={[
                  {
                     item_id: "ITM-40",
                     attempt_id: "ATT-40",
                     label: "Quotient rule",
                     lane: "hypercorrection",
                     confidence: "confident",
                     corrected_on: "2027-01-04",
                     returns_on: "2027-01-05",
                     days_until: 0
                  }
               ]}
               errorNotes={[{ attempt_id: "ATT-40", session_id: "SES-8", note: "Wrong order.", written_on: "2027-01-04", label: "Quotient rule" }]}
               provisionalPoints={[
                  { grading_id: "G-1", attempt_id: "ATT-1", label: "Question 1", point_label: "Answer", reason: "Two readings", disputed: false },
                  { grading_id: "G-2", attempt_id: "ATT-1", label: "Question 1", point_label: "Setup", reason: "Two readings", disputed: true }
               ]}
               onSaveNote={vi.fn()}
               onAskForReread={vi.fn()}
            />
         )
   },
   {
      name: "progress map and curve",
      mount: async () =>
         inPage(
            <section className="card">
               <MasteryMap map={MASTERY} />
               <CalibrationCurve calibration={CALIBRATION} />
            </section>
         )
   },
   {
      name: "progress representation matrix, one translation attempted",
      mount: async () =>
         inPage(
            <section className="card">
               <RepresentationMatrix
                  matrix={{
                     representations: [
                        { id: "BC-REP-01", name: "Symbolic (analytical) expression" },
                        { id: "BC-REP-02", name: "Graph" }
                     ],
                     cells: [
                        { source: "BC-REP-01", target: "BC-REP-02", attempts: 3, correct: 2 },
                        { source: "BC-REP-02", target: "BC-REP-01", attempts: 0, correct: 0 }
                     ],
                     translation_attempts: 3,
                     practice_attempts: 12
                  }}
               />
            </section>
         )
   },
   {
      name: "free response read-back and grading",
      mount: async () =>
         inPage(
            <section className="card">
               <ReadBackView readBack={READ_BACK} />
               <ReadBackEditor readBack={READ_BACK} onChange={vi.fn()} />
               <GradingView gradings={gradings()} onAskForReread={vi.fn()} rereadAskedFor={["G-2"]} />
            </section>
         )
   },
   { name: "free response photo read back for confirmation", mount: photographedReadBack },
   {
      name: "timed part without a calculator, worked question and open menu",
      mount: () => partRunner(noCalculatorPart({ questions: [workedQuestion(), multipleChoiceQuestion(2)] }))
   },
   {
      name: "timed part with the graphing panel open and plotting",
      mount: async () => {
         const container = await partRunner(calculatorPart());

         fireEvent.click(screen.getByRole("button", { name: "Open graphing panel" }));
         fireEvent.change(screen.getByLabelText("y ="), { target: { value: "sin(x)" } });
         fireEvent.click(screen.getByRole("button", { name: "Submit part" }));

         return container;
      }
   },
   ...(["study", "providers", "budgets", "accessibility", "operator", "data", "tutor"] as SettingsTab[]).map((tab) => ({
      name: `settings, ${tab}`,
      mount: async () => settingsPage(tab)
   })),
   {
      name: "settings, the password prompt",
      mount: async () =>
         inPage(<ReauthPromptView working={false} feedback={{ kind: "refused", detail: "the password is incorrect" }} onSubmit={vi.fn()} onCancel={vi.fn()} />)
   },
   {
      name: "app shell, signed in with the account menu open",
      mount: async () => {
         mocked.readAuthStatus.mockResolvedValue({ user_exists: true });
         mocked.readMe.mockResolvedValue(ME);
         mocked.readProgress.mockRejectedValue(new Error("offline"));

         const { container } = render(<App />);

         fireEvent.click(await screen.findByRole("button", { name: "Account and settings" }));

         return container;
      }
   },
   { name: "home, ready with the pace verdict", mount: async () => homeScreen("ready", { verdict: "on_pace", statement: "On pace." }) },
   { name: "home, ready and behind pace", mount: async () => homeScreen("ready", { verdict: "behind", statement: "Behind pace." }) },
   { name: "progress, the pace statement", mount: async () => inPage(<PaceStatement pace={PACE} />) },
   ...(["unit", "drill", "mock"] as const).map((format) => ({
      name: `assessments, ${format} setup`,
      mount: async () => assessmentsHub(format)
   })),
   {
      name: "assessments, a free-response unit check",
      mount: async () =>
         inPage(
            <FrqUnitCheck
               check={{ session_id: "SES-F", mode: "frq_unit_check", unit_id: "BC-UNIT-05", questions: [FRQ_QUESTION] }}
               onLeave={vi.fn()}
            />
         )
   },
   {
      name: "lessons tab",
      mount: async () => {
         mocked.readLibrary.mockResolvedValue(LESSONS_LIBRARY);

         const container = inPage(<LessonsRoute onOpenLesson={vi.fn()} />);

         await screen.findByTestId("lesson-library");
         fireEvent.click(screen.getAllByRole("button", { pressed: false })[0]);

         return container;
      }
   },
   ...(["notes", "provisional"] as const).map((initialTab) => ({
      name: `review, ${initialTab} tab`,
      mount: async () =>
         inPage(
            <ReviewScreen
               initialTab={initialTab}
               comingBack={[]}
               errorNotes={[{ attempt_id: "ATT-40", session_id: "SES-8", note: "Wrong order.", written_on: "2027-01-04", label: "Quotient rule" }]}
               provisionalPoints={[
                  { grading_id: "G-1", attempt_id: "ATT-1", label: "Question 1", point_label: "Answer", reason: "Two readings", disputed: false },
                  { grading_id: "G-2", attempt_id: "ATT-1", label: "Question 1", point_label: "Setup", reason: "Two readings", disputed: true }
               ]}
               onSaveNote={vi.fn()}
               onAskForReread={vi.fn()}
            />
         )
   })),
   {
      name: "account page",
      mount: async () => {
         mocked.readMe.mockResolvedValue(ME);

         const container = inPage(<AccountPage onRenamed={vi.fn()} onSignOut={vi.fn()} />);

         await screen.findByDisplayValue("student");

         return container;
      }
   },
   { name: "a screen still loading", mount: async () => inPage(<Loading testId="catalogue-loading" />) },
   {
      name: "an AI call notice",
      mount: async () =>
         inPage(
            <div className="ai-notices">
               <AiNoticeToast
                  notice={AI_NOTICE}
                  visibleMilliseconds={60000}
                  onDismiss={vi.fn()}
               />
            </div>
         )
   },
   {
      name: "session feedback, the lesson opened at the error's block",
      mount: async () => {
         mocked.readLesson.mockResolvedValue({ ...LESSON, state: null });

         const feedback = feedbackFor("unsupported");
         const container = inPage(
            <ElaboratedPanel
               elaborated={feedback.elaborated}
               sentence={feedback.sentence}
               lessonLink={{ lesson_id: LESSON.id, version: 1, anchor: LESSON.sections[0].id }}
            />
         );

         fireEvent.click(screen.getByTestId("read-error-part"));
         await screen.findByTestId("error-lesson");
         await settle();

         return container;
      }
   },
   ...TUTOR_SCREENS,
   ...TUTOR_FIGURE_SCREENS
];
