"""The three P2 evals of docs/plan/11 P2, run small. tools/p2_evals.py runs them at the recorded
size and writes docs/operator/p2-evals.md."""
import math
from pathlib import Path

import pytest

from app.engine import constants
from app.sim import p2_evals

DIAGNOSTIC_STUDENTS = 60
ARM_STUDENTS = 6
ARM_DAYS = 20

RECORD_PATH = Path(__file__).resolve().parents[2] / "docs" / "operator" / "p2-evals.md"


def eval_diagnostic_information():
   measured = p2_evals.diagnostic_information(DIAGNOSTIC_STUDENTS)

   assert measured.mean_movement_after_item_10 < measured.mean_movement_items_1_to_10
   assert measured.longest_run <= constants.DIAG_CAP
   assert measured.early_stop_share >= 0.5
   assert measured.held_out_count == DIAGNOSTIC_STUDENTS


@pytest.fixture(scope="module")
def arms():
   policy, control = p2_evals.selection_bias_control(ARM_STUDENTS, ARM_DAYS)
   two_term, five = p2_evals.two_term_against_five_term(ARM_STUDENTS, ARM_DAYS)

   return policy, control, two_term, five


def eval_selection_bias_control(arms):
   policy, control, _, _ = arms

   assert policy.sessions == control.sessions == ARM_STUDENTS * ARM_DAYS
   assert policy.items > 0 and control.items > 0
   assert math.isfinite(policy.measurement_bias) and math.isfinite(control.measurement_bias)
   assert (policy.items, policy.declared_mastered) != (control.items, control.declared_mastered)


def eval_two_term_against_five_term(arms):
   _, _, two_term, five = arms

   assert two_term.sessions == five.sessions == ARM_STUDENTS * ARM_DAYS
   assert (two_term.items, two_term.truly_mastered) != (five.items, five.truly_mastered)
   assert math.isfinite(two_term.true_mastery_per_item) and math.isfinite(five.true_mastery_per_item)


def test_the_p2_evaluation_record_is_written_and_names_all_three_evals():
   record = RECORD_PATH.read_text()

   for heading in ("## Diagnostic information", "## Selection bias control", "## Two-term against five-term"):
      assert heading in record

   assert f"seed base {p2_evals.SEED_BASE}" in record
