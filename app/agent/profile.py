"""The per-student tutoring profile and its update discipline (docs/agent/architecture.md, The
self-tuning loop; docs/agent/research/self-tuning.md, The shape of a per-learner tutoring profile,
Failure modes and the control for each, When the profile and the guardrail conflict;
docs/agent/build-plan.md, Slice 7).

The profile changes presentation only. Its fields and bounds are the research table's:

- opening_move per skill kind, one of ask_what_tried, restate_prompt, name_representation,
  point_to_prior_step. A skill kind is the skill's two-digit unit block, the stratum the
  tutor_profile switch balances on, because the library records no other kind for a skill
  [inferred].
- nudge_depth_start, concept_only or rule_named, the first rung of the nudge ladder.
- representation_lead per skill kind, one of AP's graphical, numerical, analytical and verbal,
  mapped from the item's BC-REP code by REPRESENTATION_FAMILY [inferred].
- student_terms, at most 12 {term, concept_id} pairs, each term at most 40 characters of letters,
  digits, spaces, apostrophes and hyphens, free of instruction-shaped words, and each concept_id an
  active BC-CON id. validated_terms drops anything else and repairs nothing.
- turn_length, short or standard, from the band of the student's reply length.
- help_pattern, counts of click-throughs (a student turn under 5 s after the previous one in the
  same conversation), requests before any work (an item whose first tutor move was
  ask_what_tried, because the opening message described no work) and errors without a request.
- stated_requests, the consolidation schema's enum list. Kept so the student sees what was
  recorded, and never rendered to the model.

Every stored body also carries provenance per field (source, evidence_n, updated_at) and
profile_version. The evidence column holds the bookkeeping the rules below need: when each field
last had evidence, when it last moved, when each term and request was last seen, and the count of
clipped values.

compute_profile derives the code fields from agent_turns and attempts, merges the validated
extraction fields of a ConsolidationOutcome, and applies the update discipline. An enum field moves
at most one step a week, and an ordered one (nudge_depth_start, turn_length) one position. Any
field decays to its default 30 days after its last evidence. opening_move moves only once a kind
holds 20 exploratory episodes with an outcome, representation_lead once a kind holds 20 outcomes and
turn_length once 20 student turns sit in the window (the last two floors are [inferred]).
nudge_depth_start has no code signal yet, so it stays at its default. A new tutor_profiles version
is written only when a field's value changed; otherwise the evidence of the current version is
updated in place. While the student has paused memory nothing is computed or written.

opening_move is ranked only from exploratory episodes. A conversation is exploratory when the first
eight hex digits of sha256("<conversation id>:<user id>") are 0 mod 5, recomputed every time and
stored nowhere. In an exploratory conversation the rendered profile carries no opening_move, so the
first move there is the one app/agent/moves.py chooses and not one the profile steered, which is
what keeps the ranking free of the profile's own choices.

The outcome for opening_move and representation_lead is later-day unaided correctness: the next
graded practice attempt on the same archetype, on a later calendar day, with no practice turn
before its submission. Immediate same-item correctness is never an outcome.

Precedence is fixed here and not left to the model. First the guardrail: stated_requests and the
provenance never reach a prompt, and a stored value outside its field's bounds is clipped to the
nearest allowed value and counted. Then the guardrail level from the stage and the format:
clipped_to_guardrail narrows nudge_depth_start to the rungs allowed for the item in front of the
student and counts the clip. Then the profile, only inside what the first two leave.

"Agent-assisted before submission" is computed from agent_turns, not from
attempts.agent_turns_before_submit: before submission no attempts row exists, so that column is
never incremented on the practice path. agent_assisted_arms counts the practice student turns whose
screen names the attempt's session and item and whose created_at precedes the attempt's
submitted_at. The column stays for a later slice that increments it at submission.
"""
import copy
import hashlib
import json
import os
import re
import statistics
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path

from sqlalchemy import select

from app.agent import memory
from app.agent.conversations import AGENT, STUDENT
from app.agent.moves import ASK_WHAT_TRIED, NAME_REPRESENTATION, PRACTICE, RESTATE
from app.auth.service import as_iso
from app.db import models
from app.experiments.switches import skill_unit_block

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONTENT_ROOT = REPOSITORY_ROOT / "data"
CONTENT_ROOT_VARIABLE = "GROWTH_CONTENT_ROOT"
CONCEPT_PREFIX = "BC-CON-"
ACTIVE_STATUS = "active"
DIAGNOSTIC_MODE = "diagnostic"
UNSUPPORTED = "unsupported"
FRQ = "frq"

