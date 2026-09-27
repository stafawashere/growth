"""The recovery code path of docs/plan/09-security-and-privacy.md, "Recovery".

A code is generated once at sign-up, returned in plaintext exactly once to the caller, and stored
only as a hash. Since passwords replaced passkeys (ruled 2026-09-27), presenting the correct code
resets the password: it signs every session out, clears the lockout, sets the new password, and
consumes the code, so a second presentation is refused. A replacement code is issued and shown once.
The plaintext is never persisted and never logged; only the salted, iterated hash reaches the users
row.

The code is spent with one conditional UPDATE that matches only while the stored hash is still the
one that was checked, so two resets racing with the same code cannot both succeed.
"""
import hashlib
import hmac
import secrets

from sqlalchemy import text

from app.auth import passwords
from app.auth.service import (
   AuthRefusal,
   as_iso,
   hash_with_settings,
   open_auth_session,
   sole_user,
   utc_now,
   write_audit,
)
from app.db import models

RECOVERY_AUDIT_ACTION = "password_reset_via_recovery"
RECOVERY_CODE_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
RECOVERY_CODE_GROUPS = 4
RECOVERY_CODE_GROUP_LENGTH = 5
PBKDF2_ITERATIONS = 200_000
RECOVERY_REFUSED_DETAIL = "recovery code is invalid or already used"
NO_USER_DETAIL = "this installation has no user to recover"


def generate_recovery_code():
   groups = [
      "".join(secrets.choice(RECOVERY_CODE_ALPHABET) for _ in range(RECOVERY_CODE_GROUP_LENGTH))
      for _ in range(RECOVERY_CODE_GROUPS)
   ]

   return "-".join(groups)


def hash_recovery_code(code):
   salt = secrets.token_bytes(16)
   digest = hashlib.pbkdf2_hmac("sha256", code.encode(), salt, PBKDF2_ITERATIONS)

   return f"pbkdf2_sha256${PBKDF2_ITERATIONS}${salt.hex()}${digest.hex()}"


def recovery_code_matches(code, stored):
   is_unset = not stored
   is_text = isinstance(code, str)
   cannot_match = is_unset or not is_text

   if cannot_match:
      return False

   try:
      algorithm, iterations, salt_hex, digest_hex = stored.split("$")
      salt = bytes.fromhex(salt_hex)
      expected = bytes.fromhex(digest_hex)
      candidate = hashlib.pbkdf2_hmac("sha256", code.encode(), salt, int(iterations))
   except (ValueError, UnicodeEncodeError):
      return False

   return hmac.compare_digest(candidate, expected)


def issue_recovery_code(db, user, now=None):
   moment = now or utc_now()
   code = generate_recovery_code()
   user.recovery_code_hash = hash_recovery_code(code)
   user.updated_at = as_iso(moment)
   db.flush()

   return code


def consume_recovery_code(db, user, code, now=None):
   """True only for the call whose UPDATE cleared the hash it had matched against."""
   moment = now or utc_now()
   user_id = user.id
   stored = user.recovery_code_hash
   matches = recovery_code_matches(code, stored)

   if not matches:
      return False

   cleared = db.execute(
      text(
         "UPDATE users SET recovery_code_hash = NULL, updated_at = :now "
         "WHERE id = :id AND recovery_code_hash = :matched"
      ),
      {"now": as_iso(moment), "id": user_id, "matched": stored},
   )
   db.expire_all()

   return cleared.rowcount == 1


def reset_password_via_recovery(db, settings, code, new_password, username=None, now=None):
   """Returns {user, token, recovery_code}, or an AuthRefusal: 400 for a password or username the
   rules refuse, 404 when there is no user, 401 for a wrong or spent code. username is required
   only while the user has none, as an account migrated from passkeys does, and is otherwise
   ignored, so a reset can never rename the account."""
   moment = now or utc_now()
   problem = passwords.password_problem(new_password)

   if problem is not None:
      return AuthRefusal(400, problem)

   user = sole_user(db)
   is_unclaimed = user is None

   if is_unclaimed:
      return AuthRefusal(404, NO_USER_DETAIL)

   user_id = user.id
   needs_username = user.username is None
   chosen_username = passwords.normalise_username(username) if needs_username else None
   is_missing_username = needs_username and chosen_username is None

   if is_missing_username:
      return AuthRefusal(400, passwords.USERNAME_RULE)

   consumed = consume_recovery_code(db, user, code, moment)

   if not consumed:
      return AuthRefusal(401, RECOVERY_REFUSED_DETAIL)

   user = db.get(models.User, user_id)
   user.password_hash = hash_with_settings(new_password, settings)
   user.failed_login_count = 0
   user.locked_until = None
   user.updated_at = as_iso(moment)

   if needs_username:
      user.username = chosen_username

   db.query(models.AuthSession).filter(models.AuthSession.user_id == user_id).delete(
      synchronize_session=False
   )
   db.flush()
   write_audit(db, user_id, RECOVERY_AUDIT_ACTION, f"users:{user_id}", None, moment)
   token = open_auth_session(db, user_id, settings, moment)
   replacement = issue_recovery_code(db, user, moment)

   return {"user": user, "token": token, "recovery_code": replacement}
