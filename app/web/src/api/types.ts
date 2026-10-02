/* The shapes the FastAPI layer returns, transcribed from the route and service modules each
   comment names. Nothing here is invented: a field absent from those modules is absent here, and
   client.test.ts scans the Python source so a field added or dropped on either side fails. */

export type FadingStage = "example" | "completion" | "unsupported";

export type ServedFormat = "mcq" | "short_answer";

export type Confidence = "guess" | "unsure" | "confident";

/* app/runtime/bank.py STUDENT_OPTION_FIELDS. is_key and error_path are withheld by the server.
   value carries the option's raw MathJSON, a bare number or symbol counting as the simplest
   case, so its type is unknown rather than string. */
export interface ServedOption {
   id: string;
   value?: unknown;
   label?: string;
   mathjson?: unknown;
}

/* app/runtime/bank.py served_steps: one worked solution step, numbered from 1. */
export interface ServedStep {
   index: number;
   text: string;
}

/* app/generation/kit.py figure, table_figure, label, point_mark and segment_mark, as
   prompts/generator/figure_spec_v1.md describes them. A point is [x, y] in the figure's own
   coordinates, y up. */
export type FigurePoint = [number, number];

export type GraphFigureKind =
   | "function_graph"
   | "region"
   | "parametric_curve"
   | "polar_curve"
   | "vector_diagram"
   | "number_line"
   | "slope_field"
   | "geometric_diagram";

export type FigureMark =
   | { type: "point" | "open_point"; at: FigurePoint }
   | { type: "segment"; from: FigurePoint; to: FigurePoint; style: "solid" | "dashed" };

export type FigureLabel = { text: string; anchor: FigurePoint; placement: "inside" };

export type GraphFigureSpec = {
   kind: GraphFigureKind;
   domain: [number, number];
   range: [number, number];
   curves: Array<{ segments: FigurePoint[][]; style: string }>;
   fills: Array<{ points: FigurePoint[] }>;
   marks: FigureMark[];
   labels: FigureLabel[];
   gridlines: boolean;
   axis_titles: string[];
   alt: string;
};

export type TableFigureSpec = {
   kind: "table";
   columns: string[];
   rows: string[][];
   labels: FigureLabel[];
   alt: string;
};

export type FigureSpec = GraphFigureSpec | TableFigureSpec;

/* The live tutor's figure as the server compiles it (docs/agent/drawing-build-plan.md, "The render
   spec contract"). Coordinates are world coordinates, y up, mapped into view with window and view
   the way the server laid them out; a label's offset is in view units. Nothing here names a colour,
   a class or a URL: a primitive carries a role and the client draws the role. */
export type TutorFigureKind = "graph" | "diagram" | "number_line" | "table";

export type TutorFigureRole = "given" | "constructed" | "highlight" | "error";

export type TutorFigureStrokeStyle = "solid" | "dashed" | "dotted";

export type TutorFigureStrokeWeight = "thin" | "regular" | "bold";

export type TutorFigureArrow = "none" | "end" | "start" | "both";

export type TutorFigureFill = "none" | "region" | "region_below";

export type TutorFigureAlign = "start" | "middle" | "end";

export interface TutorFigurePrimitiveBase {
   step: string;
   element: string;
   role: TutorFigureRole;
   faded_at: string | null;
   erased_at: string | null;
}

export interface TutorFigurePath extends TutorFigurePrimitiveBase {
   type: "path";
   points: FigurePoint[];
   closed: boolean;
   fill: TutorFigureFill;
   style: TutorFigureStrokeStyle;
   weight: TutorFigureStrokeWeight;
   arrow: TutorFigureArrow;
   highlighter: boolean;
}

export interface TutorFigureDot extends TutorFigurePrimitiveBase {
   type: "dot";
   at: FigurePoint;
   open: boolean;
}

export interface TutorFigureLabel extends TutorFigurePrimitiveBase {
   type: "label";
   at: FigurePoint;
   offset: FigurePoint;
   align: TutorFigureAlign;
   text: string;
}

export interface TutorFigureCell extends TutorFigurePrimitiveBase {
   type: "cell";
   row: number | null;
   column: number | null;
   text?: string;
}

export type TutorFigurePrimitive = TutorFigurePath | TutorFigureDot | TutorFigureLabel | TutorFigureCell;

export interface TutorFigureStep {
   id: string;
   caption: string;
}

/* Marks the tutor draws over the page itself (docs/agent/drawing-build-plan.md, "The marks
   contract"). Every mark names an anchor the screen declared with data-agent-anchor; the client
   finds the element and draws over it wherever it is laid out. A target's unused fields are null. */
export type TutorMarkKind =
   | "ring"
   | "underline"
   | "highlight"
   | "strike"
   | "bracket"
   | "note"
   | "arrow"
   | "point"
   | "segment"
   | "line"
   | "vline"
   | "hline";

export type TutorMarkSide = "left" | "right" | "above" | "below";

export interface TutorMarkTarget {
   anchor: string;
   quote: string | null;
   at: FigurePoint | null;
   row: number | null;
   column: number | null;
   cell: [number, number] | null;
}

export interface TutorMarkStroke {
   style: TutorFigureStrokeStyle;
   weight: TutorFigureStrokeWeight;
   arrow: TutorFigureArrow;
   highlighter: boolean;
}

export interface TutorMark {
   step: string;
   element: string;
   role: TutorFigureRole;
   stroke: TutorMarkStroke;
   faded_at: string | null;
   erased_at: string | null;
   kind: TutorMarkKind;
   target?: TutorMarkTarget | null;
   from?: TutorMarkTarget | null;
   to?: TutorMarkTarget | null;
   text?: string | null;
   side?: TutorMarkSide | null;
   at?: FigurePoint | null;
   open?: boolean | null;
   points?: [FigurePoint, FigurePoint] | null;
}

export interface TutorMarksSpec {
   id: string;
   description: string;
   steps: TutorFigureStep[];
   marks: TutorMark[];
}

export interface TutorFigureSpec {
   id: string;
   kind: TutorFigureKind;
   title: string;
   description: string;
   window: { x: [number, number]; y: [number, number] } | null;
   view: { width: number; height: number; padding: number } | null;
   axes: { x: string; y: string } | null;
   grid: boolean;
   equal_scale: boolean;
   steps: TutorFigureStep[];
   columns: string[] | null;
   rows: string[][] | null;
   primitives: TutorFigurePrimitive[];
}

