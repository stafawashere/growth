"""Declared difficulty prior and item-level prediction (docs/plan/02, Calibration plan and the
conjunctive and compensatory split). Works on plain dicts so it needs no loader.

archetypes: dict of archetype id to a record with at least "skills" (list, first entry is the
primary skill per R25) and "difficulty_factors" (list of BC-DF ids).
hard_parents: dict of skill id to the set of its hard_prerequisite parents.
"""
from collections import deque

from app.engine import constants
from app.engine.strength import probability, sigmoid, strength


def primary_skill(archetype):
   return archetype["skills"][0]


def beta_for_skill(skill_id, archetypes):
   """beta_k = -0.35 * (mean BC-DF count over the archetypes that list k - 2), R25 set."""
   counts = [
      len(record["difficulty_factors"])
      for record in archetypes.values()
      if skill_id in record["skills"]
   ]
   has_no_archetype = len(counts) == 0

   if has_no_archetype:
      return 0.0

   mean_count = sum(counts) / len(counts)

   return constants.BETA_PER_FACTOR * (mean_count - constants.BETA_CENTRE_FACTOR_COUNT)


def hard_ancestors(skill_id, hard_parents, max_hops=None):
   """Every skill reachable upward over hard_prerequisite edges, with its shortest hop count."""
   found = {}
   frontier = deque([(skill_id, 0)])

   while frontier:
      current, hops = frontier.popleft()
      next_hops = hops + 1
      past_limit = max_hops is not None and next_hops > max_hops

      if past_limit:
         continue

      for parent in hard_parents.get(current, ()):
         is_new = parent not in found

         if is_new:
            found[parent] = next_hops
            frontier.append((parent, next_hops))

   return found


def split_skills(archetype, hard_parents):
   """K_hard is every loaded skill that is a hard ancestor of the primary skill.

   The primary skill itself sits in K_soft. This is the reading under which the plan's recorded
   cold-start pre-computation (p10 0.250, p50 0.456, p90 0.587) reproduces; the pseudocode line
   that also put the primary skill in K_hard gives p90 0.344 and is withdrawn in BUILD-LEDGER.md.
   """
   primary = primary_skill(archetype)
   ancestors = hard_ancestors(primary, hard_parents)
   hard = [skill for skill in archetype["skills"] if skill in ancestors]
   soft = [skill for skill in archetype["skills"] if skill not in hard]

   return hard, soft


def p_knowledge(archetype, states, hard_parents, retrievability=None):
   """Conjunctive product over K_hard times sigmoid of the mean logit over K_soft."""
   hard, soft = split_skills(archetype, hard_parents)

   def retention_of(skill):
      has_override = retrievability is not None and skill in retrievability

      if has_override:
         return retrievability[skill]

      return 1.0

   p_hard = 1.0

   for skill in hard:
      p_hard *= probability(states[skill], retention_of(skill))

   has_soft = len(soft) > 0

   if has_soft:
      mean_logit = sum(strength(states[skill], retention_of(skill)) for skill in soft) / len(soft)
      p_soft = sigmoid(mean_logit)
   else:
      p_soft = 1.0

   return p_hard * p_soft


def p_compensatory(archetype, states, retrievability=None):
   """The pure compensatory counterfactual that invariant 23 requires on every observation."""
   skills = archetype["skills"]

   def retention_of(skill):
      has_override = retrievability is not None and skill in retrievability

      if has_override:
         return retrievability[skill]

      return 1.0

   mean_logit = sum(strength(states[skill], retention_of(skill)) for skill in skills) / len(skills)

   return sigmoid(mean_logit)


def p_raw(archetype, states, hard_parents, response_format, retrievability=None):
   knowledge = p_knowledge(archetype, states, hard_parents, retrievability)
   is_mcq = response_format == "mcq"

   if is_mcq:
      return constants.MCQ_GUESS_FLOOR + constants.MCQ_SUCCESS_CREDIT * knowledge

   return knowledge
