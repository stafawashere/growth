"""The passkey ceremonies of docs/plan/09-security-and-privacy.md over the paths 06 names.

06's API surface has no row for re-authentication, although 09 requires it for the consequential
actions. It is an assertion ceremony against an already-registered credential, so it is served at
/auth/reauth/begin and /auth/reauth/finish, which is a plan addition recorded in BUILD-LEDGER.md.

06 has no row for the recovery code either, and the ordinary registration ceremony stays closed
once the installation has a user, so recovery runs at /auth/recovery/register/begin and
/auth/recovery/register/finish. Both additions are recorded in BUILD-LEDGER.md.

09's audit-log vocabulary lists "a session established from a new authenticator" among what
audit_log records. login_finish already writes that as action "session_established", and reauth is
its own ceremony, an authenticator asserted again against a session already open, so reauth_finish
writes "reauth_established" rather than reusing the login action name, through the same write_audit
helper login_finish and logout already call.

Two more paths have no 06 row. 09's Recovery makes a second authenticator the primary recovery
answer, but register/finish closes once users is non-empty, so a signed-in student adds one at
/auth/passkey/add/begin and /auth/passkey/add/finish. 09 does not list adding a credential among the
actions that force re-authentication, so the session cookie alone admits it. /auth/status answers
whether the installation has its user, which register/begin already reveals by refusing.
"""
from fastapi import APIRouter, Body, Depends, Request, Response

from app.api.deps import current_session, get_challenges, get_db, get_settings
from app.auth import service
from app.auth.cookies import clear_session_cookie, set_session_cookie
from app.auth.service import write_audit

router = APIRouter(prefix="/auth", tags=["auth"])


def body_of(payload):
   return payload or {}


def issue_session_cookie(response, request, settings, token):
   set_session_cookie(response, settings.bind_host, request, token, settings.session_ttl_seconds)


@router.post("/passkey/register/begin")
def register_begin(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   challenges=Depends(get_challenges),
):
   fields = body_of(payload)

   return service.register_begin(db, settings, challenges, fields.get("display_name"))


@router.post("/passkey/register/finish")
def register_finish(
   request: Request,
   response: Response,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   challenges=Depends(get_challenges),
):
   fields = body_of(payload)
   finished = service.register_finish(
      db,
      settings,
      challenges,
      fields.get("challenge_id"),
      fields.get("credential") or {},
      display_name=fields.get("display_name"),
   )
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


@router.get("/status")
def status(db=Depends(get_db)):
   return {"user_exists": service.user_exists(db)}


@router.post("/passkey/add/begin")
def add_passkey_begin(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   challenges=Depends(get_challenges),
   auth_session=Depends(current_session),
):
   return service.add_passkey_begin(db, settings, challenges, auth_session)


@router.post("/passkey/add/finish")
def add_passkey_finish(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   challenges=Depends(get_challenges),
   auth_session=Depends(current_session),
):
   fields = body_of(payload)

   return service.add_passkey_finish(
      db,
      settings,
      challenges,
      auth_session,
      fields.get("challenge_id"),
      fields.get("credential") or {},
   )


@router.post("/recovery/register/begin")
def recovery_register_begin(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   challenges=Depends(get_challenges),
):
   return service.recovery_register_begin(db, settings, challenges)


@router.post("/recovery/register/finish")
def recovery_register_finish(
   request: Request,
   response: Response,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   challenges=Depends(get_challenges),
):
   fields = body_of(payload)
   finished = service.recovery_register_finish(
      db,
      settings,
      challenges,
      fields.get("challenge_id"),
      fields.get("credential") or {},
      fields.get("recovery_code"),
   )
   issue_session_cookie(response, request, settings, finished["token"])

   return {
      "user_id": finished["user"].id,
      "credential_id": finished["credential_id"],
      "recovery_code": finished["recovery_code"],
   }


@router.post("/passkey/login/begin")
def login_begin(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   challenges=Depends(get_challenges),
):
   return service.login_begin(db, settings, challenges)


@router.post("/passkey/login/finish")
def login_finish(
   request: Request,
   response: Response,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   challenges=Depends(get_challenges),
):
   fields = body_of(payload)
   finished = service.login_finish(
      db,
      settings,
      challenges,
      fields.get("challenge_id"),
      fields.get("credential") or {},
   )
   issue_session_cookie(response, request, settings, finished["token"])

   return {"user_id": finished["user_id"]}


@router.post("/logout")
def logout(
   request: Request,
   response: Response,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   auth_session=Depends(current_session),
):
   service.logout(db, auth_session)
   clear_session_cookie(response, settings.bind_host, request)

   return {"logged_out": True}


@router.post("/reauth/begin")
def reauth_begin(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   challenges=Depends(get_challenges),
   auth_session=Depends(current_session),
):
   return service.reauth_begin(db, settings, challenges, auth_session)


@router.post("/reauth/finish")
def reauth_finish(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   challenges=Depends(get_challenges),
   auth_session=Depends(current_session),
):
   fields = body_of(payload)
   finished = service.reauth_finish(
      db,
      settings,
      challenges,
      auth_session,
      fields.get("challenge_id"),
      fields.get("credential") or {},
   )
   write_audit(
      db,
      auth_session.user_id,
      "reauth_established",
      f"auth_sessions:{auth_session.id}",
      None,
   )

   return finished