OPENING_MOVE = "opening_move"
NUDGE_DEPTH_START = "nudge_depth_start"
REPRESENTATION_LEAD = "representation_lead"
STUDENT_TERMS = "student_terms"
TURN_LENGTH = "turn_length"
HELP_PATTERN = "help_pattern"
STATED_REQUESTS = "stated_requests"
PROVENANCE = "provenance"
PROFILE_VERSION = "profile_version"
TUTOR_PROFILE_ARM_KEY = "tutor_profile_arm"
TUTOR_PROFILE_CLIPPED_KEY = "tutor_profile_clipped"

FIELDS = (OPENING_MOVE, NUDGE_DEPTH_START, REPRESENTATION_LEAD, STUDENT_TERMS, TURN_LENGTH, HELP_PATTERN, STATED_REQUESTS)
PER_KIND_FIELDS = (OPENING_MOVE, REPRESENTATION_LEAD)
NEVER_RENDERED = (STATED_REQUESTS,)
RENDERED_FIELDS = tuple(name for name in FIELDS if name not in NEVER_RENDERED)

CODE_SOURCE = "code"
EXTRACTION_SOURCE = "model_extraction"
FIELD_SOURCES = {
   OPENING_MOVE: CODE_SOURCE,
   NUDGE_DEPTH_START: CODE_SOURCE,
   REPRESENTATION_LEAD: CODE_SOURCE,
   STUDENT_TERMS: EXTRACTION_SOURCE,
   TURN_LENGTH: CODE_SOURCE,
   HELP_PATTERN: CODE_SOURCE,
   STATED_REQUESTS: EXTRACTION_SOURCE,
}

OPENING_MOVES = ("ask_what_tried", "restate_prompt", "name_representation", "point_to_prior_step")
DEFAULT_OPENING_MOVE = "ask_what_tried"
OPENING_MOVE_FOR_MOVE = {
   ASK_WHAT_TRIED: "ask_what_tried",
   RESTATE: "restate_prompt",
   NAME_REPRESENTATION: "name_representation",
}

NUDGE_LADDER = ("concept_only", "rule_named", "step_shown", "answer_stated")
PROFILE_RUNGS = NUDGE_LADDER[:2]
EXAM_SHAPED_RUNGS = NUDGE_LADDER[:1]
DEFAULT_NUDGE_DEPTH = "concept_only"

REPRESENTATION_FAMILIES = ("graphical", "numerical", "analytical", "verbal")
REPRESENTATION_FAMILY = {
   "BC-REP-01": "analytical",
   "BC-REP-02": "graphical",
   "BC-REP-03": "numerical",
   "BC-REP-04": "verbal",
   "BC-REP-05": "verbal",
   "BC-REP-06": "analytical",
   "BC-REP-07": "graphical",
   "BC-REP-08": "graphical",
   "BC-REP-09": "numerical",
   "BC-REP-10": "analytical",
   "BC-REP-11": "analytical",
   "BC-REP-12": "analytical",
   "BC-REP-13": "analytical",
   "BC-REP-14": "analytical",
}

TURN_LENGTHS = ("short", "standard")
DEFAULT_TURN_LENGTH = "standard"
SHORT_REPLY_CHARACTERS = 40

HELP_COUNTS = ("click_throughs", "requests_before_work", "errors_without_request")
CLICK_THROUGH_SECONDS = 5

REQUEST_KINDS = (
   "wants_answer",
   "wants_check_of_work",
   "wants_shorter",
   "wants_longer",
   "wants_graph_first",
   "wants_algebra_first",
)

MAX_STUDENT_TERMS = 12
MAX_TERM_CHARACTERS = 40
TERM_CHARACTERS = re.compile(r"[A-Za-z0-9' -]+")
TERM_INSTRUCTION_WORDS = re.compile(
   r"\b(?:answers?|tutor|assistant|prompt|system|reveal|respond|reply|tell|say|instructions?|override)\b",
   re.IGNORECASE,
)
LEADING_ARTICLE = re.compile(r"^the\s+", re.IGNORECASE)