/* A queue slot as sessions.queue stores it: app/runtime/bank.py _as_item_dict plus the fields
   app/engine/select.py dress_item writes onto it. */
export interface QueueSlot {
   id: string;
   archetype_id: string;
   variant_id: string | null;
   snapshot_id: string | null;
   parameter_draw: unknown;
   stem: string;
   figure_spec: FigureSpec | null;
   options: ServedOption[] | null;
   calculator_status: string | null;
   representation: string | null;
   difficulty_settings: unknown;
   skills: string[] | null;
   status: string;
   requires_choice?: boolean;
   stage: FadingStage;
   format: ServedFormat;
   is_probe: boolean;
   /* app/session/build.py: the productive-failure opener, first ordinary item of block 2. */
   is_opener?: boolean;
   opener_concept?: string;
}

/* app/session/build.py LessonPlacement writes these onto a block 2 item after dress_item: kind
   "item", the lesson that went before it, or the link to a lesson deferred or not needed (15
   Session assembly). A type alias, since the item's interface lists what dress_item writes. */
export interface LessonMarks {
   kind?: "item";
   preceded_by_lesson_id?: string;
   preceded_by_lesson_version?: number;
   lesson_link?: { lesson_id: string; version: number };
}

export type MarkedQueueSlot = QueueSlot & LessonMarks;

/* GET /sessions/{id}/next: the slot plus app/session/service.py served_item's steps and the
   prompt app/api/routes/sessions.py read_next_item attaches at stage example. */
export interface ServedItem extends QueueSlot {
   served_steps: ServedStep[] | null;
   self_explanation_prompt: string | null;
}

/* A lesson or refresher slot of block 1 or block 2 (app/session/build.py LessonPlacement,
   app/lessons/refresh.py refresher_entry). GET /sessions/{id}/next serves it with the stored
   record body as lesson and the concept's name for the top bar. */
export interface SessionLessonSlot {
   kind: "lesson" | "refresher";
   lesson_id: string;
   version: number;
   band: LessonBand;
   reason: LessonReason;
   concept_id: string;
   before_item_id: string;
   minutes: number;
   plan: LessonPlan;
}

export interface ServedLesson extends SessionLessonSlot {
   lesson: LessonRecord | null;
   concept_name: string | null;
}

export type ServedEntry = (ServedItem & LessonMarks) | ServedLesson;

export function isServedLesson(entry: ServedEntry): entry is ServedLesson {
   return entry.kind === "lesson" || entry.kind === "refresher";
}

/* app/session/service.py queue_payload. Block 4 holds the ids of items corrected today, and
   forecasts maps an archetype id to its forecast minutes. */
export interface SessionQueue {
   block1: Array<MarkedQueueSlot | SessionLessonSlot>;
   block2: Array<MarkedQueueSlot | SessionLessonSlot>;
   block3: QueueSlot[];
   block4: Array<string | { kind: "read_again"; lesson_id: string; version: number }>;
   forecasts: Record<string, number>;
   coverage_gaps: string[];
   interleaving_satisfied: boolean;
   interleaving_shortfalls: Array<[number, string]>;
}

/* app/api/routes/sessions.py session_payload. */
export interface SessionPayload {
   id: string;
   mode: string;
   sub_mode: string | null;
   started_at: string | null;
   ended_at: string | null;
   updates_mastery: boolean;
   snapshot_id: string | null;
   queue: SessionQueue;
   remaining: Array<MarkedQueueSlot | SessionLessonSlot>;
}

/* app/api/routes/sessions.py submit_attempt. */
export interface AttemptResult {
   id: string;
   item_id: string;
   correct: boolean | null;
   confidence: Confidence | null;
   served_stage: FadingStage;
   format: ServedFormat;
   p_split: number | null;
   p_compensatory: number | null;
}

/* app/feedback/render.py as_dict step_marks, numbered 1-based as served_steps numbers them. A step
   the stage showed carries given true and no verdict; the blank carries the attempt's verdict. */
export interface StepMark {
   index: number;
   text: string;
   given: boolean;
   correct: boolean | null;
}

/* app/feedback/render.py ElaboratedPayload.as_prompt_fields, plus error_id. */
export interface ElaboratedPayload {
   violated_step: string | null;
   observed_behavior: string | null;
   scoring_consequence: string | null;
   worked_solution: string | null;
   error_id: string | null;
}

/* app/feedback/render.py comparison_as_dict: an opener that missed, its attempt beside the worked
   solution under one line naming the gap. attempt is the response as it was stored. */
export interface ComparisonPayload {
   label: string;
   first_step: string;
   observed_behavior: string;
   attempt: Record<string, unknown>;
   worked_steps: Array<{ index: number; text: string }>;
   error_id: string | null;
}

/* app/feedback/render.py correct_answer: the key's MathJSON, or the label of a statement key or
   keyed option. It is sent only once a wrong answer is graded, and never for an opener. */
export interface CorrectAnswer {
   label: string | null;
   mathjson: unknown;
}

/* app/api/routes/sessions.py read_feedback: render.as_dict plus the two tutor fields. */
export interface FeedbackPayload {
   kind: string;
   stage: FadingStage;
   step_marks: StepMark[];
   elaborated: ElaboratedPayload | null;
   self_explanation_prompt: string | null;
   confidence: Confidence | null;
   comparison?: ComparisonPayload | null;
   correct_answer?: CorrectAnswer | null;
   /* A correct opener's first worked step, for the comparison the tutor would have drawn. */
   first_worked_step?: { index: number; text: string } | null;
   sentence: string | null;
   tutor_unavailable: boolean;
   /* 15 Diagnosis links: the concept lesson's block on the error the answer showed. */
   lesson_link?: FeedbackLessonLink | null;
}

export interface FeedbackLessonLink {
   lesson_id: string;
   version: number;
   anchor: string;
}

/* app/session/preview.py home_state. */
export type HomeState = "first_login" | "long_gap" | "queue";

/* app/session/preview.py queue_preview. session_in_progress never names a diagnostic session;
   diagnostic_in_progress does. */
export interface ProgressPayload {
   home_state: HomeState;
   days_since_last_session: number | null;
   diagnostic_in_progress: string | null;
   skills_due_for_review: number;
   frontier_skills: number;
   corrected_items_returning: number;
   forecast_minutes: number;
   due_today_skills: number;
   due_today_minutes: number;
   session_in_progress: string | null;
   focus: BlockFocus[];
}

