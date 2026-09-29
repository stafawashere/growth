"""The correct response after a wrong answer (03, Content, part 3) and the first worked step a
correct opener gets when no comparison is drawn (01, Productive-failure openers)."""
import json

from app.engine.state import Confidence, FadingStage
from app.feedback import render
from tests.feedback.test_render import ARCHETYPE, WORKED_SOLUTION, WORKED_STEP_TEXTS

KEY_MATHJSON = ["Rational", 7, 2]

VALUE_ITEM = {
   "worked_solution": WORKED_SOLUTION,
   "answer_key": {"form": "symbolic", "mathjson": KEY_MATHJSON},
   "options": [
      {"id": "A", "is_key": True, "label": "The limit is seven halves.", "error_path": None},
      {"id": "B", "is_key": False, "label": "The limit is three.", "error_path": None, "violated_step": 2},
   ],
}


def feedback_for(stage, correct, answer, submitted=True, is_opener=False):
   return render.render_feedback(
      stage=stage,
      archetype=ARCHETYPE,
      item=VALUE_ITEM,
      submitted=submitted,
      correct=correct,
      chosen_option=VALUE_ITEM["options"][1] if "option_id" in answer else None,
      confidence=Confidence.UNSURE if submitted else None,
      is_opener=is_opener,
      answer=answer,
   )


def test_a_wrong_short_answer_carries_the_key_mathjson():
   feedback = feedback_for(FadingStage.UNSUPPORTED, False, {"mathjson": 3})

   assert render.as_dict(feedback)["correct_answer"] == {"label": None, "mathjson": KEY_MATHJSON}


def test_a_wrong_choice_carries_the_keyed_option_label():
   feedback = feedback_for(FadingStage.UNSUPPORTED, False, {"option_id": "B"})

   assert render.as_dict(feedback)["correct_answer"] == {"label": "The limit is seven halves.", "mathjson": None}


def test_a_wrong_completion_blank_carries_it_beside_the_step_marks():
   feedback = feedback_for(FadingStage.COMPLETION, False, {"option_id": "B"})

   assert feedback.kind == render.FeedbackKind.STEP_VERIFICATION
   assert render.as_dict(feedback)["correct_answer"]["label"] == "The limit is seven halves."


def test_a_statement_key_gives_its_label_to_a_typed_answer():
   item = dict(VALUE_ITEM, answer_key={"form": "statement", "label": "It does not exist."}, options=[])

   assert render.correct_answer(item, {"mathjson": 3}) == {"label": "It does not exist.", "mathjson": None}


def test_nothing_is_shown_before_the_grade_or_after_a_right_answer():
   unsubmitted = feedback_for(FadingStage.UNSUPPORTED, None, {"mathjson": 3}, submitted=False)
   unsubmitted_completion = feedback_for(FadingStage.COMPLETION, None, {"mathjson": 3}, submitted=False)
   ungraded = feedback_for(FadingStage.UNSUPPORTED, None, {"mathjson": None})
   right = feedback_for(FadingStage.UNSUPPORTED, True, {"mathjson": KEY_MATHJSON})

   for feedback in (unsubmitted, unsubmitted_completion, ungraded, right):
      serialised = render.as_dict(feedback)

      assert serialised["correct_answer"] is None
      assert json.dumps(KEY_MATHJSON) not in json.dumps(serialised)


def test_an_opener_has_no_correct_answer_and_a_correct_one_gets_the_first_step():
   missed = feedback_for(FadingStage.UNSUPPORTED, False, {"mathjson": 3}, is_opener=True)
   reached = feedback_for(FadingStage.UNSUPPORTED, True, {"mathjson": KEY_MATHJSON}, is_opener=True)
   ordinary = feedback_for(FadingStage.UNSUPPORTED, True, {"mathjson": KEY_MATHJSON})

   assert render.as_dict(missed)["correct_answer"] is None
   assert render.as_dict(reached)["first_worked_step"] == {"index": 1, "text": WORKED_STEP_TEXTS[0]}
   assert render.as_dict(ordinary)["first_worked_step"] is None
