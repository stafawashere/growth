"""Can the learning world tell selection policies apart? The controls, the noise floor and the
intervals behind docs/operator/selection-study.md.

A positive control reads the hidden world, which no policy can, and serves what the world says is
best; a negative control serves what it says is worst. If neither separates from the random
control, the simulator cannot measure selection, and a policy comparison on it says nothing. The
noise floor runs one policy against itself with only the engine's draws reseeded, so the share of
students on whom "two-term beats two-term" is what chance alone gives the paired bar.

The controls act in block 2 only, through the same ordering hook as the five-term score; blocks
1 and 3 run the shipped policy in every arm. Every number is a simulation's.
"""
import math
import statistics
from concurrent.futures import ProcessPoolExecutor

from app.sim import five_term, learning, today_policies

ENGINE_SEED_SHIFT = 7_777_777
WILSON_Z = 1.96


def known_retention(record, world, today):
   values = [
      world.retention(skill_id, today)
      for skill_id in record["skills"]
      if world.knows(skill_id)
   ]

   return min(values) if values else None


def shuffled(records, rng):
   pool = sorted(records, key=lambda record: record["id"])
   rng.shuffle(pool)

   return pool


def most_forgetting_ordering(world):
   """The positive control of the brief: the candidate that reaches the student's truly
   most-forgetting known skill first, candidates reaching no known skill last."""

   def ordering(records, states, graph, today, retrievability, rng, history):
      pool = shuffled(records, rng)

      def key(record):
         lowest = known_retention(record, world, today)
         reaches_nothing = lowest is None

         return (reaches_nothing, 1.0 if reaches_nothing else lowest)

      return sorted(pool, key=key)

   return ordering


def teaching_ordering(world):
   """A second positive control, aimed at what true mastery per item counts: the candidate whose
   loaded skills the student is ready to learn at the highest summed learning rate."""

   def ordering(records, states, graph, today, retrievability, rng, history):
      pool = shuffled(records, rng)

      def teachable(record):
         return sum(
            world.student.learning_rate.get(skill_id, learning.LEARNING_RATE_LOW)
            for skill_id in record["skills"]
            if world.ready_to_learn(skill_id)
         )

      return sorted(pool, key=lambda record: -teachable(record))

   return ordering


def most_recent_ordering(world):
   """The negative control: the candidate loading the skill the student most recently learned,
   candidates loading nothing learned in the run last."""

   def ordering(records, states, graph, today, retrievability, rng, history):
      pool = shuffled(records, rng)

      def key(record):
         dates = [
            world.learned[skill_id]
            for skill_id in record["skills"]
            if skill_id in world.learned
         ]
         has_learned = len(dates) > 0

         if not has_learned:
            return (1, 0)

         return (0, -max(dates).toordinal())

      return sorted(pool, key=key)

   return ordering


STUDY_ARMS = {
   "oracle_forgetting": learning.Arm("oracle_forgetting", world_ordering=most_forgetting_ordering),
   "oracle_teaching": learning.Arm("oracle_teaching", world_ordering=teaching_ordering),
   "most_recent": learning.Arm("most_recent", world_ordering=most_recent_ordering),
   "five_term_lambda_2": learning.Arm(
      "five_term_lambda_2",
      ordering=five_term.five_term_ordering,
      overrides=(("LAMBDA", 2.0),),
   ),
}


def wilson_interval(successes, total, z=WILSON_Z):
   if total == 0:
      return (0.0, 1.0)

   share = successes / total
   denominator = 1.0 + z * z / total
   centre = (share + z * z / (2 * total)) / denominator
   half_width = z * math.sqrt(share * (1 - share) / total + z * z / (4 * total * total)) / denominator

   return (max(0.0, centre - half_width), min(1.0, centre + half_width))


def mean_interval(values, z=WILSON_Z):
   """The mean and its normal-approximation interval."""
   mean = statistics.mean(values)
   has_spread = len(values) > 1

   if not has_spread:
      return mean, (mean, mean)

   half_width = z * statistics.stdev(values) / math.sqrt(len(values))

   return mean, (mean - half_width, mean + half_width)


def paired_counts(challenger_runs, incumbent_runs, measure):
   """Wins, ties and losses of the challenger, student by student on shared seeds."""
   wins = ties = losses = 0

   for challenger, incumbent in zip(challenger_runs, incumbent_runs):
      assert challenger.seed == incumbent.seed, "paired runs must share a seed"
      difference = measure(challenger) - measure(incumbent)

      if difference > 0:
         wins += 1
      elif difference < 0:
         losses += 1
      else:
         ties += 1

   return wins, ties, losses


def paired_differences(challenger_runs, incumbent_runs, measure):
   return [
      measure(challenger) - measure(incumbent)
      for challenger, incumbent in zip(challenger_runs, incumbent_runs)
   ]


ALL_ARMS = {**learning.ARMS, **STUDY_ARMS, **today_policies.TODAY_ARMS}
WORLDS = {
   "fixed": learning.WORLD,
   "legacy": learning.LEGACY_WORLD,
   "legacy_keyed": learning.WorldRules(keyed_draws=True, consolidated_prior=False, daily_growth=False),
}


def run_job(job):
   """One student in one arm. reseeded runs the engine on a shifted seed, for the noise floor."""
   arm_name, seed, days, curve, world_name, reseeded = job
   engine_seed = seed + ENGINE_SEED_SHIFT if reseeded else None

   return learning.run_student(
      ALL_ARMS[arm_name],
      seed,
      days,
      curve,
      keep_trace=True,
      world_rules=WORLDS[world_name],
      engine_seed=engine_seed,
   )


def run_grid(arm_names, seeds, days, curve, world_name, workers=1, reseeded_arms=()):
   """Maps each arm name (a reseeded arm gets the suffix "_reseeded") to its runs in seed order."""
   jobs = [
      (arm_name, seed, days, curve, world_name, False)
      for arm_name in arm_names
      for seed in seeds
   ]
   jobs += [
      (arm_name, seed, days, curve, world_name, True)
      for arm_name in reseeded_arms
      for seed in seeds
   ]
   use_pool = workers > 1

   if use_pool:
      with ProcessPoolExecutor(max_workers=workers) as pool:
         results = list(pool.map(run_job, jobs, chunksize=2))
   else:
      results = [run_job(job) for job in jobs]

   by_arm = {}

   for job, result in zip(jobs, results):
      arm_name, _, _, _, _, reseeded = job
      key = f"{arm_name}_reseeded" if reseeded else arm_name
      by_arm.setdefault(key, []).append(result)

   return by_arm
