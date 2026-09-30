"""The live tutor's memory store (docs/agent/architecture.md, "The memory store").

tutor_memories holds four kinds of entry: a preference for how to be helped, a confusion in the
student's words, a difficulty the student stated, and a short episode note of the last
conversation. retrieve picks what one turn's prompt carries, in the order the architecture fixes:
every preference first (at most 3), then the confusions and stated difficulties that touch a skill
on the screen, then the latest episode, then the remaining confusions and difficulties, stopping at
6 entries or 300 tokens by the 3.1 characters-per-token divisor research/math-tutoring.md measured.

apply_proposals is the only path by which a consolidation job's proposals become rows, and every
rule in the architecture is enforced here rather than trusted to the prompt: the kind is one of the
four, the text is at most 200 characters and passes screen_text, the evidence turns belong to the
conversation, the target is neither deleted nor rewritten by the student, and every skill id is an
active library id. A proposal that breaks a rule is counted and dropped, and a malformed proposal
never raises, because the job must finish and the model's output is untrusted. The model never
deletes.

screen_text is the content screen of docs/plan/09-security-and-privacy.md's 2026-09-29 amendment,
"What is deliberately not stored": nothing answer-shaped, no item or archetype id, no mastery claim
or correctness judgement, and nothing instruction-shaped, since a memory is rendered into a prompt
and must never read as an instruction to the tutor.

Memory never reaches grading, diagnosis, selection or the engine; tests/agent/test_boundary.py
holds both directions of that line. Every change the student makes writes an audit row whose
detail holds ids and counts and never the text.
"""
import re
from datetime import datetime, timedelta

from sqlalchemy import delete, select

from app.auth.service import as_iso, new_id, write_audit
from app.db import models

PREFERENCE = "preference"
CONFUSION = "confusion"
STATED_DIFFICULTY = "stated_difficulty"
EPISODE = "episode"
KINDS = (PREFERENCE, CONFUSION, STATED_DIFFICULTY, EPISODE)
STUDENT_EDITABLE_KINDS = (PREFERENCE, CONFUSION)
SKILL_SCOPED_KINDS = (CONFUSION, STATED_DIFFICULTY)

ADD = "ADD"
UPDATE = "UPDATE"
SUPERSEDE = "SUPERSEDE"
NOOP = "NOOP"
OPERATIONS = (ADD, UPDATE, SUPERSEDE, NOOP)
TARGETED_OPERATIONS = (UPDATE, SUPERSEDE, NOOP)
TEXT_BEARING_OPERATIONS = (ADD, UPDATE, SUPERSEDE)

SOURCE_CONVERSATION = "conversation"
MAX_TEXT_CHARACTERS = 200
RETRIEVE_ENTRY_LIMIT = 6
RETRIEVE_TOKEN_LIMIT = 300
CHARACTERS_PER_TOKEN = 3.1
PREFERENCES_RETRIEVED = 3
EPISODE_LIFETIME = timedelta(days=14)
ENTRY_LIFETIME = timedelta(days=60)
HARD_DELETE_AFTER = timedelta(days=30)

REJECTED_KIND = "kind"
REJECTED_LENGTH = "length"
REJECTED_TARGET = "target"
REJECTED_EVIDENCE = "evidence"
REJECTED_SKILL_IDS = "skill_ids"
REJECTED_CONTENT_SCREEN = "content_screen"
REJECTED_PAUSED = "paused"
REJECTION_REASONS = (
   REJECTED_KIND,
   REJECTED_TARGET,
   REJECTED_EVIDENCE,
   REJECTED_SKILL_IDS,
   REJECTED_LENGTH,
   REJECTED_CONTENT_SCREEN,
   REJECTED_PAUSED,
)

DELETED_ACTION = "agent_memory_deleted"
EDITED_ACTION = "agent_memory_edited"
CLEARED_ACTION = "agent_memory_cleared"
PAUSED_ACTION = "agent_memory_paused"
RESUMED_ACTION = "agent_memory_resumed"
CONSOLIDATION_ACTION = "agent_consolidation_applied"
WORKER_ACTOR = "worker"

ANSWER_SHAPED = "answer_shaped"
CARRIES_ID = "carries_id"
MASTERY_WORD = "mastery_word"
INSTRUCTION_SHAPED = "instruction_shaped"

