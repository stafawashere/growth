"""Mastery throughput of the whole-graph simulation, the instrument behind the pace goal.

One synthetic student per seed is run from app/sim/whole_graph.START_DAY to the end day in a
single run_days call, never chunked, since chunking would reset the attempts history that the
repeat window and the format alternation read. The report gives the mastered count by unit at
each checkpoint, the day each unit completes, and, for every unmastered teachable skill with at
least --min-observations observations, which of the six mastery conditions of docs/plan/02 fail.

   PYTHONPATH=. .venv/bin/python tools/throughput.py --seeds 1 2 3 --ability 3.0
   PYTHONPATH=. .venv/bin/python tools/throughput.py --fast
   PYTHONPATH=. .venv/bin/python tools/throughput.py --population 20
   PYTHONPATH=. .venv/bin/python tools/throughput.py --seeds 1 --trace BC-SKL-01054

Nothing here writes to data/ and nothing here modifies the engine.
"""
import argparse
import json
import random
from collections import Counter
from datetime import date, timedelta

from app.engine import diagnostic
from app.engine.strength import probability
from app.engine.update import mastery_conditions, required_distinct_archetypes
from app.sim import learning, whole_graph

EXAM_EVE = date(2027, 5, 7)
WORLD_FIXED = "fixed"
WORLD_LEARNING = "learning"
WORLDS = (WORLD_FIXED, WORLD_LEARNING)
DEFAULT_CHECKPOINTS = (30, 60, 90, 120, 150, 180, 219)
DEFAULT_MIN_OBSERVATIONS = 10
FAST_DAYS = 60
FAST_POPULATION = 5
POPULATION_SEED_BASE = 3000
CONDITION_NAMES = (
   "strength",
   "unaided_successes",
   "distinct_archetypes",
   "distinct_days",
   "day_span",
   "retention",
)


def day_count(start, end):
   """Calendar days from start to end, both included."""
   return (end - start).days + 1


def teachable_skills(graph):
   return sorted(skill_id for skill_id in graph.skills if graph.has_archetype(skill_id))


def skills_by_unit(graph, skill_ids):
   by_unit = {}

   for skill_id in skill_ids:
      unit = graph.skills[skill_id].get("unit")
      by_unit.setdefault(unit, []).append(skill_id)

   return by_unit


def mastered_by_unit(states, by_unit):
   return {
      unit: sum(1 for skill_id in skills if states[skill_id].mastered)
      for unit, skills in by_unit.items()
   }


def unit_completion_days(snapshots, by_unit):
   """The first offset at which every teachable skill of a unit is mastered, or None."""
   completed = {}

   for offset, counts in snapshots:
      for unit, skills in by_unit.items():
         is_done = counts.get(unit, 0) == len(skills)
         is_new = unit not in completed

         if is_done and is_new:
            completed[unit] = offset

   return {unit: completed.get(unit) for unit in by_unit}


def failing_conditions(state, today, archetypes_available):
   held = mastery_conditions(state, today, archetypes_available)

   return tuple(name for name in CONDITION_NAMES if not held[name])


def group_failures(rows):
   """Counts of each failing-condition set, most common first."""
   counts = Counter(row["failing"] for row in rows)

   return sorted(counts.items(), key=lambda entry: (-entry[1], entry[0]))


def serve_profile(history, graph):
   """Per skill: how often it was served as the primary and as a loaded secondary skill, the
   stage each serve came at, and unaided successes and failures while loaded."""
   profile = {}

   for day_record in history:
      for item, record, prediction in zip(day_record.session.served, day_record.records, day_record.predictions):
         is_correct = prediction[1]
         stage = item["stage"].value
         primary = graph.primary_skill(record["id"])

         for skill_id in record["skills"]:
            entry = profile.setdefault(skill_id, {
               "as_primary": 0,
               "as_secondary": 0,
               "stages": Counter(),
               "unaided_correct": 0,
               "unaided_wrong": 0,
            })
            is_primary = skill_id == primary

            if is_primary:
               entry["as_primary"] += 1
            else:
               entry["as_secondary"] += 1

            entry["stages"][stage] += 1
            is_unaided = stage == "unsupported"

            if is_unaided and is_correct:
               entry["unaided_correct"] += 1

            if is_unaided and not is_correct:
               entry["unaided_wrong"] += 1

   return profile