export type FocusBlock = "review" | "learn" | "mixed";

/* app/session/preview.py block_focus. */
export interface BlockFocus {
   block: FocusBlock;
   items: number;
   skills: string[];
   more_skills: number;
   units: number[];
}

/* GET /sessions/{id}/next on a diagnostic session: app/session/diagnostic_session.py advance
   numbers the item and app/api/routes/sessions.py next_diagnostic_item withholds the steps. */
export interface DiagnosticServedItem extends ServedItem {
   diagnostic_position: number;
   diagnostic_cap: number;
}

export type DiagnosticUnitState = "not_started" | "partial" | "fluent" | "unresolved" | "not_probed";

/* app/session/diagnostic_session.py result_payload, one entry of its units list. */
export interface DiagnosticUnit {
   unit: string;
   title: string;
   state: DiagnosticUnitState;
}

/* app/session/diagnostic_session.py result_payload. */
export interface DiagnosticResult {
   session_id: string;
   finished: boolean;
   asked: number;
   cap: number;
   stop_reason: string | null;
   units: DiagnosticUnit[];
   unprobeable_units: string[];
}

/* app/progress/calibration.py calibration_view. Below minimum_rated_attempts the bins list is
   empty and available is false. */
export interface CalibrationBin {
   confidence: Confidence;
   attempts: number;
   correct: number;
   accuracy: number | null;
   interval_low: number | null;
   interval_high: number | null;
}

export interface CalibrationPayload {
   available: boolean;
   rated_attempts: number;
   minimum_rated_attempts: number;
   attempts_needed: number;
   window_days: number;
   window_start: string;
   window_end: string;
   bins: CalibrationBin[];
}

/* app/progress/mastery.py mastery_map, unit_payload and node_payload. A node's state is one of the
   five 08 names; the map carries no count or percentage. */
export type MasteryNodeState = "not_attempted" | "in_progress" | "mastered" | "fading" | "gap";

export interface MasteryNode {
   skill_id: string;
   name: string;
   state: MasteryNodeState;
   depth: number;
   assumed: boolean;
   last_success_on: string | null;
   days_since_success: number | null;
}

export interface MasteryUnit {
   unit_id: string;
   number: number;
   name: string;
   nodes: MasteryNode[];
}

/* app/progress/pace.py pace_verdict. A pace on mastering the exam's skills, never a predicted score. */
export type PaceVerdict = "complete" | "ahead" | "on_pace" | "behind" | "well_behind" | "too_early" | "exam_passed";

export interface PacePayload {
   as_of: string;
   verdict: PaceVerdict;
   statement: string;
   exam_date: string;
   days_to_exam: number;
   review_reserve_days: number;
   new_mastery_deadline: string;
   skills: { total: number; held: number; fading: number; assumed: number; remaining: number; remaining_weighted: number };
   rate: {
      window_start: string;
      window_days: number;
      earned_weighted: number;
      weekly: number;
      required_weekly: number;
      pace_ratio: number | null;
      projected_finish: string | null;
   };
   study_time: {
      window_start: string;
      window_days: number;
      active_days: number;
      timed_attempts: number;
      attempts: number;
      minutes: number | null;
      minutes_per_active_day: number | null;
      active_days_per_week: number;
      minutes_per_week: number | null;
   };
   evidence: {
      graded_attempts: number;
      practice_days: number;
      recent_accuracy: { correct: number; graded: number; days: number; value: number | null };
      retention_30_day: { correct: number; attempts: number; value: number | null; floor: number };
   };
   caveat: string;
}

export interface MasteryMapPayload {
   today: string;
   states: MasteryNodeState[];
   units: MasteryUnit[];
}

/* app/review/screen.py review_screen, coming_back_entry and error_notes. provisional_points is empty
   until P3's grader writes gradings; each entry then carries PROVISIONAL_POINT_KEYS. */
export type ReviewLane = "hypercorrection" | "requeue";

export interface ComingBackEntry {
   item_id: string;
   attempt_id: string | null;
   label: string;
   lane: ReviewLane;
   confidence: Confidence | null;
   corrected_on: string;
   returns_on: string;
   days_until: number;
}

export interface ErrorNoteEntry {
   attempt_id: string;
   session_id: string;
   note: string;
   written_on: string;
   label: string;
}

export interface ProvisionalPoint {
   grading_id: string;
   attempt_id: string;
   label: string;
   point_label: string;
   reason: string;
   disputed: boolean;
}

export interface ReviewPayload {
   today: string;
   coming_back: ComingBackEntry[];
   error_notes: ErrorNoteEntry[];
   grading_available: boolean;
   provisional_points: ProvisionalPoint[];
}

/* app/settings/preferences.py settings_view. */
export interface SettingsPayload {
   exam_date: string;
   purge_after: string | null;
   desired_retention: number;
}

/* app/settings/providers.py role_entry and unwired. */
export interface ProviderRole {
   role: string;
   provider: string | null;
   model: string | null;
   wired: boolean;
}

/* app/settings/providers.py providers_view. */
/* app/settings/providers.py providers_view: chains is each role group's fallback order and cooling
   every link on cooldown now (app/providers/router.py CooldownBoard.snapshot). */
export interface ProviderCooldown {
   role: string;
   link: string;
   until: string;
   because: string | null;
}

export interface ProvidersPayload {
   roles: ProviderRole[];
   chains: { tutor: string[]; grading: string[] };
   cooling: ProviderCooldown[];
}

/* app/settings/budgets.py role_view: caps_as_dict and USAGE_FIELDS spread between role and
   hard_stopped. */
export interface RoleBudget {
   role: string;
   cap_usd: number | null;
   cap_tokens: number | null;
   cost_usd: number;
   tokens_in: number;
   tokens_out: number;
   tokens_cached_read: number;
   tokens_cached_write: number;
   hard_stopped: boolean;
}

/* app/settings/budgets.py budgets_view. */
export interface BudgetsPayload {
   day: string;
   roles: RoleBudget[];
   month_to_date_usd: number;
}

/* app/progress/learning_metrics.py value. A value whose denominator is 0 carries value null, and a
   statistic that is not a ratio, such as a Brier score or a median, carries numerator null.
   external_checkpoint adds published_total and scored_by to each points value. */
