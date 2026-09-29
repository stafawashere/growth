"""Check every lesson design document under docs/lessons/ against docs/lessons/TEMPLATE.md.

A design document is Markdown with front matter, the template's sections in order, and one
fenced JSON block under "## Machine record" that carries every served sentence, every worked step
as a SymPy string, every check and every source id. The prose sections carry the exam-attack
commentary an author reads; the machine record is what the checker computes over.

Rules, each named in RULES and each with a red fixture in tests/fixtures/lesson_designs/:
front_matter, sections, machine_record, manifest_id, referential, citations, research_lines,
caps, band_caps, style, prediction, quotes, steps, keys, errors, distractor_paths, reader_scores,
draw_exclusion, decision_stems, inferred. Directory-level: manifest coverage.

Usage: python3 tools/check_lesson_designs.py [paths...]      default docs/lessons
       python3 tools/check_lesson_designs.py --manifest       write docs/lessons/progress.json
       python3 tools/check_lesson_designs.py --progress       render docs/lessons/PROGRESS.md
Exit 0 only when every finding list is empty. The style and prediction lints reuse
tools/check_lessons.py and schemas/common.py rather than restating their rules.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import sympy
from sympy.parsing.sympy_parser import convert_xor, parse_expr, standard_transformations

from app.content.loader import load_snapshot
from app.items import verify
from app.items.distractor_paths import error_ids_for_skills
from app.lessons import constants
from app.lessons.confusable import confusable_sets
from app.lessons.source import CACHE_TEXT_DIR, authoring_bundle, reader_checks
from tools import check_lessons

DATA_ROOT = ROOT / "data"
DOCS_DIR = ROOT / "docs" / "lessons"
CONTENT_DIR = ROOT / "content"
PROGRESS_JSON = DOCS_DIR / "progress.json"
PROGRESS_MD = DOCS_DIR / "PROGRESS.md"
IDS_PATH = DATA_ROOT / "ids.json"

STATUSES = ("todo", "designed", "checked", "resolved", "signed_off")
FRONT_MATTER_KEYS = ("title", "research_date", "status", "purpose")

CONCEPT_SECTIONS = (
   "Orientation",
   "Key ideas",
   "Recognition",
   "Method choice",
   "Solution path",
   "Scoring",
   "Traps",
   "Representations",
   "Prerequisite bridge",
   "Time",
   "Checks",
   "Delivery",
   "Band plan",
   "Sources",
   "Machine record",
)
PREREQUISITE_SECTIONS = (
   "Orientation",
   "Key ideas",
   "Recognition",
   "Method choice",
   "Solution path",
   "Traps",
   "Time",
   "Checks",
   "Delivery",
   "Band plan",
   "Sources",
   "Machine record",
)
DECISION_SECTIONS = (
   "Orientation",
   "Recognition",
   "Method choice",
   "Stems",
   "Traps",
   "Time",
   "Checks",
   "Delivery",
   "Band plan",
   "Sources",
   "Machine record",
)
SECTIONS_BY_KIND = {
   "concept": CONCEPT_SECTIONS,
   "prerequisite": PREREQUISITE_SECTIONS,
   "decision": DECISION_SECTIONS,
}
KIND_BY_PREFIX = {"LSN-CON": "concept", "LSN-PRQ": "prerequisite", "LSN-DEC": "decision"}

EXAM_PARTS = {"I-A": 2.14, "I-B": 2.92, "II-A": 15.0, "II-B": 15.0}
BC_ID = re.compile(r"\bBC-[A-Z]{2,4}-[A-Z0-9]{2,}(?:-[A-Z0-9]+)*\b")
PAGE_CITATION = re.compile(r"\b(ced|sg-\d{2}|cr-\d{2}|crabbc-\d{2}):(\d+)\b")
RESEARCH_CITATION = re.compile(r"research/[\w\-/.]+\.md(?:#[^\n\]\)|,;`]+)?")
LOOSE_TAIL = re.compile(r"[.,;:]+$")
HEADING = re.compile(r"^## (.+?)\s*$")
FENCE_OPEN = re.compile(r"^```json\s*$")
FENCE_CLOSE = re.compile(r"^```\s*$")

RELATIONS = ("equivalent", "differentiate", "integrate", "evaluate", "solve", "limit", "new")
DELIVERY_MODES = ("text", "step_reveal", "figure", "table", "motion", "interactive", "model", "contrast")
DRAWN_MODES = ("figure", "table", "motion", "interactive", "model")
REPRESENTATIONS_PER_SCREEN_MAX = 2  # 01, Split-attention-free presentation, parameters

LOCAL_NAMES = {
   "e": sympy.E,
   "pi": sympy.pi,
   "ln": sympy.log,
   "log": sympy.log,
   "oo": sympy.oo,
   "inf": sympy.oo,
   "I": sympy.I,
   "E": sympy.E,
}
TRANSFORMATIONS = standard_transformations + (convert_xor,)


class DesignError(Exception):
   pass


def words_in(text):
   return check_lessons.words_in(text)


def normalise_text(text):
   return check_lessons.normalise_text(text)


def parse_expression(text):
   """A SymPy expression from the machine record's string form. "lhs = rhs" becomes Eq."""
   is_string = isinstance(text, str)

   if not is_string:
      return sympy.sympify(text)

   has_equation = "=" in text and "==" not in text and "<" not in text and ">" not in text

   if has_equation:
      left, right = text.split("=", 1)

      return sympy.Eq(parse_expression(left), parse_expression(right))

   return parse_expr(text, local_dict=dict(LOCAL_NAMES), transformations=TRANSFORMATIONS)


def as_value(expression):
   """The right side of an equation, or the expression itself."""
   is_equation = isinstance(expression, sympy.Eq)

   if is_equation:
      return expression.rhs

   return expression


def as_zero_form(expression):
   is_equation = isinstance(expression, sympy.Eq)

   if is_equation:
      return expression.lhs - expression.rhs

   return expression


def equivalent(left, right):
   are_equations = isinstance(left, sympy.Eq) and isinstance(right, sympy.Eq)

   if are_equations:
      return equivalent(as_zero_form(left), as_zero_form(right)) or equivalent(
         as_zero_form(left), -as_zero_form(right)
      )

   left = as_value(left)
   right = as_value(right)
   is_same_object = left == right

   if is_same_object:
      return True

   is_set_pair = isinstance(left, sympy.Set) and isinstance(right, sympy.Set)

   if is_set_pair:
      return sympy.simplify(left) == sympy.simplify(right)

   try:
      outcome = verify.equivalence(left, right)
   except Exception:
      outcome = "unsettled"

   if outcome == "equivalent":
      return True

   if outcome == "not_equivalent":
      return False

   numeric = verify.numeric_check(left, right)

   return numeric is True


