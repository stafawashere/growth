"""Filling a part with questions, for the part drills and the full mock.

Multiple-choice parts draw published items by calculator status, as 05 "Timed section drill"
says: a no-calculator part draws only items that need no calculator from archetypes that are not
calculator-only, and a calculator part draws calculator items plus items of archetypes marked
either. Unit representation follows the BC-UNIT band midpoints of research/exam/exam-blueprint.md
(app/engine/exam_weights.py), allotted by largest remainder over the units that have candidates.
Inside a unit, archetypes are spread before any repeats, and items the student has not met in a
timed or untimed session come first.

Free-response parts draw questions whose points total the exam's per-question maximum, read from
exam-structure.md, so a part is at the documented shape or it is refused.

The fringe gate is not applied here. A mock is the whole exam and writes no mastery state; a gated
mock could not be assembled until the whole graph was mastered (BUILD-LEDGER.md, stage 6 plan
corrections). The unit check, which does write mastery, keeps the gate (app/assessment/unit_check.py).
"""
import math
import re
from collections import Counter

from sqlalchemy import select

from app.checkpoint import published
from app.db import models
from app.engine.exam_weights import band_midpoints
from app.frq.items import FRQ_FORMAT
from app.runtime.bank import PUBLISHED_STATUS, as_served_item
from app.runtime.probe_set import probe_item_ids

CALCULATOR_ITEM = "calculator"
NO_CALCULATOR_ITEM = "no_calculator"
EITHER_ARCHETYPE = "either"
CALCULATOR_ARCHETYPE = "calculator"

TRIGONOMETRIC_PATTERN = re.compile(r"\\?(sin|cos|tan|sec|csc|cot|arcsin|arccos|arctan)\b")


class AssessmentUnavailable(ValueError):
   """The bank cannot fill the part at the documented shape. The message is shown."""


def radian_note_applies(stem, calculator_part):
   """11 P5 scope item 8: the note rides on calculator work that evaluates a trigonometric function."""
   has_trigonometry = TRIGONOMETRIC_PATTERN.search(stem or "") is not None

   return calculator_part and has_trigonometry


def fits_part(item_row, archetype, calculator_part):
   archetype_status = archetype.get("calculator_status")

   if calculator_part:
      is_calculator_item = item_row.calculator_status == CALCULATOR_ITEM
      is_either = archetype_status == EITHER_ARCHETYPE

      return is_calculator_item or is_either

   is_plain_item = item_row.calculator_status == NO_CALCULATOR_ITEM
   is_calculator_only = archetype_status == CALCULATOR_ARCHETYPE

   return is_plain_item and not is_calculator_only


def seen_item_ids(db, user_id):
   attempted = db.scalars(
      select(models.Attempt.item_id)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .where(models.Session.user_id == user_id)
   ).all()
   served = db.scalars(select(models.AssessmentResponse.item_id).where(models.AssessmentResponse.user_id == user_id)).all()

   return Counter(list(attempted) + list(served))


def published_rows(db):
   withheld = probe_item_ids()
   rows = db.scalars(select(models.Item).where(models.Item.status == PUBLISHED_STATUS)).all()

   return [row for row in rows if row.id not in withheld]


def unit_allotment(count, units, midpoints):
   """count questions over units, in proportion to their band midpoints, by largest remainder."""
   weights = {unit: float(midpoints.get(unit, 0)) for unit in units}
   total = sum(weights.values())
   has_weight = total > 0

   if not has_weight:
      weights = {unit: 1.0 for unit in units}
      total = float(len(units))

   exact = {unit: count * weight / total for unit, weight in weights.items()}
   allotment = {unit: math.floor(value) for unit, value in exact.items()}
   remainders = sorted(units, key=lambda unit: (-(exact[unit] - allotment[unit]), unit))
   short = count - sum(allotment.values())

   for unit in remainders[:short]:
      allotment[unit] += 1

   return allotment