def blocking_ancestors(skill_id, graph, memo):
   if skill_id in memo:
      return memo[skill_id]

   ancestors = set()

   for parent in graph.blocking_parents(skill_id):
      ancestors.add(parent)
      ancestors |= blocking_ancestors(parent, graph, memo)

   memo[skill_id] = frozenset(ancestors)

   return memo[skill_id]


def blocker_weights(states, graph, teachable):
   """For every unmastered skill, how many unmastered teachable skills sit behind it on the
   blocking chains, so the skill whose mastery would open the most is visible."""
   memo = {}
   weights = Counter()
   unmastered = [skill_id for skill_id in teachable if not states[skill_id].mastered]

   for skill_id in unmastered:
      for ancestor in blocking_ancestors(skill_id, graph, memo):
         is_open_blocker = ancestor in states and not states[ancestor].mastered

         if is_open_blocker:
            weights[ancestor] += 1

   return weights


def observation_histogram(states, teachable):
   """Unmastered teachable skills by observation count band."""
   bands = Counter()

   for skill_id in teachable:
      state = states[skill_id]

      if state.mastered:
         continue

      count = state.observation_count
      band = "0" if count == 0 else "1-9" if count < 10 else "10-29" if count < 30 else "30+"
      bands[band] += 1

   return dict(bands)


def stuck_rows(states, graph, engine_graph, world_model, today, min_observations, profile):
   rows = []

   for skill_id in teachable_skills(graph):
      state = states[skill_id]
      is_candidate = not state.mastered and state.observation_count >= min_observations

      if not is_candidate:
         continue

      available = engine_graph.servable_archetype_count(skill_id, states)
      blocking = [parent for parent in graph.blocking_parents(skill_id) if not states[parent].mastered]
      served = profile.get(skill_id, {})
      rows.append({
         "skill": skill_id,
         "unit": graph.skills[skill_id].get("unit"),
         "known": world_model.knows(skill_id),
         "failing": failing_conditions(state, today, available),
         "observations": state.observation_count,
         "unaided": state.unaided_success_count,
         "archetypes": len(state.distinct_archetypes_succeeded),
         "required": required_distinct_archetypes(available),
         "days": len(state.success_days),
         "p": round(probability(state), 3),
         "c": round(state.c, 2),
         "f": round(state.f, 2),
         "stage": state.fading_stage.value,
         "blocking": blocking,
         "as_primary": served.get("as_primary", 0),
         "as_secondary": served.get("as_secondary", 0),
         "unaided_correct": served.get("unaided_correct", 0),
         "unaided_wrong": served.get("unaided_wrong", 0),
      })

   return rows


def failure_rate_by_window(history, window_days=30):
   """The share of served items answered wrong, per window of days, to watch the world's decay."""
   totals = Counter()
   wrong = Counter()

   for offset, day_record in enumerate(history):
      bucket = offset // window_days

      for _, is_correct in day_record.predictions:
         totals[bucket] += 1

         if not is_correct:
            wrong[bucket] += 1

   return [
      (bucket * window_days, totals[bucket], round(wrong[bucket] / totals[bucket], 3) if totals[bucket] else None)
      for bucket in sorted(totals)
   ]


def trace_skill(history, graph, skill_id):
   lines = []

   for day_record in history:
      for item, record, prediction in zip(day_record.session.served, day_record.records, day_record.predictions):
         if skill_id not in record["skills"]:
            continue

         role = "primary" if graph.primary_skill(record["id"]) == skill_id else "secondary"
         verdict = "correct" if prediction[1] else "wrong"
         lines.append(
            f"{day_record.day.isoformat()} {record['id']} {role} {item['stage'].value} "
            f"{item['format']} {verdict} p={prediction[0]:.2f}"
         )

   return lines


def make_student(seed, ability, graph):
   units = diagnostic.graph_units(graph)
   rng = random.Random(seed)

   if ability is None:
      return whole_graph.make_student(f"population-{seed}", rng)

   return whole_graph.make_student(
      f"ability-{ability}-{seed}", rng, unit_ability={unit: ability for unit in units}
   )


def make_world(student, seed, world, hard_parents):
   """The fixed World of the P1 runner, or 10's learning world with the stage 12 rules: a
   per-skill learning rate, prior knowledge consolidated at the capped half-life, and half-life
   growth at most once a day."""
   is_fixed = world == WORLD_FIXED

   if is_fixed:
      return None

   learner = learning.learning_student_from(student, random.Random(seed + 31))

   return learning.LearningWorld(
      learner,
      hard_parents,
      random.Random(seed + 104729),
      rules=learning.WORLD,
      seed=seed + 104729,
      start_day=whole_graph.START_DAY,
   )