def close_enough(left, right, places=3):
   try:
      left_value = float(sympy.N(as_value(left)))
      right_value = float(sympy.N(as_value(right)))
   except (TypeError, ValueError):
      return False

   return abs(left_value - right_value) < 0.5 * 10 ** (-places)


class Context:
   def __init__(self, snapshot, cache_dir=CACHE_TEXT_DIR, content_dir=CONTENT_DIR, root=ROOT):
      self.snapshot = snapshot
      self.cache_dir = Path(cache_dir)
      self.content_dir = Path(content_dir)
      self.root = Path(root)
      self.registry = json.loads((self.root / "data" / "ids.json").read_text())["ids"]
      self.bundles = {}
      self.draws = None
      self.manifest = manifest_from_snapshot(snapshot)
      self.sets = confusable_sets(snapshot)

   def bundle(self, concept_id):
      if concept_id not in self.bundles:
         self.bundles[concept_id] = authoring_bundle(concept_id, self.snapshot)

      return self.bundles[concept_id]

   def is_active(self, identifier):
      record = self.registry.get(identifier)
      is_registered = record is not None

      if is_registered:
         return record.get("status") == "active"

      return False

   def published_draws(self, archetype_id):
      if self.draws is None:
         self.draws = defaultdict(list)

         for path in sorted(self.content_dir.glob("items_*/*.json")):
            record = json.loads(path.read_text())
            has_draw = record.get("archetype_id") is not None and record.get("parameter_draw") is not None

            if has_draw:
               self.draws[record["archetype_id"]].append((record["id"], record["parameter_draw"]))

      return self.draws.get(archetype_id, [])

   def page_text(self, source):
      match = PAGE_CITATION.match(source)

      if match is None:
         return None

      page_file = self.cache_dir / match.group(1) / f"page-{int(match.group(2)):03d}.txt"

      if not page_file.exists():
         return None

      return page_file.read_text()


def manifest_from_snapshot(snapshot):
   """Every lesson id the library implies, computed from the snapshot and never by hand."""
   entries = {}

   for concept_id in sorted(snapshot.concepts):
      concept = snapshot.concepts[concept_id]
      unit = concept["unit"].rsplit("-", 1)[1]
      entries[f"LSN-CON-{concept_id.rsplit('-', 1)[1]}"] = {
         "kind": "concept",
         "target_id": concept_id,
         "unit": unit,
         "name": concept["name"],
         "path": f"docs/lessons/unit-{unit}/LSN-CON-{concept_id.rsplit('-', 1)[1]}.md",
      }

   for prq_id in sorted(snapshot.prerequisites):
      record = snapshot.prerequisites[prq_id]
      digits = prq_id.rsplit("-", 1)[1]
      entries[f"LSN-PRQ-{digits}"] = {
         "kind": "prerequisite",
         "target_id": prq_id,
         "unit": digits[:2],
         "name": record["name"],
         "path": f"docs/lessons/prerequisites/LSN-PRQ-{digits}.md",
      }

   per_unit = defaultdict(int)

   for members in confusable_sets(snapshot):
      unit = snapshot.skills[members[0]]["unit"].rsplit("-", 1)[1]
      per_unit[unit] += 1
      lesson_id = f"LSN-DEC-{unit}-{per_unit[unit]:02d}"
      entries[lesson_id] = {
         "kind": "decision",
         "target_id": f"BC-UNIT-{unit}",
         "unit": unit,
         "name": ", ".join(members),
         "skills": list(members),
         "path": f"docs/lessons/decisions/{lesson_id}.md",
      }

   return entries


def manifest_details(snapshot, entries):
   """Skills, archetypes, errors and point types per concept lesson, from authoring_bundle."""
   detailed = {}

   for lesson_id, entry in entries.items():
      detail = dict(entry)
      is_concept = entry["kind"] == "concept"

      if is_concept:
         bundle = authoring_bundle(entry["target_id"], snapshot)
         detail["skills"] = [skill["id"] for skill in bundle["skills"]]
         detail["archetypes"] = [archetype["id"] for archetype in bundle["archetypes"]]
         detail["errors"] = [error["id"] for error in bundle["errors"]]
         detail["point_types"] = [record["id"] for record in bundle["point_types"]]
         detail["prerequisites"] = [record["id"] for record in bundle["prerequisites"]]

      is_prerequisite = entry["kind"] == "prerequisite"

      if is_prerequisite:
         dependents = sorted(
            {edge["to"] for edge in snapshot.edges if edge["from"] == entry["target_id"]}
         )
         detail["dependent_skills"] = dependents
         detail["archetypes"] = sorted(
            archetype_id
            for archetype_id, archetype in snapshot.archetypes.items()
            if entry["target_id"] in (archetype.get("prerequisites") or [])
         )

      detailed[lesson_id] = detail

   return detailed


def split_front_matter(text):
   lines = text.splitlines()
   has_opening = len(lines) > 0 and lines[0].strip() == "---"

   if not has_opening:
      return None, text

   for index in range(1, len(lines)):
      if lines[index].strip() == "---":
         fields = {}

         for line in lines[1:index]:
            key, separator, value = line.partition(":")

            if separator:
               fields[key.strip()] = value.strip()

         return fields, "\n".join(lines[index + 1:])

   return None, text


def split_sections(body):
   """Ordered (heading, text) pairs for every ## heading, text excluding fenced blocks kept raw."""
   sections = []
   current = None
   buffer = []

   for line in body.splitlines():
      match = HEADING.match(line)

      if match:
         if current is not None:
            sections.append((current, "\n".join(buffer)))

         current = match.group(1).strip()
         buffer = []
      elif current is not None:
         buffer.append(line)

   if current is not None:
      sections.append((current, "\n".join(buffer)))

   return sections


def extract_machine_record(section_text):
   lines = section_text.splitlines()
   inside = False
   collected = []
   found = False

   for line in lines:
      if not inside and FENCE_OPEN.match(line):
         inside = True
         found = True
         continue

      if inside and FENCE_CLOSE.match(line):
         break

      if inside:
         collected.append(line)

   if not found:
      raise DesignError("no ```json block under Machine record")

   try:
      return json.loads("\n".join(collected))
   except json.JSONDecodeError as error:
      raise DesignError(f"machine record is not valid JSON: {error}")


