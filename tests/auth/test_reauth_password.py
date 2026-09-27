"""POST /auth/reauth and the single-use token it mints, which POST /auth/password/change, /export,
/purge and PUT /settings/budgets spend (ruled 2026-09-27, replacing the passkey ceremony)."""
import pytest
from sqlalchemy.orm import Session as OrmSession

from app.api.routes.purge import PURGE_CONFIRMATION
from app.auth import service
from app.db import models
from tests.api.conftest import NEW_PASSWORD, PASSWORD, world  # noqa: F401
from tests.auth.helpers import set_user_columns, user_row

WRONG_PASSWORD = "not the right password"


def stored_reauth_hashes(engine):
   with OrmSession(engine) as db:
      return [row.reauth_token_hash for row in db.query(models.AuthSession).all()]


def change(client, reauth_token, current_password=PASSWORD, new_password=NEW_PASSWORD):
   payload = {"current_password": current_password, "new_password": new_password}
   offers_a_token = reauth_token is not None

   if offers_a_token:
      payload["reauth_token"] = reauth_token

   return client.post("/auth/password/change", json=payload)


def test_a_wrong_password_mints_no_token(world):  # noqa: F811
   client = world.client()
   world.register(client)

   refused = world.reauth(client, password=WRONG_PASSWORD)

   assert refused.status_code == 401
   assert refused.json() == {"detail": service.REAUTH_REFUSED_DETAIL}
   assert stored_reauth_hashes(world.engine) == [None]


@pytest.mark.parametrize("password", [None, 12345678901234, [PASSWORD], ""])
def test_a_password_that_is_not_text_is_a_401_not_a_500(world, password):  # noqa: F811
   client = world.client()
   world.register(client)

   refused = client.post("/auth/reauth", json={"password": password})

   assert refused.status_code == 401
   assert stored_reauth_hashes(world.engine) == [None]


def test_the_reauth_token_is_spent_by_its_first_use(world):  # noqa: F811
   client = world.client()
   world.register(client)
   token = world.reauth(client).json()["reauth_token"]
   first = client.post("/purge", json={"confirmation": PURGE_CONFIRMATION, "reauth_token": token})

   assert first.status_code == 200

   second = client.post("/purge", json={"confirmation": PURGE_CONFIRMATION, "reauth_token": token})

   assert 400 <= second.status_code < 500
   assert world.purges.calls == [world.purges.calls[0]]


@pytest.mark.parametrize("token_case", ["missing", "wrong", "used", "expired"])
def test_a_password_change_without_a_live_token_is_refused_and_changes_nothing(world, token_case):  # noqa: F811
   client = world.client()
   world.register(client)
   before = user_row(world.engine).password_hash
   is_missing = token_case == "missing"
   is_wrong = token_case == "wrong"
   is_used = token_case == "used"

   if is_missing:
      token = None
   elif is_wrong:
      world.reauth(client)
      token = "not-the-token"
   elif is_used:
      token = world.reauth(client).json()["reauth_token"]
      spent = change(client, token, current_password=WRONG_PASSWORD)

      assert spent.json() == {"detail": "the current password is incorrect"}
   else:
      world.settings.reauth_ttl_seconds = 0
      token = world.reauth(client).json()["reauth_token"]

   refused = change(client, token)

   assert refused.status_code == 401
   assert refused.json() == {"detail": service.CHANGE_NEEDS_REAUTH_DETAIL}
   assert user_row(world.engine).password_hash == before


def test_a_used_token_case_spends_the_token_on_its_first_use(world):  # noqa: F811
   """The positive control for the "used" case above: the same token, unspent, is accepted."""
   client = world.client()
   world.register(client)
   token = world.reauth(client).json()["reauth_token"]

   assert change(client, token).status_code == 200


def test_a_session_whose_user_has_no_password_is_refused_on_reauth_and_change(world):  # noqa: F811
   """A session from before the passkey retirement that somehow survived: the user row has no
   password, so neither route may treat the cookie as a signed-in student."""
   client = world.client()
   world.register(client)
   token = world.reauth(client).json()["reauth_token"]
   set_user_columns(world.engine, password_hash=None)

   reauth_refused = world.reauth(client)
   change_refused = change(client, token)

   assert reauth_refused.status_code == 401
   assert change_refused.status_code == 401
   assert user_row(world.engine).password_hash is None


def test_two_requests_holding_one_reauth_token_cannot_both_spend_it(world):  # noqa: F811
   """Each request loads its session row before either spends the token, as two concurrent calls to
   /auth/password/change or /export would, so a spend that trusted the loaded row would pass twice."""
   client = world.client()
   world.register(client)
   token = world.reauth(client).json()["reauth_token"]

   with OrmSession(world.engine) as first_db, OrmSession(world.engine) as second_db:
      first_row = first_db.query(models.AuthSession).one()
      second_row = second_db.query(models.AuthSession).one()

      assert first_row.reauth_token_hash is not None
      assert second_row.reauth_token_hash is not None

      first_spent = service.consume_reauth(first_db, first_row, token)
      first_db.commit()
      second_spent = service.consume_reauth(second_db, second_row, token)
      second_db.commit()

   assert (first_spent, second_spent) == (True, False)
   assert stored_reauth_hashes(world.engine) == [None]
