"""Retrievability priority, the candidate order of docs/pedagogy/today/design.md D1.

A candidate's need is the sum of 1 - R_k over the skills it reaches, its loaded skills and their
1-hop gating parents, each counted once. A skill counts only once it has a memory (stability set),
because R_k is 1 by definition before that. Candidates are ordered by need, highest first, then by
due coverage, then by the seeded uniform draw two-term already uses, so with nothing decayed the
order is two-term's.

The simulator (app/sim/today_policies.py) and the selection_priority switch of
app/experiments/switches.py both order with this one function.
"""
from app.engine.fringe import due_coverage, retrievability_of


def seeded_pool(records, rng):
   pool = sorted(records, key=lambda record: record["id"])
   rng.shuffle(pool)

   return pool


def reached_skills(record, graph):
   """The loaded skills and their 1-hop gating parents, each once, as due coverage reads them."""
   reached = []

   for skill_id in record["skills"]:
      for candidate in [skill_id] + graph.gating_parents(skill_id):
         if candidate not in reached:
            reached.append(candidate)

   return reached


def retrievability_need(record, states, graph, retrievability):
   need = 0.0

   for skill_id in reached_skills(record, graph):
      state = states.get(skill_id)
      has_memory = state is not None and state.stability is not None

      if has_memory:
         need += 1.0 - retrievability_of(skill_id, retrievability)

   return need


def retrievability_priority_ordering(records, states, graph, today, retrievability, rng, history):
   """Most forgotten reach first, then due coverage, then the seeded shuffle."""
   pool = seeded_pool(records, rng)

   def key(record):
      need = retrievability_need(record, states, graph, retrievability)
      cover = due_coverage(record, states, graph, today, retrievability)

      return (-need, -cover)

   return sorted(pool, key=key)