class Design:
   def __init__(self, path, text):
      self.path = Path(path)
      self.text = text
      self.front_matter, self.body = split_front_matter(text)
      self.sections = split_sections(self.body)
      self.section_map = {heading: body for heading, body in self.sections}
      self.record = None
      self.record_error = None
      machine = self.section_map.get("Machine record")

      if machine is not None:
         try:
            self.record = extract_machine_record(machine)
         except DesignError as error:
            self.record_error = str(error)

   @property
   def lesson_id(self):
      return self.path.stem

   @property
   def kind(self):
      return KIND_BY_PREFIX.get(self.lesson_id[:7])

   def prose_text(self):
      """Everything outside the machine record's fence, for the lints."""
      parts = [json.dumps(self.front_matter or {})]

      for heading, body in self.sections:
         if heading == "Machine record":
            continue

         parts.append(body)

      return "\n".join(parts)


def rule_front_matter(design, context):
   fields = design.front_matter
   messages = []

   if fields is None:
      return ["no front matter block"]

   for key in FRONT_MATTER_KEYS:
      if not fields.get(key):
         messages.append(f"front matter lacks {key}")

   return messages


def rule_sections(design, context):
   kind = design.kind

   if kind is None:
      return [f"{design.lesson_id} is not an LSN-CON, LSN-PRQ or LSN-DEC id"]

   wanted = SECTIONS_BY_KIND[kind]
   present = [heading for heading, _ in design.sections]
   messages = []

   for heading in wanted:
      if heading not in present:
         messages.append(f"section missing: {heading}")

   ordered = [heading for heading in present if heading in wanted]
   is_in_order = ordered == [heading for heading in wanted if heading in present]

   if not is_in_order:
      messages.append("sections are not in template order")

   for heading, body in design.sections:
      is_empty = heading != "Machine record" and not body.strip()

      if is_empty:
         messages.append(f"section empty: {heading}")

   return messages


def rule_machine_record(design, context):
   if design.record_error:
      return [design.record_error]

   record = design.record

   if record is None:
      return ["no machine record"]

   messages = []
   required = ("id", "kind", "target_id", "sources", "checks", "read_minutes", "word_count")

   for key in required:
      if key not in record:
         messages.append(f"machine record lacks {key}")

   is_concept = record.get("kind") == "concept"

   if is_concept:
      for key in ("orientation", "key_ideas", "strategy", "worked_examples", "common_errors", "time"):
         if key not in record:
            messages.append(f"machine record lacks {key}")

   is_prerequisite = record.get("kind") == "prerequisite"

   if is_prerequisite:
      for key in ("orientation", "key_ideas", "worked_examples", "time"):
         if key not in record:
            messages.append(f"machine record lacks {key}")

   is_decision = record.get("kind") == "decision"

   if is_decision:
      for key in ("decision", "strategy", "time"):
         if key not in record:
            messages.append(f"machine record lacks {key}")

   time = record.get("time") or {}
   part = time.get("exam_part")

   if part not in EXAM_PARTS:
      messages.append(f"time.exam_part {part!r} is not one of {sorted(EXAM_PARTS)}")
   elif abs(float(time.get("budget_minutes", -1)) - EXAM_PARTS[part]) > 0.005:
      messages.append(f"time.budget_minutes must be {EXAM_PARTS[part]} for part {part}")

   return messages


def rule_manifest_id(design, context):
   record = design.record or {}
   messages = []
   lesson_id = design.lesson_id
   is_known = lesson_id in context.manifest

   if not is_known:
      messages.append(f"{lesson_id} is not in the manifest computed from the snapshot")

      return messages

   entry = context.manifest[lesson_id]

   if record.get("id") != lesson_id:
      messages.append(f"machine record id {record.get('id')!r} differs from file name {lesson_id}")

   if record.get("kind") != entry["kind"]:
      messages.append(f"machine record kind {record.get('kind')!r} should be {entry['kind']}")

   if record.get("target_id") != entry["target_id"]:
      messages.append(f"machine record target_id {record.get('target_id')!r} should be {entry['target_id']}")

   expected_path = context.root / entry["path"]
   is_in_place = design.path.resolve() == expected_path.resolve()

   is_under_docs = str(design.path.resolve()).startswith(str((context.root / "docs" / "lessons").resolve()))

   if is_under_docs and not is_in_place:
      messages.append(f"file should live at {entry['path']}")

   is_decision = entry["kind"] == "decision"

   if is_decision:
      skills = sorted((record.get("decision") or {}).get("skills") or [])

      if skills != entry["skills"]:
         messages.append(f"decision skills {skills} are not the manifest set {entry['skills']}")

   return messages


def snapshot_has(context, identifier):
   snapshot = context.snapshot
   tables = (
      snapshot.concepts,
      snapshot.skills,
      snapshot.prerequisites,
      snapshot.errors,
      snapshot.misconceptions,
      snapshot.archetypes,
      snapshot.scoring_points,
      snapshot.signals,
   )

   for table in tables:
      if identifier in table:
         return True

   return False


def rule_referential(design, context):
   messages = []
   seen = set()

   for identifier in BC_ID.findall(design.text):
      if identifier in seen:
         continue

      seen.add(identifier)
      is_registered = identifier in context.registry
      is_active = context.is_active(identifier) if is_registered else snapshot_has(context, identifier)

      if not is_active:
         messages.append(f"{identifier} is not an active id")

   return messages


def rule_citations(design, context):
   messages = []
   seen = set()

   for match in PAGE_CITATION.finditer(design.text):
      citation = match.group(0)

      if citation in seen:
         continue

      seen.add(citation)

      if context.page_text(citation) is None:
         messages.append(f"{citation} has no cached page under cache/text")

   return messages


def heading_present(text, heading):
   wanted = normalise_text(heading)

   for line in text.splitlines():
      is_heading = line.startswith("#")

      if is_heading and normalise_text(line.lstrip("#")).startswith(wanted):
         return True

   return False


def rule_research_lines(design, context):
   messages = []
   seen = set()

   for citation in RESEARCH_CITATION.findall(design.text):
      citation = LOOSE_TAIL.sub("", citation)

      if citation in seen:
         continue

      seen.add(citation)
      file_part, _, heading = citation.partition("#")
      path = context.root / file_part

      if not path.exists():
         messages.append(f"{file_part} does not exist")
         continue

      if heading and not heading_present(path.read_text(), heading.strip()):
         messages.append(f"{file_part} has no heading {heading.strip()!r}")

   record = design.record or {}

   for entry in record.get("research_lines") or []:
      path = context.root / entry.get("file", "")

      if not path.exists():
         messages.append(f"research line file {entry.get('file')!r} does not exist")
         continue

      line = normalise_text(entry.get("line", ""))
      is_present = line != "" and line in normalise_text(path.read_text())

      if not is_present:
         messages.append(f"research line not found in {entry.get('file')}: {entry.get('line', '')[:60]!r}")

   return messages


