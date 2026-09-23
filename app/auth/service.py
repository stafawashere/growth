"""Passkey registration, login, re-authentication and logout over the two auth tables.

Everything docs/plan/09-security-and-privacy.md fixes about the flow lives here: registration is
available only while users is empty, login checks the authenticator sign count for regression, the
session cookie is long lived, and the consequential actions demand a fresh re-authentication. The
ceremony itself is verified by the injected PasskeyVerifier, never by this module.

Tokens are random and stored as sha256 hashes, so a stolen database file yields no usable session.
"""
import hashlib
import json
import secrets
import uuid
from datetime import date, datetime, timedelta, timezone

from app.audit.detail import bind_audit_detail
from app.audit.vocabulary import is_known_action
from app.db import models

CHALLENGE_TTL_SECONDS = 300
SESSION_TTL_SECONDS = 60 * 60 * 24 * 30
REAUTH_TTL_SECONDS = 300
PURGE_GRACE_DAYS = 30


class AuthError(Exception):
   def __init__(self, status_code, detail):
      super().__init__(detail)
      self.status_code = status_code
      self.detail = detail


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


class ChallengeStore:
   """Server-side challenge state between a begin and its finish, held for the process lifetime."""

   def __init__(self):
      self.entries = {}

   def prune(self, now):
      live = {
         key: entry
         for key, entry in self.entries.items()
         if entry["expires_at"] > now
      }
      self.entries = live

   def issue(self, kind, challenge, now, user_id=None):
      self.prune(now)
      challenge_id = new_id("CHL")
      self.entries[challenge_id] = {
         "kind": kind,
         "challenge": challenge,
         "user_id": user_id,
         "expires_at": now + timedelta(seconds=CHALLENGE_TTL_SECONDS),
      }

      return challenge_id

   def take(self, challenge_id, kind, now):
      self.prune(now)
      entry = self.entries.pop(challenge_id, None)
      is_missing = entry is None

      if is_missing:
         raise AuthError(400, "unknown or expired challenge")

      is_wrong_kind = entry["kind"] != kind

      if is_wrong_kind:
         raise AuthError(400, "challenge was issued for another ceremony")

      return entry


def default_exam_date():
   """06 stores whatever the exam registry says, so the fallback is the users column default."""
   return models.User.__table__.c.exam_date.default.arg


def user_count(db):
   return db.query(models.User).count()


def sole_user(db):
   return db.query(models.User).order_by(models.User.created_at, models.User.id).first()


def refuse_second_registration(db):
   """The single-user invariant: the first registration claims the installation (09, Registration)."""
   is_claimed = user_count(db) > 0

   if is_claimed:
      raise AuthError(403, "registration is closed; this installation already has a user")


def register_begin(db, settings, store, display_name, now=None):
   moment = now or utc_now()
   refuse_second_registration(db)
   user_id = new_id("USER")
   begun = settings.verifier.begin_registration(user_id, display_name or "student")
   challenge_id = store.issue("registration", begun["challenge"], moment, user_id=user_id)

   return {"challenge_id": challenge_id, "options": begun["options"]}


def purge_after_for(exam_date):
   parsed = date.fromisoformat(exam_date)

   return (parsed + timedelta(days=PURGE_GRACE_DAYS)).isoformat()


def register_finish(db, settings, store, challenge_id, credential, display_name=None, now=None):
   moment = now or utc_now()
   refuse_second_registration(db)
   entry = store.take(challenge_id, "registration", moment)
   verified = settings.verifier.finish_registration(entry["challenge"], credential)
   timestamp = as_iso(moment)
   exam_date = settings.exam_date or default_exam_date()
   user = models.User(
      id=entry["user_id"],
      display_name=display_name or "student",
      exam_date=exam_date,
      purge_after=purge_after_for(exam_date),
      created_at=timestamp,
      updated_at=timestamp,
   )
   db.add(user)
   db.flush()
   credential_row = models.PasskeyCredential(
      id=new_id("PKC"),
      user_id=user.id,
      credential_id=verified["credential_id"],
      public_key=verified["public_key"],
      sign_count=int(verified["sign_count"]),
      transports=verified.get("transports"),
      created_at=timestamp,
      updated_at=timestamp,
   )
   db.add(credential_row)
   db.flush()
   context = settings.session_context
   snapshot_row_id = context.snapshot_id if context is not None else None
   seeded = settings.resolve_seed_hook()(
      db, user.id, settings.resolve_snapshot(), moment, snapshot_id=snapshot_row_id
   )
   write_audit(db, user.id, "passkey_registered", f"passkey_credentials:{credential_row.id}", {"seeded_skill_states": seeded}, moment)
   token = open_auth_session(db, user.id, settings, moment)

   from app.auth.recovery import issue_recovery_code

   recovery_code = issue_recovery_code(db, user, moment)

   return {
      "user": user,
      "token": token,
      "seeded_skill_states": seeded,
      "recovery_code": recovery_code,
   }