def choose_from_unit(rows_by_archetype, wanted, seen, rng):
   """One item per archetype before any archetype gives a second, fewest-seen first."""
   archetype_ids = list(rows_by_archetype)
   rng.shuffle(archetype_ids)
   pools = {}

   for archetype_id in archetype_ids:
      rows = list(rows_by_archetype[archetype_id])
      rng.shuffle(rows)
      rows.sort(key=lambda row: seen.get(row.id, 0))
      pools[archetype_id] = rows

   archetype_ids.sort(key=lambda archetype_id: seen.get(pools[archetype_id][0].id, 0))
   chosen = []

   while len(chosen) < wanted:
      progressed = False

      for archetype_id in archetype_ids:
         pool = pools[archetype_id]

         if pool and len(chosen) < wanted:
            chosen.append(pool.pop(0))
            progressed = True

      if not progressed:
         break

   return chosen


def multiple_choice_items(db, user_id, archetypes, calculator_part, count, rng, excluded_ids=()):
   seen = seen_item_ids(db, user_id)
   excluded = set(excluded_ids)
   by_unit = {}

   for row in published_rows(db):
      archetype = archetypes.get(row.archetype_id)
      is_known = archetype is not None
      has_options = bool(row.options)
      is_excluded = row.id in excluded

      if not is_known or not has_options or is_excluded:
         continue

      if not fits_part(row, archetype, calculator_part):
         continue

      unit = archetype.get("primary_unit")
      by_unit.setdefault(unit, {}).setdefault(row.archetype_id, []).append(row)

   available = sum(len(rows) for archetype_rows in by_unit.values() for rows in archetype_rows.values())

   if available < count:
      raise AssessmentUnavailable(f"only {available} published items fit this part; it needs {count}")

   allotment = unit_allotment(count, sorted(by_unit), band_midpoints())
   chosen = []

   for unit in sorted(by_unit):
      chosen.extend(choose_from_unit(by_unit[unit], allotment[unit], seen, rng))

   shortfall = count - len(chosen)

   if shortfall > 0:
      taken = {row.id for row in chosen}
      spare = [row for archetype_rows in by_unit.values() for rows in archetype_rows.values() for row in rows if row.id not in taken]
      rng.shuffle(spare)
      spare.sort(key=lambda row: seen.get(row.id, 0))
      chosen.extend(spare[:shortfall])

   rng.shuffle(chosen)

   return chosen


def question_points(record):
   return sum(len(part["points"]) for part in record["parts"])


def fits_free_response_part(record, calculator_part):
   status = record["calculator_status"]

   if calculator_part:
      return status == CALCULATOR_ITEM

   return status in (NO_CALCULATOR_ITEM, EITHER_ARCHETYPE)


def free_response_attempt_counts(db, user_id):
   rows = db.scalars(
      select(models.Attempt.item_id)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .where(models.Session.user_id == user_id)
      .where(models.Attempt.format == FRQ_FORMAT)
   ).all()

   return Counter(rows)


def free_response_questions(db, user_id, frq_context, calculator_part, count, rng, excluded_ids=()):
   """Questions at the exam's per-question point total, least-used first, one per archetype while
   that is possible."""
   full_points = published.points_per_free_response_question()
   used = free_response_attempt_counts(db, user_id)
   excluded = set(excluded_ids)
   candidates = [
      record
      for record in frq_context.records.values()
      if question_points(record) == full_points
      and fits_free_response_part(record, calculator_part)
      and record["id"] not in excluded
   ]

   if len(candidates) < count:
      kind = "calculator" if calculator_part else "no-calculator"
      raise AssessmentUnavailable(f"only {len(candidates)} {kind} free-response questions carry {full_points} points; this part needs {count}")

   rng.shuffle(candidates)
   candidates.sort(key=lambda record: used.get(record["id"], 0))
   chosen = []
   archetypes_taken = set()

   for record in candidates:
      is_new_archetype = record["archetype_id"] not in archetypes_taken

      if is_new_archetype and len(chosen) < count:
         chosen.append(record)
         archetypes_taken.add(record["archetype_id"])

   for record in candidates:
      if len(chosen) >= count:
         break

      if record not in chosen:
         chosen.append(record)

   return chosen


def served_multiple_choice(row, calculator_part):
   item = as_served_item(row)
   item["radian_note"] = radian_note_applies(row.stem, calculator_part)

   return item
