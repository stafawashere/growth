"""GET /progress, the due counts home reads, per 06's API surface.

GET /progress serves the due counts home reads; the numbers come from app/session/preview.py, which
runs the Session assembly rule without persisting anything. The progress screen reads its two
sections from their own paths, GET /progress/mastery for the map and GET /progress/calibration for
the curve beneath it, so home's read stays as cheap as it was.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import current_user, get_db, get_settings
from app.progress import calibration, mastery
from app.session import preview, repository

router = APIRouter(tags=["progress"])


@router.get("/progress")
def read_progress(
   today: str | None = None,
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   """A client that sends today to POST /sessions sends the same day here, as a query parameter."""
   context = settings.session_context

   try:
      day, rng = preview.user_assembly_inputs(settings.rng_seed, user.id, today)
   except preview.UnreadableDay as unreadable:
      raise HTTPException(status_code=422, detail=str(unreadable)) from unreadable

   return preview.queue_preview(db, user.id, context.graph, context.bank, day, rng)


@router.get("/progress/calibration")
def read_calibration(
   today: str | None = None,
   db=Depends(get_db),
   user=Depends(current_user),
):
   """The calibration curve beneath the mastery map (08, "Progress"), over the 30 days ending on
   today. Below 30 counted attempts the payload says how many more are needed and carries no bins.
   """
   try:
      day = preview.assembly_day(today)
   except preview.UnreadableDay as unreadable:
      raise HTTPException(status_code=422, detail=str(unreadable)) from unreadable

   return calibration.user_calibration(db, user.id, day)


@router.get("/progress/mastery")
def read_mastery_map(
   today: str | None = None,
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   """The mastery map (08, "Progress"): one node per skill, grouped by unit, each in one of the
   five node states, read off skills_state and today's retrievability."""
   try:
      day = preview.assembly_day(today)
   except preview.UnreadableDay as unreadable:
      raise HTTPException(status_code=422, detail=str(unreadable)) from unreadable

   states = repository.load_states(db, user.id)
   graph = settings.session_context.graph

   return mastery.mastery_map(db, user.id, states, graph, day, settings.content_root)
