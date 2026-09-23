"""docs/plan/11-phased-delivery.md P1 scope item 13, the golden test on templates.

docs/plan/03-diagnosis-and-feedback.md, Who composes the string in P1 (R35): the tutor
receives exactly the four fields app/feedback/render.py produces for elaborated feedback,
and nothing wider. The tutor practice template never receives an answer key or a worked
solution, because it renders during practice, before the student has submitted.
"""
import hashlib
import json
import re
from pathlib import Path

import pytest

from app.feedback import tutor
from app.providers.base import render_template, split_template

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TUTOR_TEMPLATE = REPO_ROOT / "prompts" / "tutor" / "guardrailed_practice_v1.md"
FEEDBACK_TEMPLATE = REPO_ROOT / "prompts" / "feedback" / "elaborated_v1.md"
FEEDBACK_TEMPLATES = sorted({FEEDBACK_TEMPLATE, tutor.TEMPLATE_PATH})
PROMPTS_DIR = REPO_ROOT / "prompts"
GOLDENS_DIR = REPO_ROOT / "tests" / "fixtures" / "prompt_goldens"

VERSION_SUFFIX = re.compile(r"_v(\d+)\.md$")

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


def discovered_templates():
   """Every template under prompts/, found by scanning the directory rather than named by hand."""
   return sorted(PROMPTS_DIR.rglob("*.md"))


def golden_path_for(template_path):
   relative = template_path.relative_to(PROMPTS_DIR)
   flat_name = str(relative).replace("/", "__")

   return GOLDENS_DIR / f"{flat_name}.json"


def digest_of(template_path):
   return hashlib.sha256(template_path.read_bytes()).hexdigest()


def test_prompt_templates_are_versioned_and_golden():
   assert TUTOR_TEMPLATE.exists()
   assert FEEDBACK_TEMPLATE.exists()

   templates = discovered_templates()

   assert len(templates) > 0

   for template_path in templates:
      display_name = template_path.relative_to(REPO_ROOT)
      version_match = VERSION_SUFFIX.search(template_path.name)

      assert version_match is not None, f"{display_name} carries no _v<n> version marker"

      golden_path = golden_path_for(template_path)

      assert golden_path.exists(), f"no committed golden digest for {display_name}"

      golden = json.loads(golden_path.read_text())
      current_version = f"v{version_match.group(1)}"
      current_digest = digest_of(template_path)

      assert golden["version"] == current_version, (
         f"{display_name} golden records version {golden['version']}, "
         f"the file name says {current_version}"
      )
      assert golden["sha256"] == current_digest, (
         f"{display_name} no longer matches its committed golden digest; "
         "bump the version and record a new golden if the template changed on purpose"
      )

   tutor_text = TUTOR_TEMPLATE.read_text()
   feedback_texts = [template_path.read_text() for template_path in FEEDBACK_TEMPLATES]

   forbidden_em_dash = chr(0x2014)
   forbidden_en_dash_spaced = " " + chr(0x2013) + " "

   for text in (tutor_text, *feedback_texts):
      assert forbidden_em_dash not in text
      assert forbidden_en_dash_spaced not in text

   tutor_prefix, _tutor_variables = split_template(tutor_text)
   lowered_prefix = tutor_prefix.lower()

   assert "never" in lowered_prefix
   assert "final answer" in lowered_prefix
   assert "before the student has submitted" in lowered_prefix

   for feedback_text in feedback_texts:
      rendered_feedback = render_template(feedback_text, FEEDBACK_PAYLOAD)

      for value in FEEDBACK_PAYLOAD.values():
         assert value in rendered_feedback

      with pytest.raises(ValueError):
         render_template(feedback_text, dict(FEEDBACK_PAYLOAD, extra_field="not allowed"))

      with pytest.raises(ValueError):
         incomplete = {k: v for k, v in FEEDBACK_PAYLOAD.items() if k != "worked_solution"}
         render_template(feedback_text, incomplete)
