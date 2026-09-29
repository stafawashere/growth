"""The session cookie rule of docs/plan/09-security-and-privacy.md, "Transport and hosting".

HttpOnly and SameSite=Lax always. Secure is absent only when both the configured bind host and
the request's own host (Host header / request.url.hostname) are loopback, because a loopback bind
reached through a reverse proxy or a port forward can still carry a LAN or public Host. The
application refuses outright, rather than downgrading, to set the session cookie when the request
itself arrived over plain http on a non-loopback origin, since 09 says refuse.

A browser keys cookies on the host alone, never the port, so every installation on localhost used
to share the one growth_session cookie: signing in to a second server on another port replaced the
first server's token and signed the student out of it. The name now carries the port whenever the
origin names one (growth_session_8000), and the bare name is still read, so a cookie set before the
change keeps working until the next renewal moves it to the port name.
"""
from fastapi import HTTPException

SESSION_COOKIE = "growth_session"
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})


def is_loopback(host):
   return host in LOOPBACK_HOSTS


def request_host_is_loopback(request):
   return is_loopback(request.url.hostname)


def session_cookie_name(request):
   port = request.url.port
   names_a_port = port is not None

   if not names_a_port:
      return SESSION_COOKIE

   return f"{SESSION_COOKIE}_{port}"


def read_session_token(request):
   own_name = session_cookie_name(request)
   own_token = request.cookies.get(own_name)

   if own_token:
      return own_token

   return request.cookies.get(SESSION_COOKIE)


def cookie_is_secure(bind_host, request):
   bind_is_loopback = is_loopback(bind_host)
   request_is_loopback = request_host_is_loopback(request)
   both_loopback = bind_is_loopback and request_is_loopback

   return not both_loopback


def refuses_session_cookie(request):
   request_is_loopback = request_host_is_loopback(request)
   arrived_over_plain_http = request.url.scheme != "https"

   return arrived_over_plain_http and not request_is_loopback


def cookie_kwargs(bind_host, request, max_age):
   return {
      "key": session_cookie_name(request),
      "httponly": True,
      "samesite": "lax",
      "secure": cookie_is_secure(bind_host, request),
      "max_age": max_age,
      "path": "/",
   }


def set_session_cookie(response, bind_host, request, token, max_age):
   if refuses_session_cookie(request):
      raise HTTPException(
         status_code=400,
         detail="refusing to set a session cookie over plain http on a non-loopback origin",
      )

   response.set_cookie(value=token, **cookie_kwargs(bind_host, request, max_age))


def clear_session_cookie(response, bind_host, request):
   names = {session_cookie_name(request), SESSION_COOKIE}

   for name in sorted(names):
      response.delete_cookie(
         key=name,
         path="/",
         httponly=True,
         samesite="lax",
         secure=cookie_is_secure(bind_host, request),
      )
