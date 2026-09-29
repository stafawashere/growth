"""The account page's routes: GET /me names the username, PUT /me renames the display name, and
POST /auth/recovery/rotate replaces the recovery code behind a fresh re-authentication."""
from sqlalchemy.orm import Session as OrmSession

from app.auth.recovery import recovery_code_matches
from app.db import models
from tests.api.conftest import PASSWORD, USERNAME, world  # noqa: F401


def stored_user(engine):
   with OrmSession(engine) as db:
      return db.query(models.User).one()


def test_me_names_the_username(world):  # noqa: F811
   client = world.client()
   world.register(client)

   assert client.get("/me").json()["username"] == USERNAME


def test_put_me_renames_the_display_name_and_trims_it(world):  # noqa: F811
   client = world.client()
   world.register(client)

   renamed = client.put("/me", json={"display_name": "  Sam  "})

   assert renamed.status_code == 200
   assert renamed.json()["display_name"] == "Sam"
   assert client.get("/me").json()["display_name"] == "Sam"


def test_put_me_refuses_a_blank_or_overlong_name_and_keeps_the_old_one(world):  # noqa: F811
   client = world.client()
   world.register(client)
   before = client.get("/me").json()["display_name"]

   blank = client.put("/me", json={"display_name": "   "})
   overlong = client.put("/me", json={"display_name": "x" * 61})
   not_text = client.put("/me", json={"display_name": 7})

   assert (blank.status_code, overlong.status_code, not_text.status_code) == (400, 400, 400)
   assert client.get("/me").json()["display_name"] == before


def test_put_me_needs_a_session(world):  # noqa: F811
   client = world.client()

   assert client.put("/me", json={"display_name": "Sam"}).status_code == 401


def test_rotating_the_recovery_code_needs_a_fresh_reauthentication(world):  # noqa: F811
   client = world.client()
   world.register(client)
   hash_before = stored_user(world.engine).recovery_code_hash

   refused = client.post("/auth/recovery/rotate", json={"reauth_token": "not-a-token"})

   assert refused.status_code == 401
   assert stored_user(world.engine).recovery_code_hash == hash_before


def test_rotating_the_recovery_code_replaces_it_with_the_one_returned(world):  # noqa: F811
   client = world.client()
   first_code = world.register(client).json()["recovery_code"]
   token = world.reauth(client).json()["reauth_token"]

   rotated = client.post("/auth/recovery/rotate", json={"reauth_token": token})

   assert rotated.status_code == 200

   new_code = rotated.json()["recovery_code"]
   stored = stored_user(world.engine).recovery_code_hash

   assert new_code != first_code
   assert recovery_code_matches(new_code, stored)
   assert not recovery_code_matches(first_code, stored)


def test_a_rotated_code_resets_the_password(world):  # noqa: F811
   client = world.client()
   world.register(client)
   token = world.reauth(client).json()["reauth_token"]
   new_code = client.post("/auth/recovery/rotate", json={"reauth_token": token}).json()["recovery_code"]

   other_device = world.client()
   reset = world.recover(other_device, new_code, new_password="a fresh long password")

   assert reset.status_code == 200
   assert world.login(world.client(), password="a fresh long password").status_code == 200
   assert world.login(world.client(), password=PASSWORD).status_code == 401
