"""The capped adaptive diagnostic (docs/plan/02, Cold-start diagnostic design and the Diagnostic
mode pseudocode; docs/plan/11 P2 scope item 1).

The posterior is over unit-level states, one categorical distribution per unit over not_started,
partial and fluent, because 30 items cannot resolve 541 skills. An archetype's chance of being
answered under unit state s is the engine's own p_A_knowledge at the start of the run, shifted by
that state's logit offset (constants.DIAG_UNIT_STATE_LOGITS), so the difficulty prior and any
history the student already has both enter, and the run's own answers enter once, through the
posterior. The item asked is the one whose predictive p_A sits nearest 0.5, or whose raw
probability sits nearest 0.625 when it is served as a four-option MCQ; ties inside 0.01 go to a
uniform draw.

Gating is suspended, which is the only place in the engine that does so. Only archetypes with a
published item are candidates (R18); the rest are returned as coverage gaps. One family is asked
at most once, and no unit takes a fifth item while another servable unit is still unprobed. The
run stops at 30 items, or once at least 10 are asked and the summed unit entropy has fallen by no
more than 0.02 bits over the last 3 scored items, or when nothing is left to ask. One item per run,
drawn uniformly from every published archetype, is the held-out extra problem: it is asked and
logged but never enters the posterior.

placement() turns the posterior into skill-level state. A skill is in state when its chance of
being known under its unit's posterior reaches 0.80 and out of state below 0.20 (the ALEKS
thresholds). In-state skills whose gating parents are mastered or also in state are marked
mastered with a first-review memory, so FSRS brings them back for a retrieval check within days
and a credited failure un-masters them as it would any skill. Everything else is left as it was:
an unresolved skill keeps mastered false and sits in the fringe once its parents are mastered.
A re-diagnostic after a long gap runs the same code over the stored state and only ever adds.
"""
import math
from dataclasses import dataclass, field

from app.engine import constants, fsrs
from app.engine.prior import p_knowledge
from app.engine.state import FadingStage, ResponseFormat
from app.engine.strength import sigmoid, strength
from app.engine.update import as_datetime

UNIT_STATES = tuple(name for name, _ in constants.DIAG_UNIT_STATE_LOGITS)
UNIT_STATE_LOGIT = dict(constants.DIAG_UNIT_STATE_LOGITS)
NOT_LEARNED_RATE = dict(constants.DIAG_NOT_LEARNED_RATES)

OUTCOME_CORRECT = "correct"
OUTCOME_INCORRECT = "incorrect"
OUTCOME_NOT_LEARNED = "not_learned"

STOP_CAP = "cap"
STOP_ENTROPY = "entropy_stalled"
STOP_EXHAUSTED = "pool_exhausted"

PLACED_IN = "in_state"
PLACED_OUT = "out_of_state"
UNRESOLVED = "unresolved"

FIRST_REVIEW_GRADE = 3

PROBABILITY_FLOOR = 1e-6


def logit(probability_value):
   bounded = min(max(probability_value, PROBABILITY_FLOOR), 1.0 - PROBABILITY_FLOOR)

   return math.log(bounded / (1.0 - bounded))


def entropy_bits(distribution):
   return -sum(value * math.log2(value) for value in distribution if value > 0.0)


def raw_from_knowledge(knowledge, response_format):
   is_mcq = ResponseFormat(response_format) == ResponseFormat.MCQ

   if is_mcq:
      return constants.MCQ_GUESS_FLOOR + constants.MCQ_SUCCESS_CREDIT * knowledge

   return knowledge


def target_for(response_format):
   is_mcq = ResponseFormat(response_format) == ResponseFormat.MCQ

   return constants.TARGET_DIAG_MCQ if is_mcq else constants.TARGET_DIAG_FR


def uniform_distribution():
   share = 1.0 / len(UNIT_STATES)

   return [share for _ in UNIT_STATES]