EXPLORATION_SHARE = 5
OPENING_MOVE_EVIDENCE_FLOOR = 20
REPRESENTATION_EVIDENCE_FLOOR = 20
TURN_LENGTH_EVIDENCE_FLOOR = 20
STEP_INTERVAL = timedelta(days=7)
DECAY_AFTER = timedelta(days=30)

DEFAULT_PROFILE = {
   OPENING_MOVE: {},
   NUDGE_DEPTH_START: DEFAULT_NUDGE_DEPTH,
   REPRESENTATION_LEAD: {},
   STUDENT_TERMS: [],
   TURN_LENGTH: DEFAULT_TURN_LENGTH,
   HELP_PATTERN: {name: 0 for name in HELP_COUNTS},
   STATED_REQUESTS: [],
}


def default_profile():
   return copy.deepcopy(DEFAULT_PROFILE)


def parse_moment(stamp):
   return datetime.fromisoformat(stamp) if stamp else None


def is_exploratory(conversation_id, user_id):
   digest = hashlib.sha256(f"{conversation_id}:{user_id}".encode()).hexdigest()

   return int(digest[:8], 16) % EXPLORATION_SHARE == 0


def skill_kind(skill_id):
   return skill_unit_block(skill_id)


@lru_cache(maxsize=4)
def library_concept_ids(content_root):
   registry = json.loads((Path(content_root) / "ids.json").read_text())["ids"]

   return frozenset(
      record_id
      for record_id, record in registry.items()
      if record_id.startswith(CONCEPT_PREFIX) and record.get("status") == ACTIVE_STATUS
   )


def active_concept_ids(library=None):
   """The active BC-CON ids of the loaded snapshot when one is given (a SessionContext or a
   snapshot), else of the library the app is configured with, read from its ids registry."""
   snapshot = getattr(library, "snapshot", library)
   concepts = getattr(snapshot, "concepts", None)

   if concepts:
      return frozenset(concept_id for concept_id in concepts if concept_id.startswith(CONCEPT_PREFIX))

   return library_concept_ids(str(os.environ.get(CONTENT_ROOT_VARIABLE) or DEFAULT_CONTENT_ROOT))


def concept_names(library=None):
   snapshot = getattr(library, "snapshot", library)
   concepts = getattr(snapshot, "concepts", None) or {}

   return {concept_id: record.get("name") for concept_id, record in concepts.items() if record.get("name")}


def is_valid_term(term):
   is_text = isinstance(term, str)

   if not is_text:
      return False

   stripped = term.strip()
   is_sized = 0 < len(stripped) <= MAX_TERM_CHARACTERS
   is_plain = TERM_CHARACTERS.fullmatch(stripped) is not None
   is_instruction_shaped = TERM_INSTRUCTION_WORDS.search(stripped) is not None
   is_screened = is_plain and memory.screen_text(stripped) is None

   return is_sized and is_plain and is_screened and not is_instruction_shaped


def validated_terms(terms, active_ids):
   """The entries that pass every rule, in order, deduplicated by term, at most 12. An entry that
   fails is dropped, never repaired, and no model is called."""
   kept = []
   seen = set()

   for entry in terms if isinstance(terms, list) else []:
      is_mapping = isinstance(entry, dict)
      term = entry.get("term") if is_mapping else None
      concept_id = entry.get("concept_id") if is_mapping else None
      is_active_concept = isinstance(concept_id, str) and concept_id in active_ids
      is_acceptable = is_valid_term(term) and is_active_concept

      if not is_acceptable:
         continue

      stripped = term.strip()
      is_repeat = stripped.lower() in seen

      if is_repeat:
         continue

      seen.add(stripped.lower())
      kept.append({"term": stripped, "concept_id": concept_id})

   return kept[:MAX_STUDENT_TERMS]


def validated_requests(requests):
   kept = []

   for request in requests if isinstance(requests, list) else []:
      is_known = request in REQUEST_KINDS
      is_new = request not in kept

      if is_known and is_new:
         kept.append(request)

   return kept


def clipped_rung(value):
   """A nudge rung inside the profile's rungs, and whether it had to be clipped. A rung past the
   profile's ceiling becomes the ceiling; anything off the ladder becomes the default."""
   if value in PROFILE_RUNGS:
      return value, False

   if value in NUDGE_LADDER:
      return PROFILE_RUNGS[-1], True

   return DEFAULT_NUDGE_DEPTH, True


