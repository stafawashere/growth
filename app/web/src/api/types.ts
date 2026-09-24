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

/* A queue slot as sessions.queue stores it: app/runtime/bank.py _as_item_dict plus the fields
   app/engine/select.py dress_item writes onto it. */
export interface QueueSlot {
   id: string;
   archetype_id: string;
   variant_id: string | null;
   snapshot_id: string | null;
   parameter_draw: unknown;
   stem: string;
   figure_spec: unknown;
   options: ServedOption[] | null;
   calculator_status: string | null;
   representation: string | null;
   difficulty_settings: unknown;
   skills: string[] | null;
   status: string;
   stage: FadingStage;
   format: ServedFormat;
   is_probe: boolean;
}

/* GET /sessions/{id}/next: the slot plus app/session/service.py served_item's steps and the
   prompt app/api/routes/sessions.py read_next_item attaches at stage example. */
export interface ServedItem extends QueueSlot {
   served_steps: ServedStep[] | null;
   self_explanation_prompt: string | null;
}

/* app/session/service.py queue_payload. Block 4 holds the ids of items corrected today, and
   forecasts maps an archetype id to its forecast minutes. */
export interface SessionQueue {
   block1: QueueSlot[];
   block2: QueueSlot[];
   block3: QueueSlot[];
   block4: string[];
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
   remaining: QueueSlot[];
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

/* app/api/routes/sessions.py read_feedback: render.as_dict plus the two tutor fields. */
export interface FeedbackPayload {
   kind: string;
   stage: FadingStage;
   step_marks: StepMark[];
   elaborated: ElaboratedPayload | null;
   self_explanation_prompt: string | null;
   confidence: Confidence | null;
   sentence: string | null;
   tutor_unavailable: boolean;
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
export interface ProvidersPayload {
   roles: ProviderRole[];
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
   figure_spec: unknown;
   options: ServedOption[] | null;
   calculator_status: string | null;
   representation: string | null;
   difficulty_settings: unknown;
   skills: string[] | null;
   status: string;
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
}

export interface DisputeResult {
   grading_id: string;
   attempt_id: string;
   rereading: boolean;
}
