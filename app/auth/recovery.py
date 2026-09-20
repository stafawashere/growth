"""The recovery code path of docs/plan/09-security-and-privacy.md, "Recovery".

A code is generated once at registration, returned in plaintext exactly once to the caller, and
stored only as a hash. Presenting the correct code authenticates one new passkey registration and
consumes the code, so a second presentation is refused. The plaintext is never persisted and never
logged; only the salted, iterated hash reaches the users row.

The integrator wires register_via_recovery in where a locked-out student re-registers a passkey;
this module writes no route and touches no session cookie.
"""
import hashlib
import hmac
import secrets

from app.auth.service import AuthError, as_iso, new_id, utc_now, write_audit
from app.db import models

RECOVERY_AUDIT_ACTION = "passkey_recovery_used"
RECOVERY_CODE_ALPHABET = "23456789ABCDEFGHJKLMNPQRSTUVWXYZ"
RECOVERY_CODE_GROUPS = 4
RECOVERY_CODE_GROUP_LENGTH = 5
PBKDF2_ITERATIONS = 200_000


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

   if is_unset:
      return False

   algorithm, iterations, salt_hex, digest_hex = stored.split("$")
   salt = bytes.fromhex(salt_hex)
   expected = bytes.fromhex(digest_hex)
   candidate = hashlib.pbkdf2_hmac("sha256", code.encode(), salt, int(iterations))

   return hmac.compare_digest(candidate, expected)


def issue_recovery_code(db, user, now=None):
   moment = now or utc_now()
   code = generate_recovery_code()
   user.recovery_code_hash = hash_recovery_code(code)
   user.updated_at = as_iso(moment)
   db.flush()

   return code


def consume_recovery_code(db, user, code, now=None):
   moment = now or utc_now()
   matches = recovery_code_matches(code, user.recovery_code_hash)

   if not matches:
      return False

   user.recovery_code_hash = None
   user.updated_at = as_iso(moment)
   db.flush()

   return True


def register_via_recovery(db, user, code, verified_credential, now=None):
   moment = now or utc_now()
   consumed = consume_recovery_code(db, user, code, moment)

   if not consumed:
      raise AuthError(401, "recovery code is invalid or already used")

   timestamp = as_iso(moment)
   credential_row = models.PasskeyCredential(
      id=new_id("PKC"),
      user_id=user.id,
      credential_id=verified_credential["credential_id"],
      public_key=verified_credential["public_key"],
      sign_count=int(verified_credential.get("sign_count", 0)),
      transports=verified_credential.get("transports"),
      created_at=timestamp,
      updated_at=timestamp,
   )
   db.add(credential_row)
   db.flush()
   write_audit(
      db,
      user.id,
      RECOVERY_AUDIT_ACTION,
      f"passkey_credentials:{credential_row.id}",
      None,
      moment,
   )

   return credential_row