def normalised(body, active_ids=None):
   """A copy of body with every field inside its bounds, and the count of values clipped or
   dropped to get there. active_ids, when given, also checks every term's concept."""
   source = body if isinstance(body, dict) else {}
   profile = default_profile()
   clips = 0

   for field_name in PER_KIND_FIELDS:
      domain = OPENING_MOVES if field_name == OPENING_MOVE else REPRESENTATION_FAMILIES
      stored = source.get(field_name) if isinstance(source.get(field_name), dict) else {}

      for kind, value in stored.items():
         if value in domain:
            profile[field_name][kind] = value
         else:
            clips += 1

   rung, was_clipped = clipped_rung(source.get(NUDGE_DEPTH_START, DEFAULT_NUDGE_DEPTH))
   profile[NUDGE_DEPTH_START] = rung
   clips += 1 if was_clipped else 0

   turn_length = source.get(TURN_LENGTH, DEFAULT_TURN_LENGTH)
   is_known_length = turn_length in TURN_LENGTHS
   profile[TURN_LENGTH] = turn_length if is_known_length else DEFAULT_TURN_LENGTH
   clips += 0 if is_known_length else 1

   help_pattern = source.get(HELP_PATTERN) if isinstance(source.get(HELP_PATTERN), dict) else {}

   for name in HELP_COUNTS:
      count = help_pattern.get(name, 0)
      is_count = isinstance(count, int) and not isinstance(count, bool) and count >= 0
      profile[HELP_PATTERN][name] = count if is_count else 0

   stored_terms = source.get(STUDENT_TERMS) or []
   checked_ids = active_ids if active_ids is not None else {
      entry.get("concept_id") for entry in stored_terms if isinstance(entry, dict)
   }
   profile[STUDENT_TERMS] = validated_terms(stored_terms, checked_ids)
   clips += len(stored_terms) - len(profile[STUDENT_TERMS]) if isinstance(stored_terms, list) else 0

   stored_requests = source.get(STATED_REQUESTS) or []
   profile[STATED_REQUESTS] = validated_requests(stored_requests)

   return profile, clips


def value_fields(body):
   return {name: body.get(name) for name in FIELDS}


def current_row(db, user_id):
   statement = (
      select(models.TutorProfile)
      .where(models.TutorProfile.user_id == user_id)
      .order_by(models.TutorProfile.version.desc())
      .limit(1)
   )

   return db.scalars(statement).first()


def current_profile(db, user_id):
   """The latest stored body with its provenance, or DEFAULT_PROFILE when none was written."""
   row = current_row(db, user_id)

   if row is None:
      return default_profile()

   profile, _clips = normalised(row.body)
   profile[PROVENANCE] = copy.deepcopy((row.body or {}).get(PROVENANCE) or {})
   profile[PROFILE_VERSION] = row.version

   return profile


def ap_term(name):
   return LEADING_ARTICLE.sub("", name).strip()


def rendered_profile(profile, kind=None, exploratory=False, names=None):
   """The JSON object the prompt carries: every field but stated_requests, without provenance or
   version. With a kind, the per-kind fields give that kind's value. In an exploratory
   conversation opening_move is left out. names maps a concept id to its library name, which is
   added to each term as ap_term so the tutor can say both."""
   body, _clips = normalised(profile)
   names = names or {}
   rendered = {}

   for field_name in RENDERED_FIELDS:
      rendered[field_name] = copy.deepcopy(body[field_name])

   has_kind = kind is not None

   if has_kind:
      rendered[OPENING_MOVE] = body[OPENING_MOVE].get(kind, DEFAULT_OPENING_MOVE)
      rendered[REPRESENTATION_LEAD] = body[REPRESENTATION_LEAD].get(kind)

   if exploratory:
      rendered.pop(OPENING_MOVE)

   for entry in rendered[STUDENT_TERMS]:
      name = names.get(entry["concept_id"])

      if name:
         entry["ap_term"] = ap_term(name)

   return rendered


def allowed_rungs(mode, served_stage, item_format):
   """The rungs the guardrail level leaves for the first nudge: only concept_only during practice
   on an item at stage unsupported or in the free-response format, both rungs otherwise
   [inferred]."""
   is_practice = mode == PRACTICE
   is_exam_shaped = served_stage == UNSUPPORTED or item_format == FRQ
   is_narrowed = is_practice and is_exam_shaped

   return EXAM_SHAPED_RUNGS if is_narrowed else PROFILE_RUNGS


