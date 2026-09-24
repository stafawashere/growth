"""Run the P7 policy comparison at the recorded size and write docs/operator/p7-evals.md.

   .venv/bin/python tools/p7_evals.py [workers]

The suite runs the same functions small (tests/eval/test_p7_evals.py). The run is deterministic
from app/sim/p7_evals.py SEED_BASE: the same seed base, size and code write the same record.
"""
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPOSITORY_ROOT))

from app.sim import learning, p7_evals  # noqa: E402

RECORD_PATH = REPOSITORY_ROOT / "docs" / "operator" / "p7-evals.md"

STUDENTS = 200
DAYS = 60

ARM_HEADER = (
   "| Arm | Items | Skills learned | True mastery per item | Retention day 7 | Retention day 30 | "
   "Bias | Declared | Declared, not known | Placed, not known | Seeded, not known |\n"
   "|---|---|---|---|---|---|---|---|---|---|---|"
)


def arm_row(summary):
   return (
      f"| {summary.arm} | {summary.items} | {summary.learned} | "
      f"{summary.mean_true_mastery_per_item:.5f} | {summary.mean_retention_day_7:.4f} | "
      f"{summary.mean_retention_day_30:.4f} | {summary.mean_measurement_bias:+.4f} | "
      f"{summary.declared_mastered} | {summary.declared_not_known} | "
      f"{summary.placed_not_known} of {summary.placed_mastered} | "
      f"{summary.seeded_not_known} of {summary.seeded_mastered} |"
   )


def yes_no(flag):
   return "yes" if flag else "no"


def decision_lines(decisions, students):
   bar = f"{p7_evals.PAIRED_BAR:.0%}"

   return [
      f"- Two-term against the random-within-fringe control: two-term matched or beat the control on true mastery per item for {decisions.policy_at_least_random_share:.1%} of {students} students. Bar {bar}. Passes: {yes_no(decisions.policy_beats_random)}.",
      f"- Five-term against two-term: five-term beat two-term on true mastery per item for {decisions.five_term_beats_two_term_share:.1%} of {students} students. Bar {bar}. Five-term turned on: {yes_no(decisions.five_term_on)}.",
      f"- Decay term, arm 6 against arm 1: lambda 2.0 beat lambda 0 on true mastery per item for {decisions.lambda_mastery_share:.1%} and on retention at day 30 for {decisions.lambda_retention_share:.1%} of {students} students. Bar {bar} on either. lambda returns to 2.0: {yes_no(decisions.lambda_returns)}.",
      f"- Interleaving removed: mean retention at day 30 moved by {decisions.interleaving_removal_retention_gain:+.4f} against two-term, and was higher without interleaving for {decisions.interleaving_removal_retention_share:.1%} of {students} students. Bar {bar}. The constraint costs retention: {yes_no(decisions.interleaving_costs_retention)}.",
      f"- Measurement bias: two-term {decisions.policy_bias:+.4f}, control {decisions.control_bias:+.4f}. Within {p7_evals.BIAS_MARGIN} in absolute value: {yes_no(decisions.bias_within_margin)}.",
      f"- False mastery: the worst arm, {decisions.worst_false_mastery_arm}, declared {decisions.worst_false_mastery_share:.1%} of its masteries on skills the student did not know. Ceiling {p7_evals.FALSE_MASTERY_CEILING:.0%}. Within: {yes_no(decisions.false_mastery_within_ceiling)}. Set apart the diagnostic's placements and the seeded parents of `app/session/seed.py`, the worst arm's share among masteries declared from practice is {decisions.worst_practice_false_mastery_share:.1%}.",
   ]


