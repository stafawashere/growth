"""Four-block session assembly (docs/plan/02-adaptive-engine.md, Session assembly, R5).

Block 1 due reviews, block 2 fringe learning, block 3 interleaved mixed review, block 4 the
calibration and error-note list. The minute forecast is an assembly input only, never a target.
In a learning session block 2 opens with the productive-failure opener when one is due (02,
Session assembly; 01, Productive-failure openers), which the operator brought into scope on
2026-09-28 in place of R35's deferral. The other callers, home's queue preview and the
simulations, do not ask for it, so they neither place an opener nor set the flag.

The pending-probe queue is handed to block 2 alone, which is where 11-phased-delivery.md test 15
puts the served probe. The drain path inside next_item_review stays wired for review-mode sessions.

Block 2's fail-closed coverage gaps (R18, docs/plan/06-architecture.md traceability row for the
job worker) are recorded twice: in the session's queue payload, which sessions.service already
writes, and in audit_log, naming the skill left unserved and the reason, which the queue payload
alone does not give an operator a durable, queryable record of. The write reuses app.auth.service's
write_audit rather than a second audit writer, and is a no-op when no db is supplied, so a caller
that only wants the in-memory Session, such as the engine unit tests and home's queue preview in
app/session/preview.py, writes nothing.
"""
import json
import statistics
from dataclasses import dataclass, field
from datetime import date, timedelta

from sqlalchemy import select

from app.auth.service import write_audit
from app.db import models
from app.engine import constants
from app.engine.fringe import covered_due_skills, gated_records, outer_fringe, retrieval_eligible
from app.engine.interleave import window_filter
from app.engine.select import (
   DEFAULT_RULES,
   dress_item,
   due_skills,
   filter_interleaving,
   hypercorrection_skills,
   next_item_learning,
   next_item_retrieval,
   next_item_review,
   pick_named_item,
   requires_choice,
   retrievability_map,
   review_eligible,
   session_now,
)
from app.engine.state import Confidence
from app.lessons import constants as lesson_constants
from app.lessons import gate, refresh
from app.lessons.plan import FIRST_CONTACT, plan_lesson

COVERAGE_GAP_ACTION = "coverage_gap_fail_closed"

OPENER_GAP_ACTION = "opener_gap_fail_open"

ITEM_KIND = "item"
LESSON_KIND = "lesson"
READING_KINDS = ("lesson", "refresher")
EXAMPLE_FIRST = "example_first"
LESSON_COUNT = "lesson_count"
READING_SHARE = "reading_share"
BLOCK_MINUTES = "block_minutes"


@dataclass
class Session:
   block1: list = field(default_factory=list)
   block2: list = field(default_factory=list)
   block3: list = field(default_factory=list)
   block4: list = field(default_factory=list)
   served: list = field(default_factory=list)
   requeued: list = field(default_factory=list)
   coverage_gaps: tuple = ()
   forecasts: dict = field(default_factory=dict)
   due_queue: "DueQueue | None" = None
   shortfalls: list = field(default_factory=list)
   unit_counts: dict = field(default_factory=dict)
   opener_concepts: list = field(default_factory=list)
   opener_gaps: list = field(default_factory=list)
   lessons: list = field(default_factory=list)
   lesson_minutes: float = 0.0
   lesson_deferrals: list = field(default_factory=list)

   @property
   def blocks(self):
      return [self.block1, self.block2, self.block3, self.block4]

   @property
   def is_empty(self):
      return all(len(block) == 0 for block in self.blocks)

   def forecast(self, item):
      return self.forecasts.get(item["archetype_id"], constants.FORECAST_DEFAULT_MINUTES)

   @property
   def forecast_total(self):
      """11-phased-delivery.md Q9: the sum of the per-archetype forecast over every served item,
      plus the lesson and refresher minutes (15, Session assembly)."""
      return sum(self.forecast(item) for item in self.served) + self.lesson_minutes

   @property
   def first_contact_count(self):
      return sum(1 for entry in self.lessons if entry["kind"] == LESSON_KIND)

   @property
   def refresher_count(self):
      return sum(1 for entry in self.lessons if entry["kind"] == refresh.REFRESHER)


def forecast_minutes(archetype_id, attempts_history):
   times = [
      attempt["minutes"]
      for attempt in attempts_history
      if attempt.get("archetype_id") == archetype_id and attempt.get("minutes") is not None
   ]
   has_enough = len(times) >= constants.FORECAST_MIN_ATTEMPTS

   if not has_enough:
      return constants.FORECAST_DEFAULT_MINUTES

   return statistics.median(times)