ANSWER_SHAPED_PATTERNS = (
   re.compile(r"\\[(\[]"),
   re.compile(r"\$"),
   re.compile(r"\d\s*[-+*/^=<>]"),
   re.compile(r"[-+*/^=<>]\s*\d"),
   re.compile(r"\d\.\d"),
   re.compile(r"\b\d+[a-z]\b"),
   re.compile(r"\b(?:sin|cos|tan|sec|csc|cot|ln|log|arcsin|arccos|arctan|sqrt)\s*\(", re.IGNORECASE),
)
ID_PATTERN = re.compile(r"\b(?:ITM|BC|ACV|ATN|MEM|LSN|SES|ATT)-[A-Za-z0-9-]+")
MASTERY_WORDS = (
   "mastered",
   "mastery",
   "masters",
   "weak",
   "weaker",
   "weakest",
   "weakness",
   "strong",
   "stronger",
   "strongest",
   "strength",
   "ready",
   "behind",
   "ahead",
   "score",
   "scores",
   "scored",
   "correct",
   "incorrect",
   "wrong",
)
MASTERY_PATTERN = re.compile(r"\b(?:" + "|".join(MASTERY_WORDS) + r")\b", re.IGNORECASE)
INSTRUCTION_PHRASES = (
   "always",
   "never",
   "you must",
   "must",
   "ignore",
   "disregard",
   "from now on",
   "the tutor should",
   "you should",
   "instructions",
   "system prompt",
)
INSTRUCTION_PATTERN = re.compile(
   r"\b(?:" + "|".join(re.escape(phrase) for phrase in INSTRUCTION_PHRASES) + r")\b", re.IGNORECASE
)


class MemoryNotFound(LookupError):
   pass


class MemoryRefused(ValueError):
   pass


def parse_moment(stamp):
   return datetime.fromisoformat(stamp)


def lifetime_for(kind):
   is_episode = kind == EPISODE

   return EPISODE_LIFETIME if is_episode else ENTRY_LIFETIME


def estimated_tokens(text):
   return len(text or "") / CHARACTERS_PER_TOKEN


def screen_text(text):
   """None when the text may be stored as a memory, else the name of the class it falls in. Ids
   are looked for first, because an id's digits after a hyphen also read as answer-shaped."""
   if ID_PATTERN.search(text):
      return CARRIES_ID

   is_answer_shaped = any(pattern.search(text) for pattern in ANSWER_SHAPED_PATTERNS)

   if is_answer_shaped:
      return ANSWER_SHAPED

   if MASTERY_PATTERN.search(text):
      return MASTERY_WORD

   if INSTRUCTION_PATTERN.search(text):
      return INSTRUCTION_SHAPED

   return None


def is_active(entry, now):
   is_superseded = entry.superseded_by is not None or entry.invalid_at is not None
   is_deleted = entry.deleted_at is not None
   is_resolved = entry.resolved_at is not None
   is_expired = entry.expires_at is not None and parse_moment(entry.expires_at) <= now

   return not (is_superseded or is_deleted or is_resolved or is_expired)


def active_entries(db, user_id, now):
   rows = db.scalars(select(models.TutorMemory).where(models.TutorMemory.user_id == user_id)).all()

   return [row for row in rows if is_active(row, now)]


def is_memory_paused(db, user_id):
   user = db.get(models.User, user_id)

   return user is not None and user.agent_memory_paused == 1


def by_last_confirmed(entries):
   return sorted(entries, key=lambda entry: (entry.last_confirmed_at, entry.id), reverse=True)


def ranked_for_screen(entries, screen_skill_ids):
   screen_skills = set(screen_skill_ids or ())
   preferences = by_last_confirmed([entry for entry in entries if entry.kind == PREFERENCE])
   skill_scoped = by_last_confirmed([entry for entry in entries if entry.kind in SKILL_SCOPED_KINDS])
   touching_screen = [entry for entry in skill_scoped if screen_skills & set(entry.skill_ids or ())]
   elsewhere = [entry for entry in skill_scoped if entry not in touching_screen]
   episodes = sorted(
      [entry for entry in entries if entry.kind == EPISODE],
      key=lambda entry: (entry.created_at, entry.id),
      reverse=True,
   )

   return preferences[:PREFERENCES_RETRIEVED] + touching_screen + episodes[:1] + elsewhere


