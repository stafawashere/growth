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

PUBLISHED_STATUS = "verified"


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
