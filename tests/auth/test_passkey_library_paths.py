"""Two defects fixed against the real py_webauthn library rather than tests/api/conftest.py's
FakeVerifier: begin_login must offer the stored credential ids as allowCredentials so a
non-discoverable credential can sign in, and a malformed ceremony must be refused with a 4xx
rather than surfacing as an unhandled 500, with no row written for it.
"""
import os
from datetime import datetime, timezone

import webauthn
from sqlalchemy.orm import Session as OrmSession
from starlette.testclient import TestClient

from app.api.app import Settings, create_app
from app.auth.webauthn import LibraryVerifier
from app.db import models

RP_ID = "localhost"
ORIGIN = "http://127.0.0.1:8000"
NOW = datetime(2026, 3, 1, tzinfo=timezone.utc).isoformat()


def library_app(tmp_path):
   engine = models.make_engine(tmp_path / "growth.db")
   settings = Settings(engine=engine, verifier=LibraryVerifier(rp_id=RP_ID, origin=ORIGIN))
   application = create_app(settings)

   return application, engine


def client_for(application):
   return TestClient(application, base_url=ORIGIN)


def insert_user(engine, user_id):
   with OrmSession(engine) as db:
      db.add(
         models.User(
            id=user_id,
            display_name="Student",
            exam_date="2027-05-10",
            purge_after="2027-06-09",
            created_at=NOW,
            updated_at=NOW,
         )
      )
      db.commit()


def insert_credential(engine, user_id, credential_id, sign_count=0):
   with OrmSession(engine) as db:
      db.add(
         models.PasskeyCredential(
            id=f"PKC-{credential_id.hex()}",
            user_id=user_id,
            credential_id=credential_id,
            public_key=b"stub-public-key",
            sign_count=sign_count,
            transports=None,
            created_at=NOW,
            updated_at=NOW,
         )
      )
      db.commit()


def test_login_begin_allow_credentials_matches_stored_credentials_with_real_verifier(tmp_path):
   application, engine = library_app(tmp_path)
   user_id = "USER-1"
   first_credential_id = os.urandom(32)
   second_credential_id = os.urandom(32)
   insert_user(engine, user_id)
   insert_credential(engine, user_id, first_credential_id)
   insert_credential(engine, user_id, second_credential_id)

   response = client_for(application).post("/auth/passkey/login/begin", json={})

   assert response.status_code == 200

   allow_credentials = response.json()["options"]["allowCredentials"]
   offered_ids = {descriptor["id"] for descriptor in allow_credentials}
   expected_ids = {
      webauthn.helpers.bytes_to_base64url(first_credential_id),
      webauthn.helpers.bytes_to_base64url(second_credential_id),
   }

   assert offered_ids == expected_ids
   assert all(descriptor["type"] == "public-key" for descriptor in allow_credentials)


def test_register_finish_malformed_credential_refused_and_writes_nothing(tmp_path):
   application, engine = library_app(tmp_path)
   client = client_for(application)
   begun = client.post("/auth/passkey/register/begin", json={"display_name": "Student"})

   assert begun.status_code == 200

   finished = client.post(
      "/auth/passkey/register/finish",
      json={"challenge_id": begun.json()["challenge_id"], "credential": {}},
   )

   assert finished.status_code == 400
   assert "credential_id" not in finished.json()["detail"]
   assert "public_key" not in finished.json()["detail"]

   with OrmSession(engine) as db:
      assert db.query(models.User).count() == 0
      assert db.query(models.PasskeyCredential).count() == 0


def test_login_finish_malformed_credential_refused_and_writes_nothing(tmp_path):
   application, engine = library_app(tmp_path)
   client = client_for(application)
   user_id = "USER-1"
   credential_id = os.urandom(32)
   insert_user(engine, user_id)
   insert_credential(engine, user_id, credential_id, sign_count=0)
   begun = client.post("/auth/passkey/login/begin", json={})

   assert begun.status_code == 200

   finished = client.post(
      "/auth/passkey/login/finish",
      json={
         "challenge_id": begun.json()["challenge_id"],
         "credential": {"credential_id": credential_id.hex()},
      },
   )

   assert finished.status_code == 400
   assert credential_id.hex() not in finished.json()["detail"]

   with OrmSession(engine) as db:
      assert db.query(models.AuthSession).count() == 0
      stored = db.query(models.PasskeyCredential).filter(
         models.PasskeyCredential.credential_id == credential_id
      ).one()

      assert stored.sign_count == 0


def test_registration_options_exclude_the_credentials_already_stored():
   verifier = LibraryVerifier(rp_id=RP_ID, origin=ORIGIN)
   stored_credential_id = b"stored-credential"

   begun = verifier.begin_registration("USER-1", "Student", [stored_credential_id])
   excluded_ids = [entry["id"] for entry in begun["options"].get("excludeCredentials", [])]

   assert excluded_ids == [webauthn.helpers.bytes_to_base64url(stored_credential_id)]