def recently_served(attempts_history, today):
   window = timedelta(days=constants.REPEAT_WINDOW_DAYS)
   recent = set()
   corrected = set()

   for attempt in attempts_history:
      attempted_on = attempt.get("attempted_on")
      item_id = attempt.get("item_id")
      has_date = attempted_on is not None and item_id is not None

      if not has_date:
         continue

      is_recent = today - attempted_on <= window

      if is_recent:
         recent.add(item_id)

      if attempt.get("corrected"):
         corrected.add(item_id)

   return recent, corrected


@dataclass(frozen=True)
class OpenCorrection:
   """The latest correction of an item that no later retry has retired."""

   item_id: str
   archetype_id: str | None
   corrected_on: date
   confidence: str | None
   attempt_id: str | None

   @property
   def was_confident(self):
      return self.confidence == Confidence.CONFIDENT.value


def open_corrections(attempts_history):
   corrected = {}
   retried_on = {}

   for attempt in attempts_history:
      attempted_on = attempt.get("attempted_on")
      item_id = attempt.get("item_id")
      has_date = attempted_on is not None and item_id is not None

      if not has_date:
         continue

      is_correction = bool(attempt.get("corrected"))

      if is_correction:
         previous = corrected.get(item_id)
         is_later = previous is None or attempted_on > previous.corrected_on

         if is_later:
            corrected[item_id] = OpenCorrection(
               item_id=item_id,
               archetype_id=attempt.get("archetype_id"),
               corrected_on=attempted_on,
               confidence=attempt.get("confidence"),
               attempt_id=attempt.get("attempt_id"),
            )
      else:
         previous_retry = retried_on.get(item_id)
         is_later_retry = previous_retry is None or attempted_on > previous_retry

         if is_later_retry:
            retried_on[item_id] = attempted_on

   still_open = []

   for correction in corrected.values():
      last_retry = retried_on.get(correction.item_id)
      was_retried = last_retry is not None and last_retry > correction.corrected_on

      if not was_retried:
         still_open.append(correction)

   return still_open


def lane_order(correction):
   """The hypercorrection lane first (08, Review: high-confidence errors are "served first"),
   then by the day of the correction."""
   return (not correction.was_confident, correction.corrected_on, correction.item_id)


def requeue_pending(attempts_history, today):
   """Every open correction whose R5 window has not yet closed, including one made today whose
   window opens later, in the order block 1 serves them. The review screen lists these."""
   pending = []

   for correction in open_corrections(attempts_history):
      waited_days = (today - correction.corrected_on).days
      window_is_open_or_ahead = 0 <= waited_days <= constants.REQUEUE_GAP_DAYS_MAX
      is_known = correction.archetype_id is not None
      is_pending = window_is_open_or_ahead and is_known

      if is_pending:
         pending.append(correction)

   return sorted(pending, key=lane_order)


def requeue_ready(attempts_history, today):
   """R5: a corrected item comes back through block 1 once the REQUEUE gap has elapsed.

   The latest correction of an item opens a window from REQUEUE_GAP_DAYS_MIN to
   REQUEUE_GAP_DAYS_MAX days after it. Inside the window the item is served ahead of the FSRS
   order; a retry of the item after the correction, or the window closing, retires the requeue.
   A correction the student had rated confident is a hypercorrection and goes ahead of the rest.
   """
   ready = []

   for correction in requeue_pending(attempts_history, today):
      waited_days = (today - correction.corrected_on).days
      in_window = waited_days >= constants.REQUEUE_GAP_DAYS_MIN

      if in_window:
         ready.append((correction.item_id, correction.archetype_id))

   return ready


@dataclass(frozen=True)
class DueQueue:
   """Today's due reviews in full, of which block 1 serves the first 5 items or 5 minutes.

   skills are the mastered skills below the retention target. archetypes is a greedy cover of
   them under repetition compression, and uncovered_skills the due skills no eligible archetype
   reaches, left unserved rather than served from an unpublished row (R18). requeued are the
   corrected items whose R5 window is open. hypercorrection_skills are the skills whose
   hypercorrection date has come, which block 1 serves ahead of the FSRS order, and
   hypercorrection_archetypes the archetypes loading them directly that would serve them. minutes
   is the forecast over every archetype and requeued item in the queue.
   """
   skills: tuple
   archetypes: tuple
   uncovered_skills: tuple
   requeued: tuple
   minutes: float
   hypercorrection_skills: tuple = ()
   hypercorrection_archetypes: tuple = ()

   @property
   def item_count(self):
      return len(self.hypercorrection_archetypes) + len(self.archetypes) + len(self.requeued)


