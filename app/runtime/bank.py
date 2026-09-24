"""The item bank over the items table, per docs/plan/06-architecture.md "items".

Published means items.status == "verified" (docs/plan/11-phased-delivery.md P1 scope item 14,
Q14): app/engine/select.py and app/session/build.py call only published_items(archetype_id) and
has_published_item(archetype_id), the ItemBank protocol app/engine/fringe.py declares. An empty
bank answers with no rows rather than raising.

A bank may be given an ItemSource, the directories of item records (app/main.py GROWTH_ITEMS_DIR,
by default every content/items_* bank). Its new records go through app/items/ingest.py, checks
and provenance included, on the bank's first query rather than at build time: the checks take
seconds per hundred records, and a process that never opens a session, which is most of what
builds an application, should not pay for them.

Items the stable concept probe names (app/runtime/probe_set.py) are ingested like any other, so
the probe can be graded, and are never returned for practice: an item that is both probe and
practice would measure its own exposure.
"""
import json
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy.orm import Session as OrmSession

from app.db.models import Item
from app.engine.state import FadingStage
from app.items.ingest import ingest_new_records, load_records
from app.runtime.probe_set import probe_item_ids

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
      "requires_choice": _is_statement_keyed(row),
   }


def _is_statement_keyed(row):
   """04's key form "statement": the answer is one of the labelled options and nothing a student
   could type, so the item is always served as a choice (app/engine/select.py requires_choice)."""
   key = _json_field(row.answer_key) or {}

   return key.get("form") == "statement"


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

   Backward fading (11 P1 scope 8): stage example and stage completion both blank the last step
   and leave it for the student to answer, stage unsupported shows none. The operator's ruling on
   how a skill leaves stage example (BUILD-LEDGER.md, "Decisions taken on the operator's
   instruction, 2026-09-23") withdraws 11 implementer decision 3: example now collects a graded
   answer exactly as completion does, so the two stages blank the same way and need the same
   2-step minimum of Q16 to have a step to blank. Below the minimum, showing every given step
   would show the answer along with them, and the stage still grades and credits what it collects,
   so both stages refuse rather than degrade; app/session/service.py resolve_served_stage rewrites
   such a slot to unsupported before served_item ever calls this function on it. No step carries
   its mathjson, because the last step's mathjson is the answer key (app/items/ingest.py checks
   the key against it).
   """
   served_stage = FadingStage(stage)
   is_unsupported = served_stage == FadingStage.UNSUPPORTED

   if is_unsupported:
      return None

   steps = worked_steps(worked_solution)
   has_blank_room = supports_completion(worked_solution)

   if not has_blank_room:
      raise ValueError(
         f"stage {served_stage.value} needs at least {COMPLETION_MINIMUM_STEPS} worked steps "
         "to blank the last one"
      )

   shown = steps[:-1]

   return [
      {"index": position, "text": step["text"]}
      for position, step in enumerate(shown, start=1)
   ]


def refuse_duplicate_ids(directories):
   """ingest_new_records skips an id already stored, so an id in two banks would be served from
   whichever directory came first and the other record would be silently ignored."""
   first_seen = {}

   for directory in directories:
      for record in load_records(directory):
         item_id = record.get("id")
         earlier = first_seen.get(item_id)
         is_duplicate = item_id is not None and earlier is not None

         if is_duplicate:
            raise ValueError(f"item {item_id} is in both {earlier} and {directory}")

         first_seen[item_id] = directory


@dataclass(frozen=True)
class ItemSource:
   directories: tuple
   active_error_ids: frozenset
   snapshot_id: str


class ItemBank:
   """An ItemBank over the live items table, one short-lived session per query."""

   def __init__(self, engine, source=None, withheld_ids=None):
      self._engine = engine
      self._withheld_ids = probe_item_ids() if withheld_ids is None else frozenset(withheld_ids)
      self._pending_source = source
      self._source_lock = threading.Lock()

   def _ingest_pending_source(self):
      """Runs once per process. A failed ingestion leaves the source pending, so the error
      surfaces again on the next query instead of leaving a silently empty bank.
      """
      with self._source_lock:
         source = self._pending_source
         has_pending_source = source is not None

         if not has_pending_source:
            return

         ingested_at = datetime.now(timezone.utc).isoformat()

         refuse_duplicate_ids(source.directories)

         with OrmSession(self._engine) as db:
            for directory in source.directories:
               ingest_new_records(
                  db, directory, source.active_error_ids, source.snapshot_id, ingested_at
               )

            db.commit()

         self._pending_source = None

   def ensure_ingested(self):
      """Ingests the pending source now. The concept probe reads items rows by id, which a bank
      that has never been queried for practice has not written yet."""
      self._ingest_pending_source()

   def published_items(self, archetype_id):
      self._ingest_pending_source()

      with OrmSession(self._engine) as db:
         rows = (
            db.query(Item)
            .filter(Item.archetype_id == archetype_id, Item.status == PUBLISHED_STATUS)
            .order_by(Item.id)
            .all()
         )

         return [_as_item_dict(row) for row in rows if row.id not in self._withheld_ids]

   def has_published_item(self, archetype_id):
      return len(self.published_items(archetype_id)) > 0