export interface MetricValue {
   label: string;
   value: number | null;
   numerator: number | null;
   denominator: number;
   denominator_label: string;
   published_total?: number;
   scored_by?: string;
}

export interface MetricWindow {
   start: string;
   end: string;
}

export type MetricStatus = "measured" | "no_data";

/* app/progress/learning_metrics.py metric. */
export interface LearningMetric {
   key: string;
   name: string;
   status: MetricStatus;
   definition: string;
   window: MetricWindow | null;
   values: MetricValue[];
}

/* app/experiments/analysis.py comparison_view, arm_view. */
export interface ArmOutcomes {
   arm: string;
   outcomes: number;
   correct: number;
   accuracy: number | null;
}

/* app/experiments/analysis.py comparison_view. The interval is null until each arm holds
   minimum_outcomes_per_arm outcomes, and stated says which. */
export interface ExperimentComparison {
   name: string;
   control: ArmOutcomes;
   treatment: ArmOutcomes;
   difference: number | null;
   interval_low: number | null;
   interval_high: number | null;
   stated: boolean;
   minimum_outcomes_per_arm: number;
   guards: ComparisonGuards | null;
}

/* app/experiments/analysis.py tutor_profile_comparison: the calibration guard by arm, present on
   the tutor profile comparison and null on the others. */
export interface ComparisonGuards {
   calibration: Record<string, CalibrationBin[]>;
}

/* app/api/routes/evaluation.py read_metrics. */
export interface MetricsPayload {
   as_of: string;
   metrics: LearningMetric[];
   experiments: ExperimentComparison[];
}

/* app/progress/representations.py representation_matrix. cells holds one entry per conversion
   pair the taxonomy lists, so a source and target with no entry is not a translation. */
export interface Representation {
   id: string;
   name: string;
}

export interface RepresentationCell {
   source: string;
   target: string;
   attempts: number;
   correct: number;
}

export interface RepresentationMatrixPayload {
   representations: Representation[];
   cells: RepresentationCell[];
   translation_attempts: number;
   practice_attempts: number;
}

/* app/experiments/switches.py STATES. */
export type ExperimentState = "off" | "on" | "randomised";

/* app/experiments/switches.py switch_view. assigned_units maps each arm to the units assigned it. */
export interface ExperimentSwitch {
   name: string;
   description: string;
   unit: string;
   arms: string[];
   state: ExperimentState;
   randomised_from: string | null;
   assigned_units: Record<string, number>;
}

/* app/api/routes/evaluation.py read_experiments and set_experiment. */
export interface ExperimentsPayload {
   experiments: ExperimentSwitch[];
}

/* app/checkpoint/service.py availability. opens_on is null unless a finished checkpoint holds the
   next one back. */
export interface CheckpointAvailability {
   open_checkpoint_id: string | null;
   available: boolean;
   opens_on: string | null;
   forms_remaining: number;
   cadence_days: number;
}

/* app/checkpoint/forms.py section_plan. calculator is the exam-structure cell as written, such as
   "Required" or "Not permitted". */
export interface CheckpointPart {
   record_id: string;
   part: string;
   points: number;
}

export interface CheckpointQuestion {
   question: number;
   parts: CheckpointPart[];
}

export interface CheckpointSection {
   part: string;
   minutes: number;
   calculator: string;
   questions: CheckpointQuestion[];
}

/* app/checkpoint/service.py question_results. published_mean is null when no year's mean is
   published for the question, and published_mean_years names the years it was taken from. */
export interface CheckpointQuestionResult {
   question: number;
   earned: number;
   possible: number;
   published_mean: number | null;
   published_mean_years: number[];
}

/* app/checkpoint/service.py checkpoint_view. The form is named by reference only: it carries links
   to College Board's documents and never a question's text. */
export interface CheckpointView {
   id: string;
   form_year: number;
   started_at: string;
   finished_at: string | null;
   scored_by: string;
   free_response_url: string;
   scoring_guidelines_url: string;
   sections: CheckpointSection[];
   scores: Record<string, number>;
   questions: CheckpointQuestionResult[];
   total_earned: number;
   total_possible: number;
   published_total: number;
}

export interface ExpectedEffect {
   low: number;
   high: number;
}

/* app/api/routes/evaluation.py read_checkpoints. */
export interface CheckpointsPayload {
   availability: CheckpointAvailability;
   history: CheckpointView[];
   expected_effect: ExpectedEffect;
}

/* app/checkpoint/probe.py availability. */
export interface ProbeAvailability {
   open_administration_id: string | null;
   available: boolean;
   opens_on: string | null;
   items: number;
   cadence_days: number;
}

/* app/checkpoint/probe.py administration_view. */
export interface ProbeAdministration {
   id: string;
   probe_set: string;
   started_at: string;
   finished_at: string | null;
   answered: number;
   graded: number;
   correct: number;
   items: number;
}

/* app/api/routes/evaluation.py read_probe. */
export interface ProbePayload {
   availability: ProbeAvailability;
   history: ProbeAdministration[];
}

/* app/checkpoint/probe.py next_item: app/runtime/bank.py _as_item_dict plus the served format. A
   probe item carries no stage, no steps and no prompt. */
export interface ProbeServedItem {
   id: string;
   archetype_id: string;
   variant_id: string | null;
   snapshot_id: string | null;
   parameter_draw: unknown;
   stem: string;
   figure_spec: FigureSpec | null;
   options: ServedOption[] | null;
   calculator_status: string | null;
   representation: string | null;
   difficulty_settings: unknown;
   skills: string[] | null;
   status: string;
   requires_choice?: boolean;
   format: ServedFormat;
}
/* app/api/routes/frq.py: the free-response unit check, capture, read-back and gradings. */
export interface FrqUnit {
   unit_id: string;
   title: string;
   questions: number;
}

export interface FrqUnitsPayload {
   units: FrqUnit[];
}

export interface FrqPart {
   id: string;
   prompt: string;
   setup_required: boolean;
   points: number;
}

export interface FrqQuestion {
   id: string;
   archetype_id: string;
   calculator_status: string;
   stem: string;
   parts: FrqPart[];
   attempt_id?: string | null;
   grading_state?: string | null;
}

export interface UnitCheckPayload {
   session_id: string;
   mode: string;
   unit_id: string;
   questions: FrqQuestion[];
}

export type ReadBackLineKind = "math" | "text";

