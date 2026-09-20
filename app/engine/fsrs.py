"""FSRS-7 as the decay layer only, never as the mastery model (docs/plan/02-adaptive-engine.md).

R28 in docs/plan/11-phased-delivery.md says to copy the forms out of the source rather than out
of the plan text, so every form below is transcribed from the reference implementation:

   repo   https://github.com/open-spaced-repetition/fsrs-rs at commit
          c137ee6e096f9217632397a8fb2bdb6f6e1b92ae (2026-09-18)
   files  src/inference_v7.rs, src/model_v7.rs, src/model.rs, src/parameter_clipper_v7.rs,
          src/training_v7.rs, src/parameter_initialization_fsrs7.rs, src/simulation.rs
   cross  https://github.com/open-spaced-repetition/srs-benchmark at commit
          bd9110f791e5b37282c55a9aa8db35f68f0c4aa2 (2026-09-18), models/fsrs_v7.py and
          models/model_factory.py, the code behind the README's "FSRS-7" row

Shipped FSRS-7 takes 34 parameters (model_v7.rs PARAM_LEN = 34). The 35-entry block still printed
under "Default Parameters" in the srs-benchmark README at bd9110f is a March 2026 draft that the
finished model replaced. The vector lives in fsrs_constants.py with its source pinned by commit
and digest; DEFAULT_PARAMETERS here is that same tuple.

FSRS-7 carries two stabilities, the long-term S and the fast S_fast, and mixes their two recall
curves. P1 stores one stability per skill (SkillState has no fast column), so S_fast is
reconstructed as 0.8 * S, which is what the source's own SM-2 bridge (memory_state_from_sm2)
does when it has to invent a fast stability. S is not the 90 percent interval in FSRS-7: the
curve bases w25 and w26 are trained parameters, not the fixed 0.9 of FSRS-4.5 through FSRS-6.
"""
import math

from app.engine.fsrs_constants import FSRS7_DEFAULT_PARAMETERS

STABILITY_MIN = 0.0001
STABILITY_MAX = 36500.0
DIFFICULTY_MIN = 1.0
DIFFICULTY_MAX = 10.0

FAST_STABILITY_RATIO = 0.8
LONG_BLOCK_BASE = 7
FAST_BLOCK_BASE = 15

GRADE_HARD = 2
GRADE_EASY = 4

DECAY_MIN = 0.01
DECAY_MAX = 0.95
EXPONENT_CAP = 60.0
RETRIEVABILITY_EPSILON = 1e-5

MEAN_REVERSION_WEIGHT = 0.01
DIFFICULTY_DAMPING = 9.0
DIFFICULTY_ANCHOR_GRADE = 4

DEFAULT_PARAMETERS = FSRS7_DEFAULT_PARAMETERS
PARAMETER_COUNT = len(DEFAULT_PARAMETERS)


def clamp(value, lowest, highest):
   return max(lowest, min(highest, value))


def clamp_stability(stability):
   return clamp(stability, STABILITY_MIN, STABILITY_MAX)


def initial_stability(grade, parameters=DEFAULT_PARAMETERS):
   """S0(G) = w[G-1], the first-review stability of fsrs-rs model.rs step()."""
   return clamp_stability(parameters[grade - 1])


def initial_fast_stability(grade, parameters=DEFAULT_PARAMETERS):
   return clamp_stability(FAST_STABILITY_RATIO * initial_stability(grade, parameters))


def difficulty_anchor(parameters=DEFAULT_PARAMETERS):
   """The unclamped D0 at grade 4, the mean-reversion target of next_difficulty."""
   return parameters[4] - math.exp(parameters[5] * (DIFFICULTY_ANCHOR_GRADE - 1)) + 1.0


def initial_difficulty(grade, parameters=DEFAULT_PARAMETERS):
   """D0(G) = w4 - exp(w5 * (G - 1)) + 1, clamped to the 1 to 10 scale for storage."""
   raw = parameters[4] - math.exp(parameters[5] * (grade - 1)) + 1.0

   return clamp(raw, DIFFICULTY_MIN, DIFFICULTY_MAX)


def fast_recall(fast_stability, elapsed_days, parameters=DEFAULT_PARAMETERS):
   """r1, the fast component of the two-component forgetting curve."""
   effective_stability = clamp_stability(fast_stability)
   effective_elapsed = max(elapsed_days, 0.0)

   decay_magnitude = clamp(
      parameters[23] * effective_stability ** (parameters[33] - 0.3), DECAY_MIN, DECAY_MAX
   )
   decay = -decay_magnitude
   factor = math.exp(min(math.log(parameters[25]) / decay, EXPONENT_CAP)) - 1.0

   return (1.0 + factor * effective_elapsed / effective_stability) ** decay


