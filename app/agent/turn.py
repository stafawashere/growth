"""One live tutor turn, from the posted screen to the stored reply (docs/agent/architecture.md,
Streaming end to end, Roles, models, caps and the chain, Guard, pacing, audit, purge and export, and
The context composer; docs/agent/build-plan.md, Slice 4).

run_turn is a generator of server-sent events, each a dict with "event" and "data". Before the
chain is called it validates the screen, resolves the conversation, loads and checks the rows the
screen names, counts the ceilings, composes the packet, chooses the move, renders the prompt and
writes the student's turn, and it commits that turn before the first event leaves. A turn refused
before then writes nothing and sends one error event: timed for a timed part, ceiling at the third
practice question on an item or the twentieth in a conversation, refused for a shape, an id or a
row that does not belong to the student.

The reply runs down the agent's chain and through SentenceScreen, and each released sentence is one
text event. A sentence the screen withholds ends the stream: the decline is sent in its place, the
turn ends withheld, the stored reply is the decline, and agent_reply_withheld is written at most
once per user per day, naming the check and the turn. A failure before any sentence was released
is an error event whose kind names what stopped it, a failure after one ends the turn incomplete,
and nothing is ever queued for later (docs/agent/design.md, The empty state and the degraded
states). Every error event carries its copy from app/agent/copy.py.

The 15-second bound on the first text is measured on the stream's own clock: when the first delta
arrives later than FIRST_TEXT_BOUND_SECONDS after the call began, the stream is closed, the guard
charges it, and the turn ends unavailable. Until a delta arrives the bound is the provider's own,
the CLI's fixed API_TIMEOUT_MS and single retry and the provider's process timeout, because a
second thread watching a generator the response is iterating is not a clean way to interrupt it.

Only the turn id, the outcome, the link and the elapsed milliseconds are logged, never a delta, a
prompt, a memory entry or the student's message.
"""
import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from time import monotonic

from fastapi import HTTPException
from sqlalchemy import select

from app.agent import consolidate, conversations, memory
from app.agent import copy as agent_copy
from app.agent.context import TimedPartRefused, compose_packet, mode_for, render_prompt, validate_screen
from app.agent.moves import AFTER_SUBMISSION, PRACTICE
from app.agent.screen import SentenceScreen
from app.api.routes.sessions import attempt_diagnoses, chosen_option, owned_attempt, owned_session
from app.auth.service import write_audit
from app.db import models
from app.evals import agent_checks
from app.experiments import switches
from app.feedback import render
from app.lessons import repository as lesson_repository
from app.providers.base import CacheSettings, Message, ProviderRequest, RefusedBeforeWire
from app.providers.guard import (
   SUBSCRIPTION_DAILY_CAP,
   SUBSCRIPTION_MINUTE_RATE,
   BudgetStopped,
   DevSpendCapExceeded,
   ProviderCallFailed,
)
from app.providers.model_routing import model_for
from app.providers.router import SUBSCRIPTION_LINK, chain_for, links_from_settings
from app.providers.subscription import SubscriptionAuthFailed, SubscriptionLimitReached
from app.session import service as session_service

logger = logging.getLogger(__name__)

ROLE = "agent"
LINKS_FIELD = "agent_links"
PROVIDER_FIELD = "tutor"
AGENT_MODEL = model_for(ROLE)
MAX_OUTPUT_TOKENS = 800
PREFIX_CACHE_TTL = "1h"
AGENT_PROVIDER_OPTIONS = {
   "thinking": {"type": "disabled"},
   "output_config": {"effort": "low"},
}

PRACTICE_TURN_CEILING = agent_checks.PER_ITEM_TURN_CEILING
CONVERSATION_TURN_CEILING = 20
FIRST_TEXT_BOUND_SECONDS = 15
REPLY_STAMP_GAP = timedelta(microseconds=1)
RESET_WINDOWS = ("five_hour", "seven_day")
NO_PROVIDER_LINK = "no_provider_link"

ITEM_SCREEN = "session_item"
SESSION_LESSON_SCREEN = "session_lesson"
LESSON_SCREEN = "lesson"
PROGRESS_SCREEN = "progress"

COMPLETE = "complete"
INCOMPLETE = "incomplete"
WITHHELD = "withheld"
STOPPED = "stopped"

WITHHELD_ACTION = "agent_reply_withheld"

BAD_REQUEST = 400
NOT_FOUND = 404
CONFLICT = 409

