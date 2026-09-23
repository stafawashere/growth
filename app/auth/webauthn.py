"""The passkey verifier boundary.

docs/plan/09-security-and-privacy.md fixes WebAuthn passkeys as the only authentication method but
docs/plan/06-architecture.md names no library for them, and P1 adds no dependency that 06 does not
name. So the ceremony verification sits behind a protocol: the application depends on the four
methods below, LibraryVerifier binds them to the webauthn package when it is installed, and the
tests bind them to a double. Nothing above this boundary knows which is in place.
"""
import json
from typing import Protocol

MISSING_PACKAGE = (
   "LibraryVerifier needs the webauthn package, which is not installed; install it or pass "
   "another PasskeyVerifier as Settings.verifier"
)


class PasskeyVerifier(Protocol):
   def begin_registration(self, user_id, user_name):
      """Return {"challenge": str, "options": dict} for the authenticator."""

   def finish_registration(self, challenge, credential):
      """Return {"credential_id": bytes, "public_key": bytes, "sign_count": int, "transports": str | None}."""

   def begin_login(self, credential_ids=None):
      """Return {"challenge": str, "options": dict} for an assertion ceremony.

      credential_ids, when given, is the stored credential ids to send as allowCredentials, so a
      non-discoverable credential can be targeted directly rather than requiring a resident key."""

   def finish_login(self, challenge, credential, public_key, stored_sign_count):
      """Return {"sign_count": int}, the authenticator's counter after this assertion."""


def _webauthn_module():
   try:
      import webauthn
   except ImportError as missing:
      raise RuntimeError(MISSING_PACKAGE) from missing

   return webauthn


class LibraryVerifier:
   def __init__(self, rp_id, origin, rp_name="Growth"):
      self.rp_id = rp_id
      self.origin = origin
      self.rp_name = rp_name

   def begin_registration(self, user_id, user_name, exclude_credential_ids=()):
      webauthn = _webauthn_module()
      excluded = [
         webauthn.helpers.structs.PublicKeyCredentialDescriptor(id=credential_id)
         for credential_id in exclude_credential_ids
      ]
      options = webauthn.generate_registration_options(
         rp_id=self.rp_id,
         rp_name=self.rp_name,
         user_id=user_id.encode(),
         user_name=user_name,
         exclude_credentials=excluded,
      )

      return {
         "challenge": webauthn.helpers.bytes_to_base64url(options.challenge),
         "options": json.loads(webauthn.options_to_json(options)),
      }

   def finish_registration(self, challenge, credential):
      webauthn = _webauthn_module()
      verified = webauthn.verify_registration_response(
         credential=credential,
         expected_challenge=webauthn.helpers.base64url_to_bytes(challenge),
         expected_origin=self.origin,
         expected_rp_id=self.rp_id,
      )

      return {
         "credential_id": verified.credential_id,
         "public_key": verified.credential_public_key,
         "sign_count": verified.sign_count,
         "transports": None,
      }

   def begin_login(self, credential_ids=None):
      webauthn = _webauthn_module()
      allow_credentials = [
         webauthn.helpers.structs.PublicKeyCredentialDescriptor(id=credential_id)
         for credential_id in (credential_ids or [])
      ]
      options = webauthn.generate_authentication_options(
         rp_id=self.rp_id,
         allow_credentials=allow_credentials or None,
      )

      return {
         "challenge": webauthn.helpers.bytes_to_base64url(options.challenge),
         "options": json.loads(webauthn.options_to_json(options)),
      }

   def finish_login(self, challenge, credential, public_key, stored_sign_count):
      webauthn = _webauthn_module()
      verified = webauthn.verify_authentication_response(
         credential=credential,
         expected_challenge=webauthn.helpers.base64url_to_bytes(challenge),
         expected_origin=self.origin,
         expected_rp_id=self.rp_id,
         credential_public_key=public_key,
         credential_current_sign_count=stored_sign_count,
      )

      return {"sign_count": verified.new_sign_count}
