"""Operator command-line check over a directory of lesson records: every deterministic check of
docs/plan/15-lessons.md, Sourcing, authoring and verification, step 2, and Methods, what this
adds to the checker.

Exit 0 only when every lesson is clean. Nothing is written and no database is touched. The
checks reuse app/items (equivalence, numeric_check, run_checks, error_path_findings), the
duplicate gate's official-corpus index in app/generation/dedupe.py, and the quote rule of
qa/07_quotes.py, reimplemented over content/lessons.

Where a lint and tools/check_lesson_designs.py cover the same rule, the lint mirrors the design
checker's rule, because a faithful transcription of a design that passes the design checker must
pass here (docs/lessons/BUILD-PLAN.md, amendments A-D1 to A-D5 and A-1 to A-8, which were written
against the design checker). The design checker is imported lazily (design_rules below), since it
imports this module.

Usage: python3 tools/check_lessons.py <file or directory> [<file or directory> ...]
       python3 tools/check_lessons.py --sets
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import jsonschema
import sympy
from jsonschema.exceptions import best_match

from app.content.loader import LoaderError, load_snapshot
from app.generation import dedupe
from app.items import verify
from app.items.ingest import run_checks
from app.items.distractor_paths import error_ids_for_skills
from app.items.mathjson import UnsupportedMathJSON, to_sympy
from app.lessons import constants, plan
from app.lessons.confusable import confusable_sets
from app.lessons.source import CACHE_TEXT_DIR, UNITS_DIR, authoring_bundle, reader_checks

DATA_ROOT = ROOT / "data"
SCHEMA_PATH = ROOT / "schemas" / "lessons" / "lesson.schema.json"
CONTENT_DIR = ROOT / "content"


def load_common():
   spec = importlib.util.spec_from_file_location("schemas_common", ROOT / "schemas" / "common.py")
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)

   return module


COMMON = load_common()

TYPE_ORDER = (
   plan.ORIENTATION,
   plan.KEY_IDEAS,
   plan.STRATEGY,
   plan.WORKED_EXAMPLE,
   plan.READER_SCORES,
   plan.COMMON_ERROR,
   plan.REPRESENTATIONS,
   plan.PREREQUISITE_BRIDGE,
)

DASH_CODES = (8212, 8211)
DASHES = re.compile("[" + "".join(chr(code) for code in DASH_CODES) + "]")
EMOJI_RANGES = ((0x1F300, 0x1FAFF), (0x2600, 0x27BF), (0xFE0F, 0xFE0F), (0x2B00, 0x2BFF))
EMOJI = re.compile("[" + "".join(f"{chr(low)}-{chr(high)}" for low, high in EMOJI_RANGES) + "]")
PRAISE = re.compile(
   r"\b(great|excellent|well done|nice work|good job|awesome|fantastic|perfect|congratulations|"
   r"brilliant|impressive|amazing|wonderful)\b",
   re.I,
)
STUDY_ADVICE = re.compile(
   r"\b(study|studying|practi[cs]e|practi[cs]ing|revise|revision|memori[sz]e|remember to|"
   r"make sure to|you should|you need to|try to|tip:|review your notes)\b",
   re.I,
)
SCHEDULE = re.compile(
   r"\b(daily|weekly|every (day|week|morning|evening)|each (day|week)|per day|per week|"
   r"schedule|timetable|days a week|hours a day|minutes a day|by tomorrow|next week)\b",
   re.I,
)
SECOND_PERSON_BELIEF = re.compile(
   r"\byou (believe|think|assume|feel|thought|expect|figure|suppose|imagine)\b|"
   r"\byour (belief|assumption|misconception|idea that)\b",
   re.I,
)
SCORING_CITATION = re.compile(r"\b(?:sg|cr)-\d{2}:\d+\b")

DELIVERED_TYPES = (plan.ORIENTATION, plan.KEY_IDEAS, plan.WORKED_EXAMPLE, plan.COMMON_ERROR, plan.REPRESENTATIONS)
STEP_REVEAL_TYPES = (plan.WORKED_EXAMPLE, plan.COMMON_ERROR)
UNDRAWN_MODES = ("text", "step_reveal")
SPEC_KINDS = (
   "graph",
   "table",
   "graph_panels",
   "stacked_graphs",
   "graph_pair",
   "graph_with_table",
   "slope_field",
   "implicit_curve",
   "region",
   "diagram",
   "geometric_diagram",
   "parametric_path",
   "vector_diagram",
   "washer",
   "slice_shapes",
   "graph_sweep",
   "graph_zoom",
   "numeric_experiment",
   "particle_on_line",
   "number_line_pair",
   "parametric_trace",
   "solid_from_slices",
   "solid_of_revolution",
   "euler_steps",
   "solution_curves",
   "field_trace",
   "inverse_pair",
   "table_sweep",
   "panels",
   "region_with_axis",
   "stems",
)
RESEARCH_CITATION = re.compile(r"^research/[\w\-/.]+\.md(?:#.+)?$")
PAGE_CITATION = re.compile(r"^(ced|sg-\d{2}|cr-\d{2}|crabbc-\d{2}):(\d+)$")


def design_rules():
   """tools/check_lesson_designs, imported on first use because it imports this module."""
   from tools import check_lesson_designs

   return check_lesson_designs


def normalise_text(text):
   return re.sub(r"[^a-z0-9]+", " ", (text or "").lower()).strip()


def words_in(text):
   return len((text or "").split())


class Context:
   """Everything a lint reads besides the lesson: the snapshot and the lazily built corpora."""

   def __init__(self, snapshot, units_dir=UNITS_DIR, cache_dir=CACHE_TEXT_DIR, content_dir=CONTENT_DIR):
      self.snapshot = snapshot
      self.units_dir = units_dir
      self.cache_dir = cache_dir
      self.content_dir = Path(content_dir)
      self.bundles = {}
      self.official = None
      self.draws = None
      self.active_error_ids = frozenset(snapshot.errors)

   def bundle(self, concept_id):
      is_missing = concept_id not in self.bundles

      if is_missing:
         self.bundles[concept_id] = authoring_bundle(
            concept_id, self.snapshot, self.units_dir, self.cache_dir
         )

      return self.bundles[concept_id]

   def official_index(self):
      has_no_index = self.official is None

      if has_no_index:
         pages = dedupe.load_official_pages(self.cache_dir)
         self.official = dedupe.OfficialShingleIndex(pages)

      return self.official

   def published_draws(self, archetype_id):
      has_no_draws = self.draws is None

      if has_no_draws:
         self.draws = {}

         for path in sorted(self.content_dir.glob("items_*/*.json")):
            record = json.loads(path.read_text())
            archetype = record.get("archetype_id")
            draw = record.get("parameter_draw")
            has_draw = archetype is not None and draw is not None

            if has_draw:
               self.draws.setdefault(archetype, []).append((record.get("id"), draw))

      return self.draws.get(archetype_id, [])


def sections_of(lesson, section_type):
   return [section for section in lesson["sections"] if section["type"] == section_type]


def is_decision(lesson):
   return lesson.get("kind") == "decision"


def concept_skill_ids(lesson, context):
   """The skills the lesson teaches: the concept's, the decision set's, or none for a
   prerequisite lesson."""
   if is_decision(lesson):
      return list(lesson["decision"]["skills"])

   is_concept = lesson["kind"] == "concept"

   if is_concept:
      return list(context.snapshot.concepts[lesson["target_id"]]["skills"])

   return []


def to_expression(mathjson):
   return to_sympy(mathjson)


def contains_float(node):
   if isinstance(node, bool):
      return False

   if isinstance(node, float):
      return True

   if isinstance(node, list):
      return any(contains_float(child) for child in node)

   return False


def prose_of(lesson):
   """Every sentence a reader meets, without the anchor quotes, which are the cited page's words."""
   texts = []

   for record in list(lesson["sections"]) + list(lesson["checks"]):
      texts.extend(plan.section_texts(record))

      for option in record.get("options") or []:
         has_label = bool(option.get("label"))

         if has_label:
            texts.append(option["label"])

   for stem in (lesson.get("decision") or {}).get("stems", []):
      texts.append(stem["text"])
      texts.append(stem["method"])

   return texts


