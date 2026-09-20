"""GET /me: the user, the exam date and the purge date, per 06's API surface."""
from fastapi import APIRouter, Depends

from app.api.deps import current_user

router = APIRouter(tags=["me"])


@router.get("/me")
def read_me(user=Depends(current_user)):
   return {
      "id": user.id,
      "display_name": user.display_name,
      "exam_date": user.exam_date,
      "purge_after": user.purge_after,
   }
