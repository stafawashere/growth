"""Candidate selection policies for the Today redesign, for simulation only.

docs/operator/selection-study.md found that two-term's due coverage speaks on 1.1 to 7.5 percent
of block 2 choices, so two-term nearly is the random control, and that the forgetting oracle, which
serves the candidate reaching the truly least-retained known skill, is far ahead on delayed mastery
per item and on retention at day 30. The policies here are what the engine could do with what it
can see. Nothing in app/engine or app/session imports this module; each policy reaches selection
only through the ordering hooks. Retrievability priority lives in app/engine/priority.py, which the
running app also orders with under the selection_priority switch, so both run one implementation.

Readings fixed here: the Elo item logit is the negated mean beta of the loaded skills, since beta
enters strength with a plus sign and so is an easiness; spread reads the hook's history, which is the current session's served items, blocks 1
and 2.
"""
import math

from app.engine.priority import retrievability_need, retrievability_priority_ordering, seeded_pool
from app.sim import learning

ELO_K = 0.4
TARGET_RAW = 0.75
SPREAD_SKILL_WINDOW = 5
SPREAD_UNIT_WINDOW = 3
SPREAD_FAMILY_WINDOW = 10


def sigmoid(logit):
   return 1.0 / (1.0 + math.exp(-logit))


def item_logit(record, states):
   betas = [states[skill_id].beta for skill_id in record["skills"] if skill_id in states]
   has_betas = len(betas) > 0

   if not has_betas:
      return 0.0

   return -sum(betas) / len(betas)


class EloTarget:
   """A running rating per archetype family, started at 0 logits for each student."""

   def __init__(self, k=ELO_K, target=TARGET_RAW):
      self.k = k
      self.target = target
      self.ratings = {}
      self.states = None

   def expected_success(self, record, states):
      rating = self.ratings.get(record["family"], 0.0)

      return sigmoid(rating - item_logit(record, states))

   def observe(self, record, is_correct, today):
      has_seen_states = self.states is not None

      if not has_seen_states:
         return

      expected = self.expected_success(record, self.states)
      outcome = 1.0 if is_correct else 0.0
      family = record["family"]
      self.ratings[family] = self.ratings.get(family, 0.0) + self.k * (outcome - expected)

   def ordering(self, records, states, graph, today, retrievability, rng, history):
      self.states = states
      pool = seeded_pool(records, rng)

      def key(record):
         distance = abs(self.expected_success(record, states) - self.target)
         priority = retrievability_need(record, states, graph, retrievability)

         return (distance, -priority)

      return sorted(pool, key=key)


def served_recently(history, count, read):
   return {read(item) for item in history[-count:]}


def spread_ordering(records, states, graph, today, retrievability, rng, history):
   """Candidates whose skill, unit and family were not served lately first."""
   pool = seeded_pool(records, rng)
   recent_skills = served_recently(
      history, SPREAD_SKILL_WINDOW, lambda item: graph.primary_skill(item["archetype_id"])
   )
   recent_units = served_recently(
      history, SPREAD_UNIT_WINDOW, lambda item: graph.primary_unit(item["archetype_id"])
   )
   recent_families = served_recently(
      history, SPREAD_FAMILY_WINDOW, lambda item: graph.family(item["archetype_id"])
   )

   def spread(record):
      score = 0
      skill_is_fresh = record["skills"][0] not in recent_skills
      unit_is_fresh = record["primary_unit"] not in recent_units
      family_is_fresh = record["family"] not in recent_families

      if skill_is_fresh:
         score += 2

      if unit_is_fresh:
         score += 1

      if family_is_fresh:
         score += 1

      return score

   def key(record):
      priority = retrievability_need(record, states, graph, retrievability)

      return (-spread(record), -priority)

   return sorted(pool, key=key)


TODAY_ARMS = {
   "retrievability_priority": learning.Arm(
      "retrievability_priority", ordering=retrievability_priority_ordering
   ),
   "retrievability_priority_both": learning.Arm(
      "retrievability_priority_both",
      ordering=retrievability_priority_ordering,
      retrieval_ordering=retrievability_priority_ordering,
   ),
   "elo_target": learning.Arm("elo_target", learner=EloTarget),
   "spread": learning.Arm("spread", ordering=spread_ordering),
   "review_first": learning.Arm("review_first", retrieval_ordering=retrievability_priority_ordering),
}
