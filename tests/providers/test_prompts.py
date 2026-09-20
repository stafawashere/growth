"""docs/plan/11-phased-delivery.md P1 scope item 13, the golden test on templates.

docs/plan/03-diagnosis-and-feedback.md, Who composes the string in P1 (R35): the tutor
receives exactly the four fields app/feedback/render.py produces for elaborated feedback,
and nothing wider. The tutor practice template never receives an answer key or a worked
solution, because it renders during practice, before the student has submitted.
"""
from pathlib import Path

import pytest

from app.providers.base import render_template, split_template

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TUTOR_TEMPLATE = REPO_ROOT / "prompts" / "tutor" / "guardrailed_practice_v1.md"
FEEDBACK_TEMPLATE = REPO_ROOT / "prompts" / "feedback" / "elaborated_v1.md"

FEEDBACK_PAYLOAD = {
   "violated_step": "divide out the common factor or simplify",
   "observed_behavior": "cancels a term of a sum rather than a factor of a product",
   "scoring_consequence": "the simplification point is not earned and the answer point falls with it",
   "worked_solution": "factor the numerator, divide out the common factor, then evaluate at the target",
}


def test_tutor_template_never_receives_the_answer_key():
   text = TUTOR_TEMPLATE.read_text()
   _prefix, variable_section = split_template(text)

   assert "answer_key" not in variable_section
   assert "worked_solution" not in variable_section

   tutor_payload = {
      "misconception_list": "none recorded",
      "item_skills": "BC-SKL-02006",
      "guardrail_level": "standard",
   }

   with pytest.raises(ValueError):
      render_template(text, dict(tutor_payload, answer_key="seven halves"))

   with pytest.raises(ValueError):
      render_template(text, dict(tutor_payload, worked_solution="differentiate term by term"))

   rendered = render_template(text, tutor_payload)

   assert "seven halves" not in rendered
   assert "differentiate term by term" not in rendered


def test_prompt_templates_are_versioned_and_golden():
   assert TUTOR_TEMPLATE.exists()
   assert FEEDBACK_TEMPLATE.exists()

   tutor_text = TUTOR_TEMPLATE.read_text()
   feedback_text = FEEDBACK_TEMPLATE.read_text()

   forbidden_em_dash = chr(0x2014)
   forbidden_en_dash_spaced = " " + chr(0x2013) + " "

   for text in (tutor_text, feedback_text):
      assert forbidden_em_dash not in text
      assert forbidden_en_dash_spaced not in text

   tutor_prefix, _tutor_variables = split_template(tutor_text)
   lowered_prefix = tutor_prefix.lower()

   assert "never" in lowered_prefix
   assert "final answer" in lowered_prefix
   assert "before the student has submitted" in lowered_prefix

   rendered_feedback = render_template(feedback_text, FEEDBACK_PAYLOAD)

   for value in FEEDBACK_PAYLOAD.values():
      assert value in rendered_feedback

   with pytest.raises(ValueError):
      render_template(feedback_text, dict(FEEDBACK_PAYLOAD, extra_field="not allowed"))

   with pytest.raises(ValueError):
      incomplete = {k: v for k, v in FEEDBACK_PAYLOAD.items() if k != "worked_solution"}
      render_template(feedback_text, incomplete)
