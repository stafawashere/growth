"""11 P6 eval_prompt_goldens: every prompt template in the repository produces output that is valid
against its contract, checked on the output recorded for it. tests/providers/test_prompts.py pins
each template's text by digest; this pins what each template's answers look like.

Runtime templates are checked on recorded calls. The grader's two templates and the transcriber's
are replayed through the P3 books by the production code, and each recorded answer is validated
against the output schema its request carried, attributed to its template by the request's static
prefix. The diagnostician's answer is the one recorded in the paper-to-grade book. The tutor's
elaborated template is checked on the eight live Haiku recordings against the rules the template
states for its paragraph, and the practice tutor on its one live recording.

The offline templates are checked on what they produced and the repository keeps: every generation
template module builds a draw that passes the gate's per-draw checks, the figure and calculator
drafts among them included; every generated bank's blind formulations cover every item; and the
Monte Carlo triage template's product, a family with zero failures, is rerun at full size on three
templates.
"""
import importlib
import json
import re
from pathlib import Path

import jsonschema
import pytest

from app.diagnosis import observe
from app.feedback import tutor
from app.generation import spec as spec_module
from app.generation.template import (
   FAMILY_DRAWS,
   build,
   check_instance,
   error_ids_for_skills,
   library,
   run_family,
   spec_for,
   template_modules,
)
from app.grading import judge, transcribe
from app.providers.base import split_template
from app.providers.cassette_book import CassetteBookProvider
from tools import p3_evals

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = REPO_ROOT / "prompts"
CASSETTES = REPO_ROOT / "tests" / "fixtures" / "provider_cassettes"
PAPER_TO_GRADE_BOOK = REPO_ROOT / "tests" / "fixtures" / "grading_cassettes" / "paper_to_grade.json"
CONTENT_DIR = REPO_ROOT / "content"

EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)
PLAIN_TEXT_FORBIDDEN = ("$", "\\", "*", "_", "[\"", EM_DASH, EN_DASH, "\n\n")
MATHJSON_HEADS = re.compile(r"\b(Multiply|Add|Subtract|Divide|Power|Sin|Cos|Rational)\b")
PRACTICE_MAX_WORDS = 80
MONTE_CARLO_SAMPLE = 3


class RecordingBook(CassetteBookProvider):
   calls = []

   def generate(self, request):
      result = super().generate(request)
      RecordingBook.calls.append((request.system, request.output_schema, result.text))

      return result


@pytest.fixture(scope="module")
def replayed_calls():
   original = p3_evals.CassetteBookProvider
   RecordingBook.calls = []
   p3_evals.CassetteBookProvider = RecordingBook

   try:
      measured = p3_evals.measures()[0]
   finally:
      p3_evals.CassetteBookProvider = original

   assert measured["misses"] == 0

   return list(RecordingBook.calls)


def static_prefix(template_path):
   return split_template(template_path.read_text())[0]


def schema_valid_answers(calls, template_path):
   prefix = static_prefix(template_path)
   answers = [(schema, text) for system, schema, text in calls if system == prefix]

   for schema, text in answers:
      jsonschema.validate(json.loads(text), schema)

   return len(answers)


def check_grader_liberal(replayed_calls):
   assert schema_valid_answers(replayed_calls, judge.STANDARD_TEMPLATE) > 0


def check_grader_strict(replayed_calls):
   assert schema_valid_answers(replayed_calls, judge.STRICT_TEMPLATE) > 0


def check_transcriber(replayed_calls):
   assert schema_valid_answers(replayed_calls, transcribe.TEMPLATE_PATH) > 0


def check_diagnostician(_replayed_calls):
   book = json.loads(PAPER_TO_GRADE_BOOK.read_text())
   observations = []

   for entry in book.values():
      answer = json.loads(entry["text"])
      is_observation = "observed_errors" in answer

      if is_observation:
         observations.append(answer)

   assert observe.TEMPLATE_PATH == PROMPTS_DIR / "diagnostician" / "error_hypotheses_v1.md"
   assert len(observations) > 0

   for answer in observations:
      jsonschema.validate(answer, observe.OBSERVATION_SCHEMA)


def plain_paragraph_problems(text):
   problems = [token for token in PLAIN_TEXT_FORBIDDEN if token in text]
   problems.extend(MATHJSON_HEADS.findall(text))

   if not text.strip():
      problems.append("empty")

   return problems


def check_elaborated_v2(_replayed_calls):
   recordings = sorted(CASSETTES.glob("tutor_haiku_live_*.json"))

   assert tutor.TEMPLATE_PATH == PROMPTS_DIR / "feedback" / "elaborated_v2.md"
   assert len(recordings) > 0

   for path in recordings:
      recording = json.loads(path.read_text())

      assert recording["recorded"] is True
      assert plain_paragraph_problems(recording["text"]) == [], path.name


