"""The item bank over the items table, per docs/plan/06-architecture.md "items".

Published means items.status == "verified" (docs/plan/11-phased-delivery.md P1 scope item 14,
Q14): app/engine/select.py and app/session/build.py call only published_items(archetype_id) and
has_published_item(archetype_id), the ItemBank protocol app/engine/fringe.py declares. The items
table is empty until the operator's 130 hand-authored items land, so an empty bank answers with no
rows rather than raising.
"""
import json

from sqlalchemy.orm import Session as OrmSession

from app.db.models import Item
from app.engine.state import FadingStage

PUBLISHED_STATUS = "verified"

COMPLETION_MINIMUM_STEPS = 2


def _json_field(value):
   is_absent = value is None

   if is_absent:
      return None

   return json.loads(value)


STUDENT_OPTION_FIELDS = ("id", "value", "label", "mathjson")


def _as_served_option(option):
   """An option the student may see: the key is not identifiable and no error path leaks."""
   return {
      name: option[name]
      for name in STUDENT_OPTION_FIELDS
      if name in option
   }


def _as_item_dict(row):
   """What a served item carries. The answer key, the worked solution, the option error paths and
   the is_key flag stay in the items row, because a served item reaches the student through
   sessions.queue and GET /sessions/{id}/next before anything has been submitted (11 P1 scope 10
   and 13, R35).
   """
   options = row.options or []
   has_options = len(options) > 0

   return {
      "id": row.id,
      "archetype_id": row.archetype_id,
      "variant_id": row.variant_id,
      "snapshot_id": row.snapshot_id,
      "parameter_draw": _json_field(row.parameter_draw),
      "stem": row.stem,
      "figure_spec": _json_field(row.figure_spec),
      "options": [_as_served_option(option) for option in options] if has_options else None,
      "calculator_status": row.calculator_status,
      "representation": row.representation,
      "difficulty_settings": _json_field(row.difficulty_settings),
      "skills": _json_field(row.skills),
      "status": row.status,
   }


def _is_step_with_text(step):
   is_mapping = isinstance(step, dict)

   return is_mapping and "text" in step


def worked_steps(worked_solution):
   """The items row's worked_solution as its list of steps, refused when it is anything else."""
   try:
      steps = json.loads(worked_solution)
   except (TypeError, ValueError) as unreadable:
      raise ValueError("worked_solution is not a JSON list of steps") from unreadable

   is_list = isinstance(steps, list)
   is_empty = is_list and len(steps) == 0
   every_step_has_text = is_list and all(_is_step_with_text(step) for step in steps)
   is_step_list = is_list and not is_empty and every_step_has_text

   if not is_step_list:
      raise ValueError("worked_solution is not a non-empty list of steps with text")

   return steps


def supports_completion(worked_solution):
   """Q16: a completion blank needs one step given and one blanked."""
   return len(worked_steps(worked_solution)) >= COMPLETION_MINIMUM_STEPS


def served_steps(worked_solution, stage):
   """The steps the stage shows, numbered from 1, as text only.

   Backward fading (11 P1 scope 8): stage example shows every step, stage completion blanks the
   last one, stage unsupported shows none. A completion needs one step given and one blanked, the
   2-step minimum of Q16. No step carries its mathjson, because the last step's mathjson is the
   answer key (app/items/ingest.py checks the key against it).
   """
   served_stage = FadingStage(stage)
   is_unsupported = served_stage == FadingStage.UNSUPPORTED

   if is_unsupported:
      return None

   steps = worked_steps(worked_solution)
   is_completion = served_stage == FadingStage.COMPLETION
   is_below_minimum = is_completion and not supports_completion(worked_solution)

   if is_below_minimum:
      raise ValueError(f"a completion needs at least {COMPLETION_MINIMUM_STEPS} worked steps")

   shown = steps[:-1] if is_completion else steps

   return [
      {"index": position, "text": step["text"]}
      for position, step in enumerate(shown, start=1)
   ]


class ItemBank:
   """An ItemBank over the live items table, one short-lived session per query."""

   def __init__(self, engine):
      self._engine = engine

   def published_items(self, archetype_id):
      with OrmSession(self._engine) as db:
         rows = (
            db.query(Item)
            .filter(Item.archetype_id == archetype_id, Item.status == PUBLISHED_STATUS)
            .order_by(Item.id)
            .all()
         )

         return [_as_item_dict(row) for row in rows]

   def has_published_item(self, archetype_id):
      return len(self.published_items(archetype_id)) > 0