def slow_recall(stability, elapsed_days, difficulty, parameters=DEFAULT_PARAMETERS):
   """r2, the slow component, the only one difficulty modulates."""
   effective_stability = clamp_stability(stability)
   effective_elapsed = max(elapsed_days, 0.0)

   decay = -clamp(parameters[24], DECAY_MIN, DECAY_MAX)
   factor = parameters[26] ** (1.0 / decay) - 1.0
   difficulty_timescale = math.exp((difficulty - 5.0) * (parameters[32] - 0.3))

   return (
      1.0 + factor * difficulty_timescale * effective_elapsed / effective_stability
   ) ** decay


def retrievability(
   stability,
   elapsed_days,
   fast_stability=None,
   difficulty=None,
   parameters=DEFAULT_PARAMETERS,
):
   """The mixture R of r1 and r2. A skill with no credited observation has not decayed (R1)."""
   has_no_memory_state = stability is None

   if has_no_memory_state:
      return 1.0

   effective_stability = clamp_stability(stability)
   has_fast = fast_stability is not None
   effective_fast = clamp_stability(
      fast_stability if has_fast else FAST_STABILITY_RATIO * effective_stability
   )
   has_difficulty = difficulty is not None
   effective_difficulty = difficulty if has_difficulty else 5.0

   recall_fast = fast_recall(effective_fast, elapsed_days, parameters)
   recall_slow = slow_recall(effective_stability, elapsed_days, effective_difficulty, parameters)

   weight_fast = parameters[27] * effective_fast ** (-parameters[29])
   weight_slow = (
      parameters[28]
      * effective_stability ** parameters[30]
      * math.exp((effective_difficulty - 5.0) * (parameters[31] - 0.5))
   )
   mixed = (weight_fast * recall_fast + weight_slow * recall_slow) / (weight_fast + weight_slow)

   return RETRIEVABILITY_EPSILON + (1.0 - 2.0 * RETRIEVABILITY_EPSILON) * mixed


def post_lapse_stability(stability, recall_probability, parameters, block_base):
   effective_stability = clamp_stability(stability)
   raw = (
      parameters[block_base + 3]
      * ((effective_stability + 1.0) ** parameters[block_base + 4] - 1.0)
      * math.exp((1.0 - recall_probability) * parameters[block_base + 5])
   )

   return min(effective_stability, raw)


def stability_increase(stability, difficulty, recall_probability, grade, parameters, block_base):
   effective_stability = clamp_stability(stability)
   is_hard = grade == GRADE_HARD
   is_easy = grade == GRADE_EASY
   hard_penalty = parameters[block_base + 6] if is_hard else 1.0
   easy_bonus = parameters[block_base + 7] if is_easy else 1.0

   return 1.0 + (
      math.exp(parameters[block_base] - 1.5)
      * (11.0 - difficulty)
      * effective_stability ** (-parameters[block_base + 1])
      * (math.exp((1.0 - recall_probability) * parameters[block_base + 2]) - 1.0)
      * hard_penalty
      * easy_bonus
   )


def next_stability_success(
   stability,
   difficulty,
   recall_probability,
   grade=3,
   parameters=DEFAULT_PARAMETERS,
   block_base=LONG_BLOCK_BASE,
):
   """S' for grade >= 2, floored by what a lapse would have produced."""
   effective_stability = clamp_stability(stability)
   grown = effective_stability * stability_increase(
      effective_stability, difficulty, recall_probability, grade, parameters, block_base
   )
   floor = post_lapse_stability(effective_stability, recall_probability, parameters, block_base)

   return clamp_stability(max(floor, grown))


def next_stability_lapse(
   stability,
   difficulty=None,
   recall_probability=1.0,
   parameters=DEFAULT_PARAMETERS,
   block_base=LONG_BLOCK_BASE,
):
   """S' for grade 1. Difficulty-independent in the finished FSRS-7; the argument is ignored."""
   return clamp_stability(
      post_lapse_stability(stability, recall_probability, parameters, block_base)
   )


def next_difficulty(difficulty, grade, recall_probability=1.0, parameters=DEFAULT_PARAMETERS):
   """Linear damping, surprise weighting on a lapse, then a fixed 1 percent mean reversion."""
   delta = -parameters[6] * (grade - 3)
   is_lapse = grade == 1

   if is_lapse:
      delta = delta * (recall_probability + 0.1)

   damped = difficulty + (10.0 - difficulty) * delta / DIFFICULTY_DAMPING
   reverted = (
      MEAN_REVERSION_WEIGHT * difficulty_anchor(parameters)
      + (1.0 - MEAN_REVERSION_WEIGHT) * damped
   )

   return clamp(reverted, DIFFICULTY_MIN, DIFFICULTY_MAX)
