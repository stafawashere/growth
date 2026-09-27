"""The request checks every credential route runs before it reads a secret (ruled 2026-09-27).

A passkey ceremony was bound to the relying party id and the origin by the authenticator itself. A
password is not bound to anything, so the server does the binding, in this order: the Host must be
one this installation serves, which refuses a DNS-rebound page; a browser that says the request is
cross-site, or sends an Origin other than the one it reached, is refused, which is the CSRF check;
and a non-loopback request over plain http is refused with the same answer the cookie rule in
app/auth/cookies.py gives, before any password is processed rather than after.

Each check returns a JSONResponse rather than raising, like every refusal on these routes, so a
counter the route has already written is still committed by app/api/deps.py get_db.
"""
import time

from fastapi.responses import JSONResponse

from app.auth.cookies import LOOPBACK_HOSTS, refuses_session_cookie

FOREIGN_HOST_DETAIL = "this installation does not serve that host"
CROSS_SITE_DETAIL = "a credential request must come from this installation's own page"
PLAIN_HTTP_DETAIL = "refusing to set a session cookie over plain http on a non-loopback origin"
RATE_LIMITED_DETAIL = "too many attempts; wait before trying again"
DEFAULT_ALLOWED_HOSTS = tuple(sorted(LOOPBACK_HOSTS))


def bare_host(host):
   is_text = isinstance(host, str)

   if not is_text:
      return ""

   return host.strip().strip("[]").lower()


def host_is_allowed(request, settings):
   allowed = {bare_host(host) for host in settings.allowed_hosts}

   return bare_host(request.url.hostname) in allowed


def served_origin(request):
   return f"{request.url.scheme}://{request.url.netloc}".lower()


def is_cross_site(request):
   fetch_site = request.headers.get("sec-fetch-site")
   says_cross_site = fetch_site is not None and fetch_site.lower() == "cross-site"
   origin = request.headers.get("origin")
   names_an_origin = origin is not None
   names_another_origin = names_an_origin and origin.lower() != served_origin(request)

   return says_cross_site or names_another_origin


def refuse_untrusted_auth_request(request, settings):
   """None when the request may go on, otherwise the JSONResponse to return."""
   if not host_is_allowed(request, settings):
      return JSONResponse(status_code=400, content={"detail": FOREIGN_HOST_DETAIL})

   if is_cross_site(request):
      return JSONResponse(status_code=403, content={"detail": CROSS_SITE_DETAIL})

   if refuses_session_cookie(request):
      return JSONResponse(status_code=400, content={"detail": PLAIN_HTTP_DETAIL})

   return None


def refuse_rate_limited(request, settings, now=None):
   """The per-IP tier of app/auth/limiter.py: None when the request is admitted, otherwise a 429
   carrying Retry-After."""
   limiter = request.app.state.auth_limiter
   client = request.client
   key = client.host if client is not None else ""
   moment = now if now is not None else time.monotonic()
   wait = limiter.admit(key, moment, settings.auth_rate_limit_count, settings.auth_rate_limit_window_seconds)

   if wait is None:
      return None

   return JSONResponse(
      status_code=429,
      content={"detail": RATE_LIMITED_DETAIL},
      headers={"Retry-After": str(wait)},
   )