START_EVENT = "start"
TEXT_EVENT = "text"
END_EVENT = "end"
ERROR_EVENT = "error"


class TurnRefused(Exception):
   """A turn stopped before anything was written. status is the HTTP status the refusal would have
   carried as a plain response, sent in the error event so the client can tell a shape from an id."""

   def __init__(self, kind, status=None, conversation_ceiling=False):
      super().__init__(kind)
      self.kind = kind
      self.status = status
      self.conversation_ceiling = conversation_ceiling


@dataclass
class ScreenRows:
   session: object = None
   item: object = None
   attempt: object = None
   archetype: dict | None = None
   lesson: object = None
   feedback: object = None
   diagnosis: object = None
   skill_ids: tuple = ()


@dataclass
class PreparedTurn:
   conversation: object
   screen: dict
   packet: object
   rows: ScreenRows
   request: ProviderRequest
   student_turn: object
   turns_on_item: int
   turns_in_conversation: int


@dataclass
class StreamState:
   released: list = field(default_factory=list)
   failure: Exception | None = None
   late_first_text: bool = False


def event(name, data):
   return {"event": name, "data": data}


def error_event(kind, status=None, resets_at=None, reset_time=None, conversation_ceiling=False):
   data = {
      "kind": kind,
      "copy": agent_copy.copy_for(kind, reset_time=reset_time, conversation_ceiling=conversation_ceiling),
   }
   is_usage_limit = kind == agent_copy.USAGE_LIMIT

   if is_usage_limit:
      data["resets_at"] = resets_at

   if status is not None:
      data["status"] = status

   return event(ERROR_EVENT, data)


def elapsed_ms(clock, started):
   return int(round((clock() - started) * 1000))


def log_turn(turn_id, outcome, link, clock, started):
   logger.info("agent turn %s outcome=%s link=%s elapsed_ms=%d", turn_id, outcome, link, elapsed_ms(clock, started))


def fields_of(body):
   is_object = isinstance(body, dict)

   if not is_object:
      raise TurnRefused(agent_copy.REFUSED, BAD_REQUEST)

   message = body.get("message")
   conversation_id = body.get("conversation_id")
   is_message = isinstance(message, str) and message.strip() != ""
   is_conversation_id = conversation_id is None or isinstance(conversation_id, str)
   is_well_formed = is_message and is_conversation_id

   if not is_well_formed:
      raise TurnRefused(agent_copy.REFUSED, BAD_REQUEST)

   return body.get("screen"), message, conversation_id


def checked_screen(screen):
   try:
      check = validate_screen(screen)
   except ValueError:
      raise TurnRefused(agent_copy.REFUSED, BAD_REQUEST) from None

   if check.timed:
      raise TurnRefused(agent_copy.TIMED)

   return check


def resolved_conversation(db, user_id, conversation_id, screen_kind, now):
   """The conversation this turn joins. A conversation idle past 30 minutes, or one the panel
   already closed, is left closed and enqueued, and the turn opens a new one."""
   is_new = conversation_id is None

   if is_new:
      return conversations.open_conversation(db, user_id, screen_kind, now)

   try:
      conversation = conversations.owned_conversation(db, user_id, conversation_id)
   except conversations.ConversationNotFound:
      raise TurnRefused(agent_copy.REFUSED, NOT_FOUND) from None

   is_closed = conversation.closed_at is not None
   is_idle = conversations.is_idle(conversation, now)

   went_idle_while_open = is_idle and not is_closed

   if went_idle_while_open:
      close_and_enqueue(db, user_id, conversation, now)

   has_ended = is_closed or is_idle

   if has_ended:
      return conversations.open_conversation(db, user_id, screen_kind, now)

   return conversation


def close_and_enqueue(db, user_id, conversation, now):
   conversations.close_conversation(db, conversation, now)
   has_turns = conversation.turn_count > 0

   if has_turns:
      consolidate.enqueue(db, user_id, conversation, now)


def _owned(check, *args):
   try:
      return check(*args)
   except HTTPException:
      raise TurnRefused(agent_copy.REFUSED, NOT_FOUND) from None


def concept_lesson(db, context, archetype):
   """The servable lesson of the first of the archetype's concepts that has one, in the archetype's
   skills order, as app/api/routes/sessions.py lesson_link_for reads them."""
   skills = getattr(context.graph, "skills", {}) or {}
   servable = lesson_repository.servable_map(db)

   for skill_id in archetype.get("skills") or []:
      concept_id = (skills.get(skill_id) or {}).get("concept")
      found = servable.get(concept_id) if concept_id else None

      if found is not None:
         return db.get(models.Lesson, found)

   return None


