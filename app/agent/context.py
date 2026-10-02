"""The context composer: one packet per turn from the screen shape and the rows the route loaded
(docs/agent/architecture.md, The screen context, The context composer, Templates and the cached
prefix).

Every function here is pure over its inputs. The route validates the screen, loads the item, the
attempt, the archetype, the lesson row, the feedback app/feedback/render.py computes, the diagnosis,
the memory entries and the profile, and calls compose_packet; nothing in this module reads the
database or the model, and nothing imports the memory store.

The packet is built from an allow-list, field by field, so what is excluded before submission is
excluded by construction: the answer key, the option values and is_key, the worked solution, the
archetype's common_distractors, every error and misconception record for the item, and the draft,
which the client never sends. An MCQ's options reach the packet as their letters only. Lesson
sections reach a practice packet as ids and types, without the common_error sections (their ids
name the error record) and, at stage unsupported, without the worked_example sections.

A lesson section that poses a question (the prediction, a check, an error block with a fix prompt,
a faded example) puts its screen in practice mode too, because it holds a key the student is meant
to find. Its packet carries the question as the item text, the option letters and the archetype's
path when the section names one, and never the key, the resolution, the right step or the steps
the faded example holds back. question_key_forms builds the screen's key forms from the same key
the prompt answer route grades against (docs/agent/architecture.md, The screen context; orchestrator
ruling, 2026-09-29, after the prediction on LSN-CON-01006 had its answer stated while browsing).

After submission the packet adds the elaborated payload the feedback route already computes, the
matched error id, one scoring point and, only when the diagnostician wrote a hypothesis, the leading
misconception's discriminating probe as text. The worked solution rides only with the feedback kinds
that show it (elaborated, correct and step verification). The verification-only arm of the feedback
switch and the ungraded kind get none, so the tutor cannot undo the experiment or invent a verdict.

The library records which point types an archetype scores but not which step each point belongs
to. point_type_for_step names a point only when exactly one of the archetype's point types shares at
least three content words with the violated step, and none otherwise, so a point is named only when
the app selected it for that step (docs/agent/research/math-tutoring.md, The library records a tutor
can ground in). Two shared words were too few: BC-QA-03008's first-derivative substitution step met
the higher-derivative point on "derivative" and "point" alone (orchestrator ruling, 2026-09-29).

The packet carries drawing, open or closed, which app/agent/moves.py drawing_for decides from the
move and the drawing switch, and render_prompt fills the template's drawing field with it when the
template has one: prompts/agent/live_v2.md once it exists, live_v1.md until then. An item with a
figure adds a summary of what the student sees to the item packet, its kind, window and alt text
and a table's columns and rows, and nothing else of the figure. An agent turn whose figure was shown
reaches the history sent to the model as its text and one line naming the figure's title and
description, never the figure itself (docs/agent/drawing-design.md, The item's own figure in the
packet, and Storage, privacy and logs).

The packet lists the anchors the tutor may mark on this turn (docs/agent/drawing-design.md, Marks
on the page, and the marks contract in docs/agent/drawing-build-plan.md), composed from what the
screen shows: the stem and the item's graph with its window or its table with its row and column
counts on an item; the feedback and each worked solution step only once the item is checked and
only when they are shown; the section and a drawn section figure on a lesson. The options are never
listed, because before checking ringing one names an answer and after checking the session screen
shows no options. A text anchor's text is text the packet already carries, and turn_anchors attaches
it for the marks reader.
"""
import json
import re
from dataclasses import dataclass
from pathlib import Path

from jsonschema import Draft202012Validator

from app.agent.drawing.record import shown_spec
from app.agent.moves import (
   AFTER_SUBMISSION,
   AGENT_DRAWING_FIELD,
   BROWSING,
   DRAWING_CLOSED,
   PRACTICE,
   choose_move,
   drawing_for,
)
from app.evals import agent_checks
from app.providers.base import render_template, split_template, template_placeholders

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SCREEN_SCHEMA_PATH = REPOSITORY_ROOT / "schemas" / "agent" / "screen.schema.json"
LIVE_V1_TEMPLATE_PATH = REPOSITORY_ROOT / "prompts" / "agent" / "live_v1.md"
LIVE_V2_TEMPLATE_PATH = REPOSITORY_ROOT / "prompts" / "agent" / "live_v2.md"
LIVE_TEMPLATE_PATH = LIVE_V2_TEMPLATE_PATH if LIVE_V2_TEMPLATE_PATH.exists() else LIVE_V1_TEMPLATE_PATH

