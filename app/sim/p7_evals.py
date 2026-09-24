"""The P7 policy comparison of docs/plan/10 "Offline simulation of the engine against synthetic
students", over the learning world in app/sim/learning.py, and the decisions its acceptance
thresholds make.

Every arm runs on the same students from the same seeds, so a comparison between two arms is
paired student by student. A threshold that 10 states "on at least 90 percent of simulated
students" is read off those pairs. The numbers are a simulation's measurement on synthetic
students whose world model is invented: they can falsify a policy choice and cannot validate one.
tools/p7_evals.py runs this at the recorded size and writes docs/operator/p7-evals.md.
"""
import statistics
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

from app.sim import learning

SEED_BASE = 20270510
PAIRED_BAR = 0.90
BIAS_MARGIN = 0.05
FALSE_MASTERY_CEILING = 0.05


@dataclass(frozen=True)
class ArmSummary:
   arm: str
   curve: str
   students: int
   items: int
   learned: int
   mean_true_mastery_per_item: float
   mean_retention_day_7: float
   mean_retention_day_30: float
   mean_measurement_bias: float
   declared_mastered: int
   declared_not_known: int
   placed_mastered: int
   placed_not_known: int
   seeded_mastered: int
   seeded_not_known: int

   @property
   def false_mastery_share(self):
      return self.declared_not_known / self.declared_mastered if self.declared_mastered else 0.0

   @property
   def practice_false_mastery_share(self):
      """False declarations among skills declared from practice, with the diagnostic's placement
      and the seeded parents of app/session/seed.py set aside."""
      practised = self.declared_mastered - self.placed_mastered - self.seeded_mastered
      wrong = self.declared_not_known - self.placed_not_known - self.seeded_not_known

      return wrong / practised if practised else 0.0


def _run(job):
   arm_name, seed, days, curve = job

   return learning.run_student(learning.ARMS[arm_name], seed, days, curve, keep_trace=True)


def run_arms(arm_names, students, days, curve=learning.EXPONENTIAL, seed_base=SEED_BASE, workers=1):
   """Maps arm name to its list of StudentRun, in seed order."""
   jobs = [
      (arm_name, seed_base + index, days, curve)
      for arm_name in arm_names
      for index in range(students)
   ]
   use_pool = workers > 1

   if use_pool:
      with ProcessPoolExecutor(max_workers=workers) as pool:
         results = list(pool.map(_run, jobs, chunksize=4))
   else:
      results = [_run(job) for job in jobs]

   by_arm = {arm_name: [] for arm_name in arm_names}

   for result in results:
      by_arm[result.arm].append(result)

   return by_arm


def summarise(runs):
   first = runs[0]

   return ArmSummary(
      arm=first.arm,
      curve=first.curve,
      students=len(runs),
      items=sum(run.items for run in runs),
      learned=sum(run.learned for run in runs),
      mean_true_mastery_per_item=statistics.mean(run.true_mastery_per_item for run in runs),
      mean_retention_day_7=statistics.mean(run.retention_day_7 for run in runs),
      mean_retention_day_30=statistics.mean(run.retention_day_30 for run in runs),
      mean_measurement_bias=statistics.mean(run.measurement_bias for run in runs),
      declared_mastered=sum(run.declared_mastered for run in runs),
      declared_not_known=sum(run.declared_not_known for run in runs),
      placed_mastered=sum(run.placed_mastered for run in runs),
      placed_not_known=sum(run.placed_not_known for run in runs),
      seeded_mastered=sum(run.seeded_mastered for run in runs),
      seeded_not_known=sum(run.seeded_not_known for run in runs),
   )


def paired_share(challenger_runs, incumbent_runs, measure, strict=True):
   """The share of students on whom the challenger's measure beats the incumbent's (strict) or at
   least matches it (not strict). The runs must be the same students in the same order."""
   pairs = list(zip(challenger_runs, incumbent_runs))

   for challenger, incumbent in pairs:
      assert challenger.seed == incumbent.seed, "paired runs must share a seed"

   if strict:
      wins = sum(1 for challenger, incumbent in pairs if measure(challenger) > measure(incumbent))
   else:
      wins = sum(1 for challenger, incumbent in pairs if measure(challenger) >= measure(incumbent))

   return wins / len(pairs)


def served_identically(runs, other_runs):
   """True when two arms served every student the same items with the same outcomes. Needs the
   runs' traces, so run_arms keeps them."""
   return all(run.trace == other.trace for run, other in zip(runs, other_runs))


def mastery_per_item(run):
   return run.true_mastery_per_item


def retention_day_30(run):
   return run.retention_day_30


@dataclass(frozen=True)
class GateDecisions:
   policy_at_least_random_share: float
   policy_beats_random: bool
   five_term_beats_two_term_share: float
   five_term_on: bool
   lambda_mastery_share: float
   lambda_retention_share: float
   lambda_returns: bool
   interleaving_removal_retention_gain: float
   interleaving_removal_retention_share: float
   interleaving_costs_retention: bool
   policy_bias: float
   control_bias: float
   bias_within_margin: bool
   worst_false_mastery_share: float
   worst_false_mastery_arm: str
   false_mastery_within_ceiling: bool
   worst_practice_false_mastery_share: float


def decide(by_arm):
   """10's acceptance thresholds, each stated relative to another arm on the same students."""
   two_term = by_arm["two_term"]
   control = by_arm["random_control"]
   five = by_arm["five_term"]
   decay = by_arm["decay_lambda_2"]
   no_interleaving = by_arm["no_interleaving"]

   policy_share = paired_share(two_term, control, mastery_per_item, strict=False)
   five_share = paired_share(five, two_term, mastery_per_item)
   lambda_mastery = paired_share(decay, two_term, mastery_per_item)
   lambda_retention = paired_share(decay, two_term, retention_day_30)
   interleaving_share = paired_share(no_interleaving, two_term, retention_day_30)

   retention_gain = (
      statistics.mean(run.retention_day_30 for run in no_interleaving)
      - statistics.mean(run.retention_day_30 for run in two_term)
   )

   policy_bias = statistics.mean(run.measurement_bias for run in two_term)
   control_bias = statistics.mean(run.measurement_bias for run in control)
   bias_gap = abs(policy_bias) - abs(control_bias)

   false_shares = {arm_name: summarise(runs).false_mastery_share for arm_name, runs in by_arm.items()}
   worst_arm = max(sorted(false_shares), key=lambda arm_name: false_shares[arm_name])
   practice_shares = [summarise(runs).practice_false_mastery_share for runs in by_arm.values()]

   return GateDecisions(
      policy_at_least_random_share=policy_share,
      policy_beats_random=policy_share >= PAIRED_BAR,
      five_term_beats_two_term_share=five_share,
      five_term_on=five_share >= PAIRED_BAR,
      lambda_mastery_share=lambda_mastery,
      lambda_retention_share=lambda_retention,
      lambda_returns=lambda_mastery >= PAIRED_BAR or lambda_retention >= PAIRED_BAR,
      interleaving_removal_retention_gain=retention_gain,
      interleaving_removal_retention_share=interleaving_share,
      interleaving_costs_retention=interleaving_share >= PAIRED_BAR,
      policy_bias=policy_bias,
      control_bias=control_bias,
      bias_within_margin=bias_gap <= BIAS_MARGIN,
      worst_false_mastery_share=false_shares[worst_arm],
      worst_false_mastery_arm=worst_arm,
      false_mastery_within_ceiling=false_shares[worst_arm] <= FALSE_MASTERY_CEILING,
      worst_practice_false_mastery_share=max(practice_shares),
   )
