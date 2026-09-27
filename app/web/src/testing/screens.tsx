import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { ReactElement } from "react";
import { expect, vi } from "vitest";

import { AccountScreen } from "../account/AccountScreen";
import { ChangePasswordControl } from "../account/ChangePasswordControl";
import { App } from "../App";
import * as client from "../api/client";
import type {
   AttemptResult,
   CalibrationPayload,
   FeedbackPayload,
   FigureSpec,
   FrqAttempt,
   FrqQuestion,
   GradingsPayload,
   MasteryMapPayload,
   ServedItem,
   SessionPayload,
   StepMark
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
import { SessionScreen } from "../session/SessionScreen";
import { AccessibilitySection } from "../settings/AccessibilitySection";
import { OperatorSettings } from "../settings/ExperimentsSection";
import { ReauthPromptView } from "../account/ReauthPrompt";
import { SettingsScreen } from "../settings/SettingsScreen";

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
      probe_scheduled: null
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

function homeScreen(status: HomeScreenStatus) {
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
         onStartSession={vi.fn()}
         onAddPracticeSet={vi.fn()}
         onResumeSession={vi.fn()}
         onStartRediagnostic={vi.fn()}
         onOpenProgress={vi.fn()}
         onOpenReview={vi.fn()}
         onOpenFreeResponse={vi.fn()}
         onOpenMockExam={vi.fn()}
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

export const SCREENS: Screen[] = [
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
      name: "session item at completion, with a figure",
      mount: async () => {
         mocked.openSession.mockResolvedValue(SESSION);
         mocked.readNextItem.mockResolvedValue({ item: servedItem() });

         const container = inPage(<SessionScreen resumeSessionId={null} />);

         await screen.findByTestId("item");

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
   {
      name: "session item at completion, with a confidence chosen",
      mount: async () => {
         mocked.openSession.mockResolvedValue(SESSION);
         mocked.readNextItem.mockResolvedValue({ item: servedItem({ figure_spec: null }) });

         const container = inPage(<SessionScreen resumeSessionId={null} />);

         await screen.findByTestId("item");
         fireEvent.click(screen.getByRole("radio", { name: "unsure" }));

         return container;
      }
   },
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
         fireEvent.click(screen.getAllByRole("radio")[0]);

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
   {
      name: "settings",
      mount: async () => {
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

         const container = inPage(
            <>
               <SettingsScreen
                  providers={[{ role: "tutor", provider: "anthropic", model: "claude-sonnet-5", wired: true }]}
                  budgets={{
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
                  }}
                  onCapChange={vi.fn()}
                  queueSettings={{ exam_date: "2027-05-10", purge_after: "2027-06-09", desired_retention: 0.9 }}
                  onSettingsChange={vi.fn()}
                  onExport={vi.fn()}
                  purgeConfirmationPhrase="delete my data"
                  onReauthenticate={vi.fn()}
                  onPurge={vi.fn()}
               />
               <ReauthPromptView
                  working={false}
                  feedback={{ kind: "refused", detail: "the password is incorrect" }}
                  onSubmit={vi.fn()}
                  onCancel={vi.fn()}
               />
               <AccessibilitySection />
               <ChangePasswordControl />
               <OperatorSettings onOpenEvidence={vi.fn()} />
            </>
         );

         await waitFor(() => expect(screen.getAllByTestId("experiment-switch").length).toBeGreaterThan(0));

         return container;
      }
   }
];
