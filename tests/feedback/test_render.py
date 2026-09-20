import json

import pytest

from app.engine.state import Confidence, FadingStage
from app.feedback import render


ARCHETYPE = {
   "id": "BC-QA-01007",
   "point_types": [],
   "expected_solution_path": [
      "substitute and observe the indeterminate form",
      "rewrite the expression into an equivalent form",
      "divide out the common factor or simplify",
      "evaluate the simplified expression at the target",
   ],
}

ERROR_RECORD = {
   "id": "BC-ERR-01004",
   "observed_behavior": "cancels a term of a sum rather than a factor of a product",
   "scoring_consequence": "the simplification point is not earned and the answer point falls with it",
}

ITEM = {
   "id": "BC-ITM-0001",
   "archetype_id": "BC-QA-01007",
   "answer_key": "seven halves",
   "worked_solution": "factor the numerator, divide out the common factor, then evaluate at the target",
   "options": [
      {"value": "seven halves", "error_path": None},
      {"value": "three", "error_path": "BC-ERR-01004", "violated_step": 2},
   ],
}

WRONG_OPTION = ITEM["options"][1]


def test_step_verification_at_example_and_completion():
   for stage in (FadingStage.EXAMPLE, FadingStage.COMPLETION):
      feedback = render.render_feedback(
         stage=stage,
         archetype=ARCHETYPE,
         item=ITEM,
         submitted=False,
         step_outcomes=[True, True, False, False],
         confidence=Confidence.UNSURE,
      )

      assert feedback.kind is render.FeedbackKind.STEP_VERIFICATION
      assert len(feedback.step_marks) == len(ARCHETYPE["expected_solution_path"])
      assert [mark.correct for mark in feedback.step_marks] == [True, True, False, False]
      assert feedback.step_marks[2].description == ARCHETYPE["expected_solution_path"][2]
      assert feedback.elaborated is None


def test_nothing_returned_before_submission_at_unsupported():
   withheld = render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=False,
      step_outcomes=[True, False, False, False],
      confidence=Confidence.CONFIDENT,
   )

   assert withheld.kind is render.FeedbackKind.WITHHELD
   assert withheld.step_marks == ()
   assert withheld.elaborated is None
   assert withheld.self_explanation_prompt is None

   after = render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=True,
      correct=False,
      chosen_option=WRONG_OPTION,
      error_record=ERROR_RECORD,
      confidence=Confidence.CONFIDENT,
   )

   assert after.kind is render.FeedbackKind.ELABORATED
   assert after.elaborated is not None


def test_elaborated_payload_names_violated_step_and_error_path():
   feedback = render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=True,
      correct=False,
      chosen_option=WRONG_OPTION,
      error_record=ERROR_RECORD,
      confidence=Confidence.GUESS,
   )

   payload = feedback.elaborated

   assert payload.error_id == "BC-ERR-01004"
   assert payload.violated_step_index == 2
   assert payload.violated_step == ARCHETYPE["expected_solution_path"][2]
   assert payload.observed_behavior == ERROR_RECORD["observed_behavior"]
   assert payload.worked_solution == ITEM["worked_solution"]
   assert payload.template == render.ELABORATED_TEMPLATE
   assert payload.tutor_sentence is None

   fields = payload.as_prompt_fields()

   assert set(fields) == {
      "violated_step",
      "observed_behavior",
      "scoring_consequence",
      "worked_solution",
   }


def test_scoring_consequence_comes_from_the_error_record():
   other_record = dict(ERROR_RECORD)
   other_record["scoring_consequence"] = "neither the integral point nor the answer point is earned"

   feedback = render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=True,
      correct=False,
      chosen_option=WRONG_OPTION,
      error_record=other_record,
      confidence=Confidence.UNSURE,
   )

   assert feedback.elaborated.scoring_consequence == other_record["scoring_consequence"]
   assert feedback.elaborated.as_prompt_fields()["scoring_consequence"] == other_record["scoring_consequence"]

   with pytest.raises(ValueError):
      render.render_feedback(
         stage=FadingStage.UNSUPPORTED,
         archetype=ARCHETYPE,
         item=ITEM,
         submitted=True,
         correct=False,
         chosen_option=WRONG_OPTION,
         error_record=None,
         confidence=Confidence.UNSURE,
      )


def test_self_explanation_only_on_examples_and_corrected_errors():
   worked_example = render.render_feedback(
      stage=FadingStage.EXAMPLE,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=False,
      step_outcomes=[True, True, True, True],
   )

   corrected_error = render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=True,
      correct=False,
      chosen_option=WRONG_OPTION,
      error_record=ERROR_RECORD,
      confidence=Confidence.CONFIDENT,
   )

   completion_correct = render.render_feedback(
      stage=FadingStage.COMPLETION,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=True,
      correct=True,
      step_outcomes=[True, True, True, True],
      confidence=Confidence.CONFIDENT,
   )

   unsupported_correct = render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=True,
      correct=True,
      confidence=Confidence.CONFIDENT,
   )

   assert worked_example.self_explanation_prompt == render.self_explanation_prompt(4)
   assert corrected_error.self_explanation_prompt == render.self_explanation_prompt(3)
   assert completion_correct.self_explanation_prompt is None
   assert unsupported_correct.self_explanation_prompt is None
   assert "which rule justifies step 3" in corrected_error.self_explanation_prompt


def test_tutor_receives_no_answer_before_submission():
   withheld = render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=False,
      confidence=Confidence.UNSURE,
   )

   serialised = json.dumps(render.as_dict(withheld))

   assert ITEM["answer_key"] not in serialised
   assert ITEM["worked_solution"] not in serialised

   in_progress_example = render.render_feedback(
      stage=FadingStage.EXAMPLE,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=False,
      step_outcomes=[True, False, False, False],
   )

   assert ITEM["answer_key"] not in json.dumps(render.as_dict(in_progress_example))

   after = render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=True,
      correct=False,
      chosen_option=WRONG_OPTION,
      error_record=ERROR_RECORD,
      confidence=Confidence.UNSURE,
   )

   assert ITEM["answer_key"] not in json.dumps(after.elaborated.as_prompt_fields())
   assert after.elaborated.as_prompt_fields()["worked_solution"] == ITEM["worked_solution"]