def feedback_for(context, session_row, attempt, item, archetype):
   """The feedback the feedback route renders for this attempt, the verification-only arm included,
   without the tutor sentence."""
   answer = json.loads(attempt.response) if attempt.response else {}
   chosen = chosen_option(item, answer)
   error_path = (chosen or {}).get("error_path")
   error_record = context.errors.get(error_path) if error_path else None

   try:
      feedback = render.render_feedback(
         attempt.served_stage,
         archetype,
         {"worked_solution": item.worked_solution},
         submitted=True,
         correct=None if attempt.correct is None else bool(attempt.correct),
         chosen_option=chosen,
         error_record=error_record,
         confidence=attempt.confidence,
         is_opener=session_service.served_as_opener(session_row, attempt),
         answer=answer,
      )
   except ValueError:
      raise TurnRefused(agent_copy.REFUSED, CONFLICT) from None

   feedback_arm = switches.recorded_arms(attempt).get(switches.FEEDBACK_ELABORATION)
   is_verification_only = feedback_arm == switches.DEFINITIONS[switches.FEEDBACK_ELABORATION].treatment_arm

   if is_verification_only:
      return render.verification_only(feedback)

   return feedback


def item_rows(settings, db, user, screen):
   """Before submission no attempts row exists yet, so the screen's attempt id is checked only when
   a row carries it: it must then belong to this session and this item."""
   context = settings.session_context
   session_row = _owned(owned_session, db, screen["session_id"], user)

   try:
      session_service.queue_slot(session_row, screen["item_id"])
   except ValueError:
      raise TurnRefused(agent_copy.REFUSED, NOT_FOUND) from None

   item = db.get(models.Item, screen["item_id"])

   if item is None:
      raise TurnRefused(agent_copy.REFUSED, NOT_FOUND)

   attempt = db.get(models.Attempt, screen["attempt_id"])
   has_attempt = attempt is not None

   if has_attempt:
      _owned(owned_attempt, db, session_row, attempt.id)
      is_other_item = attempt.item_id != item.id

      if is_other_item:
         raise TurnRefused(agent_copy.REFUSED, NOT_FOUND)

   is_submitted = has_attempt and attempt.submitted_at is not None
   claims_submission = screen["submitted"] is True
   is_unsupported_claim = claims_submission and not is_submitted

   if is_unsupported_claim:
      raise TurnRefused(agent_copy.REFUSED, CONFLICT)

   archetype = context.archetypes.get(item.archetype_id)

   if archetype is None:
      raise TurnRefused(agent_copy.REFUSED, NOT_FOUND)

   rows = ScreenRows(
      session=session_row,
      item=item,
      attempt=attempt,
      archetype=archetype,
      lesson=concept_lesson(db, context, archetype),
      skill_ids=tuple(json.loads(item.skills) if isinstance(item.skills, str) else item.skills or ()),
   )

   if is_submitted:
      rows.feedback = feedback_for(context, session_row, attempt, item, archetype)
      diagnoses = attempt_diagnoses(db, attempt)
      rows.diagnosis = diagnoses[0] if diagnoses else None

   return rows


def lesson_skill_ids(lesson):
   skill_ids = []

   for section in (lesson.body or {}).get("sections") or []:
      for skill_id in section.get("skills") or []:
         if skill_id not in skill_ids:
            skill_ids.append(skill_id)

   return tuple(skill_ids)


def lesson_rows(db, user, screen):
   session_row = None
   is_in_session = screen["kind"] == SESSION_LESSON_SCREEN

   if is_in_session:
      session_row = _owned(owned_session, db, screen["session_id"], user)

   lesson = lesson_repository.servable_lesson(db, screen["lesson_id"], screen["version"])

   if lesson is None:
      raise TurnRefused(agent_copy.REFUSED, NOT_FOUND)

   return ScreenRows(session=session_row, lesson=lesson, skill_ids=lesson_skill_ids(lesson))


def screen_rows(settings, db, user, screen):
   kind = screen["kind"]

   if kind == ITEM_SCREEN:
      return item_rows(settings, db, user, screen)

   if kind in (SESSION_LESSON_SCREEN, LESSON_SCREEN):
      return lesson_rows(db, user, screen)

   skill_id = screen.get("skill_id")
   is_skill = kind == PROGRESS_SCREEN and skill_id is not None

   return ScreenRows(skill_ids=(skill_id,) if is_skill else ())