def clipped_to_guardrail(rendered, mode, served_stage, item_format):
   """The rendered profile narrowed to the guardrail level of the item in front of the student,
   and how many values were clipped."""
   clipped = copy.deepcopy(rendered)
   rungs = allowed_rungs(mode, served_stage, item_format)
   rung = clipped.get(NUDGE_DEPTH_START)
   is_outside = rung is not None and rung not in rungs

   if not is_outside:
      return clipped, 0

   clipped[NUDGE_DEPTH_START] = rungs[-1]

   return clipped, 1


def profile_for_prompt(profile, kind, mode, served_stage, item_format, exploratory=False, names=None):
   """The profile the turn's prompt carries, in the fixed precedence: the guardrail's bounds, then
   the guardrail level, then the profile."""
   rendered = rendered_profile(profile, kind=kind, exploratory=exploratory, names=names)

   return clipped_to_guardrail(rendered, mode, served_stage, item_format)


@dataclass(frozen=True)
class AttemptFacts:
   id: str
   session_id: str
   item_id: str
   archetype_id: str
   family: str | None
   kind: str | None
   submitted: datetime
   correct: bool | None

   @property
   def day(self):
      return self.submitted.date()


def attempt_facts(attempt, archetype_id, representation, skills):
   has_encoded_skills = isinstance(skills, str) and skills != ""
   skill_ids = json.loads(skills) if has_encoded_skills else list(skills or [])

   return AttemptFacts(
      id=attempt.id,
      session_id=attempt.session_id,
      item_id=attempt.item_id,
      archetype_id=archetype_id or "",
      family=REPRESENTATION_FAMILY.get(representation),
      kind=skill_kind(skill_ids[0]) if skill_ids else None,
      submitted=parse_moment(attempt.submitted_at),
      correct=None if attempt.correct is None else bool(attempt.correct),
   )


def practice_attempts(db, user_id):
   """The student's submitted attempts in sessions that update mastery, oldest first."""
   rows = db.execute(
      select(models.Attempt, models.Item.archetype_id, models.Item.representation, models.Item.skills, models.Session.mode)
      .join(models.Session, models.Session.id == models.Attempt.session_id)
      .join(models.Item, models.Item.id == models.Attempt.item_id, isouter=True)
      .where(models.Session.user_id == user_id)
      .where(models.Session.updates_mastery == 1)
      .where(models.Attempt.submitted_at.is_not(None))
      .order_by(models.Attempt.submitted_at, models.Attempt.id)
   ).all()
   facts = []

   for attempt, archetype_id, representation, skills, session_mode in rows:
      is_diagnostic = session_mode == DIAGNOSTIC_MODE

      if not is_diagnostic:
         facts.append(attempt_facts(attempt, archetype_id, representation, skills))

   return facts


def user_turns(db, user_id):
   statement = (
      select(models.AgentTurn)
      .where(models.AgentTurn.user_id == user_id)
      .order_by(models.AgentTurn.created_at, models.AgentTurn.id)
   )

   return db.scalars(statement).all()


def turn_slot(turn):
   screen = turn.screen or {}

   return screen.get("session_id"), turn.item_id


def is_practice_student_turn(turn):
   return turn.role == STUDENT and turn.mode == PRACTICE


def practice_turns_by_slot(turns):
   slots = {}

   for turn in turns:
      if is_practice_student_turn(turn):
         arm = (turn.screen or {}).get(TUTOR_PROFILE_ARM_KEY)
         slots.setdefault(turn_slot(turn), []).append((parse_moment(turn.created_at), arm))

   return slots



def assisted_arms_for(attempts, turns):
   slots = practice_turns_by_slot(turns)
   assisted = {}

   for record in attempts:
      before = [arm for moment, arm in slots.get((record.session_id, record.item_id), []) if moment < record.submitted]

      if not before:
         continue

      arms = [arm for arm in before if arm is not None]
      assisted[record.id] = arms[-1] if arms else None

   return assisted


def agent_assisted_arms(db, user_id):
   """Maps every submitted attempt that had a practice turn before its submission to the
   tutor_profile arm those turns recorded, or None when the switch was off for them."""
   return assisted_arms_for(practice_attempts(db, user_id), user_turns(db, user_id))


def agent_assisted_attempt_ids(db, user_id):
   return frozenset(agent_assisted_arms(db, user_id))


