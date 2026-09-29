"""Measure Today's assembly on synthetic students under the two-term arm.

   .venv/bin/python tools/today_metrics.py <students> <days> [curve] [world] [workers] [out.json]

Runs the first N seeds from app/sim/p7_evals.py SEED_BASE through app/sim/today_metrics.py,
prints a Markdown table of every measure with its mean over students and a 95 percent normal
interval, and writes the per-student numbers and the pooled histograms as JSON. Every number is a
simulation's measurement on synthetic students.
"""
import json
import sys
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(REPOSITORY_ROOT))

from app.sim import learning, p7_evals, selection_study, today_metrics  # noqa: E402

ARM = "two_term"


def measure_job(job):
   seed, days, curve, world_name = job

   return today_metrics.measure_student(ARM, seed, days, curve, world_name).to_json()


def pooled(results, key):
   total = Counter()

   for result in results:
      total.update(result[key])

   return dict(sorted(total.items(), key=lambda pair: [int(part) for part in pair[0].split(",")]))


def summary_rows(results):
   rows = [
      "| Measure | Students with a value | Mean [95% CI] |",
      "|---|---|---|",
   ]
   names = list(results[0]["scalars"])

   for name in names:
      values = [
         result["scalars"][name]
         for result in results
         if result["scalars"][name] is not None
      ]
      has_values = len(values) > 0

      if not has_values:
         rows.append(f"| {name} | 0 | n/a |")
         continue

      mean, (low, high) = selection_study.mean_interval(values)
      rows.append(f"| {name} | {len(values)} | {mean:.3f} [{low:.3f}, {high:.3f}] |")

   return rows


def histogram_rows(title, histogram):
   total = sum(histogram.values())
   rows = [f"| {title} | Count | Share |", "|---|---|---|"]

   for key, count in histogram.items():
      share = count / total if total else 0.0
      rows.append(f"| {key} | {count} | {share:.3f} |")

   return rows


def main():
   students = int(sys.argv[1])
   days = int(sys.argv[2])
   curve = sys.argv[3] if len(sys.argv) > 3 else learning.EXPONENTIAL
   world_name = sys.argv[4] if len(sys.argv) > 4 else "fixed"
   workers = int(sys.argv[5]) if len(sys.argv) > 5 else 1
   out_path = Path(sys.argv[6]) if len(sys.argv) > 6 else None
   jobs = [(p7_evals.SEED_BASE + index, days, curve, world_name) for index in range(students)]
   started = time.time()
   results = []

   with ProcessPoolExecutor(max_workers=workers) as pool:
      for job, result in zip(jobs, pool.map(measure_job, jobs)):
         results.append(result)
         print(f"seed {job[0]} done at {time.time() - started:.0f} s ({len(results)} of {students})", file=sys.stderr, flush=True)

   histograms = {
      "block2_tie_sizes": pooled(results, "block2_tie_sizes"),
      "block2_decided_by": dict(sum((Counter(result["block2_decided_by"]) for result in results), Counter())),
      "window_sizes": pooled(results, "window_sizes"),
      "items_before_mastery_histogram": pooled(results, "items_before_mastery_histogram"),
   }
   lines = [
      f"Arm {ARM}, world {world_name}, {curve} forgetting, {days} days, {students} students from seed {p7_evals.SEED_BASE}.",
      "",
      *summary_rows(results),
      "",
      *histogram_rows("Block 2 tied pool size", histograms["block2_tie_sizes"]),
      "",
      *histogram_rows("Window candidates before,after", histograms["window_sizes"]),
      "",
      *histogram_rows("Items before mastery", histograms["items_before_mastery_histogram"]),
   ]
   print("\n".join(lines))

   if out_path is not None:
      out_path.write_text(json.dumps({
         "arm": ARM,
         "world": world_name,
         "curve": curve,
         "days": days,
         "seed_base": p7_evals.SEED_BASE,
         "students": results,
         "pooled": histograms,
      }, indent=1))
      print(f"wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
   main()
