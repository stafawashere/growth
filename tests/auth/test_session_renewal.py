"""Sessions slide on use, outlive a server restart, and do not collide across local ports.

The operator's ruling of 2026-09-29 in docs/plan/09-security-and-privacy.md: a session ends after
session_ttl_seconds without a request, not a fixed time after sign-in, and each port on a host
gets its own session cookie.
"""
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session as OrmSession
from starlette.testclient import TestClient

from app.api.app import create_app
from app.auth.cookies import SESSION_COOKIE
from app.db import models
from tests.api.conftest import world  # noqa: F401

HOUR = 60 * 60
DAY = 24 * HOUR


def only_session(engine):
   with OrmSession(engine) as db:
      return db.query(models.AuthSession).one()


def set_session_expiry(engine, expires_at):
   with OrmSession(engine) as db:
      row = db.query(models.AuthSession).one()
      row.expires_at = expires_at.isoformat()
      db.commit()


def expiry_of(engine):
   return datetime.fromisoformat(only_session(engine).expires_at)


def signed_in_client(world, base_url="http://127.0.0.1"):  # noqa: F811
   client = TestClient(world.app, client=("127.0.0.1", 40000), base_url=base_url)
   world.register(client)

   return client


def test_a_request_after_the_renew_interval_slides_the_expiry_and_resends_the_cookie(world):  # noqa: F811
   client = signed_in_client(world)
   now = datetime.now(timezone.utc)
   set_session_expiry(world.engine, now + timedelta(days=2))

   answered = client.get("/me")

   assert answered.status_code == 200

   renewed_expiry = expiry_of(world.engine)
   expected_expiry = now + timedelta(seconds=world.settings.session_ttl_seconds)

   assert abs((renewed_expiry - expected_expiry).total_seconds()) < 60

   cookie_header = answered.headers.get("set-cookie", "")

   assert cookie_header.startswith(f"{SESSION_COOKIE}=")
   assert f"Max-Age={world.settings.session_ttl_seconds}" in cookie_header


def test_requests_inside_the_renew_interval_do_not_rewrite_the_session(world):  # noqa: F811
   client = signed_in_client(world)
   expiry_before = expiry_of(world.engine)

   answered = client.get("/me")

   assert answered.status_code == 200
   assert expiry_of(world.engine) == expiry_before
   assert "set-cookie" not in answered.headers


def test_a_session_idle_past_its_window_is_refused(world):  # noqa: F811
   client = signed_in_client(world)
   set_session_expiry(world.engine, datetime.now(timezone.utc) - timedelta(minutes=1))

   answered = client.get("/me")

   assert answered.status_code == 401


def test_the_session_window_is_ninety_days(world):  # noqa: F811
   assert world.settings.session_ttl_seconds == 90 * DAY
   assert world.settings.session_renew_interval_seconds == HOUR


def test_a_new_application_over_the_same_database_accepts_the_old_cookie(world):  # noqa: F811
   client = signed_in_client(world)
   token = client.cookies[SESSION_COOKIE]

   restarted = create_app(world.settings)
   after_restart = TestClient(restarted, client=("127.0.0.1", 40000), base_url="http://127.0.0.1")
   after_restart.cookies.set(SESSION_COOKIE, token)

   answered = after_restart.get("/me")

   assert answered.status_code == 200


def test_an_origin_with_a_port_gets_a_cookie_named_for_that_port(world):  # noqa: F811
   client = signed_in_client(world, base_url="http://localhost:8000")
   cookie_header_names = [cookie.name for cookie in client.cookies.jar]

   assert f"{SESSION_COOKIE}_8000" in cookie_header_names
   assert SESSION_COOKIE not in cookie_header_names
   assert client.get("/me").status_code == 200


def test_a_cookie_under_the_bare_name_still_signs_in_and_moves_to_the_port_name(world):  # noqa: F811
   registering = signed_in_client(world, base_url="http://localhost:8000")
   token = registering.cookies[f"{SESSION_COOKIE}_8000"]

   older_browser = TestClient(world.app, client=("127.0.0.1", 40000), base_url="http://localhost:8000")
   older_browser.cookies.set(SESSION_COOKIE, token)

   answered = older_browser.get("/me")

   assert answered.status_code == 200
   assert answered.headers.get("set-cookie", "").startswith(f"{SESSION_COOKIE}_8000=")


def test_sign_out_clears_the_port_cookie_and_the_bare_one(world):  # noqa: F811
   client = signed_in_client(world, base_url="http://localhost:8000")

   signed_out = client.post("/auth/logout", json={})

   assert signed_out.status_code == 200

   cleared_names = [value.split("=", 1)[0] for value in signed_out.headers.get_list("set-cookie")]

   assert f"{SESSION_COOKIE}_8000" in cleared_names
   assert SESSION_COOKIE in cleared_names
   assert client.get("/me").status_code == 401