def rule_caps(design, context):
   record = design.record or {}
   messages = []
   orientation = (record.get("orientation") or {}).get("text", "")

   if words_in(orientation) > constants.ORIENTATION_WORDS_MAX:
      messages.append(f"orientation has {words_in(orientation)} words, cap {constants.ORIENTATION_WORDS_MAX}")

   core = 0

   for block in record.get("key_ideas") or []:
      if words_in(block.get("text", "")) > constants.KEY_IDEA_WORDS_MAX:
         messages.append(f"{block.get('id')} has {words_in(block.get('text', ''))} words, cap {constants.KEY_IDEA_WORDS_MAX}")

      if block.get("depth") == "core":
         core += 1

   if core > constants.KEY_IDEAS_CORE_MAX:
      messages.append(f"{core} core key ideas, cap {constants.KEY_IDEAS_CORE_MAX}")

   strategies = record.get("strategy") or []

   if len(strategies) > constants.STRATEGY_BLOCKS_MAX:
      messages.append(f"{len(strategies)} strategy blocks, cap {constants.STRATEGY_BLOCKS_MAX}")

   for block in strategies:
      total = sum(words_in(block.get(key, "")) for key in ("cue", "method", "rival", "separating_feature"))

      if total > constants.STRATEGY_WORDS_MAX:
         messages.append(f"{block.get('id')} has {total} words, cap {constants.STRATEGY_WORDS_MAX}")

   examples = record.get("worked_examples") or []

   if len(examples) > constants.WORKED_EXAMPLES_MAX:
      messages.append(f"{len(examples)} worked examples, cap {constants.WORKED_EXAMPLES_MAX}")

   for example in examples:
      for index, step in enumerate(example.get("steps") or [], 1):
         if words_in(step.get("cue", "")) > constants.CUE_WORDS_MAX:
            messages.append(f"{example.get('id')} step {index} cue has {words_in(step.get('cue', ''))} words, cap {constants.CUE_WORDS_MAX}")

         if words_in(step.get("why", "")) > constants.WHY_WORDS_MAX:
            messages.append(f"{example.get('id')} step {index} why has {words_in(step.get('why', ''))} words, cap {constants.WHY_WORDS_MAX}")

         if not step.get("cue"):
            messages.append(f"{example.get('id')} step {index} has no cue line")

   errors = record.get("common_errors") or []

   if len(errors) > constants.LESSON_COMMON_ERRORS_MAX:
      messages.append(f"{len(errors)} common error blocks, cap {constants.LESSON_COMMON_ERRORS_MAX}")

   for bridge in record.get("prerequisite_bridges") or []:
      if words_in(bridge.get("text", "")) > constants.BRIDGE_WORDS_MAX:
         messages.append(f"bridge {bridge.get('prq_id')} has {words_in(bridge.get('text', ''))} words, cap {constants.BRIDGE_WORDS_MAX}")

   checks = record.get("checks") or []
   is_decision = record.get("kind") == "decision"
   has_too_few = len(checks) < constants.LESSON_CHECKS_MIN

   if has_too_few or len(checks) > constants.LESSON_CHECKS_MAX:
      messages.append(f"{len(checks)} checks, allowed {constants.LESSON_CHECKS_MIN} to {constants.LESSON_CHECKS_MAX}")

   if is_decision:
      stems = (record.get("decision") or {}).get("stems") or []

      if not 2 <= len(stems) <= 4:
         messages.append(f"{len(stems)} decision stems, allowed 2 to 4")

   return messages


def example_words(example):
   total = words_in((example.get("problem") or {}).get("text", ""))

   for step in example.get("steps") or []:
      total += words_in(step.get("cue", "")) + words_in(step.get("why", ""))

   return total


def error_words(block):
   total = 0

   for key in ("observed_behavior", "scoring_consequence"):
      total += words_in(block.get(key, ""))

   for key in ("wrong_step", "right_step", "possible_reason"):
      total += words_in((block.get(key) or {}).get("text", ""))

   return total


def strategy_words(block):
   return sum(words_in(block.get(key, "")) for key in ("cue", "method", "rival", "separating_feature"))


def reader_words(record, example_id):
   total = 0

   for scores in record.get("what_a_reader_scores") or []:
      if scores.get("example_id") != example_id:
         continue

      for line in scores.get("lines") or []:
         total += words_in(line.get("text", "") if isinstance(line, dict) else line)

   return total


def band_words(record, band):
   """The words the band's plan serves, per plan 15's band table."""
   is_low = band == "low"
   total = words_in((record.get("orientation") or {}).get("text", ""))

   for block in record.get("key_ideas") or []:
      is_served = is_low or block.get("depth", "core") == "core"

      if is_served:
         total += words_in(block.get("text", "")) + words_in(block.get("notation", ""))
         total += words_in((block.get("quote") or {}).get("text", ""))

   strategies = record.get("strategy") or []
   served_strategies = strategies if is_low else strategies[:1]
   total += sum(strategy_words(block) for block in served_strategies)

   examples = record.get("worked_examples") or []
   served_examples = examples if is_low else examples[:1]

   for example in served_examples:
      total += example_words(example) + reader_words(record, example.get("id"))

   errors = record.get("common_errors") or []
   served_errors = errors if is_low else errors[: constants.MID_ERRORS]
   total += sum(error_words(block) for block in served_errors)

   checks = record.get("checks") or []
   served_checks = checks if is_low else checks[:2]

   for check in checks:
      is_served = check in served_checks and band in (check.get("bands") or ["low", "mid"])

      if is_served:
         total += words_in((check.get("stem") or {}).get("text", ""))

         for option in check.get("options") or []:
            total += words_in(option.get("label", ""))

   if is_low:
      total += words_in((record.get("representations") or {}).get("text", ""))

   for stem in (record.get("decision") or {}).get("stems") or []:
      total += words_in(stem.get("text", "")) + words_in(stem.get("method", ""))

   for bridge in record.get("prerequisite_bridges") or []:
      total += words_in(bridge.get("text", ""))

   return total