def student_turns(db, user_id, **filters):
   statement = (
      select(models.AgentTurn)
      .where(models.AgentTurn.user_id == user_id)
      .where(models.AgentTurn.role == conversations.STUDENT)
   )

   for name, value in filters.items():
      statement = statement.where(getattr(models.AgentTurn, name) == value)

   return db.scalars(statement).all()


def turns_on_item_before(db, user_id, screen, mode, attempt):
   """Practice turns are counted per item within the screen's session, because before submission
   the attempts row does not exist yet and an item is attempted at most once in a session. Turns
   after submission are counted per attempt."""
   if mode == PRACTICE:
      rows = student_turns(db, user_id, mode=PRACTICE, item_id=screen["item_id"])

      return sum(1 for row in rows if (row.screen or {}).get("session_id") == screen["session_id"])

   if mode == AFTER_SUBMISSION:
      return len(student_turns(db, user_id, mode=AFTER_SUBMISSION, attempt_id=attempt.id))

   return 0


def conversation_history(db, conversation):
   statement = (
      select(models.AgentTurn)
      .where(models.AgentTurn.conversation_id == conversation.id)
      .where(models.AgentTurn.user_id == conversation.user_id)
      .order_by(models.AgentTurn.created_at, models.AgentTurn.id)
   )

   return [{"role": turn.role, "text": turn.text} for turn in db.scalars(statement).all()]


def answered_previous_question(history, message):
   """Whether the student's message reads as an answer to the tutor's last question: the tutor's
   last turn ended in a question and the student did not answer it with a question of their own."""
   agent_turns = [turn for turn in history if turn["role"] == conversations.AGENT]

   if not agent_turns:
      return False

   tutor_asked = agent_turns[-1]["text"].rstrip().endswith("?")
   student_asked_back = message.rstrip().endswith("?")

   return tutor_asked and not student_asked_back


def agent_request(rendered):
   return ProviderRequest(
      role=ROLE,
      model=AGENT_MODEL,
      system=rendered.system,
      messages=(Message(role="user", content=rendered.user),),
      max_output_tokens=MAX_OUTPUT_TOKENS,
      stream=True,
      cache=CacheSettings(prefix_breakpoints=1, ttl=PREFIX_CACHE_TTL),
      provider_options={key: dict(value) for key, value in AGENT_PROVIDER_OPTIONS.items()},
   )


def prepare_turn(settings, db, user, body, now):
   screen, message, conversation_id = fields_of(body)
   check = checked_screen(screen)
   conversation = resolved_conversation(db, user.id, conversation_id, check.kind, now)
   rows = screen_rows(settings, db, user, screen)
   mode = mode_for(screen, rows.attempt)
   prior_on_item = turns_on_item_before(db, user.id, screen, mode, rows.attempt)
   is_practice = mode == PRACTICE
   reached_item_ceiling = is_practice and prior_on_item >= PRACTICE_TURN_CEILING

   if reached_item_ceiling:
      raise TurnRefused(agent_copy.CEILING)

   prior_in_conversation = len(student_turns(db, user.id, conversation_id=conversation.id))
   reached_conversation_ceiling = prior_in_conversation >= CONVERSATION_TURN_CEILING

   if reached_conversation_ceiling:
      raise TurnRefused(agent_copy.CEILING, conversation_ceiling=True)

   history = conversation_history(db, conversation)
   entries = memory.retrieve(db, user.id, list(rows.skill_ids), now)

   try:
      packet, _move = compose_packet(
         settings.session_context,
         screen,
         item=rows.item,
         attempt=rows.attempt,
         archetype=rows.archetype,
         lesson=rows.lesson,
         feedback=rows.feedback,
         memory_entries=entries,
         profile=None,
         turn_index_on_item=prior_on_item,
         student_answered_question=answered_previous_question(history, message),
         diagnosis=rows.diagnosis,
      )
   except TimedPartRefused:
      raise TurnRefused(agent_copy.TIMED) from None
   except (KeyError, ValueError):
      raise TurnRefused(agent_copy.REFUSED, BAD_REQUEST) from None

   rendered = render_prompt(packet, entries, None, history, message)
   student_turn = conversations.append_turn(
      db,
      conversation,
      conversations.STUDENT,
      message,
      now,
      screen=screen,
      mode=packet.mode,
      item_id=screen.get("item_id"),
      attempt_id=screen.get("attempt_id"),
   )
   has_open_attempt = rows.attempt is not None and rows.attempt.submitted_at is None
   counts_before_submission = is_practice and has_open_attempt

   if counts_before_submission:
      rows.attempt.agent_turns_before_submit = rows.attempt.agent_turns_before_submit + 1

   is_on_an_item = mode in (PRACTICE, AFTER_SUBMISSION)

   return PreparedTurn(
      conversation=conversation,
      screen=screen,
      packet=packet,
      rows=rows,
      request=agent_request(rendered),
      student_turn=student_turn,
      turns_on_item=prior_on_item + 1 if is_on_an_item else 0,
      turns_in_conversation=prior_in_conversation + 1,
   )


