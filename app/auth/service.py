"""Password sign-up, login, re-authentication, password change and logout over the two auth tables.

Ruled 2026-09-27 on the operator's instruction: a username and password replace passkeys. What
docs/plan/09-security-and-privacy.md fixes about the flow still holds here: sign-up is available only
while users is empty, the session cookie is long lived, and the consequential actions demand a
fresh re-authentication, now a password entered again.

Passwords are scrypt hashes from app/auth/passwords.py. A wrong password counts against the user
row, not the process, so the count survives a restart and is shared by every worker. The attempt is
reserved in one UPDATE before the password is hashed, and that same transaction sets the lock the
moment the free failures run out, so parallel guesses cannot get past the free budget. After
LOCKOUT_FREE_FAILURES failures each further one locks the account for twice as long as the last,
from 30 seconds up to 15 minutes, and never for good. An attempt made while locked neither counts
nor extends the lock. Every refusal is returned as an AuthRefusal rather than raised, because
app/api/deps.py get_db rolls back on an exception and the counter would go with it.

Tokens are random and stored as sha256 hashes, so a stolen database file yields no usable session.
"""
import hashlib
import json
import secrets
import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import text

from app.audit.detail import bind_audit_detail
from app.audit.vocabulary import is_known_action
from app.auth import passwords
from app.db import models

SESSION_TTL_SECONDS = 60 * 60 * 24 * 30
REAUTH_TTL_SECONDS = 300
PURGE_GRACE_DAYS = 30
LOCKOUT_FREE_FAILURES = 4
LOCKOUT_BASE_SECONDS = 30
LOCKOUT_MAX_SECONDS = 15 * 60
DEFAULT_DISPLAY_NAME = "student"
SIGNUP_CLOSED_DETAIL = "registration is closed; this installation already has a user"
LOGIN_REFUSED_DETAIL = "username or password is incorrect"
REAUTH_REFUSED_DETAIL = "the password is incorrect"
CHANGE_NEEDS_REAUTH_DETAIL = "changing the password needs a fresh re-authentication"
LOCKOUT_ACTION = "login_failed_lockout"


@dataclass
class AuthRefusal:
   """A refusal the route returns as a JSONResponse, so the writes before it are committed."""

   status_code: int
   detail: str


def new_token():
   return secrets.token_urlsafe(32)


def token_hash(token):
   return hashlib.sha256(token.encode()).hexdigest()


def new_id(prefix):
   return f"{prefix}-{uuid.uuid4().hex}"


def utc_now():
   return datetime.now(timezone.utc)


def as_iso(moment):
   return moment.astimezone(timezone.utc).isoformat()


def default_exam_date():
   """06 stores whatever the exam registry says, so the fallback is the users column default."""
   return models.User.__table__.c.exam_date.default.arg


def user_count(db):
   return db.query(models.User).count()


def sole_user(db):
   return db.query(models.User).order_by(models.User.created_at, models.User.id).first()


def purge_after_for(exam_date):
   parsed = date.fromisoformat(exam_date)

   return (parsed + timedelta(days=PURGE_GRACE_DAYS)).isoformat()


def user_exists(db):
   return user_count(db) > 0


def user_needs_password(db):
   """True when the installation's user was migrated from passkeys and has not set a password."""
   user = sole_user(db)
   has_user = user is not None

   return has_user and user.password_hash is None


def find_user_by_username(db, username):
   normalised = passwords.normalise_username(username)

   if normalised is None:
      return None

   return db.query(models.User).filter(models.User.username == normalised).first()


def lock_moment(moment):
   """locked_until is compared as text in SQL, so every value is written at one fixed precision."""
   return moment.astimezone(timezone.utc).isoformat(timespec="microseconds")


def lock_threshold(settings):
   return settings.lockout_free_failures + 1


def lock_seconds(failed_count, settings):
   doublings = max(0, failed_count - lock_threshold(settings))

   return min(settings.lockout_base_seconds * 2 ** doublings, settings.lockout_max_seconds)


def lockout_count_cap(settings):
   """The count stops rising once the lock it earns has reached the maximum."""
   count = lock_threshold(settings)

   while lock_seconds(count, settings) < settings.lockout_max_seconds:
      count += 1

   return count