def rule_band_caps(design, context):
   record = design.record or {}
   messages = []
   computed = {"full": band_words(record, "low"), "brief": band_words(record, "mid")}
   stated = record.get("word_count") or {}
   minutes = record.get("read_minutes") or {}
   caps = {"full": constants.LESSON_WORDS_FULL_MAX, "brief": constants.LESSON_WORDS_BRIEF_MAX}
   minute_caps = {"full": constants.LESSON_READ_MINUTES_MAX, "brief": constants.LESSON_BRIEF_MINUTES_MAX}

   for form in ("full", "brief"):
      if stated.get(form) != computed[form]:
         messages.append(f"word_count.{form} is {stated.get(form)}, computed {computed[form]}")

      if computed[form] > caps[form]:
         messages.append(f"{form} form has {computed[form]} words, cap {caps[form]}")

      stated_minutes = minutes.get(form)
      has_minutes = isinstance(stated_minutes, (int, float))

      if not has_minutes:
         messages.append(f"read_minutes.{form} missing")
         continue

      floor = computed[form] / constants.WORDS_PER_MINUTE

      if stated_minutes + 1e-9 < floor:
         messages.append(f"read_minutes.{form} {stated_minutes} is below {floor:.2f}, the words at {constants.WORDS_PER_MINUTE} per minute")

      if stated_minutes > minute_caps[form]:
         messages.append(f"read_minutes.{form} {stated_minutes} is above the cap {minute_caps[form]}")

   return messages


def rule_style(design, context):
   messages = []
   raw = design.text

   if check_lessons.DASHES.search(raw):
      for number, line in enumerate(raw.splitlines(), 1):
         if check_lessons.DASHES.search(line):
            messages.append(f"line {number}: an em dash or en dash appears")

   if check_lessons.EMOJI.search(raw):
      messages.append("an emoji or pictograph appears")

   patterns = (
      ("praise", check_lessons.PRAISE),
      ("study advice", check_lessons.STUDY_ADVICE),
      ("schedule", check_lessons.SCHEDULE),
      ("second-person belief statement", check_lessons.SECOND_PERSON_BELIEF),
   )

   for number, line in enumerate(design.prose_text().splitlines(), 1):
      for name, pattern in patterns:
         found = pattern.search(line)

         if found:
            messages.append(f"{name}: {found.group(0)!r} in {line.strip()[:60]!r}")

   record_text = json.dumps(design.record or {}, ensure_ascii=False)

   for name, pattern in patterns:
      found = pattern.search(record_text)

      if found:
         messages.append(f"{name} in machine record: {found.group(0)!r}")

   return messages


def rule_prediction(design, context):
   messages = []

   for line in design.text.splitlines():
      for pattern in check_lessons.COMMON.FORBIDDEN_PREDICTION:
         found = re.search(pattern, line, re.I)

         if found:
            messages.append(f"predictive phrasing {found.group(0)!r} in {line.strip()[:60]!r}")

   return messages


def rule_quotes(design, context):
   record = design.record or {}
   messages = []

   for block in record.get("key_ideas") or []:
      quote = block.get("quote")

      if not quote:
         continue

      text = quote.get("text", "")

      if words_in(text) > constants.QUOTE_WORDS_MAX:
         messages.append(f"{block.get('id')} quote has {words_in(text)} words, cap {constants.QUOTE_WORDS_MAX}")

      page = context.page_text(quote.get("source", ""))

      if page is None:
         messages.append(f"{block.get('id')} quote cites {quote.get('source')!r}, which has no cached page")
         continue

      if normalise_text(text) not in normalise_text(page):
         messages.append(f"{block.get('id')} quote is not on {quote.get('source')}")

   return messages


def check_chain(label, steps, messages):
   """Every valued step follows from the previous valued step under its stated relation.
   Returns the last parsed expression, or None."""
   previous = None
   previous_text = None

   for index, step in enumerate(steps, 1):
      text = step.get("expr")

      if text is None:
         continue

      try:
         current = parse_expression(text)
      except Exception as error:
         messages.append(f"{label} step {index} does not parse: {text!r} ({type(error).__name__})")
         previous = None
         continue

      relation = step.get("relation", "equivalent")
      is_first = previous is None

      if relation not in RELATIONS:
         messages.append(f"{label} step {index} relation {relation!r} is not one of {RELATIONS}")
      elif is_first or relation == "new":
         pass
      elif relation == "equivalent":
         if previous_text == text:
            messages.append(f"{label} step {index} restates the step before it")
         elif not equivalent(previous, current):
            messages.append(f"{label} step {index} is not equivalent to the step before it")
      elif relation == "differentiate":
         variable = sympy.Symbol(step.get("variable", "x"))
         expected = sympy.diff(as_value(previous), variable)

         if not equivalent(expected, current):
            messages.append(f"{label} step {index} is not the derivative of the step before it")
      elif relation == "integrate":
         variable = sympy.Symbol(step.get("variable", "x"))
         back = sympy.diff(as_value(current), variable)

         if not equivalent(back, as_value(previous)):
            messages.append(f"{label} step {index} does not differentiate back to the step before it")
      elif relation == "evaluate":
         substitution = {sympy.Symbol(name): parse_expression(value) for name, value in (step.get("subs") or {}).items()}
         expected = as_value(previous).subs(substitution)
         is_close = equivalent(expected, current) or (step.get("approx") and close_enough(expected, current))

         if not is_close:
            messages.append(f"{label} step {index} is not the step before it evaluated at {step.get('subs')}")
      elif relation == "solve":
         variable = sympy.Symbol(step.get("variable", "x"))
         roots = as_value(current)
         candidates = list(roots) if isinstance(roots, (sympy.FiniteSet, set, tuple, list)) else [roots]
         zero_form = as_zero_form(previous)

         for root in candidates:
            residual = zero_form.subs(variable, root)

            if not equivalent(residual, sympy.Integer(0)):
               messages.append(f"{label} step {index}: {root} does not satisfy the step before it")
      elif relation == "limit":
         variable = sympy.Symbol(step.get("variable", "x"))
         point = parse_expression(step.get("point", "0"))
         direction = step.get("dir", "+-")
         expected = sympy.limit(as_value(previous), variable, point, dir=direction)

         if not equivalent(expected, current):
            messages.append(f"{label} step {index} is not the limit of the step before it")

      previous = current
      previous_text = text

   return previous


def rule_steps(design, context):
   record = design.record or {}
   messages = []

   for example in record.get("worked_examples") or []:
      label = example.get("id", "example")
      steps = example.get("steps") or []
      last = check_chain(label, steps, messages)
      answer = example.get("answer") or {}
      is_statement = answer.get("form") == "statement"

      if is_statement:
         continue

      if last is None:
         messages.append(f"{label} has no valued step")
         continue

      try:
         key = parse_expression(answer.get("expr"))
      except Exception:
         messages.append(f"{label} answer does not parse: {answer.get('expr')!r}")
         continue

      is_decimal = example.get("calculator_status") == "calculator"
      matches = equivalent(key, last) or (is_decimal and close_enough(key, last))

      if not matches:
         messages.append(f"{label} answer {answer.get('expr')!r} is not the last valued step")

   return messages


