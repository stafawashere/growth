"""GET /auth/status tells the account screen whether the installation already has its one user.

docs/plan/09-security-and-privacy.md, "Registration", opens registration only while users is empty,
so a signup refusal already reveals the same bit; the answer here is read from the users table.
A loopback caller is also told needs_password, true while a user migrated from passkeys has no
password yet; any other caller gets user_exists alone, so the migration window is not advertised.
"""
from datetime import datetime, timezone

from sqlalchemy.orm import Session as OrmSession

from app.auth.cookies import SESSION_COOKIE
from app.db import models
from tests.api.conftest import world  # noqa: F401

SEEDED_AT = datetime(2026, 3, 1, 9, 0, 0, tzinfo=timezone.utc).isoformat()


def seed_user(engine):
   with OrmSession(engine) as db:
      db.add(
         models.User(
            id="USER-SEEDED",
            display_name="student",
            exam_date="2027-05-10",
            purge_after="2027-06-09",
            created_at=SEEDED_AT,
            updated_at=SEEDED_AT,
         )
      )
      db.commit()


def test_status_reports_no_user_on_an_empty_installation(world):  # noqa: F811
   client = world.client()

   answered = client.get("/auth/status")

   assert answered.status_code == 200
   assert answered.json() == {"user_exists": False, "needs_password": False}


def test_status_reports_a_user_seeded_in_the_database_without_a_cookie(world):  # noqa: F811
   seed_user(world.engine)
   client = world.client()

   answered = client.get("/auth/status")

   assert client.cookies.get(SESSION_COOKIE) is None
   assert answered.status_code == 200
   assert answered.json() == {"user_exists": True, "needs_password": True}


def test_status_follows_a_registration_through_the_route(world):  # noqa: F811
   client = world.client()

   assert client.get("/auth/status").json() == {"user_exists": False, "needs_password": False}
   assert world.register(client).status_code == 200

   anonymous = world.client()

   assert anonymous.get("/auth/status").json() == {"user_exists": True, "needs_password": False}


def test_status_tells_a_remote_caller_only_whether_a_user_exists(world):  # noqa: F811
   seed_user(world.engine)
   remote = world.client(host="203.0.113.7")

   answered = remote.get("/auth/status")

   assert answered.status_code == 200
   assert answered.json() == {"user_exists": True}


def test_status_withholds_needs_password_from_a_loopback_peer_under_a_foreign_host(world):  # noqa: F811
   """A DNS-rebound page, or any caller behind a reverse proxy, arrives from 127.0.0.1 with a Host
   that is not loopback."""
   seed_user(world.engine)
   rebound = world.client()

   answered = rebound.get("/auth/status", headers={"host": "attacker.example"})

   assert answered.status_code == 200
   assert answered.json() == {"user_exists": True}
