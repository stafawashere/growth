"""The live tutor's settings routes (docs/agent/architecture.md, "The panel and the settings views").

The Tutor tab in Settings reads and changes what the tutor remembers, the stored conversations,
the pause switch and the tutoring profile. Every route needs a session, every query is scoped by
the signed-in user, and a row of another user answers 404 exactly as a missing one does. Clearing
everything needs the typed phrase "forget everything" (docs/agent/design.md, "Memory in
settings").

POST /agent/turns answers text/event-stream over app/agent/turn.py run_turn (docs/agent/
architecture.md, Streaming end to end). The request's own database session commits when the
handler returns, which is before the stream has finished, so the stream opens its own session on
the application's engine and holds it for the life of the stream: run_turn commits the student's
turn before the first byte and the reply after the end event. The route logs nothing of the turn;
run_turn logs the turn id, the outcome, the link and the elapsed time. When the student presses Stop
the client aborts the request, and the response closes the stream at once, inside the stream's
session, so run_turn stores the stopped reply then rather than whenever the garbage collector
reaches the abandoned generator.
"""
import json
from contextlib import closing

import anyio
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session as OrmSession

from app.agent import consolidate, conversations, memory
from app.agent.turn import run_turn
from app.api.deps import current_user, get_db, get_settings
from app.auth import service as auth_service
from app.db import models
from app.experiments import switches

router = APIRouter(tags=["agent"])

CLEAR_CONFIRMATION = "forget everything"
EVENT_STREAM = "text/event-stream"
STREAM_HEADERS = {"Cache-Control": "no-store", "X-Accel-Buffering": "no"}
PROFILE_EXPERIMENT = "tutor_profile"
EXPERIMENT_ABSENT = "absent"
KIND_LABELS = (
   (memory.PREFERENCE, "How you like to be helped"),
   (memory.CONFUSION, "Confusions in your words"),
   (memory.STATED_DIFFICULTY, "What you said was hard"),
   (memory.EPISODE, "Last conversation"),
)


def fields_of(payload):
   is_object = isinstance(payload, dict)

   if not is_object:
      raise HTTPException(status_code=400, detail="the request body must be a JSON object")

   return payload


def memory_view(entry):
   return {
      "id": entry.id,
      "kind": entry.kind,
      "text": entry.text,
      "skill_ids": list(entry.skill_ids or ()),
      "created_at": entry.created_at,
      "source_conversation_id": entry.source_conversation_id,
      "editable": entry.kind in memory.STUDENT_EDITABLE_KINDS,
   }


def memories_view(db, user_id, now):
   entries = sorted(memory.active_entries(db, user_id, now), key=lambda entry: (entry.created_at, entry.id), reverse=True)
   groups = []

   for kind, label in KIND_LABELS:
      of_kind = [memory_view(entry) for entry in entries if entry.kind == kind]
      groups.append({"kind": kind, "label": label, "entries": of_kind})

   return {"memory_paused": memory.is_memory_paused(db, user_id), "groups": groups}


def settings_view(db, user_id):
   return {"memory_paused": memory.is_memory_paused(db, user_id)}


@router.get("/agent/memories")
def read_memories(db=Depends(get_db, scope="function"), user=Depends(current_user)):
   return memories_view(db, user.id, auth_service.utc_now())


@router.put("/agent/memories/{memory_id}")
def edit_memory(
   memory_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
   user=Depends(current_user),
):
   fields = fields_of(payload)

   try:
      entry = memory.edit_entry(db, user.id, memory_id, fields.get("text"), auth_service.utc_now())
   except memory.MemoryNotFound as missing:
      raise HTTPException(status_code=404, detail="no such memory entry") from missing
   except memory.MemoryRefused as refused:
      raise HTTPException(status_code=400, detail=str(refused)) from refused

   return memory_view(entry)


@router.delete("/agent/memories/{memory_id}")
def delete_memory(memory_id: str, db=Depends(get_db, scope="function"), user=Depends(current_user)):
   try:
      entry = memory.delete_entry(db, user.id, memory_id, auth_service.utc_now())
   except memory.MemoryNotFound as missing:
      raise HTTPException(status_code=404, detail="no such memory entry") from missing

   return {"deleted": entry.id}


@router.delete("/agent/memories")
def clear_memories(payload: dict = Body(default=None), db=Depends(get_db, scope="function"), user=Depends(current_user)):
   fields = fields_of(payload)
   is_confirmed = fields.get("confirmation") == CLEAR_CONFIRMATION

   if not is_confirmed:
      raise HTTPException(status_code=400, detail=f'type "{CLEAR_CONFIRMATION}" to clear everything')

   removed = memory.clear_all(db, user.id, auth_service.utc_now())

   return {"cleared": removed}


