"""One skill behind a node of the mastery map: its state, what mastering it means in the student's
terms, and the skills and non-calculus prerequisites it is built on, each with its own state where
it is a skill. The words come from the skill record in the content snapshot (adaptive.mastered_if
and adaptive.partially_mastered_if, description_plain), and the states from the same node rule the
map uses, so the detail and the node can never disagree.
"""
from app.engine import constants
from app.engine.fringe import is_due
from app.engine.retention import current_retrievability
from app.lessons.repository import servable_map
from app.progress.mastery import latest_assessed_states, node_payload, node_state

HARD = "hard"
SUPPORTING = "supporting"


def named(record_id, graph, prerequisite_records):
   skill = graph.skills.get(record_id)

   if skill is not None:
      return skill.get("name") or record_id

   prerequisite = prerequisite_records.get(record_id) or {}

   return prerequisite.get("name") or record_id


def parent_entries(skill_id, graph, prerequisite_records, states, retrievability, target, latest_assessed):
   kinds = ((HARD, graph.hard_parents.get(skill_id, ())), (SUPPORTING, graph.supporting_parents.get(skill_id, ())))
   entries = []

   for kind, parents in kinds:
      for parent_id in sorted(parents):
         is_skill = parent_id in graph.skills
         state = states.get(parent_id)
         due = is_skill and state is not None and is_due(parent_id, states, retrievability, target)
         parent_state = node_state(parent_id, state, due, latest_assessed) if is_skill else None

         entries.append({"id": parent_id, "name": named(parent_id, graph, prerequisite_records), "kind": kind, "state": parent_state})

   return entries


def skill_detail(db, user_id, states, graph, snapshot, today, skill_id):
   record = graph.skills.get(skill_id)
   is_unknown = record is None

   if is_unknown:
      return None

   retrievability = current_retrievability(states, today)
   target = constants.desired_retention(today)
   latest_assessed = latest_assessed_states(db, user_id)
   state = states.get(skill_id)
   due = state is not None and is_due(skill_id, states, retrievability, target)
   node = node_payload(skill_id, record, state, 0, due, latest_assessed, today)
   prerequisite_records = getattr(snapshot, "prerequisites", None) or {}
   adaptive = record.get("adaptive") or {}
   concept_id = record.get("concept")
   lesson = servable_map(db).get(concept_id) if concept_id is not None else None

   return {
      "skill_id": skill_id,
      "name": node["name"],
      "unit_id": record.get("unit"),
      "state": node["state"],
      "assumed": node["assumed"],
      "last_success_on": node["last_success_on"],
      "days_since_success": node["days_since_success"],
      "description": record.get("description_plain"),
      "mastered_if": adaptive.get("mastered_if"),
      "partially_mastered_if": adaptive.get("partially_mastered_if"),
      "prerequisites": parent_entries(skill_id, graph, prerequisite_records, states, retrievability, target, latest_assessed),
      "concept_id": concept_id,
      "lesson_id": lesson[0] if lesson is not None else None,
   }