MEMORY_ENTRY_LIMIT = 6
HISTORY_TURN_LIMIT = 20
AGENT_ROLE = "agent"
HISTORY_ROLES = ("student", AGENT_ROLE)
ITEM_SCREEN = "session_item"
SCREEN_KINDS = ("today", "session_item", "session_lesson", "lesson", "review", "progress", "assessments", "settings", "other")
LESSON_SCREENS = ("lesson", "session_lesson")
UNSUPPORTED = "unsupported"
TABLE_FIGURE = "table"
TEXT_ANCHOR = "text"
GRAPH_ANCHOR = "graph"
TABLE_ANCHOR = "table"
ELEMENT_ANCHOR = "element"
DRAWN_DELIVERY_MODES = ("figure", "table", "motion", "interactive", "model")
FEEDBACK_TEXT_FIELDS = ("violated_step", "observed_behavior", "scoring_consequence")
ELABORATED_FEEDBACK = "elaborated"
STEP_VERIFICATION_FEEDBACK = "step_verification"
MCQ = "mcq"
SHORT_ANSWER = "short_answer"
PREDICTION = "prediction"
CHECK = "check"
COMMON_ERROR = "common_error"
WORKED_EXAMPLE = "worked_example"
PLAIN_NUMBER_LABEL = re.compile(r"^-?\d+(\.\d+)?$")
PLAIN_FRACTION_LABEL = re.compile(r"^(-?\d+)\s*/\s*(\d+)$")
WORKED_SOLUTION_KINDS = ("elaborated", "correct", "step_verification")
UNPOINTABLE_DURING_PRACTICE = ("common_error",)
UNPOINTABLE_AT_UNSUPPORTED = ("worked_example",)
PROFILE_FIELDS_NEVER_RENDERED = ("stated_requests",)
SECTION_META_KEYS = frozenset({
   "id",
   "type",
   "bands",
   "skills",
   "sources",
   "evidence_tag",
   "delivery",
   "archetype_id",
   "ek_id",
   "parameter_draw",
   "depth",
   "format",
   "example_id",
   "error_id",
   "point_type_id",
   "relation",
   "fade_from",
   "calculator_status",
   "is_key",
   "mathjson",
})
CONTENT_WORD = re.compile(r"[a-z]{4,}")
STEM_LENGTH = 5
MINIMUM_SHARED_WORDS = 3
STOP_WORDS = frozenset({"with", "from", "that", "this", "each", "when", "then", "than", "their", "into", "have", "does"})

_SCREEN_VALIDATOR = Draft202012Validator(json.loads(SCREEN_SCHEMA_PATH.read_text()))


class TimedPartRefused(ValueError):
   """A turn from a timed part, which the route refuses with the timed reason."""


@dataclass(frozen=True)
class ScreenCheck:
   kind: str
   timed: bool


@dataclass(frozen=True)
class Packet:
   mode: str
   move: str
   screen_line: str
   body: dict
   turn_index: int = 0
   memory: tuple = ()
   profile: dict | None = None
   drawing: str = DRAWING_CLOSED


@dataclass(frozen=True)
class RenderedPrompt:
   system: str
   user: str


def validate_screen(screen):
   """Refuses any shape the schema does not name, with a short message that quotes none of it."""
   is_mapping = isinstance(screen, dict)

   if not is_mapping:
      raise ValueError("screen is not an object")

   errors = list(_SCREEN_VALIDATOR.iter_errors(screen))
   has_errors = len(errors) > 0

   if has_errors:
      kind = screen.get("kind")
      is_known_kind = kind in SCREEN_KINDS

      if is_known_kind:
         raise ValueError(f"screen does not match the {kind} shape")

      raise ValueError("screen names no known kind")

   return ScreenCheck(kind=screen["kind"], timed=screen.get("timed") is True)


def _humanised(token):
   return str(token).replace("_", " ")