def rule_keys(design, context):
   record = design.record or {}
   messages = []
   examples = {example.get("id"): example for example in record.get("worked_examples") or []}

   for check in record.get("checks") or []:
      label = check.get("id", "check")
      key = check.get("key") or {}
      is_statement = key.get("form") == "statement"
      options = check.get("options") or []
      key_options = [option for option in options if option.get("is_key")]
      has_options = len(options) > 0

      if has_options and len(key_options) != 1:
         messages.append(f"{label} needs exactly one key option")

      if is_statement:
         continue

      try:
         key_expression = parse_expression(key.get("expr"))
      except Exception:
         messages.append(f"{label} key does not parse: {key.get('expr')!r}")
         continue

      last = check_chain(label, check.get("steps") or [], messages)

      if last is None:
         messages.append(f"{label} has no valued step")
      else:
         is_decimal = check.get("calculator_status") == "calculator"

         if not (equivalent(key_expression, last) or (is_decimal and close_enough(key_expression, last))):
            messages.append(f"{label} key is not the last valued step")

      completes = check.get("completes")

      if completes:
         example = examples.get(completes)

         if example is None:
            messages.append(f"{label} completes {completes!r}, which is not a worked example")
         else:
            try:
               answer = parse_expression((example.get("answer") or {}).get("expr"))
            except Exception:
               answer = None

            if answer is None or not equivalent(answer, key_expression):
               messages.append(f"{label} key differs from the answer of {completes}")

      values = []

      for option in options:
         text = option.get("expr")

         if text is None:
            messages.append(f"{label} option {option.get('id')} has no expr")
            continue

         try:
            value = parse_expression(text)
         except Exception:
            messages.append(f"{label} option {option.get('id')} does not parse: {text!r}")
            continue

         if option.get("is_key") and not equivalent(value, key_expression):
            messages.append(f"{label} key option {option.get('id')} does not equal the key")

         for other_id, other in values:
            if equivalent(value, other):
               messages.append(f"{label} options {other_id} and {option.get('id')} are equal")

         values.append((option.get("id"), value))

   return messages


def rule_errors(design, context):
   record = design.record or {}
   messages = []
   snapshot = context.snapshot

   for block in record.get("common_errors") or []:
      error_id = block.get("error_id")
      label = f"error {error_id}"
      error = snapshot.errors.get(error_id)

      if error is None:
         messages.append(f"{label} is not an active error")
         continue

      for key in ("observed_behavior", "scoring_consequence"):
         if normalise_text(block.get(key, "")) != normalise_text(error.get(key, "")):
            messages.append(f"{label} {key} is not the record's text")

      reason = block.get("possible_reason")

      if reason:
         misconception = snapshot.misconceptions.get(reason.get("misconception_id"))
         is_linked = misconception is not None and reason.get("misconception_id") in (error.get("possible_misconceptions") or [])

         if not is_linked:
            messages.append(f"{label} possible_reason names a misconception the record does not link")
         elif normalise_text(reason.get("text", "")) not in normalise_text(misconception.get("description", "")):
            messages.append(f"{label} possible_reason is not taken from the misconception's description")

      wrong = (block.get("wrong_step") or {}).get("expr")
      right = (block.get("right_step") or {}).get("expr")

      try:
         wrong_expression = parse_expression(wrong)
         right_expression = parse_expression(right)
      except Exception:
         messages.append(f"{label} wrong or right step does not parse")
         continue

      relation = block.get("relation")
      are_equivalent = equivalent(wrong_expression, right_expression)

      if relation == "distinct" and are_equivalent:
         messages.append(f"{label} wrong and right steps are equivalent but marked distinct")
      elif relation == "equivalent" and not are_equivalent:
         messages.append(f"{label} wrong and right steps differ but are marked equivalent")
      elif relation not in ("distinct", "equivalent"):
         messages.append(f"{label} relation must be distinct or equivalent")

   return messages


def lesson_skill_ids(design, context):
   record = design.record or {}
   kind = record.get("kind")

   if kind == "concept":
      concept = context.snapshot.concepts.get(record.get("target_id")) or {}

      return [skill_id for skill_id in concept.get("skills") or [] if skill_id in context.snapshot.skills]

   if kind == "decision":
      return list((record.get("decision") or {}).get("skills") or [])

   if kind == "prerequisite":
      return sorted({edge["to"] for edge in context.snapshot.edges if edge["from"] == record.get("target_id")})

   return []


def rule_distractor_paths(design, context):
   record = design.record or {}
   messages = []
   held = error_ids_for_skills(context.snapshot, lesson_skill_ids(design, context))
   block_ids = {block.get("error_id") for block in record.get("common_errors") or []}
   is_concept = record.get("kind") == "concept"

   for check in record.get("checks") or []:
      options = check.get("options") or []
      has_options = len(options) > 0
      is_mcq = check.get("format") == "mcq"

      if is_mcq and not has_options:
         messages.append(f"{check.get('id')} is an mcq with no options")

      for option in options:
         if option.get("is_key"):
            continue

         path = option.get("error_path")

         if not path:
            messages.append(f"{check.get('id')} distractor {option.get('id')} carries no error_path")
         elif path not in held:
            messages.append(f"{check.get('id')} distractor {option.get('id')} error_path {path} is not held by the lesson's skills")
         elif is_concept and path not in block_ids:
            messages.append(f"{check.get('id')} distractor {option.get('id')} error_path {path} has no error block in the lesson")

   return messages


def rule_reader_scores(design, context):
   record = design.record or {}
   messages = []
   snapshot = context.snapshot
   examples = {example.get("id"): example for example in record.get("worked_examples") or []}
   listed = {scores.get("example_id"): scores for scores in record.get("what_a_reader_scores") or []}

   for example_id, example in examples.items():
      archetype = snapshot.archetypes.get(example.get("archetype_id")) or {}
      point_types = archetype.get("point_types") or []
      tagged = [step.get("point_type_id") for step in example.get("steps") or [] if step.get("point_type_id")]
      scores = listed.get(example_id)

      if not point_types:
         if scores or tagged:
            messages.append(f"{example_id} is on an archetype without point_types but carries scoring lines or tags")

         continue

      for tag in tagged:
         if tag not in point_types:
            messages.append(f"{example_id} tags {tag}, which {archetype.get('id')} does not list")

      if scores is None:
         messages.append(f"{example_id} has no what_a_reader_scores entry")
         continue

      ids = scores.get("point_type_ids") or []

      for tag in tagged:
         if tag not in ids:
            messages.append(f"{example_id} tags {tag} but the scoring entry does not list it")

      for point_type_id in ids:
         if point_type_id not in point_types:
            messages.append(f"{example_id} scoring lists {point_type_id}, which {archetype.get('id')} does not list")

      try:
         expected = reader_checks([point_type_id for point_type_id in ids if point_type_id in snapshot.scoring_points], snapshot)
      except KeyError as error:
         messages.append(str(error))
         continue

      lines = scores.get("lines")

      if lines is None:
         continue

      given = [line.get("text") if isinstance(line, dict) else line for line in lines]

      if given != [line["text"] for line in expected]:
         messages.append(f"{example_id} scoring lines are not reader_checks({ids}) recomputed")

   return messages


