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

WORKED_STEP_TEXTS = (
   "substitute the target and observe zero over zero",
   "factor the numerator",
   "divide out the common factor",
   "evaluate at the target",
)

WORKED_SOLUTION = json.dumps([
   {"step": position + 1, "text": text, "mathjson": None}
   for position, text in enumerate(WORKED_STEP_TEXTS)
])

ITEM = {
   "id": "BC-ITM-0001",
   "archetype_id": "BC-QA-01007",
   "answer_key": "seven halves",
   "worked_solution": WORKED_SOLUTION,
   "options": [
      {"value": "seven halves", "error_path": None},
      {"value": "three", "error_path": "BC-ERR-01004", "violated_step": 2},
   ],
}

WRONG_OPTION = ITEM["options"][1]


def expected_marks(given_count, verdict):
   """Worked_solution positions from 1: the first given_count steps given, the rest the blank."""
   return [
      {
         "index": position,
         "text": text,
         "given": position <= given_count,
         "correct": None if position <= given_count else verdict,
      }
      for position, text in enumerate(WORKED_STEP_TEXTS, start=1)
   ]


def rendered_marks(feedback):
   return render.as_dict(feedback)["step_marks"]


def test_step_verification_at_example_and_completion():
   """Example blanks its last step exactly as completion does (BUILD-LEDGER.md, "Decisions taken
   on the operator's instruction, 2026-09-23": 11 implementer decision 3 is withdrawn).
   """
   step_count = len(WORKED_STEP_TEXTS)
   cases = {
      "unsubmitted": (False, None),
      "right": (True, True),
      "wrong": (True, False),
   }
   examples = {
      name: render.render_feedback(
         stage=FadingStage.EXAMPLE,
         archetype=ARCHETYPE,
         item=ITEM,
         submitted=submitted,
         correct=correct,
         confidence=Confidence.UNSURE,
      )
      for name, (submitted, correct) in cases.items()
   }
   completions = {
      name: render.render_feedback(
         stage=FadingStage.COMPLETION,
         archetype=ARCHETYPE,
         item=ITEM,
         submitted=submitted,
         correct=correct,
         confidence=Confidence.UNSURE,
      )
      for name, (submitted, correct) in cases.items()
   }

   assert rendered_marks(examples["unsubmitted"]) == expected_marks(step_count - 1, None)
   assert rendered_marks(examples["right"]) == expected_marks(step_count - 1, True)
   assert rendered_marks(examples["wrong"]) == expected_marks(step_count - 1, False)
   assert rendered_marks(completions["unsubmitted"]) == expected_marks(step_count - 1, None)
   assert rendered_marks(completions["right"]) == expected_marks(step_count - 1, True)
   assert rendered_marks(completions["wrong"]) == expected_marks(step_count - 1, False)

   for feedback in [*examples.values(), *completions.values()]:
      assert feedback.kind is render.FeedbackKind.STEP_VERIFICATION
      assert feedback.elaborated is None


def test_nothing_returned_before_submission_at_unsupported():
   withheld = render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=False,
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


def test_an_ungraded_submission_at_unsupported_states_no_verdict():
   """A wrong option on an attempt the grader never settled still elaborates nothing."""
   ungraded = render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=True,
      correct=None,
      chosen_option=WRONG_OPTION,
      error_record=ERROR_RECORD,
      confidence=Confidence.CONFIDENT,
   )

   assert ungraded.kind is render.FeedbackKind.UNGRADED
   assert ungraded.step_marks == ()
   assert ungraded.elaborated is None
   assert ungraded.self_explanation_prompt is None


def test_a_submitted_example_marks_the_blank_with_no_verdict_when_ungraded():
   example = render.render_feedback(
      stage=FadingStage.EXAMPLE,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=True,
      correct=None,
      confidence=Confidence.UNSURE,
   )

   assert rendered_marks(example) == expected_marks(len(WORKED_STEP_TEXTS) - 1, None)
   assert example.kind is render.FeedbackKind.STEP_VERIFICATION
   assert example.elaborated is None
   assert example.self_explanation_prompt is not None


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