VERBATIM_FIELDS = {
   plan.READER_SCORES: ("lines[].text",),
   plan.COMMON_ERROR: ("observed_behavior", "scoring_consequence"),
}


def authored_prose(lesson):
   """prose_of without the fields copied verbatim from library records (the reader_checks lines
   and an error's behaviour and consequence), which rule_style leaves out as authored_record
   does, since the author did not write them."""
   verbatim = []

   for section in lesson["sections"]:
      for path in VERBATIM_FIELDS.get(section["type"], ()):
         verbatim.extend(plan.prose_values(section, path))

   return [text for text in prose_of(lesson) if text not in verbatim]


def raw_text(lesson):
   return json.dumps(lesson, ensure_ascii=False)


def valued_steps(record):
   """Positions and expressions of the steps that carry a value, for an example or a check."""
   is_example = record.get("type") == plan.WORKED_EXAMPLE
   steps = record["steps"] if is_example else record["worked_solution"]
   key = "expression" if is_example else "mathjson"
   found = []

   for index, step in enumerate(steps):
      has_value = key in step

      if has_value:
         found.append((index, step[key]))

   return found


def solved_records(lesson):
   return sections_of(lesson, plan.WORKED_EXAMPLE) + list(lesson["checks"])


# lint functions


def lint_schema(lesson, context):
   schema = json.loads(SCHEMA_PATH.read_text())
   validator = jsonschema.Draft202012Validator(schema)
   errors = sorted(validator.iter_errors(lesson), key=lambda error: list(error.absolute_path))
   messages = []

   for error in errors[:5]:
      deepest = best_match([error])
      location = "/".join(str(part) for part in deepest.absolute_path) or "<root>"
      messages.append(f"{location}: {deepest.message[:160]}")

   return messages


def id_number(identifier):
   return identifier.rsplit("-", 1)[1]


def lint_referential(lesson, context):
   snapshot = context.snapshot
   messages = []
   kind_prefix = {"concept": "LSN-CON", "prerequisite": "LSN-PRQ", "decision": "LSN-DEC"}
   expected_prefix = kind_prefix[lesson["kind"]]

   if not lesson["id"].startswith(expected_prefix):
      messages.append(f"id {lesson['id']} does not match kind {lesson['kind']}")

   is_concept = lesson["kind"] == "concept"
   is_prerequisite = lesson["kind"] == "prerequisite"

   if is_concept:
      names_known_concept = lesson["target_id"] in snapshot.concepts
      numbers_agree = id_number(lesson["id"]) == id_number(lesson["target_id"])

      if not names_known_concept:
         messages.append(f"target {lesson['target_id']} is not an active concept")
         return messages

      if not numbers_agree:
         messages.append(f"id {lesson['id']} does not name target {lesson['target_id']}")

   if is_prerequisite:
      names_known_prerequisite = lesson["target_id"] in snapshot.prerequisites

      if not names_known_prerequisite:
         messages.append(f"target {lesson['target_id']} is not an active prerequisite")

   for identifier in sorted(set(COMMON.ANY_ID.findall(raw_text(lesson)))):
      record = snapshot.ids.get(identifier)
      is_active = record is not None and record.get("status") == "active"

      if not is_active:
         messages.append(f"{identifier} is not active in the snapshot")

   messages.extend(unknown_source_messages(lesson, context))
   messages.extend(unknown_archetype_messages(lesson, context))
   messages.extend(unique_id_messages(lesson))

   return messages


def unknown_source_messages(lesson, context):
   """A block's source is known when the authoring bundle holds it, or when the design checker
   would accept it: an active BC id (rule_referential), a page citation with a cached page
   (rule_citations), or a research citation whose file exists and holds the heading, in the file
   or in the bundle's topic sections (rule_research_lines)."""
   is_concept = lesson["kind"] == "concept"

   if not is_concept:
      return []

   bundle = context.bundle(lesson["target_id"])
   bundle_text = json.dumps(bundle, ensure_ascii=False)
   messages = []

   for record in lesson["sections"]:
      for source in record["sources"]:
         problem = source_problem(source, bundle, bundle_text, context)

         if problem is not None:
            messages.append(f"{record['id']} cites {source}, {problem}")

   return messages


def source_problem(source, bundle, bundle_text, context):
   is_research = RESEARCH_CITATION.match(source) is not None

   if is_research:
      return research_problem(source, bundle)

   is_page = PAGE_CITATION.match(source) is not None

   if is_page:
      return None if page_is_cached(context, source) else "which is not cached"

   is_held = f'"{source}"' in bundle_text or source in bundle_text

   if is_held:
      return None

   record = context.snapshot.ids.get(source)
   is_active = record is not None and record.get("status") == "active"

   if is_active:
      return None

   return "which the authoring bundle does not hold"


def page_is_cached(context, source):
   match = PAGE_CITATION.match(source)
   page_file = Path(context.cache_dir) / match.group(1) / f"page-{int(match.group(2)):03d}.txt"

   return page_file.exists()


def research_problem(source, bundle):
   designs = design_rules()
   file_part, _, heading = source.partition("#")
   path = ROOT / file_part

   if not path.exists():
      return "whose research file does not exist"

   heading = heading.strip()
   has_no_heading = heading == ""

   if has_no_heading:
      return None

   texts = [path.read_text()] + list((bundle.get("topic_sections") or {}).values())
   is_present = any(designs.heading_present(text, heading) for text in texts)

   if not is_present:
      return "whose heading is not in the research file or the topic sections"

   return None


def unknown_archetype_messages(lesson, context):
   messages = []
   records = list(sections_of(lesson, plan.WORKED_EXAMPLE)) + sections_of(lesson, plan.STRATEGY)
   records += list(lesson["checks"]) + list((lesson.get("decision") or {}).get("stems", []))

   for record in records:
      archetype_id = record["archetype_id"]
      is_active = archetype_id in context.snapshot.archetypes

      if not is_active:
         messages.append(f"{record['id']} names archetype {archetype_id}, which is not active")

   return messages


def unique_id_messages(lesson):
   identifiers = [record["id"] for record in lesson["sections"] + lesson["checks"]]
   repeated = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
   foreign = [identifier for identifier in identifiers if not identifier.startswith(lesson["id"] + "#")]
   messages = [f"id {identifier} appears more than once" for identifier in repeated]
   messages.extend(f"id {identifier} is not under {lesson['id']}" for identifier in foreign)

   return messages