def greedy_cover(targets, candidates, covered_by):
   """Pick, each round, the candidate retiring the most still-uncovered targets.

   Every round removes one archetype from a finite candidate list, so the cover ends. Ties go to
   the lowest archetype id, because this is an estimate of the queue and not the served draw.
   """
   remaining = set(targets)
   pool = sorted(candidates, key=lambda record: record["id"])
   chosen = []

   while remaining and pool:
      scored = [(len(covered_by(record) & remaining), record) for record in pool]
      best_cover, best = max(scored, key=lambda pair: pair[0])
      covers_nothing = best_cover == 0

      if covers_nothing:
         break

      chosen.append(best["id"])
      remaining -= covered_by(best)
      pool = [record for record in pool if record["id"] != best["id"]]

   return chosen, remaining


def compression_cover(due, states, graph, bank, today, retrievability):
   """Repetition compression: an archetype retires its due loaded skills and due 1-hop hard
   ancestors."""
   candidates = review_eligible(due, states, graph, bank, retrievability=retrievability)

   def covered_by(record):
      return covered_due_skills(record, states, graph, today, retrievability)

   return greedy_cover(due, candidates, covered_by)


def hypercorrection_cover(hyper, states, graph, bank):
   """Hypercorrection is served only by archetypes loading the flagged skill directly, with no
   retrieval floor, as next_item_review serves it."""
   candidates = review_eligible(hyper, states, graph, bank, needs_retrieval=False)

   def covered_by(record):
      return set(record["skills"])

   return greedy_cover(hyper, candidates, covered_by)


def is_published_item(bank, item_id, archetype_id):
   return any(item["id"] == item_id for item in bank.published_items(archetype_id))


def due_today_queue(states, graph, bank, attempts_history, today, retrievability=None):
   retrievability = retrievability_map(states, today, retrievability)
   due = due_skills(states, graph, today, retrievability)
   hyper = hypercorrection_skills(states, today)
   chosen, uncovered = compression_cover(due, states, graph, bank, today, retrievability)
   hyper_chosen, _hyper_uncovered = hypercorrection_cover(hyper, states, graph, bank)
   requeued = tuple(
      (item_id, archetype_id)
      for item_id, archetype_id in requeue_ready(attempts_history, today)
      if is_published_item(bank, item_id, archetype_id)
   )
   requeued_archetypes = [archetype_id for _, archetype_id in requeued]
   served_archetypes = list(hyper_chosen) + list(chosen) + requeued_archetypes
   minutes = sum(
      forecast_minutes(archetype_id, attempts_history)
      for archetype_id in served_archetypes
   )

   return DueQueue(
      skills=tuple(sorted(due)),
      archetypes=tuple(chosen),
      uncovered_skills=tuple(sorted(uncovered)),
      requeued=requeued,
      minutes=minutes,
      hypercorrection_skills=tuple(sorted(hyper)),
      hypercorrection_archetypes=tuple(hyper_chosen),
   )


def gap_already_recorded(db, user_id, archetype_id, today):
   return recorded_on_day(db, COVERAGE_GAP_ACTION, user_id, f"archetypes:{archetype_id}", today)


def recorded_on_day(db, action, user_id, subject, today):
   statement = (
      select(models.AuditLog.detail)
      .where(models.AuditLog.action == action)
      .where(models.AuditLog.actor == user_id)
      .where(models.AuditLog.subject == subject)
   )
   day = today.isoformat()

   for detail in db.scalars(statement):
      recorded = json.loads(detail) if detail else {}

      if recorded.get("day") == day:
         return True

   return False


def write_coverage_gap_audit(db, user_id, archetype_ids, graph, today):
   """R18: an archetype excluded from block 2 for want of a published item is named by its
   skill, not just its archetype id, because the skill is what an operator needs to go fill.

   One row per user per archetype per session day, the day being the `today` assembly ran for.
   A row per session opened would grow with every visit and say nothing the day's first row did
   not, while a row per day still shows the operator for how long the gap has stood.

   The row is stamped by write_audit with the wall clock rather than with the engine's session
   clock, which is local midnight of `today` whenever the caller supplies no time.
   """
   for archetype_id in archetype_ids:
      if gap_already_recorded(db, user_id, archetype_id, today):
         continue

      record = graph.archetypes.get(archetype_id)
      skill_id = graph.primary_skill(archetype_id) if record is not None else None
      detail = {
         "archetype_id": archetype_id,
         "skill": skill_id,
         "day": today.isoformat(),
         "reason": "no published item for this fringe archetype",
      }
      write_audit(db, user_id, COVERAGE_GAP_ACTION, f"archetypes:{archetype_id}", detail)


