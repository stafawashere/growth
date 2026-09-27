"""Database reads the password auth tests share, so each test asserts on the stored row rather than
on the route's own echo of it."""
import threading

from sqlalchemy import select
from sqlalchemy.orm import Session as OrmSession

from app.db import models


def user_row(engine):
   with OrmSession(engine) as db:
      user = db.query(models.User).one_or_none()

      if user is not None:
         db.expunge(user)

      return user


def user_count(engine):
   with OrmSession(engine) as db:
      return db.query(models.User).count()


def lockout_state(engine):
   user = user_row(engine)

   return user.failed_login_count, user.locked_until


def audit_rows(engine, action):
   with OrmSession(engine) as db:
      rows = db.scalars(select(models.AuditLog).where(models.AuditLog.action == action)).all()

      for row in rows:
         db.expunge(row)

      return rows


def auth_session_count(engine):
   with OrmSession(engine) as db:
      return db.query(models.AuthSession).count()


def set_user_columns(engine, **columns):
   with OrmSession(engine) as db:
      user = db.query(models.User).one()

      for name, value in columns.items():
         setattr(user, name, value)

      db.commit()


def run_together(calls):
   """Starts every call at once behind a barrier and returns their results in order."""
   barrier = threading.Barrier(len(calls))
   results = [None] * len(calls)

   def run(index, call):
      barrier.wait()
      results[index] = call()

   threads = [threading.Thread(target=run, args=(index, call)) for index, call in enumerate(calls)]

   for thread in threads:
      thread.start()

   for thread in threads:
      thread.join()

   return results