def key_forms_for(rows):
   if rows.item is None:
      return None

   return agent_checks.key_forms(rows.item)


def failure_kind(raised):
   if isinstance(raised, BudgetStopped):
      caps = tuple(raised.caps)

      if SUBSCRIPTION_MINUTE_RATE in caps:
         return agent_copy.MINUTE_CAP

      if SUBSCRIPTION_DAILY_CAP in caps:
         return agent_copy.DAILY_CAP

      if NO_PROVIDER_LINK in caps:
         return agent_copy.UNAVAILABLE

      return agent_copy.DAILY_CAP

   if isinstance(raised, DevSpendCapExceeded):
      return agent_copy.DAILY_CAP

   if isinstance(raised, RefusedBeforeWire):
      return agent_copy.UNAVAILABLE

   is_bounded = isinstance(raised, ProviderCallFailed)
   failure_type = raised.exception_type if is_bounded else type(raised).__name__

   if failure_type == SubscriptionLimitReached.__name__:
      return agent_copy.USAGE_LIMIT

   if failure_type == SubscriptionAuthFailed.__name__:
      return agent_copy.SIGN_IN

   return agent_copy.UNAVAILABLE


def _is_epoch(value):
   return isinstance(value, (int, float)) and not isinstance(value, bool)


def reset_moment(settings):
   """When the subscription said its usage window reopens: the five-hour window's resetsAt when it
   reported one, else the seven-day window's, read from the provider the agent's subscription link
   wraps. None when neither was reported."""
   for link in links_from_settings(settings, LINKS_FIELD, PROVIDER_FIELD):
      is_subscription = link.name == SUBSCRIPTION_LINK

      if not is_subscription:
         continue

      info = getattr(link.provider, "last_rate_limit", None) or {}
      windows = info.get("unifiedWindows") or {}

      for window_name in RESET_WINDOWS:
         resets_at = (windows.get(window_name) or {}).get("resetsAt")

         if _is_epoch(resets_at):
            return datetime.fromtimestamp(resets_at, timezone.utc)

   return None


def reset_time_words(moment):
   return f"{moment:%H:%M} UTC on {moment.day} {moment:%B}"


def failure_event(settings, kind):
   is_usage_limit = kind == agent_copy.USAGE_LIMIT

   if not is_usage_limit:
      return error_event(kind)

   moment = reset_moment(settings)

   if moment is None:
      return error_event(kind, resets_at=None)

   return error_event(kind, resets_at=moment.isoformat(), reset_time=reset_time_words(moment))


def withheld_already_recorded(db, user_id, day):
   statement = (
      select(models.AuditLog.detail)
      .where(models.AuditLog.action == WITHHELD_ACTION)
      .where(models.AuditLog.actor == user_id)
   )

   for detail in db.scalars(statement).all():
      recorded = json.loads(detail) if detail else {}

      if recorded.get("day") == day:
         return True

   return False


def record_withheld(db, user_id, verdict, turn_id, now):
   """One row per user per day, the bound guard.py keeps for a pacing refusal. The detail names the
   check and the turn, never the text."""
   day = now.date().isoformat()

   if withheld_already_recorded(db, user_id, day):
      return

   detail = {"check": verdict.check, "turn_id": turn_id, "day": day}
   write_audit(db, user_id, WITHHELD_ACTION, f"agent_turns:{turn_id}", detail, now=now)


def released_event(sentence, sentence_screen, state):
   """The screen keeps each sentence's leading space and releases the decline without one, so the
   decline gets a space when a sentence came before it."""
   is_decline = sentence_screen.withheld is not None and sentence == sentence_screen.decline
   follows_text = len(state.released) > 0
   delta = f" {sentence}" if is_decline and follows_text else sentence
   state.released.append(delta)

   return event(TEXT_EVENT, {"delta": delta})