def write_opener_gap_audit(db, user_id, concept_ids, graph, today):
   """The opener fails open: with no published generation item for a due concept, block 2 opens
   with an ordinary item and the flag stays 0. One row per user per concept per assembly day, as
   the coverage gap is recorded, so a gap that stands shows for how long it has stood."""
   for concept_id in concept_ids:
      subject = f"concepts:{concept_id}"

      if recorded_on_day(db, OPENER_GAP_ACTION, user_id, subject, today):
         continue

      detail = {
         "concept_id": concept_id,
         "skills": list(graph.concept_skills.get(concept_id, ())),
         "day": today.isoformat(),
         "reason": "no published item on a BC-DF-13 or BC-DF-15 archetype of this concept",
      }
      write_audit(db, user_id, OPENER_GAP_ACTION, subject, detail)


def openers_due(states, graph, fringe):
   """02 Session assembly: a target concept is due its opener while any of its skills is on the
   fringe and the flag on its first skill is still 0."""
   on_fringe = set(fringe)
   due = []

   for concept_id in constants.PRODUCTIVE_FAILURE_TARGETS:
      skills = graph.concept_skills.get(concept_id, ())
      has_skills = len(skills) > 0

      if not has_skills:
         continue

      first_state = states.get(skills[0])
      has_flag_row = first_state is not None

      if not has_flag_row:
         continue

      already_opened = bool(first_state.concept_opener_done)
      reaches_fringe = any(skill in on_fringe for skill in skills)
      is_due = reaches_fringe and not already_opened

      if is_due:
         due.append(concept_id)

   return due


def is_generation_archetype(record):
   factors = set(record.get("difficulty_factors") or ())

   return len(factors & constants.PRODUCTIVE_FAILURE_FACTORS) > 0


def opener_options(record, bank, excluded_ids):
   """An opener is always short answer, and a statement-keyed item has nothing to type, so it is
   never an opener."""
   options = []

   for item in bank.published_items(record["id"]):
      is_excluded = item["id"] in excluded_ids
      is_typable = not requires_choice(item)

      if is_typable and not is_excluded:
         options.append(item)

   return options


def opener_records(concept_id, states, graph, bank, excluded_ids):
   """Archetypes loading a skill of the concept whose factors make the item a generation task
   (01, Library IDs used), cleared by gating as every learning-mode item is (invariant 3), and
   holding a published short-answer item not served in the repeat window."""
   concept_skills = set(graph.concept_skills.get(concept_id, ()))
   loading = []

   for record in graph.archetypes.values():
      loads_concept = len(concept_skills & set(record["skills"])) > 0
      is_generation = is_generation_archetype(record)

      if loads_concept and is_generation:
         loading.append(record)

   gated = gated_records(loading, states, graph)
   excluded = set(excluded_ids)

   return [record for record in gated if len(opener_options(record, bank, excluded)) > 0]


@dataclass(frozen=True)
class OpenerChoice:
   entry: dict | None
   concept_id: str | None
   gaps: tuple
   shortfalls: tuple


def choose_opener(
   states, graph, bank, rng, excluded_ids, history, user_attempts, retrievability, rules
):
   """The first due concept with a servable generation item gets the opener. A due concept with
   none is a gap; one whose items the interleaving window refuses waits for a later session."""
   gaps = []
   fringe = outer_fringe(states, graph)

   for concept_id in openers_due(states, graph, fringe):
      records = opener_records(concept_id, states, graph, bank, excluded_ids)
      has_records = len(records) > 0

      if not has_records:
         gaps.append(concept_id)
         continue

      allowed, shortfalls = window_filter(records, history, graph, rules)
      window_allows = len(allowed) > 0

      if not window_allows:
         continue

      record = rng.choice(sorted(allowed, key=lambda candidate: candidate["id"]))
      options = opener_options(record, bank, set(excluded_ids))
      item = rng.choice(sorted(options, key=lambda candidate: candidate["id"]))
      entry = dress_item(
         record,
         item,
         states,
         graph,
         user_attempts,
         retrievability=retrievability,
         opener_concept=concept_id,
      )

      return OpenerChoice(entry, concept_id, tuple(gaps), shortfalls)

   return OpenerChoice(None, None, tuple(gaps), ())


