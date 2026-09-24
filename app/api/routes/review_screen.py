"""GET /review, the student's review screen (08, "Review"), reached from home.

The operator's queue stays at /review-queue in app/api/routes/review.py; the two share no rows.
"""
from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import current_user, get_db, get_settings
from app.review.screen import review_screen
from app.session import preview, repository

router = APIRouter(tags=["review"])


@router.get("/review")
def read_review(
   today: str | None = None,
   db=Depends(get_db),
   settings=Depends(get_settings),
   user=Depends(current_user),
):
   try:
      day = preview.assembly_day(today)
   except preview.UnreadableDay as unreadable:
      raise HTTPException(status_code=422, detail=str(unreadable)) from unreadable

   history = repository.load_attempts_history(db, user.id)
   archetypes = settings.session_context.archetypes

   point_types = settings.frq.point_types if settings.frq is not None else None

   return review_screen(db, user.id, archetypes, history, day, point_types=point_types)
