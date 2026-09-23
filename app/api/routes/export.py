"""POST /export and GET /export/{id}, per 06's API surface.

09 forces re-authentication for exporting. A refused token is answered with a 401 response rather
than a raised exception, so the request still commits and the single-use token consume_reauth
cleared stays cleared. A database with no directory to hold archives answers 503 before the token
is consumed, so the student's re-authentication is not spent on an export that cannot be written.
"""
from fastapi import APIRouter, Body, Depends, HTTPException, Response
from fastapi.responses import JSONResponse

from app.api.deps import current_session, current_user, get_db
from app.auth import service as auth_service
from app.export.archive import ExportUnavailable, archive_directory_for, produce_export, read_export

router = APIRouter(tags=["export"])


def archive_directory_or_503(db):
   try:
      return archive_directory_for(db.get_bind().engine)
   except ExportUnavailable as unavailable:
      raise HTTPException(status_code=503, detail=str(unavailable)) from unavailable


@router.post("/export")
def create_export(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   auth_session=Depends(current_session),
   user=Depends(current_user),
):
   fields = payload or {}
   archive_directory = archive_directory_or_503(db)
   now = auth_service.utc_now()
   is_reauthenticated = auth_service.consume_reauth(db, auth_session, fields.get("reauth_token"), now)

   if not is_reauthenticated:
      return JSONResponse(
         status_code=401,
         content={"detail": "an export needs a fresh passkey re-authentication"},
      )

   job = produce_export(db, archive_directory, user.id, now)

   return {"id": job.id, "status": job.state, "created_at": job.created_at}


@router.get("/export/{export_id}")
def fetch_export(
   export_id: str,
   db=Depends(get_db),
   user=Depends(current_user),
):
   archive_directory = archive_directory_or_503(db)
   archive_bytes = read_export(db, archive_directory, user.id, export_id)
   is_missing = archive_bytes is None

   if is_missing:
      raise HTTPException(status_code=404, detail="no export with that id")

   return Response(content=archive_bytes, media_type="application/json")