@dataclass
class DiagnosticRun:
   units: list
   posterior: dict
   baseline: dict
   held_out_position: int | None
   response_format: str = ResponseFormat.SHORT_ANSWER.value
   asked: list = field(default_factory=list)
   entropy_trace: list = field(default_factory=list)
   coverage_gaps: list = field(default_factory=list)
   unprobeable_units: list = field(default_factory=list)
   stop_reason: str | None = None
   placement: dict | None = None

   def as_dict(self):
      return {
         "units": list(self.units),
         "posterior": {unit: list(values) for unit, values in self.posterior.items()},
         "baseline": dict(self.baseline),
         "held_out_position": self.held_out_position,
         "response_format": self.response_format,
         "asked": [dict(entry) for entry in self.asked],
         "entropy_trace": list(self.entropy_trace),
         "coverage_gaps": list(self.coverage_gaps),
         "unprobeable_units": list(self.unprobeable_units),
         "stop_reason": self.stop_reason,
         "placement": self.placement,
      }

   @classmethod
   def from_dict(cls, payload):
      return cls(
         units=list(payload["units"]),
         posterior={unit: list(values) for unit, values in payload["posterior"].items()},
         baseline=dict(payload["baseline"]),
         held_out_position=payload["held_out_position"],
         response_format=payload.get("response_format", ResponseFormat.SHORT_ANSWER.value),
         asked=[dict(entry) for entry in payload.get("asked", [])],
         entropy_trace=list(payload.get("entropy_trace", [])),
         coverage_gaps=list(payload.get("coverage_gaps", [])),
         unprobeable_units=list(payload.get("unprobeable_units", [])),
         stop_reason=payload.get("stop_reason"),
         placement=payload.get("placement"),
      )

   @property
   def is_finished(self):
      return self.stop_reason is not None

   @property
   def scored(self):
      return [entry for entry in self.asked if not entry["held_out"]]

   @property
   def has_held_out(self):
      return any(entry["held_out"] for entry in self.asked)

   @property
   def pending(self):
      """The asked entry still waiting for its answer, if any."""
      for entry in self.asked:
         if entry.get("outcome") is None:
            return entry

      return None

   def total_entropy(self):
      return sum(entropy_bits(self.posterior[unit]) for unit in self.units)


def graph_units(graph):
   return sorted({record["unit"] for record in graph.skills.values() if record.get("unit")})


def published_archetypes(graph, bank):
   return [
      record
      for archetype_id, record in sorted(graph.archetypes.items())
      if bank.has_published_item(archetype_id)
   ]


def start_run(states, graph, bank, retrievability, rng, response_format=ResponseFormat.SHORT_ANSWER):
   """A run over the stored state as it stands: a first login and a long-gap return differ only
   in what that state already holds."""
   units = graph_units(graph)
   servable = published_archetypes(graph, bank)
   baseline = {
      record["id"]: p_knowledge(record, states, graph.hard_parents, retrievability)
      for record in servable
   }
   coverage_gaps = sorted(
      archetype_id
      for archetype_id in graph.archetypes
      if not bank.has_published_item(archetype_id)
   )
   probed_units = {record["primary_unit"] for record in servable}
   unprobeable = [unit for unit in units if unit not in probed_units]
   has_pool = len(servable) > 0
   held_out_position = rng.randrange(min(constants.DIAG_MIN, len(servable))) if has_pool else None
   run = DiagnosticRun(
      units=units,
      posterior={unit: uniform_distribution() for unit in units},
      baseline=baseline,
      held_out_position=held_out_position,
      response_format=ResponseFormat(response_format).value,
      coverage_gaps=coverage_gaps,
      unprobeable_units=unprobeable,
   )
   run.entropy_trace.append(run.total_entropy())

   return run


def likelihood_known(baseline_knowledge, unit_state):
   return sigmoid(logit(baseline_knowledge) + UNIT_STATE_LOGIT[unit_state])


def predictive_knowledge(run, record):
   """p_A for the diagnostic: the chance the archetype is known, averaged over its unit's posterior."""
   baseline_knowledge = run.baseline[record["id"]]
   distribution = run.posterior[record["primary_unit"]]

   return sum(
      weight * likelihood_known(baseline_knowledge, unit_state)
      for weight, unit_state in zip(distribution, UNIT_STATES)
   )


def entropy_stalled(run):
   window = constants.DIAG_ENTROPY_WINDOW
   has_window = len(run.entropy_trace) > window

   if not has_window:
      return False

   drop = run.entropy_trace[-window - 1] - run.entropy_trace[-1]

   return drop <= constants.DIAG_ENTROPY_STALL_BITS


def stop_reason_before_next(run):
   asked_count = len(run.asked)

   if asked_count >= constants.DIAG_CAP:
      return STOP_CAP

   past_floor = asked_count >= constants.DIAG_MIN

   if past_floor and entropy_stalled(run):
      return STOP_ENTROPY

   return None


def asked_archetypes(run):
   return {entry["archetype_id"] for entry in run.asked}


