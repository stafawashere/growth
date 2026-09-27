"""The Secure flag and the refusal rule of docs/plan/09-security-and-privacy.md,

"Transport and hosting", "TLS when exposed" and "Localhost first". Secure on the session cookie
must depend on the request's own host, not only on the configured bind host, and a request that
names a non-loopback host over plain http must be refused rather than served an insecure cookie.
"""
import hashlib

from sqlalchemy.orm import Session as OrmSession

from app.auth.cookies import SESSION_COOKIE
from app.db import models
from tests.api.conftest import PASSWORD, USERNAME, world  # noqa: F401

LAN_HOST = "lan-box.local"


def token_hash_of(raw_token):
   return hashlib.sha256(raw_token.encode()).hexdigest()


def register_at(world, client, url):  # noqa: F811
   """lan-box.local is added to the served hosts, so the Host allowlist lets the request reach the
   transport rule these tests are about."""
   world.settings.allowed_hosts = world.settings.allowed_hosts + (LAN_HOST,)

   return client.post(url, json={"username": USERNAME, "password": PASSWORD})


def auth_session_for(engine, token):
   with OrmSession(engine) as db:
      return (
         db.query(models.AuthSession)
         .filter(models.AuthSession.token_hash == token_hash_of(token))
         .one_or_none()
      )


def all_users(engine):
   with OrmSession(engine) as db:
      return db.query(models.User).all()


def all_auth_sessions(engine):
   with OrmSession(engine) as db:
      return db.query(models.AuthSession).all()


def test_loopback_bind_and_loopback_request_keep_current_behaviour(world):  # noqa: F811
   client = world.client()

   finished = register_at(world, client, "http://127.0.0.1/auth/signup")

   assert finished.status_code == 200

   header = finished.headers["set-cookie"]

   assert "Secure" not in header

   token = client.cookies[SESSION_COOKIE]
   row = auth_session_for(world.engine, token)

   assert row is not None
   assert row.user_id == finished.json()["user"]["id"]


def test_non_loopback_request_over_https_gets_secure_cookie(world):  # noqa: F811
   client = world.client()

   finished = register_at(world, client, f"https://{LAN_HOST}/auth/signup")

   assert finished.status_code == 200

   header = finished.headers["set-cookie"]

   assert "Secure" in header

   token = client.cookies[SESSION_COOKIE]
   row = auth_session_for(world.engine, token)

   assert row is not None
   assert row.user_id == finished.json()["user"]["id"]


def test_non_loopback_request_over_plain_http_is_refused(world):  # noqa: F811
   client = world.client()

   finished = register_at(world, client, f"http://{LAN_HOST}/auth/signup")

   assert finished.status_code == 400
   assert "set-cookie" not in finished.headers
   assert SESSION_COOKIE not in client.cookies

   unauthenticated = client.get("http://127.0.0.1/me")

   assert unauthenticated.status_code == 401
   assert all_users(world.engine) == []
   assert all_auth_sessions(world.engine) == []


def test_ipv6_loopback_request_gets_cookie_without_secure(world):  # noqa: F811
   registration_client = world.client()
   world.register(registration_client)

   client = world.client(host="::1")
   logged_in = world.login(client)

   assert logged_in.status_code == 200

   header = logged_in.headers["set-cookie"]

   assert "Secure" not in header

   token = client.cookies[SESSION_COOKIE]
   row = auth_session_for(world.engine, token)

   assert row is not None