def entry_payload(entry):
   return {"id": entry.id, "kind": entry.kind, "text": entry.text, "skill_ids": list(entry.skill_ids or ())}


def retrieve(db, user_id, screen_skill_ids, now, limit_entries=RETRIEVE_ENTRY_LIMIT, limit_tokens=RETRIEVE_TOKEN_LIMIT):
   """The entries one turn's prompt carries, each stamped as used. Empty while memory is paused."""
   if is_memory_paused(db, user_id):
      return []

   chosen = []
   tokens_used = 0.0

   for entry in ranked_for_screen(active_entries(db, user_id, now), screen_skill_ids):
      entry_tokens = estimated_tokens(entry.text)
      is_full = len(chosen) >= limit_entries
      would_overflow = tokens_used + entry_tokens > limit_tokens

      if is_full or would_overflow:
         break

      chosen.append(entry)
      tokens_used += entry_tokens

   stamp = as_iso(now)

   for entry in chosen:
      entry.last_used_at = stamp
      entry.expires_at = as_iso(now + lifetime_for(entry.kind))
      entry.updated_at = stamp

   db.flush()

   return [entry_payload(entry) for entry in chosen]


def user_skill_ids(db, user_id):
   return set(db.scalars(select(models.SkillState.skill_id).where(models.SkillState.user_id == user_id)).all())


def conversation_turn_ids(db, conversation):
   statement = select(models.AgentTurn.id).where(models.AgentTurn.conversation_id == conversation.id)

   return set(db.scalars(statement.where(models.AgentTurn.user_id == conversation.user_id)).all())


def is_string_list(value):
   is_list = isinstance(value, list)

   return is_list and all(isinstance(element, str) for element in value)


def proposal_fields(proposal):
   """The proposal's fields when every one has the shape the schema gives it, else None."""
   if not isinstance(proposal, dict):
      return None

   operation = proposal.get("operation")
   kind = proposal.get("kind")
   text = proposal.get("text")
   target_id = proposal.get("target_id")
   skill_ids = proposal.get("skill_ids", [])
   evidence_turn_ids = proposal.get("evidence_turn_ids", [])

   has_known_operation = operation in OPERATIONS
   has_known_kind = kind in KINDS
   has_text_string = isinstance(text, str)
   has_target_shape = target_id is None or isinstance(target_id, str)
   has_id_lists = is_string_list(skill_ids) and is_string_list(evidence_turn_ids)
   is_well_formed = has_known_operation and has_known_kind and has_text_string and has_target_shape and has_id_lists

   if not is_well_formed:
      return None

   return {
      "operation": operation,
      "kind": kind,
      "text": text.strip(),
      "target_id": target_id,
      "skill_ids": list(dict.fromkeys(skill_ids)),
      "evidence_turn_ids": evidence_turn_ids,
   }


def usable_target(db, user_id, fields, now):
   target_id = fields["target_id"]

   if target_id is None:
      return None

   target = db.get(models.TutorMemory, target_id)
   is_owned = target is not None and target.user_id == user_id

   if not is_owned:
      return None

   is_student_edited = target.edited_by_student == 1
   is_same_kind = target.kind == fields["kind"]
   is_replaceable_kind = fields["operation"] == SUPERSEDE or is_same_kind
   is_usable = is_active(target, now) and not is_student_edited and is_replaceable_kind

   return target if is_usable else None


def rejection_reason(fields, target, turn_ids, active_skill_ids):
   """The first rule a well-formed proposal breaks, in REJECTION_REASONS order, or None when it
   breaks none."""
   operation = fields["operation"]
   text = fields["text"]
   carries_text = operation in TEXT_BEARING_OPERATIONS

   needs_target = operation in TARGETED_OPERATIONS
   is_missing_target = needs_target and target is None
   has_empty_text = carries_text and text == ""
   is_too_long = carries_text and len(text) > MAX_TEXT_CHARACTERS
   has_bad_length = has_empty_text or is_too_long
   cites_outside_turns = not set(fields["evidence_turn_ids"]) <= turn_ids
   names_inactive_skill = not set(fields["skill_ids"]) <= active_skill_ids

   if is_missing_target:
      return REJECTED_TARGET

   if cites_outside_turns:
      return REJECTED_EVIDENCE

   if names_inactive_skill:
      return REJECTED_SKILL_IDS

   if has_bad_length:
      return REJECTED_LENGTH

   fails_screen = carries_text and screen_text(text) is not None

   if fails_screen:
      return REJECTED_CONTENT_SCREEN

   return None