def asked_families(run, graph):
   return {graph.family(entry["archetype_id"]) for entry in run.scored}


def unit_counts(run):
   counts = {}

   for entry in run.scored:
      counts[entry["unit"]] = counts.get(entry["unit"], 0) + 1

   return counts


def adaptive_pool(run, graph, bank):
   """Unasked published archetypes from unasked families, pooled by unit, gating suspended."""
   already = asked_archetypes(run)
   families = asked_families(run, graph)
   pool = [
      record
      for record in published_archetypes(graph, bank)
      if record["id"] not in already
      and record["family"] not in families
      and record["calculator_status"] != "calculator"
   ]
   counts = unit_counts(run)
   open_units = {record["primary_unit"] for record in pool}
   unprobed = [unit for unit in open_units if counts.get(unit, 0) == 0]
   every_unit_probed = len(unprobed) == 0

   if every_unit_probed:
      return pool

   return [
      record
      for record in pool
      if counts.get(record["primary_unit"], 0) < constants.DIAG_UNIT_POOL_CAP
   ]


def distance_to_target(run, record):
   knowledge = predictive_knowledge(run, record)
   raw = raw_from_knowledge(knowledge, run.response_format)

   return abs(raw - target_for(run.response_format)), knowledge, raw


def choose_adaptive(run, pool, rng):
   scored = [(distance_to_target(run, record), record) for record in pool]
   best = min(measure[0] for measure, _ in scored)
   ties = [
      (measure, record)
      for measure, record in scored
      if measure[0] <= best + constants.DIAG_TIE_BAND
   ]
   ties.sort(key=lambda pair: pair[1]["id"])
   (_, knowledge, raw), record = ties[rng.randrange(len(ties))]

   return record, knowledge, raw, len(ties)


def choose_held_out(run, graph, bank, rng):
   already = asked_archetypes(run)
   pool = [record for record in published_archetypes(graph, bank) if record["id"] not in already]
   has_pool = len(pool) > 0

   if not has_pool:
      return None

   return pool[rng.randrange(len(pool))]


def next_archetype(run, graph, bank, rng):
   """The archetype to ask next, recorded on the run as pending, or None once the run stops."""
   if run.is_finished:
      return None

   waiting = run.pending

   if waiting is not None:
      return graph.archetypes[waiting["archetype_id"]]

   reason = stop_reason_before_next(run)

   if reason is not None:
      run.stop_reason = reason

      return None

   is_held_out_turn = run.held_out_position == len(run.asked) and not run.has_held_out

   if is_held_out_turn:
      record = choose_held_out(run, graph, bank, rng)

      if record is not None:
         knowledge = predictive_knowledge(run, record)
         run.asked.append(entry_for(run, record, knowledge, held_out=True, ties=1))

         return record

   pool = adaptive_pool(run, graph, bank)
   is_exhausted = len(pool) == 0

   if is_exhausted:
      run.stop_reason = STOP_EXHAUSTED

      return None

   record, knowledge, raw, tie_count = choose_adaptive(run, pool, rng)
   run.asked.append(entry_for(run, record, knowledge, held_out=False, ties=tie_count))

   return record


def entry_for(run, record, knowledge, held_out, ties):
   return {
      "archetype_id": record["id"],
      "unit": record["primary_unit"],
      "family": record["family"],
      "p_a": knowledge,
      "p_raw": raw_from_knowledge(knowledge, run.response_format),
      "target": target_for(run.response_format),
      "held_out": held_out,
      "ties": ties,
      "item_id": None,
      "outcome": None,
   }


def outcome_likelihood(run, record, unit_state, outcome):
   """Three outcomes, because "I have not learned this yet" says more than a wrong answer: of the
   answers that miss, a share NOT_LEARNED_RATE[state] are declared not learned."""
   known = likelihood_known(run.baseline[record["id"]], unit_state)
   p_correct = raw_from_knowledge(known, run.response_format)
   is_correct = outcome == OUTCOME_CORRECT

   if is_correct:
      return p_correct

   declared_share = NOT_LEARNED_RATE[unit_state]
   is_not_learned = outcome == OUTCOME_NOT_LEARNED

   if is_not_learned:
      return (1.0 - p_correct) * declared_share

   return (1.0 - p_correct) * (1.0 - declared_share)