def run_one(seed, ability, days, checkpoints, min_observations, trace=None, world=WORLD_FIXED):
   library = whole_graph.library()
   graph = library.graph
   engine_graph = library.engine_graph
   bank = whole_graph.synthetic_bank(graph)
   student = make_student(seed, ability, graph)
   world_model = make_world(student, seed, world, engine_graph.hard_parents)
   known_at_start = sum(1 for skill_id in teachable_skills(graph) if student.true_state.get(skill_id))
   teachable = teachable_skills(graph)
   by_unit = skills_by_unit(graph, teachable)
   snapshots = []
   checkpoint_counts = {}
   wanted = set(checkpoints)

   def on_day(today, states):
      offset = (today - whole_graph.START_DAY).days + 1
      counts = mastered_by_unit(states, by_unit)
      snapshots.append((offset, counts))

      if offset in wanted:
         checkpoint_counts[offset] = counts

   history, states, world_model, served = whole_graph.run_days(
      student, bank, seed=seed, days=days, on_day=on_day, world_model=world_model
   )
   last_day = whole_graph.START_DAY + timedelta(days=days - 1)
   profile = serve_profile(history, graph)
   weights = blocker_weights(states, graph, teachable)
   known = [skill_id for skill_id in teachable if world_model.knows(skill_id)]
   mastered = [skill_id for skill_id in teachable if states[skill_id].mastered]
   false_mastered = [skill_id for skill_id in mastered if not world_model.knows(skill_id)]

   return {
      "seed": seed,
      "ability": ability,
      "world": world,
      "days": days,
      "served": served,
      "teachable": len(teachable),
      "known_at_start": known_at_start,
      "known": len(known),
      "mastered": len(mastered),
      "false_mastered": false_mastered,
      "unknown_unmastered": sorted(set(teachable) - set(known) - set(mastered)),
      "checkpoints": checkpoint_counts,
      "unit_sizes": {unit: len(skills) for unit, skills in by_unit.items()},
      "completion": unit_completion_days(snapshots, by_unit),
      "stuck": stuck_rows(states, graph, engine_graph, world_model, last_day, min_observations, profile),
      "unmastered_by_observations": observation_histogram(states, teachable),
      "top_blockers": [
         {
            "skill": skill_id,
            "blocked": weight,
            "observations": states[skill_id].observation_count,
            "failing": failing_conditions(
               states[skill_id], last_day, engine_graph.servable_archetype_count(skill_id, states)
            ),
            "p": round(probability(states[skill_id]), 3),
            "unaided": states[skill_id].unaided_success_count,
            "on_fringe": all(states[parent].mastered for parent in graph.blocking_parents(skill_id)),
         }
         for skill_id, weight in weights.most_common(12)
      ],
      "failure_rate": failure_rate_by_window(history),
      "trace": trace_skill(history, graph, trace) if trace else [],
   }