def later_unaided_outcome(attempts, index, assisted):
   record = attempts[index]

   for later in attempts[index + 1:]:
      is_same_archetype = later.archetype_id == record.archetype_id
      is_later_day = later.day > record.day
      is_graded = later.correct is not None
      is_unaided = later.id not in assisted
      is_outcome = is_same_archetype and is_later_day and is_graded and is_unaided

      if is_outcome:
         return (1 if later.correct else 0), later.submitted

   return None


def episode_openings(turns):
   """The first practice student turn on each (session, item) and the move of the tutor reply that
   followed it in the same conversation."""
   openings = {}
   pending = {}

   for turn in turns:
      is_opening = is_practice_student_turn(turn) and turn_slot(turn) not in openings

      if is_opening:
         openings[turn_slot(turn)] = {
            "conversation_id": turn.conversation_id,
            "moment": parse_moment(turn.created_at),
            "move": None,
         }
         pending[turn.conversation_id] = turn_slot(turn)
         continue

      is_reply = turn.role == AGENT and turn.conversation_id in pending

      if is_reply:
         openings[pending.pop(turn.conversation_id)]["move"] = turn.move

   return openings


def attempt_for_slot(attempts, slot, moment):
   session_id, item_id = slot

   for record in attempts:
      is_slot = record.session_id == session_id and record.item_id == item_id

      is_after_the_opening = record.submitted > moment

      if is_slot and is_after_the_opening:
         return record

   return None


def ranked_best(counts, current):
   """The value with the highest success rate; a tie that includes the current value keeps it,
   another tie goes to the earlier value in counts' order."""
   rates = {value: successes / trials for value, (trials, successes) in counts.items() if trials > 0}

   if not rates:
      return None

   best_rate = max(rates.values())
   leaders = [value for value, rate in rates.items() if rate == best_rate]

   return current if current in leaders else leaders[0]


def opening_move_evidence(attempts, turns, user_id, assisted):
   """Per kind: counts of (trials, successes) per opening move over exploratory episodes with an
   outcome, the episode count and the latest outcome moment."""
   index_of = {record.id: position for position, record in enumerate(attempts)}
   evidence = {}

   for slot, opening in episode_openings(turns).items():
      opening_move = OPENING_MOVE_FOR_MOVE.get(opening["move"])
      is_counted = opening_move is not None and is_exploratory(opening["conversation_id"], user_id)

      if not is_counted:
         continue

      record = attempt_for_slot(attempts, slot, opening["moment"])
      outcome = later_unaided_outcome(attempts, index_of[record.id], assisted) if record is not None else None

      has_outcome = outcome is not None and record.kind is not None

      if not has_outcome:
         continue

      success, moment = outcome
      entry = evidence.setdefault(record.kind, {"counts": {move: (0, 0) for move in OPENING_MOVES}, "n": 0, "last": moment})
      trials, successes = entry["counts"][opening_move]
      entry["counts"][opening_move] = (trials + 1, successes + success)
      entry["n"] += 1
      entry["last"] = max(entry["last"], moment)

   return evidence


def representation_evidence(attempts, assisted):
   evidence = {}

   for position, record in enumerate(attempts):
      is_assisted = record.id in assisted
      has_family = record.family is not None and record.kind is not None
      outcome = later_unaided_outcome(attempts, position, assisted) if is_assisted and has_family else None

      if outcome is None:
         continue

      success, moment = outcome
      empty_counts = {family: (0, 0) for family in REPRESENTATION_FAMILIES}
      entry = evidence.setdefault(record.kind, {"counts": empty_counts, "n": 0, "last": moment})
      trials, successes = entry["counts"][record.family]
      entry["counts"][record.family] = (trials + 1, successes + success)
      entry["n"] += 1
      entry["last"] = max(entry["last"], moment)

   return evidence


def recent(moment, now):
   return moment is not None and now - moment < DECAY_AFTER


def turn_length_evidence(turns, now):
   lengths = []
   last = None

   for turn in turns:
      is_recent_student_turn = turn.role == STUDENT and recent(parse_moment(turn.created_at), now)

      if is_recent_student_turn:
         lengths.append(len(turn.text or ""))
         last = parse_moment(turn.created_at)

   has_floor = len(lengths) >= TURN_LENGTH_EVIDENCE_FLOOR

   if not has_floor:
      return None, len(lengths), last

   band = "short" if statistics.median(lengths) <= SHORT_REPLY_CHARACTERS else "standard"

   return band, len(lengths), last