@router.get("/agent/conversations")
def read_conversations(db=Depends(get_db, scope="function"), user=Depends(current_user)):
   return {"conversations": conversations.list_conversations(db, user.id, auth_service.utc_now())}


@router.get("/agent/conversations/{conversation_id}")
def read_conversation(conversation_id: str, db=Depends(get_db, scope="function"), user=Depends(current_user)):
   try:
      return conversations.read_conversation(db, user.id, conversation_id)
   except conversations.ConversationNotFound as missing:
      raise HTTPException(status_code=404, detail="no such conversation") from missing


@router.post("/agent/conversations/{conversation_id}/close")
def close_conversation(conversation_id: str, db=Depends(get_db, scope="function"), user=Depends(current_user)):
   try:
      conversation = conversations.owned_conversation(db, user.id, conversation_id)
   except conversations.ConversationNotFound as missing:
      raise HTTPException(status_code=404, detail="no such conversation") from missing

   now = auth_service.utc_now()
   was_open = conversation.closed_at is None
   conversations.close_conversation(db, conversation, now)
   has_turns = conversation.turn_count > 0
   should_consolidate = was_open and has_turns

   if should_consolidate:
      consolidate.enqueue(db, user.id, conversation, now)

   return {"closed": conversation_id}


def sse_frame(turn_event):
   return f"event: {turn_event['event']}\ndata: {json.dumps(turn_event['data'])}\n\n"


class ClosingStreamingResponse(StreamingResponse):
   """Starlette leaves a sync body open when the client disconnects. A generator collected in a
   reference cycle has its weak references cleared before it is closed, so run_turn's Stop path met
   a conversation SQLAlchemy could no longer track and stored nothing."""

   def __init__(self, generator, **kwargs):
      super().__init__(generator, **kwargs)
      self.generator = generator

   async def stream_response(self, send):
      try:
         await super().stream_response(send)
      finally:
         with anyio.CancelScope(shield=True):
            await anyio.to_thread.run_sync(self.generator.close)


def turn_stream(request, user_id, body, now):
   settings = request.app.state.settings

   with OrmSession(request.app.state.engine) as db:
      user = db.get(models.User, user_id)

      with closing(run_turn(settings, db, user, body, now)) as turn_events:
         for turn_event in turn_events:
            yield sse_frame(turn_event)


@router.post("/agent/turns")
def post_turn(request: Request, payload: dict = Body(default=None), user=Depends(current_user)):
   return ClosingStreamingResponse(
      turn_stream(request, user.id, payload, auth_service.utc_now()),
      media_type=EVENT_STREAM,
      headers=dict(STREAM_HEADERS),
   )


@router.delete("/agent/conversations/{conversation_id}")
def delete_conversation(conversation_id: str, db=Depends(get_db, scope="function"), user=Depends(current_user)):
   try:
      conversations.delete_conversation(db, user.id, conversation_id, auth_service.utc_now())
   except conversations.ConversationNotFound as missing:
      raise HTTPException(status_code=404, detail="no such conversation") from missing

   return {"deleted": conversation_id}


@router.get("/agent/settings")
def read_agent_settings(db=Depends(get_db, scope="function"), user=Depends(current_user)):
   return settings_view(db, user.id)


@router.put("/agent/settings")
def update_agent_settings(payload: dict = Body(default=None), db=Depends(get_db, scope="function"), user=Depends(current_user)):
   fields = fields_of(payload)
   paused = fields.get("memory_paused")
   is_boolean = isinstance(paused, bool)

   if not is_boolean:
      raise HTTPException(status_code=400, detail="memory_paused must be true or false")

   memory.set_paused(db, user.id, paused, auth_service.utc_now())

   return settings_view(db, user.id)


def current_profile(db, user_id):
   return (
      db.query(models.TutorProfile)
      .filter(models.TutorProfile.user_id == user_id)
      .order_by(models.TutorProfile.version.desc())
      .first()
   )


def profile_experiment_state(db, user_id, settings, now):
   is_defined = PROFILE_EXPERIMENT in switches.DEFINITIONS

   if not is_defined:
      return EXPERIMENT_ABSENT

   default_state = settings.experiment_default_state or switches.OFF

   return switches.experiment_row(db, user_id, PROFILE_EXPERIMENT, default_state, now).state


@router.get("/agent/profile")
def read_profile(db=Depends(get_db, scope="function"), settings=Depends(get_settings), user=Depends(current_user)):
   profile = current_profile(db, user.id)
   has_profile = profile is not None

   return {
      "profile": profile.body if has_profile else None,
      "version": profile.version if has_profile else None,
      "experiment": profile_experiment_state(db, user.id, settings, auth_service.utc_now()),
   }
