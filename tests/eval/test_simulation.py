"""Offline simulation gate 31 and its two supporting tests.

docs/plan/11-phased-delivery.md gate 31 names eval_simulation_mastery_growth: over the 6 synthetic
trajectories, mastery per item served under the shipped two-term policy exceeds a random-within-
fringe control arm run as a separate simulation over the same fixtures and the same seeds. The
world model is in app/sim/runner.py and is deliberately not FSRS, per
docs/plan/10-quality-and-evaluation.md, "Forgetting".
"""
from app.engine.prior import hard_ancestors
from app.sim.runner import (
   TRAJECTORY_NAMES,
   load_trajectory,
   run_simulation,
   seed_for,
   simulation_graph,
)

GAP_SKILL = "BC-SKL-02025"


def test_simulation_reproducible_from_seed():
   trajectory = load_trajectory("slipper")

   first = run_simulation(trajectory, seed=7)
   second = run_simulation(trajectory, seed=7)

   assert len(first.trace) > 0
   assert first.trace == second.trace

   other = run_simulation(trajectory, seed=8)

   assert other.trace != first.trace


def test_simulation_prereq_gap_stalls_dependants():
   """The seeded gap is read for gating, not for attribution (gate 31's own note).

   P1 never emits prerequisite_gap, so what the trajectory exercises is that nothing above an
   open hard prerequisite is ever served. The trace carries the engine's mastered verdict on the
   served item's hard ancestors at the moment it was served, so the claim is checked per serve
   rather than off the end state.
   """
   trajectory = load_trajectory("prereq_gap_02025")
   result = run_simulation(trajectory, seed=seed_for("prereq_gap_02025"))
   graph, engine_graph = simulation_graph()
   gap_state = result.states[GAP_SKILL]

   assert gap_state.observation_count > 0
   assert gap_state.mastered is False

   dependants = [
      skill_id
      for skill_id in graph.skills
      if GAP_SKILL in hard_ancestors(skill_id, engine_graph.hard_parents)
   ]

   assert len(dependants) > 0

   for skill_id in dependants:
      state = result.states[skill_id]

      if not state.mastered:
         continue

      crediting_primaries = {
         graph.primary_skill(archetype_id) for archetype_id in state.distinct_archetypes_succeeded
      }

      assert crediting_primaries.isdisjoint(set(dependants))

   served_primaries = {record["primary_skill"] for record in result.trace}
   blocked = [record for record in result.trace if record["unmastered_hard_ancestors"]]

   assert len(result.trace) > 0
   assert blocked == []
   assert served_primaries.isdisjoint(set(dependants))


def test_simulation_records_both_predictions():
   trajectory = load_trajectory("ceiling")
   result = run_simulation(trajectory, seed=3)

   assert len(result.trace) > 0

   for record in result.trace:
      assert record["p_split"] is not None
      assert record["p_compensatory"] is not None
      assert 0.0 <= record["p_split"] <= 1.0
      assert 0.0 <= record["p_compensatory"] <= 1.0


def eval_simulation_mastery_growth(capsys):
   policy_mastered = 0
   policy_items = 0
   control_mastered = 0
   control_items = 0
   rows = []

   for name in TRAJECTORY_NAMES:
      trajectory = load_trajectory(name)
      seed = seed_for(name)
      policy = run_simulation(trajectory, seed=seed, arm="policy")
      control = run_simulation(trajectory, seed=seed, arm="control")

      policy_mastered += policy.declared_mastered
      policy_items += policy.items_served
      control_mastered += control.declared_mastered
      control_items += control.items_served

      rows.append((name, policy, control))

      carries_predictions = all(
         record["p_split"] is not None and record["p_compensatory"] is not None
         for result in (policy, control)
         for record in result.trace
      )

      assert carries_predictions

   with capsys.disabled():
      report(rows, policy_mastered, policy_items, control_mastered, control_items)

   assert policy_items > 0
   assert control_items > 0
   assert policy_mastered / policy_items > control_mastered / control_items


def report(rows, policy_mastered, policy_items, control_mastered, control_items):
   print("")
   print("eval_simulation_mastery_growth, 30 simulated days per trajectory")
   print(
      f"{'trajectory':<20}{'arm':<9}{'items':>7}{'declared':>10}"
      f"{'per item':>10}{'true ok':>9}{'true/item':>11}{'corrob':>9}{'corrob/item':>13}"
   )

   for name, policy, control in rows:
      for arm, result in (("policy", policy), ("control", control)):
         print(
            f"{name:<20}{arm:<9}{result.items_served:>7}{result.declared_mastered:>10}"
            f"{result.mastery_per_item:>10.4f}{result.true_declared_mastered:>9}"
            f"{result.true_mastery_per_item:>11.4f}{result.corroborated:>9}"
            f"{result.corroborated_per_item:>13.4f}"
         )

   policy_rate = policy_mastered / policy_items
   control_rate = control_mastered / control_items

   print(f"pooled policy  {policy_mastered} mastered over {policy_items} items = {policy_rate:.4f}")
   print(f"pooled control {control_mastered} mastered over {control_items} items = {control_rate:.4f}")