def lint_section_order(lesson, context):
   messages = []
   ranks = [TYPE_ORDER.index(section["type"]) for section in lesson["sections"]]
   is_in_order = ranks == sorted(ranks)

   if not is_in_order:
      messages.append("sections are not in the fixed order of the content model")

   for section in lesson["sections"]:
      expected = expected_id_pattern(section, lesson["id"])
      matches = re.fullmatch(expected, section["id"]) is not None

      if not matches:
         messages.append(f"{section['id']} does not follow the id form {expected}")

   for position, check in enumerate(lesson["checks"], 1):
      expected_id = f"{lesson['id']}#chk-{position}"

      if check["id"] != expected_id:
         messages.append(f"check {check['id']} should be {expected_id}")

   return messages


def expected_id_pattern(section, lesson_id):
   base = re.escape(lesson_id)

   if section["type"] == plan.COMMON_ERROR:
      return f"{base}#err-{re.escape(section['error_id'])}"

   if section["type"] == plan.PREREQUISITE_BRIDGE:
      return f"{base}#prq-{re.escape(section['prerequisite_id'])}"

   return f"{base}#s\\d+"


def lint_structure(lesson, context):
   messages = []
   checks = lesson["checks"]
   check_count_ok = constants.LESSON_CHECKS_MIN <= len(checks) <= constants.LESSON_CHECKS_MAX

   if not check_count_ok:
      messages.append(f"{len(checks)} checks, and the model holds {constants.LESSON_CHECKS_MIN} to {constants.LESSON_CHECKS_MAX}")

   if is_decision(lesson):
      return messages

   messages.extend(cardinality_messages(lesson, context))
   messages.extend(band_shape_messages(lesson))
   messages.extend(check_shape_messages(lesson))

   return messages


def cardinality_messages(lesson, context):
   messages = []
   count_of = lambda section_type: len(sections_of(lesson, section_type))
   is_concept = lesson["kind"] == "concept"

   if count_of(plan.ORIENTATION) != 1:
      messages.append(f"{count_of(plan.ORIENTATION)} orientation sections, and the model holds exactly 1")

   if count_of(plan.REPRESENTATIONS) > 1:
      messages.append("more than one representations section")

   examples = count_of(plan.WORKED_EXAMPLE)

   if not 1 <= examples <= constants.WORKED_EXAMPLES_MAX:
      messages.append(f"{examples} worked examples, and the model holds 1 or 2")

   core_blocks = [
      section for section in sections_of(lesson, plan.KEY_IDEAS) if section["depth"] == "core"
   ]

   if len(core_blocks) > constants.KEY_IDEAS_CORE_MAX:
      messages.append(f"{len(core_blocks)} core key ideas, and the model holds at most {constants.KEY_IDEAS_CORE_MAX}")

   if not is_concept:
      return messages

   bundle = context.bundle(lesson["target_id"])
   messages.extend(bundle_alignment_messages(lesson, bundle))

   return messages


def bundle_alignment_messages(lesson, bundle):
   messages = []
   expected_eks = sorted({ek for skill in bundle["skills"] for ek in skill.get("essential_knowledge") or []})
   stated_eks = sorted(section["ek_id"] for section in sections_of(lesson, plan.KEY_IDEAS) if section.get("ek_id"))

   if stated_eks != expected_eks:
      messages.append(f"key ideas cover {stated_eks}, and the skills map {expected_eks}")

   expected_bridges = sorted(record["id"] for record in bundle["prerequisites"])
   stated_bridges = sorted(
      section["prerequisite_id"] for section in sections_of(lesson, plan.PREREQUISITE_BRIDGE)
   )

   if stated_bridges != expected_bridges:
      messages.append(f"prerequisite bridges cover {stated_bridges}, and the parents give {expected_bridges}")

   return messages


def band_shape_messages(lesson):
   messages = []
   examples = sections_of(lesson, plan.WORKED_EXAMPLE)

   if examples and examples[0]["bands"] != ["low", "mid"] and sorted(examples[0]["bands"]) != ["low", "mid"]:
      messages.append("worked example 1 must serve both bands")

   for example in examples[1:]:
      if example["bands"] != ["low"]:
         messages.append(f"{example['id']} is example 2 and serves the low band only")

   for section in sections_of(lesson, plan.KEY_IDEAS):
      is_extended = section["depth"] == "extended"

      if is_extended and section["bands"] != ["low"]:
         messages.append(f"{section['id']} is extended and serves the low band only")

   return messages


def check_shape_messages(lesson):
   messages = []
   checks = lesson["checks"]
   examples = sections_of(lesson, plan.WORKED_EXAMPLE)
   expected_kinds = ["completion", "isomorph", "mcq"][:len(checks)]
   stated_kinds = [check["check_kind"] for check in checks]

   if stated_kinds != expected_kinds:
      messages.append(f"check kinds are {stated_kinds}, and the model holds {expected_kinds}")

   for position, check in enumerate(checks):
      wanted_bands = ["low"] if position == 2 else ["low", "mid"]

      if sorted(check["bands"]) != wanted_bands:
         messages.append(f"{check['id']} should serve {wanted_bands}")

   third = checks[2] if len(checks) == 3 else None
   has_mcq_third = third is not None and (third["format"] != "mcq" or len(third.get("options") or []) != 4)

   if has_mcq_third:
      messages.append(f"{checks[2]['id']} is check 3 and must be a 4-option multiple choice")

   completion = checks[0] if checks else None
   first_example = examples[0] if examples else None

   if completion and first_example:
      completes_first = completion.get("completes") == first_example["id"]
      same_draw = completion["parameter_draw"] == first_example["parameter_draw"]

      if not completes_first or not same_draw:
         messages.append(f"{completion['id']} must complete worked example 1 on its draw")

   isomorph = checks[1] if len(checks) > 1 else None

   if isomorph and first_example:
      shares_archetype = isomorph["archetype_id"] == first_example["archetype_id"]
      repeats_draw = isomorph["parameter_draw"] == first_example["parameter_draw"]

      if not shares_archetype or repeats_draw:
         messages.append(f"{isomorph['id']} must be another draw of example 1's archetype")

   return messages


def lint_band_coverage(lesson, context):
   is_concept = lesson["kind"] == "concept"

   if not is_concept:
      return []

   wanted = set(concept_skill_ids(lesson, context))
   messages = []

   for band in constants.BANDS:
      view = plan.LessonView(lesson)
      refs = plan.first_contact_refs(view, band, ())
      teaching = [
         view.by_id[ref.id] for ref in refs if ref.type in (plan.KEY_IDEAS, plan.WORKED_EXAMPLE)
      ]
      covered = {skill for record in teaching for skill in record["skills"]}
      missing = sorted(wanted - covered)

      if missing:
         messages.append(f"band {band} does not teach {missing}")

   return messages


def valued_step_records(record):
   """The steps of an example or a check that carry a value, with their position."""
   is_example = record.get("type") == plan.WORKED_EXAMPLE
   steps = record["steps"] if is_example else record["worked_solution"]
   key = "expression" if is_example else "mathjson"

   return [(index, step[key], step) for index, step in enumerate(steps) if key in step]