export interface ReadBackLine {
   kind: ReadBackLineKind;
   content: string;
   crossed_out: boolean;
   outside_box: boolean;
}

export interface ReadBackPart {
   part_id: string;
   lines: ReadBackLine[];
   answer: string;
}

export interface ReadBack {
   parts: ReadBackPart[];
   unreadable: string[];
}

export interface ImageQuality {
   accepted: boolean;
   reasons: string[];
   measurements: Record<string, unknown>;
}

export interface CaptureImage {
   image_id: string;
   accepted: boolean;
   quality: ImageQuality;
   created_at: string;
}

export interface FrqAttempt {
   attempt_id: string;
   item_id: string;
   capture_mode: string | null;
   grading_state: string | null;
   transcription_confirmed: boolean;
   read_back: ReadBack | null;
   confirmed: ReadBack | null;
   images: CaptureImage[];
}

export interface PhotoVerdict {
   image_id: string;
   accepted: boolean;
   reasons: string[];
   measurements: Record<string, unknown>;
}

export interface GradedPoint {
   grading_id: string;
   part_id: string;
   point_id: string;
   point_type_id: string;
   point_label: string;
   criterion: string;
   decided_by: string;
   earned: number | null;
   provisional: boolean;
   rationale: string;
   evidence_quote: string | null;
   eligibility_note: string | null;
   rereads: number;
}

export interface WorkedPart {
   part_id: string;
   answer_latex: string;
   steps: { text: string; latex: string }[];
}

export interface GradingsPayload {
   attempt_id: string;
   item_id: string;
   grading_state: string | null;
   points: GradedPoint[];
   earned: number;
   decided: number;
   total: number;
   provisional: number;
   worked_solution: WorkedPart[];
   probe_scheduled: string | null;
   /* app/api/routes/frq.py read_gradings: the tutor's stored paragraph on the points not earned. */
   tutor_explanation?: string | null;
   tutor_unavailable?: boolean;
}

export interface DisputeResult {
   grading_id: string;
   attempt_id: string;
   rereading: boolean;
}

/* app/api/routes/assessment.py: the mock exam, the part drills and the unit check. Counts,
   minutes and calculator rules arrive in these payloads (app/assessment/shape.py reads them from
   research/exam/exam-structure.md) and are never typed into the client. */
export type TimedKind = "mocks" | "drills";

export type PartKey = "I-A" | "I-B" | "II-A" | "II-B";

export type AssessmentTool =
   | "timer"
   | "highlight_and_notes"
   | "mark_for_review"
   | "option_eliminator"
   | "question_menu"
   | "zoom"
   | "graphing_panel";

export type PartStatus = "not_started" | "open" | "closed";

export interface ReferenceSheet {
   shown: boolean;
   note: string;
}

export interface ShapePart {
   key: string;
   section: string;
   part: string;
   label: string;
   question_type: string;
   multiple_choice: boolean;
   question_count: number;
   minutes: number | null;
   calculator: boolean;
   calculator_label: string | null;
   calculator_note: string | null;
   first_number: number;
   budget_seconds_per_question: number | null;
   tools: AssessmentTool[];
   five_minute_alert_seconds: number;
}

export interface AssessmentShape {
   form: string;
   parts: ShapePart[];
   multiple_choice_total: number;
   free_response_total: number;
   points_per_free_response_question: number;
   section_weights: Record<string, number>;
   testing_minutes: number;
   reference_sheet: ReferenceSheet;
   radian_note: string;
   timed_available: boolean;
}

export interface HighlightRange {
   start: number;
   end: number;
}

export interface AssessmentAnswer {
   option_id?: string;
   mathjson?: unknown;
   units?: string;
}

export interface AssessmentItem {
   id: string;
   archetype_id: string;
   variant_id: string | null;
   snapshot_id: string | null;
   parameter_draw: unknown;
   stem: string;
   figure_spec: FigureSpec | null;
   options: ServedOption[] | null;
   calculator_status: string | null;
   representation: string | null;
   difficulty_settings: unknown;
   skills: string[] | null;
   status: string;
   requires_choice?: boolean;
   radian_note: boolean;
}

export interface AssessmentFrqItem {
   id: string;
   archetype_id: string;
   calculator_status: string;
   stem: string;
   parts: FrqPart[];
   radian_note: boolean;
}

export type AssessmentQuestionKind = "mcq" | "short_answer" | "frq";

export interface AssessmentQuestion {
   number: number;
   kind: AssessmentQuestionKind;
   format: string;
   answer: AssessmentAnswer | null;
   marked: boolean;
   eliminated: string[];
   notes: string | null;
   highlights: HighlightRange[];
   confidence: Confidence | null;
   time_ms: number;
   attempt_id: string | null;
   item: AssessmentItem | AssessmentFrqItem;
}

export interface FreeResponseCapture {
   number: number;
   item_id: string;
   attempt_id: string | null;
   grading_state: string | null;
   item: AssessmentFrqItem;
}

export interface AssessmentPart extends ShapePart {
   position: number;
   status: PartStatus;
   timed: boolean;
   started_at: string | null;
   deadline_at: string | null;
   closed_at: string | null;
   closed_by: "submitted" | "time" | null;
   time_remaining_ms: number | null;
   answered: number;
   questions: AssessmentQuestion[];
   capture?: FreeResponseCapture[];
}

export interface AssessmentSession {
   id: string;
   mode: string;
   sub_mode: string | null;
   updates_mastery: boolean;
   started_at: string;
   ended_at: string | null;
   capture_mode: string | null;
   parts: AssessmentPart[];
   closed_part_note: string;
   break_note: string;
   reference_sheet: ReferenceSheet;
   radian_note: string;
}

export interface SavedQuestion {
   number: number;
   saved: boolean;
}

export interface PacingRatio {
   numerator: number;
   denominator: number;
   value: number | null;
}

export interface PacingQuestion {
   number: number;
   seconds: number;
   answered: boolean;
   rapid_guess: boolean;
   revisited: boolean;
   marked: boolean;
   eliminator_used: boolean;
}

export interface PartPacing {
   part_key: string;
   label: string;
   questions: number;
   limit_seconds: number;
   budget_seconds_per_question: number;
   time_used_seconds: number | null;
   time_remaining_seconds: number | null;
   closed_by: string | null;
   mean_seconds_per_question: number | null;
   mean_counts: PacingRatio;
   answered: PacingRatio;
   rapid_guess: PacingRatio;
   revisit: PacingRatio;
   marked: PacingRatio;
   per_question: PacingQuestion[];
}

