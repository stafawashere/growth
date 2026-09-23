"""A second authenticator added while signed in, per docs/plan/09-security-and-privacy.md, "Recovery":
a second registered authenticator is the primary recovery answer, so registration prompts for one.
"""
from sqlalchemy.orm import Session as OrmSession

from app.db import models
from tests.api.conftest import CREDENTIAL_ID, world  # noqa: F401

SECOND_CREDENTIAL_ID = b"cred-2"


def add_authenticator(client, credential_id_hex, sign_count=0):
   begun = client.post("/auth/passkey/add/begin", json={})

   if begun.status_code != 200:
      return begun

   payload = {
      "challenge_id": begun.json()["challenge_id"],
      "credential": {"credential_id": credential_id_hex, "sign_count": sign_count},
   }

   return client.post("/auth/passkey/add/finish", json=payload)


def login_with(client, credential_id, sign_count):
   begun = client.post("/auth/passkey/login/begin", json={})
   payload = {
      "challenge_id": begun.json()["challenge_id"],
      "credential": {"credential_id": credential_id.hex(), "sign_count": sign_count},
   }

   return client.post("/auth/passkey/login/finish", json=payload)


def stored_credentials(engine):
   with OrmSession(engine) as db:
      rows = db.query(models.PasskeyCredential).order_by(models.PasskeyCredential.created_at).all()

      return [(row.user_id, row.credential_id) for row in rows]


def registered_user_id(engine):
   with OrmSession(engine) as db:
      return db.query(models.User.id).scalar()


def test_adding_an_authenticator_without_a_session_is_refused(world):  # noqa: F811
   registered = world.client()
   world.register(registered)
   anonymous = world.client()

   begun = anonymous.post("/auth/passkey/add/begin", json={})
   finished = anonymous.post(
      "/auth/passkey/add/finish",
      json={"challenge_id": "anything", "credential": {"credential_id": SECOND_CREDENTIAL_ID.hex()}},
   )

   assert begun.status_code == 401
   assert finished.status_code == 401
   assert stored_credentials(world.engine) == [(registered_user_id(world.engine), CREDENTIAL_ID)]


def test_a_signed_in_user_gains_a_second_credential_row(world):  # noqa: F811
   client = world.client()
   world.register(client)
   user_id = registered_user_id(world.engine)

   added = add_authenticator(client, SECOND_CREDENTIAL_ID.hex())

   assert added.status_code == 200
   assert stored_credentials(world.engine) == [
      (user_id, CREDENTIAL_ID),
      (user_id, SECOND_CREDENTIAL_ID),
   ]


def test_the_added_credential_signs_in_on_its_own(world):  # noqa: F811
   client = world.client()
   world.register(client)
   add_authenticator(client, SECOND_CREDENTIAL_ID.hex())
   fresh = world.client()

   offered = fresh.post("/auth/passkey/login/begin", json={}).json()["options"]["allowCredentials"]
   logged_in = login_with(fresh, SECOND_CREDENTIAL_ID, sign_count=1)

   assert {"id": SECOND_CREDENTIAL_ID.hex(), "type": "public-key"} in offered
   assert logged_in.status_code == 200
   assert logged_in.json() == {"user_id": registered_user_id(world.engine)}
   assert fresh.get("/me").status_code == 200


def test_an_already_stored_credential_is_not_added_twice(world):  # noqa: F811
   client = world.client()
   world.register(client)

   repeated = add_authenticator(client, CREDENTIAL_ID.hex())

   assert repeated.status_code == 409
   assert len(stored_credentials(world.engine)) == 1


def test_adding_an_authenticator_writes_a_passkey_registered_audit_row(world):  # noqa: F811
   client = world.client()
   world.register(client)
   add_authenticator(client, SECOND_CREDENTIAL_ID.hex())

   with OrmSession(world.engine) as db:
      added_row = (
         db.query(models.PasskeyCredential)
         .filter(models.PasskeyCredential.credential_id == SECOND_CREDENTIAL_ID)
         .first()
      )
      added_subject = None if added_row is None else f"passkey_credentials:{added_row.id}"
      subjects = [
         entry.subject
         for entry in db.query(models.AuditLog).filter(models.AuditLog.action == "passkey_registered")
      ]

   assert added_subject is not None
   assert added_subject in subjects

def test_a_challenge_issued_to_one_user_cannot_finish_under_another_users_session():
   from datetime import datetime, timezone
   from types import SimpleNamespace
   from unittest.mock import MagicMock

   import pytest

   from app.auth import service

   issued_at = datetime(2026, 9, 23, 12, 0, tzinfo=timezone.utc)
   store = service.ChallengeStore()
   challenge_id = store.issue("add_passkey", b"challenge-for-a", issued_at, user_id="USER-A")
   verifier_calls = []

   def recording_finish_registration(*arguments):
      verifier_calls.append(arguments)

      return {"credential_id": SECOND_CREDENTIAL_ID, "public_key": b"key", "sign_count": 0}

   verifier = SimpleNamespace(finish_registration=recording_finish_registration)
   other_users_session = SimpleNamespace(user_id="USER-B")

   with pytest.raises(service.AuthError) as refused:
      service.add_passkey_finish(
         MagicMock(),
         SimpleNamespace(verifier=verifier),
         store,
         other_users_session,
         challenge_id,
         {"credential_id": SECOND_CREDENTIAL_ID.hex()},
         now=issued_at,
      )

   assert refused.value.status_code == 403
   assert verifier_calls == []


def test_adding_an_authenticator_excludes_the_passkeys_already_stored(world):  # noqa: F811
   client = world.client()
   world.register(client)

   begun = client.post("/auth/passkey/add/begin", json={})

   assert begun.status_code == 200
   assert begun.json()["options"]["excludeCredentials"] == [CREDENTIAL_ID.hex()]
