"""Conversations with the live tutor and their turns (docs/agent/architecture.md, "The memory store").

A conversation stays open while turns keep arriving: a turn more than 30 minutes after the last one
closes it and opens a new one, which is_idle decides, and the panel may close one explicitly. The
student reads the conversations of the last 30 days in Settings and deletes any of them, turns
and all, and each delete writes agent_conversation_deleted with the ids and the turn count, never
the text (docs/plan/09-security-and-privacy.md, 2026-09-29 amendment). A turn whose figure was shown
reads back with the figure's title, which the Settings view shows under it.
"""
from datetime import timedelta

from sqlalchemy import delete, func, select

from app.agent.drawing.record import shown_spec
from app.agent.memory import parse_moment
from app.auth.service import as_iso, new_id, write_audit
from app.db import models

STUDENT = "student"
AGENT = "agent"
TURN_ROLES = (STUDENT, AGENT)
IDLE_AFTER = timedelta(minutes=30)
LISTED_FOR = timedelta(days=30)
DELETED_ACTION = "agent_conversation_deleted"


class ConversationNotFound(LookupError):
   pass


def open_conversation(db, user_id, screen_kind, now):
   stamp = as_iso(now)
   conversation = models.AgentConversation(
      id=new_id("ACV"),
      user_id=user_id,
      opened_at=stamp,
      last_turn_at=stamp,
      closed_at=None,
      consolidated_at=None,
      opened_on_screen=screen_kind,
      turn_count=0,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(conversation)
   db.flush()

   return conversation


def is_idle(conversation, now):
   return now - parse_moment(conversation.last_turn_at) > IDLE_AFTER


def append_turn(
   db,
   conversation,
   role,
   text,
   now,
   screen=None,
   move=None,
   mode=None,
   item_id=None,
   attempt_id=None,
   outcome=None,
   model=None,
   link=None,
   figure=None,
):
   is_known_role = role in TURN_ROLES

   if not is_known_role:
      raise ValueError(f"{role!r} is not a turn role")

   stamp = as_iso(now)
   turn = models.AgentTurn(
      id=new_id("ATN"),
      conversation_id=conversation.id,
      user_id=conversation.user_id,
      role=role,
      text=text,
      screen=screen,
      move=move,
      mode=mode,
      item_id=item_id,
      attempt_id=attempt_id,
      outcome=outcome,
      model=model,
      link=link,
      figure=figure,
      created_at=stamp,
      updated_at=stamp,
   )
   db.add(turn)
   conversation.turn_count = conversation.turn_count + 1
   conversation.last_turn_at = stamp
   conversation.updated_at = stamp
   db.flush()

   return turn


def close_conversation(db, conversation, now):
   is_open = conversation.closed_at is None

   if is_open:
      stamp = as_iso(now)
      conversation.closed_at = stamp
      conversation.updated_at = stamp
      db.flush()

   return conversation


def conversation_summary(conversation):
   return {
      "id": conversation.id,
      "opened_at": conversation.opened_at,
      "last_turn_at": conversation.last_turn_at,
      "closed_at": conversation.closed_at,
      "opened_on_screen": conversation.opened_on_screen,
      "turn_count": conversation.turn_count,
   }


def shown_figure_title(figure):
   """The title the Settings view shows under a turn whose figure was shown, or None."""
   spec = shown_spec(figure)

   return None if spec is None else spec.get("title")


def turn_view(turn):
   return {
      "id": turn.id,
      "role": turn.role,
      "text": turn.text,
      "created_at": turn.created_at,
      "outcome": turn.outcome,
      "figure_title": shown_figure_title(turn.figure),
   }


def list_conversations(db, user_id, now):
   earliest = as_iso(now - LISTED_FOR)
   statement = (
      select(models.AgentConversation)
      .where(models.AgentConversation.user_id == user_id)
      .where(models.AgentConversation.opened_at >= earliest)
      .order_by(models.AgentConversation.opened_at.desc(), models.AgentConversation.id.desc())
   )

   return [conversation_summary(conversation) for conversation in db.scalars(statement).all()]


def owned_conversation(db, user_id, conversation_id):
   conversation = db.get(models.AgentConversation, conversation_id)
   is_owned = conversation is not None and conversation.user_id == user_id

   if not is_owned:
      raise ConversationNotFound(conversation_id)

   return conversation


def read_conversation(db, user_id, conversation_id):
   conversation = owned_conversation(db, user_id, conversation_id)
   statement = (
      select(models.AgentTurn)
      .where(models.AgentTurn.conversation_id == conversation.id)
      .where(models.AgentTurn.user_id == user_id)
      .order_by(models.AgentTurn.created_at, models.AgentTurn.id)
   )
   turns = db.scalars(statement).all()

   return {**conversation_summary(conversation), "turns": [turn_view(turn) for turn in turns]}


def delete_conversation(db, user_id, conversation_id, now):
   conversation = owned_conversation(db, user_id, conversation_id)
   owned_turns = (models.AgentTurn.conversation_id == conversation.id) & (models.AgentTurn.user_id == user_id)
   turn_count = db.scalar(select(func.count()).select_from(models.AgentTurn).where(owned_turns))

   db.execute(delete(models.AgentTurn).where(owned_turns))
   db.delete(conversation)
   db.flush()

   detail = {"conversation_id": conversation_id, "turns_deleted": turn_count}
   write_audit(db, user_id, DELETED_ACTION, f"agent_conversations:{conversation_id}", detail, now)

   return detail
