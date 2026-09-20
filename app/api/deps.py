"""Request-scoped dependencies: the database session, the settings, and the authenticated user.

Every session-scoped route depends on current_session, so a request without a live cookie never
reaches a query, and every query is scoped by the user id the cookie resolved to.
"""
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session as OrmSession

from app.auth import service
from app.auth.cookies import SESSION_COOKIE
from app.db import models


def get_settings(request: Request):
   return request.app.state.settings


def get_challenges(request: Request):
   return request.app.state.challenges


def get_db(request: Request):
   db = OrmSession(request.app.state.engine)

   try:
      yield db
      db.commit()
   except Exception:
      db.rollback()
      raise
   finally:
      db.close()


def current_session(request: Request, db=Depends(get_db)):
   token = request.cookies.get(SESSION_COOKIE)
   auth_session = service.resolve_session(db, token)
   is_anonymous = auth_session is None

   if is_anonymous:
      raise HTTPException(status_code=401, detail="a passkey session is required")

   return auth_session


def current_user(db=Depends(get_db), auth_session=Depends(current_session)):
   user = db.get(models.User, auth_session.user_id)
   is_missing = user is None

   if is_missing:
      raise HTTPException(status_code=401, detail="the session names no user")

   return user