def test_self_explanation_only_on_examples_and_corrected_errors():
   worked_example = render.render_feedback(
      stage=FadingStage.EXAMPLE,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=False,
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

   assert worked_example.self_explanation_prompt == render.self_explanation_prompt(3)
   assert corrected_error.self_explanation_prompt == render.self_explanation_prompt(3)
   assert completion_correct.self_explanation_prompt is None
   assert unsupported_correct.self_explanation_prompt is None
   assert "which rule justifies step 3" in corrected_error.self_explanation_prompt

   corrected_completion = render.render_feedback(
      stage=FadingStage.COMPLETION,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=True,
      correct=False,
      confidence=Confidence.CONFIDENT,
   )

   assert corrected_completion.self_explanation_prompt == render.self_explanation_prompt(
      len(WORKED_STEP_TEXTS) - 1
   )


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

   for step_text in WORKED_STEP_TEXTS:
      assert step_text not in serialised

   in_progress_example = render.render_feedback(
      stage=FadingStage.EXAMPLE,
      archetype=ARCHETYPE,
      item=ITEM,
      submitted=False,
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


SHORT_ANSWER_ITEM = {
   "id": "BC-ITM-0002",
   "archetype_id": "BC-QA-01007",
   "answer_key": "seven halves",
   "worked_solution": WORKED_SOLUTION,
   "options": [],
}

ARCHETYPE_WITH_POINT_TYPES = {
   "id": "BC-QA-02007",
   "point_types": ["BC-PT-99023", "BC-PT-99004", "BC-PT-99005"],
   "expected_solution_path": list(ARCHETYPE["expected_solution_path"]),
}


def _wrong_short_answer(archetype=ARCHETYPE):
   return render.render_feedback(
      stage=FadingStage.UNSUPPORTED,
      archetype=archetype,
      item=SHORT_ANSWER_ITEM,
      submitted=True,
      correct=False,
      chosen_option=None,
      error_record=None,
      confidence=Confidence.UNSURE,
   )


def test_wrong_short_answer_without_an_error_record_still_elaborates():
   feedback = _wrong_short_answer()

   assert feedback.kind is render.FeedbackKind.ELABORATED

   payload = feedback.elaborated

   assert payload is not None
   assert payload.error_id is None
   assert payload.worked_solution == SHORT_ANSWER_ITEM["worked_solution"]
   assert payload.template == render.ELABORATED_TEMPLATE
   assert feedback.self_explanation_prompt == render.self_explanation_prompt(4)


def test_absent_error_fields_are_empty_and_never_invented():
   payload = _wrong_short_answer().elaborated
   fields = payload.as_prompt_fields()

   assert payload.observed_behavior == ""
   assert payload.scoring_consequence == ""
   assert fields["observed_behavior"] == ""
   assert fields["scoring_consequence"] == ""
   assert fields["violated_step"] != ""
   assert ERROR_RECORD["observed_behavior"] not in json.dumps(fields)
   assert ERROR_RECORD["scoring_consequence"] not in json.dumps(fields)


def test_the_violated_step_falls_back_to_the_last_path_step():
   path = ARCHETYPE["expected_solution_path"]
   payload = _wrong_short_answer().elaborated

   assert payload.violated_step_index == len(path) - 1
   assert payload.violated_step == path[-1]
   assert render.violated_step_index(ARCHETYPE, None, None) == len(path) - 1


def test_the_tutor_payload_is_still_exactly_the_four_fields():
   fields = _wrong_short_answer().elaborated.as_prompt_fields()
   serialised = json.dumps(fields)

   assert tuple(fields) == render.PROMPT_FIELDS
   assert set(fields) == set(render.PROMPT_FIELDS)
   assert SHORT_ANSWER_ITEM["answer_key"] not in serialised
   assert SHORT_ANSWER_ITEM["id"] not in serialised
   assert ARCHETYPE["id"] not in serialised


def test_no_scoring_consequence_when_the_archetype_supplies_none():
   payload = _wrong_short_answer(ARCHETYPE_WITH_POINT_TYPES).elaborated

   assert payload.scoring_consequence == ""

   for point_type_id in ARCHETYPE_WITH_POINT_TYPES["point_types"]:
      assert point_type_id not in json.dumps(payload.as_prompt_fields())


def test_a_distractor_whose_error_path_does_not_resolve_is_refused():
   """A named BC-ERR id that the snapshot does not hold is a content fault, not a missing path.

   R12 rule 3 covers an answer with no error path at all, which composes without a record. An
   option that names one and cannot resolve it is the case the loader is supposed to make
   impossible, so feedback refuses rather than quietly dropping the two fields.
   """
   with pytest.raises(ValueError):
      render.elaborated_payload(ARCHETYPE, ITEM, WRONG_OPTION, None)


def test_the_payload_names_the_template_the_tutor_renders():
   from app.feedback import tutor

   repository_root = tutor.TEMPLATE_PATH.parents[2]
   rendered_template = tutor.TEMPLATE_PATH.relative_to(repository_root).as_posix()

   assert render.ELABORATED_TEMPLATE == rendered_template