def format_run(result):
   lines = []
   units = sorted(result["unit_sizes"])
   label = "population" if result["ability"] is None else f"ability {result['ability']}"
   lines.append(
      f"seed {result['seed']} ({label}, {result['world']} world): mastered {result['mastered']} of "
      f"{result['teachable']} teachable, known {result['known_at_start']} at the start and "
      f"{result['known']} at the end, {result['served']} items over {result['days']} days, "
      f"false mastered {len(result['false_mastered'])}"
   )
   lines.append("checkpoint " + " ".join(f"{unit[-2:]:>4}" for unit in units) + " total")

   for offset in sorted(result["checkpoints"]):
      counts = result["checkpoints"][offset]
      total = sum(counts.values())
      lines.append(f"day {offset:>6} " + " ".join(f"{counts.get(unit, 0):>4}" for unit in units) + f" {total:>5}")

   lines.append("unit sizes " + " ".join(f"{result['unit_sizes'][unit]:>4}" for unit in units))
   completion = result["completion"]
   lines.append("completes  " + " ".join(f"{completion[unit] if completion[unit] is not None else '-':>4}" for unit in units))
   lines.append("failure rate by 30-day window: " + ", ".join(
      f"day {start}+ {rate} of {count}" for start, count, rate in result["failure_rate"]
   ))
   lines.append("unmastered by observation count: " + ", ".join(
      f"{band} obs {count}" for band, count in sorted(result["unmastered_by_observations"].items())
   ))
   lines.append("top blockers (unmastered skills with the most unmastered teachable skills behind them):")

   for row in result["top_blockers"]:
      lines.append(
         f"  {row['skill']} blocks {row['blocked']} obs={row['observations']} unaided={row['unaided']} "
         f"p={row['p']} on_fringe={row['on_fringe']} fail={','.join(row['failing'])}"
      )

   stuck = result["stuck"]
   lines.append(f"unmastered with at least the observation floor: {len(stuck)}")

   for failing, count in group_failures(stuck):
      lines.append(f"  {count:>4}  fail {', '.join(failing) if failing else 'nothing (waiting on a re-evaluation)'}")

   for row in stuck:
      blocking = f" blocked_by={','.join(row['blocking'])}" if row["blocking"] else ""
      lines.append(
         f"  {row['skill']} {row['unit'][-2:]} known={row['known']} fail={','.join(row['failing'])} "
         f"obs={row['observations']} unaided={row['unaided']} arch={row['archetypes']}/{row['required']} "
         f"days={row['days']} p={row['p']} c={row['c']} f={row['f']} stage={row['stage']} "
         f"primary={row['as_primary']} secondary={row['as_secondary']} "
         f"unaided_ok={row['unaided_correct']} unaided_wrong={row['unaided_wrong']}{blocking}"
      )

   if result["unknown_unmastered"]:
      lines.append(f"teachable skills the student never knew: {len(result['unknown_unmastered'])}")

   if result["trace"]:
      lines.append("trace:")
      lines.extend("  " + line for line in result["trace"])

   return "\n".join(lines)


def format_population(results):
   lines = ["population: seed known mastered false completed_units"]

   for result in results:
      completed = sum(1 for offset in result["completion"].values() if offset is not None)
      lines.append(
         f"  {result['seed']} {result['known']:>4} {result['mastered']:>4} "
         f"{len(result['false_mastered']):>3} {completed:>2}"
      )

   mastered = [result["mastered"] for result in results]
   lines.append(f"  mean mastered {sum(mastered) / len(mastered):.1f}, min {min(mastered)}, max {max(mastered)}")

   return "\n".join(lines)


def parse_args(argv=None):
   parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
   parser.add_argument("--seeds", type=int, nargs="*", default=[1, 2, 3])
   parser.add_argument("--ability", type=float, default=3.0, help="unit ability for every unit")
   parser.add_argument("--population", type=int, default=0, help="also run this many default-population students")
   parser.add_argument("--end", type=date.fromisoformat, default=EXAM_EVE)
   parser.add_argument("--days", type=int, default=None, help="override the day count")
   parser.add_argument("--checkpoints", type=int, nargs="*", default=list(DEFAULT_CHECKPOINTS))
   parser.add_argument("--min-observations", type=int, default=DEFAULT_MIN_OBSERVATIONS)
   parser.add_argument("--fast", action="store_true", help="first seed only, 60 days, 5 population students")
   parser.add_argument("--trace", default=None, help="print every serve that loaded this skill")
   parser.add_argument("--world", choices=WORLDS, default=WORLD_FIXED, help="the hidden student model")
   parser.add_argument("--json", default=None, help="write the raw results here")

   return parser.parse_args(argv)


def main(argv=None):
   args = parse_args(argv)
   days = args.days if args.days is not None else day_count(whole_graph.START_DAY, args.end)
   seeds = list(args.seeds)
   population = args.population

   if args.fast:
      days = min(days, FAST_DAYS)
      seeds = seeds[:1]
      population = min(population, FAST_POPULATION) if population else 0

   checkpoints = [offset for offset in args.checkpoints if offset <= days]
   has_final = days in checkpoints

   if not has_final:
      checkpoints.append(days)

   results = []

   for seed in seeds:
      result = run_one(
         seed, args.ability, days, checkpoints, args.min_observations, trace=args.trace, world=args.world
      )
      results.append(result)
      print(format_run(result))
      print()

   population_results = []

   for index in range(population):
      seed = POPULATION_SEED_BASE + index
      result = run_one(seed, None, days, checkpoints, args.min_observations, world=args.world)
      population_results.append(result)

   if population_results:
      print(format_population(population_results))

   if args.json:
      with open(args.json, "w") as handle:
         json.dump({"ability": results, "population": population_results}, handle, indent=1, default=str)

   return 0


if __name__ == "__main__":
   raise SystemExit(main())