def help_pattern_counts(attempts, turns, assisted, now):
   counts = {name: 0 for name in HELP_COUNTS}
   previous_student = {}

   for turn in turns:
      moment = parse_moment(turn.created_at)
      is_recent_student_turn = turn.role == STUDENT and recent(moment, now)

      if not is_recent_student_turn:
         continue

      earlier = previous_student.get(turn.conversation_id)
      is_click_through = earlier is not None and (moment - earlier).total_seconds() < CLICK_THROUGH_SECONDS
      counts["click_throughs"] += 1 if is_click_through else 0
      previous_student[turn.conversation_id] = moment

   for opening in episode_openings(turns).values():
      asked_before_work = opening["move"] == ASK_WHAT_TRIED and recent(opening["moment"], now)
      counts["requests_before_work"] += 1 if asked_before_work else 0

   for record in attempts:
      is_unrequested_error = record.correct is False and record.id not in assisted and recent(record.submitted, now)
      counts["errors_without_request"] += 1 if is_unrequested_error else 0

   return counts


def settled(key, current, target, default, ordered_domain, marks, now):
   """One key's next value under the update discipline: back to the default 30 days after its last
   evidence, else toward the target by at most one step a week."""
   last = parse_moment(marks["last_evidence_at"].get(key))
   is_stale = last is None or now - last >= DECAY_AFTER

   if is_stale:
      return default

   is_holding = target is None or target == current

   if is_holding:
      return current

   moved = parse_moment(marks["moved_at"].get(key))
   moved_this_week = moved is not None and now - moved < STEP_INTERVAL

   if moved_this_week:
      return current

   is_ordered = ordered_domain is not None and current in ordered_domain and target in ordered_domain

   if is_ordered:
      step = 1 if ordered_domain.index(target) > ordered_domain.index(current) else -1

      return ordered_domain[ordered_domain.index(current) + step]

   return target


def fresh_marks(evidence):
   marks = copy.deepcopy(evidence) if isinstance(evidence, dict) else {}

   for name in ("last_evidence_at", "moved_at", "evidence_n", "term_seen_at", "request_seen_at"):
      marks.setdefault(name, {})

   marks.setdefault("clipped", 0)
   marks.setdefault("dropped", 0)

   return marks


def note_evidence(marks, key, moment, count):
   if moment is None:
      return

   stored = parse_moment(marks["last_evidence_at"].get(key))
   latest = moment if stored is None else max(stored, moment)
   marks["last_evidence_at"][key] = as_iso(latest)
   marks["evidence_n"][key] = count


def settle_per_kind(field_name, body, evidence_by_kind, floor, default, marks, now):
   current = body[field_name]
   kinds = set(current) | set(evidence_by_kind)
   settled_values = {}

   for kind in sorted(kinds):
      key = f"{field_name}:{kind}"
      entry = evidence_by_kind.get(kind)

      if entry is not None:
         note_evidence(marks, key, entry["last"], entry["n"])

      has_floor = entry is not None and entry["n"] >= floor
      current_value = current.get(kind, default)
      target = ranked_best(entry["counts"], current_value) if has_floor else None
      value = settled(key, current_value, target, default, None, marks, now)

      if value != current_value:
         marks["moved_at"][key] = as_iso(now)

      if value != default:
         settled_values[kind] = value

   body[field_name] = settled_values


def merged_extraction(body, outcome, active_ids, marks, now):
   stamp = as_iso(now)
   raw_terms = list(getattr(outcome, "student_terms", None) or []) if outcome is not None else []
   raw_requests = list(getattr(outcome, "stated_requests", None) or []) if outcome is not None else []
   new_terms = validated_terms(raw_terms, active_ids)
   new_requests = validated_requests(raw_requests)
   marks["dropped"] += (len(raw_terms) - len(new_terms)) + (len(raw_requests) - len(new_requests))
   terms = {entry["term"].lower(): entry for entry in body[STUDENT_TERMS]}

   for entry in new_terms:
      terms[entry["term"].lower()] = entry
      marks["term_seen_at"][entry["term"].lower()] = stamp

   for request in new_requests:
      marks["request_seen_at"][request] = stamp

   live_terms = [
      (marks["term_seen_at"].get(key), entry)
      for key, entry in terms.items()
      if recent(parse_moment(marks["term_seen_at"].get(key)), now)
   ]
   live_terms.sort(key=lambda pair: pair[0], reverse=True)
   body[STUDENT_TERMS] = [entry for _seen, entry in live_terms[:MAX_STUDENT_TERMS]]
   requests = set(body[STATED_REQUESTS]) | set(new_requests)
   body[STATED_REQUESTS] = [
      request
      for request in REQUEST_KINDS
      if request in requests and recent(parse_moment(marks["request_seen_at"].get(request)), now)
   ]
   marks["evidence_n"][STUDENT_TERMS] = len(body[STUDENT_TERMS])
   marks["evidence_n"][STATED_REQUESTS] = len(body[STATED_REQUESTS])


