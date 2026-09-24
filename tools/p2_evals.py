"""Run the three P2 evaluations at the recorded size and write docs/operator/p2-evals.md.

   .venv/bin/python tools/p2_evals.py

The suite runs the same functions small (tests/eval/test_p2_evals.py); this is the record the P7
gate on the five-term score reads. The run is deterministic from app/sim/p2_evals.py SEED_BASE.
"""
import sys
from datetime import date
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPOSITORY_ROOT))

from app.sim import p2_evals  # noqa: E402

RECORD_PATH = REPOSITORY_ROOT / "docs" / "operator" / "p2-evals.md"

DIAGNOSTIC_STUDENTS = 400
ARM_STUDENTS = 25
ARM_DAYS = 40


def arm_row(result):
   return (
      f"| {result.arm} | {result.sessions} | {result.items} | {result.declared_mastered} | "
      f"{result.truly_mastered} | {result.true_mastery_per_item:.4f} | {result.mean_predicted:.4f} | "
      f"{result.observed_rate:.4f} | {result.measurement_bias:+.4f} |"
   )


ARM_HEADER = (
   "| Arm | Sessions | Items | Declared mastered | Truly mastered | True mastered per item | "
   "Mean predicted p_A | Observed success | Bias |\n"
   "|---|---|---|---|---|---|---|---|---|"
)


def render(information, policy, control, two_term, five):
   placed_wrong = information.placed_skills - information.placed_skills_truly_known
   settles = information.mean_movement_after_item_10 < information.mean_movement_items_1_to_10
   shape = (
      "Measures after item 10 move less than before it, the ALEKS-observed shape 11 asks for."
      if settles
      else "Measures after item 10 do not move less than before it, so the ALEKS shape 11 asks for is not reproduced."
   )
   rises_dominate = information.early_stops_after_an_entropy_rise * 2 > information.early_stops
   stop_reading = (
      "so most early stops follow an answer the posterior did not expect rather than a posterior that settled"
      if rises_dominate
      else "and most early stops come from a posterior that settled"
   )
   calibration_gap = information.held_out_mean_predicted - information.held_out_observed_rate
   calibration = "over-predicts" if calibration_gap > 0 else "under-predicts"
   five_wins = five.true_mastery_per_item > two_term.true_mastery_per_item
   verdict = (
      "On this world the five-term score finds more truly mastered skills per item than the two-term score."
      if five_wins
      else "On this world the five-term score does not beat the two-term score on truly mastered skills per item."
   )

   return f"""---
title: P2 evaluation record
research_date: {date.today().isoformat()}
status: recorded
purpose: The measured results of eval_diagnostic_information, eval_selection_bias_control and eval_two_term_against_five_term at the recorded size, for the P7 gate on the five-term score.
---

# P2 evaluation record

Written by `tools/p2_evals.py` from `app/sim/p2_evals.py`, seed base {p2_evals.SEED_BASE}. Every
number is a simulation over synthetic students on the whole 541-skill graph with a synthetic bank
of 3 verified items per active archetype (`app/sim/whole_graph.py`). None is a human's measurement
and none is a real student's. The simulated world does not learn: a student's hidden knowledge is
fixed for the run and forgetting follows the P1 runner's half-life curve, so "truly mastered"
counts how many skills the engine declared mastered that the student really knew, which measures
how fast each policy finds what is known rather than how fast it teaches.

## Diagnostic information

{information.students} synthetic students, each one diagnostic from a fresh account.

- Mean posterior movement per item (total variation summed over units): {information.mean_movement_items_1_to_10:.4f} over items 1 to 10, {information.mean_movement_after_item_10:.4f} after item 10. {shape}
- Runs stopping early on the entropy rule: {information.early_stops} of {information.students} ({information.early_stop_share:.1%}). Longest run {information.longest_run} items, median {information.median_run}.
- Of the {information.early_stops} early stops, {information.early_stops_after_an_entropy_rise} came in a 3-item window where one answer raised the summed unit entropy. The plan's rule reads a rise as entropy that stopped falling, {stop_reading}. The error direction is conservative (the unit is left unresolved and its skills are fast-tracked), and the rule is a named tunable in 02 for the held-out agreement to settle.
- Held-out extra problem: {information.held_out_count} asked, mean predicted raw probability {information.held_out_mean_predicted:.4f}, observed success rate {information.held_out_observed_rate:.4f}. The model {calibration} on this population by {abs(calibration_gap):.4f}.
- Placement: {information.placed_skills} skills marked mastered from the unit posterior, {information.placed_skills_truly_known} truly known, {placed_wrong} not known ({placed_wrong / max(information.placed_skills, 1):.1%}). Each wrongly placed skill comes back as a review within days and a credited failure un-masters it.

## Selection bias control

{ARM_STUDENTS} students, a diagnostic each, then {ARM_DAYS} daily sessions per arm, same students and seeds in both arms. The control arm holds retrievability at 1.0, which empties the due set, so every choice is the uniform draw inside the gated fringe (10, arm 2). Bias is mean predicted p_A_knowledge minus observed success over served items.

{ARM_HEADER}
{arm_row(policy)}
{arm_row(control)}

## Two-term against five-term

Same students, seeds and days. The five-term arm replaces block 2's ordering with the deferred score of 02 (`app/sim/five_term.py`); blocks 1 and 3 and every hard constraint are unchanged. The live policy stays two-term: nothing in `app/engine` or `app/session` imports the five-term module (R4).

{ARM_HEADER}
{arm_row(two_term)}
{arm_row(five)}

{verdict} This is evidence for the P7 gate, which turns the five-term score on only when a simulation shows it beating the two-term score on true mastery per item. It is recorded here and changes nothing in P2.
"""


def main():
   information = p2_evals.diagnostic_information(DIAGNOSTIC_STUDENTS)
   policy, control = p2_evals.selection_bias_control(ARM_STUDENTS, ARM_DAYS)
   two_term, five = p2_evals.two_term_against_five_term(ARM_STUDENTS, ARM_DAYS)
   RECORD_PATH.write_text(render(information, policy, control, two_term, five))
   print(f"wrote {RECORD_PATH.relative_to(REPOSITORY_ROOT)}")


if __name__ == "__main__":
   main()