def require_sole_user(db):
   """Recovery re-registers a passkey for the single user 09's registration rule allows."""
   user = sole_user(db)
   is_unclaimed = user is None

   if is_unclaimed:
      raise AuthError(404, "this installation has no user to recover")

   return user


def recovery_register_begin(db, settings, store, now=None):
   moment = now or utc_now()
   user = require_sole_user(db)
   begun = settings.verifier.begin_registration(user.id, user.display_name or "student")
   challenge_id = store.issue("recovery", begun["challenge"], moment, user_id=user.id)

   return {"challenge_id": challenge_id, "options": begun["options"]}


def recovery_register_finish(db, settings, store, challenge_id, credential, recovery_code, now=None):
   from app.auth.recovery import issue_recovery_code, register_via_recovery

   moment = now or utc_now()
   user = require_sole_user(db)
   entry = store.take(challenge_id, "recovery", moment)
   is_other_user = entry["user_id"] != user.id

   if is_other_user:
      raise AuthError(403, "the challenge was issued for another user")

   verified = settings.verifier.finish_registration(entry["challenge"], credential)
   credential_row = register_via_recovery(db, user, recovery_code or "", verified, moment)
   token = open_auth_session(db, user.id, settings, moment)
   replacement = issue_recovery_code(db, user, moment)

   return {
      "user": user,
      "token": token,
      "credential_id": credential_row.id,
      "recovery_code": replacement,
   }


def user_exists(db):
   return user_count(db) > 0


def add_passkey_begin(db, settings, store, auth_session, now=None):
   """09, "Recovery": a second registered authenticator is the primary recovery answer. The user
   handle stays the signed-in user's id so the authenticator files both passkeys under one account."""
   moment = now or utc_now()
   user = db.get(models.User, auth_session.user_id)
   is_missing = user is None

   if is_missing:
      raise AuthError(401, "the session names no user")

   stored_for_user = [
      row[0]
      for row in db.query(models.PasskeyCredential.credential_id)
      .filter(models.PasskeyCredential.user_id == user.id)
      .all()
   ]
   begun = settings.verifier.begin_registration(user.id, user.display_name or "student", stored_for_user)
   challenge_id = store.issue("add_passkey", begun["challenge"], moment, user_id=user.id)

   return {"challenge_id": challenge_id, "options": begun["options"]}


def refuse_stored_credential(db, credential_id):
   stored = (
      db.query(models.PasskeyCredential.id)
      .filter(models.PasskeyCredential.credential_id == credential_id)
      .first()
   )
   is_already_stored = stored is not None

   if is_already_stored:
      raise AuthError(409, "this passkey is already registered")


def add_passkey_finish(db, settings, store, auth_session, challenge_id, credential, now=None):
   moment = now or utc_now()
   entry = store.take(challenge_id, "add_passkey", moment)
   is_other_user = entry["user_id"] != auth_session.user_id

   if is_other_user:
      raise AuthError(403, "the challenge belongs to another session")

   verified = settings.verifier.finish_registration(entry["challenge"], credential)
   refuse_stored_credential(db, verified["credential_id"])
   timestamp = as_iso(moment)
   credential_row = models.PasskeyCredential(
      id=new_id("PKC"),
      user_id=auth_session.user_id,
      credential_id=verified["credential_id"],
      public_key=verified["public_key"],
      sign_count=int(verified["sign_count"]),
      transports=verified.get("transports"),
      created_at=timestamp,
      updated_at=timestamp,
   )
   db.add(credential_row)
   db.flush()
   write_audit(db, auth_session.user_id, "passkey_registered", f"passkey_credentials:{credential_row.id}", None, moment)

   return {"credential_id": credential_row.id}


