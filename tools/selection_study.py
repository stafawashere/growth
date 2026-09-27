"""Run the stage 12 selection study and write docs/operator/selection-study-record.md.

   .venv/bin/python tools/selection_study.py [workers]

Deterministic from app/sim/p7_evals.py SEED_BASE: the same code, seed base and sizes write the
same record. The interpretation lives in docs/operator/selection-study.md, written by hand from
this record. Every number is a simulation's measurement on synthetic students.
"""
import json
import sys
import time
from collections import Counter
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPOSITORY_ROOT))

from app.engine import select  # noqa: E402
from app.sim import learning, p7_evals, selection_study  # noqa: E402

RECORD_PATH = REPOSITORY_ROOT / "docs" / "operator" / "selection-study-record.md"

STUDENTS = 200
SHORT_DAYS = 60
LIVE_DAYS = 226
FIRING_STUDENTS = 20

CONTROL_ARMS = ["two_term", "random_control", "oracle_forgetting", "oracle_teaching", "most_recent"]
POLICY_ARMS = ["five_term", "decay_lambda_2", "five_term_lambda_2"]

BLOCKS = [
   ("legacy", SHORT_DAYS, CONTROL_ARMS),
   ("legacy_keyed", SHORT_DAYS, ["two_term"]),
   ("fixed", SHORT_DAYS, CONTROL_ARMS + POLICY_ARMS),
   ("fixed", LIVE_DAYS, CONTROL_ARMS + POLICY_ARMS),
]

MEASURES = {
   "mastery per item": lambda run: run.true_mastery_per_item,
   "delayed mastery per item": lambda run: run.delayed_mastery_per_item,
   "retention day 30": lambda run: run.retention_day_30,
}

COMPARISONS = [
   ("two_term", "random_control", ["mastery per item", "delayed mastery per item"]),
   ("two_term_reseeded", "two_term", ["mastery per item", "delayed mastery per item"]),
   ("two_term_reseeded", "random_control", ["mastery per item", "delayed mastery per item"]),
   ("oracle_forgetting", "random_control", ["mastery per item", "delayed mastery per item"]),
   ("oracle_teaching", "random_control", ["mastery per item", "delayed mastery per item"]),
   ("most_recent", "random_control", ["mastery per item", "delayed mastery per item"]),
   ("five_term", "two_term", ["mastery per item", "delayed mastery per item"]),
   ("decay_lambda_2", "two_term", ["mastery per item", "retention day 30", "delayed mastery per item"]),
   ("five_term_lambda_2", "five_term", ["mastery per item", "retention day 30", "delayed mastery per item"]),
]


def percent(value):
   return f"{100 * value:.1f}"


def interval_text(bounds, digits=5):
   low, high = bounds

   return f"[{low:.{digits}f}, {high:.{digits}f}]"


def arm_rows(by_arm):
   rows = [
      "| Arm | Students | Items, mean | Skills learned, mean | Declared from practice, mean | Mastery per item, mean [95% CI] | Delayed mastery per item, mean [95% CI] | Retention day 30, mean |",
      "|---|---|---|---|---|---|---|---|",
   ]

   for arm_name, runs in by_arm.items():
      count = len(runs)
      items = sum(run.items for run in runs) / count
      learned = sum(run.learned for run in runs) / count
      practised = sum(run.declared_mastered - run.placed_mastered for run in runs) / count
      mastery, mastery_bounds = selection_study.mean_interval([run.true_mastery_per_item for run in runs])
      delayed, delayed_bounds = selection_study.mean_interval([run.delayed_mastery_per_item for run in runs])
      retention = sum(run.retention_day_30 for run in runs) / count
      rows.append(
         f"| {arm_name} | {count} | {items:.0f} | {learned:.1f} | {practised:.1f} | "
         f"{mastery:.5f} {interval_text(mastery_bounds)} | {delayed:.5f} {interval_text(delayed_bounds)} | {retention:.4f} |"
      )

   return rows


def comparison_rows(by_arm):
   rows = [
      "| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |",
      "|---|---|---|---|---|---|---|---|",
   ]

   for challenger, incumbent, measure_names in COMPARISONS:
      has_both = challenger in by_arm and incumbent in by_arm

      if not has_both:
         continue

      challenger_runs = by_arm[challenger]
      incumbent_runs = by_arm[incumbent]
      identical = sum(
         1 for first, second in zip(challenger_runs, incumbent_runs) if first.trace == second.trace
      )

      for measure_name in measure_names:
         measure = MEASURES[measure_name]
         wins, ties, losses = selection_study.paired_counts(challenger_runs, incumbent_runs, measure)
         total = wins + ties + losses
         at_least = selection_study.wilson_interval(wins + ties, total)
         beat = selection_study.wilson_interval(wins, total)
         difference, bounds = selection_study.mean_interval(
            selection_study.paired_differences(challenger_runs, incumbent_runs, measure)
         )
         rows.append(
            f"| {challenger} | {incumbent} | {measure_name} | {wins} / {ties} / {losses} | "
            f"{percent((wins + ties) / total)} [{percent(at_least[0])}, {percent(at_least[1])}] | "
            f"{percent(wins / total)} [{percent(beat[0])}, {percent(beat[1])}] | "
            f"{difference:+.5f} {interval_text(bounds)} | {identical} of {total} |"
         )

   return rows


