"""app/auth/guard.py on the three credential routes a stranger can reach: the Host allowlist, the
cross-site refusal and the plain-http refusal all answer before any password is read, any attempt
is counted, or the per-IP bucket is spent (ruled 2026-09-27, standing in for the origin binding a
passkey ceremony carried)."""
import pytest
from starlette.testclient import TestClient

from app.auth.guard import CROSS_SITE_DETAIL, FOREIGN_HOST_DETAIL, PLAIN_HTTP_DETAIL
from app.auth.limiter import SlidingWindowLimiter
from tests.api.conftest import PASSWORD, USERNAME, world  # noqa: F401
from tests.auth.helpers import lockout_state, user_count

WRONG_PASSWORD = "not the right password"
LAN_HOST = "lan-box.local"
ROUTE_BODIES = {
   "/auth/signup": {"username": "second_user", "password": WRONG_PASSWORD},
   "/auth/login": {"username": USERNAME, "password": WRONG_PASSWORD},
   "/auth/recovery/reset": {"recovery_code": "WRONG-CODE-HERE-XXXXX", "new_password": WRONG_PASSWORD},
}


def claimed_world(world):  # noqa: F811
   """One user with a clean lockout counter and a fresh limiter, so any count after the request
   under test is that request's doing."""
   assert world.register(world.client()).status_code == 200

   world.app.state.auth_limiter = SlidingWindowLimiter()

   return world


def nothing_was_counted(world):  # noqa: F811
   untouched_lockout = lockout_state(world.engine) == (0, None)
   untouched_limiter = world.app.state.auth_limiter.tracked_keys() == ()
   one_user = user_count(world.engine) == 1

   return untouched_lockout and untouched_limiter and one_user


def client_at(world, base_url):  # noqa: F811
   return TestClient(world.app, client=("127.0.0.1", 40000), base_url=base_url)


@pytest.mark.parametrize("path", sorted(ROUTE_BODIES))
def test_a_foreign_host_is_refused_before_anything_is_counted(world, path):  # noqa: F811
   claimed_world(world)
   rebound = client_at(world, "http://attacker.example")

   refused = rebound.post(path, json=ROUTE_BODIES[path])

   assert refused.status_code == 400
   assert refused.json()["detail"] == FOREIGN_HOST_DETAIL
   assert nothing_was_counted(world)


@pytest.mark.parametrize("path", sorted(ROUTE_BODIES))
def test_plain_http_on_a_served_non_loopback_host_is_refused_before_counting(world, path):  # noqa: F811
   claimed_world(world)
   world.settings.allowed_hosts = world.settings.allowed_hosts + (LAN_HOST,)
   plain = client_at(world, f"http://{LAN_HOST}")

   refused = plain.post(path, json=ROUTE_BODIES[path])

   assert refused.status_code == 400
   assert refused.json()["detail"] == PLAIN_HTTP_DETAIL
   assert nothing_was_counted(world)


@pytest.mark.parametrize("path", sorted(ROUTE_BODIES))
@pytest.mark.parametrize(
   "headers",
   [
      {"sec-fetch-site": "cross-site"},
      {"origin": "http://attacker.example"},
      {"origin": "http://127.0.0.1:9999"},
      {"origin": "null"},
   ],
)
def test_a_cross_site_request_is_refused_before_counting(world, path, headers):  # noqa: F811
   claimed_world(world)
   client = world.client()

   refused = client.post(path, json=ROUTE_BODIES[path], headers=headers)

   assert refused.status_code == 403
   assert refused.json()["detail"] == CROSS_SITE_DETAIL
   assert nothing_was_counted(world)


def test_the_page_s_own_origin_and_same_origin_fetch_are_let_through(world):  # noqa: F811
   """The positive control for the refusals above: the headers a same-origin page sends do not
   trip the guard, so the login reaches the password check."""
   claimed_world(world)
   client = world.client()
   headers = {"origin": "http://127.0.0.1", "sec-fetch-site": "same-origin"}

   answered = client.post("/auth/login", json={"username": USERNAME, "password": PASSWORD}, headers=headers)

   assert answered.status_code == 200


@pytest.mark.parametrize("path", sorted(ROUTE_BODIES))
def test_a_text_plain_body_is_a_422_that_echoes_nothing_and_counts_nothing(world, path):  # noqa: F811
   """A cross-site form can post text/plain without a preflight. It must neither spend the bucket
   nor count against the lockout, and the 422 must not repeat the password it carried."""
   claimed_world(world)
   client = world.client()
   raw_body = f'{{"username": "{USERNAME}", "password": "{WRONG_PASSWORD}"}}'

   refused = client.post(path, content=raw_body, headers={"content-type": "text/plain"})

   assert refused.status_code == 422
   assert WRONG_PASSWORD not in refused.text
   assert nothing_was_counted(world)


def test_reauth_from_another_site_is_refused_and_mints_no_token(world):  # noqa: F811
   client = world.client()
   world.register(client)

   refused = client.post("/auth/reauth", json={"password": PASSWORD}, headers={"sec-fetch-site": "cross-site"})

   assert refused.status_code == 403
   assert "reauth_token" not in refused.json()
   assert lockout_state(world.engine) == (0, None)