def relation_holds(designs, relation, step, previous, current):
   """One link of tools/check_lesson_designs.check_chain over converted expressions: the message
   when current does not follow from previous under the step's relation, else None."""
   equivalent = designs.equivalent
   as_value = designs.as_value

   if relation == "equivalent":
      return None if equivalent(previous, current) else "is not equivalent to the step before it"

   variable = sympy.Symbol(step.get("variable", "x"))

   if relation == "differentiate":
      expected = sympy.diff(as_value(previous), variable)

      return None if equivalent(expected, current) else "is not the derivative of the step before it"

   if relation == "integrate":
      back = sympy.diff(as_value(current), variable)

      return None if equivalent(back, as_value(previous)) else "does not differentiate back to the step before it"

   if relation == "evaluate":
      substitution = {
         sympy.Symbol(name): designs.parse_expression(value) for name, value in (step.get("subs") or {}).items()
      }
      expected = as_value(previous).subs(substitution)
      is_close = equivalent(expected, current) or (step.get("approx") and designs.close_enough(expected, current))

      return None if is_close else f"is not the step before it evaluated at {step.get('subs')}"

   if relation == "solve":
      roots = as_value(current)
      candidates = list(roots) if isinstance(roots, (sympy.FiniteSet, set, tuple, list)) else [roots]
      zero_form = designs.as_zero_form(previous)
      failing = [root for root in candidates if not equivalent(zero_form.subs(variable, root), sympy.Integer(0))]

      return None if not failing else f"roots {failing} do not satisfy the step before it"

   point = designs.parse_expression(step.get("point", "0"))
   expected = sympy.limit(as_value(previous), variable, point, dir=step.get("dir", "+-"))

   return None if equivalent(expected, current) else "is not the limit of the step before it"


def step_text(step):
   return normalise_text(step.get("text") or f"{step.get('cue')} {step.get('why')}")


def chain_messages(record):
   """tools/check_lesson_designs.check_chain over a record's valued steps: each follows from the
   one before under its relation, and a step without a relation is held to equivalence, the
   design checker's default. A restatement is a step whose words and MathJSON both repeat the
   step before it: the design checker compares the SymPy strings as written, which the record
   cannot keep, because parsing evaluates "(-2)*4 + 3*5" to the 7 of the next line, and to_sympy
   evaluates a factored quotient to its cancelled form. Returns the messages and the last converted expression."""
   designs = design_rules()
   messages = []
   previous = None
   previous_value = None
   previous_step = None
   last = None

   for index, value, step in valued_step_records(record):
      try:
         current = to_expression(value)
      except (UnsupportedMathJSON, TypeError, ValueError) as error:
         messages.append(f"{record['id']} step {index + 1} did not convert: {error}")
         previous = None
         continue

      relation = step.get("relation", "equivalent")
      is_first = previous is None

      if relation not in designs.RELATIONS:
         messages.append(f"{record['id']} step {index + 1} relation {relation!r} is not one of {designs.RELATIONS}")
      elif relation == "equivalent" and not is_first and previous_step == step_text(step) and previous_value == value:
         messages.append(f"{record['id']} step {index + 1} restates the step before it")
      elif not is_first and relation != "new":
         try:
            problem = relation_holds(designs, relation, step, previous, current)
         except Exception as error:
            problem = f"did not compare: {type(error).__name__}"

         if problem is not None:
            messages.append(f"{record['id']} step {index + 1} {problem}")

      previous = current
      previous_value = value
      previous_step = step_text(step)
      last = current

   return messages, last


def lint_step_equivalence(lesson, context):
   """Mirrors the chain half of rule_steps and rule_keys: every example is chained, a check with
   a statement key is not, and a record with a key but no valued step is reported."""
   messages = []

   for record in solved_records(lesson):
      is_example = record.get("type") == plan.WORKED_EXAMPLE
      is_statement = answer_form(record) == "statement"

      if is_statement and not is_example:
         continue

      found, last = chain_messages(record)
      messages.extend(found)
      has_no_value = last is None and not valued_step_records(record)

      if has_no_value and not is_statement:
         messages.append(f"{record['id']} has no step carrying a value")

   return messages


def answer_form(record):
   is_example = record.get("type") == plan.WORKED_EXAMPLE
   answer = record["answer"] if is_example else record["answer_key"]

   return answer["form"]


def answer_expression(record):
   is_example = record.get("type") == plan.WORKED_EXAMPLE
   answer = record["answer"] if is_example else record["answer_key"]

   return to_expression(answer["mathjson"])


def last_valued_expression(record):
   converted = []

   for _, value, _ in valued_step_records(record):
      try:
         converted.append(to_expression(value))
      except (UnsupportedMathJSON, TypeError, ValueError):
         converted.append(None)

   return converted[-1] if converted else None


def key_matches(designs, key, last, is_calculator):
   return designs.equivalent(key, last) or (is_calculator and designs.close_enough(key, last))


def lint_final_answer(lesson, context):
   """Mirrors rule_steps (examples) and rule_keys (checks): the key is the last valued step, or
   within three places of it on a calculator record; a check's key equals the answer of the
   example it completes; a key option equals the key and no two options are equal."""
   designs = design_rules()
   messages = []

   for example in sections_of(lesson, plan.WORKED_EXAMPLE):
      messages.extend(example_key_messages(designs, example))

   examples = {example["id"]: example for example in sections_of(lesson, plan.WORKED_EXAMPLE)}

   for check in lesson["checks"]:
      messages.extend(check_key_messages(designs, check, examples))

   return messages


def example_key_messages(designs, example):
   is_statement = example["answer"]["form"] == "statement"
   last = last_valued_expression(example)

   if is_statement or last is None:
      return []

   try:
      key = answer_expression(example)
   except (UnsupportedMathJSON, TypeError, ValueError) as error:
      return [f"{example['id']} answer did not convert: {error}"]

   is_calculator = example["calculator_status"] == "calculator"

   if not key_matches(designs, key, last, is_calculator):
      return [f"{example['id']} answer is not the last valued step"]

   return []


def check_key_messages(designs, check, examples):
   messages = []
   options = check.get("options") or []
   key_options = [option for option in options if option.get("is_key")]

   if options and len(key_options) != 1:
      messages.append(f"{check['id']} needs exactly one key option")

   is_statement = check["answer_key"]["form"] == "statement"

   if is_statement:
      return messages

   try:
      key = answer_expression(check)
   except (UnsupportedMathJSON, TypeError, ValueError) as error:
      return messages + [f"{check['id']} key did not convert: {error}"]

   last = last_valued_expression(check)
   is_calculator = check["calculator_status"] == "calculator"

   if last is not None and not key_matches(designs, key, last, is_calculator):
      messages.append(f"{check['id']} key is not the last valued step")

   completes = examples.get(check.get("completes"))

   if completes is not None:
      messages.extend(completion_messages(designs, check, completes, key))

   messages.extend(option_messages(designs, check, options, key))

   return messages


def completion_messages(designs, check, example, key):
   try:
      answer = answer_expression(example)
   except (UnsupportedMathJSON, TypeError, ValueError):
      answer = None

   if answer is None or not designs.equivalent(answer, key):
      return [f"{check['id']} key differs from the answer of {example['id']}"]

   return []