export interface MultipleChoiceCount {
   correct: number;
   total: number;
}

export interface FreeResponseCount {
   earned: number;
   pending: number;
   total: number;
}

export interface PublishedMean {
   year: number;
   mean: number;
   sd: number;
}

export interface QuestionComparison {
   question: number;
   earned: number;
   pending: number;
   possible: number;
   published: PublishedMean[];
}

export interface ScoreBand {
   low: number;
   high: number;
}

export interface BandAssumption {
   key: string;
   text: string;
}

export interface AssessmentResult {
   id: string;
   mode: string;
   complete: boolean;
   pacing: PartPacing[];
   multiple_choice: MultipleChoiceCount | null;
   free_response?: FreeResponseCount;
   questions?: QuestionComparison[];
   band?: ScoreBand;
   band_years?: number[];
   assumptions?: BandAssumption[];
   statement?: string;
}

export interface MockHistoryRow {
   session_id: string;
   taken_at: string;
   band: ScoreBand;
   multiple_choice: MultipleChoiceCount;
   free_response: FreeResponseCount;
}

export interface MockHistoryPayload {
   mocks: MockHistoryRow[];
}

export interface CheckUnit {
   unit_id: string;
   items: number;
   covered_skills: number;
   unit_skills: number;
   available: boolean;
   title: string;
}

export interface CheckUnitsPayload {
   units: CheckUnit[];
}

export interface WorkedStep {
   step: number;
   text: string;
   rule_named?: string;
}

export interface CheckItemResult {
   number: number;
   item_id: string;
   archetype_id: string;
   answered: boolean;
   correct: boolean | null;
   answer: AssessmentAnswer | null;
   key_option_id: string | null;
   worked_solution: WorkedStep[];
}

export interface SkillSnapshot {
   mastered: boolean;
   credited_successes: number;
   credited_failures: number;
}

export interface MovedSkill {
   skill_id: string;
   name: string;
   before: SkillSnapshot | null;
   after: SkillSnapshot | null;
}

export interface CheckCoverage {
   covered: string[];
   unreached: Record<string, string>;
}

export interface CheckResult {
   id: string;
   unit_id: string;
   items: CheckItemResult[];
   moved: MovedSkill[];
   coverage: CheckCoverage;
}


export type UnfinishedMode = "mock" | "part_drill" | "unit_check";

export interface UnfinishedAssessment {
   id: string;
   mode: UnfinishedMode;
   sub_mode: string | null;
   started_at: string;
   parts_closed: number;
   parts_total: number;
}

export interface UnfinishedPayload {
   unfinished: UnfinishedAssessment[];
}

/* app/providers/notices.py: one call to an AI model, as told to the student who made it. */
export type AiNoticeOutcome = "answered" | "failed" | "refused" | "stopped" | "interrupted" | "queued";

export interface AiNotice {
   id: number;
   role: string;
   provider: string;
   model: string;
   outcome: AiNoticeOutcome;
   replayed: boolean;
   asked: string;
   answered: string;
   created_at: string;
}

export interface NoticesPayload {
   notices: AiNotice[];
   latest: number;
}

/* Lessons, docs/plan/15-lessons.md and the lessons framework contract: the record the server
   stores (schemas/lessons/lesson.schema.json), the plan app/lessons/plan.py LessonPlan.as_dict
   returns, and the payloads of app/api/routes/lessons.py. */

export type LessonDeliveryMode = "text" | "step_reveal" | "figure" | "table" | "motion" | "interactive" | "model" | "contrast";

/* A delivery spec is the design's declarative spec verbatim, so only its kind is typed here and the
   mode components read the rest defensively. */
export type LessonSpec = { kind: string } & Record<string, unknown>;

export interface LessonDelivery {
   mode: LessonDeliveryMode;
   reason: string;
   spec?: LessonSpec;
   fallback?: string;
   keyboard?: string;
   reduced_motion?: string;
}

export type LessonSectionType =
   | "prediction"
   | "orientation"
   | "key_ideas"
   | "strategy"
   | "worked_example"
   | "what_a_reader_scores"
   | "common_error"
   | "representations"
   | "prerequisite_bridge";

export interface LessonWorkedStep {
   cue: string;
   why: string;
   expression?: unknown;
   point_type_id?: string;
}

export interface LessonErrorStep {
   text: string;
   expression?: unknown;
}

/* A prediction option: mcq only, exactly one carries is_key. */
export interface LessonPredictionOption {
   id: string;
   label: string;
   is_key: boolean;
   value?: unknown;
}

export interface LessonPredictionKey {
   form: "numeric" | "symbolic" | "statement";
   mathjson?: unknown;
   text?: string;
}

/* The first strategy block's pair: a stem of this concept beside one it is mistaken for. */
export interface LessonContrast {
   this: { text: string; archetype_id?: string };
   not_this: { text: string; why_not?: string };
   feature: string;
}

export interface LessonSection {
   id: string;
   type: LessonSectionType;
   bands?: string[];
   delivery?: LessonDelivery;
   text?: string;
   notation?: string;
   quote?: { text: string; source?: string };
   depth?: "core" | "extended";
   cue?: string;
   method?: string;
   rival?: string;
   separating_feature?: string;
   problem?: { text: string; command_verb?: string };
   steps?: LessonWorkedStep[];
   answer?: { form?: string; mathjson?: unknown };
   example_id?: string;
   lines?: Array<{ point_type_id?: string; text: string }>;
   error_id?: string;
   observed_behavior?: string;
   scoring_consequence?: string;
   wrong_step?: LessonErrorStep;
   right_step?: LessonErrorStep;
   relation?: "distinct" | "equivalent";
   possible_reason?: { misconception_id?: string; text: string };
   prerequisite_id?: string;
   stem?: { text: string; command_verb?: string };
   format?: "mcq" | "short_answer";
   options?: LessonPredictionOption[];
   answer_key?: LessonPredictionKey;
   resolution?: { text: string };
   contrast?: LessonContrast;
   fade_from?: number;
   fix_prompt?: boolean;
}

export interface LessonCheckOption {
   id: string;
   value?: unknown;
   label?: string;
   mathjson?: unknown;
   error_path?: string | null;
}