def screen_line(screen, names=None):
   """The context line design.md's table gives, composed from the same shape the client sends."""
   names = names or {}
   kind = screen["kind"]

   if kind == "today":
      return "Can see: Today, your queue for today."

   if kind == ITEM_SCREEN:
      if screen.get("submitted"):
         return "Can see: Today, practice item, checked, with its feedback and worked solution."

      return "Can see: Today, practice item, not checked yet. Cannot see: your answer or the answer key."

   if kind in LESSON_SCREENS:
      concept = names.get(screen["lesson_id"], screen["lesson_id"])
      part = screen["section_index"] + 1

      return f"Can see: Lesson, {concept}, part {part} of {screen['section_count']}."

   if kind == "review":
      return "Can see: Review, your error notes and corrected items."

   if kind == "progress":
      skill_id = screen.get("skill_id")

      if skill_id is not None:
         return f"Can see: Progress, the skill {names.get(skill_id, skill_id)}."

      return f"Can see: Progress, {names.get(screen['tab'], _humanised(screen['tab']))}."

   if kind == "assessments":
      if screen.get("timed") is True:
         return "Can see: Assessments, a timed part."

      return f"Can see: Assessments, the {names.get(screen['format'], _humanised(screen['format']))} setup."

   if kind == "settings":
      return f"Can see: Settings, the {names.get(screen['tab'], _humanised(screen['tab']))} tab."

   return f"Can see: {names.get(screen['view'], _humanised(screen['view'])).capitalize()}."


def _decoded(value):
   is_encoded = isinstance(value, str)

   return json.loads(value) if is_encoded else value


def _field(record, name, default=None):
   if record is None:
      return default

   if isinstance(record, dict):
      return record.get(name, default)

   return getattr(record, name, default)


def _stem_text(item):
   stem = _field(item, "stem")

   if isinstance(stem, dict):
      return stem.get("text", "")

   return stem or ""


def mode_for(screen, attempt=None, lesson=None):
   """Practice on an unchecked item and on a lesson section that poses a question, after
   submission on a checked item, browsing everywhere else."""
   is_item = screen["kind"] == ITEM_SCREEN

   if not is_item:
      is_question = question_section(screen, lesson) is not None

      return PRACTICE if is_question else BROWSING

   is_submitted = _field(attempt, "submitted_at") is not None

   return AFTER_SUBMISSION if is_submitted else PRACTICE


def _snapshot(context):
   return getattr(context, "snapshot", None)


def _registry(context, name):
   return getattr(_snapshot(context), name, None) or {}


def _name_of(registry, record_id):
   return (registry.get(record_id) or {}).get("name") or record_id


def target_name(context, target_id):
   for registry_name in ("concepts", "prerequisites"):
      record = _registry(context, registry_name).get(target_id)

      if record is not None:
         return record.get("name") or target_id

   unit_titles = getattr(context, "unit_titles", None) or {}

   return unit_titles.get(target_id, target_id)


def _lesson_body(lesson):
   return _decoded(_field(lesson, "body")) or {}


def _lesson_sections(lesson):
   return list(_lesson_body(lesson).get("sections") or [])


def section_type(section):
   """A check record carries no type field, so its type is check."""
   return section.get("type", CHECK)


def _lesson_checks(lesson):
   return [dict(check, type=CHECK) for check in _lesson_body(lesson).get("checks") or []]


def screen_section(screen, lesson):
   """The section or check the lesson screen is on, or None when the lesson row is not the
   screen's or holds no such id."""
   has_matching_lesson = lesson is not None and _field(lesson, "id") == screen.get("lesson_id")

   if not has_matching_lesson:
      return None

   records = _lesson_sections(lesson) + _lesson_checks(lesson)

   return next((record for record in records if record["id"] == screen.get("section_id")), None)


def poses_question(section):
   """A section the student is meant to answer: the prediction, a check, an error block with a fix
   prompt and a faded example (app/api/routes/lessons.py prompt_kind, and the checks)."""
   kind = section_type(section)
   is_prediction = kind == PREDICTION
   is_check = kind == CHECK
   is_fix_prompt = kind == COMMON_ERROR and section.get("fix_prompt") is True
   is_faded_example = kind == WORKED_EXAMPLE and section.get("fade_from") is not None

   return is_prediction or is_check or is_fix_prompt or is_faded_example


def question_section(screen, lesson):
   is_lesson_screen = screen.get("kind") in LESSON_SCREENS

   if not is_lesson_screen:
      return None

   section = screen_section(screen, lesson)
   is_question = section is not None and poses_question(section)

   return section if is_question else None


