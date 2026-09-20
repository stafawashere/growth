"""What the feedback screen shows and what the elaborated template receives (R35).

Timing follows the fading stage: step-level verification while support is present at stages
example and completion, and nothing at all at stage unsupported until the student has submitted
(docs/plan/03-diagnosis-and-feedback.md, Feedback policy). After submission a lost point gets
elaborated feedback built from the violated expected_solution_path step, the observed_behavior and
scoring_consequence of the chosen option's BC-ERR record, and the item's stored worked solution.
Those four fields are the whole of what the tutor role sees, so the final answer never reaches it
before the student has committed.

A wrong answer often carries no BC-ERR record at all. R12 in docs/plan/11-phased-delivery.md gives
an incorrect answer with no error path its own rule, and app/items/grade.py returns error_path None
for every wrong short answer, so demanding a record would leave the whole short answer path without
feedback. The payload is composed without one: the violated step falls back to the last step of
expected_solution_path, the worked solution is the item's own, and observed_behavior and
scoring_consequence stay empty rather than being guessed. 03 part 2 allows a scoring consequence to
come from the BC-PT does_not_earn text instead. app/content/loader.py does read
data/scoring_points.json and the archetype records carry BC-PT ids, but that text answers which
point the response failed to earn, and naming one of an archetype's several point types needs the
per-point decision that P1 has no component to make (03's own table puts per-point grading behind
mechanic 6). Guessing a point would put an exam consequence in front of the student that nothing
decided, so the field stays empty until a per-point grader exists.

The confidence rating and the hypercorrection flag belong to app/session/service.py and
app/engine/update.py; this module only refuses to render feedback for a stage whose rating has not
been recorded yet.
"""
from dataclasses import dataclass
from enum import Enum

from app.engine.state import Confidence, FadingStage
from app.session.service import collects_confidence

ELABORATED_TEMPLATE = "prompts/feedback/elaborated_v1.md"

PROMPT_FIELDS = ("violated_step", "observed_behavior", "scoring_consequence", "worked_solution")

STEP_VERIFICATION_STAGES = (FadingStage.EXAMPLE, FadingStage.COMPLETION)


class FeedbackKind(str, Enum):
   STEP_VERIFICATION = "step_verification"
   WITHHELD = "withheld"
   ELABORATED = "elaborated"
   CORRECT = "correct"


@dataclass(frozen=True)
class StepMark:
   index: int
   description: str
   correct: bool | None


@dataclass(frozen=True)
class ElaboratedPayload:
   error_id: str | None
   violated_step_index: int
   violated_step: str
   observed_behavior: str
   scoring_consequence: str
   worked_solution: str
   template: str = ELABORATED_TEMPLATE
   tutor_sentence: str | None = None

   def as_prompt_fields(self):
      return {
         "violated_step": self.violated_step,
         "observed_behavior": self.observed_behavior,
         "scoring_consequence": self.scoring_consequence,
         "worked_solution": self.worked_solution,
      }


@dataclass(frozen=True)
class Feedback:
   kind: FeedbackKind
   stage: FadingStage
   step_marks: tuple[StepMark, ...] = ()
   elaborated: ElaboratedPayload | None = None
   self_explanation_prompt: str | None = None
   confidence: Confidence | None = None


def self_explanation_prompt(step_number):
   return f"which rule justifies step {step_number}, and why does it apply here"


def step_verification(archetype, step_outcomes):
   """One mark per step of expected_solution_path, in the order the path lists them."""
   path = list(archetype["expected_solution_path"])
   outcomes = list(step_outcomes) if step_outcomes is not None else []
   marks = []

   for index, description in enumerate(path):
      has_outcome = index < len(outcomes)
      outcome = outcomes[index] if has_outcome else None

      marks.append(StepMark(index=index, description=description, correct=outcome))

   return tuple(marks)


def violated_step_index(archetype, chosen_option, error_record):
   """The option names the step it breaks; without one the last step of the path stands in."""
   path = list(archetype["expected_solution_path"])
   option_index = (chosen_option or {}).get("violated_step")
   record_index = (error_record or {}).get("violated_step")
   stated = option_index if option_index is not None else record_index
   has_stated_index = stated is not None

   if has_stated_index:
      is_in_range = 0 <= stated < len(path)

      if not is_in_range:
         raise ValueError(f"violated step {stated} is outside the solution path of {archetype['id']}")

      return stated

   return len(path) - 1


