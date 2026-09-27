"""The per-IP tier of app/auth/limiter.py on POST /auth/signup, /auth/login and /auth/recovery/reset:
a 429 with Retry-After once a peer has spent its window, answered before any scrypt work or
database write (ruled 2026-09-27)."""
import hashlib

import pytest

from app.auth.guard import RATE_LIMITED_DETAIL
from app.auth.limiter import SlidingWindowLimiter
from tests.api.conftest import USERNAME, world  # noqa: F401
from tests.auth.helpers import lockout_state, user_count

LIMIT = 3
WINDOW_SECONDS = 60
WRONG_PASSWORD = "not the right password"
ROUTE_BODIES = {
   "/auth/signup": {"username": "second_user", "password": WRONG_PASSWORD},
   "/auth/login": {"username": USERNAME, "password": WRONG_PASSWORD},
   "/auth/recovery/reset": {"recovery_code": "WRONG-CODE-HERE-XXXXX", "new_password": WRONG_PASSWORD},
}


def limited_world(world):  # noqa: F811
   assert world.register(world.client()).status_code == 200

   world.app.state.auth_limiter = SlidingWindowLimiter()
   world.settings.auth_rate_limit_count = LIMIT
   world.settings.auth_rate_limit_window_seconds = WINDOW_SECONDS

   return world


@pytest.mark.parametrize("path", sorted(ROUTE_BODIES))
def test_a_peer_over_the_limit_gets_a_429_with_retry_after(world, path):  # noqa: F811
   limited_world(world)
   client = world.client()

   for _ in range(LIMIT):
      admitted = client.post(path, json=ROUTE_BODIES[path])

      assert admitted.status_code != 429

   limited = client.post(path, json=ROUTE_BODIES[path])

   assert limited.status_code == 429
   assert limited.json() == {"detail": RATE_LIMITED_DETAIL}
   assert 1 <= int(limited.headers["retry-after"]) <= WINDOW_SECONDS


class ScryptSpy:
   def __init__(self, monkeypatch):
      self.calls = 0
      self.real_scrypt = hashlib.scrypt
      monkeypatch.setattr(hashlib, "scrypt", self)

   def __call__(self, *arguments, **keywords):
      self.calls += 1

      return self.real_scrypt(*arguments, **keywords)


def spend_the_window(client, path, body):
   for _ in range(LIMIT):
      assert client.post(path, json=body).status_code != 429


def test_a_limited_login_does_no_scrypt_work_and_counts_nothing(world, monkeypatch):  # noqa: F811
   limited_world(world)
   client = world.client()
   spend_the_window(client, "/auth/login", {"username": "nobody_here", "password": WRONG_PASSWORD})
   spy = ScryptSpy(monkeypatch)

   limited = client.post("/auth/login", json=ROUTE_BODIES["/auth/login"])

   assert limited.status_code == 429
   assert spy.calls == 0
   assert lockout_state(world.engine) == (0, None)

   admitted = world.client(host="::1").post("/auth/login", json=ROUTE_BODIES["/auth/login"])

   assert admitted.status_code == 401
   assert spy.calls > 0
   assert lockout_state(world.engine)[0] == 1


def test_a_limited_signup_hashes_nothing_and_claims_nothing(world, monkeypatch):  # noqa: F811
   world.settings.auth_rate_limit_count = LIMIT
   client = world.client()
   spend_the_window(client, "/auth/signup", {"username": "student", "password": "short"})
   spy = ScryptSpy(monkeypatch)

   limited = world.register(client)

   assert limited.status_code == 429
   assert spy.calls == 0
   assert user_count(world.engine) == 0


def test_a_limited_reset_does_not_spend_the_recovery_code(world):  # noqa: F811
   code = world.register(world.client()).json()["recovery_code"]
   world.app.state.auth_limiter = SlidingWindowLimiter()
   world.settings.auth_rate_limit_count = LIMIT
   client = world.client()
   spend_the_window(client, "/auth/recovery/reset", ROUTE_BODIES["/auth/recovery/reset"])

   limited = world.recover(client, code)

   assert limited.status_code == 429
   assert world.recover(world.client(host="::1"), code).status_code == 200


def test_another_peer_address_has_its_own_window(world):  # noqa: F811
   limited_world(world)
   first = world.client(host="127.0.0.1")

   for _ in range(LIMIT + 1):
      first.post("/auth/login", json=ROUTE_BODIES["/auth/login"])

   other_peer = world.client(host="::1")

   assert other_peer.post("/auth/login", json=ROUTE_BODIES["/auth/login"]).status_code == 401


def test_the_limit_is_read_from_settings_on_every_request(world):  # noqa: F811
   limited_world(world)
   client = world.client()

   for _ in range(LIMIT):
      client.post("/auth/login", json=ROUTE_BODIES["/auth/login"])

   assert client.post("/auth/login", json=ROUTE_BODIES["/auth/login"]).status_code == 429

   world.settings.auth_rate_limit_count = LIMIT + 1

   assert client.post("/auth/login", json=ROUTE_BODIES["/auth/login"]).status_code == 401


def test_a_refused_request_is_not_recorded_so_the_window_moves_on():
   limiter = SlidingWindowLimiter()

   assert limiter.admit("peer", 0, 2, 60) is None
   assert limiter.admit("peer", 10, 2, 60) is None
   assert limiter.admit("peer", 20, 2, 60) == 40
   assert limiter.admit("peer", 59, 2, 60) == 1
   assert limiter.admit("peer", 61, 2, 60) is None


def test_stale_windows_are_pruned():
   limiter = SlidingWindowLimiter()
   limiter.admit("old_peer", 0, 5, 60)
   limiter.admit("new_peer", 30, 5, 60)

   limiter.admit("new_peer", 61, 5, 60)

   assert limiter.tracked_keys() == ("new_peer",)


def test_the_number_of_tracked_peers_is_capped_dropping_the_oldest():
   limiter = SlidingWindowLimiter(max_keys=3)

   for index in range(6):
      limiter.admit(f"peer-{index}", index, 5, 600)

   assert limiter.tracked_keys() == ("peer-3", "peer-4", "peer-5")
