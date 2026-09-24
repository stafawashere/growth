"""The mastery map on the progress screen (docs/plan/08-design-brief.md, "Progress" and the
Information architecture's node states).

One node per active BC-SKL, grouped by unit and ordered along the prerequisite graph: a node's
depth is the length of the longest chain of hard prerequisite edges above it among the skills,
so within a unit every skill sits after the skills it is built on. Each node carries one of the
five states 08 names, read off skills_state and the retrievability app/engine/retention.py
derives, never stored:

- gap: the latest observation that assessed the skill named it prerequisite_gap and the skill is
  not mastered. 08's legend reads "prerequisite gap diagnosed below this node".
- fading: mastered, and due under today's retention target, the same is_due the Session assembly
  rule reads, so a fading node is exactly a skill the due queue carries.
- mastered: mastered and not due. This includes the rows seeded mastered at account creation
  (R15), which the node says in words because no attempt demonstrated them.
- in_progress: observed at least once and not mastered.
- not_attempted: never observed.

The map carries no count, percentage or retrievability figure (08, "There are no dashboards", and
the anti-pattern "Percentage-complete bars on the mastery graph"). The only numbers per node are
the day of the last unaided success and the days since it, which 08's fading copy prints.
"""
import json
from functools import lru_cache
from pathlib import Path

from sqlalchemy import select

from app.db import models
from app.engine import constants
from app.engine.fringe import is_due
from app.engine.retention import current_retrievability
from app.engine.state import MasteryState

GAP = "gap"
FADING = "fading"
MASTERED = "mastered"
IN_PROGRESS = "in_progress"
NOT_ATTEMPTED = "not_attempted"

NODE_STATES = (NOT_ATTEMPTED, IN_PROGRESS, MASTERED, FADING, GAP)

DEFAULT_CONTENT_ROOT = Path(__file__).resolve().parent.parent.parent / "data"


@lru_cache(maxsize=4)
def unit_records(content_root):
   curriculum_path = Path(content_root) / "curriculum.json"
   has_curriculum = curriculum_path.exists()

   if not has_curriculum:
      return {}

   curriculum = json.loads(curriculum_path.read_text())

   return {unit["id"]: unit for unit in curriculum.get("units", [])}


def unit_number(unit_id):
   digits = unit_id.rsplit("-", 1)[-1]
   is_numbered = digits.isdigit()

   return int(digits) if is_numbered else 0


def prerequisite_depths(graph):
   skill_ids = set(graph.skills)
   depths = {}

   def depth_of(skill_id, trail=()):
      known = depths.get(skill_id)

      if known is not None:
         return known

      parents = [
         parent
         for parent in graph.hard_parents.get(skill_id, ())
         if parent in skill_ids and parent not in trail
      ]
      depth = 0

      for parent in parents:
         depth = max(depth, depth_of(parent, trail + (skill_id,)) + 1)

      depths[skill_id] = depth

      return depth

   for skill_id in skill_ids:
      depth_of(skill_id)

   return depths


def latest_assessed_states(db, user_id):
   """The per-skill mastery_state of the latest attempt that assessed each skill."""
   rows = db.execute(
      select(models.Attempt.per_skill_states)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .where(models.Session.user_id == user_id)
      .where(models.Attempt.correct.is_not(None))
      .order_by(models.Attempt.submitted_at, models.Attempt.started_at, models.Attempt.id)
   ).scalars()
   latest = {}

   for encoded in rows:
      per_skill = json.loads(encoded or "{}")

      for skill_id, mastery_state in per_skill.items():
         was_assessed = mastery_state != MasteryState.NOT_ATTEMPTED.value

         if was_assessed:
            latest[skill_id] = mastery_state

   return latest


def node_state(skill_id, state, due, latest_assessed):
   has_state = state is not None
   is_mastered = has_state and bool(state.mastered)
   was_gap = latest_assessed.get(skill_id) == MasteryState.PREREQUISITE_GAP.value

   is_open_gap = was_gap and not is_mastered

   if is_open_gap:
      return GAP

   is_fading = is_mastered and due

   if is_fading:
      return FADING

   if is_mastered:
      return MASTERED

   was_observed = has_state and state.observation_count > 0

   if was_observed:
      return IN_PROGRESS

   return NOT_ATTEMPTED


def last_success_day(state):
   has_successes = state is not None and len(state.success_days) > 0

   if not has_successes:
      return None

   return max(state.success_days)


def node_payload(skill_id, record, state, depth, due, latest_assessed, today):
   success_day = last_success_day(state)
   has_success = success_day is not None
   was_seeded = state is not None and bool(state.mastered) and state.observation_count == 0

   return {
      "skill_id": skill_id,
      "name": record.get("name") or skill_id,
      "state": node_state(skill_id, state, due, latest_assessed),
      "depth": depth,
      "assumed": was_seeded,
      "last_success_on": success_day.isoformat() if has_success else None,
      "days_since_success": (today - success_day).days if has_success else None,
   }


def unit_payload(unit_id, unit, nodes):
   return {
      "unit_id": unit_id,
      "number": unit_number(unit_id),
      "name": unit.get("name") or unit_id,
      "nodes": sorted(nodes, key=lambda node: (node["depth"], node["skill_id"])),
   }


def mastery_map(db, user_id, states, graph, today, content_root=None):
   units = unit_records(str(content_root or DEFAULT_CONTENT_ROOT))
   retrievability = current_retrievability(states, today)
   target = constants.desired_retention(today)
   latest_assessed = latest_assessed_states(db, user_id)
   depths = prerequisite_depths(graph)
   by_unit = {}

   for skill_id, record in graph.skills.items():
      unit_id = record.get("unit") or "BC-UNIT-00"
      state = states.get(skill_id)
      due = state is not None and is_due(skill_id, states, retrievability, target)
      node = node_payload(skill_id, record, state, depths[skill_id], due, latest_assessed, today)
      by_unit.setdefault(unit_id, []).append(node)

   payload_units = [
      unit_payload(unit_id, units.get(unit_id, {}), by_unit[unit_id])
      for unit_id in sorted(by_unit, key=unit_number)
   ]

   return {
      "today": today.isoformat(),
      "states": list(NODE_STATES),
      "units": payload_units,
   }
