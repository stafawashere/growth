/* The shapes the FastAPI layer already returns, transcribed from app/api/routes/sessions.py,
   app/runtime/bank.py and app/feedback/render.py. Nothing here is invented: a field absent from
   those modules is absent here, and a client that needs one reports the gap rather than adding
   it. */

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

/* app/runtime/bank.py _as_item_dict, plus the two fields the queue slot carries
   (app/session/service.py resolve_served_format). */
export interface ServedItem {
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
   queue: Record<string, ServedItem[]>;
   remaining: ServedItem[];
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

/* app/feedback/render.py step_verification. */
export interface StepMark {
   index: number;
   description: string;
   correct: boolean;
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
