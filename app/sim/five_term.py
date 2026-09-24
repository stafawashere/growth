"""The deferred five-term learning score of docs/plan/02 ("Deferred until P7 shows it beats the
two-term score"), for simulation only.

Nothing in app/engine or app/session imports this module, so the live policy cannot read these
weights (R4). eval_two_term_against_five_term runs it through app/sim/whole_graph.py as a block 2
ordering and records the comparison for the P7 gate.

Readings the plan leaves open, fixed here: normalise(due_coverage) divides by the largest cover
among the candidates in hand (0 when nothing is due); exam_weight is the unit's band midpoint over
the sum of all ten midpoints; representation_gap is the share of the archetype's BC-REP ids that
are among the least-served representations of the student's history; the coverage tie-break takes,
among candidates within 0.02 of the best score, the one whose least-observed skill has the lowest
count, lowest id on a further tie; EXPLORE_SHARE replaces the scored choice with a uniform draw.
"""
from app.engine import constants
from app.engine.exam_weights import band_midpoints
from app.engine.fringe import due_coverage
from app.engine.prior import p_knowledge

W_LEARN = 0.50
W_DUE = 0.25
W_COV = 0.10
W_WEIGHT = 0.10
W_REP = 0.05
EXPLORE_SHARE = 0.125
TIE_BAND = 0.02


def exam_weight(unit_id):
   midpoints = band_midpoints()
   total = sum(midpoints.values())

   return float(midpoints.get(unit_id, 0) / total)


def min_observations(record, states):
   return min(states[skill_id].observation_count for skill_id in record["skills"])


def representation_gap(record, graph, history):
   seen = {}

   for item in history:
      for representation in graph.archetypes[item["archetype_id"]].get("representations", ()):
         seen[representation] = seen.get(representation, 0) + 1

   carried = list(record.get("representations") or ())
   has_carried = len(carried) > 0

   if not has_carried:
      return 0.0

   counts = [seen.get(representation, 0) for representation in carried]
   fewest = min(counts)
   least_served = [count for count in counts if count == fewest]

   return len(least_served) / len(carried)


def score(record, states, graph, today, retrievability, history, best_cover):
   knowledge = p_knowledge(record, states, graph.hard_parents, retrievability)
   cover = due_coverage(record, states, graph, today, retrievability)
   normalised_cover = cover / best_cover if best_cover > 0 else 0.0

   return (
      W_LEARN * (1.0 - abs(knowledge - constants.TARGET_LEARN))
      + W_DUE * normalised_cover
      + W_COV * (1.0 / (1.0 + min_observations(record, states)))
      + W_WEIGHT * exam_weight(record["primary_unit"])
      + W_REP * representation_gap(record, graph, history)
   )


def five_term_ordering(records, states, graph, today, retrievability, rng, history):
   """The candidates in the order block 2 should try them, best first."""
   pool = sorted(records, key=lambda record: record["id"])
   has_pool = len(pool) > 0

   if not has_pool:
      return []

   explores = rng.random() < EXPLORE_SHARE

   if explores:
      rng.shuffle(pool)

      return pool

   best_cover = max(due_coverage(record, states, graph, today, retrievability) for record in pool)
   scored = [
      (score(record, states, graph, today, retrievability, history, best_cover), record)
      for record in pool
   ]
   best = max(value for value, _ in scored)
   near_best = [record for value, record in scored if value >= best - TIE_BAND]
   rest = [record for value, record in sorted(scored, key=lambda pair: -pair[0]) if record not in near_best]
   near_best.sort(key=lambda record: (min_observations(record, states), record["id"]))

   return near_best + rest
