"""POST /purge: the destructive path, behind a typed confirmation and a fresh re-authentication.

docs/plan/09-security-and-privacy.md requires both and does not fix the confirmation string, so the
string is fixed here and the interface displays it. The order of the checks is the order of the
gate in docs/plan/11-phased-delivery.md test 24: an unconfirmed request never reaches the
re-authentication check, and neither refusal deletes anything. The audit entry is app/session/purge.py's
to write, so this route writes none of its own.

A refused token is answered with a 401 response rather than a raised exception, as the export route
does, so the request still commits and the single-use token consume_reauth cleared stays cleared.
"""
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.api.deps import current_session, current_user, get_db, get_settings
from app.auth import service as auth_service

router = APIRouter(tags=["purge"])

PURGE_CONFIRMATION = "DELETE EVERYTHING"


@router.post("/purge")
def purge(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   auth_session=Depends(current_session),
   user=Depends(current_user),
):
   fields = payload or {}
   is_confirmed = fields.get("confirmation") == PURGE_CONFIRMATION

   if not is_confirmed:
      raise HTTPException(
         status_code=400,
         detail=f"the purge needs the typed confirmation {PURGE_CONFIRMATION!r}",
      )

   now = auth_service.utc_now()
   is_reauthenticated = auth_service.consume_reauth(db, auth_session, fields.get("reauth_token"), now)

   if not is_reauthenticated:
      return JSONResponse(
         status_code=401,
         content={"detail": "the purge needs a fresh passkey re-authentication"},
      )

   deleted = settings.resolve_purge_hook()(db, user.id, now)

   return {"purged": True, "deleted": deleted}
