"""Sends the session cookie again, with a fresh max-age, after app/api/deps.py current_session
renewed the session or read it under the bare cookie name.

A pure ASGI middleware rather than a BaseHTTPMiddleware, so a streamed response passes through
untouched, and rather than a Response parameter on the dependency, because a route that returns a
JSONResponse of its own drops the headers set on that parameter. A response that already sets or
clears a session cookie, as sign-in and sign-out do, is left alone.
"""
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import Response

from app.auth.cookies import SESSION_COOKIE, cookie_kwargs, refuses_session_cookie

SET_COOKIE = "set-cookie"


def sets_session_cookie(headers):
   cookie_headers = headers.getlist(SET_COOKIE)

   return any(value.startswith(SESSION_COOKIE) for value in cookie_headers)


def renewal_cookie_header(request, token, settings):
   carrier = Response()
   carrier.set_cookie(value=token, **cookie_kwargs(settings.bind_host, request, settings.session_ttl_seconds))

   return carrier.headers[SET_COOKIE]


class SessionRenewalMiddleware:
   def __init__(self, app):
      self.app = app

   async def __call__(self, scope, receive, send):
      is_http = scope["type"] == "http"

      if not is_http:
         await self.app(scope, receive, send)

         return

      async def send_with_renewal(message):
         is_response_start = message["type"] == "http.response.start"

         if is_response_start:
            add_renewal_cookie(scope, message)

         await send(message)

      await self.app(scope, receive, send_with_renewal)


def add_renewal_cookie(scope, message):
   state = scope.get("state") or {}
   token = state.get("renewed_session_token")
   has_renewal = token is not None

   if not has_renewal:
      return

   request = Request(scope)
   headers = MutableHeaders(scope=message)
   already_sets_cookie = sets_session_cookie(headers)
   cannot_set_cookie = refuses_session_cookie(request)
   should_skip = already_sets_cookie or cannot_set_cookie

   if should_skip:
      return

   settings = request.app.state.settings
   headers.append(SET_COOKIE, renewal_cookie_header(request, token, settings))
