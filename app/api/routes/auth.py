"""The passkey ceremonies of docs/plan/09-security-and-privacy.md over the paths 06 names.

06's API surface has no row for re-authentication, although 09 requires it for the consequential
actions. It is an assertion ceremony against an already-registered credential, so it is served at
/auth/reauth/begin and /auth/reauth/finish, which is a plan addition recorded in BUILD-LEDGER.md.

06 has no row for the recovery code either, and the ordinary registration ceremony stays closed
once the installation has a user, so recovery runs at /auth/recovery/register/begin and
/auth/recovery/register/finish. Both additions are recorded in BUILD-LEDGER.md.
"""
from fastapi import APIRouter, Body, Depends, Request, Response

from app.api.deps import current_session, get_challenges, get_db, get_settings
from app.auth import service
from app.auth.cookies import clear_session_cookie, set_session_cookie

router = APIRouter(prefix="/auth", tags=["auth"])


def body_of(payload):
   return payload or {}


def issue_session_cookie(response, settings, token):
   set_session_cookie(response, settings.bind_host, token, settings.session_ttl_seconds)


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
   issue_session_cookie(response, settings, finished["token"])
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
   issue_session_cookie(response, settings, finished["token"])

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
   issue_session_cookie(response, settings, finished["token"])

   return {"user_id": finished["user_id"]}


@router.post("/logout")
def logout(
   response: Response,
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   auth_session=Depends(current_session),
):
   service.logout(db, auth_session)
   clear_session_cookie(response, settings.bind_host)

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

   return service.reauth_finish(
      db,
      settings,
      challenges,
      auth_session,
      fields.get("challenge_id"),
      fields.get("credential") or {},
   )