def new_entry(user_id, conversation, fields, now):
   stamp = as_iso(now)

   return models.TutorMemory(
      id=new_id("MEM"),
      user_id=user_id,
      kind=fields["kind"],
      text=fields["text"],
      skill_ids=fields["skill_ids"],
      source=SOURCE_CONVERSATION,
      source_conversation_id=conversation.id,
      evidence_count=1,
      last_confirmed_at=stamp,
      last_used_at=None,
      expires_at=as_iso(now + lifetime_for(fields["kind"])),
      edited_by_student=0,
      created_at=stamp,
      updated_at=stamp,
   )


def apply_one(db, user_id, conversation, fields, target, now):
   stamp = as_iso(now)
   operation = fields["operation"]

   if operation == ADD:
      db.add(new_entry(user_id, conversation, fields, now))

   if operation == UPDATE:
      target.text = fields["text"]
      target.skill_ids = list(dict.fromkeys([*(target.skill_ids or []), *fields["skill_ids"]]))
      target.evidence_count = target.evidence_count + 1
      target.last_confirmed_at = stamp
      target.updated_at = stamp

   if operation == SUPERSEDE:
      replacement = new_entry(user_id, conversation, fields, now)
      db.add(replacement)
      target.superseded_by = replacement.id
      target.invalid_at = stamp
      target.updated_at = stamp

   if operation == NOOP:
      target.last_confirmed_at = stamp
      target.updated_at = stamp


def apply_proposals(db, user_id, conversation, proposals, now, active_skill_ids=None):
   """Applies what passes every rule and counts the rest. active_skill_ids defaults to the
   student's skills_state ids, which the seeding took from the active library snapshot. Writes one
   agent_consolidation_applied row with the two counts and the rejections counted by reason, each
   rejection under the first rule it breaks, a malformed proposal or an unknown kind or operation
   under kind. While memory is paused nothing is applied and every proposal counts as rejected
   under paused."""
   proposals = proposals if isinstance(proposals, list) else []
   applied = 0
   rejected_by = dict.fromkeys(REJECTION_REASONS, 0)

   if is_memory_paused(db, user_id):
      rejected_by[REJECTED_PAUSED] = len(proposals)
   else:
      known_skill_ids = set(active_skill_ids) if active_skill_ids is not None else user_skill_ids(db, user_id)
      turn_ids = conversation_turn_ids(db, conversation)

      for proposal in proposals:
         fields = proposal_fields(proposal)

         if fields is None:
            rejected_by[REJECTED_KIND] += 1
            continue

         target = usable_target(db, user_id, fields, now)
         reason = rejection_reason(fields, target, turn_ids, known_skill_ids)

         if reason is not None:
            rejected_by[reason] += 1
            continue

         apply_one(db, user_id, conversation, fields, target, now)
         db.flush()
         applied += 1

   counts = {"applied": applied, "rejected": sum(rejected_by.values())}
   detail = {"conversation_id": conversation.id, **counts, "rejected_by": rejected_by}
   write_audit(db, WORKER_ACTOR, CONSOLIDATION_ACTION, f"agent_conversations:{conversation.id}", detail, now)

   return counts