def _shown_steps(section):
   """The faded example's steps before fade_from, the ones on screen while it waits for the
   answer."""
   steps = list(section.get("steps") or [])
   shown_count = max(section["fade_from"] - 1, 0)

   return steps[:shown_count]


def question_text(section):
   """The question as the student reads it, without the key, the resolution, the right step or
   the steps the faded example holds back."""
   kind = section_type(section)

   if kind == COMMON_ERROR:
      wrong_step = section.get("wrong_step") or {}

      return " ".join(part for part in (section.get("observed_behavior"), wrong_step.get("text")) if part)

   if kind == WORKED_EXAMPLE:
      parts = [(section.get("problem") or {}).get("text")]

      for step in _shown_steps(section):
         parts.extend([step.get("cue"), step.get("why")])

      return " ".join(part for part in parts if part)

   return (section.get("stem") or {}).get("text", "")


def question_format(section):
   has_own_format = section_type(section) in (PREDICTION, CHECK)

   return section.get("format", SHORT_ANSWER) if has_own_format else SHORT_ANSWER


def _label_value(label):
   """A keyed option's label read as a number when it is one, so a key held only as the label "2"
   still has a numeric form to screen for."""
   text = str(label or "").strip()
   fraction = PLAIN_FRACTION_LABEL.match(text)

   if fraction is not None:
      return ["Rational", int(fraction.group(1)), int(fraction.group(2))]

   is_number = PLAIN_NUMBER_LABEL.match(text) is not None

   if not is_number:
      return None

   return float(text) if "." in text else int(text)


def question_key(section):
   """The section's key in the shape agent_checks.key_forms reads, the same key the prompt answer
   route grades against (app/api/routes/lessons.py prompt_as_gradable_item)."""
   kind = section_type(section)

   if kind == COMMON_ERROR:
      return {"answer_key": {"form": "symbolic", "mathjson": section["right_step"]["expression"]}, "options": []}

   if kind == WORKED_EXAMPLE:
      return {"answer_key": section.get("answer"), "options": []}

   options = []

   for option in section.get("options") or []:
      keyed = dict(option)
      needs_value = keyed.get("is_key") is True and keyed.get("value") is None

      if needs_value:
         keyed["value"] = _label_value(keyed.get("label"))

      options.append(keyed)

   return {"answer_key": section.get("answer_key"), "options": options}


def question_key_forms(section):
   return agent_checks.key_forms(question_key(section), bare_whole_numbers=True)


def pointable_sections(lesson, served_stage, matched_error_id=None):
   excluded = set(UNPOINTABLE_DURING_PRACTICE)
   is_unsupported = served_stage == UNSUPPORTED

   if is_unsupported:
      excluded |= set(UNPOINTABLE_AT_UNSUPPORTED)

   sections = []

   for section in _lesson_sections(lesson):
      is_matched_error = matched_error_id is not None and section.get("error_id") == matched_error_id
      is_pointable = section["type"] not in excluded or is_matched_error

      if is_pointable:
         sections.append({"id": section["id"], "type": section["type"]})

   return sections


def _collected_strings(value, into):
   if isinstance(value, str):
      stripped = value.strip()

      if stripped != "":
         into.append(stripped)

      return

   if isinstance(value, dict):
      for key, inner in value.items():
         is_content = key not in SECTION_META_KEYS

         if is_content:
            _collected_strings(inner, into)

      return

   if isinstance(value, list):
      for inner in value:
         _collected_strings(inner, into)


def section_text(section):
   """A lesson section's own words, in the order the record holds them, without its metadata."""
   strings = []
   _collected_strings(section, strings)

   return " ".join(strings)


def _lesson_ref(context, lesson):
   return {
      "id": _field(lesson, "id"),
      "version": _field(lesson, "version"),
      "concept": target_name(context, _field(lesson, "target_id") or _lesson_body(lesson).get("target_id")),
   }


def _representations(context, item, archetype):
   registry = _registry(context, "representations")
   codes = [_field(item, "representation")] + list(archetype.get("representations") or [])
   ordered = [code for code in dict.fromkeys(codes) if code]

   return [{"code": code, "name": _name_of(registry, code)} for code in ordered]


def _skill_names(context, item, archetype):
   skill_ids = _decoded(_field(item, "skills")) or archetype.get("skills") or []
   registry = _registry(context, "skills")

   return [_name_of(registry, skill_id) for skill_id in skill_ids]


