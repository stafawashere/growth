"""11 P6 eval_prompt_goldens: every prompt template in the repository produces output that is valid
against its contract, checked on the output recorded for it. tests/providers/test_prompts.py pins
each template's text by digest; this pins what each template's answers look like.

Runtime templates are checked on recorded calls. The grader's two templates and the transcriber's
are replayed through the P3 books by the production code, and each recorded answer is validated
against the output schema its request carried, attributed to its template by the request's static
prefix. The diagnostician's answer is the one recorded in the paper-to-grade book. The tutor's
elaborated template is checked on the eight live Haiku recordings against the rules the template
states for its paragraph, and the practice tutor on its one live recording. The tutor's two other
templates and the memory role's are checked on calls recorded on the operator's subscription by
tools/record_prompt_outputs.py, on the routed model, against the rules each template states. The
live agent's second template is checked on the golden set's acceptable replies that draw, each
split, compiled and checked as the route does.

The offline templates are checked on what they produced and the repository keeps: every generation
template module builds a draw that passes the gate's per-draw checks, the figure and calculator
drafts among them included; every generated bank's blind formulations cover every item; the
Monte Carlo triage template's product, a family with zero failures, is rerun at full size on three
templates; and the lessons each lesson template wrote pass every lint of tools/check_lessons.py.
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
from app.providers.model_routing import model_for
from tools import p3_evals
from tools.check_lessons import Context as LessonContext
from tools.check_lessons import check_lesson

REPO_ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = REPO_ROOT / "prompts"
CASSETTES = REPO_ROOT / "tests" / "fixtures" / "provider_cassettes"
PAPER_TO_GRADE_BOOK = REPO_ROOT / "tests" / "fixtures" / "grading_cassettes" / "paper_to_grade.json"
CONTENT_DIR = REPO_ROOT / "content"
LESSONS_DIR = CONTENT_DIR / "lessons"
LESSON_FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "lessons"

EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)
PLAIN_TEXT_FORBIDDEN = ("$", "\\", "*", "_", "[\"", EM_DASH, EN_DASH, "\n\n")
MATHJSON_HEADS = re.compile(r"\b(Multiply|Add|Subtract|Divide|Power|Sin|Cos|Rational)\b")
PRACTICE_MAX_WORDS = 80
MONTE_CARLO_SAMPLE = 3
LESSON_SAMPLE = 3
REINFORCEMENT_MAX_SENTENCES = 2
SENTENCE_END = re.compile(r"[.?!](?:\s|$)")
BELIEF_WORDS = re.compile(r"\b(believes|thinks|confused)\b", re.IGNORECASE)


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


def check_agent_live(_replayed_calls):
   """No live agent call is recorded yet, so the output checked is the golden set's acceptable
   candidate replies, each streamed through the output screen on the packet its turn composes."""
   from app.agent.screen import SentenceScreen
   from app.content.loader import load_snapshot
   from app.evals import agent_checks, golden
   from app.runtime.context import DEFAULT_CONTENT_ROOT

   document = golden.load_set("agent")
   items = golden.bank_items()
   context = golden.agent_context(load_snapshot(DEFAULT_CONTENT_ROOT))
   screened = 0

   for case in document["cases"]:
      item = items.get(case.get("item_id"))
      forms = agent_checks.key_forms(item) if item is not None else None

      for index, entry in enumerate(case["turns"]):
         if not entry["acceptable"]:
            continue

         screen = SentenceScreen(golden.agent_turn_packet(case, index, context, items), forms)
         released = screen.feed(entry["candidate_reply"]) + screen.flush()

         assert screen.withheld is None, (case["id"], index)
         assert "".join(released) == entry["candidate_reply"]
         screened += 1

   assert screened > 0


def check_agent_decline(_replayed_calls):
   from app.agent.screen import decline_text
   from app.evals import agent_checks

   decline = decline_text()
   facts = {"mode": "browsing", "turn_index": 0, "rules": (), "ids": ()}

   assert decline.startswith("That reply would have given away part of the answer")
   assert all(verdict.passed for verdict in agent_checks.run_checks(decline, facts, None, agent_checks.SENTENCE_CHECKS))


def recordings(pattern, template):
   paths = sorted(CASSETTES.glob(pattern))

   assert len(paths) > 0, pattern

   for path in paths:
      recording = json.loads(path.read_text())

      assert recording["recorded"] is True, path.name
      assert recording["template"] == template, path.name
      assert recording["model"] == model_for(recording["role"]), path.name

      yield path, recording


def check_correct_reinforcement(_replayed_calls):
   assert tutor.TEMPLATES[tutor.CORRECT_REINFORCEMENT] == PROMPTS_DIR / "tutor" / "correct_reinforcement_v1.md"

   for path, recording in recordings("tutor_correct_reinforcement_live_*.json", "prompts/tutor/correct_reinforcement_v1.md"):
      text = recording["text"]

      assert plain_paragraph_problems(text) == [], path.name
      assert len(SENTENCE_END.findall(text)) <= REINFORCEMENT_MAX_SENTENCES, path.name
      assert "?" not in text, path.name


def check_frq_points(_replayed_calls):
   assert tutor.TEMPLATES[tutor.FRQ_POINTS] == PROMPTS_DIR / "tutor" / "frq_points_v1.md"

   for path, recording in recordings("tutor_frq_points_live_*.json", "prompts/tutor/frq_points_v1.md"):
      text = recording["text"]
      named_parts = set(re.findall(r"Part \((\w)\)", recording["rendered_message"]))

      assert plain_paragraph_problems(text) == [], path.name
      assert BELIEF_WORDS.search(text) is None, path.name
      assert len(named_parts) > 0, path.name
      assert all(f"({part})" in text for part in named_parts), path.name


def consolidation_rejections(pattern, template):
   """Each recorded consolidation's proposals, with the rule app/agent/memory.py would reject each
   one under, or None, on the turns and skills the recorded request carried."""
   from app.agent import consolidate, memory
   from app.providers.notices import fields_from_rendered

   _prefix, variable_section = split_template((REPO_ROOT / template).read_text())
   pieces = re.split(r"\{\{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\}\}", variable_section)
   rejections = []

   for path, recording in recordings(pattern, template):
      fields = fields_from_rendered(pieces, recording["rendered_message"])
      document = consolidate.parsed_output(recording["text"])

      assert fields is not None, path.name
      assert document is not None, path.name
      assert len(document["proposals"]) > 0, path.name

      turn_ids = {turn["id"] for turn in json.loads(fields["turns"])}
      active_skill_ids = set(json.loads(fields["active_skill_ids"]))
      has_entries = len(json.loads(fields["active_entries"])) > 0

      for proposal in document["proposals"]:
         proposal_fields = memory.proposal_fields(proposal)
         is_targeted = proposal["operation"] in memory.TARGETED_OPERATIONS

         targets_a_missing_entry = is_targeted and not has_entries

         assert proposal_fields is not None, (path.name, proposal)
         assert not targets_a_missing_entry, (path.name, proposal)

         reason = memory.rejection_reason(proposal_fields, None, turn_ids, active_skill_ids)
         rejections.append((path.name, proposal["text"], reason))

   return rejections


def check_memory_consolidate_v1(_replayed_calls):
   """Superseded by v2. Its one recording keeps every proposal well formed and inside the
   conversation, and loses one of three to the content screen, an entry kept in the student's words
   ("I always forget...") that the instruction words of app/agent/memory.py drop; v2 asks for the
   meaning without those words."""
   from app.agent import memory

   rejections = consolidation_rejections("memory_consolidate_v1_live_*.json", "prompts/memory/consolidate_v1.md")
   reasons = [reason for _name, _text, reason in rejections]

   assert set(reasons) <= {None, memory.REJECTED_CONTENT_SCREEN}


def check_memory_consolidate_v2(_replayed_calls):
   from app.agent import consolidate

   assert consolidate.TEMPLATE_PATH == PROMPTS_DIR / "memory" / "consolidate_v2.md"

   rejections = consolidation_rejections("memory_consolidate_v2_live_*.json", "prompts/memory/consolidate_v2.md")

   assert [entry for entry in rejections if entry[2] is not None] == []


def check_agent_live_v2(replayed_calls):
   """The prose of every acceptable reply passes the screen as for live_v1, and every acceptable
   reply that draws is read, compiled and passes every figure and marks check the route applies."""
   from app.agent import context as agent_context
   from app.content.loader import load_snapshot
   from app.evals import agent_checks, golden
   from app.runtime.context import DEFAULT_CONTENT_ROOT

   assert agent_context.LIVE_TEMPLATE_PATH == PROMPTS_DIR / "agent" / "live_v2.md"

   check_agent_live(replayed_calls)
   document = golden.load_set("agent")
   items = golden.bank_items()
   context = golden.agent_context(load_snapshot(DEFAULT_CONTENT_ROOT))
   drawn = 0

   for case in document["cases"]:
      item = items.get(case.get("item_id"))
      forms = golden.agent_key_forms(case, item)

      for index, entry in enumerate(case["turns"]):
         split = golden.agent_split_reply(entry["candidate_reply"])
         draws = split.opens_figure or split.opens_marks
         is_acceptable_drawing = entry["acceptable"] and draws

         if not is_acceptable_drawing:
            continue

         packet = golden.agent_turn_packet(case, index, context, items)
         facts = agent_checks.facts_from_packet(packet, index)
         verdicts = golden.agent_turn_verdicts(entry, packet, facts, forms)

         if split.opens_figure:
            assert golden.agent_figure_reading(split).source is not None, (case["id"], index)

         assert all(verdict.passed for verdict in verdicts.values()), (case["id"], index)
         drawn += 1

   assert drawn > 0


def lessons_naming(directory, prompt_version):
   named = []

   for path in sorted(directory.glob("*.json")):
      lesson = json.loads(path.read_text())
      provenance = lesson.get("provenance") or {}

      if provenance.get("prompt_version") == prompt_version:
         named.append((path, lesson))

   return named


def lesson_context():
   from app.content.loader import load_snapshot

   return LessonContext(load_snapshot(REPO_ROOT / "data"))


def check_generator_lesson_v1(_replayed_calls):
   """Superseded by v2: every served lesson was transcribed to v2, so no lesson in content names v1.
   The v1 output the repository keeps is the decision lesson control, which passes every lint."""
   assert lessons_naming(LESSONS_DIR, "generator/lesson_v1") == []

   kept = dict(lessons_naming(LESSON_FIXTURES_DIR, "generator/lesson_v1"))
   decision_control = kept[LESSON_FIXTURES_DIR / "decision_clean.json"]

   assert check_lesson(decision_control, lesson_context()) == {}


def check_generator_lesson_v2(_replayed_calls):
   lessons = lessons_naming(LESSONS_DIR, "generator/lesson_v2")
   served = sorted(LESSONS_DIR.glob("*.json"))

   assert len(lessons) > 0
   assert len(lessons) == len(served)

   chosen = lessons[:: max(1, len(lessons) // LESSON_SAMPLE)][:LESSON_SAMPLE]
   context = lesson_context()

   for path, lesson in chosen:
      assert check_lesson(lesson, context) == {}, path.name


OUTPUT_GOLDENS = {
   "agent/decline_v1.md": check_agent_decline,
   "agent/live_v1.md": check_agent_live,
   "agent/live_v2.md": check_agent_live_v2,
   "diagnostician/error_hypotheses_v1.md": check_diagnostician,
   "feedback/elaborated_v1.md": check_elaborated_v1,
   "feedback/elaborated_v2.md": check_elaborated_v2,
   "generator/calculator_v1.md": check_generator_calculator,
   "generator/figure_spec_v1.md": check_generator_figure_spec,
   "generator/lesson_v1.md": check_generator_lesson_v1,
   "generator/lesson_v2.md": check_generator_lesson_v2,
   "generator/template_v1.md": check_generator_template,
   "grader/point_liberal_v2.md": check_grader_liberal,
   "grader/point_strict_v2.md": check_grader_strict,
   "memory/consolidate_v1.md": check_memory_consolidate_v1,
   "memory/consolidate_v2.md": check_memory_consolidate_v2,
   "transcriber/readback_v1.md": check_transcriber,
   "tutor/correct_reinforcement_v1.md": check_correct_reinforcement,
   "tutor/frq_points_v1.md": check_frq_points,
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