def corrected_today(attempts_history, today):
   return [
      attempt["item_id"]
      for attempt in attempts_history
      if attempt.get("corrected") and attempt.get("attempted_on") == today
   ]


def eligible_records(states, graph, bank, unsupported_successes, retrieval_entry=None):
   pool = []

   for archetype_id, record in graph.archetypes.items():
      if not bank.has_published_item(archetype_id):
         continue

      primary = graph.primary_skill(archetype_id)
      state = states.get(primary)

      if state is None:
         continue

      count = None

      if unsupported_successes is not None:
         count = unsupported_successes.get(primary, 0)

      entry = (retrieval_entry or {}).get(primary)

      if retrieval_eligible(state, count, entry):
         pool.append(record)

   return pool


@dataclass
class FirstContact:
   """One block 2 item's lesson decision (15, First-contact target): the entries to place before
   it, or the deferral that sends the lesson to the concept's next item, and the item's link."""

   concept_id: str
   entries: list
   deferral: dict | None
   link: dict | None


class LessonPlacement:
   """The lesson layer inside one assembly. It reads the lesson inputs and the session as it is
   built and never writes a state (15, invariant L0); the service persists what it returns."""

   def __init__(self, session, inputs, states, graph, retrievability):
      self.session = session
      self.inputs = inputs
      self.states = states
      self.graph = graph
      self.retrievability = retrievability
      self.statuses = {
         lesson_id: gate.status_of(inputs.lesson_states, lesson_id) for lesson_id in inputs.lesson_states
      } if inputs is not None else {}
      self.targets = list(inputs.refreshers) if inputs is not None else []
      self.taken = set()
      self.read_again = []

   @property
   def is_active(self):
      return self.inputs is not None

   def reading_fits(self, extra, block2_left):
      """15 condition (d): lesson plus refresher minutes at most LESSON_SHARE_MAX of the forecast.
      While the session is still being built the forecast is projected as block 2 filling its
      budget; trim_to_share re-checks against the forecast actually assembled."""
      reading = self.session.lesson_minutes + extra
      projected = self.session.forecast_total + extra + max(block2_left, 0.0)

      return reading <= lesson_constants.LESSON_SHARE_MAX * projected

   def serves_example_first(self, concept_id, archetype):
      chooser = self.inputs.example_first

      if chooser is None:
         return False

      return bool(chooser(concept_id, archetype))

   def lesson_entry(self, target_id, band, item, prerequisite_ids=()):
      lesson_id, version = self.inputs.servable[target_id]
      body = self.inputs.bodies.get(lesson_id)

      if body is None:
         return None

      plan = plan_lesson(body, band, FIRST_CONTACT, prerequisite_ids=prerequisite_ids)

      return {
         "kind": LESSON_KIND,
         "lesson_id": lesson_id,
         "version": version,
         "band": band,
         "reason": FIRST_CONTACT,
         "concept_id": target_id,
         "before_item_id": item["id"],
         "minutes": gate.lesson_forecast(plan.minutes, self.inputs.completion_ratios),
         "plan": plan.as_dict(),
      }

   def deferral(self, concept_id, band, item, reason):
      lesson_id, version = self.inputs.servable[concept_id]
      deferral = {
         "concept_id": concept_id,
         "lesson_id": lesson_id,
         "version": version,
         "band": band,
         "reason": reason,
         "before_item_id": item["id"],
      }

      return FirstContact(concept_id, [], deferral, {"lesson_id": lesson_id, "version": version})

   def prerequisite_entries(self, flipped, band, item):
      """15 Across concepts: a LSN-PRQ lesson due for a flipped parent goes first. It is due while
      its state is unseen (15, By prerequisite gap)."""
      entries = []

      for prerequisite_id in flipped:
         found = self.inputs.servable.get(prerequisite_id)
         is_due = found is not None and self.statuses.get(found[0]) in (None, gate.UNSEEN)

         if not is_due:
            continue

         entry = self.lesson_entry(prerequisite_id, band, item)

         if entry is not None:
            entries.append(entry)

      return entries

   def first_contact(self, item, assembled):
      concept_id = gate.lesson_target(item, self.states, self.graph, self.statuses, self.inputs.servable)
      has_target = concept_id is not None

      if not has_target:
         return None

      archetype = self.graph.archetypes[item["archetype_id"]]
      band = gate.lesson_band(archetype, self.states, self.graph, self.retrievability)
      lesson_id, version = self.inputs.servable[concept_id]
      is_expert = band == gate.NONE

      if is_expert:
         return FirstContact(concept_id, [], None, {"lesson_id": lesson_id, "version": version})

      is_first_contact = self.statuses.get(lesson_id) in (None, gate.UNSEEN)

      if is_first_contact and self.serves_example_first(concept_id, archetype):
         return self.deferral(concept_id, band, item, EXAMPLE_FIRST)

      flipped = gate.flipped_prerequisites(archetype, self.states)
      entry = self.lesson_entry(concept_id, band, item, prerequisite_ids=tuple(flipped))

      if entry is None:
         return None

      return self.within_caps(concept_id, band, item, entry, flipped, assembled)

   def within_caps(self, concept_id, band, item, entry, flipped, assembled):
      """15 conditions (c) and (d); a LSN-PRQ lesson rides only when the caps hold with it too."""
      count = self.session.first_contact_count
      under_count = count + 1 <= lesson_constants.LESSONS_PER_SESSION_MAX

      if not under_count:
         return self.deferral(concept_id, band, item, LESSON_COUNT)

      block2_left = constants.BLOCK2_MAX_MINUTES - assembled - entry["minutes"]

      if not self.reading_fits(entry["minutes"], block2_left):
         return self.deferral(concept_id, band, item, READING_SHARE)

      entries = [entry]

      for prerequisite in self.prerequisite_entries(flipped, band, item):
         minutes = sum(chosen["minutes"] for chosen in entries) + prerequisite["minutes"]
         fits_count = count + len(entries) + 1 <= lesson_constants.LESSONS_PER_SESSION_MAX
         fits_share = self.reading_fits(minutes, constants.BLOCK2_MAX_MINUTES - assembled - minutes)

         if fits_count and fits_share:
            entries.insert(len(entries) - 1, prerequisite)

      return FirstContact(concept_id, entries, None, None)

   def place(self, block, decision, item):
      """Write the decision into the block and the item; the minutes it adds."""
      if decision is None:
         return 0.0

      if decision.link is not None:
         item["lesson_link"] = dict(decision.link)

      if decision.deferral is not None:
         self.session.lesson_deferrals.append(decision.deferral)
         self.statuses[decision.deferral["lesson_id"]] = gate.DEFERRED

      minutes = 0.0

      for entry in decision.entries:
         block.append(entry)
         self.session.lessons.append(entry)
         self.session.lesson_minutes += entry["minutes"]
         self.statuses[entry["lesson_id"]] = gate.SERVED
         minutes += entry["minutes"]

      has_entries = len(decision.entries) > 0

      if has_entries:
         concept_entry = decision.entries[-1]
         item["preceded_by_lesson_id"] = concept_entry["lesson_id"]
         item["preceded_by_lesson_version"] = concept_entry["version"]

      return minutes

   def refresher_for(self, block_name, item, block2_left):
      if not self.is_active:
         return None

      target = refresh.matching_target(self.targets, item, self.graph, block_name, self.taken)

      if target is None:
         return None

      body = self.inputs.bodies.get(target.lesson_id)

      if body is None:
         return None

      return target, refresh.refresher_entry(target, body, item)

   def place_refresher(self, block, block_name, item, block2_left):
      found = self.refresher_for(block_name, item, block2_left)

      if found is None:
         return 0.0

      target, entry = found

      def reading_fits(extra):
         return self.reading_fits(extra, block2_left - extra)

      is_served = refresh.serve_refresher(block, entry, self.session.refresher_count, reading_fits)

      if not is_served:
         return 0.0

      self.taken.add(target.lesson_id)
      self.session.lessons.append(entry)
      self.session.lesson_minutes += entry["minutes"]

      return entry["minutes"]

   def note_block3(self, item):
      """15 Re-teaching, T2 row: a match in block 3 never cues the criterion item, so it becomes a
      "Read again" link in block 4."""
      if not self.is_active:
         return

      target = refresh.matching_target(self.targets, item, self.graph, "block2", self.taken)

      if target is None:
         return

      self.taken.add(target.lesson_id)
      self.read_again.append(refresh.read_again_entry(target))

   def trim_to_share(self):
      """Invariant L5's share cap on the forecast actually assembled: the last reading entries are
      taken out until it holds, a first-contact lesson becoming a deferral of its item."""
      while self.session.lesson_minutes > lesson_constants.LESSON_SHARE_MAX * self.session.forecast_total:
         has_reading = len(self.session.lessons) > 0

         if not has_reading:
            break

         self.remove_group(self.session.lessons[-1])

   def remove_group(self, last):
      before_item_id = last["before_item_id"]
      group = [
         entry for entry in self.session.lessons
         if entry["before_item_id"] == before_item_id and entry["kind"] == last["kind"]
      ]

      for block in (self.session.block1, self.session.block2):
         block[:] = [entry for entry in block if not any(entry is chosen for chosen in group)]

      self.session.lessons[:] = [entry for entry in self.session.lessons if not any(entry is chosen for chosen in group)]
      self.session.lesson_minutes -= sum(entry["minutes"] for entry in group)
      is_first_contact = last["kind"] == LESSON_KIND

      if not is_first_contact:
         return

      item = next(entry for entry in self.session.block2 if entry.get("id") == before_item_id)
      item.pop("preceded_by_lesson_id", None)
      item.pop("preceded_by_lesson_version", None)
      item["lesson_link"] = {"lesson_id": last["lesson_id"], "version": last["version"]}
      self.session.lesson_deferrals.append({
         "concept_id": last["concept_id"],
         "lesson_id": last["lesson_id"],
         "version": last["version"],
         "band": last["band"],
         "reason": READING_SHARE,
         "before_item_id": before_item_id,
      })