def check_elaborated_v1(_replayed_calls):
   """Superseded by v2 and served by nothing; its golden is the hand-written stand-in gate 23 was
   built on, which says so in the file."""
   recording = json.loads((CASSETTES / "tutor_elaborated_v1.json").read_text())

   assert recording["synthetic"] is True
   assert plain_paragraph_problems(recording["text"]) == []


def check_guardrailed_practice(_replayed_calls):
   recording = json.loads((CASSETTES / "tutor_guardrailed_practice_v1.json").read_text())
   text = recording["text"]

   assert recording["recorded"] is True
   assert recording["template"] == "prompts/tutor/guardrailed_practice_v1.md"
   assert plain_paragraph_problems(text) == []
   assert "?" in text
   assert len(text.split()) <= PRACTICE_MAX_WORDS
   assert not re.search(r"\b6\b", text)


def one_draw_per_template():
   for archetype_id, module in sorted(template_modules().items()):
      archetype = library().archetypes[archetype_id]
      spec = spec_for(module)
      _parameters, names = spec_module.draw_with_seed(spec, f"{archetype_id}:output-golden:0")
      instance = build(module, names)
      failures = check_instance(instance, archetype, spec, names, error_ids_for_skills(library(), archetype["skills"]))

      yield archetype_id, instance, failures


def check_generator_template(_replayed_calls):
   checked = [(archetype_id, failures) for archetype_id, _instance, failures in one_draw_per_template()]
   failing = [(archetype_id, failures) for archetype_id, failures in checked if failures]

   assert len(checked) == len(library().archetypes)
   assert failing == []


def check_generator_figure_spec(_replayed_calls):
   with_figures = [(archetype_id, failures) for archetype_id, instance, failures in one_draw_per_template() if instance.figure]

   assert len(with_figures) > 0
   assert [entry for entry in with_figures if entry[1]] == []


def is_numeric_calculator_item(instance):
   is_calculator = instance.calculator_status == "calculator"
   is_numeric = instance.key.form == "numeric"

   return is_calculator and is_numeric


def check_generator_calculator(_replayed_calls):
   """calculator_v1 governs a calculator item whose answer is a number; a calculator verdict item
   is a statement item and answers to template_v1 alone."""
   calculator_draws = [
      (archetype_id, instance, failures)
      for archetype_id, instance, failures in one_draw_per_template()
      if is_numeric_calculator_item(instance)
   ]

   assert len(calculator_draws) > 0

   for archetype_id, instance, failures in calculator_draws:
      assert failures == [], archetype_id
      assert instance.key.decimals == 3, archetype_id
      assert instance.setup_required is True, archetype_id


def check_verifier_independent_resolve(_replayed_calls):
   banks = sorted(CONTENT_DIR.glob("items_gen_unit*"))

   assert len(banks) > 0

   for bank in banks:
      formulations = importlib.import_module(f"content.{bank.name}.key_formulations").FORMULATIONS
      item_ids = {path.stem for path in bank.glob("ITM-*.json")}

      assert item_ids <= set(formulations), bank.name
      assert all(callable(formulations[item_id]) for item_id in item_ids), bank.name


def check_verifier_monte_carlo(_replayed_calls):
   modules = template_modules()
   chosen = sorted(modules)[:: max(1, len(modules) // MONTE_CARLO_SAMPLE)][:MONTE_CARLO_SAMPLE]

   for archetype_id in chosen:
      report = run_family(modules[archetype_id], draws=FAMILY_DRAWS)

      assert report.draws == FAMILY_DRAWS
      assert report.failures == [], archetype_id
      assert report.passed, archetype_id


OUTPUT_GOLDENS = {
   "diagnostician/error_hypotheses_v1.md": check_diagnostician,
   "feedback/elaborated_v1.md": check_elaborated_v1,
   "feedback/elaborated_v2.md": check_elaborated_v2,
   "generator/calculator_v1.md": check_generator_calculator,
   "generator/figure_spec_v1.md": check_generator_figure_spec,
   "generator/template_v1.md": check_generator_template,
   "grader/point_liberal_v1.md": check_grader_liberal,
   "grader/point_strict_v1.md": check_grader_strict,
   "transcriber/readback_v1.md": check_transcriber,
   "tutor/guardrailed_practice_v1.md": check_guardrailed_practice,
   "verifier/independent_resolve_v1.md": check_verifier_independent_resolve,
   "verifier/monte_carlo_v1.md": check_verifier_monte_carlo,
}


def test_every_template_has_an_output_golden():
   discovered = {str(path.relative_to(PROMPTS_DIR)) for path in PROMPTS_DIR.rglob("*.md")}

   assert discovered == set(OUTPUT_GOLDENS)


@pytest.mark.parametrize("template", sorted(OUTPUT_GOLDENS))
def eval_prompt_goldens(template, replayed_calls):
   OUTPUT_GOLDENS[template](replayed_calls)
