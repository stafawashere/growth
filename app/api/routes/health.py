"""GET /healthz: liveness, no auth, loopback only (06's API surface, last row)."""
from fastapi import APIRouter, HTTPException, Request

from app.auth.cookies import is_loopback

router = APIRouter(tags=["health"])


@router.get("/healthz")
def healthz(request: Request):
   client = request.client
   host = client.host if client is not None else ""
   is_local = is_loopback(host)

   if not is_local:
      raise HTTPException(status_code=403, detail="liveness is served on loopback only")

   return {"status": "ok"}
