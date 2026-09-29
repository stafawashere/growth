"""Request-scoped dependencies: the database session, the settings, and the authenticated user.

Every session-scoped route depends on current_session, so a request without a live cookie never
reaches a query, and every query is scoped by the user id the cookie resolved to. A session whose
user has no password is refused as well: that user was migrated from passkeys and must reset first,
and app/db/migrate.py already signed such sessions out, so this is the second line.

A live session is renewed here as well. When its expiry moves, or when the token arrived under the
bare cookie name rather than this port's, the token is left on request.state and
app/api/session_renewal.py sends the cookie again on the way out.
"""
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session as OrmSession

from app.auth import service
from app.auth.cookies import read_session_token, session_cookie_name
from app.db import models


def get_settings(request: Request):
   return request.app.state.settings


def get_dummy_hash(request: Request):
   return request.app.state.dummy_hashes.for_settings(request.app.state.settings)


def get_db(request: Request):
   """Every route takes this with scope="function", so the commit lands before the response is
   sent. With the default scope it landed after, and a client that read straight after a write,
   as the diagnostic does after an answer, could read the state from before it."""
   db = OrmSession(request.app.state.engine)

   try:
      yield db
      db.commit()
   except Exception:
      db.rollback()
      raise
   finally:
      db.close()


def current_session(request: Request, db=Depends(get_db, scope="function")):
   token = read_session_token(request)
   auth_session = service.resolve_session(db, token)
   is_anonymous = auth_session is None

   if is_anonymous:
      raise HTTPException(status_code=401, detail="a session is required")

   user = db.get(models.User, auth_session.user_id)
   needs_password = user is not None and user.password_hash is None

   if needs_password:
      raise HTTPException(status_code=401, detail="a session is required")

   settings = get_settings(request)
   was_renewed = service.renew_session(db, auth_session, settings)
   arrived_under_bare_name = request.cookies.get(session_cookie_name(request)) != token
   should_resend_cookie = was_renewed or arrived_under_bare_name

   if should_resend_cookie:
      request.state.renewed_session_token = token

   return auth_session


def current_user(db=Depends(get_db, scope="function"), auth_session=Depends(current_session)):
   user = db.get(models.User, auth_session.user_id)
   is_missing = user is None

   if is_missing:
      raise HTTPException(status_code=401, detail="the session names no user")

   return user