def option_messages(designs, check, options, key):
   messages = []

   for option in options:
      if "value" not in option:
         messages.append(f"{check['id']} option {option['id']} has no value")
         continue

      try:
         value = to_expression(option["value"])
      except (UnsupportedMathJSON, TypeError, ValueError):
         messages.append(f"{check['id']} option {option['id']} did not convert")
         continue

      if option.get("is_key") and not designs.equivalent(value, key):
         messages.append(f"{check['id']} key option {option['id']} does not equal the key")

   return messages


def lint_calculator_boundary(lesson, context):
   """The calculator half of rule_steps and rule_keys: only a calculator record may state a key
   that is a three place approximation of its last step rather than equal to it. Numeric keys on
   no_calculator records are allowed, as the design checker allows them."""
   designs = design_rules()
   messages = []

   for record in solved_records(lesson):
      is_calculator = record["calculator_status"] == "calculator"
      is_statement = answer_form(record) == "statement"
      last = last_valued_expression(record)

      if is_calculator or is_statement or last is None:
         continue

      try:
         key = answer_expression(record)
      except (UnsupportedMathJSON, TypeError, ValueError):
         continue

      is_approximation = not designs.equivalent(key, last) and designs.close_enough(key, last)

      if is_approximation:
         messages.append(f"{record['id']} is {record['calculator_status']} and its key approximates its last step")

   return messages


def lint_distractor_rules(lesson, context):
   """Rejection rules 5, 6 and 7 of plan 04 as rule_keys and rule_distractor_paths state them:
   no distractor equals the key or another option under the design checker's equivalent, and
   every distractor carries an error_path. A check with a statement key compares no values, as
   rule_keys does not."""
   designs = design_rules()
   messages = []

   for check in lesson["checks"]:
      options = check.get("options") or []
      is_statement = check["answer_key"]["form"] == "statement"

      for option in options:
         is_distractor = not option.get("is_key")

         if is_distractor and not option.get("error_path"):
            messages.append(f"{check['id']} distractor {option['id']} carries no error_path")

      if is_statement:
         continue

      values = []

      for option in options:
         try:
            values.append((option, to_expression(option["value"])))
         except (KeyError, UnsupportedMathJSON, TypeError, ValueError):
            continue

      for left_index in range(len(values)):
         for right_index in range(left_index + 1, len(values)):
            left, left_value = values[left_index]
            right, right_value = values[right_index]

            if designs.equivalent(left_value, right_value):
               messages.append(f"{check['id']} options {left['id']} and {right['id']} are equal")

   return messages


def check_distractor_paths(check):
   distractors = [option for option in check.get("options") or [] if option.get("is_key") is not True]

   return [option.get("error_path") for option in distractors]


def lint_error_paths_held(lesson, context):
   if is_decision(lesson):
      return []

   held = error_ids_for_skills(context.snapshot, concept_skill_ids(lesson, context))
   messages = []

   for check in lesson["checks"]:
      paths = check_distractor_paths(check)

      for finding in verify.error_path_findings(paths, held):
         messages.append(f"{check['id']} distractor {finding['index'] + 1} error_path {finding['error_path']} is not held by the skills")

   return messages


def cited_text(context, source):
   page_number = int(source.split(":")[1])
   page_file = Path(context.cache_dir) / "ced" / f"page-{page_number:03d}.txt"
   variants = [page_file, page_file.with_suffix(".raw.txt"), page_file.with_suffix(".ocr.txt")]
   texts = [path.read_text() for path in variants if path.exists()]

   return normalise_text(" ".join(texts))


def lint_quotes(lesson, context):
   messages = []

   for section in lesson["sections"]:
      quote = section.get("quote")

      if quote is not None:
         messages.extend(quote_messages(section, quote, context))

   return messages


def prose_without_quote(record):
   texts = plan.section_texts(record)
   quote = record.get("quote")
   has_quote = quote is not None

   if not has_quote:
      return texts

   return [text for text in texts if text != quote["text"]]


def quote_messages(section, quote, context):
   messages = []
   length = words_in(quote["text"])

   if length > constants.QUOTE_WORDS_MAX:
      messages.append(f"{section['id']} quote is {length} words, and the cap is {constants.QUOTE_WORDS_MAX}")

   is_cited = quote["source"] in section["sources"]

   if not is_cited:
      messages.append(f"{section['id']} quote source {quote['source']} is not among the block's sources")

   page = cited_text(context, quote["source"])
   is_found = normalise_text(quote["text"]) in page

   if not is_found:
      messages.append(f"{section['id']} quote is not found on {quote['source']}")

   return messages


def duplicate_blocks(lesson):
   blocks = []

   for record in list(lesson["sections"]) + list(lesson["checks"]):
      texts = prose_without_quote(record)
      blocks.append((record["id"], " ".join(texts)))

   for stem in (lesson.get("decision") or {}).get("stems", []):
      blocks.append((stem["id"], stem["text"]))

   return blocks


def lint_duplicate(lesson, context):
   messages = []
   index = context.official_index()

   for block_id, text in duplicate_blocks(lesson):
      tokens = dedupe.normalise(text)
      is_too_short = len(tokens) < dedupe.SHINGLE_SIZE

      if is_too_short:
         continue

      result = index.best_match(dedupe.shingles(tokens))

      if result.hit:
         messages.append(f"{block_id} rule 10, Jaccard {result.score:.2f} with {result.neighbour}")

      run_length, where = index.longest_run(tokens)

      if run_length > dedupe.ANCHOR_QUOTE_CAP:
         messages.append(f"{block_id} rule 12, a run of {run_length} words shared with {where}")

   return messages


def lint_style(lesson, context):
   messages = []
   raw = raw_text(lesson)

   if DASHES.search(raw):
      messages.append("an em dash or en dash appears")

   if EMOJI.search(raw):
      messages.append("an emoji or pictograph appears")

   patterns = (
      ("praise", PRAISE),
      ("study advice", STUDY_ADVICE),
      ("schedule", SCHEDULE),
      ("second-person belief statement", SECOND_PERSON_BELIEF),
   )

   for text in authored_prose(lesson):
      for name, pattern in patterns:
         found = pattern.search(text)

         if found:
            messages.append(f"{name}: {found.group(0)!r} in {text[:60]!r}")

   return messages


def lint_prediction(lesson, context):
   messages = []

   for text in prose_of(lesson):
      for pattern in COMMON.FORBIDDEN_PREDICTION:
         found = re.search(pattern, text, re.I)

         if found:
            messages.append(f"predictive phrasing {found.group(0)!r} in {text[:60]!r}")

   return messages


def lint_citations(lesson, context):
   """A scoring citation in the prose is in the authoring input or, as rule_citations accepts,
   has a cached page."""
   is_concept = lesson["kind"] == "concept"

   if not is_concept:
      return []

   bundle_text = json.dumps(context.bundle(lesson["target_id"]), ensure_ascii=False)
   messages = []

   for text in prose_of(lesson):
      for citation in SCORING_CITATION.findall(text):
         is_in_input = citation in bundle_text or page_is_cached(context, citation)

         if not is_in_input:
            messages.append(f"{citation} is cited but is not in the authoring input")

   return messages