def _option_letters(item, item_format):
   is_mcq = item_format == MCQ

   if not is_mcq:
      return None

   options = _decoded(_field(item, "options")) or []

   return [option["id"] for option in options]


def figure_summary(item):
   """What the item's figure shows the student: its kind, window and alt text, and a table's columns
   and rows. None for an item without a figure. An items row holds it as figure_spec and a bank
   record as figure."""
   spec = _decoded(_field(item, "figure_spec")) or _decoded(_field(item, "figure"))
   is_figure = isinstance(spec, dict)

   if not is_figure:
      return None

   kind = spec.get("kind")
   summary = {"kind": kind, "alt": spec.get("alt") or ""}

   if kind == TABLE_FIGURE:
      summary["columns"] = [str(column) for column in spec.get("columns") or []]
      summary["rows"] = [[str(cell) for cell in row] for row in spec.get("rows") or []]

      return summary

   has_window = spec.get("domain") is not None and spec.get("range") is not None
   summary["window"] = {"x": list(spec["domain"]), "y": list(spec["range"])} if has_window else None

   return summary


def practice_body(context, screen, item, attempt, archetype, lesson, misconception_names):
   served_stage = _field(attempt, "served_stage") or screen["served_stage"]
   item_format = _field(attempt, "format") or screen["format"]
   body = {
      "item": {
         "id": _field(item, "id"),
         "format": item_format,
         "served_stage": served_stage,
         "stem": _stem_text(item),
      },
      "archetype": {
         "id": archetype["id"],
         "name": archetype["name"],
         "expected_solution_path": list(archetype["expected_solution_path"]),
      },
      "representations": _representations(context, item, archetype),
      "skills": _skill_names(context, item, archetype),
      "persistent_misconceptions": [str(name) for name in misconception_names],
      "lesson": None,
   }
   letters = _option_letters(item, item_format)

   if letters is not None:
      body["item"]["options"] = letters

   figure = figure_summary(item)

   if figure is not None:
      body["figure"] = figure

   if lesson is not None:
      body["lesson"] = dict(_lesson_ref(context, lesson), sections=pointable_sections(lesson, served_stage))

   return body


def _content_words(text):
   """Words of four letters or more cut to their first five, so trapezoid meets trapezoidal and
   value meets values."""
   return {word[:STEM_LENGTH] for word in CONTENT_WORD.findall(str(text).lower()) if word not in STOP_WORDS}


def point_type_for_step(archetype, step_index, scoring_points):
   path = list(archetype.get("expected_solution_path") or [])
   point_ids = list(archetype.get("point_types") or [])
   is_in_path = 0 <= step_index < len(path)

   has_candidates = bool(point_ids) and is_in_path

   if not has_candidates:
      return None

   step_words = _content_words(path[step_index])
   matching_ids = []

   for point_id in point_ids:
      record = scoring_points.get(point_id)

      if record is None:
         continue

      shared = len(step_words & _content_words(record.get("name", "")))
      is_match = shared >= MINIMUM_SHARED_WORDS

      if is_match:
         matching_ids.append(point_id)

   is_unambiguous = len(matching_ids) == 1

   if not is_unambiguous:
      return None

   best_id = matching_ids[0]
   record = scoring_points[best_id]

   return {
      "id": best_id,
      "name": record.get("name"),
      "earns": record.get("earns"),
      "does_not_earn": record.get("does_not_earn"),
   }


def leading_probe(context, diagnosis):
   if diagnosis is None:
      return None

   hypotheses = _decoded(_field(diagnosis, "misconception_hypotheses")) or []
   ranked = sorted(
      (entry for entry in hypotheses if isinstance(entry, dict)),
      key=lambda entry: -float(entry.get("probability") or 0.0),
   )

   if not ranked:
      return None

   leading_id = ranked[0].get("misconception_id") or ranked[0].get("id")
   record = _registry(context, "misconceptions").get(leading_id) or {}

   return record.get("discriminating_probe")


def _worked_solution_texts(worked_solution):
   steps = _decoded(worked_solution) or []

   return [step["text"] for step in steps if isinstance(step, dict) and "text" in step]


def _feedback_kind(feedback):
   kind = _field(feedback, "kind")

   return getattr(kind, "value", kind)