def rule_draw_exclusion(design, context):
   record = design.record or {}
   messages = []
   drawn = list(record.get("worked_examples") or []) + list(record.get("checks") or [])

   for entry in drawn:
      archetype_id = entry.get("archetype_id")
      draw = entry.get("parameter_draw")

      if archetype_id is None or draw is None:
         continue

      for item_id, published in context.published_draws(archetype_id):
         if published == draw:
            messages.append(f"{entry.get('id')} draw equals the parameter_draw of {item_id}")

   return messages


def rule_decision_stems(design, context):
   record = design.record or {}

   if record.get("kind") != "decision":
      return []

   decision = record.get("decision") or {}
   feature = decision.get("selecting_feature")
   stems = decision.get("stems") or []
   messages = []

   if not feature:
      messages.append("decision has no selecting_feature")

   for left_index in range(len(stems)):
      left = stems[left_index]

      for right in stems[left_index + 1:]:
         draws = (left.get("parameter_draw") or {}, right.get("parameter_draw") or {})
         keys = set(draws[0]) | set(draws[1])
         differing = sorted(key for key in keys if draws[0].get(key) != draws[1].get(key))

         if differing != [feature]:
            messages.append(f"{left.get('id')} and {right.get('id')} differ in {differing}, only {feature!r} may differ")

         if normalise_text(left.get("method", "")) == normalise_text(right.get("method", "")):
            messages.append(f"{left.get('id')} and {right.get('id')} name the same method")

   methods = {normalise_text(stem.get("method", "")) for stem in stems}

   for check in record.get("checks") or []:
      if check.get("check_kind") != "discrimination":
         messages.append(f"{check.get('id')} is not a discrimination check")

      if check.get("steps"):
         messages.append(f"{check.get('id')} carries execution steps; decision checks name the method only")

      key_options = [option for option in check.get("options") or [] if option.get("is_key")]

      for option in key_options:
         if normalise_text(option.get("label", "")) not in methods:
            messages.append(f"{check.get('id')} key label is not one of the stems' methods")

   return messages


def rule_inferred(design, context):
   record = design.record or {}
   messages = []

   for entry in record.get("inferred") or []:
      has_both = bool(entry.get("claim")) and bool(entry.get("settles"))

      if not has_both:
         messages.append("an inferred entry lacks its claim or what would settle it")

   for block in record.get("strategy") or []:
      archetype = context.snapshot.archetypes.get(block.get("archetype_id")) or {}
      has_fields = bool(archetype.get("asked_to_produce")) and bool(archetype.get("common_givens"))
      is_tagged = block.get("evidence_tag") == "inferred"

      if not has_fields and not is_tagged:
         messages.append(f"{block.get('id')} rests on typical_wording ({block.get('archetype_id')} lacks asked_to_produce or common_givens) and must carry evidence_tag inferred")

   for block in record.get("strategy") or []:
      for key in ("cue", "method", "rival", "separating_feature"):
         if not block.get(key):
            messages.append(f"{block.get('id')} lacks {key}")

   return messages


def served_blocks(record):
   """Block id to the mode the template fixes for it, or None when the rules choose."""
   blocks = {}

   if record.get("orientation"):
      blocks["orientation"] = None

   for block in record.get("key_ideas") or []:
      blocks[block.get("id")] = None

   for example in record.get("worked_examples") or []:
      blocks[example.get("id")] = "step_reveal"

   for block in record.get("common_errors") or []:
      blocks[f"err-{block.get('error_id')}"] = "step_reveal"

   if record.get("representations"):
      blocks["representations"] = None

   if (record.get("decision") or {}).get("stems"):
      blocks["stems"] = "contrast"

   return blocks


def labels_of(node):
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


def rule_delivery(design, context):
   record = design.record or {}
   messages = []
   entries = record.get("delivery")

   if entries is None:
      return ["machine record lacks delivery"]

   expected = served_blocks(record)
   seen = defaultdict(int)

   for entry in entries:
      block = entry.get("block")
      mode = entry.get("mode")
      seen[block] += 1

      if block not in expected:
         messages.append(f"delivery names {block!r}, which is not a served block")
         continue

      if mode not in DELIVERY_MODES:
         messages.append(f"{block} mode {mode!r} is not one of {DELIVERY_MODES}")
         continue

      fixed = expected[block]

      if fixed is not None and mode != fixed:
         messages.append(f"{block} must be {fixed}, not {mode}")

      if not entry.get("reason"):
         messages.append(f"{block} delivery has no reason")

      is_drawn = mode in DRAWN_MODES

      if is_drawn:
         spec = entry.get("spec")

         if not isinstance(spec, dict) or not spec.get("kind"):
            messages.append(f"{block} {mode} needs a spec with a kind")
         else:
            for label in labels_of(spec):
               if label.get("placement", "inside") != "inside":
                  messages.append(f"{block} spec places a label outside the figure")

            representations = spec.get("representations") or []

            if len(representations) > REPRESENTATIONS_PER_SCREEN_MAX:
               messages.append(f"{block} carries {len(representations)} representations, at most {REPRESENTATIONS_PER_SCREEN_MAX} per screen")

         if not entry.get("fallback"):
            messages.append(f"{block} {mode} needs a fallback")

         if not entry.get("keyboard"):
            messages.append(f"{block} {mode} needs a keyboard line")

      if mode == "motion" and not entry.get("reduced_motion"):
         messages.append(f"{block} motion needs a reduced_motion line")

   for block in expected:
      count = seen.get(block, 0)

      if count != 1:
         messages.append(f"{block} has {count} delivery entries, needs exactly 1")

   return messages


