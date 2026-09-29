"""The first-contact gate in front of the ladder: docs/plan/15-lessons.md, Engine and session
integration, First-contact target, and Cold start, placement and skipped units.

Every function here is pure. It reads skills_state as the engine holds it and the lesson states as
app/lessons/repository.py loads them (lesson id to state row), and writes nothing, so a lesson
never moves an engine state (15, invariant L0).
"""
import statistics
from dataclasses import dataclass, field

from app.engine import constants as engine_constants
from app.engine.prior import p_knowledge
from app.lessons import constants

LOW = "low"
MID = "mid"
NONE = "none"

UNSEEN = "unseen"
DEFERRED = "deferred"
SERVED = "served"
READ = "read"
SKIPPED = "skipped"
BYPASSED = "bypassed_by_placement"
NOT_YET_READ = (None, UNSEEN, DEFERRED)

MILLISECONDS_PER_MINUTE = 60000


@dataclass
class LessonInputs:
   """What assembly needs to place lessons, loaded by app/session/service.py.

   servable maps a target id (a BC-CON or BC-PRQ id) to its (lesson_id, version); bodies maps a
   lesson id to its stored record; lesson_states maps a lesson id to its state row; completion_ratios
   are read_ms over authored minutes of the user's completed lessons; example_first answers whether
   the lesson_first_contact switch serves a concept example first; refreshers are the targets of
   app/lessons/refresh.py refresher_targets."""

   servable: dict = field(default_factory=dict)
   bodies: dict = field(default_factory=dict)
   lesson_states: dict = field(default_factory=dict)
   completion_ratios: tuple = ()
   example_first: object = None
   refreshers: tuple = ()


def concept_of(graph, skill_id):
   record = graph.skills.get(skill_id)

   if record is None:
      return None

   return record.get("concept")


def status_of(lesson_states, lesson_id):
   state = lesson_states.get(lesson_id)

   if state is None:
      return None

   if isinstance(state, str):
      return state

   return state.get("status")


def lesson_target(item, states, graph, lesson_states, servable):
   """The concept whose lesson goes before this item, or None. Every loaded skill in the
   archetype's skills order, primary first (R25), so a concept reached only as a secondary skill
   still gets its lesson.

   A deferred lesson is a target whatever the skill's observations, because 15 defers it so that
   "the same concept's next item, in this session or the next, gets the lesson first", and the
   deferred item has usually been answered by then."""
   archetype = graph.archetypes[item["archetype_id"]]

   for skill_id in archetype["skills"]:
      concept_id = concept_of(graph, skill_id)
      found = servable.get(concept_id) if concept_id is not None else None
      state = states.get(skill_id)
      has_lesson = found is not None
      has_state = state is not None

      if not has_lesson or not has_state:
         continue

      status = status_of(lesson_states, found[0])
      is_deferred = status == DEFERRED
      is_unobserved = state.credited_observation_count == 0
      is_unseen = status in NOT_YET_READ
      needs_lesson = (is_unobserved and is_unseen) or is_deferred

      if needs_lesson:
         return concept_id

   return None


def lesson_band(archetype, states, graph, retrievability):
   """15 By predicted knowledge: the bands serve_stage already reads (R4, R32)."""
   knowledge = p_knowledge(archetype, states, graph.hard_parents, retrievability)

   if knowledge < engine_constants.STAGE_LOW:
      return LOW

   if knowledge > engine_constants.STAGE_HIGH:
      return NONE

   return MID


def concept_skill_map(graph):
   has_concepts = len(graph.concept_skills) > 0

   if has_concepts:
      return {concept_id: tuple(skills) for concept_id, skills in graph.concept_skills.items()}

   skills_by_concept = {}

   for skill_id in sorted(graph.skills):
      concept_id = concept_of(graph, skill_id)

      if concept_id is not None:
         skills_by_concept.setdefault(concept_id, []).append(skill_id)

   return {concept_id: tuple(skills) for concept_id, skills in skills_by_concept.items()}


def bypass_placed_concepts(states, graph):
   """15 Cold start: every concept all of whose skills are mastered after placement, sorted."""
   bypassed = []

   for concept_id, skills in sorted(concept_skill_map(graph).items()):
      known = [states[skill_id] for skill_id in skills if skill_id in states]
      has_skills = len(known) > 0
      all_mastered = has_skills and all(state.mastered for state in known)

      if all_mastered:
         bypassed.append(concept_id)

   return bypassed


def flipped_prerequisites(archetype, states):
   """The BC-PRQ ids the archetype lists whose seeded mastery a diagnosed gap has flipped (R15, 02
   BC-PRQ handling): a BC-PRQ row is seeded mastered, so an unmastered one was flipped."""
   flipped = []

   for prerequisite_id in archetype.get("prerequisites") or ():
      state = states.get(prerequisite_id)
      is_flipped = state is not None and not state.mastered

      if is_flipped:
         flipped.append(prerequisite_id)

   return flipped


def lesson_forecast(authored_minutes, completion_ratios):
   """15 Forecast: the authored minutes until LESSON_FORECAST_MIN_COMPLETIONS completions, then the
   running median of read time over authored minutes times the authored value."""
   has_enough = len(completion_ratios) >= constants.LESSON_FORECAST_MIN_COMPLETIONS

   if not has_enough:
      return float(authored_minutes)

   return float(authored_minutes) * statistics.median(completion_ratios)
