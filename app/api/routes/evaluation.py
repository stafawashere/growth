"""The P7 evaluation harness over HTTP: the metrics view, the A/B switches, the six-week checkpoint,
the concept probe and the representation matrix (docs/plan/11 P7 scope items 3 to 7).

The metrics view is for the operator and is reached from settings, never from the bar: 08 rules out
a dashboard in the student's daily path, and the metrics are the operator's evidence of whether the
app teaches, not the student's next action. Every value it returns carries its denominator.
"""
from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends, HTTPException

from app.api.deps import current_user, get_db, get_settings
from app.checkpoint import probe as probe_service
from app.checkpoint import service as checkpoint_service
from app.experiments import analysis, switches
from app.progress import learning_metrics
from app.progress.attempt_log import load_attempts
from app.progress.representations import representation_matrix
from app.session import preview

router = APIRouter(tags=["evaluation"])

OFF_WHEN_UNSET = switches.OFF


def day_of(today):
   try:
      return preview.assembly_day(today)
   except preview.UnreadableDay as unreadable:
      raise HTTPException(status_code=422, detail=str(unreadable)) from unreadable


def moment_of(today):
   """A stated day stands for noon UTC on that day, so tests and clients that pin the day pin the
   stored stamps too; no day means now."""
   if today is None:
      return datetime.now(timezone.utc)

   day = day_of(today)

   return datetime(day.year, day.month, day.day, 12, tzinfo=timezone.utc)


def default_state(settings):
   return settings.experiment_default_state or OFF_WHEN_UNSET


def body_fields(payload):
   return payload if isinstance(payload, dict) else {}


@router.get("/progress/metrics")
def read_metrics(
   today: str | None = None,
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   day = day_of(today)
   archetypes = settings.session_context.archetypes
   attempts = load_attempts(db, user.id, archetypes)

   return {
      "as_of": day.isoformat(),
      "metrics": learning_metrics.learning_metrics(db, user.id, archetypes, day),
      "experiments": [
         analysis.comparison_view(comparison)
         for comparison in analysis.comparisons(db, user.id, attempts)
      ],
   }


@router.get("/progress/representations")
def read_representation_matrix(
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   context = settings.session_context
   attempts = load_attempts(db, user.id, context.archetypes)
   records = getattr(settings.snapshot, "representations", None) or {}
   names = {
      representation_id: record.get("name", representation_id)
      for representation_id, record in records.items()
   }

   return representation_matrix(attempts, context.archetypes, context.graph.conversion_pairs, names)


@router.get("/settings/experiments")
def read_experiments(
   today: str | None = None,
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   return {"experiments": switches.switch_view(db, user.id, default_state(settings), moment_of(today))}


@router.post("/settings/experiments/{name}")
def set_experiment(
   name: str,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   fields = body_fields(payload)
   now = moment_of(fields.get("today"))

   try:
      switches.set_state(db, user.id, name, fields.get("state"), default_state(settings), now)
   except ValueError as refused:
      raise HTTPException(status_code=422, detail=str(refused)) from refused

   return {"experiments": switches.switch_view(db, user.id, default_state(settings), now)}


@router.get("/checkpoints")
def read_checkpoints(
   today: str | None = None,
   db=Depends(get_db),
   user=Depends(current_user),
):
   day = day_of(today)

   return {
      "availability": checkpoint_service.availability(db, user.id, day),
      "history": checkpoint_service.history(db, user.id),
      "expected_effect": {
         "low": checkpoint_service.EXPECTED_EFFECT_LOW,
         "high": checkpoint_service.EXPECTED_EFFECT_HIGH,
      },
   }


@router.post("/checkpoints")
def start_checkpoint(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   user=Depends(current_user),
):
   now = moment_of(body_fields(payload).get("today"))

   try:
      row = checkpoint_service.start(db, user.id, now)
   except checkpoint_service.CheckpointRefused as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   return checkpoint_service.checkpoint_view(db, row)


def owned_checkpoint(db, user, checkpoint_id):
   try:
      return checkpoint_service.owned(db, user.id, checkpoint_id)
   except LookupError as missing:
      raise HTTPException(status_code=404, detail="no such checkpoint") from missing


@router.get("/checkpoints/{checkpoint_id}")
def read_checkpoint(checkpoint_id: str, db=Depends(get_db), user=Depends(current_user)):
   return checkpoint_service.checkpoint_view(db, owned_checkpoint(db, user, checkpoint_id))


@router.post("/checkpoints/{checkpoint_id}/scores")
def score_checkpoint_part(
   checkpoint_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   user=Depends(current_user),
):
   fields = body_fields(payload)
   owned_checkpoint(db, user, checkpoint_id)

   try:
      checkpoint_service.record_score(
         db,
         user.id,
         checkpoint_id,
         fields.get("record_id"),
         fields.get("points_earned"),
         moment_of(fields.get("today")),
      )
   except checkpoint_service.CheckpointRefused as refused:
      raise HTTPException(status_code=422, detail=str(refused)) from refused

   return checkpoint_service.checkpoint_view(db, owned_checkpoint(db, user, checkpoint_id))


@router.post("/checkpoints/{checkpoint_id}/finish")
def finish_checkpoint(
   checkpoint_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   user=Depends(current_user),
):
   owned_checkpoint(db, user, checkpoint_id)

   try:
      row = checkpoint_service.finish(db, user.id, checkpoint_id, moment_of(body_fields(payload).get("today")))
   except checkpoint_service.CheckpointRefused as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   return checkpoint_service.checkpoint_view(db, row)


@router.get("/probe")
def read_probe(today: str | None = None, db=Depends(get_db), user=Depends(current_user)):
   return {
      "availability": probe_service.availability(db, user.id, day_of(today)),
      "history": probe_service.history(db, user.id),
   }


@router.post("/probe")
def start_probe(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   ingests = getattr(settings.session_context.bank, "ensure_ingested", None)

   if ingests is not None:
      ingests()

   try:
      row = probe_service.start(db, user.id, moment_of(body_fields(payload).get("today")))
   except probe_service.ProbeRefused as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   return probe_service.administration_view(db, row)


def owned_administration(db, user, administration_id):
   try:
      return probe_service.owned(db, user.id, administration_id)
   except LookupError as missing:
      raise HTTPException(status_code=404, detail="no such probe") from missing


@router.get("/probe/{administration_id}/next")
def next_probe_item(administration_id: str, db=Depends(get_db), user=Depends(current_user)):
   owned_administration(db, user, administration_id)

   try:
      item = probe_service.next_item(db, user.id, administration_id)
   except probe_service.ProbeRefused as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   return {"item": item}


@router.post("/probe/{administration_id}/answers")
def answer_probe_item(
   administration_id: str,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   fields = body_fields(payload)
   owned_administration(db, user, administration_id)

   try:
      probe_service.answer(
         db,
         user.id,
         administration_id,
         fields.get("item_id"),
         fields.get("answer") or {},
         fields.get("elapsed_ms"),
         settings.session_context.errors,
         moment_of(fields.get("today")),
      )
   except probe_service.ProbeRefused as refused:
      raise HTTPException(status_code=409, detail=str(refused)) from refused

   return probe_service.administration_view(db, owned_administration(db, user, administration_id))
