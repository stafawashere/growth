"""GET /me: the user, the exam date and the purge date, per 06's API surface, plus the username the
account menu shows. PUT /me renames the display name, which is all a student may change about the
profile; the username is the sign-in name and never changes after sign-up."""
from fastapi import APIRouter, Body, Depends, HTTPException

from app.api.deps import current_user, get_db
from app.auth import service

router = APIRouter(tags=["me"])

DISPLAY_NAME_LIMIT = 60


@router.get("/me")
def read_me(user=Depends(current_user)):
   return {
      "id": user.id,
      "username": user.username,
      "display_name": user.display_name,
      "exam_date": user.exam_date,
      "purge_after": user.purge_after,
   }


@router.put("/me")
def rename(payload: dict = Body(default=None), db=Depends(get_db, scope="function"), user=Depends(current_user)):
   is_object = isinstance(payload, dict)

   if not is_object:
      raise HTTPException(status_code=400, detail="the request body must be a JSON object")

   offered = payload.get("display_name")
   is_text = isinstance(offered, str)
   name = offered.strip() if is_text else ""
   is_blank = name == ""
   is_too_long = len(name) > DISPLAY_NAME_LIMIT

   if is_blank or is_too_long:
      raise HTTPException(status_code=400, detail=f"a display name is 1 to {DISPLAY_NAME_LIMIT} characters")

   user.display_name = name
   user.updated_at = service.as_iso(service.utc_now())
   db.flush()

   return read_me(user)