export interface LessonCheck {
   id: string;
   check_kind: "completion" | "isomorph" | "mcq" | "discrimination";
   bands?: string[];
   format: "short_answer" | "mcq";
   stem: { text: string; command_verb?: string };
   options?: LessonCheckOption[];
   worked_solution?: Array<{ step: number; text: string; mathjson?: unknown }>;
   completes?: string;
   calculator_status?: string;
   representation?: string;
}

export interface LessonDecisionStem {
   id: string;
   archetype_id: string;
   method: string;
   parameter_draw?: unknown;
   text: string;
}

export interface LessonDecision {
   unit: string;
   skills: string[];
   selecting_feature: string;
   delivery: LessonDelivery;
   stems: LessonDecisionStem[];
}

export type LessonStatus = "draft" | "checked" | "resolved" | "signed_off" | "stale" | "retired";

export interface LessonRecord {
   id: string;
   version: number;
   kind: "concept" | "prerequisite" | "decision";
   target_id: string;
   status: LessonStatus;
   read_minutes: { full: number; brief: number };
   word_count: { full: number; brief: number };
   sections: LessonSection[];
   checks: LessonCheck[];
   refresher?: string[];
   decision?: LessonDecision;
   no_figure_reason?: string;
   /* True when the worked example belongs to a calculator archetype (docs/calculator/design.md,
      Where it lives); the server adds it, and a payload without it is read as false. */
   calculator_work?: boolean;
}

export type LessonBand = "low" | "mid";

export type LessonReason = "first_contact" | "feedback" | "read_again" | "T1" | "T2" | "T3" | "T4" | "T5";

export interface LessonSectionRef {
   id: string;
   type: LessonSectionType | "check";
   form: "full" | "steps_only";
}

export interface LessonPlan {
   lesson_id: string;
   version: number;
   band: LessonBand | "none";
   reason: LessonReason;
   sections: LessonSectionRef[];
   checks: string[];
   minutes: number;
   words: number;
   anchors: string[];
}

/* The user's lesson_state row, as the server writes it; null before any read. */
export interface LessonStateRow {
   status?: string;
   read_source?: string | null;
   read_at?: string | null;
   version_seen?: number | null;
}

export type LessonRecordPayload = LessonRecord & { state: LessonStateRow | null };

export interface LessonPlanPayload {
   lesson: LessonRecord;
   plan: LessonPlan;
   band: LessonBand;
   state: LessonStateRow | null;
   calculator_work?: boolean;
}

export type LessonEventKind = "opened" | "section_viewed" | "completed" | "skipped";

/* The eight delivery modes, plus the screens the reader draws itself: a check, the decision stems
   or a strategy's contrast pair, and a prediction. */
export type LessonEventMode = LessonDeliveryMode | "check" | "prediction";

export interface LessonEventBody {
   event: LessonEventKind;
   section_id?: string;
   mode?: LessonEventMode;
   elapsed_ms: number;
   band?: LessonBand;
   reason?: LessonReason;
}

export interface LessonStatePayload {
   ok: boolean;
   state: LessonStateRow | null;
}

export interface LessonCheckAnswerBody {
   answer?: unknown;
   option_id?: string;
   elapsed_ms: number;
}

export interface LessonCheckVerdict {
   correct: boolean;
   error_id: string | null;
   anchor: string | null;
   explanation_anchor: string | null;
   right_step?: string | null;
   scoring_consequence?: string | null;
}

/* POST /lessons/{id}/prompts/{section_id}/answers: a prediction, an error block's fix prompt or a
   faded example's answer. Nothing it writes reaches the engine. */
export interface LessonPromptAnswerBody {
   answer: unknown;
   option_id: string | null;
   elapsed_ms: number;
}

export interface LessonPromptVerdict {
   correct: boolean;
   section_id: string;
   kind: "prediction" | "fix" | "fade";
   resolution: string | null;
}

export type LibraryLessonState =
   | "unseen"
   | "deferred"
   | "served"
   | "read"
   | "skipped"
   | "bypassed_by_placement"
   | "coming_up"
   | "not_available";

export interface LibraryConcept {
   concept_id: string;
   name: string;
   lesson_id: string | null;
   version: number | null;
   servable: boolean;
   state: LibraryLessonState;
   read_at: string | null;
}

export interface LibraryUnit {
   id: string;
   name: string;
   order: number;
   concepts: LibraryConcept[];
}

export interface LibraryPayload {
   units: LibraryUnit[];
}

/* app/api/routes/calculator.py, the Desmos fluency routes, transcribed from the contract in
   docs/calculator/build-plan.md ("Contracts fixed for the parallel slices"). mixed is a request
   only: the server resolves it to one of the six before the drill is served. */
export type CalculatorCapability = "plot" | "zero" | "derivative" | "integral" | "intersection" | "value";

export type CalculatorDrillRequestCapability = CalculatorCapability | "mixed";

export interface CalculatorCardSummary {
   id: string;
   capability: CalculatorCapability;
   title: string;
   task: string;
   drills: string[];
}

export interface CalculatorCardsPayload {
   cards: CalculatorCardSummary[];
}

export interface CalculatorCardStep {
   text: string;
   keys: string;
}

export interface CalculatorDemonstrationLine {
   typed: string;
   shows: string;
}

export interface CalculatorDemonstration {
   function_tex: string;
   lines: CalculatorDemonstrationLine[];
   setup_latex: string;
   answer: string;
}

export interface CalculatorExamHabit {
   text: string;
}

export interface CalculatorCard {
   id: string;
   version: number;
   capability: CalculatorCapability;
   title: string;
   task: string;
   steps: CalculatorCardStep[];
   demonstration: CalculatorDemonstration;
   exam_habit: CalculatorExamHabit[];
   bluebook_note: string | null;
   drills: string[];
}

export interface CalculatorDrillFields {
   capability: CalculatorDrillRequestCapability;
   template_id?: string;
}

export interface CalculatorDrill {
   drill_id: string;
   template_id: string;
   capability: CalculatorCapability;
   card_id: string;
   prompt: string;
   function_tex: string;
   unit: string | null;
   radian_sensitive: boolean;
   desmos_url: string;
   served_at: string;
}

export interface CalculatorAnswerFields {
   value: string;
   setup_mathjson: unknown;
   elapsed_ms: number;
   desmos_open: boolean;
}

export type CalculatorValueReason = "missing" | "not_a_number" | "not_three_places" | "outside_tolerance";

export type CalculatorSetupReason = "missing" | "not_equivalent" | "unsettled" | "unsupported";