def elaborated_payload(archetype, item, chosen_option, error_record):
   """Without a BC-ERR record the two fields it supplies are carried empty, never invented.

   An option that names an error path the snapshot cannot resolve is a different case: the id is
   there and the record is not, which the loader is meant to make impossible, so it is refused.
   """
   names_a_path = (chosen_option or {}).get("error_path") is not None
   is_unresolved = names_a_path and error_record is None

   if is_unresolved:
      raise ValueError(
         f"option {chosen_option.get('id')} names {chosen_option['error_path']}, "
         "which this snapshot does not hold"
      )

   record = error_record or {}
   index = violated_step_index(archetype, chosen_option, error_record)

   return ElaboratedPayload(
      error_id=record.get("id"),
      violated_step_index=index,
      violated_step=archetype["expected_solution_path"][index],
      observed_behavior=record.get("observed_behavior") or "",
      scoring_consequence=record.get("scoring_consequence") or "",
      worked_solution=item["worked_solution"],
   )


def render_feedback(
   stage,
   archetype,
   item,
   submitted=False,
   correct=None,
   step_outcomes=None,
   chosen_option=None,
   error_record=None,
   confidence=None,
):
   served_stage = FadingStage(stage)
   rating = Confidence(confidence) if confidence is not None else None

   _check_rating(served_stage, submitted, rating)

   shows_steps = served_stage in STEP_VERIFICATION_STAGES

   if shows_steps:
      return _supported_feedback(served_stage, archetype, step_outcomes, submitted, correct, rating)

   if not submitted:
      return Feedback(kind=FeedbackKind.WITHHELD, stage=served_stage, confidence=rating)

   if correct:
      return Feedback(kind=FeedbackKind.CORRECT, stage=served_stage, confidence=rating)

   payload = elaborated_payload(archetype, item, chosen_option, error_record)

   return Feedback(
      kind=FeedbackKind.ELABORATED,
      stage=served_stage,
      elaborated=payload,
      self_explanation_prompt=self_explanation_prompt(payload.violated_step_index + 1),
      confidence=rating,
   )


def as_dict(feedback):
   payload = feedback.elaborated
   has_payload = payload is not None

   return {
      "kind": feedback.kind.value,
      "stage": feedback.stage.value,
      "step_marks": [
         {"index": mark.index, "description": mark.description, "correct": mark.correct}
         for mark in feedback.step_marks
      ],
      "elaborated": dict(payload.as_prompt_fields(), error_id=payload.error_id) if has_payload else None,
      "self_explanation_prompt": feedback.self_explanation_prompt,
      "confidence": feedback.confidence.value if feedback.confidence is not None else None,
   }


def _supported_feedback(served_stage, archetype, step_outcomes, submitted, correct, rating):
   marks = step_verification(archetype, step_outcomes)
   is_worked_example = served_stage == FadingStage.EXAMPLE
   prompt = self_explanation_prompt(len(marks)) if is_worked_example else None
   is_completion = served_stage == FadingStage.COMPLETION
   was_marked_wrong = submitted and correct is False
   is_corrected_completion = is_completion and was_marked_wrong

   if is_corrected_completion:
      failed = [mark for mark in marks if mark.correct is False]
      has_failed_step = len(failed) > 0
      step_number = failed[0].index + 1 if has_failed_step else len(marks)
      prompt = self_explanation_prompt(step_number)

   return Feedback(
      kind=FeedbackKind.STEP_VERIFICATION,
      stage=served_stage,
      step_marks=marks,
      self_explanation_prompt=prompt,
      confidence=rating,
   )


def _check_rating(served_stage, submitted, rating):
   needs_rating = submitted and collects_confidence(served_stage)
   is_missing = needs_rating and rating is None

   if is_missing:
      raise ValueError(f"a confidence rating is collected before feedback at stage {served_stage.value}")