def feedback_body(context, item, attempt, archetype, lesson, feedback, diagnosis):
   kind = _feedback_kind(feedback)
   correct = _field(attempt, "correct")
   body = {"kind": kind, "correct": None if correct is None else bool(correct)}
   elaborated = _field(feedback, "elaborated")
   shows_worked_solution = kind in WORKED_SOLUTION_KINDS
   error_id = None

   if elaborated is not None:
      error_id = _field(elaborated, "error_id")
      step_index = _field(elaborated, "violated_step_index")
      body.update({
         "violated_step": _field(elaborated, "violated_step"),
         "observed_behavior": _field(elaborated, "observed_behavior"),
         "scoring_consequence": _field(elaborated, "scoring_consequence"),
         "error_id": error_id,
      })
      point = point_type_for_step(archetype, step_index, _registry(context, "scoring_points"))

      if point is not None:
         body["point"] = point

   if shows_worked_solution:
      source = _field(elaborated, "worked_solution") if elaborated is not None else _field(item, "worked_solution")
      body["worked_solution"] = _worked_solution_texts(source)

   probe = leading_probe(context, diagnosis)

   if probe:
      body["discriminating_probe"] = probe

   has_error_section = error_id is not None and lesson is not None

   if has_error_section:
      anchor = next(
         (section["id"] for section in _lesson_sections(lesson) if section.get("error_id") == error_id),
         None,
      )

      if anchor is not None:
         body["lesson_section"] = anchor

   return body, probe is not None


def lesson_question_body(context, screen, lesson, section):
   """The practice packet for a lesson section that poses a question: the question text, the option
   letters and, when the section names one, the archetype's path, built from an allow-list like
   practice_body, so the key, the resolution, the options' labels and correctness, the right step
   and the held-back steps are excluded by construction."""
   item_format = question_format(section)
   reference = _lesson_ref(context, lesson)
   reference.update({
      "part": screen["section_index"] + 1,
      "of": screen["section_count"],
      "section": {"id": section["id"], "type": section_type(section)},
      "sections": [entry for entry in pointable_sections(lesson, UNSUPPORTED) if entry["id"] != section["id"]],
   })
   body = {
      "screen": screen["kind"],
      "item": {"id": section["id"], "format": item_format, "stem": question_text(section)},
      "lesson": reference,
   }
   is_mcq = item_format == MCQ

   if is_mcq:
      body["item"]["options"] = [option["id"] for option in section.get("options") or []]

   archetype = getattr(context, "archetypes", {}).get(section.get("archetype_id"))

   if archetype is not None:
      body["archetype"] = {
         "id": archetype["id"],
         "name": archetype["name"],
         "expected_solution_path": list(archetype["expected_solution_path"]),
      }

   return body


def browsing_body(context, screen, lesson):
   kind = screen["kind"]

   if kind in LESSON_SCREENS:
      has_matching_lesson = lesson is not None and _field(lesson, "id") == screen["lesson_id"]

      if not has_matching_lesson:
         raise ValueError("the lesson row does not match the screen")

      section = screen_section(screen, lesson)

      if section is None:
         raise ValueError("the section is not in this lesson")

      reference = _lesson_ref(context, lesson)
      reference.update({
         "part": screen["section_index"] + 1,
         "of": screen["section_count"],
         "section": {"id": section["id"], "type": section["type"], "text": section_text(section)},
      })

      return {"screen": kind, "lesson": reference}

   skill_id = screen.get("skill_id")
   is_skill = kind == "progress" and skill_id is not None

   if is_skill:
      record = _registry(context, "skills").get(skill_id) or {}
      adaptive = record.get("adaptive") or {}

      return {
         "screen": kind,
         "skill": {
            "id": skill_id,
            "name": record.get("name") or skill_id,
            "criteria": {
               "description": record.get("description_plain"),
               "mastered_if": adaptive.get("mastered_if"),
               "partially_mastered_if": adaptive.get("partially_mastered_if"),
            },
         },
      }

   return {"screen": kind}


def screen_names(context, screen, lesson=None):
   names = {}
   lesson_id = screen.get("lesson_id")

   if lesson_id is not None:
      target = _field(lesson, "target_id") if lesson is not None else None
      names[lesson_id] = target_name(context, target) if target else lesson_id

   skill_id = screen.get("skill_id")

   if skill_id is not None:
      names[skill_id] = _name_of(_registry(context, "skills"), skill_id)

   return names


