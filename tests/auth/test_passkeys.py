"""Passkey registration, login, re-authentication and logout over the HTTP layer."""
import pytest

from app.api.routes.purge import PURGE_CONFIRMATION
from app.auth.webauthn import LibraryVerifier
from tests.api.conftest import CREDENTIAL_ID, world  # noqa: F401


def test_register_refused_once_users_nonempty(world):  # noqa: F811
   client = world.client()

   assert world.register(client).status_code == 200
   assert world.seeds.calls != []

   refused_begin = client.post("/auth/passkey/register/begin", json={"display_name": "Second"})

   assert refused_begin.status_code == 403

   refused_finish = client.post(
      "/auth/passkey/register/finish",
      json={"challenge_id": "anything", "credential": {"sign_count": 1}},
   )

   assert refused_finish.status_code == 403


def test_login_finish_sets_httponly_lax_cookie(world):  # noqa: F811
   client = world.client()
   world.register(client)
   client.cookies.clear()
   logged_in = world.login(client, sign_count=6)

   assert logged_in.status_code == 200

   header = logged_in.headers["set-cookie"]

   assert "HttpOnly" in header
   assert "SameSite=lax" in header.replace("SameSite=Lax", "SameSite=lax")
   assert "Secure" not in header

   assert client.get("/me").status_code == 200

   logged_out = client.post("/auth/logout", json={})

   assert logged_out.status_code == 200
   assert client.get("/me").status_code == 401


def test_sign_count_regression_refused(world):  # noqa: F811
   client = world.client()
   world.register(client, sign_count=5)
   client.cookies.clear()
   regressed = world.login(client, sign_count=3)

   assert regressed.status_code == 401
   assert client.get("/me").status_code == 401

   accepted = world.login(client, sign_count=6)

   assert accepted.status_code == 200


def test_reauth_token_single_use(world):  # noqa: F811
   client = world.client()
   world.register(client)
   token = world.reauth(client).json()["reauth_token"]
   first = client.post(
      "/purge",
      json={"confirmation": PURGE_CONFIRMATION, "reauth_token": token},
   )

   assert first.status_code == 200

   second = client.post(
      "/purge",
      json={"confirmation": PURGE_CONFIRMATION, "reauth_token": token},
   )

   assert 400 <= second.status_code < 500
   assert world.purges.calls == [world.purges.calls[0]]


def test_library_verifier_names_the_missing_package():
   verifier = LibraryVerifier(rp_id="localhost", origin="http://127.0.0.1:8000")

   with pytest.raises(RuntimeError) as raised:
      verifier.begin_registration("USER-1", "Student")

   assert "webauthn" in str(raised.value)