def reserve_attempt(db, user_id, settings, now):
   """Counts one attempt against the user before the password is checked, in one UPDATE that
   matches only while the user is not locked, and commits it. Returns None when the user is
   locked, which counts nothing and extends nothing. Otherwise returns the new count and, when
   this attempt used up the free failures, the locked_until it set in the same transaction."""
   moment_text = lock_moment(now)
   reserved = db.execute(
      text(
         "UPDATE users SET failed_login_count = min(failed_login_count + 1, :cap), updated_at = :now "
         "WHERE id = :id AND (locked_until IS NULL OR locked_until <= :now) "
         "RETURNING failed_login_count"
      ),
      {"cap": lockout_count_cap(settings), "now": moment_text, "id": user_id},
   ).scalar()
   is_locked = reserved is None

   if is_locked:
      db.commit()

      return None

   locked_until = None
   uses_up_free_failures = reserved >= lock_threshold(settings)

   if uses_up_free_failures:
      locked_until = lock_moment(now + timedelta(seconds=lock_seconds(reserved, settings)))
      db.execute(
         text("UPDATE users SET locked_until = :locked_until WHERE id = :id"),
         {"locked_until": locked_until, "id": user_id},
      )

   db.commit()

   return {"failed_login_count": reserved, "locked_until": locked_until}


def clear_failures(db, user_id, now):
   db.execute(
      text(
         "UPDATE users SET failed_login_count = 0, locked_until = NULL, updated_at = :now "
         "WHERE id = :id"
      ),
      {"now": as_iso(now), "id": user_id},
   )


def check_password_for_user(db, settings, user, password, dummy_hash, now):
   """The reserve, verify and clear sequence login and reauth share. A user with no usable hash
   and a locked user are verified against dummy_hash, so their refusal costs the same scrypt work,
   and a lockout this attempt engaged is audited once, when the attempt fails."""
   user_id = user.id
   stored = user.password_hash
   has_usable_hash = passwords.parse_hash(stored) is not None
   is_verifiable = passwords.can_be_verified(password)

   if not has_usable_hash:
      passwords.verify_password(password, dummy_hash)

      return False

   if not is_verifiable:
      return False

   reservation = reserve_attempt(db, user_id, settings, now)
   is_locked = reservation is None

   if is_locked:
      passwords.verify_password(password, dummy_hash)

      return False

   matched = passwords.verify_password(password, stored)

   if not matched:
      engaged_lock = reservation["locked_until"] is not None

      if engaged_lock:
         write_audit(db, user_id, LOCKOUT_ACTION, f"users:{user_id}", reservation, now)

      return False

   clear_failures(db, user_id, now)
   db.expire_all()
   refreshed = db.get(models.User, user_id)
   is_outdated = passwords.needs_rehash(
      refreshed.password_hash,
      settings.password_scrypt_n,
      settings.password_scrypt_r,
      settings.password_scrypt_p,
   )

   if is_outdated:
      refreshed.password_hash = hash_with_settings(password, settings)
      refreshed.updated_at = as_iso(now)
      db.flush()

   return True


def hash_with_settings(password, settings):
   return passwords.hash_password(
      password,
      settings.password_scrypt_n,
      settings.password_scrypt_r,
      settings.password_scrypt_p,
   )


def claim_installation(db, user_id, username, password_hash, exam_date, timestamp):
   """Inserts the one user only while users is empty, in one statement, so two sign-ups racing
   past the count check cannot both land. Returns whether this call claimed it."""
   inserted = db.execute(
      text(
         "INSERT INTO users (id, display_name, exam_date, purge_after, recovery_code_hash, username, "
         "password_hash, failed_login_count, locked_until, created_at, updated_at) "
         "SELECT :id, :display_name, :exam_date, :purge_after, NULL, :username, :password_hash, 0, "
         "NULL, :timestamp, :timestamp "
         "WHERE NOT EXISTS (SELECT 1 FROM users)"
      ),
      {
         "id": user_id,
         "display_name": DEFAULT_DISPLAY_NAME,
         "exam_date": exam_date,
         "purge_after": purge_after_for(exam_date),
         "username": username,
         "password_hash": password_hash,
         "timestamp": timestamp,
      },
   )

   return inserted.rowcount == 1