RULES = {
   "front_matter": rule_front_matter,
   "sections": rule_sections,
   "machine_record": rule_machine_record,
   "manifest_id": rule_manifest_id,
   "referential": rule_referential,
   "citations": rule_citations,
   "research_lines": rule_research_lines,
   "caps": rule_caps,
   "band_caps": rule_band_caps,
   "style": rule_style,
   "prediction": rule_prediction,
   "quotes": rule_quotes,
   "steps": rule_steps,
   "keys": rule_keys,
   "errors": rule_errors,
   "distractor_paths": rule_distractor_paths,
   "reader_scores": rule_reader_scores,
   "draw_exclusion": rule_draw_exclusion,
   "decision_stems": rule_decision_stems,
   "inferred": rule_inferred,
   "delivery": rule_delivery,
}
STRUCTURAL = ("front_matter", "sections", "machine_record")


def check_design(design, context):
   """Rule name to messages for the rules that found something. A document whose machine record
   is missing or malformed is reported for the structural rules alone."""
   findings = {}

   for name in STRUCTURAL:
      messages = RULES[name](design, context)

      if messages:
         findings[name] = messages

   has_no_record = design.record is None

   if has_no_record:
      return findings

   for name, rule in RULES.items():
      if name in STRUCTURAL:
         continue

      try:
         messages = rule(design, context)
      except Exception as error:
         messages = [f"rule crashed: {type(error).__name__}: {error}"]

      if messages:
         findings[name] = messages

   return findings


def check_support_document(path, text):
   """README, TEMPLATE, BUILD-PLAN and PROGRESS: front matter and the dash rule only."""
   messages = []
   fields, _ = split_front_matter(text)

   if fields is None:
      messages.append("no front matter block")
   else:
      for key in FRONT_MATTER_KEYS:
         if not fields.get(key):
            messages.append(f"front matter lacks {key}")

   for number, line in enumerate(text.splitlines(), 1):
      if check_lessons.DASHES.search(line):
         messages.append(f"line {number}: an em dash or en dash appears")

   return {"support": messages} if messages else {}


def is_lesson_file(path):
   return path.suffix == ".md" and path.stem[:7] in KIND_BY_PREFIX


def gather(paths):
   files = []

   for given in paths:
      path = Path(given)

      if path.is_dir():
         files.extend(sorted(candidate for candidate in path.rglob("*.md")))
      else:
         files.append(path)

   return files


def check_paths(paths, context, check_coverage=False):
   findings_by_file = {}
   lesson_ids = set()
   count = 0

   for path in gather(paths):
      text = path.read_text()
      count += 1

      if is_lesson_file(path):
         lesson_ids.add(path.stem)
         findings = check_design(Design(path, text), context)
      else:
         findings = check_support_document(path, text)

      if findings:
         findings_by_file[str(path)] = findings

   if check_coverage:
      missing = sorted(set(context.manifest) - lesson_ids)
      extra = sorted(lesson_ids - set(context.manifest))
      messages = [f"manifest id without a design: {lesson_id}" for lesson_id in missing]
      messages += [f"design without a manifest id: {lesson_id}" for lesson_id in extra]

      if messages:
         findings_by_file["<manifest coverage>"] = {"coverage": messages}

   return {"file_count": count, "findings_by_file": findings_by_file}


def print_report(report):
   for file_name, findings in report["findings_by_file"].items():
      print(f"{file_name}:")

      for name, messages in findings.items():
         for message in messages:
            print(f"  {name}: {message}")

   dirty = len(report["findings_by_file"])
   print()
   print(f"files read: {report['file_count']}")
   print(f"clean: {report['file_count'] - dirty}")
   print(f"with findings: {dirty}")


def load_progress():
   if PROGRESS_JSON.exists():
      return json.loads(PROGRESS_JSON.read_text())

   return {"lessons": {}, "notes": {}}


def write_manifest(snapshot):
   progress = load_progress()
   entries = manifest_details(snapshot, manifest_from_snapshot(snapshot))
   kept = progress.get("lessons", {})
   lessons = {}

   for lesson_id, entry in entries.items():
      previous = kept.get(lesson_id, {})
      lessons[lesson_id] = {**entry, "status": previous.get("status", "todo"), "note": previous.get("note", "")}

   progress["lessons"] = lessons
   progress["snapshot_digest"] = snapshot.digest
   PROGRESS_JSON.write_text(json.dumps(progress, indent=1, sort_keys=True) + "\n")
   print(f"manifest written: {len(lessons)} lessons")


def render_progress():
   progress = load_progress()
   lessons = progress["lessons"]
   counts = defaultdict(lambda: defaultdict(int))

   for entry in lessons.values():
      counts[entry["kind"]][entry["status"]] += 1

   lines = ["<!-- manifest:start (rendered by tools/check_lesson_designs.py --progress) -->", ""]
   lines.append("| Kind | " + " | ".join(STATUSES) + " | total |")
   lines.append("|---|" + "---|" * (len(STATUSES) + 1))

   for kind in ("concept", "prerequisite", "decision"):
      row = [str(counts[kind][status]) for status in STATUSES]
      lines.append(f"| {kind} | " + " | ".join(row) + f" | {sum(counts[kind].values())} |")

   lines.append("")
   lines.append("| Lesson | Target | Unit | Status | Note |")
   lines.append("|---|---|---|---|---|")

   for lesson_id in sorted(lessons):
      entry = lessons[lesson_id]
      lines.append(f"| {lesson_id} | {entry['target_id']} | {entry['unit']} | {entry['status']} | {entry.get('note', '')} |")

   lines += ["", "<!-- manifest:end -->"]
   rendered = "\n".join(lines)
   existing = PROGRESS_MD.read_text() if PROGRESS_MD.exists() else ""
   start = existing.find("<!-- manifest:start")
   end = existing.find("<!-- manifest:end -->")
   has_markers = start >= 0 and end >= 0

   if has_markers:
      updated = existing[:start] + rendered + existing[end + len("<!-- manifest:end -->"):]
   else:
      updated = existing.rstrip("\n") + "\n\n## Manifest\n\n" + rendered + "\n"

   PROGRESS_MD.write_text(updated)
   print(f"progress rendered: {len(lessons)} lessons")


def main(argv):
   arguments = argv[1:]
   snapshot = load_snapshot(DATA_ROOT)

   if arguments == ["--manifest"]:
      write_manifest(snapshot)

      return 0

   if arguments == ["--progress"]:
      render_progress()

      return 0

   check_coverage = "--coverage" in arguments
   paths = [argument for argument in arguments if not argument.startswith("--")]
   is_default = len(paths) == 0

   if is_default:
      paths = [str(DOCS_DIR)]
      check_coverage = True

   report = check_paths(paths, Context(snapshot), check_coverage=check_coverage)
   print_report(report)

   if report["file_count"] == 0:
      print("refusing: no files were read, so nothing was checked", file=sys.stderr)

      return 1

   return 0 if not report["findings_by_file"] else 1


if __name__ == "__main__":
   sys.exit(main(sys.argv))
