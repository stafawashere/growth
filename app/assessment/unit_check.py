"""The unit check, 05 "Unit check" and 11 P5 scope item 1.

Untimed, 8 to 12 items spanning every fringe-adjacent skill of the unit, feedback withheld until
the whole check is submitted, and every observation applied to the model at submission.

A skill of the unit is fringe-adjacent when some archetype of the unit that the student may be
served loads it: the archetype has a published item and the fringe gate clears its primary skill
(invariant 3 binds here, because a unit check writes mastery). The check is a greedy set cover of
those skills by archetypes, one item per archetype, because only 31 of 541 skills are
independently assessable and most are reached only inside multi-skill archetypes. A cover that
needs fewer than 8 items is topped up with the archetypes whose skills carry the least credited
evidence; one that would need more than 12 stops at 12. Skills the cover cannot reach are recorded
with the reason, gated or no published archetype or over the cap, never skipped silently.
"""
import json

from sqlalchemy import select

from app.assessment import service as assessment
from app.assessment.shape import PartShape
from app.db import models
from app.engine.fringe import parents_mastered
from app.engine.prior import primary_skill
from app.engine.select import format_for_item
from app.engine.state import Confidence, FadingStage
from app.runtime.bank import PUBLISHED_STATUS, as_served_item
from app.runtime.probe_set import probe_item_ids
from app.session import repository
from app.session import service as session_service

MIN_ITEMS = 8
MAX_ITEMS = 12
UNIT_CHECK_KEY = assessment.UNIT_CHECK_PART_KEY

UNREACHED_GATED = "prerequisites not yet mastered"
UNREACHED_NO_ITEM = "no published item loads it"
UNREACHED_CAP = "over the 12-item cap"


def unit_skills(snapshot, unit_id):
   return sorted(skill_id for skill_id, record in snapshot.skills.items() if record.get("unit") == unit_id)


def published_by_archetype(db):
   withheld = probe_item_ids()
   rows = db.scalars(select(models.Item).where(models.Item.status == PUBLISHED_STATUS)).all()
   grouped = {}

   for row in rows:
      if row.id in withheld or not row.options:
         continue

      grouped.setdefault(row.archetype_id, []).append(row)

   return grouped


def plan_check(snapshot, graph, states, unit_id, published):
   """Returns (chosen archetype ids in cover order, covered skills, unreached {skill: reason})."""
   targets = set(unit_skills(snapshot, unit_id))
   unit_archetypes = [
      record
      for record in graph.archetypes.values()
      if record.get("primary_unit") == unit_id
   ]
   servable = []
   gated_skills = set()

   for record in unit_archetypes:
      has_item = record["id"] in published
      is_clear = parents_mastered(primary_skill(record), states, graph)

      if has_item and is_clear:
         servable.append(record)
      elif has_item:
         gated_skills.update(record["skills"])

   reachable = targets & {skill_id for record in servable for skill_id in record["skills"]}
   uncovered = set(reachable)
   chosen = []
   remaining = sorted(servable, key=lambda record: record["id"])

   while uncovered and remaining and len(chosen) < MAX_ITEMS:
      best = max(remaining, key=lambda record: (len(uncovered & set(record["skills"])), -remaining.index(record)))
      gain = uncovered & set(best["skills"])

      if not gain:
         break

      chosen.append(best)
      remaining.remove(best)
      uncovered -= gain

   def evidence(record):
      counts = [
         states[skill_id].c + states[skill_id].f if skill_id in states else 0.0
         for skill_id in record["skills"]
      ]

      return min(counts) if counts else 0.0

   remaining.sort(key=lambda record: (evidence(record), record["id"]))

   while len(chosen) < MIN_ITEMS and remaining:
      chosen.append(remaining.pop(0))

   covered = targets & {skill_id for record in chosen for skill_id in record["skills"]}
   unreached = {}

   for skill_id in sorted(targets - covered):
      if skill_id in uncovered:
         unreached[skill_id] = UNREACHED_CAP
      elif skill_id in gated_skills:
         unreached[skill_id] = UNREACHED_GATED
      else:
         unreached[skill_id] = UNREACHED_NO_ITEM

   return [record["id"] for record in chosen], sorted(covered), unreached


def pick_item(rows, seen):
   return sorted(rows, key=lambda row: (seen.get(row.id, 0), row.id))[0]


def untimed_shape(count):
   return PartShape(
      key=UNIT_CHECK_KEY,
      section="",
      part="",
      label="Unit check",
      question_type="Unit check",
      questions=count,
      minutes=0,
      calculator_required=False,
      weighting=0.0,
   )


