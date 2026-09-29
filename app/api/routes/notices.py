"""GET /notices: the signed-in student's notices of AI calls newer than a given id.

The notices are recorded by the provider guard (app/providers/notices.py) and held in this process
only. The route reads the caller's own buffer and no other, so one student never sees another's.
"""
from fastapi import APIRouter, Depends, Query

from app.api.deps import current_user
from app.providers import notices

router = APIRouter(tags=["notices"])


@router.get("/notices")
def read_notices(after: int = Query(default=0, ge=0), user=Depends(current_user)):
   found = notices.notices_for(user.id, after)
   latest = max((notice["id"] for notice in found), default=after)

   return {"notices": found, "latest": latest}
