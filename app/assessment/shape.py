"""The shape of every timed and untimed assessment, read at run time and never restated.

Counts, minutes, calculator status and weights come from research/exam/exam-structure.md through
app/checkpoint/published.py. Order, labels, booklet wording and the part-boundary copy come from
the form template, content/assessment/form_2027.json, because the 2027 booklet layout is an
assumption (11 P5 "Risks and rollback") and a correction to it should be a data edit.

The tool set is 05's deliberate subset of Bluebook's documented tools: a hideable timer with a
five-minute alert, highlight and notes, mark for review, the option eliminator on multiple choice,
the question menu and zoom, plus the graphing panel on calculator parts only (11 P5 scope item 3).
"""
import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from app.checkpoint import published

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FORM_TEMPLATE_PATH = REPOSITORY_ROOT / "content" / "assessment" / "form_2027.json"

MULTIPLE_CHOICE = "Multiple choice"
CALCULATOR_REQUIRED = "Required"
CALCULATOR_NOT_PERMITTED = "Not permitted"

TIMER = "timer"
HIGHLIGHT_AND_NOTES = "highlight_and_notes"
MARK_FOR_REVIEW = "mark_for_review"
OPTION_ELIMINATOR = "option_eliminator"
QUESTION_MENU = "question_menu"
ZOOM = "zoom"
GRAPHING_PANEL = "graphing_panel"

FIVE_MINUTE_ALERT_SECONDS = 5 * 60


class ShapeUnreadable(RuntimeError):
   pass


@dataclass(frozen=True)
class PartShape:
   key: str
   section: str
   part: str
   label: str
   question_type: str
   questions: int
   minutes: int
   calculator_required: bool
   weighting: float

   @property
   def is_multiple_choice(self):
      return self.question_type == MULTIPLE_CHOICE

   @property
   def seconds(self):
      return self.minutes * 60

   @property
   def budget_seconds_per_question(self):
      return self.seconds / self.questions


@lru_cache(maxsize=1)
def form_template(path=FORM_TEMPLATE_PATH):
   return json.loads(Path(path).read_text())


def calculator_required(cell):
   is_required = cell == CALCULATOR_REQUIRED
   is_not_permitted = cell == CALCULATOR_NOT_PERMITTED

   if not is_required and not is_not_permitted:
      raise ShapeUnreadable(f"unknown calculator rule {cell!r} in exam-structure.md")

   return is_required


@lru_cache(maxsize=1)
def part_shapes():
   """The four parts in the template's order, each joined to its row of exam-structure.md."""
   rows = {(row.section, row.part): row for row in published.exam_parts()}
   shapes = []

   for entry in form_template()["parts"]:
      row = rows.get((entry["section"], entry["part"]))

      if row is None:
         raise ShapeUnreadable(f"exam-structure.md has no row for {entry['key']}")

      shapes.append(
         PartShape(
            key=entry["key"],
            section=row.section,
            part=row.part,
            label=entry["label"],
            question_type=row.question_type,
            questions=row.questions,
            minutes=row.minutes,
            calculator_required=calculator_required(row.calculator),
            weighting=row.weighting,
         )
      )

   has_every_row = len(shapes) == len(rows)

   if not has_every_row:
      raise ShapeUnreadable("the form template and exam-structure.md disagree on the parts")

   return tuple(shapes)


def part_shape(key):
   for shape in part_shapes():
      if shape.key == key:
         return shape

   raise KeyError(f"no exam part {key!r}")


def part_keys():
   return tuple(shape.key for shape in part_shapes())


def section_weights():
   """Each section's share of the exam in percent, summed from its parts' published weights."""
   weights = {}

   for shape in part_shapes():
      weights[shape.section] = weights.get(shape.section, 0.0) + shape.weighting

   return {section: round(weight, 1) for section, weight in weights.items()}


def multiple_choice_total():
   return sum(shape.questions for shape in part_shapes() if shape.is_multiple_choice)


def free_response_total():
   return sum(shape.questions for shape in part_shapes() if not shape.is_multiple_choice)


def first_number(shape):
   """Numbering runs continuously within a section, so Part B of Section I opens at 30."""
   earlier = [other for other in part_shapes() if other.section == shape.section]
   number = 1

   for other in earlier:
      if other.key == shape.key:
         return number

      number += other.questions

   raise KeyError(shape.key)


def tools_for(shape):
   tools = [TIMER, HIGHLIGHT_AND_NOTES, MARK_FOR_REVIEW]

   if shape.is_multiple_choice:
      tools.append(OPTION_ELIMINATOR)

   tools.extend([QUESTION_MENU, ZOOM])

   if shape.calculator_required:
      tools.append(GRAPHING_PANEL)

   return tools


def part_payload(shape):
   template = form_template()
   calculator_label = template["calculator_required_label"] if shape.calculator_required else template["calculator_absent_label"]

   return {
      "key": shape.key,
      "section": shape.section,
      "part": shape.part,
      "label": shape.label,
      "question_type": shape.question_type,
      "multiple_choice": shape.is_multiple_choice,
      "question_count": shape.questions,
      "minutes": shape.minutes,
      "calculator": shape.calculator_required,
      "calculator_label": calculator_label,
      "calculator_note": None if shape.calculator_required else template["calculator_absent_note"],
      "first_number": first_number(shape),
      "budget_seconds_per_question": shape.budget_seconds_per_question,
      "tools": tools_for(shape),
      "five_minute_alert_seconds": FIVE_MINUTE_ALERT_SECONDS,
   }


def shape_payload():
   template = form_template()

   return {
      "form": template["form"],
      "parts": [part_payload(shape) for shape in part_shapes()],
      "multiple_choice_total": multiple_choice_total(),
      "free_response_total": free_response_total(),
      "points_per_free_response_question": published.points_per_free_response_question(),
      "section_weights": section_weights(),
      "testing_minutes": sum(shape.minutes for shape in part_shapes()),
      "reference_sheet": template["reference_sheet"],
      "radian_note": template["radian_note"],
   }