def open_unit_check(db, user_id, context, unit_id, snapshot_id, now):
   states = repository.load_states(db, user_id)
   published = published_by_archetype(db)
   chosen, covered, unreached = plan_check(context.snapshot, context.graph, states, unit_id, published)

   if not chosen:
      raise assessment.AssessmentRefused(f"no archetype of {unit_id} can be served yet")

   history = repository.load_attempts_history(db, user_id)
   seen = {}

   for entry in history:
      seen[entry["item_id"]] = seen.get(entry["item_id"], 0) + 1

   session_row = models.Session(
      id=assessment.new_id("SES"),
      user_id=user_id,
      mode=assessment.UNIT_CHECK,
      sub_mode=unit_id,
      started_at=assessment.stamp(now),
      ended_at=None,
      queue="{}",
      updates_mastery=1,
      snapshot_id=snapshot_id,
      created_at=assessment.stamp(now),
      updated_at=assessment.stamp(now),
   )
   db.add(session_row)
   part = assessment.new_part_row(user_id, session_row.id, 1, untimed_shape(len(chosen)), now, timed=False)
   part.started_at = assessment.stamp(now)
   db.add(part)
   item_ids = []

   for number, archetype_id in enumerate(chosen, start=1):
      row = pick_item(published[archetype_id], seen)
      served = as_served_item(row)
      served_format = format_for_item(history, served, FadingStage.UNSUPPORTED).value
      db.add(assessment.new_response_row(user_id, session_row.id, part.id, number, row.id, served_format, served_format, now))
      item_ids.append(row.id)

   session_row.queue = json.dumps({
      "kind": assessment.UNIT_CHECK,
      "unit_id": unit_id,
      "items": item_ids,
      "frq": [],
      "coverage": {"covered": covered, "unreached": unreached},
   })
   db.flush()

   return session_row


def submit_unit_check(db, context, session_row, now, today=None):
   """Grades every answered item, then applies each observation with the student's rating, and
   reports what moved per skill."""
   part = assessment.part_at(db, session_row, 1)
   is_closed = assessment.part_status(part) == assessment.CLOSED

   if is_closed:
      raise assessment.AssessmentRefused("this unit check was already submitted")

   before = {skill_id: state_summary(state) for skill_id, state in repository.load_states(db, session_row.user_id).items()}
   assessment.close_part(db, context, session_row, part, assessment.CLOSED_BY_SUBMISSION, now)
   day = today or now.date()

   for response in assessment.responses_of(db, part.id):
      has_attempt = response.attempt_id is not None

      if not has_attempt:
         continue

      attempt = db.get(models.Attempt, response.attempt_id)
      is_graded = attempt.correct is not None

      if not is_graded:
         continue

      archetype = context.archetypes[db.get(models.Item, attempt.item_id).archetype_id]
      rating = Confidence(response.confidence) if response.confidence else Confidence.UNSURE
      attempt.confidence = rating.value
      attempt.confidence_source = session_service.CONFIDENCE_FROM_STUDENT if response.confidence else session_service.CONFIDENCE_FROM_SESSION_CLOSE
      session_service.apply_attempt(db, session_row, attempt, archetype, rating, day, context.engine_graph, now)

   session_row.ended_at = assessment.stamp(now)
   session_row.updated_at = assessment.stamp(now)
   db.flush()
   after = {skill_id: state_summary(state) for skill_id, state in repository.load_states(db, session_row.user_id).items()}

   return breakdown(db, context, session_row, part, before, after)


def state_summary(state):
   return {
      "mastered": bool(state.mastered),
      "credited_successes": round(state.c, 4),
      "credited_failures": round(state.f, 4),
   }


def breakdown(db, context, session_row, part, before, after):
   queue = assessment.queue_of(session_row)
   items = []
   touched = set()

   for response in assessment.responses_of(db, part.id):
      row = db.get(models.Item, response.item_id)
      archetype = context.archetypes[row.archetype_id]
      key_option = next((option["id"] for option in (row.options or []) if option.get("is_key")), None)
      touched.update(archetype["skills"])
      items.append({
         "number": response.number,
         "item_id": response.item_id,
         "archetype_id": row.archetype_id,
         "answered": response.answer is not None,
         "correct": None if response.correct is None else bool(response.correct),
         "answer": json.loads(response.answer) if response.answer else None,
         "key_option_id": key_option,
         "worked_solution": json.loads(row.worked_solution) if row.worked_solution else [],
      })

   moved = []

   for skill_id in sorted(touched):
      was = before.get(skill_id)
      now_state = after.get(skill_id)
      has_changed = was != now_state

      if has_changed:
         moved.append({"skill_id": skill_id, "name": context.snapshot.skills.get(skill_id, {}).get("name", skill_id), "before": was, "after": now_state})

   return {
      "id": session_row.id,
      "unit_id": queue.get("unit_id"),
      "items": items,
      "moved": moved,
      "coverage": queue.get("coverage"),
   }


def available_units(db, context, user_id):
   states = repository.load_states(db, user_id)
   published = published_by_archetype(db)
   units = sorted({record.get("primary_unit") for record in context.graph.archetypes.values() if record.get("primary_unit")})
   rows = []

   for unit_id in units:
      chosen, covered, unreached = plan_check(context.snapshot, context.graph, states, unit_id, published)
      rows.append({
         "unit_id": unit_id,
         "items": len(chosen),
         "covered_skills": len(covered),
         "unit_skills": len(covered) + len(unreached),
         "available": len(chosen) > 0,
      })

   return rows