def record_outcome(run, record, outcome, item_id=None):
   """Settle the pending entry. A scored answer updates its unit's posterior; the held-out does not."""
   entry = run.pending
   is_unexpected = entry is None or entry["archetype_id"] != record["id"]

   if is_unexpected:
      raise ValueError(f"{record['id']} is not the diagnostic item waiting for an answer")

   entry["outcome"] = outcome
   entry["item_id"] = item_id

   if entry["held_out"]:
      return run

   unit = record["primary_unit"]
   prior = run.posterior[unit]
   weighted = [
      weight * outcome_likelihood(run, record, unit_state, outcome)
      for weight, unit_state in zip(prior, UNIT_STATES)
   ]
   total = sum(weighted)
   run.posterior[unit] = [value / total for value in weighted]
   run.entropy_trace.append(run.total_entropy())

   return run


def classify_skills(run, states, graph):
   """PLACED_IN, PLACED_OUT or UNRESOLVED for every teachable skill, from the unit posterior."""
   probed = {entry["unit"] for entry in run.scored}
   classes = {}

   for skill_id, record in graph.skills.items():
      is_inert = skill_id in graph.inert_top
      state = states.get(skill_id)
      unit = record.get("unit")
      is_unprobed = unit not in probed

      if is_inert or state is None or is_unprobed:
         classes[skill_id] = UNRESOLVED
         continue

      base = strength(state)
      known = sum(
         weight * sigmoid(base + UNIT_STATE_LOGIT[unit_state])
         for weight, unit_state in zip(run.posterior[unit], UNIT_STATES)
      )

      if known >= constants.DIAG_IN_STATE:
         classes[skill_id] = PLACED_IN
      elif known <= constants.DIAG_OUT_OF_STATE:
         classes[skill_id] = PLACED_OUT
      else:
         classes[skill_id] = UNRESOLVED

   return classes


def failed_in_run(run, graph):
   failed = set()

   for entry in run.scored:
      is_miss = entry["outcome"] in (OUTCOME_INCORRECT, OUTCOME_NOT_LEARNED)

      if is_miss:
         failed.update(graph.archetypes[entry["archetype_id"]]["skills"])

   return failed


def gating_closed(candidates, states, graph):
   """Drop every candidate whose gating parent is neither mastered nor itself kept, to a fixpoint."""
   kept = set(candidates)
   changed = True

   while changed:
      changed = False

      for skill_id in sorted(kept):
         parents_ready = all(
            parent in kept or (states.get(parent) is not None and states[parent].mastered)
            for parent in graph.gating_parents(skill_id)
         )

         if not parents_ready:
            kept.discard(skill_id)
            changed = True

   return kept


def unit_summary(run):
   """The result screen's unit-level states: the most likely state once it reaches 0.80, else
   unresolved. Never a percentage (08, diagnostic result)."""
   summary = {}
   probed = {entry["unit"] for entry in run.scored}

   for unit in run.units:
      distribution = run.posterior[unit]
      best_index = max(range(len(UNIT_STATES)), key=lambda index: distribution[index])
      is_confident = distribution[best_index] >= constants.DIAG_IN_STATE
      is_probed = unit in probed

      if is_probed and is_confident:
         summary[unit] = UNIT_STATES[best_index]
      elif is_probed:
         summary[unit] = UNRESOLVED
      else:
         summary[unit] = "not_probed"

   return summary


def place(run, states, graph, today):
   """Apply the placement to the stored state, adding mastery only, and record it on the run."""
   classes = classify_skills(run, states, graph)
   failed = failed_in_run(run, graph)
   candidates = [
      skill_id
      for skill_id, placed in classes.items()
      if placed == PLACED_IN and skill_id not in failed
   ]
   kept = gating_closed(candidates, states, graph)
   newly_mastered = []

   for skill_id in sorted(kept):
      state = states[skill_id]

      if state.mastered:
         continue

      state.mastered = True
      state.mastered_at = as_datetime(today)
      state.fading_stage = FadingStage.UNSUPPORTED

      has_no_memory = state.stability is None

      if has_no_memory:
         state.stability = fsrs.initial_stability(FIRST_REVIEW_GRADE)
         state.difficulty = fsrs.initial_difficulty(FIRST_REVIEW_GRADE)
         state.last_practised_at = as_datetime(today)

      newly_mastered.append(skill_id)

   run.placement = {
      "units": unit_summary(run),
      "in_state": sorted(kept),
      "newly_mastered": newly_mastered,
      "out_of_state": sorted(skill_id for skill_id, placed in classes.items() if placed == PLACED_OUT),
      "unresolved_count": sum(1 for placed in classes.values() if placed == UNRESOLVED),
   }

   return run.placement

