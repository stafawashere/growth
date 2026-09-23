"""The settings routes, per 06's API surface.

PUT /settings/budgets is a consequential action under docs/plan/09-security-and-privacy.md, which
forces re-authentication for changing a budget cap, so it consumes a fresh re-authentication token
the way POST /purge does. The request body is checked first, so a malformed change does not spend
the token. Setting a provider key and the provider test call are not served: key storage needs the
libsodium binding 06 names for provider_configs, which is not installed.
"""
from fastapi import APIRouter, Body, Depends, HTTPException

from app.api.deps import current_session, current_user, get_db, get_settings
from app.auth import service as auth_service
from app.providers.guard import caps_in_force
from app.settings import budgets, preferences, providers

router = APIRouter(tags=["settings"])


def fields_of(payload):
   is_object = isinstance(payload, dict)

   if not is_object:
      raise HTTPException(status_code=400, detail="the request body must be a JSON object")

   return payload


@router.get("/settings")
def read_settings(user=Depends(current_user)):
   return preferences.settings_view(user, auth_service.utc_now().date())


@router.put("/settings")
def update_settings(payload: dict = Body(default=None), db=Depends(get_db), user=Depends(current_user)):
   fields = fields_of(payload)
   now = auth_service.utc_now()

   try:
      preferences.update_dates(db, user, fields, auth_service.as_iso(now))
   except preferences.SettingsRefused as refused:
      raise HTTPException(status_code=400, detail=str(refused)) from refused

   return preferences.settings_view(user, now.date())


@router.get("/settings/providers")
def read_providers(settings=Depends(get_settings), user=Depends(current_user)):
   return providers.providers_view(settings)


@router.get("/settings/budgets")
def read_budgets(db=Depends(get_db), settings=Depends(get_settings), user=Depends(current_user)):
   return budgets.budgets_view(db, user.id, settings.tutor_caps, auth_service.utc_now())


@router.put("/settings/budgets")
def change_budget(
   payload: dict = Body(default=None),
   db=Depends(get_db),
   settings=Depends(get_settings),
   auth_session=Depends(current_session),
   user=Depends(current_user),
):
   fields = fields_of(payload)
   role = fields.get("role")
   now = auth_service.utc_now()

   try:
      named = budgets.requested_units(role, fields)
      current = caps_in_force(db, user.id, role, now.date().isoformat(), settings.tutor_caps)
      budgets.merged_caps(current, named)
   except budgets.CapRefused as refused:
      raise HTTPException(status_code=400, detail=str(refused)) from refused

   is_reauthenticated = auth_service.consume_reauth(db, auth_session, fields.get("reauth_token"), now)

   if not is_reauthenticated:
      raise HTTPException(status_code=401, detail="changing a budget cap needs a fresh passkey re-authentication")

   budgets.change_cap(db, user.id, role, fields, configured=settings.tutor_caps, now=now)

   return budgets.budgets_view(db, user.id, settings.tutor_caps, now)