def due_coverage_firing(days, curve):
   """How often block 2's due coverage term had anything to say, over the first students."""
   tally = Counter()
   original = select.choose_by_due_coverage

   def counting(records, states, graph, today, retrievability, rng):
      if records:
         best = max(select.due_coverage(record, states, graph, today, retrievability) for record in records)
         tally["choices"] += 1
         tally["fired"] += best > 0

      return original(records, states, graph, today, retrievability, rng)

   select.choose_by_due_coverage = counting

   try:
      for index in range(FIRING_STUDENTS):
         learning.run_student(learning.ARMS["two_term"], p7_evals.SEED_BASE + index, days, curve)
   finally:
      select.choose_by_due_coverage = original

   return tally["fired"], tally["choices"]


def render(sections, firing, elapsed):
   lines = [
      "---",
      "title: Selection study record",
      "research_date: 2026-09-26",
      "status: recorded",
      "purpose: The numbers behind docs/operator/selection-study.md, written by tools/selection_study.py; simulation only.",
      "---",
      "",
      "# Selection study record",
      "",
      f"Written by `tools/selection_study.py` in {elapsed / 60:.0f} minutes, seed base {p7_evals.SEED_BASE}, {STUDENTS} synthetic students per arm, every arm on the same students. Every number is a simulation's measurement on synthetic students whose world model is invented; none is a person's and none is the student's. Intervals are 95 percent: Wilson for shares, normal approximation for means. `two_term_reseeded` is two-term with only the engine's draws reseeded, the noise floor. Worlds: `legacy` is the stage 8 world, `legacy_keyed` adds keyed draws only, `fixed` adds keyed draws, consolidated prior knowledge and daily half-life growth (`app/sim/learning.py` WorldRules).",
      "",
      f"Mastery per item is the stage 8 measure, read the day after the run. Delayed mastery per item reads the same skills {learning.RETENTION_PROBE_DAYS[1]} days after the run. Retention day 30 averages over every known skill.",
      "",
      "## How often due coverage fires",
      "",
   ]

   for (days, curve), (fired, choices) in firing.items():
      lines.append(
         f"- Fixed world, {curve.replace('_', ' ')}, {days} days, the first {FIRING_STUDENTS} students under two-term: due coverage was above 0 for some candidate on {fired} of {choices} block 2 choices ({percent(fired / choices if choices else 0.0)} percent); on every other choice two-term drew uniformly, as the control does."
      )

   lines.append("")

   for (world_name, days, curve), by_arm in sections:
      lines.append(f"## World {world_name}, {curve.replace('_', ' ')} forgetting, {days} days")
      lines.append("")
      lines.extend(arm_rows(by_arm))
      lines.append("")
      lines.extend(comparison_rows(by_arm))
      lines.append("")

   return "\n".join(lines)


def per_student(sections):
   out = {}

   for (world_name, days, curve), by_arm in sections:
      key = f"{world_name}/{days}/{curve}"
      out[key] = {
         arm_name: [
            {
               "seed": run.seed,
               "items": run.items,
               "learned": run.learned,
               "mastery_per_item": run.true_mastery_per_item,
               "delayed_mastery_per_item": run.delayed_mastery_per_item,
               "retention_day_30": run.retention_day_30,
            }
            for run in runs
         ]
         for arm_name, runs in by_arm.items()
      }

   return out


def main():
   workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
   dump_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
   started = time.time()
   seeds = [p7_evals.SEED_BASE + index for index in range(STUDENTS)]
   sections = []

   for world_name, days, arm_names in BLOCKS:
      for curve in learning.CURVES:
         by_arm = selection_study.run_grid(
            arm_names,
            seeds,
            days,
            curve,
            world_name,
            workers=workers,
            reseeded_arms=["two_term"],
         )
         sections.append(((world_name, days, curve), by_arm))
         print(f"{world_name} {days} days {curve}: done at {time.time() - started:.0f} s", flush=True)

   firing = {
      (days, learning.EXPONENTIAL): due_coverage_firing(days, learning.EXPONENTIAL)
      for days in (SHORT_DAYS, LIVE_DAYS)
   }

   RECORD_PATH.write_text(render(sections, firing, time.time() - started))

   if dump_path is not None:
      dump_path.write_text(json.dumps(per_student(sections)))

   print(f"wrote {RECORD_PATH.relative_to(REPOSITORY_ROOT)}")


if __name__ == "__main__":
   main()