def stored_credential_ids(db):
   """09's installation is single-user, so every stored credential belongs to the one account and
   is offered as allowCredentials, which lets a non-discoverable credential sign in too."""
   rows = db.query(models.PasskeyCredential.credential_id).all()

   return [row[0] for row in rows]


def login_begin(db, settings, store, now=None):
   moment = now or utc_now()
   begun = settings.verifier.begin_login(stored_credential_ids(db))
   challenge_id = store.issue("login", begun["challenge"], moment)

   return {"challenge_id": challenge_id, "options": begun["options"]}


def credential_for(db, credential):
   raw = credential.get("credential_id") if isinstance(credential, dict) else None
   is_named = isinstance(raw, str) and raw != ""

   if not is_named:
      raise AuthError(400, "the assertion names no credential")

   try:
      credential_id = bytes.fromhex(raw)
   except ValueError as malformed:
      raise AuthError(400, "credential_id is not hex") from malformed

   row = (
      db.query(models.PasskeyCredential)
      .filter(models.PasskeyCredential.credential_id == credential_id)
      .first()
   )
   is_unknown = row is None

   if is_unknown:
      raise AuthError(401, "unknown credential")

   return row


def check_sign_count(stored, offered):
   """A counter that fails to advance is the cloned-authenticator signal, so the assertion is refused."""
   is_below = offered < stored
   is_stalled = offered == stored and stored != 0
   has_regressed = is_below or is_stalled

   if has_regressed:
      raise AuthError(401, "authenticator sign count regressed")


def login_finish(db, settings, store, challenge_id, credential, now=None):
   moment = now or utc_now()
   entry = store.take(challenge_id, "login", moment)
   row = credential_for(db, credential)
   verified = settings.verifier.finish_login(
      entry["challenge"], credential, row.public_key, row.sign_count
   )
   offered = int(verified["sign_count"])
   check_sign_count(row.sign_count, offered)
   row.sign_count = offered
   row.updated_at = as_iso(moment)
   db.flush()
   write_audit(db, row.user_id, "session_established", f"passkey_credentials:{row.id}", None, moment)
   token = open_auth_session(db, row.user_id, settings, moment)

   return {"user_id": row.user_id, "token": token}


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


def reauth_begin(db, settings, store, auth_session, now=None):
   moment = now or utc_now()
   begun = settings.verifier.begin_login()
   challenge_id = store.issue("reauth", begun["challenge"], moment, user_id=auth_session.user_id)

   return {"challenge_id": challenge_id, "options": begun["options"]}


def reauth_finish(db, settings, store, auth_session, challenge_id, credential, now=None):
   moment = now or utc_now()
   entry = store.take(challenge_id, "reauth", moment)
   is_other_user = entry["user_id"] != auth_session.user_id

   if is_other_user:
      raise AuthError(403, "the challenge belongs to another session")

   row = credential_for(db, credential)
   belongs_to_user = row.user_id == auth_session.user_id

   if not belongs_to_user:
      raise AuthError(403, "the credential belongs to another user")

   verified = settings.verifier.finish_login(
      entry["challenge"], credential, row.public_key, row.sign_count
   )
   offered = int(verified["sign_count"])
   check_sign_count(row.sign_count, offered)
   row.sign_count = offered
   row.updated_at = as_iso(moment)
   token = new_token()
   auth_session.reauth_token_hash = token_hash(token)
   auth_session.reauth_expires_at = as_iso(moment + timedelta(seconds=settings.reauth_ttl_seconds))
   auth_session.updated_at = as_iso(moment)
   db.flush()

   return {"reauth_token": token}


def consume_reauth(db, auth_session, token, now=None):
   """Single use: the stored hash is cleared whether or not the offered token matched."""
   moment = now or utc_now()
   stored = auth_session.reauth_token_hash
   deadline = auth_session.reauth_expires_at
   auth_session.reauth_token_hash = None
   auth_session.reauth_expires_at = None
   auth_session.updated_at = as_iso(moment)
   db.flush()
   is_unset = stored is None or deadline is None

   if is_unset:
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
