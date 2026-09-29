"""The Today measurement of app/sim/today_metrics.py counts without changing what is served."""
from app.sim import learning, p7_evals, today_metrics

SEED = p7_evals.SEED_BASE
DAYS = 5


def test_a_measured_run_serves_what_an_unmeasured_run_serves():
   unmeasured = learning.run_student(learning.ARMS["two_term"], SEED, DAYS, keep_trace=True)
   measured = today_metrics.measure_student("two_term", SEED, DAYS, learning.EXPONENTIAL, keep_trace=True)

   assert len(unmeasured.trace) > 0
   assert measured.trace == unmeasured.trace


def test_block2_choices_count_the_block2_items_served(monkeypatch):
   served_in_block2 = []
   original = learning.assemble_session

   def counting(*args, **options):
      session = original(*args, **options)
      served_in_block2.extend(entry for entry in session.block2 if entry.get("kind") == "item")

      return session

   monkeypatch.setattr(learning, "assemble_session", counting)
   metrics = today_metrics.measure_student("two_term", SEED, DAYS, learning.EXPONENTIAL)

   assert len(served_in_block2) > 0
   assert metrics.block2_choices == len(served_in_block2)


def test_every_block2_choice_is_decided_by_exactly_one_rule():
   metrics = today_metrics.measure_student("two_term", SEED, DAYS, learning.EXPONENTIAL)

   assert metrics.block2_choices > 0
   assert sum(metrics.block2_decided_by.values()) == metrics.block2_choices


def test_the_tie_histogram_reads_the_pool_the_shuffle_draws_from():
   metrics = today_metrics.TodayMetrics("hand", 0, 0, learning.EXPONENTIAL, "fixed")
   candidate_covers = [[2, 2, 1], [3, 1], [0, 0, 0], [0]]

   for covers in candidate_covers:
      pool_size, decider = today_metrics.tie_outcome(covers)
      today_metrics.record_choice(metrics, {
         "pool_size": pool_size,
         "decided_by": decider,
         "window_before": len(covers),
         "window_after": len(covers),
         "window_changed_pick": False,
      })

   assert metrics.block2_tie_sizes == {2: 1, 1: 2, 3: 1}
   assert metrics.block2_tied == 2
   assert metrics.block2_decided_by == {"due_coverage": 1, "due_coverage_tie": 1, "random": 2}
