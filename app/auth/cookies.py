"""The session cookie rule of docs/plan/09-security-and-privacy.md, "Transport and hosting".

HttpOnly and SameSite=Lax always; Secure whenever the deployment is not bound to loopback, and the
application refuses to set a Secure-less cookie on a non-loopback origin rather than downgrading.
"""
SESSION_COOKIE = "growth_session"
LOOPBACK_HOSTS = frozenset({"127.0.0.1", "::1", "localhost"})


def is_loopback(host):
   return host in LOOPBACK_HOSTS


def cookie_kwargs(bind_host, max_age):
   return {
      "key": SESSION_COOKIE,
      "httponly": True,
      "samesite": "lax",
      "secure": not is_loopback(bind_host),
      "max_age": max_age,
      "path": "/",
   }


def set_session_cookie(response, bind_host, token, max_age):
   response.set_cookie(value=token, **cookie_kwargs(bind_host, max_age))


def clear_session_cookie(response, bind_host):
   response.delete_cookie(
      key=SESSION_COOKIE,
      path="/",
      httponly=True,
      samesite="lax",
      secure=not is_loopback(bind_host),
   )