def screened_text(chain, request, sentence_screen, state, clock):
   """Text events for the sentences the screen releases. A withheld sentence or a late first delta
   stops reading, and closing the chain's stream there leaves the guard's worst-case charge."""
   events = chain.stream(request)
   call_started = clock()
   saw_text = False

   try:
      for provider_event in events:
         is_text = isinstance(provider_event, dict) and provider_event.get("type") == "text"

         if not is_text:
            continue

         is_first = not saw_text
         saw_text = True
         is_late = is_first and clock() - call_started > FIRST_TEXT_BOUND_SECONDS

         if is_late:
            state.late_first_text = True
            return

         for sentence in sentence_screen.feed(provider_event["delta"]):
            yield released_event(sentence, sentence_screen, state)

         if sentence_screen.withheld is not None:
            return

      for sentence in sentence_screen.flush():
         yield released_event(sentence, sentence_screen, state)
   except Exception as raised:
      state.failure = raised
   finally:
      events.close()


def reply_moment(now, clock, started):
   return now + max(timedelta(seconds=clock() - started), REPLY_STAMP_GAP)


def store_reply(db, prepared, text, outcome, link, moment):
   screen = prepared.screen

   return conversations.append_turn(
      db,
      prepared.conversation,
      conversations.AGENT,
      text,
      moment,
      move=prepared.packet.move,
      mode=prepared.packet.mode,
      item_id=screen.get("item_id"),
      attempt_id=screen.get("attempt_id"),
      outcome=outcome,
      model=prepared.request.model,
      link=link,
   )


def end_event(prepared, turn_id, outcome):
   return event(END_EVENT, {
      "turn_id": turn_id,
      "outcome": outcome,
      "turns_on_item": prepared.turns_on_item,
      "turns_in_conversation": prepared.turns_in_conversation,
   })


def run_turn(settings, db, user, body, now, clock=None):
   """clock is the elapsed-time source, the module's monotonic unless a caller passes another."""
   clock = clock or monotonic
   started = clock()

   try:
      prepared = prepare_turn(settings, db, user, body, now)
   except TurnRefused as refused:
      db.rollback()
      log_turn(None, refused.kind, None, clock, started)
      yield error_event(refused.kind, status=refused.status, conversation_ceiling=refused.conversation_ceiling)
      return

   db.commit()
   student_turn_id = prepared.student_turn.id

   yield event(START_EVENT, {
      "conversation_id": prepared.conversation.id,
      "turn_id": student_turn_id,
      "screen_line": prepared.packet.screen_line,
      "can_see": list(prepared.screen.keys()),
   })

   chain = chain_for(settings, db, user.id, LINKS_FIELD, PROVIDER_FIELD, settings.agent_caps)

   if chain is None:
      log_turn(student_turn_id, agent_copy.UNAVAILABLE, None, clock, started)
      yield error_event(agent_copy.UNAVAILABLE)
      return

   sentence_screen = SentenceScreen(prepared.packet, key_forms_for(prepared.rows))
   state = StreamState()

   try:
      yield from screened_text(chain, prepared.request, sentence_screen, state, clock)
   except GeneratorExit:
      has_released = len(state.released) > 0

      if has_released:
         moment = reply_moment(now, clock, started)
         store_reply(db, prepared, "".join(state.released), STOPPED, chain.served_by, moment)

      db.commit()
      log_turn(student_turn_id, STOPPED, chain.served_by, clock, started)
      raise

   has_released = len(state.released) > 0
   stopped_early = state.failure is not None or state.late_first_text
   is_withheld = sentence_screen.withheld is not None
   failed_before_any_text = stopped_early and not has_released

   if failed_before_any_text:
      kind = agent_copy.UNAVAILABLE if state.late_first_text else failure_kind(state.failure)
      db.commit()
      log_turn(student_turn_id, kind, chain.served_by, clock, started)
      yield failure_event(settings, kind)
      return

   if is_withheld:
      outcome = WITHHELD
   elif stopped_early:
      outcome = INCOMPLETE
   else:
      outcome = COMPLETE

   moment = reply_moment(now, clock, started)
   reply_turn = store_reply(db, prepared, "".join(state.released), outcome, chain.served_by, moment)

   if is_withheld:
      record_withheld(db, user.id, sentence_screen.withheld, reply_turn.id, now)

   db.flush()

   try:
      yield end_event(prepared, reply_turn.id, outcome)
   finally:
      db.commit()
      log_turn(reply_turn.id, outcome, chain.served_by, clock, started)