def expire_and_resolve(db, user_id, now, mastered_skill_ids):
   """Sets expires_at from the last use (episodes 14 days, others 60), resolves a confusion whose
   skills are all mastered, and hard-deletes superseded, resolved and tombstoned rows 30 days after
   they became so. Returns the counts."""
   mastered = set(mastered_skill_ids or ())
   stamp = as_iso(now)
   expired = 0
   resolved = 0
   removable_ids = []

   rows = db.scalars(select(models.TutorMemory).where(models.TutorMemory.user_id == user_id)).all()

   for entry in rows:
      was_active = is_active(entry, now)
      last_touch = entry.last_used_at or entry.created_at
      entry.expires_at = as_iso(parse_moment(last_touch) + lifetime_for(entry.kind))
      has_expired = was_active and not is_active(entry, now)

      if has_expired:
         expired += 1

      entry_skills = set(entry.skill_ids or ())
      is_resolvable_kind = entry.kind == CONFUSION
      has_all_skills_mastered = len(entry_skills) > 0 and entry_skills <= mastered
      should_resolve = was_active and not has_expired and is_resolvable_kind and has_all_skills_mastered

      if should_resolve:
         entry.resolved_at = stamp
         entry.updated_at = stamp
         resolved += 1

      ended_at = entry.invalid_at or entry.resolved_at or entry.deleted_at
      has_ended = ended_at is not None
      is_long_ended = has_ended and parse_moment(ended_at) <= now - HARD_DELETE_AFTER

      if is_long_ended:
         removable_ids.append(entry.id)

   has_removable = len(removable_ids) > 0

   if has_removable:
      db.execute(delete(models.TutorMemory).where(models.TutorMemory.id.in_(removable_ids)))

   db.flush()

   return {"expired": expired, "resolved": resolved, "deleted": len(removable_ids)}


def owned_entry(db, user_id, memory_id):
   entry = db.get(models.TutorMemory, memory_id)
   is_owned = entry is not None and entry.user_id == user_id

   if not is_owned:
      raise MemoryNotFound(memory_id)

   return entry


def delete_entry(db, user_id, memory_id, now):
   """Leaves a tombstone: the text is erased, kind and skill_ids stay so a later consolidation
   cannot re-add what the student forgot."""
   entry = owned_entry(db, user_id, memory_id)
   is_tombstone = entry.deleted_at is not None

   if is_tombstone:
      raise MemoryNotFound(memory_id)

   stamp = as_iso(now)
   entry.text = None
   entry.deleted_at = stamp
   entry.updated_at = stamp
   db.flush()

   write_audit(db, user_id, DELETED_ACTION, f"tutor_memories:{entry.id}", {"memory_id": entry.id}, now)

   return entry


def edit_entry(db, user_id, memory_id, text, now):
   entry = owned_entry(db, user_id, memory_id)

   if not is_active(entry, now):
      raise MemoryNotFound(memory_id)

   is_editable_kind = entry.kind in STUDENT_EDITABLE_KINDS

   if not is_editable_kind:
      raise MemoryRefused("only a preference or a confusion can be edited")

   is_text = isinstance(text, str)
   cleaned = text.strip() if is_text else ""
   is_empty = cleaned == ""
   is_too_long = len(cleaned) > MAX_TEXT_CHARACTERS

   if is_empty or is_too_long:
      raise MemoryRefused(f"the text must be 1 to {MAX_TEXT_CHARACTERS} characters")

   stamp = as_iso(now)
   entry.text = cleaned
   entry.edited_by_student = 1
   entry.updated_at = stamp
   db.flush()

   write_audit(db, user_id, EDITED_ACTION, f"tutor_memories:{entry.id}", {"memory_id": entry.id}, now)

   return entry


def clear_all(db, user_id, now):
   """Every memory row including tombstones, every turn, every conversation and every profile
   version (09's 2026-09-29 amendment: the profile is deletable with the memory clear)."""
   removed = {}
   owned_tables = (
      ("tutor_memories", models.TutorMemory),
      ("agent_turns", models.AgentTurn),
      ("agent_conversations", models.AgentConversation),
      ("tutor_profiles", models.TutorProfile),
   )

   for name, model in owned_tables:
      removed[name] = db.execute(delete(model).where(model.user_id == user_id)).rowcount

   db.flush()

   write_audit(db, user_id, CLEARED_ACTION, f"users:{user_id}", removed, now)

   return removed


def set_paused(db, user_id, paused, now):
   user = db.get(models.User, user_id)
   user.agent_memory_paused = 1 if paused else 0
   user.updated_at = as_iso(now)
   db.flush()

   if paused:
      write_audit(db, user_id, PAUSED_ACTION, f"users:{user_id}", None, now)
   else:
      write_audit(db, user_id, RESUMED_ACTION, f"users:{user_id}", None, now)

   return paused