def lint_caps(lesson, context):
   messages = []
   limits = (
      (plan.ORIENTATION, constants.ORIENTATION_WORDS_MAX),
      (plan.KEY_IDEAS, constants.KEY_IDEA_WORDS_MAX),
      (plan.STRATEGY, constants.STRATEGY_WORDS_MAX),
      (plan.PREREQUISITE_BRIDGE, constants.BRIDGE_WORDS_MAX),
   )

   for section_type, limit in limits:
      for section in sections_of(lesson, section_type):
         words = capped_words(section)

         if words > limit:
            messages.append(f"{section['id']} is {words} words, and the cap is {limit}")

   for example in sections_of(lesson, plan.WORKED_EXAMPLE):
      for position, step in enumerate(example["steps"], 1):
         why_words = words_in(step["why"])

         if why_words > constants.WHY_WORDS_MAX:
            messages.append(f"{example['id']} step {position} why is {why_words} words, and the cap is {constants.WHY_WORDS_MAX}")

   errors = sections_of(lesson, plan.COMMON_ERROR)

   if len(errors) > constants.LESSON_COMMON_ERRORS_MAX:
      messages.append(f"{len(errors)} error blocks, and the cap is {constants.LESSON_COMMON_ERRORS_MAX}")

   messages.extend(band_cap_messages(lesson))

   return messages


def capped_words(section):
   """The words rule_caps counts: a key idea's text without its notation or quote, the four
   strategy fields, the orientation's or a bridge's text."""
   is_strategy = section["type"] == plan.STRATEGY

   if is_strategy:
      return sum(words_in(section[key]) for key in ("cue", "method", "rival", "separating_feature"))

   return words_in(section["text"])


def band_cap_messages(lesson):
   messages = []
   caps = {
      "full": (plan.band_words(lesson, "low"), constants.LESSON_WORDS_FULL_MAX, constants.LESSON_READ_MINUTES_MAX),
      "brief": (plan.band_words(lesson, "mid"), constants.LESSON_WORDS_BRIEF_MAX, constants.LESSON_BRIEF_MINUTES_MAX),
   }

   for form, (words, words_cap, minutes_cap) in caps.items():
      stated_words = lesson["word_count"][form]
      minutes = lesson["read_minutes"][form]
      needed_minutes = words / constants.WORDS_PER_MINUTE

      if words > words_cap:
         messages.append(f"{form} form is {words} words, and the cap is {words_cap}")

      if stated_words != words:
         messages.append(f"word_count.{form} is {stated_words}, and the sections hold {words}")

      if minutes > minutes_cap:
         messages.append(f"read_minutes.{form} is {minutes}, and the cap is {minutes_cap}")

      if minutes < needed_minutes:
         messages.append(f"read_minutes.{form} is {minutes}, below {needed_minutes:.2f} for {words} words")

   return messages


def lint_anchors(lesson, context):
   messages = []
   identifiers = {record["id"] for record in lesson["sections"] + lesson["checks"]}
   error_blocks = {section["error_id"]: section["id"] for section in sections_of(lesson, plan.COMMON_ERROR)}
   examples = sections_of(lesson, plan.WORKED_EXAMPLE)
   example_ids = {example["id"] for example in examples}

   for pointer in lesson["refresher"]:
      if pointer not in identifiers:
         messages.append(f"refresher pointer {pointer} resolves to nothing")

   expected = {section["id"] for section in lesson["sections"] if is_refresher_member(section, examples)}

   if set(lesson["refresher"]) != expected and not is_decision(lesson):
      messages.append("refresher must list the core key ideas, the error blocks and worked example 1")

   for check in lesson["checks"]:
      for path in check_distractor_paths(check):
         has_no_anchor = path not in error_blocks and not is_decision(lesson)

         if has_no_anchor:
            messages.append(f"{check['id']} distractor error_path {path} has no #err- anchor in the lesson")

      completes = check.get("completes")
      dangling = completes is not None and completes not in example_ids

      if dangling:
         messages.append(f"{check['id']} completes {completes}, which is not a worked example")

   for scores in sections_of(lesson, plan.READER_SCORES):
      if scores["example_id"] not in example_ids:
         messages.append(f"{scores['id']} scores {scores['example_id']}, which is not a worked example")

   for error_id, anchor in error_blocks.items():
      served = plan.plan_lesson(lesson, "low", "feedback", error_ids=(error_id,))

      if served.anchors != (anchor,):
         messages.append(f"feedback for {error_id} does not return {anchor}")

   return messages


def is_refresher_member(section, examples):
   is_error = section["type"] == plan.COMMON_ERROR
   is_core = section["type"] == plan.KEY_IDEAS and section["depth"] == "core"
   is_first_example = bool(examples) and section["id"] == examples[0]["id"]

   return is_error or is_core or is_first_example


def lint_draw_exclusion(lesson, context):
   messages = []

   for record in solved_records(lesson):
      draw = record["parameter_draw"]

      for item_id, published in context.published_draws(record["archetype_id"]):
         if design_rules().stringified(published) == design_rules().stringified(draw):
            messages.append(f"{record['id']} repeats the parameter draw of published item {item_id}")

   return messages


def lint_strategy_trace(lesson, context):
   """Mirrors the strategy half of rule_inferred: a block on an archetype without both
   asked_to_produce and common_givens rests on typical_wording and is tagged inferred, and every
   block states its cue, method, rival and separating feature."""
   messages = []

   for section in sections_of(lesson, plan.STRATEGY):
      archetype = context.snapshot.archetypes.get(section["archetype_id"]) or {}
      messages.extend(strategy_messages(section, archetype))

   return messages


def strategy_messages(section, archetype):
   messages = []
   has_cue_fields = bool(archetype.get("asked_to_produce")) and bool(archetype.get("common_givens"))

   if not has_cue_fields and section["evidence_tag"] != "inferred":
      messages.append(f"{section['id']} builds on typical_wording alone and must be tagged inferred")

   for key in ("cue", "method", "rival", "separating_feature"):
      if not normalise_text(section.get(key)):
         messages.append(f"{section['id']} lacks {key}")

   return messages


def lint_step_cue(lesson, context):
   messages = []

   for example in sections_of(lesson, plan.WORKED_EXAMPLE):
      for position, step in enumerate(example["steps"], 1):
         words = words_in(step["cue"])
         is_empty = words == 0
         is_long = words > constants.CUE_WORDS_MAX

         if is_empty or is_long:
            messages.append(f"{example['id']} step {position} cue is {words} words, and the cap is {constants.CUE_WORDS_MAX}")

   return messages


def tagged_points(example):
   ordered = []

   for step in example["steps"]:
      point = step.get("point_type_id")
      is_new = point is not None and point not in ordered

      if is_new:
         ordered.append(point)

   return ordered


def lint_reader_scores(lesson, context):
   messages = []
   scores_by_example = {section["example_id"]: section for section in sections_of(lesson, plan.READER_SCORES)}

   for example in sections_of(lesson, plan.WORKED_EXAMPLE):
      archetype = context.snapshot.archetypes.get(example["archetype_id"])

      if archetype is None:
         continue

      listed = archetype.get("point_types") or []
      tagged = tagged_points(example)
      scores = scores_by_example.get(example["id"])
      messages.extend(tag_messages(example, listed, tagged, scores))

      if scores is not None and listed:
         messages.extend(scores_line_messages(scores, tagged, context, listed))

   return messages


