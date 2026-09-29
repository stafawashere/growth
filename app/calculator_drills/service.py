"""Serving and answering Desmos fluency drills, and reading the procedure cards
(docs/calculator/build-plan.md, Contracts and Slice 2; docs/calculator/architecture.md, Routes).

A drill writes calculator_drills and audit_log and nothing else (invariant C0). The keys are never
stored: the row keeps the seed the task was drawn from, and the answer rebuilds the task through
the template's own build so the value and setup keys are recomputed every time.
"""
import json
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path

from sqlalchemy import func, select, update

from app.assessment.shape import part_shape
from app.auth.service import as_iso, new_id, utc_now, write_audit
from app.calculator import registry
from app.calculator.check import check_setup, check_value
from app.db import models
from app.generation.spec import DrawExhausted, draw_with_seed, rng_for

DESMOS_COLLEGE_BOARD_URL = "https://www.desmos.com/testing/collegeboard/graphing"
MIXED = "mixed"
CALCULATOR_PARTS = ("I-B", "II-A")
ELAPSED_GRACE_MS = 2000
SERVED_ACTION = "calculator_drill_served"
ANSWERED_ACTION = "calculator_drill_answered"
NO_BLUEBOOK_NOTE = "none"
CARD_FIELDS_WITHHELD = ("sources", "evidence_tag")

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CARDS_DIRECTORY = REPOSITORY_ROOT / "content" / "calculator" / "cards"


class UnknownTemplate(ValueError):
   pass


class DrillNotFound(LookupError):
   pass


class DrillAlreadyAnswered(RuntimeError):
   pass


def budget_seconds():
   return {key: part_shape(key).budget_seconds_per_question for key in CALCULATOR_PARTS}


@lru_cache(maxsize=1)
def _card_records():
   records = {}

   for path in sorted(CARDS_DIRECTORY.glob("*.json")):
      record = json.loads(path.read_text())
      records[record["id"]] = record

   return records


def card_summaries():
   return [
      {
         "id": record["id"],
         "capability": record["capability"],
         "title": record["title"],
         "task": record["task"],
         "drills": list(record["drills"]),
      }
      for record in _card_records().values()
   ]


def card(card_id):
   """The card as the student reads it: no sources, no evidence tag and no error ids, which are
   library ids."""
   record = _card_records().get(card_id)

   if record is None:
      return None

   shown = {key: value for key, value in record.items() if key not in CARD_FIELDS_WITHHELD}
   shown["exam_habit"] = [{"text": habit["text"]} for habit in record["exam_habit"]]
   has_no_note = record.get("bluebook_note") in (None, "", NO_BLUEBOOK_NOTE)
   shown["bluebook_note"] = None if has_no_note else record["bluebook_note"]

   return shown


def _count(db, user_id, *conditions):
   statement = select(func.count()).select_from(models.CalculatorDrill).where(models.CalculatorDrill.user_id == user_id)

   for condition in conditions:
      statement = statement.where(condition)

   return db.scalar(statement)


def resolve_capability(db, user_id, capability):
   is_mixed = capability == MIXED

   if not is_mixed:
      return capability

   served_so_far = _count(db, user_id)
   rng = rng_for(f"{MIXED}:{user_id}:{served_so_far}")

   return rng.choice(registry.CAPABILITIES)


def choose_template(db, user_id, capability):
   """Round robin over the capability's templates by how many drills of it the student has had."""
   template_ids = sorted(registry.templates_for(capability))
   served_of_capability = _count(db, user_id, models.CalculatorDrill.capability == capability)

   return template_ids[served_of_capability % len(template_ids)]


def draw_first_clear(module, seed):
   """registry.draw_task's loop, keeping the seed that settled so the answer can redraw it."""
   for attempt in range(registry.MAX_REDRAWS + 1):
      settled_seed = registry.redraw_seed(seed, attempt)
      _, names = draw_with_seed(module.SPEC, settled_seed)
      task = module.build(names)

      if task.exclusion is None:
         return task, settled_seed

   raise DrawExhausted(f"{module.TEMPLATE_ID} excluded {registry.MAX_REDRAWS + 1} draws from seed {seed!r}")