def takes_lessons(item):
   """A probe measures and an opener is a generation attempt, so neither is preceded by a lesson
   (15, Invariants L3; the opener order is L6's, wired where the opener is)."""
   is_probe = item.get("is_probe") is True
   is_opener = item.get("is_opener") is True

   return not is_probe and not is_opener


def assemble_session(
   states,
   graph,
   bank,
   probes,
   attempts_history,
   rng,
   today,
   now=None,
   retrievability=None,
   unsupported_successes=None,
   rules=DEFAULT_RULES,
   db=None,
   user_id=None,
   ordering=None,
   retrieval_entry=None,
   openers=False,
   lessons=None,
):
   """openers places the productive-failure opener in block 2 and sets concept_opener_done on
   the in-memory state of the concept's first skill; the caller persists the flag. Only a learning
   session asks for it (app/session/service.py open_session).

   lessons is a gate.LessonInputs, given only for a learning session (15, condition (e)); None
   serves no lesson and no refresher, which is how every other caller assembles."""
   retrievability = retrievability_map(states, today, retrievability)
   now = session_now(today, now)
   history = []
   session = Session()
   placement = LessonPlacement(session, lessons, states, graph, retrievability)
   session.due_queue = due_today_queue(
      states, graph, bank, attempts_history, today, retrievability
   )
   recent = recently_served(attempts_history, today)[0]
   requeue = requeue_ready(attempts_history, today)
   ready_ids = {item_id for item_id, _ in requeue}
   blocked_later = set(recent)
   blocked_block1 = set(recent) - ready_ids

   def forecast_for(item):
      archetype_id = item["archetype_id"]

      if archetype_id not in session.forecasts:
         session.forecasts[archetype_id] = forecast_minutes(archetype_id, attempts_history)

      return session.forecasts[archetype_id]

   def serve(block, item, shortfalls=()):
      for rule_name in shortfalls:
         session.shortfalls.append({"position": len(session.served), "rule": rule_name})

      if block is session.block2:
         item["kind"] = ITEM_KIND

      block.append(item)
      session.served.append(item)
      history.append(item)
      blocked_later.add(item["id"])
      blocked_block1.add(item["id"])
      counts_toward_quota = block is session.block2 or block is session.block3

      if counts_toward_quota:
         unit = graph.primary_unit(item["archetype_id"])
         session.unit_counts[unit] = session.unit_counts.get(unit, 0) + 1

      return forecast_for(item)

   assembled = 0.0

   def fits(current, item, cap):
      return current + forecast_for(item) <= cap

   pending_requeue = list(requeue)

   def next_requeue_index():
      """R5 keeps the corrected item ahead of the FSRS order, but never past the max-2 rule."""
      for index, (item_id, archetype_id) in enumerate(pending_requeue):
         record = graph.archetypes.get(archetype_id)
         is_served_already = item_id in blocked_block1
         is_unknown = record is None

         if is_served_already or is_unknown:
            continue

         interleaves = len(filter_interleaving([record], history, graph, rules)) > 0

         if interleaves:
            return index

      return None

   while len(session.block1) < constants.BLOCK1_MAX_ITEMS:
      index = next_requeue_index()
      is_requeue_turn = index is not None

      shortfalls = ()

      if is_requeue_turn:
         item_id, archetype_id = pending_requeue.pop(index)
         served = pick_named_item(
            item_id, archetype_id, states, graph, bank, attempts_history, retrievability
         )
         shortfalls = window_filter([graph.archetypes[archetype_id]], history, graph, rules)[1]
      else:
         selection = next_item_review(
            states, graph, bank, None, history, rng, today,
            now=now,
            retrievability=retrievability,
            excluded_ids=blocked_block1,
            user_attempts=attempts_history,
            rules=rules,
         )
         served = selection.item
         shortfalls = selection.shortfalls

      if served is None:
         if is_requeue_turn:
            continue

         break

      if not fits(assembled, served, constants.BLOCK1_MAX_MINUTES):
         break

      placement.place_refresher(session.block1, "block1", served, constants.BLOCK2_MAX_MINUTES)
      assembled += serve(session.block1, served, shortfalls)

      if is_requeue_turn:
         session.requeued.append(served)

   assembled = 0.0
   gaps = ()
   opener_pending = openers

   def place_opener():
      choice = choose_opener(
         states, graph, bank, rng, blocked_later, history, attempts_history, retrievability, rules
      )
      session.opener_gaps.extend(choice.gaps)
      is_placed = choice.entry is not None

      if not is_placed:
         return None

      first_skill = graph.concept_skills[choice.concept_id][0]
      states[first_skill].concept_opener_done = True
      session.opener_concepts.append(choice.concept_id)

      return serve(session.block2, choice.entry, choice.shortfalls)

   while True:
      selection = next_item_learning(
         states, graph, bank, probes, history, rng, today,
         now=now,
         retrievability=retrievability,
         excluded_ids=blocked_later,
         user_attempts=attempts_history,
         rules=rules,
         unit_counts=session.unit_counts,
         ordering=ordering,
      )
      gaps = gaps or selection.coverage_gaps
      is_probe = selection.item is not None and selection.item.get("is_probe") is True
      opens_now = opener_pending and not is_probe

      if opens_now:
         opener_pending = False
         opener_minutes = place_opener()
         was_placed = opener_minutes is not None

         if was_placed:
            assembled += opener_minutes

         reselects = was_placed and selection.item is not None

         if reselects:
            continue

      if selection.item is None:
         break

      if not fits(assembled, selection.item, constants.BLOCK2_MAX_MINUTES):
         break

      item = selection.item
      block2_left = constants.BLOCK2_MAX_MINUTES - assembled - forecast_for(item)
      assembled += placement.place_refresher(session.block2, "block2", item, block2_left)
      decision = None

      if placement.is_active and takes_lessons(item):
         decision = placement.first_contact(item, assembled)

      reading = sum(entry["minutes"] for entry in decision.entries) if decision is not None else 0.0
      overruns_block = reading > 0 and not fits(assembled + reading, item, constants.BLOCK2_MAX_MINUTES)

      if overruns_block:
         decision = placement.deferral(decision.concept_id, decision.entries[-1]["band"], item, BLOCK_MINUTES)

      assembled += placement.place(session.block2, decision, item)
      assembled += serve(session.block2, item, selection.shortfalls)

   session.coverage_gaps = gaps
   has_gaps = len(gaps) > 0
   has_audit_target = db is not None and user_id is not None

   if has_gaps and has_audit_target:
      write_coverage_gap_audit(db, user_id, gaps, graph, today)

   has_opener_gaps = len(session.opener_gaps) > 0

   if has_opener_gaps and has_audit_target:
      write_opener_gap_audit(db, user_id, session.opener_gaps, graph, today)

   pool = eligible_records(states, graph, bank, unsupported_successes, retrieval_entry)
   assembled = 0.0

   while assembled < constants.BLOCK3_MIN_MINUTES:
      selection = next_item_retrieval(
         pool, states, graph, bank, history, rng, today,
         retrievability=retrievability,
         excluded_ids=blocked_later,
         user_attempts=attempts_history,
         rules=rules,
         unit_counts=session.unit_counts,
      )

      if selection.item is None:
         break

      if not fits(assembled, selection.item, constants.BLOCK3_MAX_MINUTES):
         break

      placement.note_block3(selection.item)
      assembled += serve(session.block3, selection.item, selection.shortfalls)

   session.block4 = corrected_today(attempts_history, today) + placement.read_again
   placement.trim_to_share()

   return session
