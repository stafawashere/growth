"""The session cookie rule of docs/plan/09-security-and-privacy.md, "Transport and hosting".

HttpOnly and SameSite=Lax always. Secure is absent only when both the configured bind host and
the request's own host (Host header / request.url.hostname) are loopback, because a loopback bind
reached through a reverse proxy or a port forward can still carry a LAN or public Host. The
application refuses outright, rather than downgrading, to set the session cookie when the request
itself arrived over plain http on a non-loopback origin, since 09 says refuse.
"""
from fastapi import HTTPException

SESSION_COOKIE = "growth_session"
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})


def is_loopback(host):
   return host in LOOPBACK_HOSTS


def request_host_is_loopback(request):
   return is_loopback(request.url.hostname)


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
      "key": SESSION_COOKIE,
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
   response.delete_cookie(
      key=SESSION_COOKIE,
      path="/",
      httponly=True,
      samesite="lax",
      secure=cookie_is_secure(bind_host, request),
   )