export interface CalculatorValueVerdict {
   correct: boolean;
   reason: CalculatorValueReason | null;
   rounded: string;
   truncated: string;
}

export interface CalculatorSetupVerdict {
   shown: boolean;
   correct: boolean | null;
   reason: CalculatorSetupReason | null;
   key_latex: string;
}

export interface CalculatorBudgetSeconds {
   "I-B": number;
   "II-A": number;
}

export interface CalculatorAnswerPayload {
   drill_id: string;
   value: CalculatorValueVerdict;
   setup: CalculatorSetupVerdict;
   elapsed_ms: number;
   budget_seconds: CalculatorBudgetSeconds;
}

export interface CalculatorRatio {
   numerator: number;
   denominator: number;
   value: number | null;
}

export interface CalculatorCapabilityMeasure {
   capability: CalculatorCapability;
   served: number;
   answered: number;
   value_correct: CalculatorRatio;
   setup_shown: CalculatorRatio;
   setup_correct: CalculatorRatio;
   median_ms: number | null;
}

export interface CalculatorRecentDrill {
   drill_id: string;
   capability: CalculatorCapability;
   function_tex: string;
   value_correct: boolean;
   setup_correct: boolean | null;
   setup_shown: boolean;
   elapsed_ms: number;
   submitted_at: string;
}

export interface CalculatorMeasuredPayload {
   capabilities: CalculatorCapabilityMeasure[];
   budget_seconds: CalculatorBudgetSeconds;
   recent: CalculatorRecentDrill[];
}

/* The live tutor's Tutor tab in Settings, app/api/routes/agent.py (docs/agent/architecture.md,
   "The panel and the settings views"). Each group carries the kind's plain label from
   docs/agent/design.md; only preferences and confusions are editable. */
export type AgentMemoryKind = "preference" | "confusion" | "stated_difficulty" | "episode";

export interface AgentMemoryEntry {
   id: string;
   kind: AgentMemoryKind;
   text: string;
   skill_ids: string[];
   created_at: string;
   source_conversation_id: string | null;
   editable: boolean;
}

export interface AgentMemoryGroup {
   kind: AgentMemoryKind;
   label: string;
   entries: AgentMemoryEntry[];
}

export interface AgentMemoriesPayload {
   memory_paused: boolean;
   groups: AgentMemoryGroup[];
}

export interface AgentMemoryDeleted {
   deleted: string;
}

/* DELETE /agent/memories: the counts of rows removed per table, never their text. */
export interface AgentMemoryCleared {
   cleared: {
      tutor_memories: number;
      agent_turns: number;
      agent_conversations: number;
      tutor_profiles: number;
   };
}

export type AgentScreenKind =
   | "today"
   | "session_item"
   | "session_lesson"
   | "lesson"
   | "review"
   | "progress"
   | "assessments"
   | "settings"
   | "other";

export interface AgentConversationSummary {
   id: string;
   opened_at: string;
   last_turn_at: string;
   closed_at: string | null;
   opened_on_screen: AgentScreenKind;
   turn_count: number;
}

export type AgentTurnOutcome = "complete" | "stopped" | "incomplete" | "withheld" | "declined";

export interface AgentConversationTurn {
   id: string;
   role: "student" | "agent";
   text: string;
   created_at: string;
   outcome: AgentTurnOutcome | null;
}

export interface AgentConversationsPayload {
   conversations: AgentConversationSummary[];
}

export interface AgentConversationPayload extends AgentConversationSummary {
   turns: AgentConversationTurn[];
}

export interface AgentConversationDeleted {
   deleted: string;
}

export interface AgentSettingsPayload {
   memory_paused: boolean;
}

/* GET /agent/profile: the highest tutor_profiles version, and the tutor_profile switch's state, or
   "absent" while the switch has no definition. */
export interface AgentProfilePayload {
   profile: Record<string, unknown> | null;
   version: number | null;
   experiment: ExperimentState | "absent";
}

/* The one structured shape the client sends with every turn as screen (docs/agent/architecture.md,
   "The screen context"; schemas/agent/screen.schema.json). Never the draft answer, the selected
   option or a key. section_index counts from 0. */
export type AgentScreen =
   | { kind: "today" }
   | {
        kind: "session_item";
        session_id: string;
        attempt_id: string;
        item_id: string;
        format: ServedFormat;
        served_stage: FadingStage;
        submitted: boolean;
        feedback_kind?: string;
     }
   | {
        kind: "session_lesson";
        session_id: string;
        lesson_id: string;
        version: number;
        section_id: string;
        section_index: number;
        section_count: number;
     }
   | {
        kind: "lesson";
        lesson_id: string;
        version: number;
        section_id: string;
        section_index: number;
        section_count: number;
        return_to: string | null;
     }
   | { kind: "review" }
   | { kind: "progress"; tab: string; skill_id?: string }
   | { kind: "assessments"; format: string; timed?: boolean }
   | { kind: "settings"; tab: string }
   | { kind: "other"; view: string };

/* POST /agent/turns, answered as text/event-stream (docs/agent/architecture.md, "Streaming end to
   end"). */
export interface AgentTurnBody {
   conversation_id: string | null;
   screen: AgentScreen;
   message: string;
}

export type AgentErrorKind = "usage_limit" | "daily_cap" | "minute_cap" | "sign_in" | "unavailable" | "timed" | "ceiling" | "refused";

export interface AgentStartEvent {
   conversation_id: string;
   turn_id: string;
   screen_line: string;
   can_see: string[];
}

export interface AgentTextEvent {
   delta: string;
}

export interface AgentEndEvent {
   turn_id: string;
   outcome: AgentTurnOutcome;
   turns_on_item: number;
   turns_in_conversation: number;
}

/* The figure events of docs/agent/drawing-design.md, "Events and order". figure_pending carries no
   data and figure carries the render spec, TutorFigureSpec, which the client checks again. */
export interface AgentFigureStepEvent {
   figure: string;
   step: string;
}

export type AgentFigureRefusedReason = "malformed" | "oversized" | "unclosed" | "extra" | "closed" | "off";

export interface AgentFigureRefusedEvent {
   reason: AgentFigureRefusedReason;
   copy: string;
   part?: "figure" | "marks";
}

export interface AgentErrorEvent {
   kind: AgentErrorKind;
   resets_at?: string | null;
   copy?: string;
}