def provenance_for(body, previous, marks, now):
   stamp = as_iso(now)
   provenance = {}
   previous_values = value_fields(previous)

   for field_name in FIELDS:
      earlier = (previous.get(PROVENANCE) or {}).get(field_name) or {}
      has_changed = body[field_name] != previous_values[field_name]
      counts = [count for key, count in marks["evidence_n"].items() if key == field_name or key.startswith(f"{field_name}:")]
      provenance[field_name] = {
         "source": FIELD_SOURCES[field_name],
         "evidence_n": sum(counts),
         "updated_at": stamp if has_changed else earlier.get("updated_at"),
      }

   provenance[HELP_PATTERN]["evidence_n"] = sum(body[HELP_PATTERN].values())

   return provenance


def compute_profile(db, user_id, now, library=None, outcome=None):
   """Derives, merges, disciplines and clips the profile, and writes a new version only when a
   field's value changed. library supplies the active concept ids, and without one they are read
   from the configured library. Returns the current profile."""
   if memory.is_memory_paused(db, user_id):
      return current_profile(db, user_id)

   row = current_row(db, user_id)
   previous = copy.deepcopy(row.body) if row is not None else default_profile()
   active_ids = active_concept_ids(library)
   body, clips = normalised(previous, active_ids)
   marks = fresh_marks(row.evidence if row is not None else None)
   marks["clipped"] += clips

   attempts = practice_attempts(db, user_id)
   turns = user_turns(db, user_id)
   assisted = assisted_arms_for(attempts, turns)

   settle_per_kind(
      OPENING_MOVE,
      body,
      opening_move_evidence(attempts, turns, user_id, assisted),
      OPENING_MOVE_EVIDENCE_FLOOR,
      DEFAULT_OPENING_MOVE,
      marks,
      now,
   )
   settle_per_kind(
      REPRESENTATION_LEAD,
      body,
      representation_evidence(attempts, assisted),
      REPRESENTATION_EVIDENCE_FLOOR,
      None,
      marks,
      now,
   )

   band, turn_count, last_turn = turn_length_evidence(turns, now)
   note_evidence(marks, TURN_LENGTH, last_turn, turn_count)
   turn_length = settled(TURN_LENGTH, body[TURN_LENGTH], band, DEFAULT_TURN_LENGTH, TURN_LENGTHS, marks, now)

   if turn_length != body[TURN_LENGTH]:
      marks["moved_at"][TURN_LENGTH] = as_iso(now)

   body[TURN_LENGTH] = turn_length
   body[NUDGE_DEPTH_START] = settled(
      NUDGE_DEPTH_START, body[NUDGE_DEPTH_START], None, DEFAULT_NUDGE_DEPTH, PROFILE_RUNGS, marks, now
   )
   body[HELP_PATTERN] = help_pattern_counts(attempts, turns, assisted, now)
   merged_extraction(body, outcome, active_ids, marks, now)

   stamp = as_iso(now)
   has_changed = value_fields(body) != value_fields(previous)

   if not has_changed:
      if row is not None:
         row.evidence = marks
         row.updated_at = stamp
         db.flush()

      return current_profile(db, user_id)

   version = (row.version if row is not None else 0) + 1
   body[PROVENANCE] = provenance_for(body, previous, marks, now)
   body[PROFILE_VERSION] = version
   db.add(
      models.TutorProfile(
         user_id=user_id,
         version=version,
         body=body,
         evidence=marks,
         created_at=stamp,
         updated_at=stamp,
      )
   )
   db.flush()

   return current_profile(db, user_id)