def signup(db, settings, username, password, now=None):
   """Creates the installation's one user. Returns {user, token, seeded_skill_states,
   recovery_code}, or an AuthRefusal: 400 for a username or password the rules refuse, 403 once
   the installation has its user."""
   moment = now or utc_now()
   normalised = passwords.normalise_username(username)

   if normalised is None:
      return AuthRefusal(400, passwords.USERNAME_RULE)

   problem = passwords.password_problem(password)

   if problem is not None:
      return AuthRefusal(400, problem)

   is_claimed = user_exists(db)

   if is_claimed:
      return AuthRefusal(403, SIGNUP_CLOSED_DETAIL)

   password_hash = hash_with_settings(password, settings)
   user_id = new_id("USER")
   timestamp = as_iso(moment)
   exam_date = settings.exam_date or default_exam_date()
   claimed = claim_installation(db, user_id, normalised, password_hash, exam_date, timestamp)

   if not claimed:
      return AuthRefusal(403, SIGNUP_CLOSED_DETAIL)

   user = db.get(models.User, user_id)
   context = settings.session_context
   snapshot_row_id = context.snapshot_id if context is not None else None
   seeded = settings.resolve_seed_hook()(
      db, user.id, settings.resolve_snapshot(), moment, snapshot_id=snapshot_row_id
   )
   write_audit(db, user.id, "account_created", f"users:{user.id}", {"seeded_skill_states": seeded}, moment)
   token = open_auth_session(db, user.id, settings, moment)

   from app.auth.recovery import issue_recovery_code

   recovery_code = issue_recovery_code(db, user, moment)

   return {
      "user": user,
      "token": token,
      "seeded_skill_states": seeded,
      "recovery_code": recovery_code,
   }


def login(db, settings, username, password, dummy_hash, now=None):
   """Returns {user_id, token}, or an AuthRefusal(401, LOGIN_REFUSED_DETAIL) that is the same for
   an unknown username, a wrong password, a user with no password yet and a locked user."""
   moment = now or utc_now()
   user = find_user_by_username(db, username)
   is_unknown = user is None

   if is_unknown:
      passwords.verify_password(password, dummy_hash)

      return AuthRefusal(401, LOGIN_REFUSED_DETAIL)

   user_id = user.id
   matched = check_password_for_user(db, settings, user, password, dummy_hash, moment)

   if not matched:
      return AuthRefusal(401, LOGIN_REFUSED_DETAIL)

   write_audit(db, user_id, "session_established", f"users:{user_id}", None, moment)
   token = open_auth_session(db, user_id, settings, moment)

   return {"user_id": user_id, "token": token}


def mint_reauth(db, settings, auth_session, now):
   token = new_token()
   auth_session.reauth_token_hash = token_hash(token)
   auth_session.reauth_expires_at = as_iso(now + timedelta(seconds=settings.reauth_ttl_seconds))
   auth_session.updated_at = as_iso(now)
   db.flush()

   return token


def reauth_with_password(db, settings, auth_session, password, dummy_hash, now=None):
   """Returns {reauth_token}, or an AuthRefusal(401). A wrong password counts toward the same
   lockout login does, and a locked user is refused here too."""
   moment = now or utc_now()
   session_id = auth_session.id
   user = db.get(models.User, auth_session.user_id)
   is_missing = user is None

   if is_missing:
      return AuthRefusal(401, "the session names no user")

   matched = check_password_for_user(db, settings, user, password, dummy_hash, moment)

   if not matched:
      return AuthRefusal(401, REAUTH_REFUSED_DETAIL)

   live_session = db.get(models.AuthSession, session_id)
   token = mint_reauth(db, settings, live_session, moment)
   write_audit(db, live_session.user_id, "reauth_established", f"auth_sessions:{session_id}", None, moment)

   return {"reauth_token": token}