def tag_messages(example, listed, tagged, scores):
   """Mirrors rule_reader_scores: tags only on an archetype that lists point types, and only
   types it lists; a tagged example has its scoring section. A design's empty scoring entry is
   transcribed as no section, so an untagged example needs none."""
   messages = []
   has_no_point_types = len(listed) == 0

   if has_no_point_types and tagged:
      messages.append(f"{example['id']} tags points on an archetype that lists none")

   if has_no_point_types and scores is not None:
      messages.append(f"{scores['id']} scores an archetype that lists no point types")

   stray = [point for point in tagged if point not in listed]

   if listed and stray:
      messages.append(f"{example['id']} tags {stray}, which the archetype does not list")

   if listed and tagged and scores is None:
      messages.append(f"{example['id']} has no what_a_reader_scores section")

   return messages


def scores_line_messages(scores, tagged, context, listed=()):
   stated_ids = [line["point_type_id"] for line in scores["lines"]]
   messages = []
   untold = [point for point in tagged if point not in stated_ids]

   if untold:
      messages.append(f"{scores['id']} does not list {untold}, which the example tags")

   stray = [point for point in stated_ids if listed and point not in listed]

   if stray:
      messages.append(f"{scores['id']} lists {stray}, which the archetype does not list")

   known = [point for point in stated_ids if point in context.snapshot.scoring_points]

   try:
      expected = reader_checks(known, context.snapshot)
   except KeyError as error:
      return messages + [f"{scores['id']} {error}"]

   given = [line["text"] for line in scores["lines"]]

   if given != [line["text"] for line in expected]:
      messages.append(f"{scores['id']} lines differ from reader_checks over the current records")

   return messages


def lint_error_blocks(lesson, context):
   is_concept = lesson["kind"] == "concept"

   if not is_concept:
      return []

   bundle = context.bundle(lesson["target_id"])
   records = {record["id"]: record for record in bundle["errors"]}
   expected = [record["id"] for record in bundle["errors"]][:constants.LESSON_COMMON_ERRORS_MAX]
   blocks = sections_of(lesson, plan.COMMON_ERROR)
   stated = [block["error_id"] for block in blocks]
   messages = []

   if stated != expected:
      messages.append(f"error blocks cover {stated}, and the records give {expected}")

   for block in blocks:
      record = records.get(block["error_id"])

      if record is not None:
         messages.extend(error_record_messages(block, record, bundle, context))

   return messages


def error_record_messages(block, record, bundle, context):
   messages = []

   if normalise_text(block["observed_behavior"]) != normalise_text(record["observed_behavior"]):
      messages.append(f"{block['id']} observed_behavior is not the record's")

   if normalise_text(block["scoring_consequence"]) != normalise_text(record["scoring_consequence"]):
      messages.append(f"{block['id']} scoring_consequence is not the record's")

   allowed_skills = set(record["skills"]) & set(bundle["concept"]["skills"])
   stray_skills = sorted(set(block["skills"]) - allowed_skills)

   if stray_skills:
      messages.append(f"{block['id']} names skills {stray_skills} the error does not hold")

   reason = block.get("possible_reason")

   if reason is not None:
      messages.extend(reason_messages(block, reason, record, context))

   messages.extend(relation_messages(block))

   return messages


def reason_messages(block, reason, record, context):
   linked = reason["misconception_id"] in record.get("possible_misconceptions", [])
   messages = []

   if not linked:
      messages.append(f"{block['id']} reason names {reason['misconception_id']}, which the error does not link")

   description = normalise_text(context.snapshot.misconceptions[reason["misconception_id"]]["description"])
   is_verbatim = normalise_text(reason["text"]) in description

   if not is_verbatim:
      messages.append(f"{block['id']} reason is not in the misconception's own words")

   return messages


def relation_messages(block):
   """Mirrors rule_errors: the wrong and right steps are compared with the design checker's
   equivalent, which reads an equation against a value by its right side."""
   try:
      wrong = to_expression(block["wrong_step"]["expression"])
      right = to_expression(block["right_step"]["expression"])
   except (UnsupportedMathJSON, TypeError, ValueError) as error:
      return [f"{block['id']} step did not convert: {error}"]

   are_equivalent = design_rules().equivalent(wrong, right)
   comparison = verify.EQUAL if are_equivalent else verify.DISTINCT
   wanted = verify.DISTINCT if block["relation"] == "distinct" else verify.EQUAL

   if comparison != wanted:
      return [f"{block['id']} says the steps are {block['relation']}, and the comparison is {comparison}"]

   return []


def lint_source_digest(lesson, context):
   is_concept = lesson["kind"] == "concept"

   if not is_concept:
      return []

   current = context.bundle(lesson["target_id"])["source_digest"]

   if lesson["source_digest"] != current:
      return [f"source_digest is stale, the records or research lines it hashes have changed"]

   return []


def lint_provenance(lesson, context):
   provenance = lesson["provenance"]
   messages = []
   is_signed_off = lesson["status"] == "signed_off"
   names_signer = provenance["signed_off_by"] is not None and provenance["signed_off_at"] is not None

   if is_signed_off and not names_signer:
      messages.append("status signed_off needs signed_off_by and signed_off_at")

   if names_signer and not is_signed_off and lesson["status"] != "stale":
      messages.append("a signer is recorded but the status is not signed_off")

   return messages


def lint_decision_stems(lesson, context):
   if not is_decision(lesson):
      return []

   decision = lesson["decision"]
   feature = decision["selecting_feature"]
   stems = decision["stems"]
   messages = []
   known_sets = {tuple(members) for members in confusable_sets(context.snapshot)}

   if tuple(sorted(decision["skills"])) not in known_sets:
      messages.append("the skills are not a confusable set of the snapshot")

   for left_index in range(len(stems)):
      for right in stems[left_index + 1:]:
         left = stems[left_index]
         draws = (left["parameter_draw"], right["parameter_draw"])
         keys = set(draws[0]) | set(draws[1])
         differing = sorted(key for key in keys if draws[0].get(key) != draws[1].get(key))

         if differing != [feature]:
            messages.append(f"{left['id']} and {right['id']} differ in {differing}, and only {feature} may differ")

         if normalise_text(left["method"]) == normalise_text(right["method"]):
            messages.append(f"{left['id']} and {right['id']} name the same method")

   return messages


def lint_discrimination_checks(lesson, context):
   if not is_decision(lesson):
      return []

   held = error_ids_for_skills(context.snapshot, lesson["decision"]["skills"])
   messages = []

   for check in lesson["checks"]:
      has_options = bool(check.get("options"))

      if not has_options:
         messages.append(f"{check['id']} is not a multiple choice on the methods")
         continue

      for finding in verify.error_path_findings(check_distractor_paths(check), held):
         messages.append(f"{check['id']} distractor {finding['index'] + 1} error_path {finding['error_path']} is not held by the set")

   return messages


def labels_of(node):
   """The labels rule_delivery reads: any object naming a placement, or carrying text and at, at
   any depth, because panels and sweeps nest whole specs."""
   found = []

   if isinstance(node, dict):
      is_label = "placement" in node or ("text" in node and "at" in node)

      if is_label:
         found.append(node)

      for value in node.values():
         found.extend(labels_of(value))
   elif isinstance(node, list):
      for value in node:
         found.extend(labels_of(value))

   return found


