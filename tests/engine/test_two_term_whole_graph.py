"""P2 scope items 2 and 5: two-term selection over the whole graph, and the exam-weight quota."""
import math
import random
from collections import Counter
from datetime import timedelta
from fractions import Fraction

import pytest

import app.engine.select as select_module
from app.engine import exam_weights
from app.engine.fringe import candidates, due_coverage, outer_fringe
from app.engine.retention import current_retrievability
from app.engine.select import next_item_learning
from app.sim import five_term, whole_graph

TODAY = whole_graph.START_DAY


@pytest.fixture(scope="module")
def library():
   return whole_graph.library()


def placed_states(library, seed):
   bank = whole_graph.synthetic_bank(library.graph)
   student = whole_graph.make_student(f"placed-{seed}", random.Random(seed))

   return whole_graph.run_diagnostic(student, bank, seed=seed).states, bank


def test_two_term_selection_whole_graph(library):
   graph = library.graph
   units_chosen = set()
   checked = 0

   for seed in range(30):
      states, bank = placed_states(library, 900 + seed)
      later = TODAY + timedelta(days=12)
      retrievability = current_retrievability(states, later)
      available, _ = candidates(outer_fringe(states, graph), graph, bank)
      covers = {record["id"]: due_coverage(record, states, graph, later, retrievability) for record in available}
      best = max(covers.values())
      selection = next_item_learning(
         states, graph, bank, [], [], random.Random(seed), later, retrievability=retrievability
      )
      chosen = selection.item["archetype_id"]

      assert covers[chosen] == best
      units_chosen.add(graph.primary_unit(chosen))
      checked += 1

   assert checked == 30
   assert len(units_chosen) > 3


def test_ties_resolve_uniformly_inside_the_fringe(library):
   graph = library.graph
   states = whole_graph.fresh_states()
   bank = whole_graph.synthetic_bank(graph)
   available, _ = candidates(outer_fringe(states, graph), graph, bank)
   draws = Counter()
   rounds = 60 * len(available)
   rng = random.Random(4)

   for _ in range(rounds):
      selection = next_item_learning(states, graph, bank, [], [], rng, TODAY)
      draws[selection.item["archetype_id"]] += 1

   expected = rounds / len(available)
   chi_square = sum((draws[record["id"]] - expected) ** 2 / expected for record in available)
   degrees = len(available) - 1

   assert set(draws) == {record["id"] for record in available}
   assert chi_square < degrees + 4 * (2 * degrees) ** 0.5


def test_no_five_term_weight_reaches_the_live_selection(library, monkeypatch):
   graph = library.graph
   states, bank = placed_states(library, 77)
   later = TODAY + timedelta(days=12)

   def draw():
      return [
         next_item_learning(states, graph, bank, [], [], random.Random(seed), later).item["id"]
         for seed in range(20)
      ]

   baseline = draw()

   for name in ("W_LEARN", "W_DUE", "W_COV", "W_WEIGHT", "W_REP", "EXPLORE_SHARE"):
      monkeypatch.setattr(five_term, name, 1000.0)

   assert draw() == baseline


def test_blueprint_bands_are_the_bc_column_of_the_blueprint_table():
   blueprint = exam_weights.BLUEPRINT_PATH.read_text()
   rows = [line for line in blueprint.splitlines() if line.startswith("| BC-UNIT-")]
   expected = {}

   for row in rows:
      cells = [cell.strip() for cell in row.strip("|").split("|")]
      low, high = cells[-1].rstrip("%").split(" to ")
      expected[cells[0]] = (int(low), int(high))

   assert exam_weights.bc_bands() == expected
   assert len(expected) == 10


def test_exam_weight_quota_never_empties_and_never_lets_a_unit_pass_its_ceiling(library):
   graph = library.graph
   records = sorted(graph.archetypes.values(), key=lambda record: record["id"])
   midpoints = exam_weights.band_midpoints()
   rng = random.Random(11)

   for _ in range(2000):
      sample = rng.sample(records, rng.randint(1, 12))
      counts = {unit: rng.randint(0, 6) for unit in midpoints}
      allowed = exam_weights.filter_exam_weight(sample, counts)
      open_units = sorted({record["primary_unit"] for record in sample})
      open_total = sum(Fraction(midpoints[unit]) for unit in open_units)
      counted = sum(counts.values())

      assert allowed

      for record in sample:
         unit = record["primary_unit"]
         share = Fraction(midpoints[unit]) / open_total
         within_quota = counts[unit] < math.ceil(share * (counted + 1))

         assert (record in allowed) == within_quota


def heavy_share(library, monkeypatch, quota_on):
   if not quota_on:
      monkeypatch.setattr(select_module, "filter_exam_weight", lambda records, unit_counts: list(records))

   graph = library.graph
   bank = whole_graph.synthetic_bank(graph)
   served = Counter()

   for index in range(8):
      student = whole_graph.make_student(f"weight-{index}", random.Random(1200 + index))
      history, _, _, _ = whole_graph.run_days(student, bank, seed=1200 + index, days=15)

      for day_record in history:
         for block in (day_record.session.block2, day_record.session.block3):
            for item in block:
               served[graph.primary_unit(item["archetype_id"])] += 1

   heavy = sum(served[unit] for unit in ("BC-UNIT-05", "BC-UNIT-06", "BC-UNIT-09", "BC-UNIT-10"))

   return heavy / sum(served.values())


def test_exam_weight_quota_tilts_blocks_two_and_three_toward_the_heavy_units(library, monkeypatch):
   with_quota = heavy_share(library, monkeypatch, quota_on=True)
   without_quota = heavy_share(library, monkeypatch, quota_on=False)

   assert with_quota > without_quota