def render(results):
   lines = [
      "---",
      "title: P7 simulation record",
      "research_date: 2026-09-24",
      "status: recorded",
      "purpose: The P7 policy comparison on a synthetic world that learns, and the decisions it makes on the five-term score, the decay term and the other acceptance thresholds of docs/plan/10.",
      "---",
      "",
      "# P7 simulation record",
      "",
      f"Written by `tools/p7_evals.py` from `app/sim/p7_evals.py` and `app/sim/learning.py`, seed base {p7_evals.SEED_BASE}, {STUDENTS} synthetic students, {DAYS} daily sessions after a diagnostic, every arm on the same students and seeds. Every number is a simulation's measurement on synthetic students whose world model is invented. None is a human's measurement and none is a real student's. A simulation can falsify a policy choice and cannot validate one.",
      "",
      "The world learns. Each student starts from the P2 knowledge state, closed under hard prerequisites, and carries a learning rate per skill drawn uniformly from "
      f"{learning.LEARNING_RATE_LOW} to {learning.LEARNING_RATE_HIGH}. An attempt can teach a loaded skill whose hard parents are all known, with that rate scaled by the fading stage the item was served at (example 1.0, completion 0.75, unsupported 0.5). True mastery per item is the sum, over skills learned during the run, of the student's chance of retrieving each skill the day after the run, divided by items served. Retention at day 7 and day 30 is the mean retrieval chance over every known skill that many days after the run with no practice. Bias is 10's measurement bias, the mean of sigmoid(m_k) minus the retrieval chance over observed skills. The learning band and the stage multipliers are [inferred]; no source gives them.",
      "",
   ]

   for curve, (summaries, decisions, _) in results.items():
      lines.append(f"## Forgetting curve: {curve.replace('_', ' ')}")
      lines.append("")
      lines.append(ARM_HEADER)

      for summary in summaries:
         lines.append(arm_row(summary))

      lines.append("")
      lines.extend(decision_lines(decisions, STUDENTS))
      lines.append("")

   identical = {
      curve: [arm_name for arm_name in twins]
      for curve, (_, _, twins) in results.items()
   }
   lines.extend([
      "## Reading the table",
      "",
      "Arms that served every student exactly what two-term served, item for item: "
      + "; ".join(f"{curve.replace('_', ' ')}, {', '.join(names) if names else 'none'}" for curve, names in identical.items())
      + ". Under two-term selection `LAMBDA` reaches only `sigmoid(m_k)` taken with a retrievability argument. The fringe, block 1's due coverage and the mastery rule read none of that, so the decay term has no path into what is served, and arm 6 cannot pass its gate by construction. Its failure is not evidence that decay is useless. The compensatory prediction is read only by the stage bands of skills with no credited observation.",
      "",
      "Retention at day 7 and day 30 averages over every known skill, including skills known from the start and never practised, which sit at 1.0. An arm that teaches fewer skills keeps a higher mean, so an arm can lead on retention while losing on true mastery per item.",
      "",
   ])

   exponential = results[learning.EXPONENTIAL][1]
   power_law = results[learning.POWER_LAW][1]
   five_on = exponential.five_term_on and power_law.five_term_on
   lambda_on = exponential.lambda_returns and power_law.lambda_returns

   lines.extend([
      "## Decisions",
      "",
      "A setting changes only when it clears its bar under both forgetting curves, so no decision rests on a curve shape the world model invented.",
      "",
      f"- The five-term score, `W_LEARN`, `W_COV`, `W_WEIGHT`, `W_REP` and `EXPLORE_SHARE`: {'turned on' if five_on else 'stays off'}.",
      f"- `lambda`: {'returns to 2.0' if lambda_on else 'stays 0'}.",
      "",
   ])

   return "\n".join(lines)


def main():
   workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
   results = {}

   for curve in learning.CURVES:
      by_arm = p7_evals.run_arms(list(learning.ARMS), STUDENTS, DAYS, curve=curve, workers=workers)
      summaries = [p7_evals.summarise(runs) for runs in by_arm.values()]
      twins = [
         arm_name
         for arm_name, runs in by_arm.items()
         if arm_name != "two_term" and p7_evals.served_identically(runs, by_arm["two_term"])
      ]
      results[curve] = (summaries, p7_evals.decide(by_arm), twins)

   RECORD_PATH.write_text(render(results))
   print(f"wrote {RECORD_PATH.relative_to(REPOSITORY_ROOT)}")


if __name__ == "__main__":
   main()
