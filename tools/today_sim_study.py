"""Run the Today selection study: the candidate policies of app/sim/today_policies.py beside the
two-term policy, the random control and the forgetting oracle, on the same synthetic students.

   .venv/bin/python tools/today_sim_study.py [students] [workers] [out.md] [per_student.json]
      [--worlds fixed,legacy] [--days 60,226] [--arms two_term,random_control,...]

Deterministic from app/sim/p7_evals.py SEED_BASE: the same code, seed base and sizes write the
same record. Every number is a simulation's measurement on synthetic students.
"""
import argparse
import json
import sys
import time
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPOSITORY_ROOT))

from app.sim import learning, p7_evals, selection_study, today_policies  # noqa: E402

DEFAULT_RECORD_PATH = REPOSITORY_ROOT / "docs" / "operator" / "today-sim-study-record.md"
RESEARCH_DATE = "2026-09-29"

STUDENTS = 200
WORKERS = 4
WORLDS = ["fixed", "legacy"]
HORIZONS = [60, 226]
BASELINE_ARMS = ["two_term", "random_control", "oracle_forgetting"]
DEFAULT_ARMS = BASELINE_ARMS + list(today_policies.TODAY_ARMS)
INCUMBENTS = ["two_term", "random_control"]

MEASURES = {
   "mastery per item": lambda run: run.true_mastery_per_item,
   "delayed mastery per item": lambda run: run.delayed_mastery_per_item,
   "retention day 30": lambda run: run.retention_day_30,
   "skills learned": lambda run: run.learned,
}


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


def comparisons(arm_names):
   """Every arm but the incumbents, the oracle among them, against each incumbent that ran."""
   pairs = []

   for challenger in arm_names:
      is_incumbent = challenger in INCUMBENTS

      if is_incumbent:
         continue

      for incumbent in INCUMBENTS:
         if incumbent in arm_names:
            pairs.append((challenger, incumbent))

   return pairs


def comparison_rows(by_arm):
   rows = [
      "| Challenger | Incumbent | Measure | Wins / ties / losses | Matched or beat, % [95% CI] | Beat, % [95% CI] | Mean paired difference [95% CI] | Traces identical |",
      "|---|---|---|---|---|---|---|---|",
   ]

   for challenger, incumbent in comparisons(list(by_arm)):
      challenger_runs = by_arm[challenger]
      incumbent_runs = by_arm[incumbent]
      identical = sum(
         1 for first, second in zip(challenger_runs, incumbent_runs) if first.trace == second.trace
      )

      for measure_name, measure in MEASURES.items():
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


def render(sections, students, elapsed):
   lines = [
      "---",
      "title: Today selection study record",
      f"research_date: {RESEARCH_DATE}",
      "status: recorded",
      "purpose: The numbers behind the Today selection policies of app/sim/today_policies.py, written by tools/today_sim_study.py; simulation only.",
      "---",
      "",
      "# Today selection study record",
      "",
      f"Written by `tools/today_sim_study.py` in {elapsed / 60:.0f} minutes, seed base {p7_evals.SEED_BASE}, {students} synthetic students per arm, every arm on the same students. Every number is a simulation's measurement on synthetic students whose world model is invented; none is a person's and none is the student's. Intervals are 95 percent: Wilson for shares, normal approximation for means. Worlds: `legacy` is the stage 8 world, `fixed` adds keyed draws, consolidated prior knowledge and daily half-life growth (`app/sim/learning.py` WorldRules). Every arm keeps the full interleaving rules and the shipped block 1; `review_first` and `retrievability_priority_both` change block 3, every other candidate changes block 2 only.",
      "",
      f"Mastery per item is the stage 8 measure, read the day after the run. Delayed mastery per item reads the same skills {learning.RETENTION_PROBE_DAYS[1]} days after the run. Retention day 30 averages over every known skill. Skills learned counts the skills the world turned known during the run.",
      "",
   ]

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


def comma_list(text):
   return [part.strip() for part in text.split(",") if part.strip()]


def parse_arguments(argv):
   parser = argparse.ArgumentParser(description="Run the Today selection study.")
   parser.add_argument("students", nargs="?", type=int, default=STUDENTS)
   parser.add_argument("workers", nargs="?", type=int, default=WORKERS)
   parser.add_argument("record", nargs="?", type=Path, default=DEFAULT_RECORD_PATH)
   parser.add_argument("per_student", nargs="?", type=Path, default=None)
   parser.add_argument("--worlds", type=comma_list, default=WORLDS)
   parser.add_argument("--days", type=lambda text: [int(part) for part in comma_list(text)], default=HORIZONS)
   parser.add_argument("--arms", type=comma_list, default=DEFAULT_ARMS)
   arguments = parser.parse_args(argv)
   unknown_arms = [name for name in arguments.arms if name not in selection_study.ALL_ARMS]
   unknown_worlds = [name for name in arguments.worlds if name not in selection_study.WORLDS]

   if unknown_arms:
      parser.error(f"unknown arms: {', '.join(unknown_arms)}")

   if unknown_worlds:
      parser.error(f"unknown worlds: {', '.join(unknown_worlds)}")

   if arguments.per_student is None:
      arguments.per_student = arguments.record.with_suffix(".json")

   return arguments


def main(argv=None):
   arguments = parse_arguments(sys.argv[1:] if argv is None else argv)
   started = time.time()
   seeds = [p7_evals.SEED_BASE + index for index in range(arguments.students)]
   sections = []

   for world_name in arguments.worlds:
      for days in arguments.days:
         for curve in learning.CURVES:
            by_arm = selection_study.run_grid(
               arguments.arms,
               seeds,
               days,
               curve,
               world_name,
               workers=arguments.workers,
            )
            sections.append(((world_name, days, curve), by_arm))
            print(
               f"{world_name} {days} days {curve}: done at {time.time() - started:.0f} s",
               file=sys.stderr,
               flush=True,
            )

   arguments.record.write_text(render(sections, arguments.students, time.time() - started))
   arguments.per_student.write_text(json.dumps(per_student(sections)))
   print(f"wrote {arguments.record} and {arguments.per_student}", file=sys.stderr)


if __name__ == "__main__":
   main()