def delivered_blocks(lesson):
   blocks = [(section["id"], section) for section in lesson["sections"] if section["type"] in DELIVERED_TYPES]
   decision = lesson.get("decision")

   if decision is not None:
      blocks.append(("decision stems", decision))

   return blocks


def spec_messages(block_id, mode, delivery):
   designs = design_rules()
   spec = delivery.get("spec")
   messages = []

   if not isinstance(spec, dict) or not spec.get("kind"):
      return [f"{block_id} {mode} needs a spec with a kind"]

   kind = spec.get("kind")

   if kind not in SPEC_KINDS:
      messages.append(f"{block_id} spec kind {kind!r} is not a known spec kind")

   for label in labels_of(spec):
      is_inside = label.get("placement", "inside") == "inside"

      if not is_inside:
         messages.append(f"{block_id} spec places a label {label.get('text')!r} outside the figure")

   representations = spec.get("representations") or []
   per_screen_max = designs.REPRESENTATIONS_PER_SCREEN_MAX

   if len(representations) > per_screen_max:
      messages.append(f"{block_id} carries {len(representations)} representations, at most {per_screen_max} per screen")

   return messages


def delivery_messages(block_id, section, delivery):
   mode = delivery["mode"]
   is_drawn = mode not in UNDRAWN_MODES
   is_decision = section.get("type") is None
   messages = []

   if section.get("type") in STEP_REVEAL_TYPES and mode != "step_reveal":
      messages.append(f"{block_id} is a {section['type']} and must be step_reveal, not {mode}")

   if is_decision and mode != "contrast":
      messages.append(f"{block_id} of a decision lesson must be contrast, not {mode}")

   if mode == "contrast" and not is_decision:
      messages.append(f"{block_id} is contrast, which only a decision lesson's stems carry")

   if is_drawn:
      messages.extend(spec_messages(block_id, mode, delivery))

      if not delivery.get("fallback"):
         messages.append(f"{block_id} {mode} needs a fallback")

      if not delivery.get("keyboard"):
         messages.append(f"{block_id} {mode} needs a keyboard line")

   if mode == "motion" and not delivery.get("reduced_motion"):
      messages.append(f"{block_id} motion needs a reduced_motion line")

   return messages


def lint_delivery(lesson, context):
   """Mirrors rule_delivery (amendment A-D1): every served block names its delivery, worked
   examples and error blocks are step_reveal, the stems are contrast, a drawn block carries a
   spec of a known kind with every label inside, a fallback and a keyboard line, motion carries a
   reduced_motion line, and a spec shows at most REPRESENTATIONS_PER_SCREEN_MAX representations.
   TEMPLATE.md caps representations per screen, not drawn blocks per lesson, so there is no
   lesson cap."""
   messages = []

   for block_id, section in delivered_blocks(lesson):
      delivery = section.get("delivery")

      if delivery is None:
         messages.append(f"{block_id} carries no delivery")
         continue

      messages.extend(delivery_messages(block_id, section, delivery))

   return messages


LINTS = {
   "schema": lint_schema,
   "referential": lint_referential,
   "section_order": lint_section_order,
   "structure": lint_structure,
   "band_coverage": lint_band_coverage,
   "step_equivalence": lint_step_equivalence,
   "final_answer": lint_final_answer,
   "calculator_boundary": lint_calculator_boundary,
   "distractor_rules": lint_distractor_rules,
   "error_paths_held": lint_error_paths_held,
   "quotes": lint_quotes,
   "duplicate": lint_duplicate,
   "style": lint_style,
   "prediction": lint_prediction,
   "citations": lint_citations,
   "caps": lint_caps,
   "anchors": lint_anchors,
   "draw_exclusion": lint_draw_exclusion,
   "strategy_trace": lint_strategy_trace,
   "step_cue": lint_step_cue,
   "reader_scores": lint_reader_scores,
   "error_blocks": lint_error_blocks,
   "source_digest": lint_source_digest,
   "provenance": lint_provenance,
   "decision_stems": lint_decision_stems,
   "discrimination_checks": lint_discrimination_checks,
   "delivery": lint_delivery,
}


def check_lesson(lesson, context):
   """Lint name to messages, only for the lints that found something. A record that fails the
   schema is reported for the schema alone, because the other lints read fields it may lack."""
   schema_messages = lint_schema(lesson, context)
   fails_schema = len(schema_messages) > 0

   if fails_schema:
      return {"schema": schema_messages}

   findings = {}

   for name, lint in LINTS.items():
      if name == "schema":
         continue

      try:
         messages = lint(lesson, context)
      except Exception as error:
         messages = [f"lint crashed: {type(error).__name__}: {error}"]

      if messages:
         findings[name] = messages

   return findings


def lesson_paths(paths):
   """Every *.json named, or inside a directory named, in the order given."""
   found = []

   for given in paths:
      path = Path(given)

      if path.is_dir():
         found.extend(sorted(child for child in path.iterdir() if child.suffix == ".json"))
      elif path.suffix == ".json":
         found.append(path)

   return found


def load_lessons(directory):
   return [(path.name, json.loads(path.read_text())) for path in lesson_paths([directory])]


def check_paths(paths, context):
   findings_by_file = {}
   count = 0

   for path in lesson_paths(paths):
      lesson = json.loads(path.read_text())
      count += 1
      findings = check_lesson(lesson, context)

      if findings:
         findings_by_file[path.name] = findings

   return {"lesson_count": count, "findings_by_file": findings_by_file}


def check_directory(directory, context):
   return check_paths([directory], context)


def print_report(report):
   for file_name, findings in report["findings_by_file"].items():
      print(f"{file_name}:")

      for name, messages in findings.items():
         for message in messages:
            print(f"  {name}: {message}")

   dirty = len(report["findings_by_file"])
   print()
   print(f"lessons read: {report['lesson_count']}")
   print(f"clean: {report['lesson_count'] - dirty}")
   print(f"with findings: {dirty}")


def print_sets(snapshot):
   sets = confusable_sets(snapshot)

   for members in sets:
      print(", ".join(members))

   print()
   print(f"confusable sets: {len(sets)}")


def main(argv):
   arguments = argv[1:]
   is_sets_mode = arguments == ["--sets"]
   paths = [argument for argument in arguments if not argument.startswith("--")]
   takes_paths = len(paths) > 0 and len(paths) == len(arguments)

   if not is_sets_mode and not takes_paths:
      print("usage: python3 tools/check_lessons.py <file or directory> [...] | --sets", file=sys.stderr)

      return 1

   try:
      snapshot = load_snapshot(DATA_ROOT)
   except LoaderError as error:
      print(f"refusing: the content snapshot did not load: {error}", file=sys.stderr)

      return 1

   if is_sets_mode:
      print_sets(snapshot)

      return 0

   missing = [path for path in paths if not Path(path).exists()]

   if missing:
      print(f"refusing: {', '.join(missing)} does not exist", file=sys.stderr)

      return 1

   report = check_paths(paths, Context(snapshot))
   print_report(report)
   has_no_lessons = report["lesson_count"] == 0

   if has_no_lessons:
      print("refusing: no lesson files were read, so nothing was checked", file=sys.stderr)

      return 1

   all_clean = len(report["findings_by_file"]) == 0

   return 0 if all_clean else 1


if __name__ == "__main__":
   sys.exit(main(sys.argv))
