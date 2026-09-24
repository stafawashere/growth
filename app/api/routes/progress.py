"""GET /progress, the due counts home reads, per 06's API surface.

In P1 the progress screen is not built (11-phased-delivery.md, item 17), so the route serves the
due counts only; the mastery map and calibration arrive with that screen. The numbers come from
app/session/preview.py, which runs the Session assembly rule without persisting anything.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import current_user, get_db, get_settings
from app.progress import calibration
from app.session import preview

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
