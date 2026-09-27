"""Sign-up, login, logout, re-authentication, password change and recovery over a username and
password.

Ruled 2026-09-27 on the operator's instruction, reversing docs/plan/09-security-and-privacy.md's
passkey-only rule for this installation. 06's API surface lists these paths, and BUILD-LEDGER.md
records the ruling: POST /auth/signup, /auth/login, /auth/logout, /auth/reauth,
/auth/password/change and /auth/recovery/reset, and GET /auth/status.

Every route that takes a credential first runs app/auth/guard.py refuse_untrusted_auth_request,
which stands in for the origin binding a passkey ceremony carried: the Host must be one this
installation serves, a cross-site or foreign-Origin request is refused, and plain http on a
non-loopback origin is refused before any password is read. The three routes a stranger can reach,
signup, login and recovery/reset, then pass the per-IP limit of app/auth/limiter.py, checked after
the body has parsed and before any scrypt work or database write.

Every refusal is returned as a JSONResponse, never raised, because app/api/deps.py get_db rolls
back on an exception and would take the failed-login count with it. Login answers every failure,
an unknown username included, with the same 401 and the same detail.

/auth/status answers whether the installation has its user, which signup already reveals by
refusing. It adds needs_password, true while a user migrated from passkeys has not set a password,
only for a caller whose peer and Host are both loopback, so the migration window is not advertised
to the network, to a DNS-rebound page or through a reverse proxy.
"""
from fastapi import APIRouter, Body, Depends, Request, Response
from fastapi.responses import JSONResponse

from app.api.deps import current_session, get_db, get_dummy_hash, get_settings
from app.auth import service
from app.auth.cookies import clear_session_cookie, is_loopback, request_host_is_loopback, set_session_cookie
from app.auth.guard import refuse_rate_limited, refuse_untrusted_auth_request
from app.auth.recovery import reset_password_via_recovery

router = APIRouter(prefix="/auth", tags=["auth"])


def body_of(payload):
   return payload or {}


def issue_session_cookie(response, request, settings, token):
   set_session_cookie(response, settings.bind_host, request, token, settings.session_ttl_seconds)


def refusal_response(refusal):
   return JSONResponse(status_code=refusal.status_code, content={"detail": refusal.detail})


def is_refusal(outcome):
   return isinstance(outcome, service.AuthRefusal)


def caller_is_loopback(request):
   """Both the peer and the Host must be loopback. A DNS-rebound page arrives from 127.0.0.1 under a
   foreign Host, and a reverse proxy makes every caller's peer loopback while the Host stays public."""
   client = request.client
   peer = client.host if client is not None else ""
   peer_is_loopback = is_loopback(peer)
   host_is_loopback = request_host_is_loopback(request)

   return peer_is_loopback and host_is_loopback


@router.post("/signup")
def signup(
   request: Request,
   response: Response,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
):
   untrusted = refuse_untrusted_auth_request(request, settings)

   if untrusted is not None:
      return untrusted

   limited = refuse_rate_limited(request, settings)

   if limited is not None:
      return limited

   fields = body_of(payload)
   finished = service.signup(db, settings, fields.get("username"), fields.get("password"))

   if is_refusal(finished):
      return refusal_response(finished)

   issue_session_cookie(response, request, settings, finished["token"])
   user = finished["user"]

   return {
      "user": {
         "id": user.id,
         "display_name": user.display_name,
         "exam_date": user.exam_date,
         "purge_after": user.purge_after,
      },
      "seeded_skill_states": finished["seeded_skill_states"],
      "recovery_code": finished["recovery_code"],
   }


@router.post("/login")
def login(
   request: Request,
   response: Response,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
   dummy_hash=Depends(get_dummy_hash),
):
   untrusted = refuse_untrusted_auth_request(request, settings)

   if untrusted is not None:
      return untrusted

   limited = refuse_rate_limited(request, settings)

   if limited is not None:
      return limited

   fields = body_of(payload)
   finished = service.login(db, settings, fields.get("username"), fields.get("password"), dummy_hash)

   if is_refusal(finished):
      return refusal_response(finished)

   issue_session_cookie(response, request, settings, finished["token"])

   return {"user_id": finished["user_id"]}


@router.get("/status")
def status(request: Request, db=Depends(get_db, scope="function")):
   user_exists = service.user_exists(db)

   if not caller_is_loopback(request):
      return {"user_exists": user_exists}

   return {"user_exists": user_exists, "needs_password": service.user_needs_password(db)}


@router.post("/logout")
def logout(
   request: Request,
   response: Response,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
   auth_session=Depends(current_session),
):
   untrusted = refuse_untrusted_auth_request(request, settings)

   if untrusted is not None:
      return untrusted

   service.logout(db, auth_session)
   clear_session_cookie(response, settings.bind_host, request)

   return {"logged_out": True}


@router.post("/reauth")
def reauth(
   request: Request,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
   dummy_hash=Depends(get_dummy_hash),
   auth_session=Depends(current_session),
):
   untrusted = refuse_untrusted_auth_request(request, settings)

   if untrusted is not None:
      return untrusted

   fields = body_of(payload)
   finished = service.reauth_with_password(db, settings, auth_session, fields.get("password"), dummy_hash)

   if is_refusal(finished):
      return refusal_response(finished)

   return {"reauth_token": finished["reauth_token"]}


@router.post("/password/change")
def change_password(
   request: Request,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
   dummy_hash=Depends(get_dummy_hash),
   auth_session=Depends(current_session),
):
   untrusted = refuse_untrusted_auth_request(request, settings)

   if untrusted is not None:
      return untrusted

   fields = body_of(payload)
   finished = service.change_password(
      db,
      settings,
      auth_session,
      fields.get("current_password"),
      fields.get("new_password"),
      fields.get("reauth_token"),
      dummy_hash,
   )

   if is_refusal(finished):
      return refusal_response(finished)

   return {"password_changed": finished["password_changed"]}


@router.post("/recovery/reset")
def recovery_reset(
   request: Request,
   response: Response,
   payload: dict = Body(default=None),
   db=Depends(get_db, scope="function"),
   settings=Depends(get_settings),
):
   untrusted = refuse_untrusted_auth_request(request, settings)

   if untrusted is not None:
      return untrusted

   limited = refuse_rate_limited(request, settings)

   if limited is not None:
      return limited

   fields = body_of(payload)
   finished = reset_password_via_recovery(
      db,
      settings,
      fields.get("recovery_code"),
      fields.get("new_password"),
      username=fields.get("username"),
   )

   if is_refusal(finished):
      return refusal_response(finished)

   issue_session_cookie(response, request, settings, finished["token"])

   return {
      "user_id": finished["user"].id,
      "recovery_code": finished["recovery_code"],
   }
