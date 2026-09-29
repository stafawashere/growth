"""The live tutor's settings routes (docs/agent/architecture.md, "The panel and the settings views").

The Tutor tab in Settings reads and changes what the tutor remembers, the stored conversations,
the pause switch and the tutoring profile. Every route needs a session, every query is scoped by
the signed-in user, and a row of another user answers 404 exactly as a missing one does. Clearing
everything needs the typed phrase "forget everything" (docs/agent/design.md, "Memory in
settings"). The turn route arrives with Slice 4 of docs/agent/build-plan.md.
"""
from fastapi import APIRouter, Body, Depends, HTTPException

from app.agent import conversations, memory
from app.api.deps import current_user, get_db, get_settings
from app.auth import service as auth_service
from app.db import models
from app.experiments import switches

router = APIRouter(tags=["agent"])

CLEAR_CONFIRMATION = "forget everything"
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