def change_password(db, settings, auth_session, current_password, new_password, reauth_token, dummy_hash, now=None):
   """Spends the reauth token, checks the current password (which counts toward the lockout),
   then sets the new one and signs every other session out. The current session and the
   recovery code are kept. Returns {"password_changed": True} or an AuthRefusal."""
   moment = now or utc_now()
   session_id = auth_session.id
   user_id = auth_session.user_id
   is_reauthenticated = consume_reauth(db, auth_session, reauth_token, moment)

   if not is_reauthenticated:
      return AuthRefusal(401, CHANGE_NEEDS_REAUTH_DETAIL)

   user = db.get(models.User, user_id)
   is_missing = user is None

   if is_missing:
      return AuthRefusal(401, "the session names no user")

   matched = check_password_for_user(db, settings, user, current_password, dummy_hash, moment)

   if not matched:
      return AuthRefusal(401, "the current password is incorrect")

   problem = passwords.password_problem(new_password)

   if problem is not None:
      return AuthRefusal(400, problem)

   refreshed = db.get(models.User, user_id)
   refreshed.password_hash = hash_with_settings(new_password, settings)
   refreshed.updated_at = as_iso(moment)
   db.query(models.AuthSession).filter(
      models.AuthSession.user_id == user_id,
      models.AuthSession.id != session_id,
   ).delete(synchronize_session=False)
   db.flush()
   write_audit(db, user_id, "password_changed", f"users:{user_id}", None, moment)

   return {"password_changed": True}


def open_auth_session(db, user_id, settings, now):
   timestamp = as_iso(now)
   token = new_token()
   expires_at = now + timedelta(seconds=settings.session_ttl_seconds)
   row = models.AuthSession(
      id=new_id("AUS"),
      user_id=user_id,
      token_hash=token_hash(token),
      expires_at=as_iso(expires_at),
      reauth_token_hash=None,
      reauth_expires_at=None,
      created_at=timestamp,
      updated_at=timestamp,
   )
   db.add(row)
   db.flush()

   return token


def resolve_session(db, token, now=None):
   moment = now or utc_now()
   is_absent = not token

   if is_absent:
      return None

   row = (
      db.query(models.AuthSession)
      .filter(models.AuthSession.token_hash == token_hash(token))
      .first()
   )
   is_missing = row is None

   if is_missing:
      return None

   has_expired = datetime.fromisoformat(row.expires_at) <= moment

   if has_expired:
      return None

   return row


def consume_reauth(db, auth_session, token, now=None):
   """Single use: the stored hash is cleared whether or not the offered token matched. Only the call
   whose UPDATE cleared the hash it had read may compare, the same guard consume_recovery_code uses,
   so two requests holding one token cannot both spend it."""
   moment = now or utc_now()
   session_id = auth_session.id
   db.flush()
   seen = db.execute(
      text("SELECT reauth_token_hash, reauth_expires_at FROM auth_sessions WHERE id = :id"),
      {"id": session_id},
   ).first()
   stored, deadline = seen if seen is not None else (None, None)
   is_unset = stored is None or deadline is None

   if is_unset:
      return False

   cleared = db.execute(
      text(
         "UPDATE auth_sessions SET reauth_token_hash = NULL, reauth_expires_at = NULL, updated_at = :now "
         "WHERE id = :id AND reauth_token_hash = :seen"
      ),
      {"now": as_iso(moment), "id": session_id, "seen": stored},
   )
   db.expire(auth_session)
   won_the_spend = cleared.rowcount == 1

   if not won_the_spend:
      return False

   has_expired = datetime.fromisoformat(deadline) <= moment

   if has_expired:
      return False

   is_offered = isinstance(token, str) and token != ""

   if not is_offered:
      return False

   return secrets.compare_digest(stored, token_hash(token))


def logout(db, auth_session, now=None):
   moment = now or utc_now()
   write_audit(db, auth_session.user_id, "session_closed", f"auth_sessions:{auth_session.id}", None, moment)
   db.delete(auth_session)
   db.flush()


def write_audit(db, actor, action, subject, detail, now=None):
   """docs/plan/09-security-and-privacy.md, "Audit log": no key material ever reaches detail, and
   the action comes from the controlled vocabulary in app/audit/vocabulary.py. detail is bound by
   app/audit/detail.py before it reaches json.dumps, per docs/plan/13-ai-engineering.md item 9."""
   if not is_known_action(action):
      raise ValueError(f"{action!r} is not in the audit_log vocabulary")

   bound_detail = bind_audit_detail(detail)
   timestamp = as_iso(now or utc_now())
   row = models.AuditLog(
      id=new_id("AUD"),
      at=timestamp,
      actor=actor,
      action=action,
      subject=subject,
      detail=json.dumps(bound_detail) if bound_detail is not None else None,
      created_at=timestamp,
      updated_at=timestamp,
   )
   db.add(row)
   db.flush()

   return row