def memory_payload(entries):
   payload = []

   for entry in list(entries)[:MEMORY_ENTRY_LIMIT]:
      text = _field(entry, "text")
      has_text = isinstance(text, str) and text.strip() != ""

      if has_text:
         payload.append({"kind": _field(entry, "kind"), "text": text})

   return tuple(payload)


def profile_payload(profile):
   if profile is None:
      return None

   return {key: value for key, value in dict(profile).items() if key not in PROFILE_FIELDS_NEVER_RENDERED}


def _item_figure_anchor(figure):
   if figure is None:
      return None

   if figure["kind"] == TABLE_FIGURE:
      return {"id": "item_table", "kind": TABLE_ANCHOR, "rows": len(figure["rows"]), "columns": len(figure["columns"])}

   window = figure.get("window")

   return None if window is None else {"id": "item_figure", "kind": GRAPH_ANCHOR, "window": window}


def feedback_text(feedback):
   parts = [feedback.get(field) for field in FEEDBACK_TEXT_FIELDS]

   return " ".join(part for part in parts if isinstance(part, str) and part.strip() != "")


def item_anchors(mode, body):
   anchors = [{"id": "stem", "kind": TEXT_ANCHOR}]
   figure_anchor = _item_figure_anchor(body.get("figure"))

   if figure_anchor is not None:
      anchors.append(figure_anchor)

   is_checked = mode == AFTER_SUBMISSION

   if not is_checked:
      return anchors

   feedback = body.get("feedback") or {}
   kind = feedback.get("kind")
   is_unsupported = body["item"]["served_stage"] == UNSUPPORTED
   has_feedback_text = feedback_text(feedback) != ""

   # app/web/src/session/SessionScreen.tsx shows the elaborated panel only at the unsupported stage
   # and the step marks only below it.
   shows_elaborated_panel = is_unsupported and kind == ELABORATED_FEEDBACK and has_feedback_text
   shows_step_marks = not is_unsupported and kind == STEP_VERIFICATION_FEEDBACK

   if shows_elaborated_panel:
      anchors.append({"id": "feedback", "kind": TEXT_ANCHOR})

   if not shows_step_marks:
      return anchors

   for number, _step in enumerate(feedback.get("worked_solution") or [], start=1):
      anchors.append({"id": f"solution_step_{number}", "kind": TEXT_ANCHOR})

   return anchors


def lesson_anchors(section):
   anchors = [{"id": "section", "kind": TEXT_ANCHOR}]
   delivery = (section or {}).get("delivery") or {}
   is_drawn = delivery.get("mode") in DRAWN_DELIVERY_MODES and delivery.get("spec") is not None

   if is_drawn:
      anchors.append({"id": "section_figure", "kind": ELEMENT_ANCHOR})

   return anchors


def anchor_texts(body):
   """The text of every text anchor, read from the fields the packet carries for it."""
   texts = {}
   stem = (body.get("item") or {}).get("stem")
   section = (body.get("lesson") or {}).get("section") or {}
   feedback = body.get("feedback") or {}
   is_lesson_question = body.get("screen") in LESSON_SCREENS and isinstance(stem, str)

   if isinstance(stem, str):
      texts["stem"] = stem

   if section.get("text"):
      texts["section"] = section["text"]
   elif is_lesson_question:
      texts["section"] = stem

   if feedback_text(feedback):
      texts["feedback"] = feedback_text(feedback)

   for number, step in enumerate(feedback.get("worked_solution") or [], start=1):
      texts[f"solution_step_{number}"] = str(step)

   return texts


def turn_anchors(body):
   """The packet's anchors with each text anchor's text attached, as the marks reader takes them."""
   texts = anchor_texts(body)
   anchors = []

   for anchor in body.get("anchors") or []:
      is_text = anchor["kind"] == TEXT_ANCHOR
      anchors.append(dict(anchor, text=texts.get(anchor["id"], "")) if is_text else dict(anchor))

   return anchors