def serve(db, user_id, capability, template_id=None, now=None):
   moment = now or utc_now()
   known_templates = registry.templates()

   if template_id is not None:
      module = known_templates.get(template_id)
      is_unknown = module is None
      names_other_capability = not is_unknown and capability not in (MIXED, module.CAPABILITY)

      if is_unknown or names_other_capability:
         raise UnknownTemplate(f"no drill template {template_id!r} for {capability}")
   else:
      template_id = choose_template(db, user_id, resolve_capability(db, user_id, capability))
      module = known_templates[template_id]

   drills_of_template = _count(db, user_id, models.CalculatorDrill.template_id == template_id)
   seed = f"{template_id}:v{module.TEMPLATE_VERSION}:{user_id}:{drills_of_template}"
   task, settled_seed = draw_first_clear(module, seed)
   stamp = as_iso(moment)
   draw = {"template_version": module.TEMPLATE_VERSION, "seed": seed, "settled_seed": settled_seed, "parameters": task.draw}
   row = models.CalculatorDrill(
      id=new_id("cdr"),
      user_id=user_id,
      template_id=template_id,
      capability=module.CAPABILITY,
      draw=json.dumps(draw),
      desmos_url=DESMOS_COLLEGE_BOARD_URL,
      served_at=stamp,
      setup_shown=0,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(row)
   db.flush()
   write_audit(
      db,
      user_id,
      SERVED_ACTION,
      f"calculator_drills:{row.id}",
      {"template_id": template_id, "capability": module.CAPABILITY},
      moment,
   )

   return {
      "drill_id": row.id,
      "template_id": template_id,
      "capability": module.CAPABILITY,
      "card_id": module.CARD_ID,
      "prompt": task.prompt,
      "function_tex": task.function_tex,
      "unit": task.unit,
      "radian_sensitive": task.radian_sensitive,
      "desmos_url": row.desmos_url,
      "served_at": stamp,
   }


def rebuilt_task(row):
   draw = json.loads(row.draw)
   module = registry.templates()[row.template_id]
   _, names = draw_with_seed(module.SPEC, draw["settled_seed"])

   return module.build(names)


def bounded_elapsed(elapsed_ms, served_at, moment):
   """The client's measurement, never longer than the time since the task was served plus a grace
   for the clock the client starts after the response arrives."""
   since_served = moment - datetime.fromisoformat(served_at)
   ceiling = int(since_served / timedelta(milliseconds=1)) + ELAPSED_GRACE_MS

   return max(0, min(int(elapsed_ms), ceiling))


def as_flag(value):
   return None if value is None else int(bool(value))


def answer(db, user_id, drill_id, value, setup_mathjson, elapsed_ms, desmos_open, now=None):
   moment = now or utc_now()
   row = db.get(models.CalculatorDrill, drill_id)
   is_theirs = row is not None and row.user_id == user_id

   if not is_theirs:
      raise DrillNotFound(drill_id)

   if row.submitted_at is not None:
      raise DrillAlreadyAnswered(drill_id)

   task = rebuilt_task(row)
   value_verdict = check_value(value, task.value_key)
   setup_verdict = check_setup(setup_mathjson, task)
   elapsed = bounded_elapsed(elapsed_ms, row.served_at, moment)
   stamp = as_iso(moment)
   completed = db.execute(
      update(models.CalculatorDrill)
      .where(models.CalculatorDrill.id == drill_id)
      .where(models.CalculatorDrill.submitted_at.is_(None))
      .values(
         submitted_at=stamp,
         elapsed_ms=elapsed,
         value_entered=value,
         value_correct=as_flag(value_verdict.correct),
         value_reason=value_verdict.reason,
         setup_entered=None if setup_mathjson is None else json.dumps(setup_mathjson),
         setup_shown=as_flag(setup_verdict.shown),
         setup_correct=as_flag(setup_verdict.correct),
         setup_reason=setup_verdict.reason,
         updated_at=stamp,
      )
      .execution_options(synchronize_session="fetch")
   )
   lost_the_race = completed.rowcount == 0

   if lost_the_race:
      raise DrillAlreadyAnswered(drill_id)

   write_audit(
      db,
      user_id,
      ANSWERED_ACTION,
      f"calculator_drills:{drill_id}",
      {
         "template_id": row.template_id,
         "capability": row.capability,
         "value_correct": value_verdict.correct,
         "setup_shown": setup_verdict.shown,
         "setup_correct": setup_verdict.correct,
         "elapsed_ms": elapsed,
         "desmos_open": bool(desmos_open),
      },
      moment,
   )

   return {
      "drill_id": drill_id,
      "value": {
         "correct": value_verdict.correct,
         "reason": value_verdict.reason,
         "rounded": value_verdict.rounded,
         "truncated": value_verdict.truncated,
      },
      "setup": {
         "shown": setup_verdict.shown,
         "correct": setup_verdict.correct,
         "reason": setup_verdict.reason,
         "key_latex": setup_verdict.key_latex,
      },
      "elapsed_ms": elapsed,
      "budget_seconds": budget_seconds(),
   }
