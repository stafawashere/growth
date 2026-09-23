/* The shapes the FastAPI layer returns, transcribed from the route and service modules each
   comment names. Nothing here is invented: a field absent from those modules is absent here, and
   client.test.ts scans the Python source so a field added or dropped on either side fails. */

export type FadingStage = "example" | "completion" | "unsupported";

export type ServedFormat = "mcq" | "short_answer";

export type Confidence = "guess" | "unsure" | "confident";

/* app/runtime/bank.py STUDENT_OPTION_FIELDS. is_key and error_path are withheld by the server. */
export interface ServedOption {
   id: string;
   value?: string;
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

/* app/session/preview.py queue_preview. */
export interface ProgressPayload {
   skills_due_for_review: number;
   frontier_skills: number;
   corrected_items_returning: number;
   forecast_minutes: number;
   session_in_progress: string | null;
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