def compose_packet(
   context,
   screen,
   item=None,
   attempt=None,
   archetype=None,
   lesson=None,
   feedback=None,
   memory_entries=(),
   profile=None,
   misconception_names=(),
   turn_index_on_item=0,
   student_answered_question=False,
   diagnosis=None,
   drawing_enabled=True,
):
   """The packet and the move for one turn. diagnosis is the attempt's diagnoses row, read only for
   the leading misconception's probe after submission. drawing_enabled is the drawing switch."""
   check = validate_screen(screen)

   if check.timed:
      raise TimedPartRefused("not available during a timed part")

   mode = mode_for(screen, attempt, lesson)
   line = screen_line(screen, screen_names(context, screen, lesson))
   has_probe = False
   lesson_question = question_section(screen, lesson)

   if mode == BROWSING:
      body = browsing_body(context, screen, lesson)
      is_lesson = check.kind in LESSON_SCREENS
      body["anchors"] = lesson_anchors(screen_section(screen, lesson)) if is_lesson else []
   elif lesson_question is not None:
      body = lesson_question_body(context, screen, lesson, lesson_question)
      body["anchors"] = lesson_anchors(lesson_question)
   else:
      has_item = item is not None and _field(item, "id") == screen["item_id"]

      if not has_item:
         raise ValueError("the item row does not match the screen")

      archetype = archetype or getattr(context, "archetypes", {}).get(_field(item, "archetype_id"))

      if archetype is None:
         raise ValueError("the item names no archetype in this snapshot")

      body = practice_body(context, screen, item, attempt, archetype, lesson, misconception_names)

   if mode == AFTER_SUBMISSION:
      feedback_fields, has_probe = feedback_body(context, item, attempt, archetype, lesson, feedback, diagnosis)
      body["feedback"] = feedback_fields
      matched = feedback_fields.get("error_id")
      has_lesson = lesson is not None

      if has_lesson:
         served_stage = body["item"]["served_stage"]
         body["lesson"]["sections"] = pointable_sections(lesson, served_stage, matched)

   is_on_an_item = "anchors" not in body

   if is_on_an_item:
      body["anchors"] = item_anchors(mode, body)

   move = choose_move(
      mode,
      turn_index_on_item,
      student_answered_question,
      has_probe=has_probe,
      screen_kind=check.kind,
   )
   packet = Packet(
      mode=mode,
      move=move,
      screen_line=line,
      body=body,
      turn_index=turn_index_on_item,
      memory=memory_payload(memory_entries),
      profile=profile_payload(profile),
      drawing=drawing_for(move, drawing_enabled),
   )

   return packet, move


def shown_figure_line(figure):
   """The line an agent turn's shown figure adds to the history, or None."""
   spec = shown_spec(figure)

   if spec is None:
      return None

   return f"[Figure shown: {spec.get('title', '')}. {spec.get('description', '')}]"


def _history_payload(history):
   turns = []

   for turn in list(history)[-HISTORY_TURN_LIMIT:]:
      role = _field(turn, "role")
      is_known_role = role in HISTORY_ROLES

      if not is_known_role:
         continue

      text = _field(turn, "text") or ""
      figure_line = shown_figure_line(_field(turn, "figure")) if role == AGENT_ROLE else None

      if figure_line is not None:
         text = f"{text}\n{figure_line}"

      turns.append({"role": role, "text": text})

   return turns


def live_template_text():
   return LIVE_TEMPLATE_PATH.read_text()


def render_prompt(packet, memory_entries, profile, history, student_message):
   """The system prefix, byte-identical on every turn, and the variable section below the marker,
   where every field is JSON-encoded except the three the app composes itself."""
   text = live_template_text()
   system, variable_section = split_template(text)
   rendered_profile = profile_payload(profile)
   fields = {
      "mode": packet.mode,
      "move": packet.move,
      "screen_line": packet.screen_line,
      "packet": json.dumps(packet.body, sort_keys=True, ensure_ascii=False),
      "memory": json.dumps(list(memory_payload(memory_entries)), ensure_ascii=False),
      "profile": "null" if rendered_profile is None else json.dumps(rendered_profile, sort_keys=True, ensure_ascii=False),
      "history": json.dumps(_history_payload(history), ensure_ascii=False),
      "student_message": json.dumps(str(student_message), ensure_ascii=False),
   }
   asks_for_drawing = AGENT_DRAWING_FIELD in template_placeholders(variable_section)

   if asks_for_drawing:
      fields[AGENT_DRAWING_FIELD] = packet.drawing

   return RenderedPrompt(system=system, user=render_template(text, fields))
